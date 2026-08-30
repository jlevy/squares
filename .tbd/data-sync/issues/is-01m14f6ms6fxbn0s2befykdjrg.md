---
type: is
id: is-01m14f6ms6fxbn0s2befykdjrg
title: Settle rigidity for n=5, 28 and 40 beyond single-square translation
kind: task
status: open
priority: 2
version: 5
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T15:18:21.210Z
updated_at: 2026-08-30T12:24:55.522Z
---
The translation escape screen finds no movable square for n=5, 11, 28 and 40, but a miss is one-directional: rotation of a single square and coordinated multi-square motion are outside it. So frontier/n-005, n-028 and n-040 now carry rigidity.property: undetermined, which is a result rather than an absence, while Kingbird annotates all four 'Rigid.'

n=11 is the worked example of settling this properly: cases/trump11/tangent_cones.py builds all 128 derivative-distinct branchwise one-sided linearized cones at the exact fixed-side pose, shows each is the zero cone, and upgrades that to local isolation by a finite-branch subsequence argument. That gives frontier/n-011.md its locally-rigid block with assurance verified and method exact-algebraic.

The work: apply the same machinery to n=5, 28 and 40. n=5 is the easiest target - its side is 2+sqrt(2)/2, it is proved optimal, and its structure is small. Success means each record's rigidity block moves from undetermined to locally-rigid on a first-party certificate, independently confirming the catalogue's annotation instead of transcribing it.

Failure is also a result: if a feasible motion exists, the record becomes not-rigid and the catalogue's annotation is wrong, which is a finding about the source worth reporting.

Do not shortcut this by promoting catalogue_rigid into the rigidity block. That conflation is D-354 and tests/test_frontier_rigidity_assessment.py fails on it.

## Notes

2026-08-30 phases 16-17 (session-045). n=40 DECIDED at first order: infinitesimally FLEXIBLE, with an exact witness, and that witness refused at second order.

THE MOTION. All sixteen tilted-block squares turn together, each about its own centre at the same rate, with translations. No frame square moves. Exactly zero gap rate on all 248 contacts that hold in every branch; at each of the 42 corner-touching pairs one separating axis is given up and the other kept, which is all non-overlap asks (it only has to do that at 24 of the 42). Vector in Q(sqrt 2)^120, every claim re-decided in the field.

MECHANISM, checked by hand on the pair (24,25): for two block squares sharing a full edge, the moving corner's rotation term is +1/2 and the host normal's rotation term is -1/2, and they cancel. No instrument that ignores the host's rotation could find this.

METHOD. No 2^42 enumeration. Candidates come from the null space of the single-axis rows (rank 115, null dimension 5) -- exact, so no rounding can push a candidate out of the cone it came from, which is what defeated the LP-vertex route. A candidate is a motion exactly when every disjunctive pair still has an admissible axis, and that choice names the branch directly.

SECOND ORDER. 104 of the 283 tight contacts curve into the obstacle; a verified non-negative self-stress (w.A = 0, w.q < 0, 55 rows carrying weight) rules out every second-order correction. Only tight rows enter the stress -- a contact already opening at first order imposes nothing at second, and including one would assemble a refusal from non-binding constraints.

HOW MUCH OF THE CONE. Measured, not assumed: of the 3124 nonzero integer combinations in [-2,2]^5 of the null basis, exactly four extend, and all four are multiples of one basis vector. So inside the subspace where every all-branch contact is tight, the admissible set is exactly a LINE -- the same shape as n=5. This does not bound the cone: directions leaving some all-branch contact strictly opening are outside the subspace and unsearched. So NOT second-order rigid; one line refused, in one branch.

D-391's cost is measured, not counterfactual: it INVERTS the answer. An assessor that intersects the disjunctions certifies all 120 coordinates as pinned -- reports this packing rigid. Removing it is what found the witness.

INDEPENDENT CONFIRMATION. An adversarial sub-agent reimplemented constraint_rows from scratch and compared all 48,000 entries (zero mismatches), wrote its own finite-motion checker, and confirmed t^2 scaling (fitted exponent 1.981). It also caught a real misstatement: the 42 given-up rows fall across 24 pairs, not one per pair. Corrected everywhere.

NOTHING IS PROMOTED. An infinitesimal flex is not a motion. frontier n-040 stays `undetermined`; the catalogue's "Rigid." is not contradicted. What is settled is that no first-order argument can establish n=40's rigidity.

Tools: devtools/assess_n40_rigidity.py (+ shared machinery in assess_n5_rigidity.py, whose name is now wrong and owes a rename); record bc-049-n40-rigidity-bracket.json; tests/test_n40_rigidity.py; gate step "n=40 rigidity bracket still reproduces" (full tier only, ~3 min). X-007 updated for all of it, including making its n=5 disjunction exemption a check rather than prose.

n=28 remains untouched: it retains only decimals and has no exact construction.

NEXT: whether n=40's first-order cone is larger than that line -- i.e. directions outside the null space of the all-branch rows.
