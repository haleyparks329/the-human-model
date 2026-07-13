from __future__ import annotations

from typing import List, Optional, Tuple

from .models import ReadinessResult, RecoveryDay


RED_FLAG_TERMS = (
    "ill",
    "sick",
    "pain",
    "injury",
    "injured",
    "fatigue",
    "exhausted",
    "sore",
    "travel",
    "hangover",
)


def _avg(values: List[float]) -> Optional[float]:
    return sum(values) / len(values) if values else None


def _linear(value: float, low: float, high: float) -> float:
    if high == low:
        return 100.0
    return max(0.0, min(100.0, (value - low) / (high - low) * 100.0))


def _hrv_score(value: float, baseline: Optional[float]) -> Tuple[float, Optional[str]]:
    if not baseline:
        return 75.0, "HRV present but baseline is thin"
    ratio = value / baseline
    if ratio >= 1.0:
        return 100.0, None
    if ratio >= 0.9:
        return 80.0, "HRV slightly below baseline"
    if ratio >= 0.8:
        return 55.0, "HRV below baseline"
    return 25.0, "HRV well below baseline"


def _rhr_score(value: float, baseline: Optional[float]) -> Tuple[float, Optional[str]]:
    if not baseline:
        return 75.0, "Resting HR present but baseline is thin"
    delta = value - baseline
    if delta <= 1:
        return 100.0, None
    if delta <= 4:
        return 75.0, "Resting HR slightly elevated"
    if delta <= 8:
        return 45.0, "Resting HR elevated"
    return 20.0, "Resting HR much higher than baseline"


def _confidence(available_count: int, baseline_count: int, missing_critical: List[str]) -> str:
    if available_count < 3 or baseline_count < 3 or missing_critical:
        return "Low"
    if available_count < 4 or baseline_count < 7:
        return "Medium"
    return "High"


def calculate_readiness(target: RecoveryDay, history: List[RecoveryDay]) -> ReadinessResult:
    """Transparent readiness score adapted from the private Coach Dashboard model.

    Public-slice change: this version scores only Apple Health recovery signals.
    It intentionally excludes Telegram/manual check-ins and training context.
    """

    previous = [row for row in history if row.date < target.date]
    baseline_rows = sorted(previous, key=lambda row: row.date, reverse=True)[:14]
    hrv_baseline = _avg([row.hrv_ms for row in baseline_rows if row.hrv_ms is not None])
    rhr_baseline = _avg(
        [row.resting_hr_bpm for row in baseline_rows if row.resting_hr_bpm is not None]
    )

    components: List[Tuple[str, float, float]] = []
    factors: List[str] = []
    red_flags: List[str] = []

    if target.sleep_hours is not None:
        components.append(("sleep", _linear(target.sleep_hours, 4.0, 8.0), 0.35))
        if target.sleep_hours < 5:
            red_flags.append("sleep under 5h")
        elif target.sleep_hours < 6:
            factors.append("sleep is short")
    else:
        factors.append("sleep missing")

    if target.hrv_ms is not None:
        score, factor = _hrv_score(target.hrv_ms, hrv_baseline)
        components.append(("hrv", score, 0.35))
        if factor:
            factors.append(factor)
        if hrv_baseline and target.hrv_ms < hrv_baseline * 0.8:
            red_flags.append("HRV well below baseline")
    else:
        factors.append("HRV missing")

    if target.resting_hr_bpm is not None:
        score, factor = _rhr_score(target.resting_hr_bpm, rhr_baseline)
        components.append(("resting_hr", score, 0.30))
        if factor:
            factors.append(factor)
        if rhr_baseline and target.resting_hr_bpm > rhr_baseline + 8:
            red_flags.append("resting HR much higher than baseline")
    else:
        factors.append("resting HR missing")

    if "missing_sleep" in target.quality_flags and "sleep missing" not in factors:
        factors.append("sleep missing")
    if "hrv_daily_mean_used" in target.quality_flags:
        factors.append("HRV used daily mean because no sleep window was available")
    if "partial_export" in target.quality_flags:
        factors.append("partial Apple Health export")

    score: Optional[int]
    if components:
        total_weight = sum(weight for _, _, weight in components)
        score = round(sum(value * weight for _, value, weight in components) / total_weight)
    else:
        score = None

    present = {name for name, _, _ in components}
    missing_critical = [
        name for name in ("sleep", "hrv", "resting_hr") if name not in present
    ]
    for missing in missing_critical:
        red_flags.append("missing critical data: {0}".format(missing))

    if score is None:
        status = "Modify"
    elif score >= 80:
        status = "Push"
    elif score >= 65:
        status = "Maintain"
    elif score >= 50:
        status = "Modify"
    else:
        status = "Rest"

    if red_flags:
        if score is not None and score < 50:
            status = "Rest"
        elif status == "Push":
            status = "Maintain"
        elif status == "Maintain":
            status = "Modify"

    confidence = _confidence(len(components), len(baseline_rows), missing_critical)
    data_freshness = [
        "{0} scored inputs".format(len(components)),
        "{0} baseline days".format(len(baseline_rows)),
        "source {0}".format(target.source),
    ]
    if missing_critical:
        data_freshness.append("missing " + ", ".join(missing_critical))

    factor_text = tuple(dict.fromkeys(red_flags + factors)) or ("all primary signals look usable",)
    return ReadinessResult(
        date=target.date,
        score=score,
        status=status,
        confidence=confidence,
        factors=factor_text,
        data_freshness=tuple(data_freshness),
        final_call=status,
    )
