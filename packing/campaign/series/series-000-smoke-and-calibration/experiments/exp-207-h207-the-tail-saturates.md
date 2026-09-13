---
title: exp-207 — restarts are the whole of the method, and the tail saturates near 0.98
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-207
  series: series-000
  title: Restarts are the whole of the method, and the tail saturates near 0.98
  date: '2026-09-12'
  hypotheses:
  - H-207
  tier: exploratory
  subject:
    label: the workbench's blind physics, resolved to a packing before scoring
    engine: workbench page, branch claude/annealing-search-benchmark
    engine_commit: e9d13c1d
    assurance: numerically-checked
    method: numerical-f64
    tolerance: 1e-5 of a unit side of deepest pairwise overlap, measured from the snapped control
    host_system: macOS on Apple silicon, one headless Chromium
    selftest_passed: true
    precision:
      binary_bits: 53
      rounding: nearest-even
    migration_annotation: '2026-09-13: source reference mapped from pre-purge 1eab3313 to reachable
      e9d13c1d; the retained harness and workbench source trees compare equal in Git. Original
      run provenance was not recaptured.'
  instance:
    axis: n
    point: 5
    role: calibration
  method:
    operator: claude-opus-5, unattended
    control: one blind run, the method as the page ships it
    candidate: the best of k blind runs at the same parameters
    trials: 80000
    interleaved: false
    commit: e9d13c1d
    entry_point: packing/devtools/bench_annealing.py
    command: python -m devtools.bench_annealing --n 5 10 --seeds 40000 --anneal 6
    budget: 40,000 seeds per n, about two minutes
    record: packing/campaign/results/annealing/deep-n5-n10.jsonl
  results:
  - shape: record
    metric: closed, the fraction of the record-to-grid gap closed by a valid packing
    direction: higher
    score: 0.986
    standing_best: 1.0
    standing_best_source: the known-best side recorded in the atlas
    beat_record: false
    runs: 40000
  - shape: conditions
    metric: closed at the best of k, n = 5
    control_median: -0.084
    candidate_median: 0.977
    control_range:
    - -0.286
    - -0.015
    candidate_range:
    - 0.974
    - 0.986
    change_pct: 1263.0
    overlapping: false
  complexity:
    lines_changed: 0
    notes: No change to the method; the round is a measurement of what budget buys. The resolver
      and the guard landed in exp-210.
  verdict:
    decision: unresolved
    primary_criterion: closed at the best of k against closed at k = 1
    reason: Historical summary retained; the raw geometry and exact-check receipts are absent
      from the reachable branch. Prefix best-of-k and incomplete cohort metadata do not establish
      the registered comparison. Re-admission requires reproducible valid trials and disjoint-block
      reporting.
    commit: e9d13c1d
  effort:
    stopped_by: dependency
    wall_seconds: unrecorded-historical
    migration_annotation: '2026-09-13: no complete elapsed-time receipt was retained. Per-trial
      median milliseconds and approximate prose budgets cannot recover total wall or operator
      time. This marker records missing history and is unavailable to new experiments.'
---
# exp-207 — restarts are the whole of the method, and the tail saturates near 0.98

## Correction — 2026-09-13

The retained summaries lack raw geometry and exact-check receipts, and best-of-k is a
single prefix rather than a distribution over independent blocks.
These values remain historical observations and are not admitted evidence for the
registered comparison.
The original selftest flag describes the original account; no historical run has been
replayed in this repair.

The source reference `1eab3313` was rewritten when raw JSONL files were removed from the
branch. Its retained harness and workbench source compare equal to reachable `e9d13c1d`
with `git diff`; the metadata now uses that reachable source.
This is a source mapping, not a reconstructed run receipt.
Timing is explicitly unrecorded rather than estimated or entered as zero.

The original verdict was **accepted**: One run scores below the trivial grid at every n
while the best of a thousand reaches 0.974 at n = 5, so restarts are not an improvement
to the method, they are the method.
The original account below is preserved for provenance; the current verdict is
unresolved.

## Original account

## What the budget buys

| n | k=1 | k=10 | k=100 | k=1000 | k=10000 | k=40000 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | −0.084 | −0.037 | −0.015 | 0.974 | 0.977 | 0.986 |
| 10 | −0.099 | −0.080 | 0.874 | 0.947 | 0.974 | — |

A single run is worse than putting the squares in a grid.
The best of a thousand is a valid packing within 0.28% of the record.
That is not a method improved by restarts; it is a method that only exists as restarts.

## And then it stops

From k=1000 to k=40000 — forty times the budget — `closed` moves from 0.974 to 0.986.
The tail **saturates near 0.98** and does not reach the record.

That is the useful half of the result.
A search whose best-of-k kept climbing would be worth more budget; this one is worth
about a thousand tries and no more, so the way to do better is a different method rather
than a longer run of this one.

## Where it works and where it does not

Only at n = 5 and n = 10. At n = 11, 17 and 29 the best of a thousand barely clears the
trivial grid (−0.012, −0.062, −0.193). The gradient runs with the number of squares, and
the crossing is somewhere between 10 and 11.

## What the prediction got wrong

H-207 predicted that restarts would beat schedule tuning at equal cost, which reads as a
claim about two comparable options.
The measurement is more lopsided than that: there is no schedule worth tuning, because
every schedule’s median is below the grid.
The claim is accepted on its criterion and the criterion was the wrong shape for what is
actually true.

## What bounds every number here

The resolver only translates; angles are held.
A resolver that could rotate, or that solved for the smallest enclosing square directly,
would score these same runs higher — so 0.986 is a lower bound on what the physics
found, not a measurement of it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
