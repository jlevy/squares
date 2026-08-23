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
    LP-quenching multistarts at n <= 10 yields a basin count that saturates: the
    discovery curve plateaus within tier-S budget, giving a near-complete atlas with
    canonical identities and exact side lengths.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:12', 'search:18']
  criterion:
    shape: determination
    metric: does the basin discovery curve plateau by n = 8 within tier S
    direction: plateau reached
  instrument: >-
    Not yet built. Multistart proposer + LP quench (H-002) + canonical dedup (R-1 keys),
    emitting the atlas as a soft-schema artifact with versioned descriptor definitions.
  instrument_ready: false
  regime: existing Python plus the validated LP; no Rust required
  instance: {axis: n, point: 8}
  sweep: {axis: n, points: [5, 6, 7, 8, 9, 10]}
  priority: 1
  cost_estimate: tier S (1e9 pair-tests)
  prereqs: [H-002]
  replication: false
  registered: retroactive
  notes: >-
    Gates the atlas, which the search-philosophy report argues is the campaign's real
    deliverable. Kill: no plateau by n = 8 within tier S - enumeration will not scale to
    11, and the fallback is coverage estimation over descriptor space (H-007).
---
# H-011 — making the landscape countable

A local minimum stops being “a tolerance-dependent place where an annealer got tired”
once the quench endpoint is exact and the identity is canonical.
It becomes a discrete, nameable, exactly-valued object — and then “how many are there”
is a census question, which is a question a program can be *finished* with.

The census starts where the answers are proved, so the atlas machinery is validated
against ground truth before it is pointed at `n = 11`.

This is the cheapest strategic item in the registry: it runs on the existing Python plus
the LP that the standing review already validated, so it needs no Rust and no new
engine.
