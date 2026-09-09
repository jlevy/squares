---
title: H-135 — a simultaneous all-square perturbation move rescues the cells single-square moves cannot leave
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-135
  kind: hypothesis
  claim: >-
    With a simultaneous perturbation proposal added to the ordinary move menu at
    probability p_perturb, and every other parameter at its sqsearch default, the median
    best side over five seeds is at least 0.01 lower than the paired single-square-only
    control, and the two seed ranges do not overlap, on at least half the cells of the
    non-grid subset, at equal pair-test budget.
  lane: search
  derived_from: []
  strategy_refs: ['search:10']
  criterion:
    shape: paired
    metric: best_side
    direction: candidate lower by at least 0.01 on at least 6 of the 11 cells
    threshold: 0.01
  instrument: >-
    devtools/run_arm_sweep.py over sqsearch --p-perturb/--perturb-scale, at equal
    --budget-pair-tests, gated by sqsearch --selftest and re-checked pose by pose by
    packing-campaign verify-archive
  instrument_ready: true
  regime: >-
    sqsearch 0.1.0 at the commit under test, f64 screening, 8 chains, 1.25e9 pair tests
    per chain, 4 rayon threads, seeds 1-5, one host, control and candidate run from the
    same plan file in the same process
  instance: {axis: n, point: 11}
  sweep:
    axis: n
    points: [5, 10, 11, 17, 19, 26, 27, 29, 37, 50, 52]
  priority: 1
  cost_estimate: 5.5e11 pair tests per arm, about 20 minutes wall per arm on a loaded 10-core host
  prereqs: []
  replication: false
  registered: '2026-09-08'
  runner:
    command: './sqsearch/target/release/sqsearch --n {n} --seed {seed} --chains 8 --threads 4 --budget-moves 9223372036854775807 --budget-pair-tests 1250000000 --p-perturb 0.05 --perturb-scale 4'
    cells: [5, 10, 11, 17, 19, 26, 27, 29, 37, 50, 52]
    seeds: [1, 2, 3, 4, 5]
    timebox: 1h
  notes: >-
    Registered from the 2026-09-08 annealing survey, which proposes exactly this move as
    the cheapest structural change available to sqsearch and predicts a large payoff by
    analogy with Gensane's spheres-in-a-cube measurements. The two free parameters were
    fixed by a calibration pilot on held-out non-grid cells (n = 18, 40) before this
    round ran, so nothing was tuned on the cells that score it.
---
# H-135 — the move the record engines have and `sqsearch` does not

## The defect this is aimed at

`required_side(c) = max(hix - lox, hiy - loy)` is a max over the two to four squares
attaining the binding span.
Every *other* single-square translation leaves the side term exactly unchanged, so its
energy change comes only from the overlap term, and once `lambda` has ramped, any move
that creates overlap is rejected outright.
At `n = 17` roughly four proposals in seventeen can improve the objective at all; at
`n = 52`, four in fifty-two.
The remainder are a random walk on a plateau bounded by rejection.

That is an analytic property of the objective, not a measurement, and it predicts
exactly the failure
[exp-011](../series/series-000-smoke-and-calibration/experiments/exp-011-h-020-n17.md)
recorded: the annealer returned the trivial `5.0` at `n = 17` on five seeds of five.
It is also the failure the record-holders describe in their own words.
The provenance comment on the `n = 55` record says that without special modifications a
GPU annealer “almost always gets stuck just above the trivial size”.

## Why this move rather than another

Gensane and Ryckelynck’s algorithm — the first that worked on squares in a square, and
the holder of the `n = 29` record from 2004 until December 2025 — is not an annealer at
all.
Its acceptance rule is strictly greedy and its escape mechanism is layer 3: displace
*every* object simultaneously, then re-converge.
Their stated reason is that greedy single-object search converges to configurations that
are **solid** — no single object can be moved to improve the packing — and solid is
weaker than locally optimal.
Simultaneous perturbation is what walks along a connected path of solid configurations
to a genuine local optimum.

Gensane measured the payoff on spheres in a cube, where a particle has three degrees of
freedom, as a freely rotating square in the plane does: at `n = 12`, ten thousand plain
billiard runs gave six digits and adding perturbation gave six more; at `n = 21`, two
digits became twelve.

`search.rs` already contains `perturb`, written for the basin-entry mode and not on the
ordinary move menu. Putting it there is the cheapest structural change available.

## What would refute it

Fewer than six of the eleven cells improving by `0.01` with disjoint seed ranges.
That result would say either that the plateau diagnosis is wrong, or that the plateau is
not the binding constraint at this budget — and it would move the next attempt to the
inflation rewrite rather than to more moves.

## Limits declared before the round

- `f64` screening only, and no claim here can be certified.
- One host, one engine version, one budget tier.
  Nothing here says anything about the same move at a budget two orders of magnitude
  larger, which is the regime the record engines actually run in.
- The move’s two parameters are calibrated, not swept: a single point in that plane is
  measured on the scoring cells, and a negative result is a result about that point.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
