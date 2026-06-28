"""Sanitized movement-quality example.

The private prototype analyzes exercise video and stores rep-level metrics for
dashboard review. This public example uses small mock angle traces to show the
same interpretation layer without copying video files, MediaPipe output, or
private training history.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, pstdev


@dataclass(frozen=True)
class RepTrace:
    rep_index: int
    hip_angles: tuple[float, ...]
    duration_seconds: float
    tracking_confidence: float


@dataclass(frozen=True)
class RepQuality:
    rep_index: int
    range_of_motion: float
    bottom_angle: float
    tempo_seconds: float
    tracking_confidence: float
    flags: tuple[str, ...]


def summarize_rep(trace: RepTrace) -> RepQuality:
    """Convert one mock joint-angle trace into dashboard-ready metrics."""

    if not trace.hip_angles:
        raise ValueError("hip_angles must include at least one sample")

    top_angle = max(trace.hip_angles)
    bottom_angle = min(trace.hip_angles)
    range_of_motion = round(top_angle - bottom_angle, 1)
    flags: list[str] = []

    if range_of_motion < 42:
        flags.append("short range of motion")
    if trace.duration_seconds < 2.2:
        flags.append("fast tempo")
    if trace.tracking_confidence < 0.75:
        flags.append("low tracking confidence")

    return RepQuality(
        rep_index=trace.rep_index,
        range_of_motion=range_of_motion,
        bottom_angle=round(bottom_angle, 1),
        tempo_seconds=trace.duration_seconds,
        tracking_confidence=trace.tracking_confidence,
        flags=tuple(flags),
    )


def set_quality_summary(reps: list[RepTrace]) -> dict:
    """Summarize a set without pretending the metrics are a final coach."""

    qualities = [summarize_rep(rep) for rep in reps]
    ranges = [quality.range_of_motion for quality in qualities]
    tempos = [quality.tempo_seconds for quality in qualities]
    all_flags = tuple(dict.fromkeys(flag for quality in qualities for flag in quality.flags))
    consistency = "stable"
    if len(ranges) > 1 and pstdev(ranges) >= 5:
        consistency = "variable range"
    if len(tempos) > 1 and pstdev(tempos) >= 0.45:
        consistency = "variable tempo"

    return {
        "rep_count": len(qualities),
        "average_range_of_motion": round(mean(ranges), 1) if ranges else None,
        "average_tempo_seconds": round(mean(tempos), 2) if tempos else None,
        "consistency": consistency,
        "needs_review": bool(all_flags),
        "flags": all_flags,
        "rep_metrics": [quality.__dict__ for quality in qualities],
        "interpretation": interpret_set(qualities, consistency),
    }


def interpret_set(qualities: list[RepQuality], consistency: str) -> str:
    if not qualities:
        return "No reps available for review."
    if any("low tracking confidence" in quality.flags for quality in qualities):
        return "Review the source video before trusting the movement signal."
    if any("short range of motion" in quality.flags for quality in qualities):
        return "Range of motion changed enough to deserve set-level review."
    if consistency != "stable":
        return "Execution varied across the set; compare against fatigue and load."
    return "Movement signal looks consistent enough to use as context."


def sample_reps() -> list[RepTrace]:
    return [
        RepTrace(1, (164, 150, 132, 118, 126, 146, 162), 2.8, 0.94),
        RepTrace(2, (163, 149, 134, 121, 130, 148, 161), 2.7, 0.91),
        RepTrace(3, (162, 151, 140, 128, 135, 150, 160), 2.1, 0.88),
    ]


def main() -> None:
    summary = set_quality_summary(sample_reps())
    for key, value in summary.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
