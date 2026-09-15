---
type: is
id: is-01m2hh8fgdmf1h23j7d1d9xghv
title: "PR #160 review D47: through every dwell the gap bar measures the invisible arriving square"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:20:07.948Z
updated_at: 2026-09-15T03:32:50.890Z
closed_at: 2026-09-15T03:32:50.889Z
close_reason: "Fixed on PR #160 in 8c41c8b4: the gap bar measures only the first state.liveN squares (side and overlap); check_animate_view requires n - 1's record read valid through the dwell of the steps into 17 and 26, and the stage to draw n - 1 squares there (46b8f14e)."
resolution: null
duplicate_of: null
---
Canonical defect D47 from the 2026-09-14 stack triage (Medium). Source: #125 F11.

Through every dwell the gap bar measured the invisible arriving square against n's record: the arriving square is at opacity 0 but in the pose buffers, and `gapOf` and the overlap included it. Into 17 reported side 4.6755 for n = 16 (record 4) with `valid` false, hiding the hand over a valid record. The default view since #171 opens on Animate.

Files: `packages/workbench/src/application.js` (~:3660-3663, `gapOf` ~:2297, `measureFrameGeometry` ~:3396 @bb3f7c99).
