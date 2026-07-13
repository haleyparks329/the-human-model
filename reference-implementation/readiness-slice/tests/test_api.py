from __future__ import annotations

from fastapi.testclient import TestClient

from readiness_slice.api import app


def test_api_import_and_fetch_flow():
    client = TestClient(app)

    response = client.post(
        "/imports/mock-health",
        json={"fixture_names": ["health_export_recovery_complete.json", "health_export_missing_sleep.json"]},
    )
    assert response.status_code == 200
    assert response.json()["rows_inserted"] == 7

    recovery = client.get("/recovery/2026-06-23")
    assert recovery.status_code == 200
    assert recovery.json()["quality_flags"] == ["hrv_daily_mean_used", "missing_sleep"]

    readiness = client.post("/readiness/2026-06-23")
    assert readiness.status_code == 200
    assert readiness.json()["confidence"] == "Low"

    review = client.get("/daily-review/2026-06-23")
    assert review.status_code == 200
    payload = review.json()
    assert payload["date"] == "2026-06-23"
    assert "sleep" in payload["missing_data"]
    assert "Public reference slice" in payload["public_boundary"]


def test_invalid_fixture_handling_returns_404():
    client = TestClient(app)

    response = client.post("/imports/mock-health", json={"fixture_names": ["missing.json"]})

    assert response.status_code == 404
    assert "Fixture not found" in response.text


def test_invalid_date_returns_validation_response():
    client = TestClient(app)

    response = client.get("/recovery/not-a-date")

    assert response.status_code == 422


def test_invalid_calendar_date_returns_validation_response():
    client = TestClient(app)

    response = client.get("/recovery/2026-99-99")

    assert response.status_code == 422


def test_missing_recovery_returns_404():
    client = TestClient(app)

    response = client.get("/daily-review/2026-01-01")

    assert response.status_code == 404
