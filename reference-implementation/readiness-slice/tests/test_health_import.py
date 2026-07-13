from __future__ import annotations

import json

from readiness_slice.db import connect
from readiness_slice.health_import import import_mock_health_export, parse_health_datetime
from readiness_slice.repository import get_recovery


def _minimal_fixture(sleep_hours: float = 7.0) -> dict:
    return {
        "data": {
            "metrics": [
                {
                    "name": "sleep_analysis",
                    "data": [
                        {
                            "sleepStart": "2026-06-18 00:30:00 +0200",
                            "sleepEnd": "2026-06-18 07:30:00 +0200",
                            "totalSleep": sleep_hours,
                        }
                    ],
                },
                {
                    "name": "heart_rate_variability",
                    "data": [{"date": "2026-06-18 06:30:00 +0200", "qty": 80}],
                },
                {
                    "name": "resting_heart_rate",
                    "data": [{"date": "2026-06-18 06:30:00 +0200", "qty": 52}],
                },
            ]
        }
    }


def test_parse_health_datetime_accepts_health_auto_export_offset():
    parsed = parse_health_datetime("2026-06-18 06:30:00 +0200")

    assert parsed.isoformat() == "2026-06-18T06:30:00+02:00"


def test_import_complete_fixture_normalizes_recovery_day():
    result = import_mock_health_export(["health_export_recovery_complete.json"])

    assert result.status == "ok"
    assert result.files_seen == 1
    assert result.rows_inserted == 6
    row = get_recovery("2026-06-18")
    assert row is not None
    assert row.sleep_hours == 7.6
    assert row.hrv_ms == 84.0
    assert row.resting_hr_bpm == 51.0
    assert row.steps == 7100
    assert row.weight_kg == 68.3
    assert row.source == "mock_apple_health"
    assert "sleep_analysis" in row.raw_metrics


def test_import_missing_sleep_sets_quality_flag_not_failure():
    result = import_mock_health_export(["health_export_missing_sleep.json"])

    assert result.status == "ok"
    row = get_recovery("2026-06-23")
    assert row is not None
    assert row.sleep_hours is None
    assert "missing_sleep" in row.quality_flags
    assert row.hrv_ms == 75.0


def test_import_is_idempotent():
    first = import_mock_health_export(["health_export_recovery_complete.json"])
    second = import_mock_health_export(["health_export_recovery_complete.json"])

    assert first.rows_inserted == 6
    assert second.rows_inserted == 0
    assert second.rows_unchanged == 6
    with connect() as conn:
        count = conn.execute("SELECT COUNT(*) FROM recovery_days").fetchone()[0]
    assert count == 6


def test_import_counts_updated_versus_unchanged(tmp_path, monkeypatch):
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    fixture = fixture_dir / "one_day.json"
    fixture.write_text(json.dumps(_minimal_fixture(sleep_hours=7.0)))
    monkeypatch.setenv("READINESS_SLICE_FIXTURE_DIR", str(fixture_dir))

    first = import_mock_health_export(["one_day.json"])
    fixture.write_text(json.dumps(_minimal_fixture(sleep_hours=8.0)))
    second = import_mock_health_export(["one_day.json"])
    third = import_mock_health_export(["one_day.json"])

    assert first.rows_inserted == 1
    assert second.rows_updated == 1
    assert second.rows_unchanged == 0
    assert third.rows_updated == 0
    assert third.rows_unchanged == 1


def test_fixture_names_cannot_escape_fixture_directory(tmp_path, monkeypatch):
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    outside_fixture = tmp_path / "outside.json"
    outside_fixture.write_text(json.dumps(_minimal_fixture()))
    monkeypatch.setenv("READINESS_SLICE_FIXTURE_DIR", str(fixture_dir))

    result = import_mock_health_export(["../outside.json"])

    assert result.status == "blocked"
    assert any("Invalid fixture name" in error for error in result.errors)
    with connect() as conn:
        assert conn.execute("SELECT COUNT(*) FROM recovery_days").fetchone()[0] == 0


def test_import_records_unknown_metric_warning():
    result = import_mock_health_export([
        "health_export_recovery_complete.json",
        "health_export_unknown_metric.json",
    ])

    assert result.status == "ok"
    assert any("unknown metric ignored" in warning for warning in result.warnings)


def test_malformed_json_records_error_without_rows(tmp_path, monkeypatch):
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    (fixture_dir / "bad.json").write_text("{bad json")
    monkeypatch.setenv("READINESS_SLICE_FIXTURE_DIR", str(fixture_dir))

    result = import_mock_health_export(["bad.json"])

    assert result.status == "error"
    with connect() as conn:
        recovery_count = conn.execute("SELECT COUNT(*) FROM recovery_days").fetchone()[0]
        import_count = conn.execute("SELECT COUNT(*) FROM import_runs").fetchone()[0]
    assert recovery_count == 0
    assert import_count == 1


def test_non_numeric_metric_records_error_without_partial_rows(tmp_path, monkeypatch):
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    (fixture_dir / "bad_metric.json").write_text(
        json.dumps(
            {
                "data": {
                    "metrics": [
                        {
                            "name": "sleep_analysis",
                            "data": [
                                {
                                    "sleepStart": "2026-06-18 00:30:00 +0200",
                                    "sleepEnd": "2026-06-18 06:30:00 +0200",
                                    "totalSleep": "not-a-number",
                                }
                            ],
                        }
                    ]
                }
            }
        )
    )
    monkeypatch.setenv("READINESS_SLICE_FIXTURE_DIR", str(fixture_dir))

    result = import_mock_health_export(["bad_metric.json"])

    assert result.status == "error"
    with connect() as conn:
        assert conn.execute("SELECT COUNT(*) FROM recovery_days").fetchone()[0] == 0
