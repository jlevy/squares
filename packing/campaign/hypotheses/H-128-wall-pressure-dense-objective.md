---
title: H-128 — a dense wall-pressure term repairs the sparse objective without the inflation rewrite
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-128
  kind: hypothesis
  claim: >-
    Adding an aggregate inward wall-pressure term to the annealing energy, so that every
    square has a nonzero derivative of the objective rather than only the two to four
    attaining the binding span, lowers the median best side over five seeds by at least
    0.01 against the paired control with disjoint seed ranges, on at least half the cells
    of the non-grid subset, at equal pair-test budget.
  lane: search
  derived_from: []
  strategy_refs: ['search:10']
  criterion:
    shape: paired
    metric: best_side
    direction: candidate lower by at least 0.01 on at least 6 of the 11 cells
    threshold: 0.01
  instrument: >-
    devtools/run_arm_sweep.py over sqsearch --mu0/--mu1, at equal --budget-pair-tests,
    gated by sqsearch --selftest and re-checked pose by pose by packing-campaign
    verify-archive
  instrument_ready: true
  regime: >-
    sqsearch 0.1.0 at the commit under test, f64 screening, 8 chains, 1.25e9 pair tests
    per chain, 4 rayon threads, seeds 1-5, one host
  instance: {axis: n, point: 11}
  sweep:
    axis: n
    points: [5, 10, 11, 17, 19, 26, 27, 29, 37, 50, 52]
  priority: 2
  cost_estimate: 5.5e11 pair tests, about 20 minutes wall per arm on a loaded 10-core host
  prereqs: []
  replication: false
  registered: '2026-09-08'
  runner:
    command: './sqsearch/target/release/sqsearch --n {n} --seed {seed} --chains 8 --threads 4 --budget-moves 9223372036854775807 --budget-pair-tests 1250000000 --mu0 5.0 --mu1 5.0'
    cells: [5, 10, 11, 17, 19, 26, 27, 29, 37, 50, 52]
    seeds: [1, 2, 3, 4, 5]
    timebox: 1h
  notes: >-
    This is the *surrogate* form of the fix, not the formulation change. The 2026-09-08
    survey's section 7 asks for the inflation rewrite, in which the container is fixed and
    a common square side is maximised; section 8 offers the wall-pressure term as the
    cheap partial substitute that is ablatable against it. Registered separately from
    H-127 so that one round tests one move, which is H-031's standing rule.
---
# H-128 — making every square feel the objective, cheaply

## The term, and what it is a surrogate for

`geom::spread` is the mean squared distance of the centres from the centre of their own
bounding box, and the energy becomes

```
F = required_side + lambda * total_overlap + mu * spread
```

with `mu` ramped geometrically like `lambda`. `required_side` is a max over two to four
squares; `spread` is a sum over all `n`, so every single-square translation changes the
energy. That is the whole intent: a uniform inward pressure that compacts the
configuration while the side term is flat.

It is deliberately **not** the inflation formulation.
Inflation fixes the container and maximises a common square side, and the survey argues
it is the highest-value change available; it is also a rewrite of `geom.rs`. The honest
description of `mu * spread` is that it adds a dense term beside the sparse one rather
than replacing it.

Two properties are what make it safe to measure:

- **The reported side is never the pressured energy.** `best_side` is tracked from
  `required_side` under the overlap gate in every arm, so a pressure weight can lower
  the energy the search walks on and can never lower the number the round reports.
- **The control is bit-identical.** The term is off unless both ends of the ramp are
  positive, and the selftest pins the control chain’s value to the literal the pre-arm
  engine printed.

## What would refute it

Fewer than six of eleven cells improving by `0.01` with disjoint seed ranges.
Since `spread` and `required_side` disagree about what a good packing is — a compact
blob is not the same object as a tight square — a plausible failure mode is that the
term helps early and hurts late, and the ramp is the only thing standing between those.
A refutation here is evidence that the *surrogate* is the wrong shape and that the
inflation rewrite has to be built to answer the question.

## Limits declared before the round

- One functional form and one parameter point on the scoring cells.
  A negative result is a result about that point, not about wall pressure in general.
- `f64` screening only; nothing here can be certified.
- The term is isotropic.
  Squarl’s wall-pressure solver pushes each square from the container boundary it is
  nearest, which is a different and more local operator; this one has no directional
  structure at all.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
