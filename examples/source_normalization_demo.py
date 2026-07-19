"""Public-safe source normalization demo.

The private Human Model foundation now has focused PostgreSQL loaders for
several formerly separate Notion data sources. This example uses tiny mock rows
to show the product behavior that matters publicly: each source becomes a
typed, reviewable record, and missing or duplicated source data stays visible
instead of being hidden by the dashboard layer.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Optional


@dataclass(frozen=True)
class SourceRow:
    source: str
    source_id: str
    date: str
    fields: dict[str, object]


@dataclass(frozen=True)
class CanonicalRecord:
    source: str
    source_id: str
    record_date: str
    record_type: str
    numeric_fields: dict[str, Decimal]
    text_fields: dict[str, str]
    review_notes: tuple[str, ...] = ()


SOURCE_RECORD_TYPES = {
    "body_measurements": "body_measurement_session",
    "nutrition": "daily_nutrition",
    "weekly_checkin": "weekly_coach_checkin",
    "training_log": "training_session",
    "training_plan": "training_plan_day",
}

NUMERIC_FIELDS = {
    "weight_kg",
    "waist_cm",
    "calories_kcal",
    "protein_g",
    "carbs_g",
    "fat_g",
    "sets",
    "reps",
    "load_kg",
}


def normalize_rows(rows: list[SourceRow]) -> list[CanonicalRecord]:
    """Convert mock source rows into typed records for review."""

    normalized = [_normalize_row(row) for row in rows]
    duplicate_keys = _duplicate_keys(normalized)
    if not duplicate_keys:
        return normalized

    with_notes: list[CanonicalRecord] = []
    for record in normalized:
        key = (record.source, record.record_date, record.record_type)
        if key in duplicate_keys:
            with_notes.append(
                CanonicalRecord(
                    record.source,
                    record.source_id,
                    record.record_date,
                    record.record_type,
                    record.numeric_fields,
                    record.text_fields,
                    (*record.review_notes, "duplicate source date retained for review"),
                )
            )
        else:
            with_notes.append(record)
    return with_notes


def source_coverage(records: list[CanonicalRecord]) -> dict:
    """Return a dashboard-friendly source coverage report."""

    by_source = Counter(record.source for record in records)
    review_notes = [
        f"{record.source}:{record.source_id}: {note}"
        for record in records
        for note in record.review_notes
    ]
    dates_by_source: dict[str, set[str]] = defaultdict(set)
    for record in records:
        dates_by_source[record.source].add(record.record_date)

    missing_sources = sorted(set(SOURCE_RECORD_TYPES) - set(by_source))
    return {
        "source_counts": dict(sorted(by_source.items())),
        "date_ranges": {
            source: (min(dates), max(dates))
            for source, dates in sorted(dates_by_source.items())
        },
        "missing_sources": missing_sources,
        "review_notes": tuple(review_notes),
        "ready_for_dashboard": not missing_sources,
    }


def dashboard_source_payload(records: list[CanonicalRecord]) -> dict:
    """Create the compact payload a dashboard source-health card could use."""

    coverage = source_coverage(records)
    return {
        "canonical_record_count": len(records),
        "coverage": coverage,
        "latest_training_date": _latest_date(
            record.record_date for record in records if record.source == "training_log"
        ),
        "private_data_policy": "mock rows only; no Notion IDs, secrets, or health exports",
    }


def sample_source_rows() -> list[SourceRow]:
    return [
        SourceRow(
            "body_measurements",
            "mock-body-1",
            "2026-07-01",
            {"weight_kg": "72.4", "waist_cm": "73.2", "notes": "morning check"},
        ),
        SourceRow(
            "nutrition",
            "mock-nutrition-1",
            "2026-07-01",
            {"calories_kcal": "1825", "protein_g": "142.5", "carbs_g": None, "fat_g": "61"},
        ),
        SourceRow(
            "weekly_checkin",
            "mock-checkin-1",
            "2026-07-05",
            {"mood": "steady", "training_reflection": "good recovery after deload"},
        ),
        SourceRow(
            "training_log",
            "mock-training-1",
            "2026-07-06",
            {"exercise": "RDL", "sets": "3", "reps": "8", "load_kg": "80"},
        ),
        SourceRow(
            "training_log",
            "mock-training-2",
            "2026-07-06",
            {"exercise": "RDL backoff", "sets": "2", "reps": "10", "load_kg": "65"},
        ),
        SourceRow(
            "training_plan",
            "mock-plan-1",
            "2026-07-08",
            {"planned_workout": "Glutes and hamstrings", "notes": "mock planned day"},
        ),
    ]


def _normalize_row(row: SourceRow) -> CanonicalRecord:
    if row.source not in SOURCE_RECORD_TYPES:
        raise ValueError(f"Unsupported source: {row.source}")
    _parse_date(row.date)

    numeric_fields: dict[str, Decimal] = {}
    text_fields: dict[str, str] = {}
    notes: list[str] = []
    for key, value in row.fields.items():
        if value in (None, ""):
            notes.append(f"{key} missing")
        elif key in NUMERIC_FIELDS:
            numeric_fields[key] = _decimal(value, key)
        else:
            text_fields[key] = str(value)

    return CanonicalRecord(
        source=row.source,
        source_id=row.source_id,
        record_date=row.date,
        record_type=SOURCE_RECORD_TYPES[row.source],
        numeric_fields=numeric_fields,
        text_fields=text_fields,
        review_notes=tuple(notes),
    )


def _decimal(value: object, field_name: str) -> Decimal:
    try:
        return Decimal(str(value))
    except InvalidOperation as error:
        raise ValueError(f"{field_name} must be numeric: {value}") from error


def _parse_date(value: str) -> None:
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as error:
        raise ValueError(f"Unsupported date format: {value}") from error


def _duplicate_keys(records: list[CanonicalRecord]) -> set[tuple[str, str, str]]:
    counts = Counter((record.source, record.record_date, record.record_type) for record in records)
    return {key for key, count in counts.items() if count > 1}


def _latest_date(values) -> Optional[str]:
    dates = list(values)
    return max(dates) if dates else None


if __name__ == "__main__":
    payload = dashboard_source_payload(normalize_rows(sample_source_rows()))
    for key, value in payload.items():
        print(f"{key}: {value}")
