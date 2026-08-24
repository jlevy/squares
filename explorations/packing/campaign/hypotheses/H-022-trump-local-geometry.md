---
title: H-022 — what is the certified local geometry of Trump's packing?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-022
  kind: open_question
  claim: >-
    Is Trump's n = 11 packing isolated and locally optimal modulo D4 and relabelling,
    under the complete active inequality system rather than contact counting alone?
  lane: proof
  derived_from: [X-001]
  strategy_refs: ['proof:20', 'proof:21']
  instrument: >-
    Active-constraint Jacobian and feasible tangent analysis followed by interval-local
    exclusion or an explicit feasible continuation witness.
  instrument_ready: false
  regime: exact algebraic reference packing with all containment and non-overlap inequalities
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: analytic rank screen, then a separately budgeted interval neighborhood proof
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    Either answer matters. Isolation would justify a point-like local model; a feasible
    optimal family would change component identity and the interpretation of attraction
    measurements. Neither answer follows from the 14 exact contacts already verified.
---
# H-022 — certify the local object before using it as a landmark

Trump’s construction is a strong rigidity candidate, but this repository currently has
no active-system rank or interval-local certificate.
The question is registered because several strategy claims refer to its basin or
component as though its local geometry were settled.

The first deliverable is a complete constraint matrix and tangent calculation.
It is a screen, not the final certificate: inequality directions and higher-order
obstruction still have to be handled.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
