"""Pure domain of the long-running lift model: estimates, progression and scoring.

No database, workout-app or message parsing here. Exercise identity comes through the
ExerciseCatalog port and interpreted signals through SignalInterpreter, so
each can be replaced (see ports.py and adapters.py).

Sets are not taken to failure and reps in reserve are not logged, so the estimate
measures working capacity at the athlete's usual effort, not a tested 1RM.
"""
from __future__ import annotations

import math
import re
from datetime import datetime, timedelta

MODEL_VERSION = 'lift-kalman-v1'
# Kalman settings as fractions of the lift's level (per day where noted). Session
# noise and level drift are recalibrated on every run from the athlete's own history.
INITIAL_LEVEL_SD, INITIAL_SLOPE_SD, SLOPE_DRIFT_SD = 0.08, 0.002, 0.0005
DEFAULTS = {'session_noise_sd': 0.05, 'level_drift_sd': 0.01}
GRID = [{'session_noise_sd': n, 'level_drift_sd': d} for n in (0.03, 0.05, 0.08, 0.12) for d in (0.003, 0.01, 0.02)]
SLOPE_LIMITS = (-0.002, 0.0035)                 # about -1.4% to +2.5% per week
STRENGTH_REPS = 6                               # prescribed reps at or below: load-based progression
MAX_STEP = 0.05                                 # largest change per session
STRENGTH_CAP = 0.10                             # largest strength-lift increase per session
# A gap is long relative to how often the athlete normally does this lift, not a fixed week.
GAP_FACTOR, GAP_MIN_DAYS, RETURN_REDUCTION = 1.75, 10, 0.10

COMPOUND = re.compile(r'deadlift|squat|lunge|press|row|thrust|pull[ -]?up|pulldown|pull through|rdl|romanian', re.I)
REGIONS = {
    'elbow': r'curl|row|pulldown|pull[ -]?up|chin|press|tricep|skull|dip|fly',
    'wrist': r'curl|row|pulldown|pull[ -]?up|chin|press|tricep|dip',
    'shoulder': r'press|raise|fly|pulldown|pull[ -]?up|row|dip|bench',
    'knee': r'squat|lunge|leg extension|leg press|step[ -]?up|split',
    'back': r'deadlift|rdl|romanian|row|good morning|pull through|squat|swing',
    'hip': r'hip thrust|deadlift|rdl|romanian|squat|lunge|glute|abduct|adduct|kickback|bridge',
}
GENERIC = {'dumbbell', 'barbell', 'machine', 'cable', 'smith', 'single', 'arm', 'with', 'band', 'bodyweight'}


def epley(load, reps):
    return load * (1 + reps / 30)


def working_sets(exercise):
    return [s for s in exercise.get('sets', []) if s.get('type', 'normal') == 'normal'
            and isinstance(s.get('weight_kg'), (int, float)) and s['weight_kg'] > 0
            and isinstance(s.get('reps'), int) and s['reps'] >= 1]


def session_e1rm(exercise):
    """Epley from sets of 1-12 reps; high-rep work (13-30) still counts, as the only evidence for that lift."""
    sets = working_sets(exercise)
    usable = [s for s in sets if s['reps'] <= 12] or [s for s in sets if s['reps'] <= 30]
    return max((epley(s['weight_kg'], s['reps']) for s in usable), default=None)


