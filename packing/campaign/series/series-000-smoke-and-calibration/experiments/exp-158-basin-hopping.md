---
title: exp-158 — basin hopping against multistart over the LP quench, at equal refined optima
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-158
  series: series-000
  title: Basin hopping against multistart over the LP quench, at equal refined optima
  date: '2026-09-08'
  hypotheses:
  - H-160
  tier: exploratory
  subject:
    label: Gensane algorithm 4 with quench_bracket substituted for the greedy billiard
    engine: sqpack.research.quench.quench_bracket 0.1.0 under devtools/run_basin_hopping.py
    engine_commit: 9ae7700
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 53
      rounding: nearest-even
    tolerance: 1e-9 for the independent pose re-check; strict zero penetration for emission
    host_system: Apple M1 Pro class, 10 cores, 32 GB, shared with other agents at load 19 to 37
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: 'multistart: every proposal a fresh uniform scatter, refined by the same quench'
    candidate: 'basin-hop: perturb the incumbent refined optimum, accept only on improvement,
      double the step on success and halve it on failure'
    runs_per_condition: 5
    trials: 20
    interleaved: false
    operator: claude-opus-5
    commit: 9ae7700
    dirty: true
    entry_point: devtools/run_basin_hopping.py
    command: python3 devtools/run_basin_hopping.py --cells 5,10,11,17,19 --seeds 1,2,3,4,5
      --quenches 20 --quench-seconds 4 --eps0 0.1 --out <dir>
    budget: 1,000 refined local optima, 500 per condition, 4,871 s wall
    record: campaign/series/series-000-smoke-and-calibration/results/exp-158-basin-hopping/
  effort:
    timebox: 2h
    wall_seconds: 4871.0
    agent_minutes: 40
    stopped_by: criterion
  results:
  - shape: conditions
    metric: best_side_n11
    role: outcome
    control_median: 4.093022595527
    candidate_median: 3.975619237842
    control_range:
    - 3.976260556953
    - 4.148808948971
    candidate_range:
    - 3.897230786850
    - 3.985709772109
    change_pct: -2.87
    overlapping: true
  - shape: conditions
    metric: best_side_n17
    role: outcome
    control_median: 5.056305082981
    candidate_median: 4.923064570793
    control_range:
    - 4.930211664573
    - 5.058504687651
    candidate_range:
    - 4.825372823030
    - 4.938533843603
    change_pct: -2.63
    overlapping: true
  - shape: conditions
    metric: best_side_n19
    role: outcome
    control_median: 5.325335046242
    candidate_median: 5.239540190914
    control_range:
    - 5.314127279395
    - 5.372525873437
    candidate_range:
    - 5.159620780950
    - 5.306345008317
    change_pct: -1.61
    overlapping: false
  - shape: conditions
    metric: best_side_n10
    role: outcome
    control_median: 3.873290103679
    candidate_median: 3.767766952966
    control_range:
    - 3.850686309126
    - 3.915269463400
    candidate_range:
    - 3.730819660112
    - 3.828427124746
    change_pct: -2.72
    overlapping: false
  - shape: determination
    question: does basin hopping beat multistart by 0.01 on at least three of the five cells
    role: outcome
    outcome: criterion_met
    checked_by: 'four of five cells (n = 10, 11, 17, 19) improve by 0.06 to 0.13 in median,
      with disjoint seed ranges at n = 10 and n = 19; n = 5 regresses by 0.14'
  - shape: record
    metric: best_side
    role: outcome
    direction: lower
    score: 3.897230786850
    standing_best: 3.877083590023
    standing_best_source: frontier/n-011.md (Walter Trump 1979)
    beat_record: false
    runs: 5
  - shape: determination
    question: is every emitted pose a valid packing at the side its line claims
    role: guard
    outcome: criterion_met
    checked_by: 'packing-campaign verify-archive over 50 poses in a separate process,
      sqpack.verify at tolerance 1e-9, zero failures; every pose repaired to strict zero
      penetration before emission'
  complexity:
    lines_changed: 351
    new_dependencies: []
    new_failure_modes:
    - 'The LP quench returns separations non-negative only to solver tolerance, so an
      emitted pose needs a monotone repair before it is a packing. The repair scales
      centres apart and can only raise the reported side.'
    - 'quench_bracket overruns its declared per-call wall bound; a 4 s budget produced
      calls of up to about 30 s, so the refiner is truncated unevenly across proposals.'
    notes: devtools/run_basin_hopping.py, budgeted in refined local optima rather than moves.
  verdict:
    decision: accepted
    primary_criterion: median best_side, basin-hop against multistart at equal quench calls
    reason: 'The proposal structure is worth its complexity at this budget: H-160 declared
      three of five cells improving by 0.01 and four did, two of them with disjoint seed
      ranges, but the other two overlap and no run came within 1e-2 of any record, so this
      accepts a proposer and settles nothing about record-finding.'
    commit: 9ae7700
