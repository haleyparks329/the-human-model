from __future__ import annotations

import json
from datetime import date, timedelta
from typing import List, Optional, Tuple

from .db import connect, rows_to_dicts
from .models import DailyHealth, ImportResult, ReadinessResult, RecoveryDay, require_iso_date


def _pack(values: Tuple[str, ...]) -> str:
    return json.dumps(list(values), sort_keys=True)


def _unpack(value: str) -> Tuple[str, ...]:
    if not value:
        return ()
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return tuple(part.strip() for part in value.split(",") if part.strip())
    return tuple(str(item) for item in parsed)


def _recovery_from_row(row) -> RecoveryDay:
    return RecoveryDay(
        date=row["date"],
        sleep_hours=row["sleep_hours"],
        hrv_ms=row["hrv_ms"],
        resting_hr_bpm=row["resting_hr_bpm"],
        steps=row["steps"],
        weight_kg=row["weight_kg"],
        source=row["source"],
        quality_flags=_unpack(row["quality_flags"]),
        raw_metrics=_unpack(row["raw_metrics"]),
    )


def upsert_recovery_day(day: DailyHealth) -> str:
    """Persist one normalized recovery day and return insert/update/unchanged."""

    require_iso_date(day.date)
    quality_flags = _pack(day.quality_flags)
    raw_metrics = _pack(day.raw_metrics)
    values = (
        day.date,
        day.sleep_hours,
        day.hrv_ms,
        day.resting_hr_bpm,
        day.steps,
        day.weight_kg,
        day.source,
        quality_flags,
        raw_metrics,
    )
    with connect() as conn:
        existing = conn.execute(
            """
            SELECT date, sleep_hours, hrv_ms, resting_hr_bpm, steps, weight_kg,
                   source, quality_flags, raw_metrics
            FROM recovery_days
            WHERE date = ?
            """,
            (day.date,),
        ).fetchone()
        if existing is None:
            conn.execute(
                """
                INSERT INTO recovery_days (
                  date, sleep_hours, hrv_ms, resting_hr_bpm, steps, weight_kg,
                  source, quality_flags, raw_metrics
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                values,
            )
            return "inserted"

        existing_values = tuple(existing[key] for key in existing.keys())
        if existing_values == values:
            return "unchanged"

        conn.execute(
            """
            UPDATE recovery_days SET
              sleep_hours = ?,
              hrv_ms = ?,
              resting_hr_bpm = ?,
              steps = ?,
              weight_kg = ?,
              source = ?,
              quality_flags = ?,
              raw_metrics = ?,
              updated_at = CURRENT_TIMESTAMP
            WHERE date = ?
            """,
            (
                day.sleep_hours,
                day.hrv_ms,
                day.resting_hr_bpm,
                day.steps,
                day.weight_kg,
                day.source,
                quality_flags,
                raw_metrics,
                day.date,
            ),
        )
        return "updated"


def list_recovery(limit: int = 100) -> List[RecoveryDay]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM recovery_days ORDER BY date DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [_recovery_from_row(row) for row in rows]


def get_recovery(target_date: str) -> Optional[RecoveryDay]:
    require_iso_date(target_date)
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM recovery_days WHERE date = ?",
            (target_date,),
        ).fetchone()
    return _recovery_from_row(row) if row else None


def recovery_history_through(target_date: str, lookback_days: int = 30) -> List[RecoveryDay]:
    require_iso_date(target_date)
    start = (date.fromisoformat(target_date) - timedelta(days=lookback_days)).isoformat()
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT * FROM recovery_days
            WHERE date >= ? AND date <= ?
            ORDER BY date ASC
            """,
            (start, target_date),
        ).fetchall()
    return [_recovery_from_row(row) for row in rows]


def upsert_readiness_result(result: ReadinessResult) -> ReadinessResult:
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO readiness_results (
              date, score, status, confidence, factors, data_freshness, final_call, computed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(date) DO UPDATE SET
              score=excluded.score,
              status=excluded.status,
              confidence=excluded.confidence,
              factors=excluded.factors,
              data_freshness=excluded.data_freshness,
              final_call=excluded.final_call,
              computed_at=CURRENT_TIMESTAMP
            """,
            (
                result.date,
                result.score,
                result.status,
                result.confidence,
                _pack(result.factors),
                _pack(result.data_freshness),
                result.final_call,
            ),
        )
    return result


def get_readiness_result(target_date: str) -> Optional[ReadinessResult]:
    require_iso_date(target_date)
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM readiness_results WHERE date = ?",
            (target_date,),
        ).fetchone()
    if not row:
        return None
    return ReadinessResult(
        date=row["date"],
        score=row["score"],
        status=row["status"],
        confidence=row["confidence"],
        factors=_unpack(row["factors"]),
        data_freshness=_unpack(row["data_freshness"]),
        final_call=row["final_call"],
    )


def record_import_run(result: ImportResult) -> ImportResult:
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO import_runs (
              source, status, files_seen, rows_seen, rows_inserted, rows_updated,
              rows_unchanged, warnings, errors, finished_at
            ) VALUES (
              'mock_apple_health', ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP
            )
            """,
            (
                result.status,
                result.files_seen,
                result.rows_seen,
                result.rows_inserted,
                result.rows_updated,
                result.rows_unchanged,
                _pack(result.warnings),
                _pack(result.errors),
            ),
        )
    return result


def list_import_runs(limit: int = 20) -> List[dict]:
    with connect() as conn:
        rows = rows_to_dicts(
            conn.execute(
                "SELECT * FROM import_runs ORDER BY started_at DESC, id DESC LIMIT ?",
                (limit,),
            )
        )
    for row in rows:
        row["warnings"] = list(_unpack(row["warnings"]))
        row["errors"] = list(_unpack(row["errors"]))
    return rows
