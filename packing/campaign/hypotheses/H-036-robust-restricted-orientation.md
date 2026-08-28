---
title: H-036 — Stromquist's restricted-orientation gap survives a neighborhood
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-036
  kind: hypothesis
  claim: >-
    If every n = 11 square orientation modulo quarter turns lies within 0.25 degrees of
    either 0 or 45 degrees, then the containing side is at least 3.878.
  lane: proof
  derived_from: [X-002]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  criterion:
    shape: determination
    metric: certified lower bound over the declared restricted-orientation configuration space
    direction: at least 3.878
    threshold: 3.878
  instrument: >-
    First reproduce Stromquist's exact 0/45-degree lower bound. Then run interval branch
    and bound over centers and the two angle neighborhoods, using unavoidable-set and
    containment cuts, while an independent search tries to falsify the 3.878 threshold.
  instrument_ready: false
  regime: n = 11; every folded angle within 0.25 degrees of 0 or 45 degrees
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: tier S numerical falsifier; certified proof is an hour-to-day ladder
  prereqs: [checked Stromquist restricted-orientation control, interval PoseBox]
  replication: true
  registered: '2026-08-24'
  notes: >-
    Stromquist proves the exact 0/45-degree optimum is about 3.8856. This claim asks for
    a much weaker but robust neighborhood statement above Trump's side. A valid packing
    below 3.878 refutes it immediately.
---
# H-036 — a structural theorem between one slice and the full problem

The threshold and angle radius are fixed before computation.
If refuted, retain the pose and shrink the radius only in a newly registered claim
rather than moving the goal.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