---
# exp-158 — spending the budget in the currency the record engines use

## What was measured

Both conditions got **exactly 500 quench calls each** — 20 refined local optima per
seed, five seeds, five cells — and differ only in where the proposal comes from.
`multistart` draws a fresh uniform scatter every time.
`basin-hop` perturbs the incumbent refined optimum by `eps`, accepts only on
improvement, doubles `eps` on success and halves it on failure: Gensane and Ryckelynck’s
algorithm 4 with the campaign’s LP-in-cell quench substituted for their greedy billiard.

| cell | record | multistart median / best | basin-hop median / best | median improvement |
| ---: | --- | --- | --- | ---: |
| 5 | `2.707107` | `2.796224` / `2.742256` | `2.940518` / `2.768118` | `-0.144` |
| 10 | `3.707107` | `3.873290` / `3.850686` | `3.767767` / `3.730820` | `+0.106` |
| 11 | `3.877084` | `4.093023` / `3.976261` | `3.975619` / `3.897231` | `+0.117` |
| 17 | `4.675530` | `5.056305` / `4.930212` | `4.923065` / `4.825373` | `+0.133` |
| 19 | `4.885618` | `5.325335` / `5.314127` | `5.239540` / `5.159621` | `+0.086` |

Seed ranges, which the accept rule requires reported next to the medians:

| cell | multistart range | basin-hop range |
| ---: | --- | --- |
| 5 | `[2.742256, 2.828427]` | `[2.768118, 2.942809]` |
| 10 | `[3.850686, 3.915269]` | `[3.730820, 3.828427]` |
| 11 | `[3.976261, 4.148809]` | `[3.897231, 3.985710]` |
| 17 | `[4.930212, 5.058505]` | `[4.825373, 4.938534]` |
| 19 | `[5.314127, 5.372526]` | `[5.159621, 5.306345]` |

## Result

**H-160 is confirmed on its own criterion and the confirmation is narrow.** The declared
threshold was three of five cells improving by `0.01`; four improved, by `0.086` to
`0.133`. Grosso and colleagues’ finding that multistart is the wrong shape for packing
transfers to squares under free rotation.

Three qualifications belong next to that, and the second is the important one.

**Only two of the five cells separate cleanly.** The campaign’s accept rule clause 1
wants the seed ranges disjoint, and they are at `n = 10` (`3.828427` against `3.850686`)
and at `n = 19` (`5.306345` against `5.314127`) — the candidate’s worst seed beats the
control’s best.
At `n = 11` and `n = 17` the ranges overlap, and by that clause those two
cells show no detectable effect however large the median shift looks.
So the verdict rests on two cells that separate, two more that move the median in the
same direction without separating, and one that moves the other way.
This is an exploratory round and is marked so.

