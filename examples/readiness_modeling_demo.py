"""Sanitized baseline readiness-modeling example.

The private Coach Dashboard now has a small modeling layer that builds daily
features, scores readiness against personal baselines, and emits a reviewable
report. This public demo keeps that shape while using mock rows only.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Optional


@dataclass(frozen=True)
class DailyFeature:
    date: str
    sleep_hours: Optional[float]
    hrv_ms: Optional[float]
    resting_hr_bpm: Optional[float]
    energy: Optional[int]
    stress: Optional[int]
    soreness: Optional[int]
    training_day: bool
    active_kcal: Optional[float] = None
    workout_minutes: Optional[int] = None


@dataclass(frozen=True)
class BaselineResult:
    date: str
    score: int
    band: str
    data_quality: str
    limiting_factor: str
    model_notes: tuple[str, ...]
    so_what: str


def average(values: list[Optional[float]]) -> Optional[float]:
    present = [value for value in values if value is not None]
    return mean(present) if present else None


def score_sleep(hours: Optional[float]) -> tuple[Optional[float], list[str]]:
    if hours is None:
        return None, ["missing sleep"]
    if hours < 5:
        return 20.0, ["sleep under 5h"]
    if hours < 6:
        return 45.0, ["sleep between 5h and 6h"]
    if hours < 7:
        return 70.0, ["sleep slightly short"]
    if hours <= 9:
        return 95.0, []
    return 75.0, ["sleep unusually long"]


def score_hrv(value: Optional[float], baseline: Optional[float]) -> tuple[Optional[float], list[str]]:
    if value is None:
        return None, ["missing HRV"]
    if baseline is None:
        return 70.0, ["HRV present but baseline is thin"]
    ratio = value / baseline
    if ratio >= 1.0:
        return 95.0, []
    if ratio >= 0.9:
        return 75.0, ["HRV slightly below personal baseline"]
    if ratio >= 0.8:
        return 55.0, ["HRV below personal baseline"]
    return 30.0, ["HRV more than 20% below personal baseline"]


def score_resting_hr(
    value: Optional[float],
    baseline: Optional[float],
) -> tuple[Optional[float], list[str]]:
    if value is None:
        return None, ["missing resting HR"]
    if baseline is None:
        return 70.0, ["resting HR present but baseline is thin"]
    delta = value - baseline
    if delta <= 1:
        return 95.0, []
    if delta <= 4:
        return 75.0, ["resting HR slightly elevated"]
    if delta <= 8:
        return 50.0, ["resting HR elevated"]
    return 25.0, ["resting HR much higher than personal baseline"]


def score_subjective(
    energy: Optional[int],
    stress: Optional[int],
    soreness: Optional[int],
) -> tuple[Optional[float], list[str]]:
    notes: list[str] = []
    values: list[float] = []
    if energy is None:
        notes.append("missing energy")
    else:
        values.append((energy - 1) / 9 * 100)
    if stress is None:
        notes.append("missing stress")
    else:
        values.append((10 - stress) / 9 * 100)
    if soreness is None:
        notes.append("missing soreness")
    else:
        values.append((10 - soreness) / 9 * 100)
    return (mean(values) if values else None), notes


def data_quality(scored_inputs: int, missing_inputs: int, baseline_days: int) -> str:
    if scored_inputs >= 4 and missing_inputs == 0 and baseline_days >= 7:
        return "High"
    if scored_inputs >= 3 and baseline_days >= 3:
        return "Medium"
    return "Low"


def readiness_band(score: int) -> str:
    if score >= 80:
        return "Green"
    if score >= 60:
        return "Yellow"
    return "Red"


def score_day(target: DailyFeature, history: list[DailyFeature]) -> BaselineResult:
    previous = [row for row in history if row.date < target.date]
    hrv_baseline = average([row.hrv_ms for row in previous[-14:]])
    rhr_baseline = average([row.resting_hr_bpm for row in previous[-14:]])

    components: list[tuple[str, float, float]] = []
    notes: list[str] = []

    sleep_score, sleep_notes = score_sleep(target.sleep_hours)
    notes.extend(sleep_notes)
    if sleep_score is not None:
        components.append(("sleep", sleep_score, 0.30))

    hrv_score, hrv_notes = score_hrv(target.hrv_ms, hrv_baseline)
    notes.extend(hrv_notes)
    if hrv_score is not None:
        components.append(("hrv", hrv_score, 0.25))

    rhr_score, rhr_notes = score_resting_hr(target.resting_hr_bpm, rhr_baseline)
    notes.extend(rhr_notes)
    if rhr_score is not None:
        components.append(("resting_hr", rhr_score, 0.20))

    subjective_score, subjective_notes = score_subjective(
        target.energy,
        target.stress,
        target.soreness,
    )
    notes.extend(subjective_notes)
    if subjective_score is not None:
        components.append(("subjective", subjective_score, 0.25))

    if not components:
        return BaselineResult(target.date, 0, "Red", "Low", "none", ("no usable inputs",), "Do not trust today's call yet.")

    total_weight = sum(weight for _, _, weight in components)
    score = round(sum(value * weight for _, value, weight in components) / total_weight)
    limiting_factor = min(components, key=lambda item: item[1])[0]
    missing_count = sum(1 for note in notes if note.startswith("missing "))
    quality = data_quality(len(components), missing_count, len(previous))
    band = readiness_band(score)
    so_what = training_posture(band, quality, limiting_factor, target.training_day)

    return BaselineResult(
        date=target.date,
        score=score,
        band=band,
        data_quality=quality,
        limiting_factor=limiting_factor,
        model_notes=tuple(dict.fromkeys(notes)) or ("primary signals usable",),
        so_what=so_what,
    )


def training_posture(band: str, quality: str, limiting_factor: str, training_day: bool) -> str:
    if quality == "Low":
        return "Treat this as a weak signal; collect missing inputs before changing the plan."
    if band == "Green" and training_day:
        return "Good day to train as planned, while checking execution quality."
    if band == "Yellow":
        return f"Cautious training day; keep intensity flexible because {limiting_factor} is the main limiter."
    if band == "Red":
        return "Reduce intensity or bias toward recovery unless context clearly explains the signal."
    return "Maintain the plan and keep logging outcomes for calibration."


def report_lines(result: BaselineResult) -> list[str]:
    return [
        "# Baseline Readiness Report",
        f"Date: {result.date}",
        f"Score: {result.score}",
        f"Band: {result.band}",
        f"Data Quality: {result.data_quality}",
        f"Main Limiting Factor: {result.limiting_factor}",
        f"So What: {result.so_what}",
        "Model Notes: " + "; ".join(result.model_notes),
    ]


def movement_output_summary(day: DailyFeature) -> str:
    """Summarize Watch movement output without treating it as the model input."""

    if day.workout_minutes:
        return (
            f"Watch output: {day.workout_minutes} min workout, "
            f"{round(day.active_kcal or 0)} active kcal."
        )
    if day.active_kcal:
        return f"Watch output: {round(day.active_kcal)} active kcal; no workout session detail."
    return "Watch output: no movement-output rows available yet."


def sample_history() -> list[DailyFeature]:
    return [
        DailyFeature("2026-06-16", 7.3, 81, 52, 7, 4, 3, True, 420, 52),
        DailyFeature("2026-06-17", 7.6, 84, 51, 8, 3, 2, False, 280, 0),
        DailyFeature("2026-06-18", 6.9, 79, 53, 7, 4, 4, True, 510, 65),
        DailyFeature("2026-06-19", 7.2, 82, 52, 8, 3, 3, False, 300, 0),
        DailyFeature("2026-06-20", 7.8, 85, 51, 8, 2, 2, True, 540, 70),
        DailyFeature("2026-06-21", 7.1, 80, 53, 7, 4, 3, False, 260, 0),
        DailyFeature("2026-06-22", 6.8, 78, 54, 6, 5, 4, True, 470, 58),
    ]


def main() -> None:
    target = DailyFeature(
        date="2026-06-23",
        sleep_hours=6.4,
        hrv_ms=72,
        resting_hr_bpm=54,
        energy=None,
        stress=None,
        soreness=None,
        training_day=True,
        active_kcal=410,
        workout_minutes=0,
    )
    result = score_day(target, sample_history())
    print("\n".join(report_lines(result) + [movement_output_summary(target)]))


if __name__ == "__main__":
    main()
