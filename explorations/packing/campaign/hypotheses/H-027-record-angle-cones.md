---
title: H-027 — published record cells have positive class-angle cones
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-027
  kind: hypothesis
  claim: >-
    In the imported reference contact cells at n = 11 and n = 17, the minimum one-sided
    directional derivative of the reoptimized side over unit independent class-angle
    directions is at least 1e-4 side units per radian.
  lane: search
  derived_from: [X-002]
  strategy_refs: ['search:15', 'search:17', 'search:18']
  criterion:
    shape: conditions
    metric: certified or interval-bounded minimum directional derivative of the local cell-value model
    direction: at least 1e-4 on both cells
    threshold: 0.0001
  instrument: >-
    Import each reference cell, enumerate locally competing LP bases, build its
    piecewise first-order class-angle value model, and minimize the directional
    derivative over the quotient unit sphere. Retain any zero or negative direction.
  instrument_ready: false
  regime: published n = 11 and n = 17 record cells; class assignments fixed
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [11, 17]}
  priority: 2
  cost_estimate: tier S after n = 17 pose import; interval refinement only if the screen passes
  prereqs: [verified geometry corpus]
  replication: true
  registered: '2026-08-24'
  notes: >-
    H-019 measured one one-dimensional Trump slice. This hypothesis tests the full local
    class-angle cone and a two-oblique-angle prediction at n = 17. It is not a universal
    record law until a larger corpus is measured.
---
# H-027 — test the corner before naming a kink-codimension law

A zero derivative parks first-order tie-locus search and routes that direction to a
second-order analysis.
A positive result promotes active-basis continuation as a search mechanism.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
