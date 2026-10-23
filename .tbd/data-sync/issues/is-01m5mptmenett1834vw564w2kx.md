---
type: is
id: is-01m5mptmenett1834vw564w2kx
title: "Regularization step: choose each drawing's rotation/flip (the 8 symmetries of the square) by a weight rule across quadrants; owner request, no PR found"
kind: task
status: open
priority: 1
version: 1
labels:
  - regularization
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T15:42:14.485Z
updated_at: 2026-10-23T15:42:14.485Z
---
Owner, 23 October 2026 (in conversation): asked whether a PR exists for 'regularization over rotations/flips based on weights across quadrants'. Search found none: no PR, issue, bead, branch or commit; the only orientation code on main is packing/devtools/atlas_orientation.py, one registered isometry (n = 211's mirror, history since 11 October), and #474 reflected n = 211 by hand. The rule (which weights, which quadrant goes where, tie-breaks) needs the owner's specification before a lane starts. It belongs with regularization: it changes no side, is tracked separately from the record's packing (pre- and post-regularization versions), and applies to every drawing.
