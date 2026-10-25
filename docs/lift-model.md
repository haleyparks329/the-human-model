# Lift model

Predicts the working sets of the next session of each routine, explains every
number, and scores itself against what was lifted. Code: `src/human_model_lift/`.

## The nightly loop (production)

1. Snapshot the current routines (a new row only when they change).
2. Learn from scored outcomes how each kind of contributor moved the loads.
3. Let every registered model predict the next session of every routine done in
   the last 28 days, and combine them.
4. Store each model's run in an append-only ledger.

After a workout syncs, the latest prediction made before it is scored for every
model. `backtest.py` replays the same loop over history, walk-forward.

## Estimating strength

Each session gives an estimated one-rep max per lift (Epley, from sets of 1–12
reps; 13–30 reps only when nothing else exists). A two-state Kalman filter tracks
level and trend per lift. Session noise and level drift are picked nightly from a
grid by one-session-ahead error on the last 180 days, so the filter adapts to how
noisy this athlete's logs are. The trend is clamped to about −1.4% to +2.5% a week.

## From estimate to sets

**Progression type.** A lift named in a current strength goal, or prescribed at
6 reps or fewer, progresses by load. Rep-range work progresses by reps until
every set reaches the target, then by one step.

**Strength lifts** step from the last session toward the estimate: at least one
step, at most +10%.

**Steps and rounding.** The step is the median of the athlete's past increases on
that lift; rounding uses the equipment step from the exercise rules (2.5 kg for a
barbell, 1 kg for a cable stack).

**Gaps.** A gap is long relative to how often the athlete normally does that lift
(1.75 times the usual interval, at least 10 days), not a fixed week. After one,
the recommendation drops 10%.

**Swaps.** A new exercise is its own lift (loads are not comparable across
equipment); the prediction names what it replaced. A substitute from the same
group is scored `substituted`, not `missed`.

## Expected and recommended

Each set has `expected_kg`, what the athlete will most likely lift (model plus
learned effects), and `kg`, the recommendation. What the athlete said shapes the
recommendation immediately:

| Signal | Recommendation |
|---|---|
| Pain in a region (elbow, knee, back...) | Hold the load on exercises that load that region |
| "Drop the weight" about this lift | One step lighter |
| "It flew" about this lift | Allow a step |
| Tiredness, stress, low mood | Note only (they did not predict lower loads) |

Sleep and HRV against the athlete's own 28-day baseline are recorded the same
way, as notes.

## Learning

`learn_effects` compares the "surprise" (actual against the plain model, relative
to the last load) on outcomes with and without each contributor. An effect is
adopted only with at least 20 cases on each side, a mean shift of 2% or more with
70% of cases agreeing, fitted on the older two thirds, and only if it also
reduces error on the newest third.

## Models and combination

Models share one signature, so a new one is a function added to `domain.MODELS`.
The champion is the lowest mean absolute error on the expected top load over the
last 60 days, among models with at least 10 outcomes. The ensemble averages
expected loads equally until every model has 20 outcomes, then uses inverse
recent error shrunk halfway to equal, and recommends the most cautious load.

## Limits

- Estimates are working capacity at the usual effort, not tested maxima.
- Past prescriptions before the first routine snapshot are unknown, so the
  backtest does not use performed reps as targets.
- The keyword reader is crude; every match is stored with its sentence so it can
  be checked, and a language model's structured reading replaces it in production.
