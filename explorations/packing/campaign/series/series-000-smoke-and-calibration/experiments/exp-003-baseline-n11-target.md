---
title: exp-003 — reproducible baseline at n = 11 (target)
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-003
  series: series-000
  title: Reproducible baseline at n = 11
  date: '2026-08-23'
  hypotheses:
  - H-016
  tier: exploratory
  subject:
    label: stock sqsearch annealer, default parameters, corrected archive
    engine: sqsearch 0.1.0
    engine_commit: 1e70bc8
    assurance: numerically-checked
    method: numerical-f64
    precision:
      binary_bits: 53
      rounding: nearest-even
    tolerance: unrecorded-historical
    migration_annotation: '2026-08-25: the v1 artifact identified float64 arithmetic but did not retain
      one experiment-wide acceptance tolerance.'
    host_system: Apple M1 Pro, 8 performance + 2 efficiency cores, 32 GB
    selftest_passed: true
  instance:
    axis: n
    point: 11
    role: target
  method:
    control: the trivial ceil(sqrt(n)) grid, which every chain starts from
    candidate: 'sqsearch defaults: steps 400000, t_hot 0.25, t_cold 1e-9, lambda 2 -> 1e6, p_rotate
      0.35, p_reseed 0.5'
    runs_per_condition: 5
    interleaved: false
    operator: claude-opus-5
    commit: 1e70bc8
    entry_point: explorations/packing/run_baseline.sh
    command: sqsearch --n 11 --seed S --chains 8 --budget-moves 100000000, for S in 1..5
    budget: 4,000,000,000 moves, 107.2 s wall
    record: campaign/series/series-000-smoke-and-calibration/results/exp-003-baseline-n11-target.jsonl
  effort:
    wall_seconds: 107.2
    stopped_by: criterion
  results:
  - shape: record
    metric: best_side
    role: outcome
    direction: lower
    score: 3.9144165418191186
    standing_best: 3.877083590022814
    standing_best_source: frontier/n-011.md (Trump 1979)
    beat_record: false
    runs: 5
  - shape: determination
    question: does the stock annealer reach the standing best at n = 11
    role: outcome
    outcome: near_miss
    checked_by: overlap recomputed from each stored configuration (max 0.0e+00); every archived record
      re-derives its own reported side
  - shape: conditions
    metric: best_side_across_seeds
    role: mechanism
    control_median: 3.927939617731721
    candidate_median: 3.927939617731721
    control_range:
    - 3.9144165418191186
    - 3.9361125018580427
    candidate_range:
    - 3.9144165418191186
    - 3.9361125018580427
    overlapping: true
  complexity:
    lines_changed: 0
    new_dependencies: []
    new_failure_modes: []
    notes: Replication of exp-001 on a corrected instrument and archive.
  verdict:
    decision: rejected
    primary_criterion: best_side
    reason: On this cell the annealer misses the standing best by +3.733e-02, outside the 1e-4 H-016
      declared, so the claim is refuted here.
    commit: 1e70bc8
---
# exp-003 — reproducible baseline at n = 11

## What was measured

The same sweep cell as [exp-001](exp-001-baseline-sweep.md), re-run on the corrected
engine and archive: five deterministic seeds, eight chains each, 100M moves per chain.

|  |  |
| --- | --- |
| best | `3.9144165418` |
| median | `3.9279396177` |
| range across seeds | `[3.9144165, 3.9361125]` |
| standing best | `3.8770835900` |
| gap | `+3.733e-02` |

## Why this round exists

[The standing review of PR #5](../../../../docs/project/reviews/review-2026-08-23-experiment-loop-and-campaign.md)
found that exp-001’s archive kept only summary lines, discarding the configurations, and
that its recorded commit had been made unreachable by a rebase.
Its numbers were sound — the review re-derived them — but nothing in it could be
re-verified at the level of an actual packing.

Three things changed in the instrument, none of them to the search itself: the archive
now keeps every per-chain record, the summary line carries the best configuration, and
the reported overlap is **recomputed from the stored configuration** rather than read
off an accumulator maintained across hundreds of millions of incremental updates.

## Result

**The numbers are identical to exp-001’s, to every digit reported.** That is the outcome
worth noting: the corrections touched the record, not the search, and the same seeds
produced the same answer — which is what the engine’s determinism claim asserts and had
not previously been demonstrated across a rebuild.
It also means exp-001’s figures stand on their own terms, retroactively, even though its
archive could not show its work.

Every archived record here re-derives its own reported side from its own coordinates,
and every stored configuration has recomputed overlap of exactly zero.

## Limits

- `f64` screening. Nothing here is certified and none of it may claim a record.
- One cell. This is the sweep’s `n = 11` point and says nothing about the others; the
  companion rounds carry those.
- Five seeds is enough to see the spread, not enough for a confirmatory interval.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
