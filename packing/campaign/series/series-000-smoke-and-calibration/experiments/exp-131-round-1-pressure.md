---
title: exp-131 — the wall-pressure term makes the search worse, and says why the surrogate is wrong
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-131
  series: series-000
  title: The wall-pressure term makes the search worse, and says why the surrogate is wrong
  date: '2026-09-08'
  hypotheses:
  - H-126
  tier: exploratory
  subject:
    label: sqsearch --mu0 5.0 --mu1 5.0, against the stock annealer
    engine: sqsearch 0.1.0 with the arm flags
    engine_commit: 9ae7700
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 53
      rounding: nearest-even
    tolerance: 1e-9 for the independent pose re-check; 1e-12 for the engine's own feasibility screen
    host_system: Apple M1 Pro class, 10 cores, 32 GB, shared with other agents at load 17 to 52
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: sqsearch at its defaults, energy = required_side + lambda * total_overlap
    candidate: the same energy plus mu * spread, at constant mu = 5
    runs_per_condition: 5
    interleaved: false
    operator: claude-opus-5
    commit: 9ae7700
    dirty: true
    entry_point: devtools/run_arm_sweep.py
    command: python3 devtools/run_arm_sweep.py plan-part-3.yaml --out part-3
    budget: 1.25e9 pair tests per chain, 8 chains, 5 seeds, 11 cells
    record: campaign/series/series-000-smoke-and-calibration/results/exp-130-round-1/
  effort:
    timebox: 2h
    wall_seconds: 2349.0
    agent_minutes: 25
    pair_tests: 553480000000
    stopped_by: criterion
  results:
  - shape: conditions
    metric: best_side_n5
    role: guard
    control_median: 2.707106793025
    candidate_median: 2.828427126000
    control_range:
    - 2.707106787735
    - 2.707106805215
    candidate_range:
    - 2.828427126000
    - 2.828427126000
    change_pct: 4.48
    overlapping: false
  - shape: conditions
    metric: best_side_n11
    role: outcome
    control_median: 3.935790212325
    candidate_median: 4.0
    control_range:
    - 3.922760527419
    - 3.946821043844
    candidate_range:
    - 4.0
    - 4.0
    change_pct: 1.63
    overlapping: false
  - shape: conditions
    metric: best_side_n17
    role: outcome
    control_median: 5.0
    candidate_median: 4.937931855
    control_range:
    - 4.997152231858
    - 5.0
    candidate_range:
    - 4.933367020
    - 4.938784435
    change_pct: -1.24
    overlapping: false
  - shape: determination
    question: does the candidate lower the median best side by 0.01 with disjoint seed ranges
      on at least six of the eleven cells
    role: outcome
    outcome: criterion_missed
    checked_by: 'one cell (n = 17) improves; three (n = 5, 10, 11) regress, two of them past
      a proved optimum the control reaches; six improvements were required'
  - shape: determination
    question: does the n=10 positive control land within 1e-2 of its proved value
    role: guard
    outcome: no_progress
    checked_by: 'candidate median 3.883618 against the proved 3.707107, a gap of 1.77e-01;
      the control lands at 7.08e-04'
  - shape: determination
    question: is every archived pose a valid packing at the side its line claims
    role: guard
    outcome: criterion_met
    checked_by: 'packing-campaign verify-archive over 495 poses in a separate process,
      sqpack.verify at tolerance 1e-9, zero failures, zero candidates below any record'
  complexity:
    lines_changed: 34
    new_dependencies: []
    new_failure_modes:
    - 'The term is a different objective from the one reported, so it can steer the search
      to a configuration that is compact but not square. That is what it did.'
    notes: geom::spread plus a two-flag ramp; the reported side is still required_side under the overlap gate.
  verdict:
    decision: rejected
    primary_criterion: median best_side, candidate against control, at equal pair-test budget
    reason: 'The criterion was measured and missed in the wrong direction: one cell of
      eleven improves and three regress, including both proved controls, so the aggregate
      compaction surrogate is not a weak version of the inflation formulation but a
      different and worse objective, and it should not be carried.'
    commit: 9ae7700
---
# exp-131 — the cheap substitute for inflation, and why cheap was the wrong axis

## What was measured

The same eleven non-grid cells, the same five seeds, the same `1.25e9` pair tests per
chain, and the same control as [exp-130](exp-130-round-1-perturbation.md) — the two arms
ran from the same plan and their delivered budgets are identical to four figures
(`5.5348e11` pair tests each).
The only change is the energy:

```
F = required_side + lambda * total_overlap + mu * spread
```

with `spread` the mean squared distance of the centres from the centre of their own
bounding box and `mu` held at `5`. `best_side` is still tracked from `required_side`
under the overlap gate, so the term can steer the search and can never flatter the
number.

