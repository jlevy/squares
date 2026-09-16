---
title: exp-207 — what a budget of runs buys once runs are repaired to packings
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-207
  series: series-000
  title: What a budget of runs buys once runs are repaired to packings
  date: '2026-09-12'
  hypotheses: [H-207]
  tier: exploratory
  known_defects: [D-067]
  subject:
    label: the workbench's blind physics, repaired to a packing before scoring
    engine: workbench page, branch claude/annealing-search-benchmark
    engine_commit: e9d13c1d
    assurance: numerically-checked
    method: numerical-f64
    tolerance: 1e-5 of a unit side of deepest pairwise overlap, chosen; the snapped observation
      beside it was run once and not kept (think-2ngs)
    host_system: macOS on Apple silicon, one headless Chromium
    selftest_passed: false
    precision:
      binary_bits: 53
      rounding: nearest-even
    migration_annotation: '2026-09-13: source reference mapped from pre-purge 1eab3313 to reachable
      e9d13c1d; the retained harness and workbench source trees compare equal in Git. Original
      run provenance was not recaptured. The command requests n = 5 and 10; the retained summary
      holds n = 5 only, with 39,871 seeds.'
  instance:
    axis: n
    point: 5
    role: calibration
  method:
    operator: claude-opus-5, unattended
    control: none; one seed stream at one schedule, and no schedule was compared
    trials: 39871
    interleaved: false
    commit: e9d13c1d
    entry_point: packing/devtools/bench_annealing.py
    command: python -m devtools.bench_annealing --n 5 10 --seeds 40000 --anneal 6 --budget 900
    budget: 900 seconds of wall clock, the harness default; 40,000 seeds requested for each of
      n = 5 and 10, and 39,871 retained for n = 5, consistent with the budget stopping the run
    record: packing/campaign/results/annealing/summaries.json, entry deep-n5-n10.jsonl
  results:
  - shape: record
    metric: closed at n = 5, the best of all 39,871 repaired runs of one seed stream
    direction: higher
    score: 0.986
    standing_best: 1.0
    standing_best_source: the known-best side recorded in the atlas
    beat_record: false
    runs: 39871
  - shape: record
    metric: closed at n = 5, the best of the first 100 repaired runs of that stream
    direction: higher
    score: -0.015
    standing_best: 1.0
    standing_best_source: the known-best side recorded in the atlas
    beat_record: false
    runs: 100
  - shape: record
    metric: closed at n = 5, the best of the first 1,000 repaired runs of that stream
    direction: higher
    score: 0.974
    standing_best: 1.0
    standing_best_source: the known-best side recorded in the atlas
    beat_record: false
    runs: 1000
  complexity:
    lines_changed: 0
    notes: No change to the method; the round measures what a budget of runs buys at one
      schedule.
  verdict:
    decision: unresolved
    primary_criterion: closed at the best of the first k repaired runs of one seed stream
    reason: At n = 5 the best of the first 1,000 repaired runs is 0.28% above the record while a
      single run is worse than the grid, but these are prefix values from one seed stream with
      no spread, and no schedule was compared at equal cost, so H-207's criterion was not tested.
    commit: e9d13c1d
  effort:
    stopped_by: dependency
    wall_seconds: unrecorded-historical
    migration_annotation: '2026-09-13: no complete elapsed-time receipt was retained. Per-trial
      median milliseconds and approximate prose budgets cannot recover total wall or operator
      time. This marker records missing history and is unavailable to new experiments.'
---
# exp-207 — What a Budget of Runs Buys Once Runs Are Repaired to Packings

**Rewritten 2026-09-14** to remove claims the retained record does not support.
The previous text is at commit `a40d272c`.

## What Was Measured

One seed stream of blind runs at `n = 5` and shake level 6, 39,871 seeds long.
Every run was repaired to a packing and checked before scoring.
The table gives the best of the first `k` runs.

| k | best of first k, `closed` | above `s(5)` |
| ---: | ---: | ---: |
| 1 | −0.084 | 11.72% |
| 10 | −0.037 | 11.22% |
| 100 | −0.015 | 10.98% |
| 1,000 | 0.974 | 0.28% |
| 10,000 | 0.977 | 0.25% |
| 39,871 | 0.986 | 0.15% |

The trivial grid is 10.82% above `s(5)`. The same command asked for `n = 10`; no
`n = 10` result from it was retained.

## What It Shows

- **One run is worse than the grid.** The median over all 39,871 runs is −0.074.
- **A budget of runs gets close.** The best of the first 1,000 is 0.28% above the
  record, and forty times as many runs brought that to 0.15%.
- **No run reached the record.**
- **The improvement came in one step.** One run between seed 100 and seed 999 scored
  0.974. With a single stream there is no way to say how often a block of 1,000 runs
  contains such a run.

## What It Does Not Test

H-207 claims that restarts beat schedule tuning at equal cost.
No schedule was compared, so this round measures what a budget buys at one schedule and
leaves the claim untested.

## Evidence

Retained: the `deep-n5-n10.jsonl` entry in
`packing/campaign/results/annealing/summaries.json`, which holds the median and the
best-of-first-k ladder.
Not retained: the trials and their final poses.
No value here carries a spread.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
