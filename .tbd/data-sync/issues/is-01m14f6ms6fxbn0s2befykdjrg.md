---
type: is
id: is-01m14f6ms6fxbn0s2befykdjrg
title: Settle rigidity for n=5, 28 and 40 beyond single-square translation
kind: task
status: open
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T15:18:21.210Z
updated_at: 2026-08-30T11:55:12.362Z
---
The translation escape screen finds no movable square for n=5, 11, 28 and 40, but a miss is one-directional: rotation of a single square and coordinated multi-square motion are outside it. So frontier/n-005, n-028 and n-040 now carry rigidity.property: undetermined, which is a result rather than an absence, while Kingbird annotates all four 'Rigid.'

n=11 is the worked example of settling this properly: cases/trump11/tangent_cones.py builds all 128 derivative-distinct branchwise one-sided linearized cones at the exact fixed-side pose, shows each is the zero cone, and upgrades that to local isolation by a finite-branch subsequence argument. That gives frontier/n-011.md its locally-rigid block with assurance verified and method exact-algebraic.

The work: apply the same machinery to n=5, 28 and 40. n=5 is the easiest target - its side is 2+sqrt(2)/2, it is proved optimal, and its structure is small. Success means each record's rigidity block moves from undetermined to locally-rigid on a first-party certificate, independently confirming the catalogue's annotation instead of transcribing it.

Failure is also a result: if a feasible motion exists, the record becomes not-rigid and the catalogue's annotation is wrong, which is a finding about the source worth reporting.

Do not shortcut this by promoting catalogue_rigid into the rigidity block. That conflation is D-354 and tests/test_frontier_rigidity_assessment.py fails on it.

## Notes

2026-08-30 phase 16 (session-045). n=40 DECIDED at first order: infinitesimally FLEXIBLE, with an exact witness.

The motion: all sixteen squares of the tilted block turn together, each about its own centre at the same angular velocity, with translations. No frame square moves. Exactly zero gap rate on all 248 contacts that hold in every branch; at each of the 42 corner-touching pairs it gives up one separating axis and keeps the other, which is all non-overlap asks. Vector in Q(sqrt 2)^120, every claim re-decided in the field.

Mechanism, checked by hand on the pair (24,25): for two block squares sharing a full edge, the moving corner's rotation term is +1/2 and the host normal's rotation term is -1/2, and they cancel. That is why the block can spin in place to first order.

Found without enumerating 2^42 branches. Candidates come from the null space of the single-axis rows (rank 115, null dimension 5) -- exact, so no rounding can push a candidate out of the cone it came from, which is what defeated the LP route. A candidate is a motion exactly when every disjunctive pair still has an admissible axis, and that choice names the branch directly.

D-391's cost is now measured, not counterfactual: it INVERTS the answer. An assessor that intersects the 42 disjunctions certifies all 120 coordinates as pinned -- i.e. reports this packing rigid. Removing the defect is what found the witness. D-391's entry and SYNOPSIS are corrected accordingly.

Independent confirmation by an instrument that reads no constraint row: move along the witness by finite t, measure real SAT gaps in floats. Worst gap -5.0e-7 / -5.0e-9 / -5.0e-11 at t = 1e-3 / 1e-4 / 1e-5 -- exactly -t^2/2. Quadratic, so no first-order error in the linearization.

NOTHING IS PROMOTED. An infinitesimal flex is not a motion. The gaps curve shut at second order, so frontier n-040's rigidity block stays `undetermined` and the catalogue's "Rigid." is not contradicted. What is settled is that no first-order argument can establish n=40's rigidity.

Tool: devtools/assess_n40_rigidity.py; record bc-049-n40-rigidity-bracket.json; tests/test_n40_rigidity.py.

Next slice: the second-order question, posed on the chosen branch. n=5's route is a non-negative self-stress w with w.A = 0 and w.q < 0 refusing every second-order correction. The -t^2/2 signature says some row has negative curvature; whether a correction rescues it is open. Also open: whether the first-order cone is larger than this witness (only a short integer sweep of a 5-dimensional null space was searched).
