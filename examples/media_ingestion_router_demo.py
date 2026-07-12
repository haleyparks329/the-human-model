"""Sanitized media-ingestion routing example.

The private project now has a design boundary for future media intake from
desktop drops, Apple Shortcuts, Bridget uploads, and manual workflows. This
public example keeps that behavior mock-only: it normalizes request metadata,
detects duplicates, infers a review route, and emits a manifest without reading
or moving local files.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import PurePath


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".mov", ".mp4"}
RDL_VIEW_TOKENS = {
    "side": "side",
    "left": "side",
    "right": "side",
    "front": "front",
    "rear": "rear",
    "back": "rear",
    "oblique": "oblique",
}


@dataclass(frozen=True)
class MediaIntakeRequest:
    source: str
    filename: str
    content_fingerprint: str
    captured_at: str
    note: str = ""


def intake_key(request: MediaIntakeRequest) -> str:
    """Build a deterministic public-safe dedupe key."""

    normalized = "|".join(
        [
            request.source.strip().lower(),
            PurePath(request.filename).name.strip().lower(),
            request.content_fingerprint.strip().lower(),
        ]
    )
    return sha256(normalized.encode("utf-8")).hexdigest()[:16]


def infer_media_kind(filename: str) -> str:
    extension = PurePath(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        return "unsupported"
    if extension in {".mov", ".mp4"}:
        return "training_video"
    return "image"


def infer_camera_view(filename: str, note: str = "") -> str:
    tokens = _tokens(filename) | _tokens(note)
    for token, camera_view in RDL_VIEW_TOKENS.items():
        if token in tokens:
            return camera_view
    return "unknown"


def route_request(
    request: MediaIntakeRequest,
    existing_keys: set[str] | None = None,
) -> dict:
    """Normalize one intake request into a reviewable manifest row."""

    existing_keys = existing_keys or set()
    key = intake_key(request)
    media_kind = infer_media_kind(request.filename)
    camera_view = infer_camera_view(request.filename, request.note)
    duplicate = key in existing_keys
    review_status = "duplicate" if duplicate else "needs_review"
    if media_kind == "unsupported":
        review_status = "blocked"

    analysis_route = "manual_review"
    if media_kind == "training_video" and "rdl" in _tokens(request.filename):
        analysis_route = "movement_quality_rdl"
    elif media_kind == "image":
        analysis_route = "body_or_progress_review"

    return {
        "intake_key": key,
        "source": request.source,
        "filename": PurePath(request.filename).name,
        "captured_at": request.captured_at,
        "media_kind": media_kind,
        "camera_view": camera_view,
        "analysis_route": analysis_route,
        "review_status": review_status,
    }


def build_manifest(requests: list[MediaIntakeRequest]) -> list[dict]:
    seen: set[str] = set()
    manifest: list[dict] = []
    for request in requests:
        row = route_request(request, seen)
        manifest.append(row)
        if row["review_status"] != "blocked":
            seen.add(row["intake_key"])
    return manifest


def _tokens(value: str) -> set[str]:
    cleaned = "".join(char.lower() if char.isalnum() else " " for char in value)
    return {token for token in cleaned.split() if token}


def sample_requests() -> list[MediaIntakeRequest]:
    return [
        MediaIntakeRequest(
            source="desktop_drop",
            filename="2026-07-10_rdl_side_set1.mov",
            content_fingerprint="mock-video-a",
            captured_at="2026-07-10T09:10:00",
        ),
        MediaIntakeRequest(
            source="bridget_upload",
            filename="2026-07-10_rdl_front_set1.mov",
            content_fingerprint="mock-video-b",
            captured_at="2026-07-10T09:11:00",
        ),
        MediaIntakeRequest(
            source="apple_shortcut",
            filename="progress_checkin_front.png",
            content_fingerprint="mock-image-a",
            captured_at="2026-07-10T09:12:00",
        ),
        MediaIntakeRequest(
            source="desktop_drop",
            filename="2026-07-10_rdl_side_set1.mov",
            content_fingerprint="mock-video-a",
            captured_at="2026-07-10T09:10:00",
        ),
    ]


def main() -> None:
    for row in build_manifest(sample_requests()):
        print(row)


if __name__ == "__main__":
    main()
