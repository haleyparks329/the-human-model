from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from zoneinfo import ZoneInfo

from .config import fixture_dir, timezone_name
from .models import DailyHealth, ImportResult
from .repository import record_import_run, upsert_recovery_day


# Adapted from human-model/apps/coach-dashboard/backend/app/apple_health.py.
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) ([+-]\d{4})$")
KNOWN_METRICS = {
    "sleep_analysis",
    "heart_rate_variability",
    "resting_heart_rate",
    "step_count",
    "weight_body_mass",
}


@dataclass
class _DailyHealthBucket:
    date: str
    sleep_hours: Optional[float] = None
    hrv_ms: Optional[float] = None
    resting_hr_bpm: Optional[float] = None
    steps: Optional[float] = None
    weight_kg: Optional[float] = None
    sleep_start: Optional[datetime] = None
    sleep_end: Optional[datetime] = None
    hrv_samples: List[Tuple[datetime, float]] = field(default_factory=list)
    raw_metrics: Set[str] = field(default_factory=set)
    quality_flags: Set[str] = field(default_factory=set)

    def finalize_hrv(self) -> None:
        if not self.hrv_samples:
            return
        if self.sleep_start and self.sleep_end:
            in_sleep = [
                value
                for timestamp, value in self.hrv_samples
                if self.sleep_start <= timestamp <= self.sleep_end
            ]
            if in_sleep:
                self.hrv_ms = sum(in_sleep) / len(in_sleep)
                return
        self.hrv_ms = sum(value for _, value in self.hrv_samples) / len(self.hrv_samples)
        self.quality_flags.add("hrv_daily_mean_used")

    def to_daily_health(self) -> DailyHealth:
        self.finalize_hrv()
        if self.sleep_hours is None:
            self.quality_flags.add("missing_sleep")
        if self.hrv_ms is None:
            self.quality_flags.add("missing_hrv")
        if self.resting_hr_bpm is None:
            self.quality_flags.add("missing_resting_hr")
        if not self.raw_metrics:
            self.quality_flags.add("partial_export")
        return DailyHealth(
            date=self.date,
            sleep_hours=round(self.sleep_hours, 2) if self.sleep_hours is not None else None,
            hrv_ms=round(self.hrv_ms, 1) if self.hrv_ms is not None else None,
            resting_hr_bpm=round(self.resting_hr_bpm, 1)
            if self.resting_hr_bpm is not None
            else None,
            steps=round(self.steps) if self.steps is not None else None,
            weight_kg=round(self.weight_kg, 2) if self.weight_kg is not None else None,
            quality_flags=tuple(sorted(self.quality_flags)),
            raw_metrics=tuple(sorted(self.raw_metrics)),
        )


def parse_health_datetime(value: str) -> datetime:
    match = DATE_RE.match(value)
    if match:
        date_part, time_part, offset = match.groups()
        return datetime.fromisoformat("{0}T{1}{2}:{3}".format(
            date_part,
            time_part,
            offset[:3],
            offset[3:],
        ))
    return datetime.fromisoformat(value)


def local_date(value: str) -> str:
    return parse_health_datetime(value).astimezone(ZoneInfo(timezone_name())).date().isoformat()