| cell | record | control median / best | candidate median / best | change |
| ---: | --- | --- | --- | --- |
| 5 | `2.707107` | `2.707107` / `2.707107` | `2.828427` / `2.828427` | **`+0.121` worse** |
| 10 | `3.707107` | `3.707815` / `3.707526` | `3.883618` / `3.883050` | **`+0.176` worse** |
| 11 | `3.877084` | `3.935790` / `3.922761` | `4.000000` / `4.000000` | **`+0.064` worse** |
| 17 | `4.675530` | `5.000000` / `4.997152` | `4.937932` / `4.933367` | `-0.062` better |
| 19 | `4.885618` | `5.000000` / `5.000000` | `5.000000` / `5.000000` | `0` |
| 26 | `5.621320` | `6.000000` / `6.000000` | `6.000000` / `5.975125` | `0` |
| 27, 29, 37, 50, 52 | — | grid on every seed | grid on every seed | `0` |

| arm | verified poses | beating the grid | basin `1e-4` | hits `1e-6` | below any record |
| --- | ---: | ---: | ---: | ---: | ---: |
| control | 495 ok | 16/55 | 5 | 5 | 0 |
| candidate | 495 ok | 16/55 | **0** | **0** | 0 |

## Result

**H-126 is refuted, and the arm is harmful.** One cell of eleven improves against six
required, and three regress — including both proved controls, which the accept rule’s
clause 4 exists to protect.

The regressions are the informative part, because they are not noise.

**At `n = 5` every seed returns exactly `2.828427126`.** That is `2 * sqrt(2)`, the side
of the container that holds five unit squares in the compact 45°-rotated cross, and it
is `0.121` above the proved optimum `2 + 1/sqrt(2)` that the control reaches on every
seed to `1.2e-08`. The pressure term found the arrangement that minimises *spread* and
stopped there. The engine selftest’s own `s(5)` positive control still passes, because
the selftest runs the control parameters; the arm fails a control the control passes.

**At `n = 11` every seed returns exactly `4.0`, the trivial grid**, where the control
reaches `3.935790`. The pressure term made the grid *more* attractive than it already
was, which is the opposite of the intent.

**The one improvement is at `n = 17`**, from `5.000000` to `4.937932` with disjoint
ranges — real, and a quarter of what the perturbation arm gets on the same cell.

## Why it failed, and what that says about the formulation it stood in for

The term was registered as a **surrogate** for the inflation formulation, and the
registry artifact says so: inflation replaces the max over the two to four extreme
squares with a min over the active contact set, while `mu * spread` replaces nothing and
adds a dense term alongside.

The measurement says the surrogate is not a weak version of that idea.
It is a *different objective* whose minimiser is a different object.
`required_side` is minimised by a tight square; `spread` is minimised by a disc.
Where the two disagree — and at `n = 5` and `n = 11` they disagree exactly at the
optimum — the search follows the term it can feel everywhere rather than the one it is
scored on. Making the objective dense was the right diagnosis, and making it dense with
*this* function was the wrong prescription.

[exp-129](exp-129-arm-calibration.md) already showed that the term does nothing when
ramped down and something when held constant, over `mu` from `0.02` to `50`, three
orders of magnitude.
Together with this round, the reading is that the useful range is empty: small `mu` is
inert and large `mu` optimises the wrong thing.

**This does not refute the inflation formulation, and the two must not be conflated.**
What it refutes is the cheap substitute.
The honest consequence is that the inflation rewrite has to be built and measured on its
own, and a round-2 arm that claims to test “wall pressure” should implement a
*directional* term — Squarl pushes each square from the container boundary it is
nearest, which has no reason to prefer a disc — rather than this isotropic one.

## What the prediction got wrong

The registered kill condition anticipated the shape of the failure and got the mechanism
right in one sentence: “a plausible failure mode is that the term helps early and hurts
late, and the ramp is the only thing standing between those.”
The ramp was the thing that was removed, on exp-129’s evidence that the ramped versions
did nothing at all, and removing it produced exactly the predicted harm.
So both settings fail for the same reason and the parameter has no window.

What was not anticipated is that the harm would be *exact and structural* rather than
noisy: `2 * sqrt(2)` on every seed at `n = 5`, `4.0` on every seed at `n = 11`. An arm
that lands on a named wrong answer with zero spread is telling you what it optimised,
and that is more useful than a merely worse number.

## Limits

- One functional form, one constant weight, on top of exp-129’s ramped sweep from `0.02`
  to `50`. This refutes the isotropic mean-squared-offset surrogate and nothing wider.
- `f64` screening; 495 poses independently re-checked at tolerance `1e-9`, zero
  failures.
- Wall clock is not comparable across arms here: the host carried other agents’ work at
  load 17 to 52 on ten cores.
  The delivered pair-test budget is identical to the control’s, which is the comparison
  that matters.
- The candidate never reported a side below a standing best, so no promotion question
  arises.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
