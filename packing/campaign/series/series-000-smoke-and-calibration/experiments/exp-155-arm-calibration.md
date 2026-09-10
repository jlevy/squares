---
title: exp-155 — calibrating the move-set arms on held-out cells, and the ablation that backfired
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-155
  series: series-000
  title: Calibrating the move-set arms on held-out cells, and the ablation that backfired
  date: '2026-09-08'
  hypotheses:
  - H-158
  tier: exploratory
  subject:
    label: sqsearch with the arm flags, four calibration passes on non-scoring cells
    engine: sqsearch 0.1.0 with --p-perturb, --perturb-scale, --mu0/--mu1, --budget-pair-tests
    engine_commit: 9ae7700
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 53
      rounding: nearest-even
    tolerance: 1e-9 for the independent pose re-check; 1e-12 for the engine's own feasibility screen
    host_system: Apple M1 Pro class, 10 cores, 32 GB, shared with other agents at load 12 to 95
    selftest_passed: true
  instance:
    axis: n
    point: 18
    role: calibration
  method:
    control: sqsearch at its defaults, no arm flag named
    candidate: 'nine, twelve, seven and eight flag groups over four passes: p_perturb in
      [0.02, 1.0], perturb_scale in [0.5, 4], mu in [0.02, 50] ramped and flat, t_hot in
      [0.25, 4.0], p_reseed 0, steps 4e6'
    runs_per_condition: 3
    interleaved: true
    operator: claude-opus-5
    commit: 9ae7700
    dirty: true
    entry_point: devtools/run_arm_sweep.py
    command: python3 devtools/run_arm_sweep.py <plan>.yaml --out <pass>
    budget: 1.13e12 pair tests over four passes, 2,681 s wall
    record: campaign/series/series-000-smoke-and-calibration/results/exp-155-arm-calibration/
  effort:
    timebox: 90m
    wall_seconds: 2681.0
    agent_minutes: 95
    pair_tests: 1130000000000
    stopped_by: criterion
  results:
  - shape: conditions
    metric: best_side_n18_stock_budget
    role: mechanism
    control_median: 5.0
    candidate_median: 4.845902
    control_range:
    - 5.0
    - 5.0
    candidate_range:
    - 4.840488
    - 4.913694
    change_pct: -3.08
    overlapping: false
  - shape: conditions
    metric: best_side_n18_round_budget
    role: outcome
    control_median: 5.0
    candidate_median: 4.834329
    control_range:
    - 5.0
    - 5.0
    candidate_range:
    - 4.831435
    - 4.874385
    change_pct: -3.31
    overlapping: false
  - shape: determination
    question: does raising the annealing temperature alone leave the trivial grid at n = 18
    role: guard
    outcome: no_progress
    checked_by: 'four temperatures from 0.25 to 4.0, three seeds each, every seed returning
      exactly 5.0; poses re-checked by packing-campaign verify-archive'
  - shape: determination
    question: does lengthening the anneal alone leave the trivial grid at n = 18
    role: mechanism
    outcome: criterion_met
    checked_by: '--steps 4000000, single-square moves only, median 4.914602 against the
      control 5.0 on three seeds; poses re-checked by packing-campaign verify-archive'
  - shape: determination
    question: is every archived pose a valid packing at the side its line claims
    role: guard
    outcome: criterion_met
    checked_by: 'packing-campaign verify-archive over 1,944 poses in a separate process,
      sqpack.verify at tolerance 1e-9, zero failures, zero candidates below any record'
  complexity:
    lines_changed: 236
    new_dependencies: []
    new_failure_modes:
    - 'A perturbation arm has a different wall cost per pair test from the control, so
      equal pair tests is not equal seconds. Reported as a cost, never as an outcome.'
    notes: 'Rust: three flag groups plus a pair-test budget, all off by default, with four
      new selftest checks. Python: devtools/run_arm_sweep.py.'
  verdict:
    decision: baseline
    primary_criterion: best_side on the held-out cells n = 18 and n = 40
    reason: 'Calibration, not a scored round: it freezes p_perturb = 1.0, perturb_scale = 2
      and a flat mu = 5 for exp-156 and exp-157, and it turned up a schedule-length effect
      that is now registered as H-161 rather than folded into an arm.'
    commit: 9ae7700
---
# exp-155 — what the arms were tuned to, and on what

## Why a calibration round exists at all

Arm B has two free parameters and arm C has one.
Choosing them on the cells that score them is how a campaign measures its own tuning and
calls it a result.
So this round runs on `n = 18` and `n = 40` — both non-grid, so no arm
can score by returning the incumbent grid, and **neither appears in the eleven-cell
subset** that [exp-156](exp-156-round-1-perturbation.md),
[exp-157](exp-157-round-1-pressure.md) and [exp-159](exp-159-round-1-schedule.md) score.

