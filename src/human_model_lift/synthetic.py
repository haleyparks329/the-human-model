"""A synthetic athlete, so the model can be run and tested without anyone's real data.

The athlete trains two routines a week. Each lift has a true capacity (e1RM) that
drifts upward, and the athlete adds a load step whenever the last session hit its
reps and the day allows it. That matches the real log the generator was calibrated
on: the top load rose in about 40% of sessions and reps held across sets.
Performed reps come from the capacity on the day (Epley inverted, a couple of reps
short of failure). Some events have real effects and some only look like they should:

- a 12-day break detrains every lift by about 5%, and the athlete returns about 10% lighter;
- on strength lifts the athlete works up as far as the day allows (up to +10%);
- an elbow complaint makes the athlete hold curl loads for two sessions;
- "it flew" comes before a deadlift jump;
- tiredness messages, short sleep and low HRV are generated but do not change
  performance, which is what the real data showed (see docs/lift-model-findings.md).

The generator is a test fixture, not evidence that the model works on people.
"""
from __future__ import annotations

import math
import random
from datetime import date, datetime, timedelta, timezone

START = datetime(2026, 1, 5, 17, tzinfo=timezone.utc)  # a Monday

# title, template id, sets, rep target (fixed) or range, starting e1RM kg, weekly gain, load step
ROUTINES = {
    'Lower': [
        ('Deadlift (Barbell)', 'T-DL', 3, (5, 5), 110.0, 0.015, 2.5),
        ('Smith Machine Hip Thrust', 'T-HT', 3, (8, 12), 120.0, 0.006, 2.5),
        ('Leg Press (Machine)', 'T-LP', 3, (10, 12), 160.0, 0.005, 2.5),
        ('Machine Lying Leg Curl', 'T-LC', 3, (10, 12), 45.0, 0.004, 1.0),
    ],
    'Upper': [
        ('Push Press', 'T-PP', 3, (5, 5), 55.0, 0.012, 2.5),
        ('Machine Row', 'T-MR', 3, (10, 12), 70.0, 0.012, 1.0),
        ('Dumbbell Lateral Raise', 'T-LR', 3, (12, 15), 12.0, 0.010, 1.0),
        ('EZ Bar Biceps Curl', 'T-BC', 3, (10, 12), 32.0, 0.010, 2.5),
    ],
}
SWAP_WEEK = 11  # Leg press is replaced by the hack squat from this week on
SWAP = ('Machine Hack Squat', 'T-HS', 3, (10, 12), 150.0, 0.012, 2.5)
BREAK_WEEK, BREAK_DAYS, DETRAINING, RETURN_DROP = 9, 12, 0.05, 0.10
ELBOW_WEEK = 6
RESERVE = 3  # reps short of failure on a usual day
PUSH = 2     # reps of that margin the athlete will spend to add a step


def _iso(at):
    return at.isoformat().replace('+00:00', 'Z')


def _reps_at(capacity, load):
    return max(1, math.floor(30 * (capacity / load - 1)) - RESERVE)


