---
title: H-042 — the retained n = 29 serialization has at most three numerical angle classes
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-042
  kind: hypothesis
  claim: >-
    The retained Kingbird n = 29 SVG serialization has at most three orientation classes
    modulo quarter turns when reconstructed at 160 decimal digits, with pair and container
    zero tolerance 1e-80 and angle-interval radius 1e-90 degrees.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:2', 'search:6']
  criterion:
    shape: determination
    metric: numerical orientation-class count in the retained n = 29 serialization
    direction: at most 3
    threshold: 3
  instrument: >-
    cases.kingbird29.verify_svg reconstructs every serialized square, numerically checks
    all containment and pair constraints, replays the source equations, and counts
    quarter-turn classes under the declared intervals.
  instrument_ready: true
  regime: >-
    retained Kingbird square-29.svg; 160 decimal digits; 1e-80 pair/container zero
    tolerance; 1e-90 degree angle-interval radius
  instance: {axis: n, point: 29}
  sweep: {axis: n, points: [29]}
  priority: 1
  cost_estimate: one deterministic source replay under one second
  prereqs: []
  replication: true
  registered: '2026-08-25'
  notes: >-
    This successor deliberately asks only about the numerical serialization. It does not
    claim that the source geometry is formally feasible, record-setting, or optimal.
---
# H-042 — a numerical claim with numerical prerequisites

This is the narrow claim that exp-012’s arithmetic could actually decide.
It keeps the method, precision, tolerance, and source serialization in the statement, so
rejection cannot be mistaken for a formal result about an exact packing.

[Exp-037](../series/series-000-smoke-and-calibration/experiments/exp-037-h-042-n29-numerical-angle-classes.md)
numerically rejects the three-class bound: the retained serialization has six
well-separated classes under the declared rules.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
