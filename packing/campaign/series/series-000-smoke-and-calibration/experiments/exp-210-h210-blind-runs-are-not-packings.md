---
title: exp-210 — every blind run of the workbench's physics ends overlapping
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-210
  series: series-000
  title: Every blind run of the workbench's physics ends overlapping
  date: '2026-09-12'
  hypotheses:
  - H-210
  tier: exploratory
  subject:
    label: the workbench's contact-and-jiggle simulation in blind mode
    engine: workbench page, build 4.4 MB, branch claude/annealing-search-benchmark
    engine_commit: d3c3a778
    assurance: numerically-checked
    method: numerical-f64
    tolerance: 1e-5 of a unit side of deepest pairwise overlap, taken from the snapped run's
      own float noise rather than chosen
    host_system: macOS on Apple silicon, one headless Chromium
    selftest_passed: true
    precision:
      binary_bits: 53
      rounding: nearest-even
    migration_annotation: '2026-09-13: source reference mapped from pre-purge ee27f8e3 to reachable
      d3c3a778; the retained harness and workbench source trees compare equal in Git. Original
      run provenance was not recaptured.'
  instance:
    axis: n
    point: 11
    role: target
  method:
    operator: claude-opus-5, unattended
    control: the snapped trajectory, which ends on the record's poses by construction
    candidate: the blind trajectory, told nothing about the target
    trials: 15000
    interleaved: false
    commit: d3c3a778
    entry_point: packing/devtools/bench_annealing.py
    command: python -m devtools.bench_annealing --n 5 10 11 17 26 29 --seeds 2000 --anneal 6
    record: packing/campaign/results/annealing/
  results:
  - shape: determination
    question: does any blind run end on an arrangement with no overlapping squares, checked
      by a separating-axis test over the final poses written in the harness rather than read
      off the simulation
    role: guard
    outcome: invalid
  - shape: conditions
    metric: deepest pairwise overlap in the final arrangement, unit sides
    control_median: 1.0e-06
    candidate_median: 0.035146
    control_range:
    - 5.5e-07
    - 1.01e-06
    candidate_range:
    - 0.035146
    - 0.086189
    change_pct: 3400000.0
    overlapping: false
  complexity:
    lines_changed: 96
    new_failure_modes:
    - a trial can now be refused as invalid rather than recorded as poor
    notes: The guard is the change; the simulation was not touched. Adding it turned every previously
      recorded result in this campaign into a measurement of something else.
  verdict:
    decision: unresolved
    primary_criterion: the deepest pairwise overlap in the final arrangement
    reason: Historical summary retained; the raw geometry and exact-check receipts are absent
      from the reachable branch. Prefix best-of-k and incomplete cohort metadata do not establish
      the registered comparison. Re-admission requires reproducible valid trials and disjoint-block
      reporting.
    commit: d3c3a778
  effort:
    stopped_by: dependency
    wall_seconds: unrecorded-historical
    migration_annotation: '2026-09-13: no complete elapsed-time receipt was retained. Per-trial
      median milliseconds and approximate prose budgets cannot recover total wall or operator
      time. This marker records missing history and is unavailable to new experiments.'
---
# exp-210 — every blind run of the workbench’s physics ends overlapping

## Correction — 2026-09-13

The retained summaries lack raw geometry and exact-check receipts, and best-of-k is a
single prefix rather than a distribution over independent blocks.
These values remain historical observations and are not admitted evidence for the
registered comparison.
The original selftest flag describes the original account; no historical run has been
replayed in this repair.
The declared 15,000 trials disagree with the command, which requests 6 × 2,000 = 12,000;
no retained manifest resolves that difference.
The older divide-and-concur experiment keeps exp-206; this record is renumbered exp-210.

The source reference `ee27f8e3` was rewritten when raw JSONL files were removed from the
branch. Its retained harness and workbench source compare equal to reachable `d3c3a778`
with `git diff`; the metadata now uses that reachable source.
This is a source mapping, not a reconstructed run receipt.
Timing is explicitly unrecorded rather than estimated or entered as zero.

The original verdict was **accepted**: 15,000 of 15,000 blind trials end with squares
inside each other by 0.03 to 0.12 of a unit side, at every n and every shake level
including zero, against a snapped control that scores 1e-6. The original account below
is preserved for provenance; the current verdict is unresolved.

## Original account

## What was measured

The deepest overlap between any two squares in the arrangement a run **ends on**, by the
separating axis theorem, computed in the harness from the final poses with none of the
simulation’s own bookkeeping.
`maxPenetration`, which the page already reports, is a running maximum over the whole
trajectory and says nothing about where the squares stopped.

## The control is what makes the tolerance a measurement

| mode | n=5 | n=11 | n=17 |
| --- | ---: | ---: | ---: |
| snap — ends on the record’s poses by construction | 5.5e-7 | 1.0e-6 | 7.3e-7 |
| free — physics with a target, no snap | 3.9e-5 | 4.5e-5 | 3.1e-2 |
| blind — physics with no target | 8.4e-2 | 3.5e-2 | 8.6e-2 |

The snapped row is the float noise the stored poses carry.
Two orders of magnitude separate it from the smallest real overlap, so 1e-5 refuses
overlaps without refusing arithmetic.

## What it means

The workbench’s physics does not settle to a packing.
The animation looks right because its last frame is snapped onto the record; underneath,
the contacts stay soft and the squares come to rest inside each other.

The page’s own gap bar already knew this — it reports `valid: false` and hides its
pointer during a blind run — and nothing had connected that to the question of whether
the physics is a search.

## What the prediction got wrong

The hypotheses this campaign opened with asked *how well* the blind run searches: which
n are hard, whether the schedule or the drop decides, how the tail scales.
All of them assumed the thing being scored was a packing.
The first two rounds produced clean, reproducible, entirely meaningless numbers —
including thirty parameter cells reporting a container **below** the known-best side,
which should have been the tell and was instead read as a promising tail.

The lesson is the one the method already names and this round had to learn: an
independent check that the result is real, **before** it may be good.
The check cost ninety lines and would have cost nothing at the start.

## What follows

The instrument needs a resolution phase — a final stage that separates overlapping
squares and reports the container the separated arrangement actually needs — before any
number from it is about packing.
That is a change to the method rather than to its dials, and it is what the next round
builds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
