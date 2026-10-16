---
type: is
id: is-01m50xqsa4f5tfq632b71bj3cv
title: "Regularization leftovers: grid-slack 1 and 5 deg on 102, 236, 258, 263, 269; record outcomes for 110, 123, 155, 179, 180; 39, 55, 290, 291 under think-yk2h"
kind: task
status: in_progress
priority: 1
version: 7
delegate: user-eb-reg-leftovers
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
hold: null
hold_until: null
created_at: 2026-10-15T23:18:12.547Z
updated_at: 2026-10-16T09:54:40.237Z
started_at: 2026-10-16T05:22:35.967Z
---

## Notes

2026-10-16T05:28Z user-eb-reg-leftovers: started. Branch claude/intake-2026-10-16-regularize-leftovers at e2e018f32 (main). Grid-slack at 0.5/1/5 deg running on 102 110 123 155 179 180 236 258 263 269 (run dirs laneD/runs/leftovers-deg{05,1,5}-1016, two lanes, nice 10); Evan Daniel driver (evand-regularize-leftovers-1016) next on the same ten; then selection.

2026-10-16T05:53Z user-eb-reg-leftovers: grid-slack done (runs grid-slack-leftovers-deg05-1016 / -deg1-1016 / -deg5-1016 on 102 110 123 155 179 180 236 258 263 269 270 301 305; 39 invocations, 1,613 CPU-s user+sys, 05:28-05:52Z, two lanes nice 10; timing in scratch laneD/logs/grid-timing.tsv). At 102 236 258 263 269 every threshold gives the house back (max move ~1e-19, no change). Evan Daniel driver evand-regularize-leftovers-1016 started 05:52Z on the twelve (not 301) at --workers 2. Next: regularize_select. Branch still at main e2e018f32, nothing committed.

2026-10-16T07:02Z user-eb-reg-leftovers: evand-regularize-leftovers-1016 11 of 12 done (102 258 263 269 no change; 110 123 179 row 7 refuse; 155 270 row 4 held; 180 236 row 10 admit, to be judged by the selection); 305 still in its same-side stage. Selection is chained to start when the run ends. Coordinator: lane J stacks on this branch, so the infographics cut is not mine; data commits are pushed as soon as made and never rewritten.

2026-10-16T08:01Z user-eb-reg-leftovers: runs and selection done. evand-regularize-leftovers-1016: 4,212 s wall, 2,917.2 CPU-s (receipt), 2 workers, 05:52-07:02Z; grid-slack 1,613 CPU-s; regularize_select --workers 2 at e2e018f32, 3,007 s wall (07:03-07:53Z): 0 chosen, 0 register candidates, 13 counts with no adoptable view. Per count: 102 258 263 269 no change everywhere; 236 evand +1 class/hue, grid no change; 180 all tie the axis view; 123 evand row 7, grid ties; 155 evand row 4 (9.9e-31 above U), grid worse on light/uneven; 179 all row 7 (stage falls); 110 all row 7 (fewer sides). SETTLED rewritten on the four new runs with per-count outcomes, every owed dropped; README paragraph; guide sentence; test updated; record regenerated; --check-state and test_default_drawings/test_bead_tree pass (uncommitted, waiting to stack on lane B's push, per brief).

2026-10-16T09:54Z user-eb-reg-leftovers: INTERIM. Data commit prepared LOCALLY (not pushed) on #644's branch 780d81b82: 7fb79b461 (SETTLED per-count outcomes on the four 16 Oct runs, no owed left; README paragraph; guide; test; record regenerated; --check-state and test_default_drawings/test_bead_tree pass there). Waiting for lane B's 3b/3c push to rebase onto it, then re-pin, release-impact record, validate, push, PR. Evidence tarball laneD/evidence/leftovers-1016-runs.tar.gz (sha256 6142cb07...13dc4e). Audit bead think-drze opened and claimed.
