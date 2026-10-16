---
type: is
id: is-01m50xqsa4f5tfq632b71bj3cv
title: "Regularization leftovers: grid-slack 1 and 5 deg on 102, 236, 258, 263, 269; record outcomes for 110, 123, 155, 179, 180; 39, 55, 290, 291 under think-yk2h"
kind: task
status: in_progress
priority: 1
version: 5
delegate: user-eb-reg-leftovers
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
hold: null
hold_until: null
created_at: 2026-10-15T23:18:12.547Z
updated_at: 2026-10-16T07:02:18.674Z
started_at: 2026-10-16T05:22:35.967Z
---

## Notes

2026-10-16T05:28Z user-eb-reg-leftovers: started. Branch claude/intake-2026-10-16-regularize-leftovers at e2e018f32 (main). Grid-slack at 0.5/1/5 deg running on 102 110 123 155 179 180 236 258 263 269 (run dirs laneD/runs/leftovers-deg{05,1,5}-1016, two lanes, nice 10); Evan Daniel driver (evand-regularize-leftovers-1016) next on the same ten; then selection.

2026-10-16T05:53Z user-eb-reg-leftovers: grid-slack done (runs grid-slack-leftovers-deg05-1016 / -deg1-1016 / -deg5-1016 on 102 110 123 155 179 180 236 258 263 269 270 301 305; 39 invocations, 1,613 CPU-s user+sys, 05:28-05:52Z, two lanes nice 10; timing in scratch laneD/logs/grid-timing.tsv). At 102 236 258 263 269 every threshold gives the house back (max move ~1e-19, no change). Evan Daniel driver evand-regularize-leftovers-1016 started 05:52Z on the twelve (not 301) at --workers 2. Next: regularize_select. Branch still at main e2e018f32, nothing committed.

2026-10-16T07:02Z user-eb-reg-leftovers: evand-regularize-leftovers-1016 11 of 12 done (102 258 263 269 no change; 110 123 179 row 7 refuse; 155 270 row 4 held; 180 236 row 10 admit, to be judged by the selection); 305 still in its same-side stage. Selection is chained to start when the run ends. Coordinator: lane J stacks on this branch, so the infographics cut is not mine; data commits are pushed as soon as made and never rewritten.
