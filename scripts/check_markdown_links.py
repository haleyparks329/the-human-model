#!/usr/bin/env python3
"""Validate local Markdown links and image paths.

This intentionally checks only repository-local targets. External URLs and
in-page anchors are left to humans because this public repo should not need a
large link-checking dependency to stay healthy.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"(!?)\[[^\]]+\]\(([^)]+)\)")


def markdown_files() -> list[Path]:
    ignored_dirs = {".git", "__pycache__", ".venv", "venv", "env"}
    files: list[Path] = []
    for path in ROOT.rglob("*.md"):
        if any(part in ignored_dirs for part in path.relative_to(ROOT).parts):
            continue
        files.append(path)
    return sorted(files)


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return unquote(target.split("#", 1)[0].strip())


def should_skip(target: str) -> bool:
    if not target:
        return True
    return target.startswith(("http://", "https://", "mailto:", "#"))


def main() -> int:
    missing: list[str] = []

    for markdown_path in markdown_files():
        text = markdown_path.read_text(encoding="utf-8", errors="replace")
        for match in LINK_PATTERN.finditer(text):
            target = normalize_target(match.group(2))
            if should_skip(target) or "://" in target:
                continue

            resolved = (markdown_path.parent / target).resolve()
            if not resolved.exists():
                rel_markdown = markdown_path.relative_to(ROOT)
                missing.append(f"{rel_markdown}: missing local target: {match.group(2)}")

    if missing:
        print("Markdown link check failed:")
        for item in missing:
            print(f"- {item}")
        return 1

    print("Markdown link check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
