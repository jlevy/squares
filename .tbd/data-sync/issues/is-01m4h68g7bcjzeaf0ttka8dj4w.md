---
type: is
id: is-01m4h68g7bcjzeaf0ttka8dj4w
title: "Quick lane over capacity: replace the temporary suite_a..d ceiling raise with a structural fix (fifth shard or lane-capacity decision)"
kind: task
status: in_progress
priority: 2
version: 4
delegate: claude-code@vm
labels:
  - ci
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-09T20:39:17.994Z
updated_at: 2026-10-09T22:05:05.308Z
started_at: 2026-10-09T20:40:50.366Z
---
Owner decision 2026-10-09: raise the quick-lane PR suite ceilings in packing/devtools/gate-budgets.yaml for the moment (branch claude/quick-lane-ceilings) and track the real fix here. The quick lane carries about 3,200-3,500 test-seconds against roughly 2,150 s of ceiling capacity (suite_a 143, suite_b 168, suite_c 168, suite_d 143); hosted walls reached about 295-308 s. Options: a fifth shard, moving unavoidably slow modules out of the PR surface on their own measurement (OR-13), or cutting per-module cost. Done when the ceilings return to a justified level with the lane fitting under them and the temporary raise is reverted. Related: think-8tq3 (suite record rebuild), think-be1s (drift rule against spread), think-p684 (owner decision on behavioural-lane capacity).

## Notes

2026-10-09: temporary ceiling raise in progress on branch claude/quick-lane-ceilings.

2026-10-09 PR #480 (cdc71e96a, CI green): suite ceilings raised to A/D 335 s, B/C 360 s (slowest 2026-10-07..09 reading of each shard pair + >=10%, rounded to 5 s) and records re-taken from 2026-10-09 readings (180.84/215.82/190.24/183.08 s; the register refuses a ceiling above 2x its record). Revert both once a fifth shard, OR-13 moves or cheaper modules fit the lane under a justified ceiling. Evidence: 1,328 readings 10-07..10-09; tier-wall medians 167/218/186/159 s; four-shard sum median 725.9 s, max 998.6 s; recorded lane cost grew 1,213.6 (10-01) -> 2,232.4 (10-08) -> 3,178.9 test-s (10-09). Ceilings exceed OR-14's 180 s outer edge; the 2x hang detector now fires at 670-720 s.