def _float_or_error(value: Any, field_name: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("{0} must be numeric".format(field_name)) from exc
    if parsed < 0:
        raise ValueError("{0} must be non-negative".format(field_name))
    return parsed


def _load_metrics(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    metrics = payload.get("data", {}).get("metrics")
    if not isinstance(metrics, list):
        raise ValueError("{0} does not contain data.metrics".format(path.name))
    return metrics


def aggregate_files(paths: Iterable[Path]) -> Tuple[List[DailyHealth], Tuple[str, ...]]:
    by_date: Dict[str, _DailyHealthBucket] = defaultdict(lambda: _DailyHealthBucket(date=""))
    warnings: List[str] = []

    for path in paths:
        for metric in _load_metrics(path):
            name = str(metric.get("name") or "")
            rows = metric.get("data") or []
            if name not in KNOWN_METRICS:
                warnings.append("unknown metric ignored: {0}".format(name or "(blank)"))
                continue
            if not isinstance(rows, list):
                warnings.append("metric data ignored because it is not a list: {0}".format(name))
                continue
            for entry in rows:
                date_field = entry.get("date") or entry.get("sleepStart")
                if not date_field:
                    warnings.append("metric row ignored without date: {0}".format(name))
                    continue
                day = local_date(str(date_field))
                bucket = by_date[day]
                bucket.date = day
                bucket.raw_metrics.add(name)

                if name == "sleep_analysis":
                    total = entry.get("totalSleep") if entry.get("totalSleep") is not None else entry.get("asleep")
                    if total is not None:
                        sleep_hours = _float_or_error(total, "sleep_hours")
                        if sleep_hours > 24:
                            raise ValueError("sleep_hours must be <= 24")
                        bucket.sleep_hours = sleep_hours
                    if entry.get("sleepStart"):
                        bucket.sleep_start = parse_health_datetime(str(entry["sleepStart"]))
                    if entry.get("sleepEnd"):
                        bucket.sleep_end = parse_health_datetime(str(entry["sleepEnd"]))
                elif name == "heart_rate_variability":
                    if entry.get("qty") is not None:
                        bucket.hrv_samples.append((
                            parse_health_datetime(str(date_field)),
                            _float_or_error(entry["qty"], "hrv_ms"),
                        ))
                elif name == "resting_heart_rate":
                    if entry.get("qty") is not None:
                        bucket.resting_hr_bpm = _float_or_error(entry["qty"], "resting_hr_bpm")
                elif name == "step_count":
                    bucket.steps = (bucket.steps or 0) + _float_or_error(entry.get("qty") or 0, "steps")
                elif name == "weight_body_mass":
                    if entry.get("qty") is not None:
                        bucket.weight_kg = _float_or_error(entry["qty"], "weight_kg")

    return [bucket.to_daily_health() for bucket in by_date.values()], tuple(dict.fromkeys(warnings))


def _fixture_paths(names: Optional[List[str]] = None) -> List[Path]:
    root = fixture_dir().resolve()
    if names is None:
        return sorted(root.glob("*.json"))
    paths = []
    for name in names:
        requested = Path(name)
        if (
            requested.is_absolute()
            or requested.name != name
            or "\\" in name
            or name in {"", ".", ".."}
            or not name.endswith(".json")
        ):
            raise FileNotFoundError("Invalid fixture name: {0}".format(name))
        path = (root / name).resolve()
        if path.parent != root or not path.is_file():
            raise FileNotFoundError("Fixture not found: {0}".format(name))
        paths.append(path)
    return paths


def import_mock_health_export(fixture_names: Optional[List[str]] = None) -> ImportResult:
    try:
        paths = _fixture_paths(fixture_names)
    except FileNotFoundError as exc:
        result = ImportResult("blocked", 0, 0, 0, 0, 0, errors=(str(exc),))
        return record_import_run(result)

    if not paths:
        result = ImportResult("blocked", 0, 0, 0, 0, 0, errors=("No fixture files found",))
        return record_import_run(result)

    try:
        days, warnings = aggregate_files(paths)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        result = ImportResult(
            status="error",
            files_seen=len(paths),
            rows_seen=0,
            rows_inserted=0,
            rows_updated=0,
            rows_unchanged=0,
            errors=(str(exc),),
        )
        return record_import_run(result)

    inserted = updated = unchanged = 0
    for day in days:
        action = upsert_recovery_day(day)
        if action == "inserted":
            inserted += 1
        elif action == "updated":
            updated += 1
        else:
            unchanged += 1

    result = ImportResult(
        status="ok",
        files_seen=len(paths),
        rows_seen=len(days),
        rows_inserted=inserted,
        rows_updated=updated,
        rows_unchanged=unchanged,
        warnings=warnings,
    )
    return record_import_run(result)
