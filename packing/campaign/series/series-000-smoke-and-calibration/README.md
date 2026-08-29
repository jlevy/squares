---
title: series-000 (S0) — smoke and calibration
softschema:
  contract: packing.squares:Series/v1
  schema: ../../schemas/series.schema.yaml
  envelope: series
  status: enforced
series:
  id: series-000
  slug: smoke-and-calibration
  title: 'S0: smoke and calibration — prove the machinery, establish every baseline metric'
  status: open
  opened: '2026-08-22'
  closed: null
  goal: >-
    Prove the loop works end to end on cheap, checkable claims — that the engine
    recovers a proved case, refuses to beat a grid it should not beat, and that a
    round's numbers survive the trip from JSONL to artifact to ledger — before
    anything subtle is attempted.
  opened_because: >-
    First series. There is no prior instrument, so nothing is carried forward and
    every number here starts from zero. Renumbered from series-001 when this campaign
    merged with the standing review's series plan, so that S0-S6 map onto
    series-000..series-006 exactly; no artifact had been published under the old id.
  instrument:
    name: sqsearch
    version: 0.1.0
    commit: d6a1057
    selftest: >-
      sqsearch --selftest — 12 checks: the simplified four-axis SAT against the
      naive form, three known-geometry cases, chain reproducibility from
      (seed, chain), chain divergence, and a positive control that recovers
      s(5) = 2 + 1/sqrt(2).
  supersedes: null
  carries_forward: []
  budget: one overnight session, 40 rounds
---
# series-000 (S0) — smoke and calibration

## Current Scope and Safe Reading

This artifact opened as **S0** of the
[standing review’s series plan](../../../../docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#series-and-priorities):
prove all the machinery works end to end and establish every baseline metric, before any
strategy is tested.

The record has outgrown that opening description.
The current record contains experiments `exp-001` through `exp-044`, including search
baselines, exact proof determinations, event-contract controls, and the H-023 sequence
through the complete first-order inventory in `exp-038` and fixed-angle polytope paths
in `exp-039`. Exp-040 retains an unresolved rotating-path checker and its finite
independent-review blockers.
Exp-041 rejects a stricter proof-perimeter criterion on an exact endpoint-only zero axis
while retaining the candidate paths and path-feasibility question.
Exp-042 is the accepted endpoint-aware successor: it certifies six explicit R4/R5 paths
and positive pathwise first-order stresses with twenty semantic controls and retained
replay. Exp-043 stops unresolved before retained measurement: its draft checker passes
temporary checks, but independent review finds five finite second-order instrument
defects. The W7 exact-jet repair now passes source-bound tests.
Exp-044 stops unresolved without target measurement after freezing its case-level
criterion and adding a reviewed production row-jet builder; weighted stress, sheet,
scale, mutation, and disposition integration remain open.
Those records do not imply that full connectivity has been established.
Those result shapes are not pooled or compared merely because they share `series-000`.
Each experiment’s `subject`, method, regime, and provenance govern what comparison is
legal; the frontmatter `instrument` records the series’ opening search instrument, not
every checker later used.

`think-i08r` tracks the all-at-once persisted-record migration needed to restore strict
series boundaries.
Until that lands, treat this as a legacy campaign container and do not
infer a shared numerical regime from its id.
The original S0 intent below remains useful history and still explains why the early
controls exist.

The first pass exists to test the loop, not the mathematics.
Its hypotheses are deliberately the obvious ones, its cells are mostly cases whose
answers are already known, and a round that merely confirms something everyone expects
is a success here — because what is under test is the machinery that will carry the
non-obvious rounds later.

## What Had to Be True Before S0 Could Conclude Anything

Three things, in order, and each was already worth its cost.

**The engine must recover a case whose answer is proved.** `n = 10` is the positive
control: `s(10) = 3 + 1/√2`, and crucially it is *not* the grid — it needs a genuine
tilted family, so recovering it exercises the part of the search that matters.
An early version of the search never left the grid basin at all, and would have produced
a whole night of confident, meaningless numbers at `n = 11`. The control caught it in
seconds.

**The engine must reject configurations known to be invalid.** The original campaign
called `n = 12` a negative control because the 4×4 grid is believed optimal.
That was not a known-answer test: `s(12) = 4` is open, so a valid result below `4` would
be a discovery. The valid guard is independent geometry verification plus deliberately
invalid fixtures; `n = 12` remains an open-case calibration
([D-042](../../../../defects.md)).

**The declared budget must actually bind.** It did not, at first: a restart cap stopped
every chain before the move budget did, so `--budget-moves` was inert and two strategies
compared “at equal budget” would have had unequal work.
The tell was that results got *worse* when the declared budget was raised.

## What S0 Could Not Tell Us

The review’s calibration ladder and this series’ controls both use `n = 5` and `n = 10`.
The
[search-philosophy report](../../../../docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md#calibration-must-match-mechanism-not-just-difficulty)
makes the sharp point that **both proved optima are 45°-tilt mechanisms** — symmetric,
and sitting in basins blind search reaches without help.
An engine can pass this ladder and remain structurally blind to what `n = 11` actually
demands: an oblique core locked at `≈ 40.182°`, a mechanism **no proved case
exercises**.

So the original S0 controls validate *machinery*, not *strategy*, and their passing
results must not be read as evidence that the search can find records.
Mechanism-matched calibration was assigned to a later topical stage in the original
plan. Exp-011 subsequently ran the `n = 17` cell inside this legacy container; its own
subject and regime carry that evidence, not the S0 label.

## What This Series Cannot Claim

The shared id does not establish that all 42 experiments used one executable instrument
or that unlike measurements are comparable.
Screening in `f64` also cannot certify a record—Trump’s packing has 14 of its 55 pairs
touching at exactly zero separation, which no floating-point check can decide.
A record claim still needs exact promotion, whatever series contains the proposing
screen.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
