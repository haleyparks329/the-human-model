"""Walk-forward backtest: predict every logged session using only what came before it."""
from __future__ import annotations

from datetime import timedelta

from . import domain as d

CALIBRATION_WINDOW = timedelta(days=180)


class InMemoryEvidence:
    """The Evidence port over plain lists (for example synthetic.generate())."""

    def __init__(self, data):
        self.data = data

    def workouts(self, cutoff=None):
        return [w for w in self.data['workouts'] if cutoff is None or d._ended(w) <= cutoff]

    def messages(self, since, until):
        return [m for m in self.data['messages'] if since <= m['at'] < until]

    def health(self, on):
        return [h for h in self.data['health'] if h['date'] < on]

    def strength_goals(self):
        return self.data.get('strength_goals', [])


def _kinds(contributors):
    return {c['kind'] for c in contributors if c['kind'] not in ('progression_type', 'strength_estimate')}


def backtest(evidence, catalog, interpreter, use_signals=True):
    """Every model's error on the expected top load, per prediction, and a summary."""
    workouts = sorted(evidence.workouts(), key=d._performed)
    goals = evidence.strength_goals()
    rows, learning = [], []
    for i, w in enumerate(workouts):
        prior = workouts[:i]
        previous = next((x['payload'] for x in reversed(prior) if x['payload']['title'] == w['payload']['title']), None)
        if previous is None:
            continue
        at = d._performed(w) - timedelta(minutes=1)
        params, _ = d.calibrate([x for x in prior if d._performed(x) > at - CALIBRATION_WINDOW], catalog)
        lifts = d.history(prior, catalog, params)
        signals = interpreter.read(evidence.messages(at - timedelta(days=21), at)) if use_signals else []
        health = d.health_contributors(evidence.health(at.date()), at.date()) if use_signals else []
        learned = d.learn_effects([o for o in learning if o['at'] < at])
        for p in d.routine_plan(None, previous, catalog):
            # Past prescriptions are unknown in a log; performed reps are not targets.
            p = {**p, 'sets': [{'reps': None, 'start': None, 'end': None} for _ in p['sets']]}
            entry = lifts.get(p['key'])
            status, sets, mean, sd, last, contributors = d.predict_exercise(
                entry, p, at, w['payload']['title'], signals, health, None, goals, learned)
            if status != 'available':
                continue
            prediction = {'exercise_template_id': p['template'], 'exercise_title': p['title'],
                          'predicted_sets_json': sets, 'estimate_e1rm_kg': mean}
            outcome, actual, _, _, error, _ = d.score_exercise(prediction, w, catalog, [])
            if error is None:
                continue
            actual_top, expected = max(s['kg'] for s in actual), max(s['expected_kg'] for s in sets)
            plain = max(s['kg'] for s in d._sets(p, entry['sessions'][-1], mean, d.increment(entry), contributors[0]['type'],
                                                  {c['effect'] for c in contributors}, False, d.granularity(entry)))
            learning.append({'at': d._ended(w), 'kinds': _kinds(contributors), 'surprise': (actual_top - plain) / last})
            rows.append({'date': at.date().isoformat(), 'routine': w['payload']['title'], 'exercise': p['title'],
                         'type': contributors[0]['type'], 'outcome': outcome, 'actual_top_kg': actual_top,
                         'errors_kg': {d.MODEL_VERSION: actual_top - expected,
                                       d.BASELINE_VERSION: actual_top - last,
                                       d.ENSEMBLE_VERSION: actual_top - (expected + last) / 2,  # equal weights before 20 outcomes
                                       'last-plus-2.5': actual_top - (last + 2.5)},
                         'contributors': sorted(_kinds(contributors))})
    return {'n': len(rows), 'rows': rows, 'summary': summarize(rows), 'learned_at_end': d.learn_effects(learning)}


def summarize(rows):
    def mae(rows, model):
        return round(sum(abs(r['errors_kg'][model]) for r in rows) / len(rows), 2) if rows else None
    models = list(rows[0]['errors_kg']) if rows else []
    groups = {'all': rows, **{t: [r for r in rows if r['type'] == t] for t in ('strength', 'hypertrophy')}}
    return {name: {'n': len(group), **{m: mae(group, m) for m in models}} for name, group in groups.items()}
