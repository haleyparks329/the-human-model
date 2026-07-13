from __future__ import annotations

import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    monkeypatch.setenv("READINESS_SLICE_DB", str(tmp_path / "readiness_slice.sqlite3"))
    from readiness_slice.db import apply_migrations

    apply_migrations()
    return tmp_path / "readiness_slice.sqlite3"
