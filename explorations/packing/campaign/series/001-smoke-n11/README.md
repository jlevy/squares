---
title: series-001 — smoke pass at n = 10, 11, 12
softschema:
  contract: packing.squares:Series/v1
  schema: ../../schemas/series.schema.yaml
  envelope: series
  status: enforced
series:
  id: series-001
  slug: smoke-n11
  title: Smoke pass — reproduce what is known, then try the obvious hypotheses
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
    every number here starts from zero.
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
# series-001 — the smoke pass

The first pass exists to test the loop, not the mathematics.
Its hypotheses are deliberately the obvious ones, its cells are mostly cases whose
answers are already known, and a round that merely confirms something everyone expects
is a success here — because what is under test is the machinery that will carry the
non-obvious rounds later.

## What has to be true before this series can conclude anything

Three things, in order, and each was already worth its cost.

**The engine must recover a case whose answer is proved.** `n = 10` is the positive
control: `s(10) = 3 + 1/√2`, and crucially it is *not* the grid — it needs a genuine
tilted family, so recovering it exercises the part of the search that matters.
An early version of the search never left the grid basin at all, and would have produced
a whole night of confident, meaningless numbers at `n = 11`. The control caught it in
seconds.

**The engine must fail to beat a case it should not beat.** `n = 12` is the negative
control. The 4×4 grid is almost certainly optimal, so a run reporting anything below `4`
has found a bug in the geometry, not a packing.
A search harness that has never been asked to fail has not been tested.

**The declared budget must actually bind.** It did not, at first: a restart cap stopped
every chain before the move budget did, so `--budget-moves` was inert and two strategies
compared “at equal budget” would have had unequal work.
The tell was that results got *worse* when the declared budget was raised.

## What this series will not do

It will not attempt a record.
Screening in `f64` cannot certify one — Trump’s packing has 14 of its 55 pairs touching
at exactly zero separation, which no floating-point check can decide — so a record claim
needs the polish and exact tiers, and those are the subject of a later series.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
