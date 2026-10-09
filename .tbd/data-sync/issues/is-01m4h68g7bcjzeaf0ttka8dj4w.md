---
type: is
id: is-01m4h68g7bcjzeaf0ttka8dj4w
title: "Quick lane over capacity: replace the temporary suite_a..d ceiling raise with a structural fix (fifth shard or lane-capacity decision)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@vm
labels:
  - ci
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-09T20:39:17.994Z
updated_at: 2026-10-09T20:40:53.214Z
started_at: 2026-10-09T20:40:50.366Z
---
Owner decision 2026-10-09: raise the quick-lane PR suite ceilings in packing/devtools/gate-budgets.yaml for the moment (branch claude/quick-lane-ceilings) and track the real fix here. The quick lane carries about 3,200-3,500 test-seconds against roughly 2,150 s of ceiling capacity (suite_a 143, suite_b 168, suite_c 168, suite_d 143); hosted walls reached about 295-308 s. Options: a fifth shard, moving unavoidably slow modules out of the PR surface on their own measurement (OR-13), or cutting per-module cost. Done when the ceilings return to a justified level with the lane fitting under them and the temporary raise is reverted. Related: think-8tq3 (suite record rebuild), think-be1s (drift rule against spread), think-p684 (owner decision on behavioural-lane capacity).

## Notes

2026-10-09: temporary ceiling raise in progress on branch claude/quick-lane-ceilings.
