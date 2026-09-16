---
title: exp-208 — the shake dial from level 0 to 10, on repaired runs
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-208
  series: series-000
  title: The shake dial from level 0 to 10, on repaired runs
  date: '2026-09-12'
  hypotheses: [H-212]
  tier: exploratory
  known_defects: [D-067]
  subject:
    label: the workbench's blind physics at six shake levels, repaired to packings before scoring
    engine: workbench page, branch claude/annealing-search-benchmark
    engine_commit: 88d452f1
    assurance: numerically-checked
    method: numerical-f64
    tolerance: 1e-5 of a unit side of deepest pairwise overlap, chosen; the snapped observation
      beside it was run once and not kept (think-2ngs)
    host_system: macOS on Apple silicon, one headless Chromium
    selftest_passed: false
    precision:
      binary_bits: 53
      rounding: nearest-even
    migration_annotation: '2026-09-13: source reference mapped from pre-purge 7de8b688 to reachable
      88d452f1; the retained harness and workbench source trees compare equal in Git. Original
      run provenance was not recaptured. The second command requests n = 11, 17, 26 and 29 at
      20,000 seeds; the retained summary holds n = 11 only, with 16,319 seeds, whose first 3,000
      repeat the sweep cell. Level 3, the page default, was not in the sweep.'
  instance:
    axis: n
    point: 11
    role: target
  method:
    operator: claude-opus-5, unattended
    control: shake level 0, no shake
    candidate: shake levels 2, 4, 6, 8 and 10
    trials: 67319
    interleaved: false
    commit: 88d452f1
    entry_point: packing/devtools/bench_annealing.py
    command: python -m devtools.bench_annealing --n 5 10 11 --seeds 3000 --sweep anneal=0,2,4,6,8,10
      --budget 900; then --n 11 17 26 29 --seeds 20000 --anneal 8 --budget 900
    record: packing/campaign/results/annealing/summaries.json
  results:
  - shape: record
    metric: closed at n = 11, the best of the first 1,000 repaired runs at shake level 0
    direction: higher
    score: -0.112
    standing_best: 1.0
    standing_best_source: the known-best side recorded in the atlas
    beat_record: false
    runs: 1000
  - shape: record
    metric: closed at n = 11, the best of the first 1,000 repaired runs at shake level 2
    direction: higher
    score: -0.015
    standing_best: 1.0
    standing_best_source: the known-best side recorded in the atlas
    beat_record: false
    runs: 1000
  - shape: record
    metric: closed at n = 11, the best of the first 1,000 repaired runs at shake level 4
    direction: higher
    score: -0.021
    standing_best: 1.0
    standing_best_source: the known-best side recorded in the atlas
    beat_record: false
    runs: 1000
  - shape: record
    metric: closed at n = 11, the best of the first 1,000 repaired runs at shake level 6
    direction: higher
    score: -0.012
    standing_best: 1.0
    standing_best_source: the known-best side recorded in the atlas
    beat_record: false
    runs: 1000
  - shape: record
    metric: closed at n = 11, the best of the first 1,000 repaired runs at shake level 8
    direction: higher
    score: 0.564
    standing_best: 1.0
    standing_best_source: the known-best side recorded in the atlas
    beat_record: false
    runs: 1000
  - shape: record
    metric: closed at n = 11, the best of the first 1,000 repaired runs at shake level 10
    direction: higher
    score: 0.325
    standing_best: 1.0
    standing_best_source: the known-best side recorded in the atlas
    beat_record: false
    runs: 1000
  - shape: record
    metric: closed at n = 11, the best of all 16,319 repaired runs at shake level 8
    direction: higher
    score: 0.616
    standing_best: 1.0
    standing_best_source: the known-best side recorded in the atlas
    beat_record: false
    runs: 16319
  complexity:
    lines_changed: 0
    notes: A measurement of the existing dial; nothing in the method changed.
  verdict:
    decision: unresolved
    primary_criterion: closed at the best of the first 1,000 repaired runs
    reason: At levels 0, 2 and 4 no repaired run in 3,000 beat the grid at n = 5, 10 or 11, and
      at levels 6, 8 and 10 the best run did in eight of nine cells, the ninth within 5,000
      seeds, but each value is one prefix from one seed stream and the page's own level 3 was
      not measured on repaired runs.
    commit: 88d452f1
  effort:
    stopped_by: dependency
    wall_seconds: unrecorded-historical
    migration_annotation: '2026-09-13: no complete elapsed-time receipt was retained. Per-trial
      median milliseconds and approximate prose budgets cannot recover total wall or operator
      time. This marker records missing history and is unavailable to new experiments.'
---
# exp-208 — The Shake Dial From Level 0 to 10, on Repaired Runs

**Rewritten 2026-09-14** to remove claims the retained record does not support.
The previous text is at commit `a40d272c`.

**Exploratory data, filed under the open question
[H-212](../../../hypotheses/H-212-the-workbench-physics-as-a-search.md).** H-211 was
registered from this round’s table, so the round cannot also be its test.

## What Was Measured

3,000 seeds at each of six shake levels for `n = 5`, 10 and 11. Every run was repaired
to a packing and checked before scoring.
`n = 11` at level 8 then continued to 16,319 seeds.

Each entry is the best of the first 1,000 runs, then the median run, in `closed`:

| level | n = 5 | n = 10 | n = 11 |
| ---: | --- | --- | --- |
| 0 | −0.082 / −0.082 | −0.114 / −0.114 | −0.112 / −0.112 |
| 2 | −0.056 / −0.090 | −0.076 / −0.104 | −0.015 / −0.103 |
| 4 | −0.018 / −0.083 | −0.070 / −0.103 | −0.021 / −0.103 |
| 6 | 0.974 / −0.074 | 0.947 / −0.099 | −0.012 / −0.106 |
| 8 | 0.958 / −0.076 | 0.977 / −0.098 | 0.564 / −0.115 |
| 10 | 0.864 / −0.095 | 0.879 / −0.098 | 0.325 / −0.249 |

At level 8, `n = 11` reached 0.616 over 16,319 seeds, 1.22% above `s(11)`.

## What It Shows

- **Without shake every seed gives the same run**, because the shake is the only
  randomness.
- **At levels 0, 2 and 4 no run beat the grid** in 3,000 seeds at any of the three `n`.
- **At levels 6, 8 and 10 the best run beat it in eight cells of nine.** The ninth,
  `n = 11` at level 6, marks the budget rather than the level: the same seed stream beat
  the grid before seed 5,000 (`resolved-5k-a6.jsonl`).
- **The median barely moves**, except `n = 11` at level 10, so the dial changes the best
  run rather than the typical one.
- **The best of 1,000 peaks at level 6 for `n = 5` and at level 8 for `n = 10` and 11.**
  H-211’s maximum near levels 6 to 8 was drawn from this pattern, which is why it needs
  a test on other seeds or `n`.

## What Is Not Established

- **No spread.** Each cell is one prefix from one seed stream.
- **The page’s level 3 was not measured on repaired runs**, so H-211’s threshold, which
  compares against level 3, cannot be applied.
  Levels 1 and 3 have only void cells, and levels 5, 7 and 9 none.
- **Larger `n` at level 8 is missing.** The run requested `n = 17`, 26 and 29 and
  retained only `n = 11`.
- **Whether the best level moves with `n`** is untested beyond these three.

## Evidence

Retained: the six `20260912T015702-sweep-anneal*.jsonl` entries and the `a8-deep.jsonl`
entry in `packing/campaign/results/annealing/summaries.json`. Not retained: the trials
and their final poses.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
