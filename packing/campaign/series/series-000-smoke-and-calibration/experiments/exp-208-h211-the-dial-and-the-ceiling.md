---
title: exp-208 — the dial's sweet spot, and the ceiling it reveals
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-208
  series: series-000
  title: The dial's sweet spot, and the ceiling it reveals
  date: '2026-09-12'
  hypotheses:
  - H-211
  tier: exploratory
  subject:
    label: the workbench's blind physics at six shake levels, resolved to packings
    engine: workbench page, branch claude/annealing-search-benchmark
    engine_commit: 88d452f1
    assurance: numerically-checked
    method: numerical-f64
    tolerance: 1e-5 of a unit side of deepest pairwise overlap, measured from the snapped control
    host_system: macOS on Apple silicon, one headless Chromium
    selftest_passed: true
    precision:
      binary_bits: 53
      rounding: nearest-even
    migration_annotation: '2026-09-13: source reference mapped from pre-purge 7de8b688 to reachable
      88d452f1; the retained harness and workbench source trees compare equal in Git. Original
      run provenance was not recaptured.'
  instance:
    axis: n
    point: 11
    role: target
  method:
    operator: claude-opus-5, unattended
    control: the page's shipped dial level, 3
    candidate: levels 0, 2, 4, 6, 8 and 10
    trials: 134000
    interleaved: false
    commit: 88d452f1
    entry_point: packing/devtools/bench_annealing.py
    command: python -m devtools.bench_annealing --n 5 10 11 --seeds 3000 --sweep anneal=0,2,4,6,8,10
      ; then --n 11 17 26 29 --seeds 20000 --anneal 8
    record: packing/campaign/results/annealing/
  results:
  - shape: conditions
    metric: closed at the best of a thousand valid runs, n = 5
    control_median: -0.018
    candidate_median: 0.974
    control_range:
    - -0.082
    - -0.018
    candidate_range:
    - 0.864
    - 0.974
    change_pct: 5511.0
    overlapping: false
  - shape: record
    metric: closed at the best of ten thousand valid runs, n = 11
    direction: higher
    score: 0.616
    standing_best: 1.0
    standing_best_source: the known-best side recorded in the atlas
    beat_record: false
    runs: 20000
  complexity:
    lines_changed: 0
    notes: A measurement of the existing dial; nothing in the method changed.
  verdict:
    decision: unresolved
    primary_criterion: closed at the best of a thousand valid runs
    reason: Historical summary retained; the raw geometry and exact-check receipts are absent
      from the reachable branch. Prefix best-of-k and incomplete cohort metadata do not establish
      the registered comparison. Re-admission requires reproducible valid trials and disjoint-block
      reporting.
    commit: 88d452f1
  effort:
    stopped_by: dependency
    wall_seconds: unrecorded-historical
    migration_annotation: '2026-09-13: no complete elapsed-time receipt was retained. Per-trial
      median milliseconds and approximate prose budgets cannot recover total wall or operator
      time. This marker records missing history and is unavailable to new experiments.'
---
# exp-208 — the dial’s sweet spot, and the ceiling it reveals

## Correction — 2026-09-13

The retained summaries lack raw geometry and exact-check receipts, and best-of-k is a
single prefix rather than a distribution over independent blocks.
These values remain historical observations and are not admitted evidence for the
registered comparison.
The original selftest flag describes the original account; no historical run has been
replayed in this repair.

The source reference `7de8b688` was rewritten when raw JSONL files were removed from the
branch. Its retained harness and workbench source compare equal to reachable `88d452f1`
with `git diff`; the metadata now uses that reachable source.
This is a source mapping, not a reconstructed run receipt.
Timing is explicitly unrecorded rather than estimated or entered as zero.

The original verdict was **accepted**: Below level 6 the tail never clears the trivial
grid at any n measured; at 6 to 8 it reaches 0.95 to 0.98 at n = 5 and 10, so the
shipped level of 3 is below the useful range entirely.
The original account below is preserved for provenance; the current verdict is
unresolved.

## Original account

## The sweet spot

Best-of-1000 `closed`, 54,000 valid trials:

| level | n = 5 | n = 10 | n = 11 |
| ---: | ---: | ---: | ---: |
| 0 | −0.082 | −0.114 | −0.112 |
| 2 | −0.056 | −0.076 | −0.015 |
| 4 | −0.018 | −0.070 | −0.021 |
| 6 | **0.974** | 0.947 | −0.012 |
| 8 | 0.958 | **0.977** | **0.564** |
| 10 | 0.864 | — | — |

The page ships level 3, chosen for how the animation looks.
As a search parameter it is below the useful range entirely: under it the tail never
clears the trivial grid at any of the three.

## The ceiling

At level 8 with 20,000 seeds per cell, the best the method reaches anywhere:

| n | best-of-10000 |
| ---: | ---: |
| 5 | 0.986 |
| 10 | 0.977 |
| 11 | 0.616 |
| 17 | 0.275 |
| 26 | 0.280 |
| 29 | −0.148 |

A monotone decline with the number of squares, and it is steep.
Five and ten reach within half a per cent of their records; eleven gets two thirds of
the way; seventeen and twenty-six get a quarter; twenty-nine never beats a grid.

**No cell at any level, at any n, produced a packing within 0.1% of a record.** H-209 is
not refuted by 134,000 trials.

## What the prediction got wrong

H-211 predicted a maximum and found one, but the interesting part is what the maximum
reveals rather than where it is.
Tuning the dial from 3 to 8 is the difference between “never clears the grid” and “two
thirds of the way at n = 11” — an enormous relative gain that still leaves the method
short of every record.

So the dial was worth finding and is not worth much: the ceiling is set by something
else. The candidates, in the order they are worth testing, are the resolver (which only
translates, so every number here is a lower bound), the proposal (one coarse-grid drop
per run), and the contact law itself.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
