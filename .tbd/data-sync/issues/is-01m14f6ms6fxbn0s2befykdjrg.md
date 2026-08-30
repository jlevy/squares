---
type: is
id: is-01m14f6ms6fxbn0s2befykdjrg
title: Settle rigidity for n=5, 28 and 40 beyond single-square translation
kind: task
status: open
priority: 2
version: 6
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T15:18:21.210Z
updated_at: 2026-08-30T13:06:29.214Z
---
The translation escape screen finds no movable square for n=5, 11, 28 and 40, but a miss is one-directional: rotation of a single square and coordinated multi-square motion are outside it. So frontier/n-005, n-028 and n-040 now carry rigidity.property: undetermined, which is a result rather than an absence, while Kingbird annotates all four 'Rigid.'

n=11 is the worked example of settling this properly: cases/trump11/tangent_cones.py builds all 128 derivative-distinct branchwise one-sided linearized cones at the exact fixed-side pose, shows each is the zero cone, and upgrades that to local isolation by a finite-branch subsequence argument. That gives frontier/n-011.md its locally-rigid block with assurance verified and method exact-algebraic.

The work: apply the same machinery to n=5, 28 and 40. n=5 is the easiest target - its side is 2+sqrt(2)/2, it is proved optimal, and its structure is small. Success means each record's rigidity block moves from undetermined to locally-rigid on a first-party certificate, independently confirming the catalogue's annotation instead of transcribing it.

Failure is also a result: if a feasible motion exists, the record becomes not-rigid and the catalogue's annotation is wrong, which is a finding about the source worth reporting.

Do not shortcut this by promoting catalogue_rigid into the rigidity block. That conflation is D-354 and tests/test_frontier_rigidity_assessment.py fails on it.

## Notes

2026-08-30 phases 16-19 (session-045). n=40 decided at first order and characterized; nothing promoted.

RESULT. n=40 is infinitesimally FLEXIBLE, exactly, over Q(sqrt 2). Seven admissible directions are known: one in the null space of the rows every branch carries, six outside it (retained in devtools/n40_rays.py), together spanning rank 5. ALL SEVEN are refused at second order by verified non-negative self-stresses (w.A = 0, w.q < 0, only tight rows entering). This is NOT second-order rigidity: the cone is not bounded, and the record says so in three places.

WHERE THE FLEX LIVES. Every admissible direction found, by two unrelated routes, turns squares of the tilted block and leaves all 24 axis-aligned squares fixed. Stronger: 52 of the frame's 72 coordinates are PROVED zero in every branch -- every branch's cone sits inside the relaxed cone, so a coordinate the relaxed rows pin is pinned however the 42 disjunctions resolve, and each carries a Farkas certificate verified in the field. No branch enumeration needed. The other 20 are unproved; 40 targeted searches found no admissible direction for them, which is coverage and not a proof (the translation-escape screen carries the same registered limitation).

MECHANISM. For two block squares sharing a full edge, the moving corner's rotation term is +1/2 and the host normal's rotation term is -1/2; they cancel. That is why the block turns in place at first order, and why no instrument ignoring host rotation could see it.

METHOD, and the two things that did not work. The 2^42 branch enumeration was never run. Candidates come from exact null spaces -- of the all-branch rows, and of a linear program's ACTIVE SET (the vertex itself cannot be rationalized into its own cone; the set of rows it makes tight is combinatorial and re-solving it exactly gives a direction satisfying those rows by construction). What did not work: the relaxed cone is not a subspace (152 of 248 rows proved to vanish on it, 96 not), so the problem could not be collapsed into 5 dimensions that way.

DEFECTS. D-390 fixed (incidence != contact; 208 of 560 pair rows). D-391 OUTSTANDING and it INVERTS the n=40 answer -- an assessor that intersects the disjunctions certifies the block's 48 coordinates as pinned and reports this packing rigid. D-392, D-393 (the pre-push floor does not run tests; CI was red 75 min across 4 pushes), D-394. count 394.

NOTHING PROMOTED. An infinitesimal flex is not a motion; the gaps curve shut at -t^2/2. frontier n-040 stays `undetermined` and the catalogue's "Rigid." is not contradicted. What is settled is that no first-order argument can establish n=40's rigidity.

ARTIFACTS. devtools/assess_n40_rigidity.py (gate step 3m18s, full tier, path-selected), devtools/n40_rays.py, devtools/assess_n5_rigidity.py (shared machinery; its name is now wrong and a rename is owed), tests/test_n40_rigidity.py, record bc-049-n40-rigidity-bracket.json, X-007 current.

n=28 untouched: decimals only, no exact construction.

NEXT: bound the cone, or say what a bound needs. With 52 frame coordinates proved the live question is the block's 48 plus the 20 unproved frame ones.
