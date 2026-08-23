---
title: H-004 — Trump's configuration has an attracting neighbourhood
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-004
  kind: hypothesis
  claim: >-
    Started from Trump's exact configuration perturbed by uniform noise of size eps, the
    stock annealer returns to within 1e-6 of it in at least half of runs at eps = 1e-3.
  lane: search
  derived_from: []
  strategy_refs: ['search:12']
  criterion:
    shape: determination
    metric: fraction of runs returning within 1e-6
    direction: at least 0.5 at eps = 1e-3
  instrument: >-
    sqsearch seeded from sqpack.packings.trump11 (exact, converted to f64) with uniform
    perturbation, swept over eps in {1e-5, 1e-4, 1e-3, 1e-2, 1e-1}, 40 runs per eps.
  regime: sqsearch 0.1.0, f64 screening
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: 2e9 moves, under a minute
  prereqs: []
  replication: false
  registered: '2026-08-22'
  notes: >-
    The cheapest informative measurement in the campaign, and it explains the baseline
    rather than merely adding to it. The eps at which the return rate collapses IS the
    basin width, so a refutation is as quantitative as a confirmation.
---
# H-004 — measuring the thing the baseline could not explain

The baseline says the annealer does not find Trump’s packing.
Two very different worlds produce that observation: one where the basin is real but
small, and finding it is a matter of restart count; and one where the configuration is
an isolated point with no attracting neighbourhood at all, where no amount of undirected
restarting will ever land on it.

This distinguishes them directly, by starting *inside* the answer and walking outward.
The `eps` at which the return rate collapses is the basin width, in the units the search
actually moves in — so this produces a number either way, and a refutation is exactly as
informative as a confirmation.

## Why rigidity makes the refutation likely

Trump’s packing is flagged rigid in the record catalogue and verified here to have 14 of
its 55 pairs touching at exactly zero gap.
Rigidity means the contact conditions determine `s` exactly, which is what makes the
algebraic value computable — and it is also what suggests the configuration is a point
rather than a region.

This is the measurement [H-002](H-002-budget-scaling.md) is predicated on, and the two
should be read together: if the basin is measure-zero, budget scaling cannot help, and
the campaign’s weight should move to the structural rows of the
[idea board](../ideas.md).
