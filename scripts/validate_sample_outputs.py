#!/usr/bin/env python3
"""Validate curated public sample outputs."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "examples" / "sample-output"
EXPECTED_FILES = {
    "README.md",
    "readiness-modeling-report.md",
    "bridget-daily-card.svg",
    "training-workout-sheet.csv",
    "dashboard-data-shaping-summary.json",
    "movement-quality-review-summary.json",
}
TEXT_SUFFIXES = {".csv", ".json", ".md", ".svg", ".txt"}
FORBIDDEN_TEXT = ("/Users/", "\\Users\\")


def fail(message: str) -> int:
    print(f"Sample output validation failed: {message}")
    return 1


def validate_expected_files() -> int:
    if not SAMPLE_DIR.exists():
        return fail(f"{SAMPLE_DIR.relative_to(ROOT)} does not exist")

    missing = sorted(EXPECTED_FILES - {path.name for path in SAMPLE_DIR.iterdir() if path.is_file()})
    if missing:
        return fail(f"missing expected files: {', '.join(missing)}")
    return 0


def validate_file_contents() -> int:
    for path in sorted(SAMPLE_DIR.iterdir()):
        if not path.is_file():
            continue
        if path.stat().st_size == 0:
            return fail(f"{path.relative_to(ROOT)} is empty")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for forbidden in FORBIDDEN_TEXT:
            if forbidden in text:
                return fail(f"{path.relative_to(ROOT)} contains an absolute user path pattern")
    return 0


def validate_structured_outputs() -> int:
    try:
        json.loads((SAMPLE_DIR / "dashboard-data-shaping-summary.json").read_text(encoding="utf-8"))
        json.loads((SAMPLE_DIR / "movement-quality-review-summary.json").read_text(encoding="utf-8"))

        rows = list(csv.DictReader((SAMPLE_DIR / "training-workout-sheet.csv").open(encoding="utf-8")))
        if len(rows) != 4:
            return fail("training-workout-sheet.csv should contain four public sample rows")
        if rows[0].get("exercise") != "Smith Machine Incline Bench Press":
            return fail("training-workout-sheet.csv first exercise changed unexpectedly")

        svg = (SAMPLE_DIR / "bridget-daily-card.svg").read_text(encoding="utf-8")
        if "<svg" not in svg or "Bridget daily card" not in svg:
            return fail("bridget-daily-card.svg does not look like the expected daily-card artifact")
    except (csv.Error, json.JSONDecodeError, OSError) as exc:
        return fail(str(exc))

    return 0


def main() -> int:
    for check in (validate_expected_files, validate_file_contents, validate_structured_outputs):
        result = check()
        if result:
            return result

    print("Sample output validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
