---
title: H-010 — the Stromquist conditional-forcing argument reproduces
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-010
  kind: hypothesis
  claim: >-
    A checked computational reconstruction reproduces Stromquist's complete Theorem 2
    mechanism: avoiding the initial 10 points localizes a unit square to the declared
    top or bottom exceptional region; the relevant lemmas force that same square to
    contain all three A-points; and nine further points complete the counting
    contradiction for 11 packed squares.
  lane: proof
  derived_from: [X-001]
  strategy_refs: ['proof:2', 'proof:3', 'proof:15']
  criterion:
    shape: conditions
    metric: independently checked localization, forced-triple cohabitation, and final counting implications
    direction: every implication and its boundary cases reproduce the published proof
  instrument: >-
    Not yet built. A source-faithful point-set transcription, continuous escape
    falsifier, and certificate-producing interval subdivision for each localization and
    cohabitation implication.
  instrument_ready: false
  regime: published point sets transcribed with provenance; exact geometry at certificate checking
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [11]}
  priority: 2
  cost_estimate: tier S falsifier checks; proof leg separately budgeted
  prereqs: []
  replication: true
  registered: retroactive
  notes: >-
    This is a known-answer machinery test of Stromquist's proof structure, not a claim
    that one standalone 12-point set is unavoidable. Ten points localize an avoiding
    square; three A-points are forced into that same square; nine further points then
    make the count work. A saturated numerical falsifier remains censored until the
    corresponding implication has an independently checked certificate.
---
# H-010 — a source-faithful proof-lane calibration

The original artifact compressed Stromquist’s proof into “10-point escape, 12-point
unavoidability.” That is not the published implication and would calibrate the tool on
the wrong object. The load-bearing structure is conditional: localization of an avoiding
square, forced cohabitation of three points in that same square, then a count using nine
more points.

Each implication needs a falsifier and an independently checkable certificate.
Keeping them separate prevents numerical search saturation from being narrated as the
theorem.

The source transcription and the final certificate need independent checks because a
faithfully executed experiment on the wrong point set answers nothing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
