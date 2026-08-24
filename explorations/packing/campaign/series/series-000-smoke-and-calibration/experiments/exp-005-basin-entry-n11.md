---
title: exp-005 — basin entry at n = 11, from inside Trump's packing
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-005
  series: series-000
  title: Basin entry at n = 11, perturbing outward from Trump's exact packing
  date: '2026-08-23'
  hypotheses: [H-018]
  tier: exploratory
  subject:
    label: sqsearch local quench and stock schedule, seeded from the exact packing
    engine: sqsearch 0.1.0
    engine_commit: '41b3e18'
    precision: f64_screen
    host_system: Linux container, 8 cores (remote session)
    selftest_passed: true
  instance: {axis: n, point: 11, role: target}
  method:
    control: 'eps = 0: the unperturbed seed, which must return unchanged'
    candidate: 'uniform perturbation of every pose by eps, then anneal; three arms'
    runs_per_condition: 40
    interleaved: false
    operator: claude-opus-5
    commit: '41b3e18'
    entry_point: explorations/packing/run_basin_entry.sh
    command: 'sqsearch --basin-entry --seed-config <trump11.json> --eps 0,1e-5,1e-4,1e-3,1e-2,1e-1 --trials 40, over three arms'
    budget: '720 trials, 77.1 s engine wall'
    record: campaign/series/series-000-smoke-and-calibration/results/exp-005-basin-entry.jsonl
  effort:
    timebox: 90m
    wall_seconds: 77.1
    agent_minutes: 75
    stopped_by: criterion
  results:
  - shape: determination
    question: 'does the search return to within 1e-6 of Trump''s configuration in at least half of runs at eps = 1e-3'
    role: outcome
    outcome: no_progress
    checked_by: 'max_dev against the seed, both configurations normalised to their bounding box; 0 of 40 trials in every arm'
  - shape: conditions
    metric: max_dev_at_eps_1e-3
    role: outcome
    control_median: 0.0
    candidate_median: 0.002322
    control_range: [0.0, 0.0]
    candidate_range: [1.216e-05, 8.731e-02]
    overlapping: false
  - shape: conditions
    metric: max_dev_over_eps_ratio_by_effort
    role: mechanism
    control_median: 11.13
    candidate_median: 4.93
    control_range: [11.13, 11.13]
    candidate_range: [4.93, 4.93]
    overlapping: false
  - shape: record
    metric: best_side_gap_at_eps_1e-5
    role: mechanism
    direction: lower
    score: 1.413e-10
    standing_best: 0.0
    standing_best_source: 'frontier/n-011.md (Trump 1979), as the seed itself'
    beat_record: false
    runs: 40
  - shape: determination
    question: 'does the campaign''s stock schedule (t_hot = 0.25) hold the basin when started inside it'
    role: outcome
    outcome: no_progress
    checked_by: 'hot arm, median max_dev 2.2-2.7 at every eps including 1e-5; median side gap 0.23-0.27'
  complexity:
    lines_changed: 232
    new_dependencies: []
    new_failure_modes: ['seed export is a one-way door out of the exact field; nothing downstream may certify']
    notes: 'Adds --basin-entry to the engine, tools/export_trump11.py, and run_basin_entry.sh.'
  verdict:
    decision: rejected
    primary_criterion: max_dev
    reason: >-
      Refutes H-018 as stated - 0 of 40 trials return within 1e-6 at eps = 1e-3 in any
      arm - but the shape of the failure is the result: the return distance scales
      linearly with eps with no threshold, and halves when the effort is multiplied by
      ten, so what was measured is the refiner's convergence rate, not a basin wall.
    commit: '41b3e18'
---
# exp-005 — basin entry at `n = 11`

## What was measured

Trump’s exact packing, exported to `f64` poses, perturbed by uniform noise of size `eps`
on every coordinate and angle, then annealed — 40 independent trials at each of six
`eps` values, in three arms:

