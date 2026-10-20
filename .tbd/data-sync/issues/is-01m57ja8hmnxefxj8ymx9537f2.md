---
type: is
id: is-01m57ja8hmnxefxj8ymx9537f2
title: "PR #665 A3: reconcile adoption regression fixtures"
kind: bug
status: in_progress
priority: 2
version: 7
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m57j9xsga57szgfah5ex2bcd
hold: null
hold_until: null
created_at: 2026-10-18T13:13:16.083Z
updated_at: 2026-10-18T21:48:42.006Z
started_at: 2026-10-18T13:13:25.542Z
---
Medium; review A https://github.com/jlevy/squares/pull/665#pullrequestreview-5562201404. tests/test_house_adoption.py:80,93,162 and poster, announcement, recent-result, grid-slack, frontier-draft and chunk-taxonomy fixtures retain displaced house assumptions. Use retained old records for old-packing behavior; update current-record expectations and replay closed-form writer in required order.

## Notes

Fixed in391fdc594 with retained old records for historical behavior, current adopted-house expectations and closed-form replay. Tiny strict rational improvements display beyond40 places. bf93722b1 also updates source-stratified chunk fixture to1779/27 and declares the synthetic tie test as a ceiling consumer. Focused batches131+21 pass; final record/pin quartet4 pass at2890be7fa. Closed linked harness child think-lrrt / b88568f9a preserves60s subprocess timeout, isolates9 pool items and guarantees sibling cleanup;69 module tests pass, including2 real-child negative controls. Exact earlier broad-run probe stall remains unproved. Full rerun/hosted shards remain pending.

Latest clean head1d20b28d7ef53846600d5d2054a8f42c9b1c83b9. Full isolated n5 gate atcd5cc5cff completes1513.52s/1800:68/69steps,18,931normal passed,1failed,55skipped,1xfailed; all18,988normal identities completed, pool21 not reached. Only failure is the real0.5s stalled-preflight control's absent PID-pair file before reap assertions; deadline receipt remains operational/unresolved.1d20b28d7 adds only its pool_heavy marker, preserving0.5s/2s,receipt checks and both reap assertions. Quiet control1pass0.97s; module135same identities=134normal/1pool,disjoint. Derived full19,009=18,987normal/22pool; fresh full collection and final broad gate pending after #676. Hooks4.79s pass, clean. Exact earlier setup delay remains unproved. No unrelated #676 PID guard duplicated. Offline PR/disposition retain failed-gate evidence; final local/hosted proof and marked reply remain required before closure.

Coordinator-authorized frontier metadata fixture correction is implemented locally after clean1d20b28d7. Only packing/tests/test_validation_cli.py changes: preserve success/corpus assertions, accept only exact single-frontier-step heartbeat grammar (including valid starting/completed reporter states), and reject other stderr. One pure rejection-control test covers quiet/legitimate heartbeat streams and unrelated, malformed, wrong-count/step, failed-step, blank-line and unterminated diagnostics. git diff --check passes; manual diff inspected. No tests/lint/hooks/commit yet: all execution waits for root to release testing slot after #676. No production limits, markers, source data or GitHub state changed.

Coordinator released a short isolated testing/commit slot after #406. Final correction is committed locally as d6a035e30f1803a3f3636512516664e229c9882c, parent1d20b28d7ef53846600d5d2054a8f42c9b1c83b9. Only packing/tests/test_validation_cli.py changed (+35/-1); worktree clean. Exact stderr grammar accepts quiet output and complete single-frontier-step heartbeat lines (including legitimate starting/completed reporter states), rejects other text, and preserves status0 and all corpus assertions. No production limit/marker/data edits. The original successful frontier invocation with heartbeat is an established fixture mismatch; the other three readiness/budget/collection failures in the canceled full gate remain unclassified pending quiet focused diagnosis.

Targeted execution: new pure rejection control, existing frontier metadata test, and both parameterizations of existing active-heartbeat/failure-report contract all pass:4/4 in5.50s initially and4/4 in1.57s after Ruff joined two string literals. Ruff lint, Ruff format check and file-scoped BasedPyright all pass (0errors/0warnings). The two focused batches were capped120s and90s, and complete check/format/recheck interval measured21:47:00-21:47:40UTC (40s). Normal hooks with installed Flowmark and own external Python pass3.44s;4reviewed+10referenced paper titles agree. No shared packing/.venv mutation. Evidence prefix /Volumes/spud-ext1/agent-source/squares-665-review-20261018/frontier-heartbeat-1d20b28d7-20261018T2146Z contains raw pytest/JUnit/lint/format/type logs and provenance; frontier-heartbeat-commit.log records normal hooks and commit. Initial formatting-only failure is retained, followed by clean checks.

Heavy slot released to coordinator. No push, PR/GitHub mutation or broad rerun. A3 stays open until exact-new-head collection, required full --push and hosted qualification/disposition are complete. This one new pure node derives19,010 quick identities (normal18,988/pool22) from prior19,009; this is a derived expectation, not a fresh collection receipt. Preserve #661 T-195 and provisional merge-order site metadata.
