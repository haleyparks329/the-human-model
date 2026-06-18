"""Sanitized readiness scoring example for The Human Model.

This demo mirrors the shape of the private readiness pipeline without Notion,
Apple Health exports, private records, or live writeback. It combines objective
signals, subjective check-in data, recent training context, and confidence
metadata into a simple daily training call.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Optional


@dataclass(frozen=True)
class RecoveryDay:
    date: str
    sleep_hours: Optional[float] = None
    hrv_ms: Optional[float] = None
    resting_hr_bpm: Optional[float] = None
    energy: Optional[float] = None
    stress: Optional[float] = None
    mood: Optional[str] = None
    notes: str = ""


@dataclass(frozen=True)
class TrainingContext:
    trained_yesterday: bool = False
    workout_days_7d: int = 0
    notes: str = ""


@dataclass(frozen=True)
class ReadinessResult:
    score: Optional[int]
    status: str
    confidence: str
    factors: tuple[str, ...]


MOOD_SCORES = {
    "Great": 100.0,
    "Good": 85.0,
    "Okay": 65.0,
    "Low": 35.0,
    "Bad": 10.0,
}

RED_FLAG_TERMS = ("sick", "pain", "injury", "exhausted", "sore")


def _linear(value: float, low: float, high: float) -> float:
    if high == low:
        return 100.0
    return max(0.0, min(100.0, (value - low) / (high - low) * 100.0))


def _average(values: list[float]) -> Optional[float]:
    return mean(values) if values else None


def _hrv_score(value: float, baseline: Optional[float]) -> tuple[float, Optional[str]]:
    if baseline is None:
        return 75.0, "HRV present but baseline is thin"
    ratio = value / baseline
    if ratio >= 1.0:
        return 100.0, None
    if ratio >= 0.9:
        return 80.0, "HRV slightly below baseline"
    if ratio >= 0.8:
        return 55.0, "HRV below baseline"
    return 25.0, "HRV well below baseline"


def _resting_hr_score(value: float, baseline: Optional[float]) -> tuple[float, Optional[str]]:
    if baseline is None:
        return 75.0, "Resting HR present but baseline is thin"
    delta = value - baseline
    if delta <= 1:
        return 100.0, None
    if delta <= 4:
        return 75.0, "Resting HR slightly elevated"
    if delta <= 8:
        return 45.0, "Resting HR elevated"
    return 20.0, "Resting HR much higher than baseline"


def _training_component(context: TrainingContext) -> tuple[float, list[str]]:
    score = 85.0
    factors: list[str] = []
    if context.trained_yesterday:
        score -= 15
        factors.append("trained yesterday")
    if context.workout_days_7d >= 5:
        score -= 15
        factors.append(f"{context.workout_days_7d} training days in the last 7 days")
    if "needs review" in context.notes.lower():
        score -= 5
        factors.append("training log has review warnings")
    return max(30.0, min(100.0, score)), factors


def calculate_readiness(
    target: RecoveryDay,
    history: list[RecoveryDay],
    training: TrainingContext,
) -> ReadinessResult:
    previous = [row for row in history if row.date < target.date]
    hrv_baseline = _average([row.hrv_ms for row in previous if row.hrv_ms is not None])
    rhr_baseline = _average(
        [row.resting_hr_bpm for row in previous if row.resting_hr_bpm is not None]
    )

    components: list[tuple[str, float, float]] = []
    factors: list[str] = []
    red_flags: list[str] = []

    if target.sleep_hours is not None:
        components.append(("sleep", _linear(target.sleep_hours, 4.0, 8.0), 0.25))
        if target.sleep_hours < 5:
            red_flags.append("sleep under 5h")
    else:
        factors.append("sleep missing")

    if target.hrv_ms is not None:
        score, factor = _hrv_score(target.hrv_ms, hrv_baseline)
        components.append(("hrv", score, 0.20))
        if factor:
            factors.append(factor)
    else:
        factors.append("HRV missing")

    if target.resting_hr_bpm is not None:
        score, factor = _resting_hr_score(target.resting_hr_bpm, rhr_baseline)
        components.append(("resting_hr", score, 0.15))
        if factor:
            factors.append(factor)
    else:
        factors.append("resting HR missing")

    if target.energy is not None:
        components.append(("energy", _linear(target.energy, 1.0, 10.0), 0.15))
        if target.energy <= 3:
            red_flags.append("energy 3 or lower")
    else:
        factors.append("energy missing")

    if target.stress is not None:
        components.append(("stress", _linear(11.0 - target.stress, 1.0, 10.0), 0.10))
        if target.stress >= 8:
            red_flags.append("stress 8 or higher")
    else:
        factors.append("stress missing")

    if target.mood:
        components.append(("mood", MOOD_SCORES.get(target.mood, 60.0), 0.05))
        if target.mood == "Bad":
            red_flags.append("mood is Bad")
    else:
        factors.append("mood missing")

    training_score, training_factors = _training_component(training)
    components.append(("training", training_score, 0.10))
    factors.extend(training_factors)

    lowered_notes = target.notes.lower()
    note_flags = [term for term in RED_FLAG_TERMS if term in lowered_notes]
    if note_flags:
        red_flags.append("notes mention " + ", ".join(note_flags[:3]))

    if not components:
        return ReadinessResult(None, "Modify", "Low", ("no scored inputs",))

    total_weight = sum(weight for _, _, weight in components)
    score = round(sum(value * weight for _, value, weight in components) / total_weight)

    if score >= 80:
        status = "Push"
    elif score >= 65:
        status = "Maintain"
    elif score >= 50:
        status = "Modify"
    else:
        status = "Rest"

    if red_flags:
        if status == "Push":
            status = "Maintain"
        elif status == "Maintain":
            status = "Modify"
        if "energy 3 or lower" in red_flags or "mood is Bad" in red_flags:
            status = "Rest"

    scored_inputs = {name for name, _, _ in components}
    missing_critical = [
        name for name in ("sleep", "energy", "stress", "mood") if name not in scored_inputs
    ]
    if missing_critical or len(previous) < 3:
        confidence = "Low"
    elif len(scored_inputs) < 6 or len(previous) < 7:
        confidence = "Medium"
    else:
        confidence = "High"

    return ReadinessResult(
        score=score,
        status=status,
        confidence=confidence,
        factors=tuple(dict.fromkeys(red_flags + factors)) or ("primary signals usable",),
    )


def sample_history() -> list[RecoveryDay]:
    return [
        RecoveryDay("2026-06-10", 7.4, 80, 52, 7, 4, "Good"),
        RecoveryDay("2026-06-11", 7.1, 82, 51, 8, 3, "Good"),
        RecoveryDay("2026-06-12", 6.9, 78, 53, 7, 4, "Okay"),
        RecoveryDay("2026-06-13", 7.8, 84, 51, 8, 3, "Great"),
        RecoveryDay("2026-06-14", 7.2, 79, 52, 7, 4, "Good"),
        RecoveryDay("2026-06-15", 7.5, 81, 52, 8, 3, "Good"),
        RecoveryDay("2026-06-16", 7.0, 80, 53, 7, 4, "Okay"),
    ]


def main() -> None:
    target = RecoveryDay(
        date="2026-06-17",
        sleep_hours=7.6,
        hrv_ms=83,
        resting_hr_bpm=52,
        energy=8,
        stress=3,
        mood="Good",
    )
    result = calculate_readiness(
        target,
        sample_history(),
        TrainingContext(trained_yesterday=True, workout_days_7d=4),
    )
    print(result)


if __name__ == "__main__":
    main()
