from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Literal, Optional, Tuple

from pydantic import BaseModel, Field


ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ReadinessStatus = Literal["Push", "Maintain", "Modify", "Rest"]
Confidence = Literal["Low", "Medium", "High"]


def require_iso_date(value: str) -> str:
    if not ISO_DATE_RE.match(value):
        raise ValueError("date must use YYYY-MM-DD format")
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("date must be a valid calendar date") from exc
    return value


@dataclass(frozen=True)
class DailyHealth:
    date: str
    sleep_hours: Optional[float] = None
    hrv_ms: Optional[float] = None
    resting_hr_bpm: Optional[float] = None
    steps: Optional[float] = None
    weight_kg: Optional[float] = None
    source: str = "mock_apple_health"
    quality_flags: Tuple[str, ...] = ()
    raw_metrics: Tuple[str, ...] = ()


@dataclass(frozen=True)
class RecoveryDay:
    date: str
    sleep_hours: Optional[float] = None
    hrv_ms: Optional[float] = None
    resting_hr_bpm: Optional[float] = None
    steps: Optional[float] = None
    weight_kg: Optional[float] = None
    source: str = "mock_apple_health"
    quality_flags: Tuple[str, ...] = ()
    raw_metrics: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ReadinessResult:
    date: str
    score: Optional[int]
    status: str
    confidence: str
    factors: Tuple[str, ...]
    data_freshness: Tuple[str, ...]
    final_call: str


@dataclass(frozen=True)
class ImportResult:
    status: str
    files_seen: int
    rows_seen: int
    rows_inserted: int
    rows_updated: int
    rows_unchanged: int
    warnings: Tuple[str, ...] = ()
    errors: Tuple[str, ...] = ()


class ImportRequest(BaseModel):
    fixture_names: Optional[List[str]] = Field(
        default=None,
        description="Fixture file names to import. Omit to import all committed fixtures.",
    )


class ImportResultOut(BaseModel):
    status: str
    files_seen: int
    rows_seen: int
    rows_inserted: int
    rows_updated: int
    rows_unchanged: int
    warnings: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)


class RecoveryDayOut(BaseModel):
    date: str
    sleep_hours: Optional[float] = None
    hrv_ms: Optional[float] = None
    resting_hr_bpm: Optional[float] = None
    steps: Optional[float] = None
    weight_kg: Optional[float] = None
    source: str
    quality_flags: List[str] = Field(default_factory=list)
    raw_metrics: List[str] = Field(default_factory=list)


class ReadinessOut(BaseModel):
    date: str
    score: Optional[int]
    status: ReadinessStatus
    confidence: Confidence
    factors: List[str]
    data_freshness: List[str]
    final_call: ReadinessStatus


class DailyReviewOut(BaseModel):
    date: str
    recovery: Optional[RecoveryDayOut]
    readiness: Optional[ReadinessOut]
    import_health: Dict[str, object]
    review_summary: str
    missing_data: List[str]
    public_boundary: str
