"""python -m human_model_lift backtest | predict  (synthetic athlete; no real data)."""
from __future__ import annotations

import argparse
import json
from datetime import timedelta

from . import domain as d
from .backtest import InMemoryEvidence, backtest
from .catalog import YamlCatalog
from .signals import KeywordSignals
from .synthetic import generate, routine

MODELS = (d.MODEL_VERSION, d.BASELINE_VERSION, d.ENSEMBLE_VERSION, 'last-plus-2.5')


def show_backtest(result):
    print(f"Walk-forward backtest on a synthetic athlete: {result['n']} predictions, each using only earlier sessions.")
    print('Mean absolute error of the expected top-set load (kg), lower is better:\n')
    print(f"{'':14}{'n':>5}" + ''.join(f'{m:>18}' for m in MODELS))
    for group, row in result['summary'].items():
        print(f'{group:14}{row["n"]:>5}' + ''.join(f'{row[m]:>18}' for m in MODELS))
    print(f"\nEffects learned from outcomes (held-out check): {result['learned_at_end'] or 'none'}")


def show_prediction(data, catalog, interpreter, weeks):
    workouts = sorted(data['workouts'], key=d._performed)
    previous = workouts[-2]['payload']  # the routine done before the last one comes next
    at = d._performed(workouts[-1]) + timedelta(days=3)
    prescription = routine(previous['title'], weeks)
    lifts = d.history(workouts, catalog, d.calibrate(workouts, catalog)[0])
    signals = interpreter.read(InMemoryEvidence(data).messages(at - timedelta(days=21), at))
    health = d.health_contributors(data['health'], at.date())
    print(f"Next session: {previous['title']} on {at.date()}\n")
    for item in d.routine_plan(prescription, previous, catalog):
        status, sets, mean, sd, last, contributors = d.predict_exercise(
            lifts.get(item['key']), item, at, previous['title'], signals, health, None, data['strength_goals'])
        print(f"{item['title']}: " + ', '.join(f"{s['reps']} x {s['kg']} kg" for s in sets)
              + (f"   (expected {max(s['expected_kg'] for s in sets)} kg)" if sets and sets[0].get('expected_kg') else ''))
        for c in contributors:
            print(f"    {c['kind']:<18} {c['effect']:<14} {c.get('detail') or c.get('source', {}).get('text', '')}")


def main():
    parser = argparse.ArgumentParser(prog='human_model_lift')
    parser.add_argument('command', choices=('backtest', 'predict'))
    parser.add_argument('--weeks', type=int, default=16)
    parser.add_argument('--seed', type=int, default=7)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    data, catalog, interpreter = generate(args.weeks, args.seed), YamlCatalog(), KeywordSignals()
    if args.command == 'backtest':
        result = backtest(InMemoryEvidence(data), catalog, interpreter)
        print(json.dumps(result['summary'], indent=2)) if args.json else show_backtest(result)
    else:
        show_prediction(data, catalog, interpreter, args.weeks)


if __name__ == '__main__':
    main()
