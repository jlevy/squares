---
type: is
id: is-01m0r3zv2hh2jj64rb8mhqbtre
title: Measure terminal flatness and connectivity before defining basin identity
kind: bug
status: open
priority: 0
version: 12
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-correctness
dependencies:
  - type: blocks
    target: is-01m0pw86qg81x5qnjvzge42f4v
  - type: blocks
    target: is-01m0pw8698kc2bqm7d7fy0xydy
  - type: blocks
    target: is-01m0p4asxdaenzfkx53j4vh6qs
  - type: blocks
    target: is-01m0qxpb7634zbzt638d239jks
  - type: blocks
    target: is-01m0r50mrppgcvsp2ewrac0x6z
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T20:11:30.757Z
updated_at: 2026-08-23T21:48:06.165Z
---
D-034, blocking the census. Exact evidence: the n=3 side-2 sliding family is a connected positive-dimensional terminal set that one contact certificate and many geometric keys split into quantum-dependent rows. The n=5 golden adds an unresolved pair: equal side, short form, contact certificate, angle signature and contact count but different geometry. Those facts do not prove the n=5 rows are connected or establish a five-dimensional family; raw constraint counting is not a rank certificate. Acceptance: archive both n=5 poses and their active cells; compute the fixed-cell optimal-face rank/nullity from the active LP matrix and objective; compute the full pose/angle active-constraint Jacobian; continue every null direction with independent validity checks; test whether the two endpoints are path-connected across cell/contact strata; report certified dimension or unresolved bounds; and feed the evidence to think-0yo9 rather than choosing identity from side/contact hashes.

## Notes

2026-08-23, CONCEDED after the PR #15 review (F-18). The n=5 "five-dimensional family" claim was rank-free and should not stand as written.

Counting 11 contact constraints against 16 degrees of freedom only bounds the dimension if the 11 constraint gradients are linearly independent, which was never established; and a first-order flex need not extend to a finite motion. Constraint counting is a heuristic for SUSPECTING under-constraint, not a proof of it.

What survives: two quenches landed on two configurations with the same side, the same closed form and the same contact certificate. That is real evidence the endpoint is not unique. What does not survive: the dimension, and the word "family".

So: n = 3 is the airtight witness (three unit squares in a 2x2 box slide freely -- a demonstrable continuous motion). n = 5 is an UNRESOLVED OBSERVATION pending active-matrix rank, full Jacobian, feasible-null-direction, or continuation evidence. PR #15's living docs already say this; main's do not yet and should be brought into line when the branches reconcile.

This does not weaken D-034 as a blocker. It sharpens what has to be measured: the LP-degeneracy route in the note above is exactly the rank evidence the claim was missing, so the planned work is unchanged -- only the confidence of the prose was wrong.
