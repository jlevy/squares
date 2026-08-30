---
type: is
id: is-01m14f6ms6fxbn0s2befykdjrg
title: Settle rigidity for n=5, 28 and 40 beyond single-square translation
kind: task
status: open
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T15:18:21.210Z
updated_at: 2026-08-30T11:37:08.115Z
---
The translation escape screen finds no movable square for n=5, 11, 28 and 40, but a miss is one-directional: rotation of a single square and coordinated multi-square motion are outside it. So frontier/n-005, n-028 and n-040 now carry rigidity.property: undetermined, which is a result rather than an absence, while Kingbird annotates all four 'Rigid.'

n=11 is the worked example of settling this properly: cases/trump11/tangent_cones.py builds all 128 derivative-distinct branchwise one-sided linearized cones at the exact fixed-side pose, shows each is the zero cone, and upgrades that to local isolation by a finite-branch subsequence argument. That gives frontier/n-011.md its locally-rigid block with assurance verified and method exact-algebraic.

The work: apply the same machinery to n=5, 28 and 40. n=5 is the easiest target - its side is 2+sqrt(2)/2, it is proved optimal, and its structure is small. Success means each record's rigidity block moves from undetermined to locally-rigid on a first-party certificate, independently confirming the catalogue's annotation instead of transcribing it.

Failure is also a result: if a feasible motion exists, the record becomes not-rigid and the catalogue's annotation is wrong, which is a finding about the source worth reporting.

Do not shortcut this by promoting catalogue_rigid into the rigidity block. That conflation is D-354 and tests/test_frontier_rigidity_assessment.py fails on it.

## Notes

2026-08-30 phase 15 (session-045). n=40 attempted with the machinery this bead asks for, and the answer is a bracket rather than a verdict.

D-388 predicted the blocker was arithmetic: 296 of 608 rows mix rational and sqrt-2 parts, so a rational-weight Farkas search answers a different system. That search now exists (assess_n5_rigidity.certify: a restricted cone plus a sign-free one ordered by p + sqrt(2) q >= 0, both verified exactly in the field) and it reproduces n=5's fourteen certificates without rationalize. The prediction was right and the blocker was somewhere else.

Two further defects, both flattering, both absent at n=5 and so invisible until the tool met a second pose:
- D-390 (fixed): _on_edge accepts a corner on an edge ENDPOINT, so edge-to-edge neighbours registered contacts on the two perpendicular edges that separate nothing. 208 of n=40's 560 pair rows. Each forbids a motion that overlaps nothing. Fixed by `separating`, which keeps only edges putting the whole moving square on their outer side.
- D-391 (outstanding): squares meeting at one corner are held apart by TWO axes and non-overlap asks that either keep separating, so the tangent cone is a union of half-spaces. The assessor intersected them. 42 of n=40's 98 touching pairs; n=5 has none. Guarded by DisjunctiveContactError, not fixed.

The bracket (devtools/assess_n40_rigidity.py, record bc-049-n40-rigidity-bracket.json):
- intersect the disjunctions -> cone contained in every branch -> 120/120 pinned, so no flex is exhibitable cheaply
- drop them -> cone containing every branch -> 56/120 pinned, so rigidity is not proved
n=40 is first-order undecided with both sides measured. No frontier record moves; n-040 stays undetermined on the translation-escape screen's evidence.

Deciding it is the n=11 route at 2^42 instead of 2^7. A branch-and-bound pruning on a fully pinned prefix is the same instrument and may not need every leaf -- that is the next slice for n=40, and it is a real one rather than a wait.

n=5 remains the finished instance: 14 pinned, one free direction, obstructed at second order. Its record is bit-identical under both new guards, which is the check that matters.

X-007 states D-391's principle in prose and argues n=5 is exempt; that exemption is now a check and the document should say so.