| Arm | Schedule | The question it asks |
| --- | --- | --- |
| `quench-1x` | `t_hot = eps`, 400 k steps | does the configuration have an attracting neighbourhood? |
| `quench-10x` | `t_hot = eps`, 4 M steps | is reaching it bounded by the landscape, or by effort? |
| `hot` | `t_hot = 0.25`, 400 k steps | does the annealer `exp-003` actually ran hold the basin when handed it? |

The `hot` arm is the campaign’s own default schedule.
The two quench arms tie the starting temperature to the perturbation, which is what
makes them a *local* quench: a chain started `1e-3` away and then heated to `0.25` has
left the neighbourhood before its first accepted move.

Return is scored by `max_dev` — the largest per-coordinate deviation from the seed,
after normalising both configurations to their bounding box, with angles compared modulo
`π/2`. Normalisation matters: `required_side` is translation-invariant, so an
un-normalised comparison would measure drift rather than the basin.

## Result

| Arm | `eps` | median `max_dev` | range | median side gap | best side gap | returns ≤ `1e-6` |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| `quench-1x` | `1e-5` | `1.210e-04` | `[3.85e-05, 2.71e-04]` | `3.071e-05` | `8.300e-06` | 0/40 |
| `quench-1x` | `1e-4` | `1.092e-03` | `[2.88e-04, 3.01e-03]` | `3.147e-04` | `7.775e-05` | 0/40 |
| `quench-1x` | `1e-3` | `1.190e-02` | `[4.41e-03, 2.44e-02]` | `3.428e-03` | `1.084e-03` | 0/40 |
| `quench-1x` | `1e-2` | `1.170e-01` | `[3.81e-02, 3.86e-01]` | `3.704e-02` | `9.862e-03` | 0/40 |
| `quench-1x` | `1e-1` | `1.026e+00` | `[7.32e-01, 1.98e+00]` | `1.918e-01` | `1.229e-01` | 0/40 |
| `quench-10x` | `1e-5` | `6.511e-06` | `[7.33e-10, 1.79e-04]` | `1.133e-06` | `1.413e-10` | **12/40** |
| `quench-10x` | `1e-4` | `1.159e-04` | `[2.31e-06, 6.84e-03]` | `1.385e-05` | `2.996e-07` | 0/40 |
| `quench-10x` | `1e-3` | `2.322e-03` | `[1.22e-05, 8.73e-02]` | `3.928e-04` | `2.259e-06` | 0/40 |
| `quench-10x` | `1e-2` | `6.244e-01` | `[7.93e-03, 8.21e-01]` | `2.468e-02` | `1.458e-03` | 0/40 |
| `quench-10x` | `1e-1` | `2.123e+00` | `[1.56e+00, 3.00e+00]` | `1.229e-01` | `2.019e-02` | 0/40 |
| `hot` | `1e-5` | `2.672e+00` | `[1.69e+00, 3.77e+00]` | `2.733e-01` | `1.229e-01` | 0/40 |
| `hot` | `1e-3` | `2.280e+00` | `[1.54e+00, 3.23e+00]` | `2.436e-01` | `1.229e-01` | 0/40 |
| `hot` | `1e-1` | `2.236e+00` | `[1.19e+00, 3.33e+00]` | `2.629e-01` | `1.022e-01` | 0/40 |

**H-018 is refuted as stated.** Its criterion was at least half of runs returning within
`1e-6` at `eps = 1e-3`; the observed rate is 0 of 40 in every arm.

## What the prediction got wrong

**Interpretation correction, 2026-08-24.** The approximately linear residual under the
tested finite schedules supports the conclusion that this refiner had not converged.
It does not establish that Trump’s terminal component attracts perturbations through
`eps = 1e-1`, that the endpoint is isolated, or that the perturbed trajectories remain
in one component. The paragraph below is retained as the original interpretation; its
“basin is attracting” conclusion is retracted.

