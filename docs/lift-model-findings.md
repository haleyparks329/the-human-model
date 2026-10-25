# Lift model: what the data said

Summary of the experiments recorded in the private science journal (one
append-only entry per experiment, failures included). Results are aggregates
from one athlete (me), September to October 2026; no individual sessions or
measurements are published.

## 1. The estimator beats "same as last time", narrowly

The coaching agent was progressing deadlifts by a fixed +2.5 kg with no
expectation to check against. Walk-forward over 68 predictions, mean absolute
error on the expected top-set load:

| Model | Error |
|---|---|
| Lift model without message signals | **2.4 kg** |
| Lift model with signals | 2.5 kg |
| Same as last time | 2.6 kg |
| Last + 2.5 kg | 3.2 kg |

Strength lifts alone: 8.3 kg against 13.3 kg. The first version lost to the
baseline (4.4 kg against 2.7 kg) because a ±5% strength cap could not follow
early-block jumps; the cap became +10% anchored on the last session.

## 2. What I say does not predict what I lift

Tiredness, stress and "exhausted" messages appeared in most 3-day windows and
made predictions worse when they lowered the expectation (3.2–3.7 kg against
2.5 kg). I often lifted the same or more after saying I was tired. The design
split each prediction into an expected load and a recommendation: what I say
changes the recommendation (a pain report holds the load), and changes the
expectation only after it passes the learning rule.

## 3. Learning needs held-out evidence

Effects fitted on all outcomes looked plausible and made later predictions worse
(2.7–3.0 kg against 2.4 kg). The current rule needs 20 cases with and without a
signal, a consistent direction, and improvement on the newest third. On the
current data it adopts nothing, which is the honest answer.

## 4. No readiness score predicted performance

Readiness scores built from the published inputs of WHOOP, Oura, Garmin and
Apple (approximations with assumed weights, not the vendors' scores), an HRV
smallest-worthwhile-change guideline, and a personal model that adds my own
reports, were compared with performance per training day (relative change of
top loads) by Spearman rank correlation. Over 39 days every model was between
−0.15 and 0.16: effectively zero. The registry keeps scoring them nightly; a
model is called predictive only with at least 20 days and ρ ≥ 0.3. Because of
this, missing wearable data now means "maintain", not caution.

## 5. Bugs the first live run found

- A gap rule with a fixed 7-day threshold fired on lifts done weekly; it became
  relative to each lift's usual interval.
- The backtest used performed reps as targets, which leaked the answer.
- "chin" (a body region) matched inside "Machine"; regions now match word starts.
- Lifts done only at 15 reps had no history; high-rep sets now count when
  nothing else exists.
- "less exhausted" was read as exhaustion; a negation guard fixed it.

Each fix has a regression test in `tests/`.
