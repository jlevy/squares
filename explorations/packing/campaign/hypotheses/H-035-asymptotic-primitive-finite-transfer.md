---
title: H-035 — asymptotic construction primitives transfer to a finite record
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-035
  kind: hypothesis
  claim: >-
    A finite, independently and formally verified instantiation of the stack, strip, or
    near-rectangular-quadrilateral primitives from the 2025-2026 O(x^(3/5)) work improves
    at least one preregistered public parent at 100 <= n <= 324 by at least 1e-5.
  lane: search
  derived_from: [X-002]
  strategy_refs: ['search:4', 'search:8', 'search:9']
  criterion:
    shape: record
    metric: independently and formally verified reduction from a preregistered public parent side
    direction: below parent by at least 1e-5 on one target
    threshold: 0.00001
  instrument: >-
    Encode the published primitives with their integer synchronization parameters,
    reproduce one paper figure or asymptotic estimate, freeze a finite target list from
    the extended corpus, optimize parameters, and certify every candidate with outward-rounded
    intervals or exact arithmetic.
  instrument_ready: false
  regime: formally verified public parents at 100 <= n <= 324; finite construction claim only
  instance: {axis: n, point: 100-to-324}
  priority: 3
  cost_estimate: agent-tier constructor; tier S per finite parameter family before any broad sweep
  prereqs: [verified frontier corpus beyond n = 100]
  replication: true
  registered: '2026-08-24'
  notes: >-
    A finite improvement does not improve the asymptotic exponent. A null result can
    still identify which boundary overhead prevents current asymptotic primitives from
    helping at catalogue scale.
---
# H-035 — connect the active asymptotic literature to explicit finite geometry

This lane is independent of basin identity.
Its event is a valid construction, and its negative evidence is a parameterized
finite-overhead curve.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
