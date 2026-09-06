---
title: H-095 — adaptive cores certify side 61/16 for n = 11
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-095
  kind: hypothesis
  claim: >-
    At container side 61/16, the BC-230 adaptive-core language admits a finite
    D4-invariant measure of nonnegative rational point atoms with total mass below
    eleven, nonconstant rational core sides B_k, and mass at least one in every
    admissible core at every declared net direction.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:21', 'proof:22']
  criterion:
    shape: determination
    metric: exact adaptive-core certificate at side 61/16
    direction: >-
      Accept only if the project sweep, interval route and source-distinct
      standalone verifier all accept the same certificate under BC-230's
      legacy-linear-v1 contract, with complete angle-cell coverage, safe
      containment, D4 invariance, nonconstant core sides and total mass below
      eleven. Incomplete verification or a failed search leaves the claim unresolved.
    threshold: exact adaptive certificate at side 61/16 with total mass below eleven
  instrument: >-
    BC-231's planned adaptive project sweep, interval route and standalone verifier,
    followed by BC-234 synthesis and BC-238 independent candidate review.
  instrument_ready: false
  regime: >-
    n = 11; side 61/16; exact rational atoms, weights and BC-230 angle-cell data;
    legacy-linear-v1 containment. The synthesis rule is frozen before measurement.
  instance: {axis: side, point: '61/16'}
  prereqs: [reviewed BC-230 contract, all BC-231 routes and controls accepted]
  registered: '2026-09-06'
---
# H-095 — Adaptive Cores at 61/16

The
[BC-230 contract](../series/series-000-smoke-and-calibration/results/agenda-025/bc-230-adaptive-core-contract.md)
proves the containment and counting implication.
The
[contributed strategy, B1](../../../docs/project/reviews/review-2026-09-05-strategy-gpt-56-pro-gemini-grok.md)
motivates using each angle cell’s mismatch instead of one global shrink.
BC-231 implementation and controls remain prerequisites for a target run.

BC-234’s 25-percent reduction of same-support excess is a routing test, not acceptance
of this certificate-existence claim.
A matched comparison needs its own frozen scalar control, support and synthesis rule.
A successful adaptive certificate alone does not establish an advantage over H-093.

Stop variant synthesis when a candidate requires independent verification.
If H-093 already certifies this side, reassess the value of running this target before
spending more work; retain H-095’s side and criterion unchanged.
Exact basis recovery may support a candidate, while a new side or containment contract
requires a separate prospective claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
