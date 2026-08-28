---
title: H-008 — float-refined endpoints have a measurable exact-rejection rate
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-008
  kind: hypothesis
  claim: >-
    Under the declared search and refinement pipeline, the rate at which endpoints
    accepted by the floating-point screen are rejected by an independent stronger
    verifier can be estimated with retained witnesses and uncertainty at each tested n.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:17', 'search:19']
  criterion:
    shape: determination
    metric: per-n exact-rejection count, rate, and confidence interval among float-accepted endpoints
    direction: determine the rate without assuming it is positive or monotone
  instrument: >-
    Not yet complete. Retain every float-accepted endpoint from the event archive and
    batch it through an independently implemented interval or exact verification path.
  instrument_ready: false
  regime: checker version, arithmetic method, actual precision, and tolerance recorded per endpoint
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 6, 7, 8, 9, 10, 11, 12, 17]}
  priority: 1
  cost_estimate: marginal counter plus the cost of stronger verification
  prereqs: []
  replication: true
  registered: retroactive
  notes: >-
    The original directional wording is not used as the accept rule: zero is a valid
    measurement. Increasing with n is exploratory until enough cells exist to register a
    separate trend claim. Failures remain artifacts with witnesses rather than counts only.
---
# H-008 — measure the soundness perimeter on real outputs

Constructed negative controls prove that the stronger verifier can reject known bad
packings.
This hypothesis asks how often that distinction matters on the distribution the
search actually produces.

The endpoint archive is essential: a scalar rate without rejected witnesses cannot
diagnose whether the problem is search tolerance, refinement, serialization, or the
stronger verifier itself.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