class Estimate:
    """Level (kg e1RM) and slope (kg/day), with covariance."""

    def __init__(self, first, at, params=DEFAULTS):
        self.params = params
        self.x = [first, 0.0]
        self.p = [[(INITIAL_LEVEL_SD * first) ** 2, 0.0], [0.0, (INITIAL_SLOPE_SD * first) ** 2]]
        self.at, self.n = at, 1

    def predicted(self, at):
        dt = max(0.0, (at - self.at).total_seconds() / 86400)
        level = self.x[0]
        slope = min(max(self.x[1], SLOPE_LIMITS[0] * level), SLOPE_LIMITS[1] * level)
        mean = level + slope * dt
        p = self.p
        var = p[0][0] + 2 * dt * p[0][1] + dt * dt * p[1][1] + (self.params['level_drift_sd'] * level) ** 2 * dt
        return mean, math.sqrt(var), slope

    def update(self, value, at):
        dt = max(0.0, (at - self.at).total_seconds() / 86400)
        level = self.x[0]
        x = [self.x[0] + self.x[1] * dt, self.x[1]]
        p = self.p
        p00 = p[0][0] + 2 * dt * p[0][1] + dt * dt * p[1][1] + (self.params['level_drift_sd'] * level) ** 2 * dt
        p01 = p[0][1] + dt * p[1][1]
        p11 = p[1][1] + (SLOPE_DRIFT_SD * level) ** 2 * dt
        s = p00 + (self.params['session_noise_sd'] * level) ** 2
        k0, k1 = p00 / s, p01 / s
        residual = value - x[0]
        self.x = [x[0] + k0 * residual, x[1] + k1 * residual]
        self.p = [[(1 - k0) * p00, (1 - k0) * p01], [(1 - k0) * p01, p11 - k1 * p01]]
        self.at, self.n = at, self.n + 1


def _performed(workout):
    return datetime.fromisoformat(str(workout['payload']['start_time']).replace('Z', '+00:00'))


def _ended(workout):
    return datetime.fromisoformat(str(workout['payload']['end_time']).replace('Z', '+00:00'))


def history(workouts, catalog, params=DEFAULTS, errors=None):
    """Per lift: estimate, sessions and distinct logged loads. Collects one-step errors."""
    lifts = {}
    for w in sorted(workouts, key=_performed):
        for e in w['payload'].get('exercises', []):
            value = session_e1rm(e)
            if value is None:
                continue
            key = catalog.key(e)
            entry = lifts.get(key)
            if entry is None:
                entry = lifts[key] = {'key': key, 'title': e['title'], 'estimate': Estimate(value, _performed(w), params),
                                      'sessions': [], 'loads': set()}
            else:
                if errors is not None:
                    errors.append(abs(value - entry['estimate'].predicted(_performed(w))[0]) / value)
                entry['estimate'].update(value, _performed(w))
                entry['title'] = e['title']
            sets = working_sets(e)
            entry['sessions'].append({'workout': w['external_id'], 'at': _performed(w), 'e1rm': value,
                                      'top_kg': max(s['weight_kg'] for s in sets),
                                      'sets': [{'reps': s['reps'], 'kg': s['weight_kg']} for s in sets]})
            entry['loads'].update(s['weight_kg'] for s in sets)
    return lifts


def calibrate(workouts, catalog):
    """Pick the noise settings with the lowest one-session-ahead error on the athlete's own history."""
    scored = []
    for params in GRID:
        errors = []
        history(workouts, catalog, params, errors)
        if errors:
            scored.append((sum(errors) / len(errors), params, len(errors)))
    if not scored:
        return DEFAULTS, {'status': 'default', 'reason': 'No repeated lifts yet'}
    error, params, n = min(scored, key=lambda item: item[0])
    return params, {'status': 'calibrated', 'mean_abs_pct_error': round(100 * error, 2), 'pairs': n, **params}


EQUIPMENT_STEP = {'barbell': 2.5, 'ez_bar': 2.5, 'smith_machine': 2.5, 'plate_loaded_machine': 2.5,
                  'trap_bar': 2.5, 'dumbbell': 1.0, 'kettlebell': 2.0, 'cable_stack': 1.0, 'machine_stack': 1.0}


def granularity(entry):
    """Smallest load change the equipment allows, from the exercise rules; else the smallest logged gap."""
    parts = entry.get('key', '').split('::')
    if len(parts) == 3 and parts[1] in EQUIPMENT_STEP:
        return EQUIPMENT_STEP[parts[1]]
    loads = sorted(entry['loads'])
    steps = [b - a for a, b in zip(loads, loads[1:]) if b - a > 0.2]
    return min(min(steps), 2.5) if steps else 2.5


