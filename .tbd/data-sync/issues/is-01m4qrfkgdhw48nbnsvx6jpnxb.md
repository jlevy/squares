---
type: is
id: is-01m4qrfkgdhw48nbnsvx6jpnxb
title: "Atlas second-press test races the move's start: wall-clock wait finds the tile moves pending"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@vm
labels:
  - bug
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T09:53:11.692Z
updated_at: 2026-10-12T09:53:19.054Z
started_at: 2026-10-12T09:53:19.054Z
---
tests/test_site_atlas_views.py::test_a_second_press_mid_move_starts_from_where_the_tiles_are failed on PR #516's frontend check (run 38228717409, job 114742577926) with assert 0 > 0 on moving_after (line 1130). Root cause: packing/tests/probes/site_atlas_views/interrupted.js waited 120 ms on setTimeout after the first press; on a loaded machine Chromium still holds the tile moves pending (startTime null, currentTime 0), so the tiles are where the grid had them, the page's FLIP finds every tile still and starts no move. Pre-existing on main (20 of 30 old-probe presses fail at load 16-23 on 4 CPUs). Fix: wait on the move's own clock (await ready, set each running move to wait ms into its course, read and press in the same task).
