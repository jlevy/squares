---
type: is
id: is-01m4p42yjaz3qj1kd5n86hsj8n
title: Regularization spikes across n, with a before/after gallery, and the end-to-end effort scope
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
created_at: 2026-10-11T18:37:31.081Z
updated_at: 2026-10-11T21:46:14.343Z
started_at: 2026-10-11T20:03:58.751Z
---
Owner 2026-10-11: run spikes to test it on various values of n and show the result; scope the effort to run it end to end, automated plus manual review.

## Notes

2026-10-11: spikes run at n = 5, 10, 11, 17, 26, 37, 51, 70, 101, 129, 146, 200, 261, 292, 324 (+ fewest at 129, 292) in attic/regularize-runs/spike-2026-10-11 (gitignored). Reports: admitted 26, 146, 292; held (register first) 37, 70, 129; no change 5, 10, 11, 17, 51, 101, 200, 324; no view 261; refused 0. Register candidates: 17, 37, 101, 200 (exact re-solve at printed side), 70, 129, 146 (certificate). Effort: automated pass 5-7 CPU-h (about 3 h wall at 2 processes) for 1..324; exact solve 479 s, regularize 135 s, import 238 s wall over the 15 spikes. Owner gallery: https://claude.ai/artifact/5PriKHaABeT1ZG5bZ6u87g (generator in session scratchpad; to be ported into devtools.regularize_evand as a gallery subcommand in the tools layer, OR-1). Policy points raised: row 3 before rows 6/7 hides failures (70, 129 fewest); exact-solve turns as named.
