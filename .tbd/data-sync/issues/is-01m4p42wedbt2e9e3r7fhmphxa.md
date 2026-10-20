---
type: is
id: is-01m4p42wedbt2e9e3r7fhmphxa
title: Exact same-side re-solve over Q of a regularized view at the witness side (slice 3)
kind: task
status: in_progress
priority: 1
version: 13
delegate: claude-code@vm
labels:
  - regularization
dependencies: []
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
hold: null
hold_until: null
created_at: 2026-10-11T18:37:28.909Z
updated_at: 2026-10-12T01:10:39.581Z
started_at: 2026-10-11T20:03:59.728Z
closed_at: 2026-10-11T23:35:51.728Z
close_reason: Committed in jlevy/squares#515 (claude/regularize-tools)
resolution: null
duplicate_of: null
---
think-ux1v slice 3. Tools layer: branch claude/busy-pascal-vgiccb, stacked on #509 (claude/gifted-bell-57e62o).

## Notes

2026-10-11: implemented (packing/devtools/regularize_same_side.py + 12 tests, uncommitted, for the tools layer). resolve_view re-solves a view exactly over Q at the witness side; refuse mode succeeds only on exactly consistent tight sets (axis grids, 2 of 22 tilted rational), relax mode leaves conflicting/ill-conditioned rows as slack and is the one the driver uses. Survey n = 1..176 from witnesses' own floats: rational 119/120 under relax (155 fails), decimal 26/55 (20 Farkas: Göbel-family printed sides truncated below x + sqrt2/2, e.g. n = 10 at -9.7e-30). 14 decimal counts refused by the axis tool (17, 29, 37, 41, 50, 53, 54, 71, 87, 124, 128, 147, 148, 173) get exact packings at the promoted side 1e-22..1e-14 below the verified bound: register-result candidates (owner question 3). Fable max correctness review of the contract dispatched before commit.

2026-10-11 (session_017JNnKDwL74rnktr9s8BdjP): the implementation the note above records was never committed or pushed; no remote branch carries packing/devtools/regularize_same_side.py (claude/gifted-bell-57e62o holds only the vendor layer), so it was lost with that session's container. Rebuilt in this session on branch claude/busy-pascal-vgiccb (the tools layer, stacked on #509) against a fixed interface (resolve(source_witness, view poses, mode=relax|refuse) -> SameSideOutcome; CLI with --survey), by a Fable sub-agent; the survey figures above are to be re-measured, not carried over.

2026-10-11 (session_017JNnKDwL74rnktr9s8BdjP): rebuilt and landed (b56f6cb60; generator_box diagnostic fix in 6cba173ed): 18 tests. Survey n = 1..80 (own poses perturbed 1e-12, relax): every rational witness same (54); decimal 15 same, 10 overlap (the Göbel family: printed sides truncate an irrational optimum, so no rational packing exists at s_W); n = 51 no-exact-frame. relax is required (refuse mode: inconsistent-tight-set at most counts). Pilot: same at 11, 17, 26, 37, 66, 87, 101, 126, 200, 260, 292, 295, 324; unmatched-rotation at 70, 102, 129, 146, 206, 267 because the exact solve turns tilted bands by up to hundredths of a degree (0.0115 at 70) to a lower packing.

2026-10-11: PR https://github.com/jlevy/squares/pull/511 (draft, base claude/gifted-bell-57e62o), added to GitHub stack #498 (#487 merged, #497, #509, #511) via POST /stacks/498/add (gh stack could not be installed: the session proxy refuses github/gh-stack).

2026-10-12: reopened. I closed this as committed in #515, but #511 (claude/busy-pascal-vgiccb, another session, opened earlier) implements the same layer and the owner answered against #511; #515 duplicates it and waits on the owner's call (session_014Y3kYUK2wqLWoA4rqK1Wng).
