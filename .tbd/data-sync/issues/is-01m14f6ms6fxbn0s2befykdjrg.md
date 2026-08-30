---
type: is
id: is-01m14f6ms6fxbn0s2befykdjrg
title: Settle rigidity for n=5, 28 and 40 beyond single-square translation
kind: task
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T15:18:21.210Z
updated_at: 2026-08-30T10:37:37.630Z
---
The translation escape screen finds no movable square for n=5, 11, 28 and 40, but a miss is one-directional: rotation of a single square and coordinated multi-square motion are outside it. So frontier/n-005, n-028 and n-040 now carry rigidity.property: undetermined, which is a result rather than an absence, while Kingbird annotates all four 'Rigid.'

n=11 is the worked example of settling this properly: cases/trump11/tangent_cones.py builds all 128 derivative-distinct branchwise one-sided linearized cones at the exact fixed-side pose, shows each is the zero cone, and upgrades that to local isolation by a finite-branch subsequence argument. That gives frontier/n-011.md its locally-rigid block with assurance verified and method exact-algebraic.

The work: apply the same machinery to n=5, 28 and 40. n=5 is the easiest target - its side is 2+sqrt(2)/2, it is proved optimal, and its structure is small. Success means each record's rigidity block moves from undetermined to locally-rigid on a first-party certificate, independently confirming the catalogue's annotation instead of transcribing it.

Failure is also a result: if a feasible motion exists, the record becomes not-rigid and the catalogue's annotation is wrong, which is a finding about the source worth reporting.

Do not shortcut this by promoting catalogue_rigid into the rigidity block. That conflation is D-354 and tests/test_frontier_rigidity_assessment.py fails on it.

## Notes

2026-08-30 session-045: BC-049 settled at n=5; n=28 and n=40 remain. Asked exactly over Q(sqrt 2) at Goebel's construction rather than the retained decimal witness, which is 2.4e-30 off the diagonal and infeasible at the scale a certificate works at. The cone of infinitesimal motions is exactly the line spanned by rotation of the middle square about its own centre: 14 of 15 coordinates pinned by Farkas certificates verified in the field, and the fifteenth mentioned by no constraint because each corner square's inner corner rests at the midpoint of the middle square's edge, where (p-c).n_perp vanishes. The same geometry shuts it at second order -- each pair gap is exactly (1/2)cos(t) - 1/2, curvature -1/2 at both signs -- and a verified non-negative self-stress with w.A = 0 and w.q < 0 refuses every second-order correction. So no twice-differentiable feasible arc leaves this pose with a nonzero derivative: second-order rigidity, which is not local rigidity. The frontier property stays undetermined and everything saying why it does changed: verified rather than numerically-checked, exact-algebraic rather than numerical-multiprecision, and first-party evidence E-n005-second-order-rigidity in place of the screen's, which takes n=5 out of assess_frontier_rigidity's ownership. Both D-354 guards stayed green without being edited. Three independent numerical methods confirm; a review corrected the closing argument (an analytic arc does not reparametrize to nonzero derivative when its leading Puiseux exponent is at least 2). Evidence: campaign/explorations/X-007-the-n5-optimum-flexes-once-and-that-once-is-shut.md, devtools/assess_n5_rigidity.py, campaign/series/series-000-smoke-and-calibration/results/bc-049-n5-rigidity-certificates.json, tests/test_n5_rigidity.py. Next action: n=28 and n=40 need an EXACT construction, not another assessment -- the machinery is general in shape and specific in inputs, and both retain decimal witnesses. That is the real price.
