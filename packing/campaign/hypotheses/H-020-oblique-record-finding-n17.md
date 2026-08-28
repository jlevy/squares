---
title: H-020 — stock annealer reaches the n=17 oblique standing best in one baseline seed
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-020
  kind: hypothesis
  claim: >-
    The stock annealer reaches within 1e-4 of the standing best at n = 17, whose record
    uses genuinely oblique structure (tilts of 0, +39.80496 and -36.62379 degrees), on
    at least one seed of five at the baseline budget of 1e8 moves per chain.
  lane: search
  derived_from: []
  strategy_refs: ['search:10']
  criterion:
    shape: record
    metric: best_side
    direction: lower
    threshold: 1e-4
  instrument: 'sqsearch --n 17 --chains 8 --budget-moves 1e8, five seeds, gated by --selftest'
  instrument_ready: true
  regime: sqsearch 0.1.0, f64 screening, deterministic seeds 1-5
  instance: {axis: n, point: 17}
  sweep: {axis: n, points: [17]}
  priority: 2
  cost_estimate: 4e9 moves, ~7 minutes wall at the measured 9.9M moves/s
  prereqs: []
  replication: false
  registered: '2026-08-23'
  runner:
    command: './sqsearch/target/release/sqsearch --n {n} --seed {seed} --chains 8 --budget-moves 100000000'
    cells: [17]
    seeds: [1, 2, 3, 4, 5]
    timebox: 1h
  notes: >-
    Codifies idea-board row 20, shaped since the strategy report and never run. The
    prediction is that it fails; a one-seed probe at 4e7 moves per chain already returned
    exactly 5.0, the trivial 5x5 grid, against Bidwell's 4.67553. Recorded here before the
    round so that outcome is evidence rather than hindsight.
---
# H-020 — the only cell that tests record-*finding*

## Why this cell and not another

The campaign’s ladder is `n = 5` and `n = 10`, and both are **45° mechanisms**:
symmetric arrangements that blind search reaches without help.
`n = 12` is the trivial grid.
So every control the campaign runs validates *machinery* — that the engine can descend,
that the refiner converges, that the verifier decides — and **none of them exercises the
thing `n = 11` actually demands**, which is an oblique core whose trigonometric
coordinates are algebraic but whose nonzero radian angle is transcendental, and which no
proved case uses.

`n = 17` is the nearest case whose record does.
Bidwell’s 1998 packing uses tilts of `0°`, `+39.8049589798°`, and `−36.6237863834°`: two
unequal non-trivial orientations against a grid frame, structurally the same *kind* of
object as Trump’s, at a case that is cheap to run.
The former `±40°` shorthand was not an accurate transcription of the primary SVG.

The [synopsis](../../SYNOPSIS.md#the-lay-of-the-land-by-n) calls it the largest unforced
gap in the campaign’s coverage, and the
[runbook](../README.md#subject-and-the-instance-axis) has carried it in the declared
instance axis since the campaign opened.
It has never been run.

## What either outcome buys

This is registered because **both branches are informative**, which is rare enough to be
worth saying explicitly.

- **If the annealer reaches the published `n=17` standing best** — the engine can find
  this oblique record under the registered regime.
  Then the `n = 11` failure is more plausibly instance-specific: its basin may be rarer,
  narrower, or less forgiving.
  That localises the problem and makes [H-012](H-012-record-basins-are-rare.md)’s rarity
  measurement the right next question.
- **If it does not** — this version of the engine did not reach this oblique standing
  best in five seeds at the registered budget.
  That supports testing changed move sets, schedules, and structured proposers; it does
  not establish blindness at other `n`, larger budgets, or even along trajectories whose
  final retained best is the grid.

Failure under this registered regime is the prediction.
A single seed at 40% of the round’s budget already returned **exactly `5.000000000`** —
the trivial `5×5` grid, `+0.324` from Bidwell.
Because only the retained best is stored, that result does not say whether the
trajectory left the grid neighbourhood.
Recorded here, before the round, so the scoped outcome is evidence rather than
hindsight.

## What this does not claim

Not that `s(17) = 4.67553…`. That case is **open**, and the standing best is an upper
bound like any other.
The criterion is reaching the standing best, not proving it optimal.

Nor does a failure here identify *which* part of the proposer underperformed — the move
set, cooling schedule, absent angle-class structure, budget, or retention rule.
It says only that the registered composite did not meet the declared `n=17` criterion.
Separating those is [H-001](H-001-angle-class-reduction.md)’s job and needs an
instrument that does not exist.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
