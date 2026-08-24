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
  instance: {axis: n, point: 29}
  sweep: {axis: n, points: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}
  priority: 1
  cost_estimate: verify the primary n = 29 SVG first; stop the corpus tranche if it refutes the bound
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    The primary n = 29 SVG contains five distinct nonzero angle entities plus the
    axis-aligned class, making it a direct counterexample candidate. Independently
    reconstruct and verify that one packing before importing the rest of n <= 30.
    Missing or picture-only cases do not count as confirmations. Refutation of this
    descriptive corpus claim does not refute H-001's algorithmic comparison; its useful
    successor asks about effective angular rank or compressibility rather than raw class
    count.
---
# H-024 — separate the corpus law from the search algorithm

The original H-001 joined two propositions: record packings appear to use few angles,
and restricting a search to a few angle classes should improve it.
One can fail while the other holds.
This artifact owns only the descriptive corpus statement.

The equality rule is part of the measurement.
Numerically close orientations remain an ambiguity unless their representation or
interval evidence resolves them.

**Counterexample candidate, 2026-08-24.** The primary Kingbird `n = 29` SVG declares
nonzero orientations `25.258655°`, `20.800127°`, `17.506268°`, `24.962588°`, and
`24.308358°`, in addition to axis-aligned squares.
If the imported pose passes the independent verifier, six classes determine this
hypothesis immediately.
Do that one-cell check before a full corpus sweep.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
