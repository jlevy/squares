---
type: is
id: is-01m4p42wedbt2e9e3r7fhmphxa
title: Exact same-side re-solve over Q of a regularized view at the witness side (slice 3)
kind: task
status: in_progress
priority: 1
version: 3
labels:
  - regularization
dependencies: []
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
created_at: 2026-10-11T18:37:28.909Z
updated_at: 2026-10-11T19:48:55.906Z
---
think-ux1v slice 3. Branch claude/gifted-bell-57e62o.

## Notes

2026-10-11: implemented (packing/devtools/regularize_same_side.py + 12 tests, uncommitted, for the tools layer). resolve_view re-solves a view exactly over Q at the witness side; refuse mode succeeds only on exactly consistent tight sets (axis grids, 2 of 22 tilted rational), relax mode leaves conflicting/ill-conditioned rows as slack and is the one the driver uses. Survey n = 1..176 from witnesses' own floats: rational 119/120 under relax (155 fails), decimal 26/55 (20 Farkas: Göbel-family printed sides truncated below x + sqrt2/2, e.g. n = 10 at -9.7e-30). 14 decimal counts refused by the axis tool (17, 29, 37, 41, 50, 53, 54, 71, 87, 124, 128, 147, 148, 173) get exact packings at the promoted side 1e-22..1e-14 below the verified bound: register-result candidates (owner question 3). Fable max correctness review of the contract dispatched before commit.
