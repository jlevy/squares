---
title: H-205 — a constraint-projection search reaches feasible packings where a penalty cannot
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-205
  kind: hypothesis
  claim: >-
    Divide and concur searched with relaxed-reflect-reflect, run cold over a bounded
    square container with no record consulted, reaches an exactly feasible packing
    strictly below the trivial grid on at least three of the four cells n in {5, 10, 11,
    17}, and comes within 1 per cent of the best known on at least half of them.
  lane: search
  derived_from: []
  strategy_refs: []
  criterion:
    shape: conditions
    metric: best_side
    direction: strictly below the trivial grid on at least 3 of 4 cells, within 1 per cent on at least 2
    threshold: 0.01
  instrument: >-
    devtools/run_projection_ratchet.py over devtools/divide_and_concur.py, with every
    reported pose re-checked out of process by sqpack.verify
  instrument_ready: true
  regime: >-
    f64 numpy, corner-space replicas, beta in {0.3, 0.5}, m-monotonicity stop at m = 700,
    5,000 iterations per run, six attempts per ratchet step, container schedule floored at
    1e-3, one loaded 10-core host
  instance: {axis: n, point: 11}
  sweep:
    axis: n
    points: [5, 10, 11, 17]
  priority: 2
  cost_estimate: about 200 solver calls per ratchet run, an hour of wall clock for a 16-run arm
  prereqs: []
  replication: false
  registered: '2026-09-09'
  notes: >-
    Registered after the pilot runs and before the arm campaign, so the tier is
    exploratory and the record says which numbers preceded the claim. The pilot
    established that the method produces exactly feasible arrangements at all, which is
    the precondition the penalty calibration failed; the claim above is about how close
    it gets, which the pilot did not measure.
---
# H-205 — the first mechanism here whose failures are visible

## Why this claim, and why now

The
[penalty calibration of 2026-09-08](../../atlas/known-best/video/spikes/v2-transitions/NOTES.md)
ended in a precondition failure rather than a ranking.
Zero of 48 runs finished feasible; the least overlap anywhere was `0.0042` of a unit
side; and holding eleven squares still for thirteen times as many steps moved the
overlap from `0.004578` to `0.004570` and the container side not at all.
The reason is structural rather than budgetary.
A penalty force settles where the springs balance the walls, and the residual overlap
there is pressure divided by stiffness, so only infinite stiffness removes it and the
timestep forbids that.
The stiffest law in that sweep reported `3.88987` against the standing record `3.87708`
— a third of a per cent off a record it had no packing for.

A ranking presumes the thing being ranked can produce an answer.
So the question that has to be settled before any calibration means anything is whether
*some* mechanism available here lands exactly on the constraint set.

The
[simulation survey](../../../docs/project/research/research-2026-09-09-simulation-mechanisms-for-packing.md)
answers it by name. Divide and concur has no potential, no derivative and no smoothness
requirement: it alternates two projections, and its fixed points are packings by
construction.
It is also the only mechanism in either survey with a cold, whole-benchmark
result on the sibling problem — 197 values of `n`, up to 400 random starts each, “No
information about the known packings … apart from their densities”, best known reached
within `1e-9` on 143 and beaten on 38.

## What would make this wrong

Three distinct outcomes falsify it, and they are worth separating because they point at
different repairs.

- **It does not reach feasibility.** If the iteration wanders without converging, or
  converges to points that are not packings, the mechanism is no better than the penalty
  and the survey’s rank ordering is wrong for this problem.
- **It reaches feasibility but not below the grid.** The trivial grid is feasible for
  every `n` and is where the container schedule starts, so a run that never improves on
  it has found nothing.
  This is the outcome to watch: a grid of `k` squares in a row needs a container of
  exactly `k`, so every tightening makes the grid topology infeasible all at once and
  there is no small repair to find.
  That is the same wall [H-201](H-201-simultaneous-perturbation-move.md) measured for
  the annealing engine, arriving by a different road.
- **It reaches feasibility below the grid but stalls well short of the records.** Then
  the mechanism works and the schedule is wrong, and the repair is in the container
  ratchet and the restart policy rather than in the projections.

## What this does not claim

Nothing about optimality, and nothing about beating the existing engine.
`sqsearch` with a long schedule and the collective move reaches `3.8958` at `n = 11` and
`4.7071` at `n = 17`, at a budget three orders of magnitude larger than anything here.
This claim is about a property the existing engine’s physics arm does not have — that
what comes out is a packing — and about how far a first, honest implementation gets.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
