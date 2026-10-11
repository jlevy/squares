---
type: is
id: is-01m4p42wedbt2e9e3r7fhmphxa
title: Exact same-side re-solve over Q of a regularized view at the witness side (slice 3)
kind: task
status: in_progress
priority: 1
version: 6
delegate: claude-code@vm
labels:
  - regularization
dependencies: []
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
hold: null
hold_until: null
created_at: 2026-10-11T18:37:28.909Z
updated_at: 2026-10-11T20:04:32.180Z
started_at: 2026-10-11T20:03:59.728Z
---
think-ux1v slice 3. Tools layer: branch claude/busy-pascal-vgiccb, stacked on #509 (claude/gifted-bell-57e62o).

## Notes

2026-10-11: implemented (packing/devtools/regularize_same_side.py + 12 tests, uncommitted, for the tools layer). resolve_view re-solves a view exactly over Q at the witness side; refuse mode succeeds only on exactly consistent tight sets (axis grids, 2 of 22 tilted rational), relax mode leaves conflicting/ill-conditioned rows as slack and is the one the driver uses. Survey n = 1..176 from witnesses' own floats: rational 119/120 under relax (155 fails), decimal 26/55 (20 Farkas: Göbel-family printed sides truncated below x + sqrt2/2, e.g. n = 10 at -9.7e-30). 14 decimal counts refused by the axis tool (17, 29, 37, 41, 50, 53, 54, 71, 87, 124, 128, 147, 148, 173) get exact packings at the promoted side 1e-22..1e-14 below the verified bound: register-result candidates (owner question 3). Fable max correctness review of the contract dispatched before commit.

2026-10-11 (session_017JNnKDwL74rnktr9s8BdjP): the implementation the note above records was never committed or pushed; no remote branch carries packing/devtools/regularize_same_side.py (claude/gifted-bell-57e62o holds only the vendor layer), so it was lost with that session's container. Rebuilt in this session on branch claude/busy-pascal-vgiccb (the tools layer, stacked on #509) against a fixed interface (resolve(source_witness, view poses, mode=relax|refuse) -> SameSideOutcome; CLI with --survey), by a Fable sub-agent; the survey figures above are to be re-measured, not carried over.
