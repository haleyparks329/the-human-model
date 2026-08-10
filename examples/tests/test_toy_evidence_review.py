import json
import sys
import unittest
from pathlib import Path


EXAMPLES = Path(__file__).parents[1]
sys.path.insert(0, str(EXAMPLES))

from toy_evidence_review import review


class ToyEvidenceReviewTests(unittest.TestCase):
    def test_preserves_provenance_and_visible_uncertainty(self):
        payload = json.loads((EXAMPLES / "toy_observations.json").read_text(encoding="utf-8"))
        result = review(payload)
        self.assertEqual([item["status"] for item in result], ["supported", "partial", "unsupported"])
        self.assertEqual(result[0]["evidence"][0]["source"], "synthetic session note")
        self.assertTrue(all("Human review required" in item["review_note"] for item in result))


if __name__ == "__main__":
    unittest.main()
