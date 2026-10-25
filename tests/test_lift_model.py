from datetime import datetime, timedelta, timezone


from human_model_lift import domain as d
from human_model_lift.catalog import YamlCatalog
from human_model_lift.signals import KeywordSignals

T0 = datetime(2026, 10, 1, 5, tzinfo=timezone.utc)


def session(day, title, sets, routine='Lower 1', template='T1'):
    at = (T0 + timedelta(days=day)).isoformat()
    return {'external_id': f'w{day}', 'payload': {'title': routine, 'start_time': at, 'end_time': at, 'exercises': [
        {'title': title, 'exercise_template_id': template,
         'sets': [{'type': 'normal', 'weight_kg': kg, 'reps': reps} for kg, reps in sets]}]}}


def predict(workouts, item_sets, signals=(), goals=(), learned=None, title='Leg Extension (Machine)', at_day=14):
    catalog = YamlCatalog()
    lifts = d.history(workouts, catalog)
    item = {'template': 'T1', 'title': title, 'key': catalog.key({'title': title, 'exercise_template_id': 'T1'}), 'sets': item_sets}
    return d.predict_exercise(lifts[item['key']], item, T0 + timedelta(days=at_day), 'Lower 1', list(signals), [], None, goals, learned)


def test_bodybuilding_lift_adds_load_only_after_the_rep_target():
    history = [session(0, 'Leg Extension (Machine)', [(60, 10)] * 3), session(7, 'Leg Extension (Machine)', [(64, 10)] * 3)]
    target = [{'reps': 10, 'start': None, 'end': None}] * 3
    assert [s['kg'] for s in predict(history, target)[1]] == [68, 68, 68]
    short = history[:1] + [session(7, 'Leg Extension (Machine)', [(64, 10), (64, 9), (64, 8)])]
    assert [s['kg'] for s in predict(short, target)[1]] == [64, 64, 64]


def test_high_rep_work_still_builds_history():
    history = [session(0, 'Hip Thrust (Dumbbell)', [(30, 15)] * 3), session(7, 'Hip Thrust (Dumbbell)', [(30, 15)] * 3)]
    assert predict(history, [{'reps': 15, 'start': None, 'end': None}] * 3, title='Hip Thrust (Dumbbell)')[0] == 'available'


def test_strength_lift_steps_from_last_session_within_the_cap():
    history = [session(0, 'Deadlift (Barbell)', [(80, 5)]), session(7, 'Deadlift (Barbell)', [(90, 5)])]
    sets = predict(history, [{'reps': 5, 'start': None, 'end': None}], goals=['Clean conventional deadlift 1RM'],
                   title='Deadlift (Barbell)')[1]
    assert 90 < sets[0]['kg'] <= 99


def test_reported_pain_holds_the_recommendation_not_the_expectation():
    history = [session(0, 'Bicep Curl (Dumbbell)', [(10, 12)] * 3), session(7, 'Bicep Curl (Dumbbell)', [(12, 12)] * 3)]
    pain = {'kind': 'pain', 'region': 'elbow', 'source': 'conversation', 'id': '1', 'at': str(T0 + timedelta(days=10)), 'text': 'elbow pops'}
    sets = predict(history, [{'reps': 12, 'start': None, 'end': None}] * 3, [pain], title='Bicep Curl (Dumbbell)')[1]
    assert sets[0]['kg'] == 12 and sets[0]['expected_kg'] == 14
    machine = [session(0, 'Leg Extension (Machine)', [(60, 10)] * 3), session(7, 'Leg Extension (Machine)', [(64, 10)] * 3)]
    assert predict(machine, [{'reps': 10, 'start': None, 'end': None}] * 3, [pain])[1][0]['kg'] == 68  # "chin" is not in "Machine"


def test_learned_effects_need_enough_consistent_cases():
    case = lambda day, kinds, surprise: {'at': T0 + timedelta(days=day), 'kinds': kinds, 'surprise': surprise}
    cases = [case(i, {'pain'} if i % 2 else set(), 0.05 if i % 2 else 0.0) for i in range(90)]
    assert d.learn_effects(cases) == {'pain': 0.05}
    reversed_later = cases[:60] + [case(i, {'pain'}, -0.05) for i in range(60, 90)]
    assert d.learn_effects(reversed_later) == {}


def test_keyword_reader_keeps_exercise_names_and_idioms_apart():
    read = lambda text: {(s['kind'], s.get('region')) for s in KeywordSignals().read([{'source': 'c', 'ref': '1', 'at': T0, 'text': text}])}
    assert read('My left elbow is feeling weird.') == {('pain', 'elbow')}
    assert read("I'm sick of hip thrusts.") == set()
    assert read('Old videos of my hip thrusts from a weird angle.') == set()
    assert read("I'm just less exhausted now that I'm not working.") == set()


def test_combined_prediction_averages_equally_until_models_have_a_track_record():
    row = lambda kg: {'routine': 'Lower 1', 'template': 'T1', 'title': 'x', 'status': 'available', 'mean': 1, 'sd': 1, 'last': 60,
                      'sets': [{'reps': 10, 'kg': kg - 4, 'expected_kg': kg}]}
    combined = d.combine({'a': [row(60)], 'b': [row(64)]}, [])
    assert combined[0]['sets'][0] == {'reps': 10, 'expected_kg': 62.0, 'kg': 56}
    board = [{'model_version': 'a', 'n': 20, 'mean_abs_error_kg': 1.0}, {'model_version': 'b', 'n': 20, 'mean_abs_error_kg': 3.0}]
    assert d.ensemble_weights(['a', 'b'], board)[0]['a'] == 0.625


def test_backtest_is_walk_forward_and_reproducible():
    from human_model_lift.backtest import InMemoryEvidence, backtest
    from human_model_lift.synthetic import generate
    first = backtest(InMemoryEvidence(generate(weeks=6, seed=3)), YamlCatalog(), KeywordSignals())
    again = backtest(InMemoryEvidence(generate(weeks=6, seed=3)), YamlCatalog(), KeywordSignals())
    assert first['n'] > 0 and first['summary'] == again['summary']
    assert set(first['summary']['all']) == {'n', d.MODEL_VERSION, d.BASELINE_VERSION, d.ENSEMBLE_VERSION, 'last-plus-2.5'}
