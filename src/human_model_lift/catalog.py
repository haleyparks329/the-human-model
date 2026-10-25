"""Exercise catalog adapter: one identity per lift, and substitution groups for swaps."""
from __future__ import annotations

from pathlib import Path

RULES = Path(__file__).with_name('exercise_rules.yaml')


class YamlCatalog:
    """Lift identity and substitution groups from exercise_rules.yaml."""

    def __init__(self, path=RULES):
        import yaml
        self.rules = {' '.join(a.lower().split()): r for r in (yaml.safe_load(Path(path).read_text()) or [])
                      for a in r.get('exercise_aliases', [])}

    def _rule(self, title):
        return self.rules.get(' '.join(title.lower().split()))

    def key(self, exercise):
        rule = self._rule(exercise['title'])
        if rule:
            return f"{rule['canonical_exercise_id']}::{rule['equipment_type']}::{rule['load_input_type']}"
        return 'template:' + str(exercise['exercise_template_id'])

    def group(self, title):
        return (self._rule(title) or {}).get('substitution_group')
