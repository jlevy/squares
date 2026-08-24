---
title: H-011 — the small-n landscape is censusable
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-011
  kind: hypothesis
  claim: >-
    Under a versioned proposer P, deterministic quench Q, and terminal-component
    equivalence E, LP-quenching multistarts at n <= 10 yields a component-discovery
    curve whose estimated unseen mass falls below a preregistered threshold within
    tier-S budget.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:12', 'search:18']
  criterion:
    shape: determination
    metric: 95% upper confidence bound on unseen terminal-component mass by n = 8
    direction: below 0.05 within tier S
  instrument: >-
    Not yet built. Multistart proposer + LP quench (H-002) + terminal-component
    classification + canonical endpoint comparison, emitting a provenance-complete
    event archive and derived atlas with versioned descriptor definitions.
  instrument_ready: false
  regime: existing Python plus the validated LP; no Rust required
  instance: {axis: n, point: 8}
  sweep: {axis: n, points: [5, 6, 7, 8, 9, 10]}
  priority: 1
  cost_estimate: tier S (1e9 pair-tests)
  prereqs: [H-002, H-021, H-023]
  replication: true
  registered: retroactive
  notes: >-
    Gates the atlas, which the search-philosophy report argues is the campaign's real
    deliverable. A visual plateau is not an accept rule: preregister an unseen-mass
    estimator, interval, and replicate policy. Kill: the upper confidence bound on
    unseen mass remains above threshold by n = 8 within tier S - enumeration will not
    scale to 11, and the fallback is coverage estimation over descriptor space (H-007).
---
# H-011 — testing whether a declared landscape view is censusable

A numerical quench endpoint does not automatically become a discrete local minimum when
its key is canonicalized.
At `n=3`, an exact side-2 family contains a continuously sliding square; the current
geometric key splits that connected family, interior members share one contact key, and
the wall endpoints have a second contact key.
The census is therefore blocked on a declared terminal-component relation, isolation
tests, and an ambiguity policy as well as on canonical endpoint comparison.

Once proposer `P`, quench `Q`, and terminal equivalence `E` are versioned, the countable
question is conditional: how much component support under this regime has the sample
covered, with what uncertainty?
That can be answered by an event archive, an unseen-mass estimator, and independent
replicates; a flat key-discovery curve alone cannot establish completeness.

The census starts where the answers are proved, so the atlas machinery is validated
against ground truth before it is pointed at `n = 11`.

This is the cheapest strategic item in the registry: it runs on the existing Python plus
the LP that the standing review already validated, so it needs no Rust and no new
engine.
