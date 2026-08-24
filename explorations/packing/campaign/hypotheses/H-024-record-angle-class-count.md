---
title: H-024 — verified small-n record packings use at most three angle classes
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-024
  kind: hypothesis
  claim: >-
    Every independently reconstructed standing-record packing at n <= 30 uses at most
    three square-orientation classes modulo quarter turns under a preregistered angle
    equality rule.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:2', 'search:6']
  criterion:
    shape: determination
    metric: maximum independently verified orientation-class count over the declared corpus
    direction: at most 3
    threshold: 3
  instrument: >-
    Not yet complete. Import full record geometry with provenance, independently verify
    each packing, and count quarter-turn orientation classes with exact values where
    available and ambiguity intervals otherwise.
  instrument_ready: false
  regime: all n <= 30 with retained, independently verified record geometry; missing cases reported
  instance: {axis: n, point: 30}
  sweep: {axis: n, points: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}
  priority: 2
  cost_estimate: geometry-import and verification effort; analysis is negligible
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    Missing or picture-only cases do not count as confirmations. Refutation of this
    descriptive corpus claim does not refute H-001's algorithmic comparison, and
    confirmation does not show that an angle-class proposer can discover the classes.
---
# H-024 — separate the corpus law from the search algorithm

The original H-001 joined two propositions: record packings appear to use few angles,
and restricting a search to a few angle classes should improve it.
One can fail while the other holds.
This artifact owns only the descriptive corpus statement.

The equality rule is part of the measurement.
Numerically close orientations remain an ambiguity unless their representation or
interval evidence resolves them.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
