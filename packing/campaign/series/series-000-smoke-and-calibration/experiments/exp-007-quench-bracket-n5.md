---
title: exp-007 — the bracketing quench at n = 5
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-007
  series: series-000
  title: Class-bracketing quench versus angle descent on annealer output, n = 5
  date: '2026-08-23'
  hypotheses:
  - H-002
  tier: exploratory
  subject:
    label: sqpack.quench_bracket (class-merged golden section) over sqsearch output
    engine: sqpack.quench 0.2.0 over sqsearch 0.1.0
    engine_commit: 8b450a1
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 53
      rounding: nearest-even
    tolerance: unrecorded-historical
    migration_annotation: '2026-08-25: the v1 artifact identified float64 arithmetic but did not retain
      one experiment-wide acceptance tolerance.'
    host_system: Linux container, 8 cores (remote session)
    selftest_passed: true
  instance:
    axis: n
    point: 5
    role: positive_control
  method:
    control: the same annealer output refined by finite-difference angle descent (exp-006)
    candidate: cyclic golden-section search over merged angle classes, each evaluated by an LP-in-cell
      fixed point
    runs_per_condition: 5
    interleaved: true
    operator: claude-opus-5
    commit: 8b450a1
    entry_point: explorations/packing/run_quench.py
    command: python3 run_quench.py
    budget: 5 seeds, 30 s wall budget per quench
    record: campaign/series/series-000-smoke-and-calibration/results/exp-007-quench-bracket.jsonl
  effort:
    timebox: 30m
    wall_seconds: 3.4
    agent_minutes: 25
    stopped_by: criterion
  results:
  - shape: conditions
    metric: gap_to_analytic
    role: outcome
    control_median: 3.1875e-08
    candidate_median: 2.2204e-15
    control_range:
    - 2.5499e-08
    - 2.4587e-07
    candidate_range:
    - -4.4409e-16
    - 6.1864e-08
    overlapping: false
  - shape: determination
    question: does the bracketing quench refine annealer output to the analytic value within 1e-12
    role: outcome
    outcome: reached_basin
    checked_by: gap to the analytic optimum over 5 seeds, lifted from exp-007-quench-bracket.jsonl
  - shape: record
    metric: median_gap_to_analytic
    role: outcome
    direction: lower
    score: 2.2204e-15
    standing_best: 0.0
    standing_best_source: frontier/n-05.md
    beat_record: false
    runs: 5
  complexity:
    lines_changed: 0
    new_dependencies: []
    new_failure_modes:
    - a quench may exhaust its wall budget and return early; reported as reason "time budget", never
      silently
    notes: Same instrument as the other two cells of this sweep; only n differs.
  verdict:
    decision: accepted
    primary_criterion: gap_to_analytic
    reason: 'Confirms H-002 on this cell: the bracketing quench refines annealer output from 3.43e-08
      to a median 2.22e-15 - the analytic value to machine precision - where the same output under
      angle descent moves only to 3.19e-08. Two of five seeds hit the 30 s wall budget and are reported
      as such.'
    commit: 8b450a1
---
# exp-007 — the bracketing quench at `n = 5`

The first cell of the sweep, and the one whose answer is proved: `s(5) = 2 + 1/√2`.

## Result

| Stage | median gap | range |
| --- | ---: | --- |
| annealer | `3.4274e-08` | `[2.5499e-08, 2.4587e-07]` |
| + angle descent ([exp-006](exp-006-lp-quench-n5-n10-n11.md)) | `3.1875e-08` | `[2.2652e-08, 2.3968e-07]` |
| + class bracketing | **`2.2204e-15`** | `[-4.4409e-16, 6.1864e-08]` |

Seven orders, on the same annealer output, from changing only how the angle half of the
quench searches. The negative end of the range is the solver’s own floor, not a packing
below the proved optimum: at a primal feasibility tolerance of `1e-10` a side is not
resolvable past roughly `1e-15` here, and nothing at this tier may claim otherwise.

Both quenches find the same contact structure (4 contacts) and the same two angle
classes, so the difference is entirely in whether the search can land on the corner.

## Limits

Two of five seeds hit the 30-second wall budget and returned early — at `6.19e-08` and
just under, which is why the candidate range spans to `6.19e-08` while its median is at
machine precision. The budget is reported, never silent.
That the *median* is `2.2e-15` and the *worst* is `6.2e-08` says the method either lands
exactly or does not land at all, which is what a corner-seeking search should do.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
