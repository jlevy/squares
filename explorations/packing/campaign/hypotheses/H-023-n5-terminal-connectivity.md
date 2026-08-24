---
title: H-023 — how are the observed n = 5 endpoint candidates connected?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-023
  kind: open_question
  claim: >-
    Are the two observed n = 5 endpoint candidates at side 2.767766953 connected within
    the declared stationary set at that side; and what verified minimax side-clearance
    bounds connect the unequal-side endpoint candidates?
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:12', 'search:18']
  instrument: >-
    Retained poses, full active-system rank and feasible tangent analysis, followed by
    bidirectional continuation at fixed objective and independent validity checks.
  instrument_ready: false
  regime: >-
    six observed non-optimal n = 5 endpoint candidates; no identity conclusion from
    side/contact summaries alone
  instance: {axis: n, point: 5}
  priority: 1
  cost_estimate: focused local geometry experiment before the n <= 10 census
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    The retained summary says found_optimum false: all six sides exceed the proved
    2.70710678 optimum and only the first two share a side. A feasible path need not be
    a path in the terminal set. This question therefore separates same-level terminal
    connectivity for that pair from the weaker clearance-connectivity question for
    unequal-side candidates. Exp-033 preregisters a narrower first test: whether the
    equal-side pair shares one exact fixed-angle LP optimal face. Acceptance would be
    partial evidence, not a complete answer to this hypothesis.
---
# H-023 — resolve the first ambiguous census cell

The `n = 5` sample is the earliest place where endpoint keys, matching side/contact
summaries, and geometric interpretation disagree.
It contains no observed optimum and therefore cannot be described as six points in one
optimum-side family.
Calling it either a rich landscape or one flat family before continuation would repeat
the same soundness error in opposite directions.

This is the focused control for H-021 and the practical precursor to H-011.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
