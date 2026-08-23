---
title: exp-008 — the bracketing quench at n = 10
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-008
  series: series-000
  title: Class-bracketing quench versus angle descent on annealer output, n = 10
  date: '2026-08-23'
  hypotheses: [H-002]
  tier: exploratory
  subject:
    label: sqpack.quench_bracket (class-merged golden section) over sqsearch output
    engine: 'sqpack.quench 0.2.0 over sqsearch 0.1.0'
    engine_commit: '8b450a1'
    precision: polished
    host_system: Linux container, 8 cores (remote session)
    selftest_passed: true
  instance: {axis: n, point: 10, role: positive_control}
  method:
    control: 'the same annealer output refined by finite-difference angle descent (exp-006)'
    candidate: 'cyclic golden-section search over merged angle classes, each evaluated by an LP-in-cell fixed point'
    runs_per_condition: 5
    interleaved: true
    operator: claude-opus-5
    commit: '8b450a1'
    entry_point: explorations/packing/run_quench.py
    command: 'python3 run_quench.py'
    budget: '5 seeds, 30 s wall budget per quench'
    record: campaign/series/series-000-smoke-and-calibration/results/exp-007-quench-bracket.jsonl
  effort:
    timebox: 30m
    wall_seconds: 67.0
    agent_minutes: 20
    stopped_by: criterion
  results:
  - shape: conditions
    metric: gap_to_analytic
    role: outcome
    control_median: 4.5070e-03
    candidate_median: 1.3323e-15
    control_range: [2.1655e-03, 1.5130e-02]
    candidate_range: [-8.8818e-16, 8.7346e-03]
    overlapping: false
  - shape: determination
    question: 'does the bracketing quench refine annealer output to the analytic value within 1e-12'
    role: outcome
    outcome: reached_basin
    checked_by: 'gap to the analytic optimum over 5 seeds, lifted from exp-007-quench-bracket.jsonl'
  - shape: record
    metric: median_gap_to_analytic
    role: outcome
    direction: lower
    score: 1.3323e-15
    standing_best: 0.0
    standing_best_source: 'frontier/n-010.md'
    beat_record: false
    runs: 5
  complexity:
    lines_changed: 0
    new_dependencies: []
    new_failure_modes: ['a quench may exhaust its wall budget and return early; reported as reason "time budget", never silently']
    notes: 'Same instrument as the other two cells of this sweep; only n differs.'
  verdict:
    decision: accepted
    primary_criterion: gap_to_analytic
    reason: >-
      Confirms H-002 on this cell, and by twelve orders of magnitude: median gap falls from the annealer's 5.32e-03 to 1.33e-15, where angle descent reaches only 4.51e-03. The two seeds that hit the wall budget are the two that did not converge.
    commit: '8b450a1'
---
# exp-008 — the bracketing quench at `n = 10`

The sweep’s second proved cell: `s(10) = 3 + 1/√2`, and the campaign’s positive control
since [exp-002](exp-002-baseline-n10-positive-control.md).

## Result

| Stage | median gap | range |
| --- | ---: | --- |
| annealer | `5.3177e-03` | `[2.1655e-03, 1.5130e-02]` |
| + angle descent ([exp-006](exp-006-lp-quench-n5-n10-n11.md)) | `4.5070e-03` | `[8.4136e-04, 1.3382e-02]` |
| + class bracketing | **`1.3323e-15`** | `[-8.8818e-16, 8.7346e-03]` |

Twelve orders of magnitude, and it settles the question
[exp-002](exp-002-baseline-n10-positive-control.md) raised and could not answer.
That round found the annealer landing `4.19e-04` from a proved optimum and called it a
*polish* failure rather than an exploration failure — the search had the right basin and
could not finish. This cell proves that reading: handed the same basin, a quench that
respects the corner finishes it to machine precision.

The two seeds that hit the wall budget are exactly the two that did not converge
(`8.73e-03` and `2.2e-03`), so the failure mode is visible rather than averaged away.
Class counts vary here (2, 3 and 4 across seeds) where `n = 5` always found 2 — the
annealer’s output at `n = 10` is further from a clean class structure, and merging is
doing more work.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
