---
title: H-034 — fractional piercing rules out ten pure points at Trump's side
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-034
  kind: hypothesis
  claim: >-
    For the family U_s of all open unit-square poses contained in a square at Trump's
    published side s, the continuous fractional piercing value tau-star(U_s) is strictly
    greater than 10.
  lane: proof
  derived_from: [X-002]
  strategy_refs: ['proof:17', 'proof:21', 'proof:22']
  criterion:
    shape: determination
    metric: certified lower bound on the continuous fractional piercing value at s = 3.877083590022814...
    direction: strictly above 10
    threshold: 10
  instrument: >-
    Primal-dual column generation over point mass and square-pose mass, with separate
    restricted-point and restricted-pose discretizations and interval bounds that cover
    every omitted continuous point and pose.
  instrument_ready: false
  regime: pure point piercing only; open-pose limiting convention fixed; no threshold or moving-resource certificates
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: tier S coarse two-sided pilot; resolution ladder only if bounds narrow monotonically
  prereqs: [continuous pose falsifier, certified discretization bounds]
  replication: true
  registered: '2026-08-24'
  notes: >-
    A value above 10 rules out an integral ten-point unavoidable set. A value at most 10
    does not produce one because the integrality gap may be positive. Bašić-Slivkova is
    the direct integral-piercing precedent; the fractional continuous decision is new
    only relative to the retrieved corpus.
---
# H-034 — a one-sided decision experiment for a proof-method ceiling

The pure-point method is only one part of Stromquist’s and Bentz’s proof language.
A confirmed ceiling would not rule out conditional forcing, weighted resources, or
moving families.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