Four passes, each with its plan file written before it ran and retained beside its
archive.

## Pass 1: the survey’s recommended value does nothing

The 2026-09-08 survey proposes `p_perturb = 0.05`. At `2e8` pair tests per chain,
`p_perturb` at `0.02`, `0.05` and `0.15`, and `perturb_scale` at `1` and `4`, every seed
of every arm returned **exactly the trivial grid** — `5.0` at `n = 18` and `7.0` at
`n = 40`, indistinguishable from the control.
So did every wall-pressure weight from `0.02` to `0.5`.

One arm did not: `p_perturb = 0.50`, the largest value in the sweep, reached a median
`4.935182`. That is not a bracketed optimum, it is the edge of the grid that was swept,
which is why there was a pass 2.

## Pass 2: the optimum is at the far end, and it is not where the survey said

| arm | `n = 18` median | best | seeds |
| --- | --- | --- | --- |
| A-control | `5.000000` | `5.000000` | `[5.0, 5.0, 5.0]` |
| B-p030-s1 | `4.970585` | `4.929842` | `[4.929842, 4.970585, 5.0]` |
| B-p050-s1 | `4.935182` | `4.903448` | `[4.903448, 4.935182, 4.938222]` |
| B-p050-s2 | `4.909668` | `4.839852` | `[4.839852, 4.909668, 4.963692]` |
| B-p070-s1 | `4.931023` | `4.835609` | `[4.835609, 4.931023, 4.946326]` |
| B-p090-s1 | `4.956294` | `4.889112` | `[4.889112, 4.956294, 4.978824]` |
| **B-p100-s1** | **`4.845902`** | `4.840488` | `[4.840488, 4.845902, 4.913694]` |
| C-flat-mu5 | `4.956999` | `4.952302` | `[4.952302, 4.956999, 4.958631]` |
| C-mu2, C-mu20 | `5.000000` | `5.000000` | grid on every seed |

Two things in that table are worth more than the parameter it picks.

**The best value of `p_perturb` is 1.0, which switches the stock move set off
entirely.** At `p_perturb = 1.0` no single-square proposal is ever made; every proposal
displaces all eighteen squares at once.
The survey’s recommendation was `0.05`, twenty times smaller, and at `0.05` the arm is
indistinguishable from the control.

**Ramping the pressure down does not work; holding it constant does.** `C-mu2` and
`C-mu20`, ramped from their value to `1e-6` across the anneal, returned the grid on
every seed, while `C-flat-mu5` at constant weight beat it on three of six.
A term ramped over 400,000 steps is negligible for almost the whole anneal, which is
what the ramp was doing.

## Pass 3: the ablation that was supposed to close the question, and opened one

A whole-configuration perturbation at scale `temperature` moves the state much further
per proposal than a single-square move does.
Before pass 2 could be read as “the collective move matters”, the alternative had to be
excluded: that arm B is a hotter search wearing a structural costume.

| arm | `n = 18` median | `n = 40` median |
| --- | --- | --- |
| A-control (`t_hot = 0.25`) | `5.000000` | `7.000000` |
| A-hot050, A-hot100, A-hot200, A-hot400 | `5.000000` | `7.000000` |
| A-reseed0 | `5.000000` | `7.000000` |
| **A-steps4M** | **`4.914602`** | `7.000000` |

Raising the temperature by a factor of **sixteen** changes nothing.
Not one seed of twelve left the grid.
Turning off reseeding changes nothing.
So arm B’s effect is not exploration temperature, and the guard did its job.

The seventh arm was not a temperature change.
`--steps 4000000` lengthens each anneal tenfold, so the same pair-test budget buys a
tenth as many restarts, each cooled ten times more slowly — and it left the grid on
three seeds of six, with single-square moves only.

That is a positive from an ablation designed to produce a negative.
It is registered as [H-161](../../../hypotheses/H-161-cooling-schedule-length.md) and
scored in its own round rather than written up here, because a finding discovered while
calibrating is a hypothesis, not a result.

## Pass 4: the finalists at the budget that will score them

A parameter that wins at a sixth of the budget is not the same claim as a parameter that
wins at the budget being scored, so the finalists were re-run at exactly round 1’s
`1.25e9` pair tests per chain.

