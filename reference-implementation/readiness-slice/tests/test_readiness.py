from __future__ import annotations

from readiness_slice.health_import import import_mock_health_export
from readiness_slice.models import RecoveryDay
from readiness_slice.repository import get_recovery, recovery_history_through
from readiness_slice.readiness import calculate_readiness


def test_readiness_with_sufficient_baseline_returns_push_or_maintain():
    import_mock_health_export(["health_export_recovery_complete.json"])
    target = get_recovery("2026-06-22")
    history = recovery_history_through("2026-06-22")

    result = calculate_readiness(target, history)

    assert result.score is not None
    assert result.status in {"Push", "Maintain"}
    assert result.confidence in {"Medium", "High"}
    assert result.factors


def test_readiness_with_missing_data_low_confidence():
    import_mock_health_export([
        "health_export_recovery_complete.json",
        "health_export_missing_sleep.json",
    ])
    target = get_recovery("2026-06-23")
    history = recovery_history_through("2026-06-23")

    result = calculate_readiness(target, history)

    assert result.confidence == "Low"
    assert result.status in {"Maintain", "Modify", "Rest"}
    assert any("missing critical data: sleep" == factor for factor in result.factors)
    assert "missing sleep" in "; ".join(result.data_freshness)


def test_readiness_with_thin_baseline_is_low_confidence_without_missing_inputs():
    target = RecoveryDay(
        date="2026-06-03",
        sleep_hours=7.5,
        hrv_ms=75.0,
        resting_hr_bpm=52.0,
    )
    history = [
        RecoveryDay(date="2026-06-01", sleep_hours=7.0, hrv_ms=72.0, resting_hr_bpm=53.0),
        RecoveryDay(date="2026-06-02", sleep_hours=7.2, hrv_ms=74.0, resting_hr_bpm=52.0),
        target,
    ]

    result = calculate_readiness(target, history)

    assert result.score is not None
    assert result.confidence == "Low"
    assert "2 baseline days" in result.data_freshness
