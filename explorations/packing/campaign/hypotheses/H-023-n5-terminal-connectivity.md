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
    unequal-side candidates. Exp-033 proves the equal-side pair shares one exact
    fixed-angle LP optimal face with endpoint/interior nullities 0/1/0. Exp-034 then
    proves that face lies in an exact two-parameter angle-and-slide sheet of optima.
    Exp-035 then proves that the complete branchwise first-order systems at both
    endpoints and one interior point admit an exact direction outside that sheet. These
    are partial results, not a complete answer: nonlinear realization, the full
    nonsmooth stationary component, and the unequal-side clearance questions remain
    open.
---
# H-023 — resolve the first ambiguous census cell

The `n = 5` sample is the earliest place where endpoint keys, matching side/contact
summaries, and geometric interpretation disagree.
It contains no observed optimum and therefore cannot be described as six points in one
optimum-side family.
Calling it either a rich landscape or one flat family before continuation would repeat
the same soundness error in opposite directions.

## Two exact slices

Exp-033 aligns the two equal-side source poses after one declared D4 action and
relabelling. Four squares coincide, and the fifth traverses an exact segment at constant
side and fixed angles.
Exact endpoint validity, a common separating cell, an exact LP dual, and fixed-side
nullities `0/1/0` prove that the two different geometric keys lie in one connected
fixed-angle optimal face.

This removes key inequality as evidence of separation for this pair.
Exp-034 goes further: for `t = tan(theta_0/2)` with `|t| <= 1/100`, it certifies every
slide parameter in the exact strip `e(t) <= u <= 3sqrt(2)/2 - 2 - e(t)`, where
`e(t) = |t|(1 - |t|)/(1 + t^2)`. The same exact dual proves the resulting two-parameter
sheet optimal because its support avoids the moving square.

This still does not identify the full stationary component.
Exp-035 derives the complete active first-order rows at both endpoints and one interior
point. Both owner-axis branches admit the same exact non-sheet direction, with both tied
support rows enforced, but no nonlinear continuation has yet realized it.
Certified continuation and deterministic quench selection have not been established.
The unequal-side rows still require minimax-clearance bounds.

This is the focused control for H-021 and the practical precursor to H-011.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
