---
type: is
id: is-01m14f6ms6fxbn0s2befykdjrg
title: Settle rigidity for n=5, 28 and 40 beyond single-square translation
kind: task
status: open
priority: 2
version: 9
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T15:18:21.210Z
updated_at: 2026-08-30T15:21:04.590Z
---
The translation escape screen finds no movable square for n=5, 11, 28 and 40, but a miss is one-directional: rotation of a single square and coordinated multi-square motion are outside it. So frontier/n-005, n-028 and n-040 now carry rigidity.property: undetermined, which is a result rather than an absence, while Kingbird annotates all four 'Rigid.'

n=11 is the worked example of settling this properly: cases/trump11/tangent_cones.py builds all 128 derivative-distinct branchwise one-sided linearized cones at the exact fixed-side pose, shows each is the zero cone, and upgrades that to local isolation by a finite-branch subsequence argument. That gives frontier/n-011.md its locally-rigid block with assurance verified and method exact-algebraic.

The work: apply the same machinery to n=5, 28 and 40. n=5 is the easiest target - its side is 2+sqrt(2)/2, it is proved optimal, and its structure is small. Success means each record's rigidity block moves from undetermined to locally-rigid on a first-party certificate, independently confirming the catalogue's annotation instead of transcribing it.

Failure is also a result: if a feasible motion exists, the record becomes not-rigid and the catalogue's annotation is wrong, which is a finding about the source worth reporting.

Do not shortcut this by promoting catalogue_rigid into the rigidity block. That conflation is D-354 and tests/test_frontier_rigidity_assessment.py fails on it.

## Notes

2026-08-30 session-046 (one slice, 35 min). Goebel's family: all four optimal sizes now have exact constructions.

BUILT. cases/gobel_family/ holds the general form of the rule -- build(a, b) for any (a,b) with a-1 < b/sqrt2 < a+1 -- and verify_exact covers the two sizes that had none: n=65 (a=4,b=5) and n=89 (a=4,b=7). 2080 and 3916 pairs, every one decided by exact sign over Q(sqrt 2); 64 boundary coordinates each; duplicated-square negative control rejected at both. Wired into the `exact verification` gate step. One package rather than two copies of gobel40, and the control that makes the generalization trustworthy is that at a=3,b=4 it reproduces cases/gobel40 corner for corner (compared on coefficients, since each build makes its own NumberField).

UNEXPECTED FINDING. The witness-agreement bound started at 1e-11, on the reasoning that n=65 and n=89 are `numerical-multiprecision` records that might be independent optimisations merely landing on the same side. They agree with the construction to 4.81e-33 and 3.28e-33. Nothing independently optimised lands within 1e-32 of a construction it was not built from, so those two decimals ARE materialisations of Goebel's family -- exactly as n=40's turned out to be (D-389). Bound tightened to 1e-32; the docstring that said the opposite is corrected.

So all four sizes where the family is exactly the best known -- n = 5, 40, 65, 89 -- now have exact constructions here, and three of the four retained witnesses are identified as materialisations of it.

NOT DONE, deliberately: n=65 and n=89's witnesses stay `numerical-multiprecision`. Feasible at the retained side is not optimal, and moving them to `exact-algebraic` is an assurance-contract question this session did not open. That is the next askable thing.

n=28 remains out: the family gives it a valid packing 0.004 worse than the best known, whose optimum is at algebraic degree 6 and is not in the family.

SYNOPSIS's Current Handoff was still describing the morning's state and now carries the day.

934 tests pass; --edit green.
