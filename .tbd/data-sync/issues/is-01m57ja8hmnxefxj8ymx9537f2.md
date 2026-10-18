---
type: is
id: is-01m57ja8hmnxefxj8ymx9537f2
title: "PR #665 A3: reconcile adoption regression fixtures"
kind: bug
status: in_progress
priority: 2
version: 6
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m57j9xsga57szgfah5ex2bcd
hold: null
hold_until: null
created_at: 2026-10-18T13:13:16.083Z
updated_at: 2026-10-18T21:12:57.241Z
started_at: 2026-10-18T13:13:25.542Z
---
Medium; review A https://github.com/jlevy/squares/pull/665#pullrequestreview-5562201404. tests/test_house_adoption.py:80,93,162 and poster, announcement, recent-result, grid-slack, frontier-draft and chunk-taxonomy fixtures retain displaced house assumptions. Use retained old records for old-packing behavior; update current-record expectations and replay closed-form writer in required order.

## Notes

Fixed in391fdc594 with retained old records for historical behavior, current adopted-house expectations and closed-form replay. Tiny strict rational improvements display beyond40 places. bf93722b1 also updates source-stratified chunk fixture to1779/27 and declares the synthetic tie test as a ceiling consumer. Focused batches131+21 pass; final record/pin quartet4 pass at2890be7fa. Closed linked harness child think-lrrt / b88568f9a preserves60s subprocess timeout, isolates9 pool items and guarantees sibling cleanup;69 module tests pass, including2 real-child negative controls. Exact earlier broad-run probe stall remains unproved. Full rerun/hosted shards remain pending.

Latest clean head1d20b28d7ef53846600d5d2054a8f42c9b1c83b9. Full isolated n5 gate atcd5cc5cff completes1513.52s/1800:68/69steps,18,931normal passed,1failed,55skipped,1xfailed; all18,988normal identities completed, pool21 not reached. Only failure is the real0.5s stalled-preflight control's absent PID-pair file before reap assertions; deadline receipt remains operational/unresolved.1d20b28d7 adds only its pool_heavy marker, preserving0.5s/2s,receipt checks and both reap assertions. Quiet control1pass0.97s; module135same identities=134normal/1pool,disjoint. Derived full19,009=18,987normal/22pool; fresh full collection and final broad gate pending after #676. Hooks4.79s pass, clean. Exact earlier setup delay remains unproved. No unrelated #676 PID guard duplicated. Offline PR/disposition retain failed-gate evidence; final local/hosted proof and marked reply remain required before closure.

Coordinator-authorized frontier metadata fixture correction is implemented locally after clean1d20b28d7. Only packing/tests/test_validation_cli.py changes: preserve success/corpus assertions, accept only exact single-frontier-step heartbeat grammar (including valid starting/completed reporter states), and reject other stderr. One pure rejection-control test covers quiet/legitimate heartbeat streams and unrelated, malformed, wrong-count/step, failed-step, blank-line and unterminated diagnostics. git diff --check passes; manual diff inspected. No tests/lint/hooks/commit yet: all execution waits for root to release testing slot after #676. No production limits, markers, source data or GitHub state changed.
