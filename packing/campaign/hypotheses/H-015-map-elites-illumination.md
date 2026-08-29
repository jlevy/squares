---
title: H-015 — MAP-Elites improves terminal-component discovery rate
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-015
  kind: hypothesis
  claim: >-
    A MAP-Elites proposer keyed by versioned tilt-class and contact-class descriptors
    discovers at least 1.5 times as many distinct terminal components per pair-test as
    temperature-matched restarts at n = 10 and n = 11.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:12', 'search:16']
  criterion:
    shape: paired
    metric: distinct independently verified terminal components per pair-test
    direction: MAP-Elites divided by paired restarts is at least 1.5 at both cells
    threshold: 1.5
  instrument: >-
    Not yet built. A MAP-Elites archive over calibrated, versioned descriptors using the
    common proposer/quench/component/verifier spine and a pair-test-matched restart arm.
  instrument_ready: false
  regime: n = 10 and 11; same move set, polish, identity relation, and seed blocks
  instance: {axis: n, point: 10}
  sweep: {axis: n, points: [10, 11]}
  priority: 2
  cost_estimate: tier M (1e11 pair-tests)
  prereqs: [H-011]
  replication: true
  registered: retroactive
  notes: >-
    Kill as a steering method if the 1.5x threshold is missed. The descriptor grid and
    negative result remain useful atlas diagnostics. Descriptor definitions are frozen
    before the comparison so the grid cannot be retuned to the observed archive.
---
# H-015 — retain diversity instead of only the current best

A search that retains only low side length can repeatedly sample one broad funnel.
Illumination tests whether preserving mechanism diversity finds more terminal components
for the same budget.

Single scalar descriptors are easy to game: a grid can maximize contact count without
representing the rare oblique mechanisms of interest.
The paired descriptor definition is therefore part of the registered regime and must be
calibrated before the run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
