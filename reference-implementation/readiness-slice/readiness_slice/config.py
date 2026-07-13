from __future__ import annotations

import os
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent
DEFAULT_DB_PATH = PROJECT_ROOT / ".local" / "readiness_slice.sqlite3"
DEFAULT_FIXTURE_DIR = PROJECT_ROOT / "data" / "fixtures"


def db_path() -> Path:
    return Path(os.getenv("READINESS_SLICE_DB", str(DEFAULT_DB_PATH)))


def fixture_dir() -> Path:
    return Path(os.getenv("READINESS_SLICE_FIXTURE_DIR", str(DEFAULT_FIXTURE_DIR)))


def timezone_name() -> str:
    return os.getenv("READINESS_SLICE_TIMEZONE", "Europe/Copenhagen")