def increment(entry):
    """The athlete's own step for this lift: the median of past increases, else the equipment step."""
    raises = sorted(b['top_kg'] - a['top_kg'] for a, b in zip(entry['sessions'], entry['sessions'][1:])
                    if b['top_kg'] - a['top_kg'] > 0.2)
    return raises[len(raises) // 2] if raises else granularity(entry)


LEARN_MIN_CASES, LEARN_MIN_EFFECT, LEARN_MIN_AGREEMENT = 20, 0.02, 0.7


def _fit(cases, kind):
    with_kind = [o['surprise'] for o in cases if kind in o['kinds']]
    without = [o['surprise'] for o in cases if kind not in o['kinds']]
    if len(with_kind) < LEARN_MIN_CASES or len(without) < LEARN_MIN_CASES:
        return None  # a signal present nearly every day cannot be compared
    baseline = sum(without) / len(without)
    shifted = [x - baseline for x in with_kind]
    effect = sum(shifted) / len(shifted)
    agreement = sum(1 for x in shifted if x * effect > 0) / len(shifted)
    return (effect, baseline) if abs(effect) >= LEARN_MIN_EFFECT and agreement >= LEARN_MIN_AGREEMENT else None


def learn_effects(outcomes):
    """How each kind of contributor actually moved the athlete's loads, from scored outcomes.

    outcomes: [{'at', 'kinds': contributor kinds present, 'surprise': (actual - expected) / last}].
    An effect is fitted on the older two thirds and adopted only if it also improves the
    newest third; otherwise the signal stays a note.
    """
    ordered = sorted(outcomes, key=lambda o: o['at'])
    cut = len(ordered) * 2 // 3
    older, newer = ordered[:cut], ordered[cut:]
    learned = {}
    for kind in {k for o in ordered for k in o['kinds']}:
        fitted = _fit(older, kind)
        if not fitted:
            continue
        effect, baseline = fitted
        held_out = [o['surprise'] - baseline for o in newer if kind in o['kinds']]
        if len(held_out) >= 3 and sum(abs(x - effect) for x in held_out) < sum(abs(x) for x in held_out):
            learned[kind] = round(effect, 4)
    return learned


def _mentions(sentence, title):
    words = {w.rstrip('s') for w in re.findall(r'[a-z]{4,}', re.sub(r'\(.*?\)', '', title.lower()))} - GENERIC
    said = {w.rstrip('s') for w in re.findall(r'[a-z]{4,}', sentence.lower())}
    return bool(words & said)


def health_contributors(days, on):
    """Sleep, HRV and resting HR in the last 3 days against the athlete's own 28-day baseline."""
    recent = [d for d in days if on - timedelta(days=3) <= d['date'] < on]
    base = [d for d in days if on - timedelta(days=31) <= d['date'] < on - timedelta(days=3)]
    out = []

    def values(rows, key):
        return [float(r[key]) for r in rows if r.get(key) is not None]

    sleep, sleep_base = values(recent, 'sleep_hours'), values(base, 'sleep_hours')
    if len(sleep_base) >= 7 and sleep:
        median = sorted(sleep_base)[len(sleep_base) // 2]
        short = sum(1 for s in sleep if s < median - 1)
        out.append({'kind': 'sleep', 'effect': 'hold_compound' if short >= 2 else 'none',
                    'detail': f'{short} of last {len(sleep)} nights >1 h under the {median:.1f} h median'})
    else:
        out.append({'kind': 'sleep', 'effect': 'unknown', 'detail': 'Too little recent or baseline sleep data'})
    hrv, hrv_base = values(recent, 'hrv_ms'), values(base, 'hrv_ms')
    rhr, rhr_base = values(recent, 'resting_hr_bpm'), values(base, 'resting_hr_bpm')
    if len(hrv_base) >= 7 and len(rhr_base) >= 7 and hrv and rhr:
        def stats(v):
            mean = sum(v) / len(v)
            return mean, math.sqrt(sum((x - mean) ** 2 for x in v) / max(1, len(v) - 1))
        (hm, hs), (rm, rs) = stats(hrv_base), stats(rhr_base)
        h, r = sum(hrv) / len(hrv), sum(rhr) / len(rhr)
        off = h < hm - hs and r > rm + rs
        out.append({'kind': 'hrv_rhr', 'effect': 'hold_compound' if off else 'none',
                    'detail': f'HRV {h:.0f} ms vs {hm:.0f}±{hs:.0f}; resting HR {r:.0f} vs {rm:.0f}±{rs:.0f}'})
    else:
        out.append({'kind': 'hrv_rhr', 'effect': 'unknown', 'detail': 'Too little recent or baseline HRV/resting HR data'})
    return out


def _mentions_all(text, title):
    words = {w.rstrip('s') for w in re.findall(r'[a-z]{4,}', re.sub(r'\(.*?\)', '', title.lower()))} - GENERIC
    said = {w.rstrip('s') for w in re.findall(r'[a-z]{4,}', text.lower())}
    return bool(words) and words <= said


def progression_type(item, strength_goals):
    """Strength lifts progress by load; bodybuilding lifts by reps within a range, then load."""
    goal = next((g for g in strength_goals if _mentions_all(g, item['title'])), None)
    if goal:
        return 'strength', 'Named in a current strength goal or block'
    targets = [x['reps'] or x['start'] for x in item['sets'] if x['reps'] or x['start']]
    if targets and min(targets) <= STRENGTH_REPS:
        return 'strength', f'Prescribed {min(targets)} reps or fewer'
    return 'hypertrophy', 'Rep-range work: double progression (reps first, then load)'


def predict_exercise(entry, item, at, routine, sig, health, substitutes_for=None, strength_goals=(), learned=None):
    """Working sets for one exercise and every contributor that shaped them."""
    title = item['title']
    kind, why = progression_type(item, strength_goals)
    contributors = [{'kind': 'progression_type', 'effect': 'none', 'type': kind, 'detail': why}]
    if substitutes_for:
        contributors.append({'kind': 'swap', 'effect': 'none', 'detail': f'Replaces {substitutes_for} in {routine}; loads are not comparable'})
    if not entry:
        return 'insufficient_evidence', [{'reps': x['reps'] or x['start'], 'kg': None} for x in item['sets']], None, None, None, contributors + [
            {'kind': 'history', 'effect': 'calibrate', 'detail': 'No logged sets yet; the first session sets the baseline'}]
    mean, sd, slope = entry['estimate'].predicted(at)
    last = entry['sessions'][-1]
    step = increment(entry)
    contributors.append({'kind': 'strength_estimate', 'effect': 'base',
                         'detail': f'e1RM {mean:.1f}±{sd:.1f} kg from {entry["estimate"].n} sessions; trend {slope * 7:+.2f} kg/week'})
    gap = (at - last['at']).days
    intervals = sorted((b['at'] - a['at']).days for a, b in zip(entry['sessions'], entry['sessions'][1:]))
    usual = intervals[len(intervals) // 2] if intervals else 7
    if gap >= max(GAP_MIN_DAYS, GAP_FACTOR * usual):
        contributors.append({'kind': 'gap', 'effect': 'reduce_gap', 'detail': f'{gap} days since this lift was last logged; usually {usual}'})
    compound = bool(COMPOUND.search(title))
    for h in health:
        # Recorded for the coach's judgment; sleep/HRV holds were not supported by real outcomes.
        contributors.append({**h, 'effect': 'note' if h['effect'] == 'hold_compound' and compound else
                             ('none' if h['effect'] == 'hold_compound' else h['effect'])})
    for s in sig:
        said_at = datetime.fromisoformat(s['at'])
        if said_at <= last['at'] - timedelta(hours=1):
            continue
        about_this = _mentions(s['text'], title)
        if s['kind'] == 'pain' and re.search(r'\b(?:' + REGIONS.get(s['region'], '$^') + r')', title, re.I):
            contributors.append({'kind': 'pain', 'effect': 'hold', 'region': s['region'], 'source': s})
        elif s['kind'] in ('reduce', 'hard') and about_this:
            contributors.append({'kind': s['kind'], 'effect': 'reduce' if s['kind'] == 'reduce' else 'note', 'source': s})
        elif s['kind'] == 'easy' and about_this:
            contributors.append({'kind': 'easy', 'effect': 'allow_step', 'source': s})
        elif s['kind'] == 'state_hold' and said_at > at - timedelta(days=3):
            # Backtest: whole-body tiredness did not predict lower loads, so it informs, not holds.
            contributors.append({'kind': 'state', 'effect': 'note', 'source': s})
        elif s['kind'] == 'state_note' and said_at > at - timedelta(days=3):
            contributors.append({'kind': 'state', 'effect': 'note', 'source': s})
    effects = {c['effect'] for c in contributors}
    # Learned from past outcomes: the expected load shifts by each present kind's measured effect.
    shift = sum((learned or {}).get(k, 0.0) for k in {c['kind'] for c in contributors})
    if shift:
        contributors.append({'kind': 'learned', 'effect': 'expected_shift', 'detail': f'{100 * shift:+.1f}% from past outcomes',
                             'kinds': sorted(k for k in {c['kind'] for c in contributors} if k in (learned or {}))})
    grain = granularity(entry)
    expected = _sets(item, last, mean, step, kind, effects, False, grain)
    for e in expected:
        e['kg'] = round(max(grain, round((e['kg'] * (1 + shift)) / grain) * grain), 2) if shift else e['kg']
    sets = [dict(a, expected_kg=e['kg']) for a, e in zip(_sets(item, last, mean, step, kind, effects, True, grain), expected)]
    return 'available', sets, mean, sd, last['top_kg'], contributors


def _sets(item, last, mean, step, kind, effects, safety, grain=None):
    """Working sets. What the athlete said (pain, "drop it", "it flew") shapes the recommendation; the
    expectation comes from the model and effects learned from past outcomes."""
    held = safety and 'hold' in effects
    grain = grain or step
    snap = lambda kg: math.floor(kg / grain + 1e-9) * grain
    sets = []
    for i, x in enumerate(item['sets']):
        prior = last['sets'][min(i, len(last['sets']) - 1)]
        top = x['end'] or x['reps'] or x['start'] or prior['reps']
        x = {**x, 'start': x['start'] or None}
        bottom = x['start'] or x['reps'] or top
        if kind == 'strength':
            # Anchored on last session: step toward the estimate, never more than +10%.
            reps = x['reps'] or bottom
            estimate = snap(mean / (1 + reps / 30))
            kg = prior['kg'] if held else min(max(prior['kg'] + step, estimate), prior['kg'] * (1 + STRENGTH_CAP))
            kg = max(prior['kg'], snap(kg)) if kg > prior['kg'] else kg
        else:
            # Double progression. A prescribed target comes from the routine; without one,
            # matching the first set's reps on every set counts as completing the target.
            target = x['end'] or x['reps']
            done = target is not None and all(q['reps'] >= target for q in last['sets'])
            if done and not held:
                kg, reps = prior['kg'] + step, bottom
            else:
                kg, reps = prior['kg'], min(top, prior['reps'] + 1) if x['end'] else top
        if 'reduce_gap' in effects:
            kg = snap(prior['kg'] * (1 - RETURN_REDUCTION))
        elif safety and 'reduce' in effects:  # the athlete asked to drop the weight
            kg = prior['kg'] - grain
        elif safety and 'allow_step' in effects and not held:  # the athlete said it moved easily
            kg = max(kg, prior['kg'] + step)
        target = {'reps': reps, 'kg': round(max(kg, grain), 2)}
        if x['end']:
            target['rep_range'] = [x['start'], x['end']]
        sets.append(target)
    return sets


def routine_plan(routine, previous, catalog):
    """Exercises in the next session: the current routine, else the last session."""
    source = routine or previous
    plan = []
    for e in (source or {}).get('exercises', []):
        sets = [s for s in e.get('sets', []) if s.get('type', 'normal') == 'normal']
        if not any(isinstance(s.get('weight_kg'), (int, float)) and s['weight_kg'] > 0 for s in sets):
            continue
        plan.append({'template': e['exercise_template_id'], 'title': e['title'], 'key': catalog.key(e),
                     'sets': [{'reps': s['reps'] if isinstance(s.get('reps'), int) else None,
                               'start': (s.get('rep_range') or {}).get('start'),
                               'end': (s.get('rep_range') or {}).get('end')} for s in sets]})
    return plan


def swaps(plan, previous, catalog):
    """New exercises that took the place of one in the previous session of the routine."""
    group = catalog.group
    before = routine_plan(None, previous, catalog)
    planned = {p['template'] for p in plan}
    dropped = [e for e in before if e['template'] not in planned]
    result = {}
    for p in plan:
        if p['template'] in {e['template'] for e in before}:
            continue
        match = next((d for d in dropped if group(d['title']) and group(d['title']) == group(p['title'])), None)
        if match is None:
            position = next((i for i, q in enumerate(plan) if q is p), None)
            old = [e['template'] for e in before]
            match = next((d for d in dropped if old.index(d['template']) == position), None)
        if match:
            result[p['template']] = match['title']
    return result


def score_exercise(prediction, workout, catalog, sig_after):
    """Compare one prediction with the session that followed it."""
    performed = {catalog.key(e): e for e in workout['payload'].get('exercises', [])}
    actual = performed.get(catalog.key({'title': prediction['exercise_title'], 'exercise_template_id': prediction['exercise_template_id']}))
    # What the athlete said after the session explains the outcome; it does not change it.
    contributors = [{'kind': s['kind'], 'source': s} for s in sig_after]
    if actual is None or not working_sets(actual):
        group = catalog.group(prediction['exercise_title'])
        sub = next((e for e in performed.values() if group and catalog.group(e['title']) == group
                    and e['exercise_template_id'] != prediction['exercise_template_id']), None)
        if sub:
            return 'substituted', [{'title': sub['title'], 'sets': [{'reps': s['reps'], 'kg': s['weight_kg']} for s in working_sets(sub)]}], None, None, None, contributors
        return 'not_performed', [], None, None, None, contributors
    sets = [{'reps': s['reps'], 'kg': s['weight_kg']} for s in working_sets(actual)]
    predicted = [s for s in prediction['predicted_sets_json'] if s.get('kg') is not None]
    e1rm = session_e1rm(actual)
    error = None if prediction['estimate_e1rm_kg'] is None or e1rm is None else e1rm - float(prediction['estimate_e1rm_kg'])
    if not predicted:
        return 'hit', sets, e1rm, error, None, contributors
    top_p, top_a = max(s['kg'] for s in predicted), max(s['kg'] for s in sets)
    expected_top = max(s.get('expected_kg', s['kg']) for s in predicted)
    paired = list(zip(predicted, sets))
    if top_a > top_p + 1e-6 or (top_a >= top_p - 1e-6 and any(a['reps'] >= p['reps'] + 2 for p, a in paired)):
        outcome = 'exceeded'
    elif top_a >= top_p - 1e-6 and all(a['reps'] >= p['reps'] for p, a in paired) and len(sets) >= len(predicted):
        outcome = 'hit'
    else:
        outcome = 'missed'
    return outcome, sets, e1rm, error, top_a - expected_top, contributors


BASELINE_VERSION = 'same-as-last-v1'


def predict_same_as_last(entry, item, at, routine, sig, health, substitutes_for=None, strength_goals=(), learned=None):
    """Baseline model: repeat the last session. Any new model has to beat this on real outcomes."""
    contributors = [{'kind': 'progression_type', 'effect': 'none', 'type': progression_type(item, strength_goals)[0],
                     'detail': 'Baseline: same sets as last time'}]
    if not entry:
        return 'insufficient_evidence', [{'reps': x['reps'] or x['start'], 'kg': None} for x in item['sets']], None, None, None, contributors
    last = entry['sessions'][-1]
    sets = [{'reps': last['sets'][min(i, len(last['sets']) - 1)]['reps'], 'kg': last['sets'][min(i, len(last['sets']) - 1)]['kg'],
             'expected_kg': last['sets'][min(i, len(last['sets']) - 1)]['kg']} for i in range(len(item['sets']))]
    mean, sd, _ = entry['estimate'].predicted(at)
    return 'available', sets, mean, sd, last['top_kg'], contributors


# Every registered model runs nightly and is scored; the champion is the one the coach uses.
MODELS = {MODEL_VERSION: predict_exercise, BASELINE_VERSION: predict_same_as_last}
CHAMPION_MIN_OUTCOMES, CHAMPION_WINDOW_DAYS = 10, 60


def champion(scoreboard, default=MODEL_VERSION):
    """Lowest recent error among models with enough scored outcomes; else the default."""
    eligible = [m for m in scoreboard if m['n'] >= CHAMPION_MIN_OUTCOMES]
    return min(eligible, key=lambda m: m['mean_abs_error_kg'])['model_version'] if eligible else default


ENSEMBLE_VERSION = 'ensemble-v1'
ENSEMBLE_MIN_OUTCOMES, ENSEMBLE_SHRINK = 20, 0.5


def ensemble_weights(versions, scoreboard):
    """Equal weights until every model has enough outcomes; then inverse recent error, shrunk halfway
    to equal. Equal averages usually win with little data (the forecast-combination puzzle)."""
    board = {m['model_version']: m for m in scoreboard}
    equal = {v: 1 / len(versions) for v in versions}
    if not all(board.get(v, {}).get('n', 0) >= ENSEMBLE_MIN_OUTCOMES and board[v]['mean_abs_error_kg'] for v in versions):
        return equal, 'equal'
    inverse = {v: 1 / float(board[v]['mean_abs_error_kg']) for v in versions}
    total = sum(inverse.values())
    return {v: ENSEMBLE_SHRINK * equal[v] + (1 - ENSEMBLE_SHRINK) * inverse[v] / total for v in versions}, 'inverse_error_shrunk'


def combine(rows_by_model, scoreboard):
    """One combined row per exercise that every model could predict."""
    versions = sorted(rows_by_model)
    weights, method = ensemble_weights(versions, scoreboard)
    index = {v: {(r['routine'], r['template']): r for r in rows if r['status'] == 'available'} for v, rows in rows_by_model.items()}
    keys = set.intersection(*(set(i) for i in index.values())) if index else set()
    combined = []
    for key in sorted(keys):
        parts = {v: index[v][key] for v in versions}
        base = parts[versions[0]]
        sets = []
        for i in range(min(len(r['sets']) for r in parts.values())):
            expected = sum(weights[v] * parts[v]['sets'][i]['expected_kg'] for v in versions)
            sets.append({'reps': base['sets'][i]['reps'], 'expected_kg': round(expected, 1),
                         'kg': min(parts[v]['sets'][i]['kg'] for v in versions)})  # most cautious recommendation
        combined.append({**{k: base[k] for k in ('routine', 'template', 'title', 'status', 'mean', 'sd', 'last')}, 'sets': sets,
                         'contributors': [{'kind': 'ensemble', 'effect': 'none', 'method': method, 'weights': weights,
                                           'models': {v: [x['expected_kg'] for x in parts[v]['sets']] for v in versions}}]})
    return combined
