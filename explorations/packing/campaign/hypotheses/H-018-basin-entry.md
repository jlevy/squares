---
title: H-018 — the polish loop falls into Trump's cell and stays
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-018
  kind: hypothesis
  claim: >-
    Started from Trump's exact configuration perturbed by uniform noise of size eps, the
    search returns to within 1e-6 of it in at least half of runs at eps = 1e-3.
  lane: search
  derived_from: []
  strategy_refs: ['search:12', 'search:19']
  criterion:
    shape: determination
    metric: fraction of runs returning within 1e-6
    direction: at least 0.5 at eps = 1e-3
  instrument: >-
    sqsearch seeded from sqpack.packings.trump11 (exact, converted to f64) with uniform
    perturbation, swept over eps in {1e-5, 1e-4, 1e-3, 1e-2, 1e-1}, 40 runs per eps.
  instrument_ready: true
  regime: sqsearch 0.1.0, f64 screening; re-run against the LP polish once H-002 lands
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: 2e9 moves, under a minute
  prereqs: []
  replication: false
  registered: '2026-08-22'
  notes: >-
    The search-philosophy report names basin-entry tests as mechanism-matched
    calibration: they separate "search cannot find the region" from "the refiner cannot
    hold it", two failures with identical symptoms and different fixes. Runnable today,
    unlike most of the strategy register.
---
# H-018 — refuted; the finite quench measured its own residual

The registered claim is refuted by
[exp-005](../series/series-000-smoke-and-calibration/experiments/exp-005-basin-entry-n11.md):
at `eps = 1e-3`, zero of forty trials in every arm returned within `1e-6`. Across the
tested schedules the residual scaled approximately linearly with the perturbation and
decreased when effort increased.

That pattern diagnoses incomplete convergence of the tested refiner.
It does **not** establish an attracting basin, a basin radius, isolation, or
terminal-component membership; those require a converged quench and the component
analysis now registered in H-021 through H-023.

## Original rationale

exp-001 says the annealer does not find Trump’s packing.
Two very different worlds produce that observation: one where the basin is real but
small, so finding it is a matter of restart count; and one where the configuration is an
isolated point with no attracting neighbourhood, where undirected restarting will never
land on it.

Starting *inside* the answer and walking outward distinguishes them directly.
The proposed diagnostic was the `eps` at which return rate collapsed.
The completed round showed that, under a finite non-converged refiner, this score is a
convergence measurement rather than a basin-width measurement.

## Where it sits among the merged register

[H-012](H-012-record-basins-are-rare.md) is designed to measure component attraction
frequency across a declared landscape.
This round attempted a cheaper inside-out diagnostic, but the completed evidence shows
its finite-quench score did not measure a component radius.
The
[search-philosophy report](../../docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md#calibration-must-match-mechanism-not-just-difficulty)
lists basin-entry tests as one of three mechanism-matched calibration targets, alongside
`s(17)` and inflated `n = 11` — none of which the current `n = 5` / `n = 10` ladder
exercises, because both proved cases are 45° mechanisms.

A successor may reuse the perturbation fixtures only after it declares a terminal-
component relation and an independently checked convergence condition.
H-002’s fixed- cell LP result alone does not supply either one.
