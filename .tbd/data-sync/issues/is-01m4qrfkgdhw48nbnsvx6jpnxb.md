---
type: is
id: is-01m4qrfkgdhw48nbnsvx6jpnxb
title: "Atlas second-press test races the move's start: wall-clock wait finds the tile moves pending"
kind: bug
status: closed
priority: 1
version: 5
delegate: claude-code@vm
labels:
  - bug
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T09:53:11.692Z
updated_at: 2026-10-12T23:39:26.029Z
started_at: 2026-10-12T09:53:19.054Z
closed_at: 2026-10-12T23:39:26.028Z
close_reason: "Fixed by PR #547 (merged 2026-10-12, commits 5762e7aee and c8c479ad9 on main); #516 merged after it."
resolution: null
duplicate_of: null
---
tests/test_site_atlas_views.py::test_a_second_press_mid_move_starts_from_where_the_tiles_are failed on PR #516's frontend check (run 38228717409, job 114742577926) with assert 0 > 0 on moving_after (line 1130). Root cause: packing/tests/probes/site_atlas_views/interrupted.js waited 120 ms on setTimeout after the first press; on a loaded machine Chromium still holds the tile moves pending (startTime null, currentTime 0), so the tiles are where the grid had them, the page's FLIP finds every tile still and starts no move. Pre-existing on main (20 of 30 old-probe presses fail at load 16-23 on 4 CPUs). Fix: wait on the move's own clock (await ready, set each running move to wait ms into its course, read and press in the same task).

## Notes

Fix PR: https://github.com/jlevy/squares/pull/547 (branch claude/wizardly-meitner-wqn4x3-atlas-press-race, commit 5762e7aee). Failing PR: https://github.com/jlevy/squares/pull/516 (frontend run https://github.com/jlevy/squares/actions/runs/38228717409/job/114742577926). Diagnosis comment on #516: https://github.com/jlevy/squares/pull/516#issuecomment-6122160245. Evidence: old probe fails 20/30 on main 7847cf3d5 (19 pending, 1 move over), 10/30 on 3307bdd84 (4 pending, 6 over); new probe 0/40 on main, 0/30 on 3307bdd84. #516's stack owner ports 5762e7aee.

Review A (https://github.com/jlevy/squares/pull/547#pullrequestreview-5490054488), A1: awaiting ready left the "move over" side open under a main-thread stall longer than the move (5762e7aee's probe 6/6 fail under a 600 ms stall). Fixed in c8c479ad9: the probe seeks every move the first press started while it is still pending and reads and presses in the same task, no await; 0/60 natural presses and 0/6 under the 600 ms stall. A2: the moving assertions carry the reading as their message. #516's stack owner ports 5762e7aee and c8c479ad9.
