---
title: H-024 — formally supported small-n records use at most three angle classes
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-024
  kind: hypothesis
  claim: >-
    Every formally supported standing-record packing at n <= 30 uses at most three
    square-orientation classes modulo quarter turns under a preregistered angle equality
    rule.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:2', 'search:6']
  criterion:
    shape: determination
    metric: maximum formally supported orientation-class count over the declared corpus
    direction: at most 3
    threshold: 3
  instrument: >-
    A formal witness verifier must first establish feasibility;
    cases.kingbird29.verify_svg can then reconstruct the retained source and screen its
    quarter-turn classes numerically.
  instrument_ready: false
  regime: all n <= 30 with formally supported standing-record geometry; missing cases reported
  instance: {axis: n, point: 29}
  sweep: {axis: n, points: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}
  priority: 1
  cost_estimate: verify the primary n = 29 SVG first; stop the corpus tranche if it refutes the bound
  prereqs: [a formal certificate for the candidate record geometry]
  replication: true
  registered: '2026-08-24'
  notes: >-
    Exp-012 reconstructed and numerically checked the primary n = 29 SVG: its five
    distinct nonzero angle entities plus the axis-aligned class give six well-separated
    numerical classes. The public serialization lacks a formal feasibility certificate,
    so the original claim remains unresolved. H-042 owns the precisely numerical
    successor; H-025 asks about effective angular compressibility.
---
# H-024 — separate the corpus law from the search algorithm

The original H-001 joined two propositions: record packings appear to use few angles,
and restricting a search to a few angle classes should improve it.
One can fail while the other holds.
This artifact owns only the descriptive corpus statement.

The equality rule is part of the measurement.
Numerically close orientations remain an ambiguity unless their representation or
interval evidence resolves them.

**Unresolved, 2026-08-25.**
[Exp-012](../series/series-000-smoke-and-calibration/experiments/exp-012-h-024-n29-angle-classes.md)
reconstructs the primary Kingbird `n = 29` SVG and numerically checks all 29 squares and
406 pairs at 160 decimal digits and tolerance `1e-80`. Its orientations are aligned,
`a = 25.258655°`, `b = 20.800127°`, `−c = −17.506268°`, `d = 24.962588°`, and
`i = 24.308358°`. The six intervals are disjoint by a minimum of `0.296067°`, so the
serialized numerical geometry misses the upper bound of three without a clustering
ambiguity. But this is not a formal feasibility certificate for the source geometry.
It therefore does not satisfy this hypothesis’s prerequisite.

[H-042](H-042-n29-numerical-angle-classes.md) preserves the useful numerical claim
without weakening the meaning of formal support.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
