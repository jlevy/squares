---
type: is
id: is-01m4p42yjaz3qj1kd5n86hsj8n
title: Regularization spikes across n, with a before/after gallery, and the end-to-end effort scope
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - regularization
dependencies: []
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
hold: null
hold_until: null
created_at: 2026-10-11T18:37:31.081Z
updated_at: 2026-10-11T20:04:24.761Z
started_at: 2026-10-11T20:03:58.751Z
---
Owner 2026-10-11: run spikes to test it on various values of n and show the result; scope the effort to run it end to end, automated plus manual review.

## Notes

2026-10-11 (session_017JNnKDwL74rnktr9s8BdjP): started. Owner asked for spikes on particular counts with a before/after view of what changes, especially in the house conventions (hue by angle class, shade by full-side contacts). Gallery tool devtools/regularize_gallery.py (self-contained HTML, no JS, published as a private Artifact for the owner) on claude/busy-pascal-vgiccb. Pilot set: 5, 10, 11, 17, 26, 37, 51, 70, 101, 129, 146, 200, 261, 292, 324 (the epic's eight pilot counts plus the refused-kind controls 5, 10, 11, 17, 37, 51 and the T-146 non-one-to-one counts 129, 292). Results and run cost to follow here.
