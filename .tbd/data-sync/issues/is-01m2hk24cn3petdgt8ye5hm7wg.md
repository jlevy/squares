---
type: is
id: is-01m2hk24cn3petdgt8ye5hm7wg
title: "PR #171 review D16: stage height and headline clearance measured on geometry the SVG clips"
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb41hy7fx18dy67asht84d
created_at: 2026-09-15T03:51:37.108Z
updated_at: 2026-09-15T04:49:50.230Z
closed_at: 2026-09-15T04:16:19.559Z
close_reason: "Fixed on PR #171 in 8fe4749e: stage/lowest-drawn counts only displayed, painted shapes with half their stroke, cut at the SVG's floor where it clips, over 97 instants (agrees with screenshot ink to 1 px). The stage is 979 px with the headline at bottom 7: 41 px above and below, the deepest moving frames cut at 991, 3 px above the headline ink. check_animate_view's stage_clearance reads the probe and fails with the clip ignored or overflow visible."
resolution: null
duplicate_of: null
---
Canonical defect D16 from the 2026-09-14 stack triage (High). Sources: #155 R3; #171 R4.

Stage height and headline clearance are measured on geometry the SVG clips. `#packing-svg` computes to `overflow: hidden`, but `probes/stage/lowest-drawn.js` reads `getBoundingClientRect()` of every square, `#container`, `#bound-box` and `#bound-trace`, none clipped to the SVG's box. The guard built on it enforces the mismeasurement, and the 971 -> 954 (#155, a63da6cd) and 954 -> 949 (#171, 26d44ee5) shrinks rest on it.

Files: `packages/workbench/assets/workbench.css:75-84` (size cap and comment), `packages/workbench/probes/stage/lowest-drawn.js:14-21`, the guard in `check_workbench.py:3262-3272` @bb3f7c99, now `check_animate_view.py` `stage_clearance`.

Coordinator decision (triage section 5): fix the probe to measure only what the SVG draws, keep `overflow: hidden`, then take the largest stage height that gives equal space above and below the headline with the measured clearance, verified by screenshot. Feature bead: think-31ln.

## Notes

2026-09-14, coordinator decision: the 979 px height in 8fe4749e (and in the close reason above) is superseded by b7627cef, which restores the owner-approved 971 px with the headline at bottom 11: 45 px above and below, deepest moving frames cut at 983, 7 px above the headline ink. stage_clearance now requires HEADLINE_CLEARANCE = 5 px on the clipped measure; it fails with the clip ignored (998.5), with overflow: visible, and at 979 px (3 px).
