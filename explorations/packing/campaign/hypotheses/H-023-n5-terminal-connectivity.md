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
    Exp-035 proves that the complete branchwise first-order systems at both endpoints
    and one interior point admit an exact direction outside that sheet. Exp-036 excludes
    that particular direction from the true Bouligand tangent cone by exact second-order
    obstructions in both possible nearby owner-axis branches. Exp-038 now certifies the
    complete branchwise linearization-cone inventory: both owner branches coincide, the
    endpoint quotients have eight rays, and the interior quotients have six. These are
    partial results, not a complete answer. Exp-039 proves that R1, R2, R3, and R6 have
    exact fixed-angle continuations inside one connected five-dimensional cell-local
    LP-optimal position polytope, with positive first-order stresses on twelve declared
    path segments. It does not prove the whole polytope stationary or join A to B inside
    the stationary set. Nonlinear realization of the remaining transverse and mixed
    directions, the full nonsmooth stationary component, and the unequal-side clearance
    questions remain open. Exp-040 preregistered a shared exact rotating path for R4 and
    R5 but stopped unresolved before retained measurement: temporary generation and
    replay passed, while independent review retained five exact proof-perimeter gaps in
    axis strictness, multiplier positivity, tied-feature derivation, partial-result
    routing, and semantic controls. Its draft checker is a resume point, not an R4/R5
    result. Exp-041 then rejects a stricter proof-perimeter criterion because
    `0-3:owner3:a-` is zero only at the positive path endpoint. That exact root does not
    harm the separately certified pair separator or refute path feasibility. A successor
    must distinguish base, open-interval, and positive-endpoint zero inventories and
    close three remaining control and partial-result guards. Exp-042 meets that
    endpoint-aware criterion: all six R4/R5 paths have exact universal feasibility and
    positive first-order stress certificates, retained generation and replay agree, and
    all twenty semantic controls reject. This is six-path nonlinear realization, not an
    A-to-B stationary connection or exhaustive realization. The `-W`, mixed-direction,
    whole-component, and unequal-side questions remain open.
    Exp-043 stops before retained measurement because its draft evaluator does not
    derive rowwise second-order constants from full jets or check its exp-034
    acceleration witness. It leaves pure -W unresolved with a finite instrument list.
---
# H-023 — resolve the first ambiguous census cell

The `n = 5` sample is the earliest place where endpoint keys, matching side/contact
summaries, and geometric interpretation disagree.
It contains no observed optimum and therefore cannot be described as six points in one
optimum-side family.
Calling it either a rich landscape or one flat family before continuation would repeat
the same soundness error in opposite directions.

## Exact slices

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
support rows enforced.
Exp-036 then proves that displayed direction is not a true Bouligand tangent: the
owner-4 branch has exact excess coefficient `sqrt(2)/8`, and the owner-3 branch has gap
coefficient `-1/4` with positive relative-angle cusp margin `sqrt(2)/2 - 1/4`.

This is a strict linearized-versus-true-tangent gap for one direction, not a local
isolation theorem. Exp-038 completes the branchwise linear inventory: the owner branches
coincide at first order, the endpoint quotients have eight rays, the interior quotients
have six, and the common transverse cone has six rays with sole relation
`R3 + R6 = R4 + R5`.

That finite inventory does not prove that a transverse or mixed direction is a true
tangent. Exp-039 supplies exact fixed-angle continuation for `R1`, `R2`, `R3`, and `R6`:
their twelve A, interior, and B paths lie in one connected five-dimensional cell-local
LP-optimal position polytope and carry positive branchwise first-order stresses.
The stress is proved only on those paths, not throughout the polytope or on an A-to-B
connector. The remaining release classes, mixed-angle realization, deterministic quench
selection, the complete stationary component, and unequal-side minimax-clearance bounds
remain open.

Exp-040 preserves the original candidate and exp-041 records the exact endpoint defect
in its first correction criterion.
Exp-042 closes that finite list without changing the six paths: its case-indexed
endpoint inventory, both exact owner stresses, twenty typed semantic controls, and
deterministic retained replay pass.
R4 and R5 therefore have six explicit pathwise realizations at A, the midpoint, and B.
The result neither exhausts those release classes nor supplies a stationary connector
between A and B.

Exp-043 freezes a separate exact test of canonical pure `-W`, then stops at independent
review before retained measurement.
Its draft makes the predicted coefficients sign-even by construction instead of deriving
rowwise nonlinear wall and SAT constants, and its sheet control does not consume a
checked acceleration witness.
The retained finite successor list is an exact truncated-series row engine, full jets,
weighted rowwise curvature, a production sheet witness, and mechanical two-scale
routing. Pure `-W` and mixed directions remain unresolved.

The following W7 phase now supplies the case-free exact-jet layer and source-bound
first-order row tests.
It derives exact wall and SAT values, gradients, Hessians, path coefficients, and
weighted combinations, but deliberately makes no branch-completeness, scale-routing, or
obstruction claim. A separately preregistered exp-044 must add those case-level
obligations before pure `-W` can be measured again.

Exp-044 now freezes that case-level integration: every production row must flow through
the accepted jet helper, the sheet witness must be checked, and the bounded/unbounded
owner-3 scale cases must be executable before a retained pure `-W` disposition exists.

This is the focused control for H-021 and the practical precursor to H-011.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