| arm | `n = 18` median | best | median gap |
| --- | --- | --- | --- |
| A-control | `5.000000` | `5.000000` | `+1.77e-01` |
| B-p050-s2 | `4.870978` | `4.839852` | `+4.81e-02` |
| B-p070-s2 | `4.888341` | `4.831647` | `+6.55e-02` |
| B-p100-s05 | `4.922989` | `4.878292` | `+1.00e-01` |
| B-p100-s1 | `4.840484` | `4.831300` | `+1.76e-02` |
| **B-p100-s2** | **`4.834329`** | `4.831435` | `+1.15e-02` |
| C-flat-mu5 | `4.952937` | `4.952302` | `+1.30e-01` |
| C-flat-mu50 | `5.000000` | `5.000000` | `+1.77e-01` |

**Frozen for round 1:** arm B is `--p-perturb 1.0 --perturb-scale 2`; arm C is
`--mu0 5.0 --mu1 5.0`; the long schedule is `--steps 4000000`.

The `n = 18` record is Hämäläinen’s `4.822876`, so arm B’s median is `+0.0115` from a
1980 hand construction, cold, in about twenty seconds of a loaded machine.
Its worst seed is `4.874385`. The control is at `5.0` on every seed of every pass.

## The mechanism, measured rather than argued

The survey lists among the things it could not establish that its structural argument
“predicts a specific plateau statistic that no experiment here has yet measured”.
`devtools/measure_objective_sparsity.py` measures it, by drawing proposals from the same
two distributions the engine draws from and counting what each does to `required_side`.

At the **trivial grid**, over 8,000 proposals per kind per cell, at proposal scales
`0.01`, `0.05` and `0.2` alike:

| cell | single-square proposals that *lower* the side | that change it at all | collective proposals that lower it |
| ---: | ---: | ---: | ---: |
| 5 | `0.0646` | `0.4716` | `0.054` to `0.071` |
| 10 | **`0.0000`** | `0.3488` | `0.0041` to `0.0068` |
| 11 | **`0.0000`** | `0.3038` | `0.0034` to `0.0051` |
| 17 | **`0.0000`** | `0.2801` | `0.0006` to `0.0009` |
| 19 | **`0.0000`** | `0.2465` | `0.0000` to `0.0005` |
| 26, 27, 29, 37, 50, 52 | **`0.0000`** | `0.24` down to `0.17` | `0.0000` |

The survey’s claim is that *most* single-square moves are no-ops.
The measurement is stronger and simpler: at the trivial grid, for every cell in the
subset except `n = 5`, **no single-square proposal lowers the objective at all**, at any
scale tried. The grid is a strict local minimum of `required_side` under the entire
single-square move set, and the reason is that its binding span is attained by a whole
row or column of `m` squares at once, so no single square is the unique extremum whose
retreat could shrink it.
A quarter to a third of proposals *change* the side, and every one of them raises it.

That explains pass 3 exactly.
No temperature can help, because there is no downhill single-square direction to find at
any temperature; the number of admissible improving proposals is not small, it is zero.

Off the grid the picture inverts.
Probing arm B’s own emitted `n = 18` configurations at side `4.84`, **3.5 %** of
single-square proposals lower the side.
So the single-square move set is not weak in general — it is exactly, and only, useless
at the configuration every chain starts from and keeps falling back into.

## What the prediction got wrong

Right about the mechanism, wrong about the dose and wrong about the exclusivity.

The survey predicted the move would help at `p_perturb = 0.05`. At that value it does
nothing measurable. It works at `1.0`, where the move it was supposed to supplement no
longer runs at all. “Add a proposal at 5 %” and “replace the proposal distribution” are
different changes, and only the second one moved the number.

And the ablation meant to establish that the move set is the whole story found that a
schedule-length change gets a good part of the way on its own.
The survey’s section 4 is titled “the move set, not the cooling schedule”, and on the
evidence here that dichotomy is too clean: schedule *shape* and *temperature* are inert,
schedule *length* is not.

## Limits

- Two held-out cells and three seeds per arm.
  This round chooses parameters; it decides nothing.
- `n = 40` never left the grid under any of the 36 arm-configurations tried, at this
  budget. The calibration is therefore effectively an `n = 18` calibration, and whether
  the chosen point transfers is what round 1 measures.
- The parameter planes are swept coarsely and one factor at a time.
  Nothing here brackets an optimum in `(p_perturb, perturb_scale)` jointly.
- Wall-clock figures in this round are uninterpretable as costs: the host carried other
  agents’ work throughout, with the one-minute load average moving between `12` and `95`
  on ten cores. That is why the budget is denominated in pair tests, and why the arms
  were compared at equal pair tests rather than equal seconds.
- `f64` screening. Every archived pose was rebuilt and re-decided by `sqpack.verify` in a
  separate process at tolerance `1e-9` — 1,944 poses, zero failures — which refutes a
  forged pose and certifies nothing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