**`n = 5` regresses, and it regresses hard.** Basin hopping is `0.144` *worse* than
multistart on the smallest cell, and its worst seed, `2.942809`, is the value five
axis-aligned unit squares need in a `2.943` box — the arm found a structured local
optimum and never left it.
That is exactly the failure Grosso and colleagues describe for too-small a perturbation:
the new start lies in the basin of the current minimiser.
With 20 refinements and a monotone accept rule, the arm has almost no way to escape,
while multistart’s fresh scatters keep sampling until one lands in the `2.7071` funnel.
So the operator that wins on four cells is the operator that loses on the fifth, and
which it will be is not predictable in advance — which is Lai and colleagues’ result on
circles and spheres reproduced here in miniature.

**Nothing came close to a record.** The best result of the whole round is `3.897231` at
`n = 11`, `+2.01e-02` from Trump.
Not one of the 50 emitted packings is within `1e-2` of its record, let alone the `1e-4`
basin proxy or the `1e-6` hit threshold.
Both hit rates are `0/25`.

That `n = 11` number is still worth pausing on, because it is **better than the
annealer’s** at a budget four orders of magnitude smaller in raw operations: the arm-A
control in [exp-156](exp-156-round-1-perturbation.md) reaches `3.922761` as its best of
five seeds at `1e10` pair tests per seed, and 20 quench calls beat it.
Refined local optima are worth far more per unit than annealing moves, exactly as the
survey argues — and 20 of them is still three orders of magnitude short of the `10^3`
per record hit that Ellsworth’s statistics price a record at.

## What the prediction got wrong

The claim was right and the reason was partly wrong.
H-160’s registered kill condition anticipated a refutation reading as “the quench is too
weak a refiner for the proposal structure to matter”, echoing
[exp-006](exp-006-lp-quench-n5-n10-n11.md)’s “the quench is a polisher, not a rescue”.
The proposal structure mattered a great deal — 0.13 at `n = 17` is ten times the
declared threshold — so the quench is strong enough for the proposer to be visible
through it.

What was not anticipated is that the arm would fail *upward in structure and downward in
`n`*: the cell it loses is the one where the answer is a small symmetric arrangement a
random scatter finds by luck.

## Two instrument findings, recorded because they bound the result

**The quench does not honour its wall budget.** `quench_bracket(time_budget=4.0)`
produced individual calls of up to roughly 30 seconds, because the budget is tested
between solver operations and a single fixed-point solve can run long past it.
So the two conditions got equal *calls* but unequal *work* per call, and the refiner is
truncated unevenly. The budget currency is still the honest one — a call is what the
proposer buys — but a per-call CPU bound would make the comparison sharper.

**An LP solution is not a packing until it is repaired.** The quench enforces
separations to solver tolerance, so a returned configuration routinely has pairs
penetrating by around `1e-16`. Emitting those with `overlap: 0` would have been a
fabricated guard. Every pose is instead scaled apart about its own centroid by the
smallest factor that removes all penetration — monotone, so it can only *raise* the
reported side — then re-checked by `sqpack.verify`, and 50 of 50 emitted poses pass an
independent verification in a separate process.

## Limits

- Five cells, all `n <= 19`, because one quench call at `n = 27` or above does not
  finish inside any budget this round could afford.
  Nothing here transfers to the larger half of the subset.
- 20 refined optima per seed against the `10^3` per record hit that Ellsworth’s `n = 51`
  statistics imply. This round cannot see a record-rate effect and does not claim to.
- One perturbation schedule (`eps0 = 0.1`, doubling and halving) and one accept rule
  (monotone). Grosso and colleagues’ sweep found a threefold difference in failure count
  across four magnitudes, so this is one point in a plane known to matter.
- The funnel-restart branch never fired: `eps` did not collapse below `1e-6` inside 20
  refinements on any seed, so the arm as measured is single-funnel basin hopping with no
  restart, which is a weaker algorithm than the one the code implements.
- `f64` throughout, and `numerically-checked` assurance only.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