The hypothesis was written to distinguish two worlds — “the basin is real but small”
from “the configuration is an isolated point with no attracting neighbourhood” — and
expected the `eps` at which the return rate collapses to be the basin’s radius.

**No collapse exists to find.** In the local-quench arms the return distance is a clean
linear function of the perturbation, `max_dev ≈ 11 · eps` at 1× effort and `≈ 4.9 · eps`
at 10×, holding over four decades with no threshold anywhere.
A basin wall would show as a rate that falls off a cliff at some `eps`. What is here
instead is a *rate*: the quench is still converging when it stops, and multiplying
effort by ten roughly halves the residual — at `eps = 1e-5` the best trial lands
`1.4e-10` from Trump’s side, which is the answer to machine precision.

The original interpretation called that pattern an attracting basin out to `eps = 1e-1`.
The correction above narrows the finding to the tested refiner’s residual; component
attraction remains unresolved.
The measurement’s own criterion (`1e-6` in `max_dev`) turns out to be a statement about
the refiner rather than about the basin, which is why the answer is “refuted” and the
finding is not “no basin”.

**The `hot` arm is the sharper result, and it was not the point of the round.** Started
`1e-5` from a configuration that has stood since 1979, the campaign’s default schedule
wanders off and lands with a median side gap of `0.27` — *worse* than the `3.73e-02`
that `exp-003` reached from cold starts.
A temperature of `0.25` is a move size roughly `10⁴` times the structure being held.
That reframes `exp-003`: its `n = 11` failure is not purely a failure of exploration,
because the same engine cannot hold the answer when handed it.
The polish tier is not a refinement of this campaign’s search, it is a precondition for
it.

## What this says about what to run next

[H-002](../../../hypotheses/H-002-lp-in-cell-polish.md), the LP-in-cell quench, is
already the registry’s top priority; this round makes its test sharper.
For fixed angles and a fixed axis assignment the cell optimum is a *linear program* —
one solve, not `4 × 10⁶` annealing moves — so the prediction is that re-running this
sweep against the LP quench returns to Trump’s cell at `eps` where annealing needs 10×
effort to get close, and does it in a single step.
That is a direct, cheap, falsifiable successor, and it inherits this round’s seed
export, arms, and scoring unchanged.

## Limits

- `f64` screening only.
  The seed itself is a one-way export out of the degree-8 field, so nothing in this
  round may certify anything — and the return criterion (`1e-6`) sits far above the
  `8.9e-16` residual overlap the exported seed carries.
- `max_dev` is deliberately **not** invariant under relabelling or the container’s
  symmetries. At small `eps` a returning chain returns to the same labelled
  configuration; at `eps = 1e-1` a permuted or reflected match would be scored as a
  non-return, which is the conservative direction but means the large-`eps` cells
  understate returns.
- The `eps = 0` cells are instrument checks, not evidence: the seed is recorded as the
  incumbent best before any move, so all three arms return `0.000e+00` there by
  construction. That is what the cell is for — it caught two instrument defects below.
- One host, one seed block, one parameter set outside the swept arms.

## Instrument defects found before recording

Both were caught by the `eps = 0` cell, which exists precisely because its answer is
known in advance.

1. **The starting configuration was never a candidate for `best`.** The annealer only
   updated its incumbent on an *accepted move*, so a chain that started feasible and
   never improved reported *no feasible configuration found* — recording a perfect
   return as a total failure.
   Fixed in `search.rs`; the initial configuration is now scored on entry.
2. **`eps = 0` made the temperature schedule degenerate.** `t_hot = 0` gives an infinite
   geometric cooling ratio and `NaN` for every subsequent move.
   The starting temperature is now floored at `t_cold`.

A third was designed out rather than found: a chain that never reaches feasibility keeps
the seed as its stored `best`, so reporting its deviation would show a perfect return
for a trial that failed.
Such trials now report `null` and are counted as non-returns.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
