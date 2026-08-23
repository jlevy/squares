---
title: exp-009 — the bracketing quench at n = 11
softschema:
  contract: packing.squares:Experiment/v1
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-009
  series: series-000
  title: Class-bracketing quench versus angle descent on annealer output, n = 11
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
  instance: {axis: n, point: 11, role: target}
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
    wall_seconds: 150.0
    agent_minutes: 30
    stopped_by: criterion
  results:
  - shape: conditions
    metric: gap_to_analytic
    role: outcome
    control_median: 6.9987e-02
    candidate_median: 6.2894e-02
    control_range: [6.4397e-02, 1.0020e-01]
    candidate_range: [2.8090e-02, 9.4285e-02]
    overlapping: false
  - shape: determination
    question: 'does the bracketing quench refine annealer output to the analytic value within 1e-12'
    role: outcome
    outcome: no_progress
    checked_by: 'gap to the analytic optimum over 5 seeds, lifted from exp-007-quench-bracket.jsonl'
  - shape: record
    metric: median_gap_to_analytic
    role: outcome
    direction: lower
    score: 6.2894e-02
    standing_best: 0.0
    standing_best_source: 'frontier/n-011.md'
    beat_record: false
    runs: 5
  complexity:
    lines_changed: 0
    new_dependencies: []
    new_failure_modes: ['a quench may exhaust its wall budget and return early; reported as reason "time budget", never silently']
    notes: 'Same instrument as the other two cells of this sweep; only n differs.'
  verdict:
    decision: rejected
    primary_criterion: gap_to_analytic
    reason: >-
      Refutes H-002 on this cell: the median gap improves only from 8.85e-02 to 6.29e-02, against machine precision at n = 5 and n = 10. The quench is not failing - it is being handed the wrong basin, which is what exp-006 concluded and this cell confirms at the target.
    commit: '8b450a1'
---
# exp-009 — the bracketing quench at `n = 11`, the target

## Result

| Stage | median gap | range |
| --- | ---: | --- |
| annealer | `8.8456e-02` | `[6.4397e-02, 1.0020e-01]` |
| + angle descent ([exp-006](exp-006-lp-quench-n5-n10-n11.md)) | `6.9987e-02` | `[4.6077e-02, 8.8456e-02]` |
| + class bracketing | `6.2894e-02` | `[2.8090e-02, 9.4285e-02]` |

Against machine precision at [`n = 5`](exp-007-quench-bracket-n5.md) and
[`n = 10`](exp-008-quench-bracket-n10.md), this is nothing: a 1.4× improvement on the
annealer, and the ranges overlap.

## Why this cell fails while the other two succeed, and why that is the useful part

The quench is not broken here — it is being handed the wrong basin.

At `n = 5` and `n = 10` the annealer reaches the neighbourhood of the proved optimum and
stops short; the quench then finishes the job exactly.
At `n = 11` the annealer is `8.8e-02` away, and no amount of local refinement crosses
that: an LP-in-cell solve optimises the cell it is given, and cyclic bracketing moves
angles within the structure it is given.
Both are *local* operations by construction.

So the sweep separates the two failures that
[exp-002](exp-002-baseline-n10-positive-control.md) and
[exp-003](exp-003-baseline-n11-target.md) could not tell apart, and assigns each to a
different cell:

- `n = 10` was a **polish** failure — now fixed, to `1.3e-15`.
- `n = 11` is an **exploration** failure — untouched by any of this, and unaffected by
  fixing polish.

That is worth more than a better number at `n = 11` would have been.
It says the spine is done arguing with the wrong problem: the burden sits squarely on
the proposer, and the register’s proposer entries — δ-continuation
([H-013](../../../ideas.md)), neighbour transfer, angle-class search
([H-001](../../../hypotheses/H-001-angle-class-reduction.md)) — are now the campaign’s
critical path rather than its speculative tail.

Three of five seeds hit the 30-second wall budget here, against two at each of the
smaller cells, and the class counts run 4 to 6 rather than 2 — both signs that the
annealer’s `n = 11` output has no clean angle-class structure to merge, which is itself
consistent with it being in a grid-like rather than record-like basin.

## Limits

- `polished` tier throughout; the analytic target at `n = 11` is Trump’s *conjectured*
  optimum, not a proved one, so “gap to analytic” here means “gap to the standing best”.
- Five seeds, one host, one parameter set.
  `exploratory`.
- The wall budget truncates 3 of 5 seeds, so these numbers are a lower bound on what the
  method would reach given more time — but the gap is `6e-02`, and no plausible amount
  of local refinement closes that.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
