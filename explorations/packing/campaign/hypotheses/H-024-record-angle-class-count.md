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
    cases.kingbird29.verify_svg imports the retained primary SVG, reconstructs every
    square, replays its source equations, independently checks all pairs with
    sqpack.verify, and counts quarter-turn orientation classes under declared intervals.
  instrument_ready: true
  regime: all n <= 30 with retained, independently verified record geometry; missing cases reported
  instance: {axis: n, point: 29}
  sweep: {axis: n, points: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}
  priority: 1
  cost_estimate: verify the primary n = 29 SVG first; stop the corpus tranche if it refutes the bound
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    Exp-012 reconstructed and numerically verified the primary n = 29 SVG: its five
    distinct nonzero angle entities plus the axis-aligned class give six unambiguous
    classes and refute this universal claim at the preregistered stop cell. Refutation
    of this descriptive corpus claim does not refute H-001's algorithmic comparison;
    H-025 asks the useful successor question about effective angular compressibility.
---
# H-024 — separate the corpus law from the search algorithm

The original H-001 joined two propositions: record packings appear to use few angles,
and restricting a search to a few angle classes should improve it.
One can fail while the other holds.
This artifact owns only the descriptive corpus statement.

The equality rule is part of the measurement.
Numerically close orientations remain an ambiguity unless their representation or
interval evidence resolves them.

**Refuted, 2026-08-24.**
[Exp-012](../series/series-000-smoke-and-calibration/experiments/exp-012-h-024-n29-angle-classes.md)
reconstructs the primary Kingbird `n = 29` SVG and checks all 29 squares and 406 pairs
at 160 decimal digits.
Its orientations are aligned, `a = 25.258655°`, `b = 20.800127°`, `−c = −17.506268°`,
`d = 24.962588°`, and `i = 24.308358°`. The six intervals are disjoint by a minimum of
`0.296067°`, so the result misses the registered upper bound of three without a
clustering ambiguity.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