def generate(weeks=16, seed=7):
    """Workouts, messages and daily health rows in the shapes the domain reads."""
    rng = random.Random(seed)
    workouts, messages, health = [], [], []
    capacity, last, detrained, returning = {}, {}, set(), set()
    day_offset = {'Lower': 0, 'Upper': 3}
    elbow_sessions = 0
    for week in range(weeks):
        for routine, offset in day_offset.items():
            at = START + timedelta(weeks=week, days=offset) + timedelta(days=BREAK_DAYS if week >= BREAK_WEEK else 0)
            plan = [SWAP if (week >= SWAP_WEEK and title == 'Leg Press (Machine)') else row
                    for row in ROUTINES[routine] for title in [row[0]]]
            if routine == 'Upper' and week == ELBOW_WEEK:
                messages.append({'source': 'chat', 'ref': f'm{len(messages)}', 'at': at - timedelta(days=1),
                                 'text': 'My left elbow feels weird when I curl.'})
                elbow_sessions = 2
            exercises = []
            for title, template, n_sets, (low, high), start, gain, step in plan:
                level = capacity.get(title, start) * (1 + gain * rng.uniform(0.4, 1.6))
                if week == BREAK_WEEK and title in capacity and title not in detrained:
                    level *= 1 - DETRAINING
                    detrained.add(title)
                    returning.add(title)
                capacity[title] = level
                today = level * (1 + rng.gauss(0, 0.025))  # day-to-day variation nothing in the data explains
                previous = last.get(title)
                aim = low  # the athlete works at the bottom of the range and adds load, as the real log shows
                if previous is None:
                    load = round(level / (1 + (low + RESERVE + 1) / 30) / step) * step
                else:
                    load, reps_done = previous
                    sore = title == 'EZ Bar Biceps Curl' and elbow_sessions
                    if title in returning:
                        load = round(load * (1 - RETURN_DROP) / step) * step  # back from the break: start lighter
                        returning.discard(title)
                    elif not sore and min(reps_done) >= low and _reps_at(today, load + step) + PUSH >= low:
                        # Add a step whenever the last session hit its reps and today allows it; on a
                        # strength lift, work up as far as today allows (at most +10%).
                        ceiling = load * 1.10 if low == high else load + step
                        while load + step <= ceiling and _reps_at(today, load + step) + PUSH >= low:
                            load += step
                # Sets stop short of failure, so reps hold across sets unless the load is near capacity.
                reps = [max(1, min(aim, _reps_at(today * (1 - 0.01 * i), load))) for i in range(n_sets)]
                last[title] = (load, reps)
                exercises.append({'title': title, 'exercise_template_id': template,
                                  'sets': [{'type': 'normal', 'weight_kg': load, 'reps': r} for r in reps]})
            if routine == 'Upper' and elbow_sessions:
                elbow_sessions -= 1
            if routine == 'Lower' and week in (4, 13):
                messages.append({'source': 'chat', 'ref': f'm{len(messages)}', 'at': at + timedelta(hours=2),
                                 'text': 'Deadlift flew today, could have gone heavier.'})
                load, reps = last['Deadlift (Barbell)']
                last['Deadlift (Barbell)'] = (load + 2.5, reps)  # the athlete jumps next time
            if rng.random() < 0.25:
                messages.append({'source': 'chat', 'ref': f'm{len(messages)}', 'at': at - timedelta(hours=5),
                                 'text': rng.choice(['Exhausted after work today.', 'Super tired, slept badly.',
                                                     'Stressful week, but heading to the gym.'])})
            end = at + timedelta(minutes=70)
            workouts.append({'external_id': f'w{len(workouts)}',
                             'payload': {'title': routine, 'start_time': _iso(at), 'end_time': _iso(end), 'exercises': exercises}})
    first = START.date() - timedelta(days=30)
    for i in range((weeks + 6) * 7):
        health.append({'date': first + timedelta(days=i), 'sleep_hours': round(rng.gauss(7.2, 0.8), 1),
                       'hrv_ms': round(rng.gauss(55, 8)), 'resting_hr_bpm': round(rng.gauss(58, 3))})
    return {'workouts': workouts, 'messages': messages, 'health': health,
            'strength_goals': ['Conventional deadlift strength block']}


def routine(title, week):
    """The prescription for a routine in a given week, in the workout app's routine shape."""
    rows = [SWAP if week >= SWAP_WEEK and row[0] == 'Leg Press (Machine)' else row for row in ROUTINES[title]]
    return {'title': title, 'exercises': [
        {'title': name, 'exercise_template_id': template,
         'sets': [{'type': 'normal', 'weight_kg': 1, 'reps': low if low == high else None,
                   'rep_range': None if low == high else {'start': low, 'end': high}} for _ in range(n_sets)]}
        for name, template, n_sets, (low, high), *_ in rows]}
