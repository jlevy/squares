---
title: H-040 — active-cell neighbor walks discover structure efficiently
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-040
  kind: hypothesis
  claim: >-
    After a known-answer n = 5 control, pivoting across one active separating or wall
    feature at a time discovers at least twice as many new independently verified
    canonical active cells per LP solve as matched random-coordinate multistart at n = 10.
  lane: search
  derived_from: [X-002]
  strategy_refs: ['search:15', 'search:17', 'search:18']
  criterion:
    shape: paired
    metric: new independently verified canonical active cells per LP solve
    direction: neighbor walk at least two times matched multistart
    threshold: 2
  instrument: >-
    Define a complete active-cell signature, enumerate one-feature pivots from each
    retained cell, solve and independently verify the neighboring cell, and compare
    paired budgets with random-coordinate proposals. Report invalid pivots, duplicates,
    side distribution, and cell-signature sensitivity separately from terminal-component
    counts.
  instrument_ready: false
  regime: n = 5 known-answer control before n = 10; equal LP-solve budget and common verifier
  instance: {axis: n, point: 5}
  sweep: {axis: n, points: [5, 10]}
  priority: 2
  cost_estimate: tier S after complete active-cell extraction and canonicalization
  prereqs: [complete active-cell signature, canonical attribute regression]
  replication: true
  registered: '2026-08-24'
  notes: >-
    A new cell is not automatically a new terminal component or basin. The paired metric
    tests combinatorial exploration efficiency only; topology and attraction remain
    separate layers.
---
# H-040 — walk the piecewise-linear adjacency graph

The fixed-angle problem is partitioned into LP cells.
If neighboring cells can be generated cheaply, search can spend solves on structural
boundaries instead of drawing the same cell repeatedly.
Failure parks the enumerative proposer without weakening the atlas ontology.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
