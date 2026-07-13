from __future__ import annotations

import json

from .db import apply_migrations, db_path
from .health_import import import_mock_health_export
from .repository import list_recovery
from .review import daily_review_for_date


def main() -> None:
    path = db_path()
    if path.exists():
        path.unlink()
    apply_migrations()
    result = import_mock_health_export()
    recovery_rows = list_recovery()
    latest_date = recovery_rows[0].date if recovery_rows else ""
    print("Imported mock Apple Health fixtures:")
    print(json.dumps(result.__dict__, indent=2, sort_keys=True))
    if latest_date:
        print("\nDaily review:")
        print(daily_review_for_date(latest_date).model_dump_json(indent=2))


if __name__ == "__main__":
    main()
