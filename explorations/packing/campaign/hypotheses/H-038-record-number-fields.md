---
title: H-038 — which number fields and elimination mechanisms occur in record packings?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-038
  kind: open_question
  claim: >-
    Which algebraic number fields, minimal-polynomial degrees, Galois groups, and
    discriminant patterns occur in independently reconstructed record packings, and how
    are they determined by the active contact cell and angle-class mechanism?
  lane: proof
  derived_from: [X-002]
  strategy_refs: ['search:17', 'search:18', 'proof:15']
  instrument: >-
    Import and independently verify full witnesses before assigning algebraic metadata.
    Derive the exact polynomial system of each declared active cell, eliminate to the
    side and angle variables, factor over the rationals, and compute field invariants
    with replayable computer-algebra receipts. Never inherit a polynomial from a
    superseded side row.
  instrument_ready: false
  regime: independently reconstructed algebraic record witnesses with active-cell certificates
  instance: {axis: corpus, point: verified-algebraic-records}
  priority: 2
  cost_estimate: tier S for one known-answer field; agent-days for a checked corpus table
  prereqs: [verified geometry corpus, exact active-cell extraction]
  replication: true
  registered: '2026-08-24'
  notes: >-
    Degree is a descriptor and theorem target, not a ceiling on unavoidable-point
    proofs. The 2026 n=69 witness does not inherit the degree-82 polynomial of the
    superseded parent. A useful result may be a mechanism-conditioned taxonomy even if
    no simple degree law survives.
---
# H-038 — let the exact witness choose its field

This lane asks what the algebra is after the geometry is fixed and verified.
It does not infer a construction from a decimal side value or use algebraic degree as a
proxy for rigidity. A failed simple pattern is retained as a counterexample to the
proposed taxonomy.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
