from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from typing import Iterable, List

from .config import db_path


MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def connect() -> sqlite3.Connection:
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def apply_migrations() -> None:
    with connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS schema_migrations "
            "(version TEXT PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )
        applied = {
            row["version"]
            for row in conn.execute("SELECT version FROM schema_migrations").fetchall()
        }
        for migration in sorted(MIGRATIONS_DIR.glob("*.sql")):
            version = migration.stem
            if version in applied:
                continue
            conn.executescript(migration.read_text())
            conn.execute("INSERT INTO schema_migrations (version) VALUES (?)", (version,))


def rows_to_dicts(rows: Iterable[sqlite3.Row]) -> List[dict]:
    return [dict(row) for row in rows]


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else "migrate"
    if command != "migrate":
        print("Usage: python -m readiness_slice.db migrate")
        return 2
    apply_migrations()
    print("Migrated {0}".format(db_path()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
