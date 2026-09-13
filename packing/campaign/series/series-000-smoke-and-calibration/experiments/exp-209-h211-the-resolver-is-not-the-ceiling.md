---
title: exp-209 — the resolver is not the ceiling
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-209
  series: series-000
  title: The resolver is not the ceiling
  date: '2026-09-12'
  hypotheses:
  - H-211
  tier: exploratory
  subject:
    label: the resolved arrangements, tested for local compactness
    engine: workbench page, branch claude/annealing-search-benchmark
    engine_commit: f91fc7d4
    assurance: numerically-checked
    method: numerical-f64
    tolerance: a move is accepted only if it creates no overlap deeper than 1e-9
    host_system: macOS on Apple silicon, one headless Chromium
    selftest_passed: true
    precision: unrecorded-historical
    migration_annotation: '2026-09-13: source reference mapped from pre-purge 6ed8bd56 to reachable
      f91fc7d4; the retained harness and workbench source trees compare equal in Git. Original
      run provenance was not recaptured.'
  instance:
    axis: n
    point: 11
    role: target
  method:
    operator: claude-opus-5, unattended
    control: the same arrangement scattered outward by 0.15 of a side, then compacted
    candidate: the resolved arrangement, compacted
    trials: 3320
    interleaved: true
    commit: f91fc7d4
    entry_point: packing/devtools/bench_annealing.py
    command: a compaction pass over the resolver's output, with a scatter control
    record: run inline; the pass is not retained in the harness
  results:
  - shape: conditions
    metric: closed at the best of 800, resolved against resolved-then-compacted, n = 5
    control_median: 0.958
    candidate_median: 0.958
    control_range:
    - 0.958
    - 0.958
    candidate_range:
    - 0.958
    - 0.958
    change_pct: 0.0
    overlapping: true
  - shape: determination
    question: does walking every square toward the box centre, as far as it will go without
      overlapping, shrink the container the resolved arrangement needs
    role: guard
    outcome: no_progress
  complexity:
    lines_changed: 0
    notes: The original inline compaction pass and outputs were discarded. The dated correction
      below preserves the account but withdraws the exclusion claim; future use requires a retained
      instrument.
  verdict:
    decision: unresolved
    primary_criterion: closed at the best of 800, with and without compaction
    reason: The historical compaction program and outputs were not retained, so its null result
      and the inference that the resolver is not the ceiling cannot be reproduced or used to
      exclude an optimization.
    commit: f91fc7d4
  effort:
    stopped_by: dependency
    wall_seconds: unrecorded-historical
    migration_annotation: '2026-09-13: no complete elapsed-time receipt was retained. Per-trial
      median milliseconds and approximate prose budgets cannot recover total wall or operator
      time. This marker records missing history and is unavailable to new experiments.'
---
# exp-209 — the resolver is not the ceiling

## Correction — 2026-09-13

The inline compaction program, its raw inputs, and its outputs were deliberately not
retained.
The source reference below identifies the surrounding harness only; it does not
recover that program.
The reported zero improvement is an unreproducible historical observation.
It does not establish local optimality, stationarity, a general failure of translation
repair, or a limit on rotating repair.
The claim that this round eliminates the resolver as a cause is withdrawn.
No new compaction experiment was run during this repair.

The source reference `6ed8bd56` was rewritten when raw JSONL files were removed from the
branch. Its retained harness and workbench source compare equal to reachable `f91fc7d4`
with `git diff`; the metadata now uses that reachable source.
This is a source mapping, not a reconstructed run receipt.
Timing is explicitly unrecorded rather than estimated or entered as zero.

The original verdict was **rejected**: Compaction moves nothing at four n to four
decimal places, while the same pass shrinks a deliberately scattered arrangement from
3.279 to 3.028, so the resolved arrangements are already locally compact and the
resolver is not what caps the score.
The original account below is preserved for provenance; the current verdict is
unresolved.

## Original account

exp-208 ended by naming three candidates for what caps the method at 0.98 and falling:
the resolver, which only translates; the proposal, one coarse-grid drop per run; and the
contact law. This round eliminates the first.

## The measurement

Adding a compaction pass — walk every square toward the bounding box’s centre, as far as
it goes without overlapping, at a shrinking step — changes `closed` at the best of 800
by **nothing** at n = 5, 10, 11 and 17, to four decimal places.

## The control is what makes that a result rather than a bug

The same pass, applied to the same arrangements scattered outward by 0.15 of a side
first:

| n | scattered | compacted | accepted moves |
| ---: | ---: | ---: | ---: |
| 5 | 3.2789 | 3.0284 | 20 |
| 11 | 4.2435 | 4.0301 | 47 |
| 17 | 5.2664 | 5.0553 | 90 |

The pass works. On the physics’ own output it accepts 6 to 24 moves and shrinks the box
in 4 of 40 trials at n = 5 and **0 of 40** at n = 11 and 17 — squares move inward, and
never the ones that set the box.

## What this leaves

The separated arrangements are already locally compact, so the number this campaign
reports is not being depressed by how it is measured.
Two candidates remain, and the proposal is the cheaper to test: every run makes one drop
into the emptiest cell of a coarse grid, and a method whose median is below the trivial
grid may be failing at the proposal rather than at the annealing.

A rotating resolver is still untested and is a weaker candidate than it was — a
translation compaction finding nothing suggests the arrangements are jammed rather than
loose, and a jammed arrangement is not usually freed by turning one square.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
