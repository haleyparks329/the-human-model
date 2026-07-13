from __future__ import annotations

from readiness_slice.health_import import import_mock_health_export
from readiness_slice.readiness import calculate_readiness
from readiness_slice.repository import (
    get_readiness_result,
    get_recovery,
    recovery_history_through,
    upsert_readiness_result,
)


def test_readiness_persistence_is_idempotent():
    import_mock_health_export(["health_export_recovery_complete.json"])
    target = get_recovery("2026-06-22")
    result = calculate_readiness(target, recovery_history_through("2026-06-22"))

    upsert_readiness_result(result)
    upsert_readiness_result(result)
    stored = get_readiness_result("2026-06-22")

    assert stored is not None
    assert stored.score == result.score
    assert stored.status == result.status
