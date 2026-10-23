---
type: is
id: is-01m5kperf5ps0wf10syemhyaqb
title: "PR #742 A2: beyond_horizon_replay.source_history has no test"
kind: bug
status: closed
priority: 2
version: 3
delegate: c-addr-742-1023
labels: []
dependencies: []
parent_id: is-01m5kpejtm3fmbx0sb888yj3t4
hold: null
hold_until: null
created_at: 2026-10-23T06:16:30.949Z
updated_at: 2026-10-23T07:42:22.580Z
started_at: 2026-10-23T06:16:59.141Z
closed_at: 2026-10-23T07:42:22.580Z
close_reason: "fixed in a1c3b0bed: tmp_path git fixture tests for source_history (first publication across a rename, lower side, out-of-band files unread; header, manifest path/digest/bound, count-set and two-file refusals). Reply: https://github.com/jlevy/squares/pull/742#issuecomment-6360024272"
resolution: null
duplicate_of: null
---
Medium, review A of PR #742 (https://github.com/jlevy/squares/pull/742#issuecomment-6358224906). packing/devtools/beyond_horizon_replay.py:2803-2915. Add a tmp_path git fixture test: first publication across renames, header/path guard, manifest guard, in-band filter.
