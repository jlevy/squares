---
title: H-014 — superdisk continuation imports useful circle-packing structure
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-014
  kind: hypothesis
  claim: >-
    Continuation from circles through a preregistered superdisk-exponent ladder produces
    square-limit endpoints at n <= 10 that occupy terminal components not reached by an
    equal-budget direct square proposer.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:8', 'search:13']
  criterion:
    shape: paired
    metric: distinct square terminal components unique to each proposer per pair-test
    direction: at least one independently verified component unique to superdisk continuation
  instrument: >-
    Not yet built. A superdisk geometry predicate and exponent-continuation proposer,
    ending in the common square quench, terminal-component relation, and verifier.
  instrument_ready: false
  regime: small-n ladder first; identical square-end budget and identity policy
  instance: {axis: n, point: 10}
  sweep: {axis: n, points: [5, 6, 7, 8, 9, 10]}
  priority: 4
  cost_estimate: tier M plus new non-square geometry
  prereqs: [H-011]
  replication: true
  registered: retroactive
  notes: >-
    Kill if square endpoints occupy only components already found by the direct proposer.
    This is deliberately last among search proposers because it alone requires a new
    geometry model before it can use the shared square spine.
---
# H-014 — test a geometry-changing continuation ladder

Circle packings have a much richer existing record literature.
A superdisk ladder asks whether that structure survives long enough to seed square
components that direct search misses, and where orientation symmetry breaks as the
geometry changes.

The comparison is at the square endpoint.
Intermediate superdisk configurations are mechanism evidence, not square-packing
results.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
