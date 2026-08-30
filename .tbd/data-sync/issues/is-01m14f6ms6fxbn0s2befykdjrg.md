---
type: is
id: is-01m14f6ms6fxbn0s2befykdjrg
title: Settle rigidity for n=5, 28 and 40 beyond single-square translation
kind: task
status: open
priority: 2
version: 7
labels: []
dependencies: []
parent_id: is-01m12zjr144a4kg6rnv1t0pm6n
created_at: 2026-08-28T15:18:21.210Z
updated_at: 2026-08-30T14:10:24.355Z
---
The translation escape screen finds no movable square for n=5, 11, 28 and 40, but a miss is one-directional: rotation of a single square and coordinated multi-square motion are outside it. So frontier/n-005, n-028 and n-040 now carry rigidity.property: undetermined, which is a result rather than an absence, while Kingbird annotates all four 'Rigid.'

n=11 is the worked example of settling this properly: cases/trump11/tangent_cones.py builds all 128 derivative-distinct branchwise one-sided linearized cones at the exact fixed-side pose, shows each is the zero cone, and upgrades that to local isolation by a finite-branch subsequence argument. That gives frontier/n-011.md its locally-rigid block with assurance verified and method exact-algebraic.

The work: apply the same machinery to n=5, 28 and 40. n=5 is the easiest target - its side is 2+sqrt(2)/2, it is proved optimal, and its structure is small. Success means each record's rigidity block moves from undetermined to locally-rigid on a first-party certificate, independently confirming the catalogue's annotation instead of transcribing it.

Failure is also a result: if a feasible motion exists, the record becomes not-rigid and the catalogue's annotation is wrong, which is a finding about the source worth reporting.

Do not shortcut this by promoting catalogue_rigid into the rigidity block. That conflation is D-354 and tests/test_frontier_rigidity_assessment.py fails on it.

## Notes

2026-08-30 session-045 phases 15-23. HANDOFF for BC-049.

STATE OF THE THREE INSTANCES.
n=5 DONE: second-order rigid on first-party exact evidence (E-n005-second-order-rigidity), replayed in the gate. Remaining gap is that second-order rigidity is not local rigidity; X-007 writes the curve-selection argument out as prose and nothing machine-checks it. That is by design.
n=40 DECIDED AT FIRST ORDER, open beyond it. Infinitesimally FLEXIBLE. Seven directions retained, each verified in Q(sqrt 2), each refused at second order by its own verified self-stress, each turning the tilted block and leaving the frame fixed. 52 of 72 frame coordinates PROVED zero in every branch; 12 of 16 block squares PROVED to turn at one rate (the 4 left out are exactly the block's interior cells). Cone bounded to dimension 45; known directions span 6. Registered as E-n040-first-order-flexibility; frontier property stays `undetermined` because an infinitesimal flex is not a motion.
n=28 UNTOUCHED: decimals only, no exact construction. D-389 is the reason to read the literature before pricing machinery against it -- n=40 turned out to be published all along.

WHAT n=40 WOULD TAKE TO FINISH. Not more of what this session did; the route is exhausted and the wall is measured:
- the all-branch rows can never bound the cone below the relaxed cone's own span, measured at rank 41, so 41-45 is the ceiling of every certificate available here;
- branch enumeration is 2^42 and does NOT reduce -- with 56 coordinates pinned, not one of the 42 disjunctions becomes vacuous on what remains;
- a linear program's vertex cannot be rationalized back into its own cone; what works is re-solving its ACTIVE SET exactly (that is how the six wider rays came out). Worth knowing before anyone retries the obvious thing.
Needed: an instrument that reasons about the disjunctions without enumerating them. cases/trump11/tangent_cones.py is the only branchwise-cone decider in the repo and it enumerates 2^7.

COST. Five defects, four in tools written hours earlier the same day: D-390 and D-391 (rigidity assessor), D-392 and D-394 (contract sweep), D-393 (this session's own gate discipline). D-391 is OUTSTANDING and it INVERTS the n=40 answer rather than weakening it -- an assessor that intersects the disjunctions reports this packing rigid.

OWED. (1) devtools/assess_n5_rigidity.py holds the machinery both sizes use and its name says otherwise; a rename touches the gate, the tests and two records. (2) The `n=40 rigidity bracket still reproduces` gate step is 4m57s, about a third of the full gate, which is what D-369 warns about; left whole deliberately -- if the cost bites, move it behind a flag rather than thinning the checks.

ARTIFACTS: devtools/assess_n40_rigidity.py, devtools/n40_rays.py, devtools/assess_n5_rigidity.py, tests/test_n40_rigidity.py, tests/test_n5_rigidity.py, record bc-049-n40-rigidity-bracket.json, X-007 (owns the argument for both sizes), frontier/n-040.md, frontier/evidence.yaml.
