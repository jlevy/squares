---
title: exp-004 — reproducible baseline at n = 12 (open-case calibration)
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-004
  series: series-000
  title: Reproducible baseline at n = 12
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
    point: 12
    role: calibration
  method:
    control: the trivial ceil(sqrt(n)) grid, which every chain starts from
    candidate: 'sqsearch defaults: steps 400000, t_hot 0.25, t_cold 1e-9, lambda 2 -> 1e6, p_rotate
      0.35, p_reseed 0.5'
    runs_per_condition: 5
    interleaved: false
    operator: claude-opus-5
    commit: 1e70bc8
    entry_point: explorations/packing/run_baseline.sh
    command: sqsearch --n 12 --seed S --chains 8 --budget-moves 100000000, for S in 1..5
    budget: 4,000,000,000 moves, 108.8 s wall
    record: campaign/series/series-000-smoke-and-calibration/results/exp-004-baseline-n12-negative-control.jsonl
  effort:
    wall_seconds: 108.8
    stopped_by: criterion
  results:
  - shape: record
    metric: best_side
    role: outcome
    direction: lower
    score: 4.0
    standing_best: 4.0
    standing_best_source: frontier/n-012.md (trivial 4x4 grid)
    beat_record: false
    runs: 5
  - shape: determination
    question: does the stock annealer reach the standing best at n = 12
    role: outcome
    outcome: reached_basin
    checked_by: overlap recomputed from each stored configuration (max 0.0e+00); every archived record
      re-derives its own reported side
  - shape: conditions
    metric: best_side_across_seeds
    role: mechanism
    control_median: 4.0
    candidate_median: 4.0
    control_range:
    - 4.0
    - 4.0
    candidate_range:
    - 4.0
    - 4.0
    overlapping: true
  complexity:
    lines_changed: 0
    new_dependencies: []
    new_failure_modes: []
    notes: Replication of exp-001 on a corrected instrument and archive.
  verdict:
    decision: accepted
    primary_criterion: best_side
    reason: On this cell the annealer is within 1e-4 of the standing best (gap +0.000e+00), so H-016
      holds here; the claim is universally quantified over the sweep and is refuted elsewhere.
    commit: 1e70bc8
---
# exp-004 — reproducible baseline at n = 12

## What was measured

The same sweep cell as [exp-001](exp-001-baseline-sweep.md), re-run on the corrected
engine and archive: five deterministic seeds, eight chains each, 100M moves per chain.

|  |  |
| --- | --- |
| best | `4.0000000000` |
| median | `4.0000000000` |
| range across seeds | `[4.0000000, 4.0000000]` |
| standing best | `4.0000000000` |
| gap | `+0.000e+00` |

## Why this round exists

**Correction (D-042).** This round was originally labeled a negative control.
That role was invalid because `s(12) = 4` is not proved.
The measurements remain a reproducible baseline at the standing best; they provide no
known-answer evidence that a value below `4` must be a bug.

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
- One cell. This is the sweep’s `n = 12` point and says nothing about the others; the
  companion rounds carry those.
- Five seeds is enough to see the spread, not enough for a confirmatory interval.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
