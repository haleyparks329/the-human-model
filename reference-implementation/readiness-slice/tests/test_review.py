from __future__ import annotations

from readiness_slice.health_import import import_mock_health_export
from readiness_slice.review import daily_review_for_date


def test_daily_review_json_has_public_boundary_and_missing_data():
    import_mock_health_export([
        "health_export_recovery_complete.json",
        "health_export_missing_sleep.json",
    ])

    review = daily_review_for_date("2026-06-23")

    assert review.recovery is not None
    assert review.readiness is not None
    assert review.import_health["status"] == "ok"
    assert "sleep" in review.missing_data
    assert "synthetic" in review.public_boundary
    assert "no Telegram" in review.public_boundary
