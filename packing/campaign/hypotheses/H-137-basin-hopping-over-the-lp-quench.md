---
title: H-137 — basin hopping over the LP quench beats multistart at equal refined optima
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-137
  kind: hypothesis
  claim: >-
    At an equal budget of refined local optima, basin hopping -- perturbing the incumbent
    refined optimum with an adaptive step and accepting only on improvement -- reaches a
    lower median best side than multistart from fresh scatters, by at least 0.01 on at
    least half the cells, with both conditions refined by the same LP-in-cell quench.
  lane: search
  derived_from: []
  strategy_refs: ['search:10']
  criterion:
    shape: conditions
    metric: best_side
    direction: basin-hop lower by at least 0.01 on at least 3 of the 5 cells
    threshold: 0.01
  instrument: >-
    devtools/run_basin_hopping.py, budgeted in quench calls, every emitted pose repaired
    to strict validity and re-checked by sqpack.verify and by packing-campaign
    verify-archive
  instrument_ready: true
  regime: >-
    sqpack.research.quench.quench_bracket at a 4 s per-call wall bound, f64 scipy HiGHS,
    20 refined optima per seed, seeds 1-5, one loaded 10-core host
  instance: {axis: n, point: 11}
  sweep:
    axis: n
    points: [5, 10, 11, 17, 19]
  priority: 3
  cost_estimate: 1,000 quench calls per condition, about an hour of wall clock
  prereqs: []
  replication: false
  registered: '2026-09-08'
  notes: >-
    No `runner` block on purpose. The instrument writes an archive directory rather than
    a JSONL stream per (cell, seed), so the unattended harness must report this as needing
    an operator rather than guess an invocation. The budget is denominated in refined
    local optima because that is the unit Ellsworth's published statistics use, and
    because a move budget cannot compare a proposer whose move is a random displacement
    with one whose move is a sequence of linear programs.
---
# H-137 — the currency the record engines actually spend

## Why this is denominated in refined optima

Ellsworth’s `n = 51` run statistics classify 3,004 refined basins and find the record
family 4 times; at `n = 55`, 1,893 instances below `s = 8` contain 5 of the record
family.
The unit of work in a serious record search is one refined local optimum, and the
rate is basins per record.
A budget in moves cannot be compared across a proposer whose move is a displacement and
one whose move is a sequence of linear programs, because the two differ by orders of
magnitude in cost per move.

So this round gives both conditions **exactly the same number of quench calls** and asks
which spends them better.

## Why multistart is the right control

Grosso, Jamali, Locatelli and Schoen ran 50,000 local searches from random starts on
circles in a circle and found roughly **16,000 distinct local minimisers by `n = 40`**,
concluding that multistart is most likely not an appropriate method for this problem.
Against monotonic basin hopping, plain multistart with twice the local searches reached
the best known solution in only a few cases.
If that transfers, basin hopping should win here at equal refinements; if it does not,
the landscape’s funnel structure is different for squares and that is worth knowing.

## What the perturbation does, and the one parameter that matters

Gensane’s algorithm 4: perturb every square at once, refine, accept only on improvement,
double the step on success and halve it on failure, and restart the funnel when the step
collapses. Grosso and colleagues swept the displacement magnitude on circles and found a
sharp optimum — 14 failures at `1.2`, 8 at `1.0`, 8 at `0.6`, **3 at `0.8`** — with the
cleanest available statement of why: too small and the new start lies in the basin of
the current minimiser, too large and the method degenerates to multistart.
`eps0 = 0.1` here, adaptive from there, which is a guess and is marked as one.

## The honesty problem this instrument has to solve, and how

The quench solves a linear program, so its separations are non-negative only to the
solver’s tolerance, and a configuration one part in `1e16` inside itself is not a
packing. Every refined pose is therefore scaled apart about its own centroid by the
smallest factor that removes all penetration, re-measured, and emitted only when
`sqpack.verify` accepts it.
Scaling centres apart increases every separating-axis gap and leaves every half-extent
alone, so the repair is monotone and can only *raise* the side the round reports.

## What would refute it

Fewer than three of five cells improving by `0.01`. Two distinct readings would then be
open, and the round’s job is to say which: that the quench is too weak a refiner for the
proposal structure to matter, which is what
[exp-006](../series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md)
already concluded from the other direction — “the quench is a polisher, not a rescue” —
or that 20 refinements per seed is three orders of magnitude short of the regime where
the difference appears.

## Limits declared before the round

- 20 refined optima per seed against Ellsworth’s `10^3` per record hit.
  This round cannot see a record-rate effect and does not claim to.
- The quench’s per-call wall bound is 4 seconds, and at `n = 17` and `n = 19` that bound
  binds: the refiner returns unconverged and the arm is measuring a *truncated* refiner.
  That is recorded with the result rather than hidden by it.
- Five cells, all at `n <= 19`. Nothing here transfers to the larger cells, where one
  quench call would not finish.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
