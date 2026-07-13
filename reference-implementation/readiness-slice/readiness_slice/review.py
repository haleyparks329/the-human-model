from __future__ import annotations

from typing import Dict, List, Optional

from .models import DailyReviewOut, ReadinessOut, RecoveryDayOut
from .readiness import calculate_readiness
from .repository import (
    get_readiness_result,
    get_recovery,
    list_import_runs,
    recovery_history_through,
    upsert_readiness_result,
)


PUBLIC_BOUNDARY_NOTE = (
    "Public reference slice: uses synthetic Apple Health-style fixtures only; "
    "no Telegram, Notion, private health exports, local device paths, or real user data."
)


def recovery_to_out(row) -> RecoveryDayOut:
    return RecoveryDayOut(
        date=row.date,
        sleep_hours=row.sleep_hours,
        hrv_ms=row.hrv_ms,
        resting_hr_bpm=row.resting_hr_bpm,
        steps=row.steps,
        weight_kg=row.weight_kg,
        source=row.source,
        quality_flags=list(row.quality_flags),
        raw_metrics=list(row.raw_metrics),
    )


def readiness_to_out(row) -> ReadinessOut:
    return ReadinessOut(
        date=row.date,
        score=row.score,
        status=row.status,
        confidence=row.confidence,
        factors=list(row.factors),
        data_freshness=list(row.data_freshness),
        final_call=row.final_call,
    )


def compute_and_store_readiness(target_date: str):
    history = recovery_history_through(target_date)
    target = next((row for row in history if row.date == target_date), None)
    if target is None:
        raise LookupError("Recovery day not found for {0}".format(target_date))
    return upsert_readiness_result(calculate_readiness(target, history))


def get_or_compute_readiness(target_date: str):
    existing = get_readiness_result(target_date)
    if existing:
        return existing
    return compute_and_store_readiness(target_date)


def missing_data_for_recovery(recovery) -> List[str]:
    missing = []
    if recovery.sleep_hours is None:
        missing.append("sleep")
    if recovery.hrv_ms is None:
        missing.append("hrv")
    if recovery.resting_hr_bpm is None:
        missing.append("resting_hr")
    return missing


def _import_health_summary() -> Dict[str, object]:
    latest = list_import_runs(limit=1)
    if not latest:
        return {"status": "not_run", "message": "No mock health imports have run yet."}
    row = latest[0]
    return {
        "status": row["status"],
        "files_seen": row["files_seen"],
        "rows_seen": row["rows_seen"],
        "rows_inserted": row["rows_inserted"],
        "rows_updated": row["rows_updated"],
        "rows_unchanged": row["rows_unchanged"],
        "warnings": row["warnings"],
        "errors": row["errors"],
    }


def daily_review_for_date(target_date: str) -> DailyReviewOut:
    recovery = get_recovery(target_date)
    if recovery is None:
        raise LookupError("Recovery day not found for {0}".format(target_date))
    readiness = get_or_compute_readiness(target_date)
    missing = missing_data_for_recovery(recovery)
    if readiness.score is None:
        summary = "No reliable readiness score yet; import more recovery signals."
    else:
        summary = "{0}: {1}/100 readiness with {2} confidence.".format(
            readiness.status,
            readiness.score,
            readiness.confidence.lower(),
        )
    if missing:
        summary += " Missing: {0}.".format(", ".join(missing))

    return DailyReviewOut(
        date=target_date,
        recovery=recovery_to_out(recovery),
        readiness=readiness_to_out(readiness),
        import_health=_import_health_summary(),
        review_summary=summary,
        missing_data=missing,
        public_boundary=PUBLIC_BOUNDARY_NOTE,
    )
