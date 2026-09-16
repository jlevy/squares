---
type: is
id: is-01m2gxkhmczffa661vb6emdxz5
title: "[epic] Strategies with declared guidance, compared in one evaluation loop"
kind: epic
status: open
priority: 1
version: 14
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
refs:
  - kind: pr
    url: https://github.com/jlevy/squares/pull/190
    at: 2026-09-16T22:15:34.937Z
labels: []
dependencies: []
parent_id: is-01m29kqwefbzzpt7bngm68pq6p
child_order_hints:
  - is-01m2gxkkqkb0ckc9w3m3mp4apv
  - is-01m2gxkp2c5hk981zhv3aejfga
  - is-01m2gxks9tdr1hhatv3mx359y3
  - is-01m2gxkvbndg46r6pjy3352cb8
  - is-01m2gxkxbhyqesd394p4ezr66c
  - is-01m2gxkzqdxb01e2h4tpkvczw7
  - is-01m2gyp18kcxq2g8gq7hjacg3n
  - is-01m2gyp41nh48d2kc155rrvzy7
  - is-01m2p0xq9nac6ftmr19978krh3
created_at: 2026-09-14T21:36:39.047Z
updated_at: 2026-09-16T22:15:34.938Z
---
Owner, 2026-09-14: "the likeliness of how well this works is going to depend very much on how the structure and strategy work, and there are many midpoints that are not fully blind nor fully guided... different levels of configuration mapped everywhere, from just partitioning the connected components to the contact graphs to the contacts where the sides are flush, to simplified contact graphs where the touching components are simplified to be parallel initially... by contracting further, they could pull apart... build the simplified, highly efficient versions of each of these and use those as intermediate targets that are not fully blind but not fully showing the optimal solution."

The research question this turns the benchmark into: **for each record, how much of its structure must a search be given before it finds the rest?** Success is measured against a rung of given information, not as one blind number.

What is already known (verified 2026-09-14; details in the annealing plan's "The Guidance Ladder" section):
- Blind is a middle rung. It closes the walls onto the record side for n, and in the `bodies` style the benchmark used it welds squares into blocks chosen by matching the two records.
- A first ladder ran on the projection solver on 2026-09-09 (X-025, `packing/devtools/sweep_structure_hints.py`). Structure declared as constraints made search worse at n <= 17: success fell as contacts were declared, the reachable side got worse, and exact equalities repelled. Structure used to build the start helped (1/8 to 5/8 at a loose side, commit 2d2a7790). Samples were 4-8 cold starts, and no registered experiment exists.
- The workbench's contact-graph attraction did not realise the graph: its range is 0.25 of a side and it has no aligning torque (spike NOTES.md 2219-2254).
- The owner's merge-near-flush-then-release has not been built in any engine.

Design rules those facts impose: structure constructs and stages a run and is not held as a constraint; bands, never equalities; every structural rung is run beside rewired and thinned controls of the same size; a result names its rung and never claims discovery.

Children: extraction, kernel mechanics, start construction, benchmark cells, the rung in Pack and Search, hypotheses before the first round.

## Notes

2026-09-16 continuation: this existing epic is the authoritative owner for the newly requested graded guidance program. Add workbench Phase 5A and compare none, touching-component partitions, contact graphs, and oriented face assignments through one shared backend/browser contract. Keep ordinary global stickiness distinct from structural guidance; require continuous strength and schedules, known-answer calibration, held-out controls, deterministic replay, and retained accepted/rejected/invalid rounds. The first systematic sweep is think-0epc.
