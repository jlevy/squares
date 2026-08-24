---
title: H-010 — the Stromquist falsifier triple reproduces
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-010
  kind: hypothesis
  claim: >-
    The continuous falsifier finds the known stage-one escape from the 10-point
    Stromquist candidate, finds no escape from the 12-point candidate within its declared
    search budget, and a later interval PoseBox procedure proves the 12-point candidate
    unavoidable.
  lane: proof
  derived_from: [X-001]
  strategy_refs: ['proof:2', 'proof:3', 'proof:15']
  criterion:
    shape: conditions
    metric: ordered outcomes of the 10-point falsifier, 12-point falsifier, and PoseBox certificate checker
    direction: escape, saturated-within-budget, then independently checked unavoidable certificate
  instrument: >-
    Not yet built. A continuous escape falsifier for the first two legs and a
    certificate-producing interval PoseBox subdivision for the proof leg.
  instrument_ready: false
  regime: published point sets transcribed with provenance; exact geometry at certificate checking
  instance: {axis: n, point: 12}
  sweep: {axis: n, points: [10, 12]}
  priority: 2
  cost_estimate: tier S falsifier checks; proof leg separately budgeted
  prereqs: []
  replication: true
  registered: retroactive
  notes: >-
    This is a known-answer machinery test. Failure on the 10-point escape is a tool bug;
    failure to find a 12-point escape is only a censored search result until the
    independent PoseBox certificate is produced and checked.
---
# H-010 — a three-stage proof-lane calibration

The first two legs test whether the falsifier distinguishes a known escape from a hard
candidate. Only the third leg can establish unavoidability.
Keeping the stages separate prevents search saturation from being narrated as proof.

The source transcription and the final certificate need independent checks because a
faithfully executed experiment on the wrong point set answers nothing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
