---
title: H-102 — which complete restricted angle and support families admit exclusion?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-102
  kind: open_question
  claim: >-
    Which explicitly delimited n = 11 angle-composition or wall-support families admit
    a complete exclusion theorem below a declared side, and which such families admit
    a verified counterexample instead?
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  instrument: >-
    Select a finite family and side before a run. Use complete disjunctive containment
    and separation cases, exact fixed-angle center LP/Farkas certificates or rigorous
    interval bounds over angle boxes, with an independent feasible-witness falsifier.
    No general complete-family producer and verifier exists.
  instrument_ready: false
  regime: >-
    n = 11; only the angle and support family stated in the concrete hypothesis;
    every covered center, angle, wall, and degeneracy case retains its original scope
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: first reuse H-036's bounded falsifier and price one complete proof family
  prereqs: [prospectively fixed family and threshold, checked feasible control for the chosen branch]
  replication: true
  registered: '2026-09-06'
  notes: >-
    H-036 already supplies the first concrete proof target and independent falsifier:
    every folded angle within 0.25 degrees of 0 or 45 implies side at least 3.878.
    Keep that claim and its threshold unchanged. A new family or radius needs its own
    prospective claim. Partial case closure and solver timeout leave a family unresolved.
---
# H-102 — A Restricted Theorem Before a Global Enumeration

Use [H-036](H-036-robust-restricted-orientation.md) for the first theorem attempt and
the adversarial packing search.
A rigorously feasible witness within its angle regime and below 3.878 refutes that
claim; an unsuccessful search is not proof.
No additional hypothesis is needed merely to run its independent falsifier.

A fixed-angle LP closes only its declared separation branch.
Angle intervals require bounds valid throughout each box, and a family theorem requires
every disjunction, boundary, and degeneracy case covered.
A wall-support signature must identify the square, supporting feature, wall, and any
angle or order restrictions; an incomplete signature catalogue remains a restricted
result.
[H-063’s refuted two-threshold language](H-063-n11-class-certificate.md) does not
refute richer families, but cannot be revived by renaming it.

[Agenda 026](../agendas/agenda-026-density-stationarity-and-trump-capture.md) routes
these structural precursors through think-dene and the paired falsifier through
think-pjk7. BC-246/247 can supply reusable controls and branch prices; a self-contained
restricted lemma need not await a full typed producer, density construction, or global
atlas. This implements
[X-016’s distinction between proof layers](../explorations/X-016-after-381-two-managers-one-proof-boundary.md#proof-layers-and-fractional-objects).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
