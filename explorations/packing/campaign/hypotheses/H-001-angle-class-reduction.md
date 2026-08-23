---
title: H-001 — angle-class reduction beats free 3n-dimensional annealing
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-001
  kind: hypothesis
  claim: >-
    Optimal packings at n <= ~30 use at most 3 distinct tilt angles, so a two-level
    search - outer over (class count, class assignment, angles), inner LP-in-cell -
    reaches known optima in less budget than free 3n-dimensional annealing.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:2', 'search:6', 'search:18']
  criterion:
    shape: record
    metric: pair_tests_to_known_optimum
    direction: lower
    threshold: baseline annealer at equal pair-test budget
  instrument: >-
    Not yet built. Needs the LP-in-cell quench (H-002) plus an angle-class proposer in
    which squares carry a class index rather than a free angle.
  instrument_ready: false
  regime: ladder cases n = 5, 10 plus n = 11; equal pair-test budget; same polish backend
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 10, 11]}
  priority: 2
  cost_estimate: tier M (1e11 pair-tests)
  prereqs: [H-002]
  replication: false
  registered: retroactive
  notes: >-
    Merges the standing review's H-1 with this campaign's earlier two-tilt-restriction
    hypothesis, which was the same claim stated less generally (exactly 2 classes rather
    than at most 3). Kill: fails to reach known optima the baseline reaches, or corpus
    mining shows angle counts growing fast with n.
---
# H-001 — the search space is smaller than it looks

The
[LP-in-cell result](../../docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#r-2)
says the honest continuous dimension of this problem is `n` — the angles — not `3n + 1`.
Everything else is the combinatorial choice of cell, and the cell is solved exactly by a
linear program.

Empirically the angle count is far below `n`: Trump’s `n = 11` uses one non-trivial
tilt; the `s(17)` record uses two.
If that holds generally at small `n`, a search that treats angle *classes* as the outer
variable is searching a handful of dimensions rather than thirty-four.

## Why this is registered retroactively

It originates in the standing review’s register (as H-1), which was written before this
campaign’s registry existed, so it is marked `retroactive` rather than back-dated.
It absorbed this campaign’s own two-tilt-restriction hypothesis, which claimed the same
thing for the special case of exactly two classes.

The general form is better: two classes is what `n = 11` happens to use, and a
hypothesis tuned to the answer we already have would have proved much less.
The caution recorded against the narrow version still applies — a win here shows that
*given* the right angular structure the rest is easy, which is a real finding about
where the difficulty lives, but is not evidence that an unguided method could find
`n = 11`. The sweep is what keeps that honest: it must also hold at `n = 5` and
`n = 10`.
