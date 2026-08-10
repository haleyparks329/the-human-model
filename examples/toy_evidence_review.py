"""Deliberately incomplete synthetic provenance example."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).parent


def review(payload: dict) -> list[dict]:
    observations = {item["id"]: item for item in payload["observations"]}
    result = []
    for claim in payload["claims"]:
        evidence = [observations[item] for item in claim["evidence_ids"] if item in observations]
        if len(evidence) > 1:
            status = "supported"
        elif evidence:
            status = "partial"
        else:
            status = "unsupported"
        result.append(
            {
                "claim": claim["statement"],
                "status": status,
                "evidence": [
                    {"observation": item["statement"], "source": item["source"]}
                    for item in evidence
                ],
                "review_note": "Human review required; toy labels are not decision rules.",
            }
        )
    return result


if __name__ == "__main__":
    source = json.loads((ROOT / "toy_observations.json").read_text(encoding="utf-8"))
    print(json.dumps(review(source), indent=2))
