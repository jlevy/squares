---
type: is
id: is-01m14f6ms6fxbn0s2befykdjrg
title: Settle rigidity for n=5, 28 and 40 beyond single-square translation
kind: task
status: open
priority: 2
version: 8
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T15:18:21.210Z
updated_at: 2026-08-30T14:34:31.351Z
---
The translation escape screen finds no movable square for n=5, 11, 28 and 40, but a miss is one-directional: rotation of a single square and coordinated multi-square motion are outside it. So frontier/n-005, n-028 and n-040 now carry rigidity.property: undetermined, which is a result rather than an absence, while Kingbird annotates all four 'Rigid.'

n=11 is the worked example of settling this properly: cases/trump11/tangent_cones.py builds all 128 derivative-distinct branchwise one-sided linearized cones at the exact fixed-side pose, shows each is the zero cone, and upgrades that to local isolation by a finite-branch subsequence argument. That gives frontier/n-011.md its locally-rigid block with assurance verified and method exact-algebraic.

The work: apply the same machinery to n=5, 28 and 40. n=5 is the easiest target - its side is 2+sqrt(2)/2, it is proved optimal, and its structure is small. Success means each record's rigidity block moves from undetermined to locally-rigid on a first-party certificate, independently confirming the catalogue's annotation instead of transcribing it.

Failure is also a result: if a feasible motion exists, the record becomes not-rigid and the catalogue's annotation is wrong, which is a finding about the source worth reporting.

Do not shortcut this by promoting catalogue_rigid into the rigidity block. That conflation is D-354 and tests/test_frontier_rigidity_assessment.py fails on it.

## Notes

2026-08-30 session-045 CLOSED (23 phases). Addendum to the handoff: Goebel's family, mapped.

D-389 was specific to n=40 -- a route priced while the construction sat published. The general question took twenty minutes: devtools/price_gobel_family.py enumerates every (a,b) with a-1 < b/sqrt2 < a+1 reaching n <= 100, compares the side a+1+b/sqrt2 against the retained best known, and verifies exactly where they match.

TWELVE sizes reached. OPTIMAL at FOUR: n = 5, 40, 65, 89.
- n=5 and n=40 already have exact case packages here.
- **n=65 (a=4,b=5) and n=89 (a=4,b=7) do NOT.** Both retain numerical-multiprecision witnesses and no case package, and both verify exactly in seconds -- 2080 and 3916 pairs decided by exact sign. Building cases/gobel65 and cases/gobel89 is the cheapest open work this bead offers.
- Nothing promoted: feasible at the retained side is not optimal.

THE NEAR MISS, which is the part that saves an afternoon: at a=2,b=4 the family gives n=28 -- a VALID packing of side 3+2sqrt2 = 5.82843, but the best known is 5.82444, better by 0.004, at algebraic degree 6. So n=28's optimum is NOT in this family and the n=40 answer does not carry over to it. That is why no exact construction is retained for n=28. `28 = 2(4)+4+16` is not the shortcut it looks like, and tests/test_gobel_family.py asserts the near miss so a future reader is stopped at the guess.

The generalization is controlled against cases/gobel40: built at a=3,b=4 it must reproduce that case corner for corner (compared on coefficients, since each builder makes its own NumberField and the field API refuses cross-field comparison -- which is the point of that refusal).

Gate step "Goebel's family reaches the sizes it reaches", ~5s, records tier. Record bc-049-gobel-family-coverage.json. 925 tests pass; CI green.

PROCESS NOTE: this slice happened inside a phase declared as process-review, which OR-5 says should have been redeclared. Recorded as a slip rather than papered over with a retroactive declaration.
