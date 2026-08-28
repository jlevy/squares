---
title: H-004 — neighbor-transfer seeding improves n = 11 search
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-004
  kind: hypothesis
  claim: >-
    At n = 11, seeds constructed by adding a square to the proved n = 10 packing or
    removing one from the standing n = 12 grid produce a median best side at least 0.01
    lower than paired cold starts at equal pair-test budget.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:20', 'search:12']
  criterion:
    shape: paired
    metric: paired difference in best side after the fixed pair-test budget
    direction: neighbor-transfer median at least 0.01 lower than cold-start median
    threshold: 0.01
  instrument: >-
    Not yet built. Add-one-in-largest-gap and remove-one-and-straighten proposers over
    versioned n = 10 and n = 12 source packings, with the common quench and verifier.
  instrument_ready: false
  regime: n = 11; identical seed blocks, pair-test budgets, quench, and verification
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [11]}
  priority: 2
  cost_estimate: tier S (1e9 pair-tests)
  prereqs: [H-002]
  replication: true
  registered: retroactive
  notes: >-
    Kill if the paired median improvement is below 0.01. The standing review's original
    n = 12 test targeted side 4 + epsilon, but a cold grid already starts at side 4, so
    that criterion was vacuous and is not carried into the registry.
---
# H-004 — transfer information across neighboring values of n

Human record tables often advance by adding or removing a square from a nearby
construction. This turns that practice into a controlled proposer comparison at a cell
where the target is cheap to recognize.

The target is deliberately an equal-budget improvement at the open `n = 11` cell.
Reaching or missing Trump’s standing upper bound is reported separately; it is not
needed to decide whether transfer is a useful proposer.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
