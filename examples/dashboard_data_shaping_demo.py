"""Sanitized Coach Dashboard data-shaping example.

The private dashboard turns noisy recovery, training, body-measurement, and
import records into compact review payloads. This public demo uses mock rows to
show that aggregation layer without exposing Notion IDs, health exports, local
paths, or private training history.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional


@dataclass(frozen=True)
class BodyMetric:
    date: str
    metric_name: str
    value: float
    unit: str
    source: str = "mock"


@dataclass(frozen=True)
class TrainingSet:
    exercise: str
    set_index: int
    reps: Optional[float]
    weight_kg: Optional[float]
    load_label: str = ""
    parse_warnings: tuple[str, ...] = ()


@dataclass(frozen=True)
class TrainingSession:
    date: str
    session_name: str
    sets: tuple[TrainingSet, ...]
    source: str = "mock"


@dataclass(frozen=True)
class ImportRun:
    source: str
    status: str
    rows_seen: int
    rows_changed: int
    message: str = ""


def body_trends(rows: list[BodyMetric]) -> list[dict]:
    """Return latest value, previous value, delta, and direction per metric."""

    by_metric: dict[str, list[BodyMetric]] = defaultdict(list)
    for row in rows:
        by_metric[row.metric_name].append(row)

    trends: list[dict] = []
    for metric_name, metric_rows in sorted(by_metric.items()):
        ordered = sorted(metric_rows, key=lambda row: row.date, reverse=True)
        current = ordered[0]
        previous = ordered[1] if len(ordered) > 1 else None
        previous_value = previous.value if previous else None
        delta = round(current.value - previous_value, 2) if previous_value is not None else None
        if delta is None:
            direction = "new"
        elif abs(delta) < 0.05:
            direction = "flat"
        elif delta > 0:
            direction = "up"
        else:
            direction = "down"
        trends.append(
            {
                "metric_name": metric_name,
                "date": current.date,
                "value": current.value,
                "unit": current.unit,
                "previous_date": previous.date if previous else None,
                "previous_value": previous_value,
                "delta": delta,
                "direction": direction,
                "source": current.source,
            }
        )
    return trends


def training_session_summary(session: TrainingSession) -> dict:
    """Summarize a session into dashboard-ready output fields."""

    volume_load = 0.0
    work_set_count = 0
    warnings: list[str] = []
    muscle_groups = set()

    for item in session.sets:
        if item.reps is not None and item.weight_kg is not None:
            volume_load += item.reps * item.weight_kg
            work_set_count += 1
        elif item.load_label:
            warnings.append(f"{item.exercise}: qualitative load '{item.load_label}'")
        warnings.extend(f"{item.exercise}: {warning}" for warning in item.parse_warnings)
        group = infer_muscle_group(item.exercise)
        if group:
            muscle_groups.add(group)

    return {
        "date": session.date,
        "session_name": session.session_name,
        "exercise_count": len({item.exercise for item in session.sets}),
        "work_set_count": work_set_count,
        "volume_load": round(volume_load, 1),
        "muscle_groups": tuple(sorted(muscle_groups)),
        "needs_review": bool(warnings),
        "review_warnings": tuple(dict.fromkeys(warnings)),
        "source": session.source,
    }


def weekly_volume(sessions: list[TrainingSession], anchor_date: str) -> dict:
    anchor = date.fromisoformat(anchor_date)
    monday = anchor - timedelta(days=anchor.weekday())
    week_dates = {(monday + timedelta(days=offset)).isoformat() for offset in range(7)}
    summaries = [
        training_session_summary(session)
        for session in sessions
        if session.date in week_dates
    ]

    by_group: dict[str, int] = defaultdict(int)
    for summary in summaries:
        for group in summary["muscle_groups"]:
            by_group[group] += 1

    return {
        "session_count": len(summaries),
        "work_sets": sum(summary["work_set_count"] for summary in summaries),
        "volume_load": round(sum(summary["volume_load"] for summary in summaries), 1),
        "muscle_group_counts": dict(sorted(by_group.items())),
    }


def progression_signals(sessions: list[TrainingSession]) -> list[dict]:
    by_exercise: dict[str, list[tuple[str, float]]] = defaultdict(list)
    for session in sessions:
        for item in session.sets:
            if item.reps is None or item.weight_kg is None:
                continue
            by_exercise[item.exercise].append((session.date, item.reps * item.weight_kg))

    signals: list[dict] = []
    for exercise, rows in by_exercise.items():
        by_date: dict[str, float] = defaultdict(float)
        for row_date, volume in rows:
            by_date[row_date] += volume
        ordered = sorted(by_date.items(), key=lambda row: row[0], reverse=True)
        current_date, current_volume = ordered[0]
        previous_volume = ordered[1][1] if len(ordered) > 1 else None
        volume_delta = (
            round(current_volume - previous_volume, 1)
            if previous_volume is not None
            else None
        )
        signals.append(
            {
                "exercise": exercise,
                "date": current_date,
                "volume_load": round(current_volume, 1),
                "volume_delta": volume_delta,
                "status": "new baseline"
                if previous_volume is None
                else "up"
                if volume_delta and volume_delta > 0
                else "steady",
            }
        )

    return sorted(signals, key=lambda signal: abs(signal["volume_delta"] or 0), reverse=True)


def infer_muscle_group(exercise_name: str) -> str:
    text = exercise_name.lower()
    rules = (
        ("glutes", ("glute", "hip thrust", "abduction", "kickback")),
        ("hamstrings", ("hamstring", "leg curl", "rdl", "romanian", "back extension")),
        ("quads", ("squat", "leg press", "leg extension", "lunge")),
        ("shoulders", ("shoulder", "delt", "lateral raise")),
        ("chest", ("bench", "press", "fly")),
        ("back", ("row", "pulldown", "pull-up", "lat pulldown")),
        ("biceps", ("curl", "bicep")),
        ("triceps", ("tricep", "pushdown", "skullcrusher", "overhead extension")),
        ("calves", ("calf", "calves")),
        ("core", ("plank", "crunch", "abs", "core")),
    )
    for group, terms in rules:
        if any(term in text for term in terms):
            return group
    return ""


def signal_health(imports: list[ImportRun]) -> dict:
    blocked = [run for run in imports if run.status in {"blocked", "error"}]
    return {
        "sources": len({run.source for run in imports}),
        "rows_seen": sum(run.rows_seen for run in imports),
        "rows_changed": sum(run.rows_changed for run in imports),
        "blocked_sources": tuple(run.source for run in blocked),
        "status": "Needs review" if blocked else "OK",
    }


def dashboard_payload(
    body_rows: list[BodyMetric],
    sessions: list[TrainingSession],
    imports: list[ImportRun],
    anchor_date: str = "2026-06-18",
) -> dict:
    """Create the compact payload a dashboard or Bridget card could consume."""

    session_summaries = [training_session_summary(session) for session in sessions]
    latest_session = session_summaries[0] if session_summaries else None
    return {
        "body_trends": body_trends(body_rows),
        "latest_training": latest_session,
        "weekly_volume": weekly_volume(sessions, anchor_date),
        "progression_signals": progression_signals(sessions),
        "signals": signal_health(imports),
        "daily_review_hint": review_hint(latest_session, imports),
    }


def review_hint(latest_session: Optional[dict], imports: list[ImportRun]) -> str:
    if any(run.status in {"blocked", "error"} for run in imports):
        return "Check import health before trusting today's call."
    if latest_session and latest_session["needs_review"]:
        return "Training parsed with warnings; review the log before modeling load."
    if latest_session and latest_session["volume_load"] > 0:
        return "Training load is structured enough for a lightweight readiness context."
    return "Waiting for enough structured rows to summarize."


def sample_body_rows() -> list[BodyMetric]:
    return [
        BodyMetric("2026-06-01", "waist_cm", 73.2, "cm"),
        BodyMetric("2026-06-15", "waist_cm", 72.6, "cm"),
        BodyMetric("2026-06-01", "weight_kg", 66.4, "kg"),
        BodyMetric("2026-06-15", "weight_kg", 66.5, "kg"),
    ]


def sample_sessions() -> list[TrainingSession]:
    return [
        TrainingSession(
            date="2026-06-18",
            session_name="Upper body",
            sets=(
                TrainingSet("Bench press", 1, 8, 57.5),
                TrainingSet("Bench press", 2, 8, 60),
                TrainingSet("Machine row", 1, 10, 45),
                TrainingSet("Lateral raise", 1, None, None, "unclear OCR", ("reps missing",)),
            ),
        ),
        TrainingSession(
            date="2026-06-17",
            session_name="Lower body",
            sets=(
                TrainingSet("Hip thrust", 1, 10, 90),
                TrainingSet("Hip thrust", 2, 8, 95),
                TrainingSet("Leg press", 1, 12, 140),
                TrainingSet("Back extension", 1, 12, None, "bodyweight"),
            ),
        ),
        TrainingSession(
            date="2026-06-15",
            session_name="Upper body",
            sets=(
                TrainingSet("Bench press", 1, 8, 55),
                TrainingSet("Bench press", 2, 8, 57.5),
                TrainingSet("Machine row", 1, 10, 42.5),
            ),
        ),
    ]


def sample_imports() -> list[ImportRun]:
    return [
        ImportRun("apple_health", "OK".lower(), 4, 3),
        ImportRun("notion_training", "OK".lower(), 12, 4),
    ]


def main() -> None:
    payload = dashboard_payload(sample_body_rows(), sample_sessions(), sample_imports())
    for key, value in payload.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
