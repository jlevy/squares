---
title: H-039 — can the n=12 lower bound be improved or closed?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-039
  kind: open_question
  claim: >-
    Can a checked extension of Stromquist's conditional forcing or another certified
    resource system improve the standing lower bound for s(12), ultimately proving the
    conjectured equality s(12) = 4?
  lane: proof
  derived_from: [X-002]
  strategy_refs: ['proof:2', 'proof:3', 'proof:6', 'proof:7', 'proof:15']
  instrument: >-
    First pass H-010's source-faithful known-answer reconstruction. Then use
    counterexample-guided synthesis over explicit points, segments, threshold resources,
    and moving families: every candidate certificate faces a continuous escaping-pose
    falsifier before interval or symbolic proof, and every failure retains the escaping
    pose and failed implication.
  instrument_ready: false
  regime: twelve unit squares in every container side below a declared proof threshold
  instance: {axis: n, point: 12}
  priority: 1
  cost_estimate: tier S per falsifier candidate; agent-days to weeks for a certified improvement
  prereqs: [H-010]
  replication: true
  registered: '2026-08-24'
  notes: >-
    The first promoted claim must fix a numeric lower-bound threshold before synthesis;
    this open question does not let the threshold move after counterexamples. Proving
    4 is the ultimate target, but any independently checked improvement is a durable
    result.
---
# H-039 — put the central exact-value problem in the registry

The proof generator is useful only if it returns either a replayable certificate or a
counterconfiguration tied to a named forcing step.
Search saturation is never a proof of unavoidability.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
