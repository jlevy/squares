---
type: is
id: is-01m4p42yjaz3qj1kd5n86hsj8n
title: Regularization spikes across n, with a before/after gallery, and the end-to-end effort scope
kind: task
status: in_progress
priority: 1
version: 4
delegate: claude-code@vm
labels:
  - regularization
dependencies: []
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
hold: null
hold_until: null
created_at: 2026-10-11T18:37:31.081Z
updated_at: 2026-10-11T21:07:08.014Z
started_at: 2026-10-11T20:03:58.751Z
---
Owner 2026-10-11: run spikes to test it on various values of n and show the result; scope the effort to run it end to end, automated plus manual review.

## Notes

2026-10-11 (session_017JNnKDwL74rnktr9s8BdjP): started. Owner asked for spikes on particular counts with a before/after view of what changes, especially in the house conventions (hue by angle class, shade by full-side contacts). Gallery tool devtools/regularize_gallery.py (self-contained HTML, no JS, published as a private Artifact for the owner) on claude/busy-pascal-vgiccb. Pilot set: 5, 10, 11, 17, 26, 37, 51, 70, 101, 129, 146, 200, 261, 292, 324 (the epic's eight pilot counts plus the refused-kind controls 5, 10, 11, 17, 37, 51 and the T-146 non-one-to-one counts 129, 292). Results and run cost to follow here.

2026-10-11 (session_017JNnKDwL74rnktr9s8BdjP), spikes done. Gallery published privately for the owner: https://claude.ai/artifact/GGkxS3NBJzodZcJzaUb1qX (25 counts, source / regularized / current layer, house colours). Pilot 1 (5, 10, 11, 17, 26, 37, 51, 70, 101, 129, 146, 200, 261, 292, 324): 857 CPU-s, 670 s wall at 2 workers. Pilot 2 (66, 86, 87, 102, 126, 127, 206, 260, 267, 295): 1,598 CPU-s, 933 s wall at 3 workers. fewest at 129 and 292: 282 CPU-s. Combined decisions: admit 5 (11, 26, 66, 126, 292), candidate 11, refuse 8, unchanged 1 (324). Headline effects (house rule): 292 angle classes 24 -> 9, four-side squares 84 -> 198 (admitted, same side); 206 classes 44 -> 4, light 135 -> 26, four-side 32 -> 144 (refused row 4, though its solved side equals the verified bound exactly); 295 light 62 -> 3, four-side 101 -> 166 (refused row 7, 22 per-square counts fall); 126 classes 5 -> 2, light 26 -> 7. Candidates at 70, 102, 129, 146 are T-146's registered certificates rediscovered (1e-10 below the case records' bounds); 37, 87, 101, 200, 260 are exact packings at printed sides about 1e-14 below 14-decimal bounds. fewest: 129 loses 26 four-side squares and one-to-one identity; 292 gains 2 merges. Exact solve fails (not jammed) at 86, 127, 261. Effort scope for 1..324: about 7 CPU-h by a fit (cost ~ n^2.3, heavy solve tail: 801 s at 260), 2-3 h wall at 3-4 workers; review 30-60 gallery entries. Full write-up: docs/project/research/research-2026-10-11-regularization-state-and-approach.md (think-pwmi).
