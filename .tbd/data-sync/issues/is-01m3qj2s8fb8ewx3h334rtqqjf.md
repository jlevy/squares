---
type: is
id: is-01m3qj2s8fb8ewx3h334rtqqjf
title: Expose child pytest timings and live worker progress for reachable validation
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
created_at: 2026-09-29T21:45:38.317Z
updated_at: 2026-10-06T08:34:42.571Z
closed_at: 2026-10-06T08:34:42.571Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): devtools/reachable_progress.py (session_finish receipts) and child JUnit/durations are on origin/main via PR #246 (MERGED 2026-09-30) with test_reachable_progress.py; published CI passed
resolution: null
duplicate_of: null
---
The reachable-test wrapper prevents the gate from injecting direct-pytest JUnit and duration receipts. A ten-worker broad run can stall near completion with one CPU-active worker, without enough evidence to distinguish an indivisible test from queued imbalance. Preserve exact selection, markers and assertions. Add maintained child-pytest durations/JUnit plus live start/finish receipts naming run, worker, node and source, with interrupted partial states and focused regression tests. Do not claim that changing xdist scheduling helps until matched workload evidence exists.

## Notes

Sol implementation and independent Sol review are running in the isolated validation-parity checkout while primary candidate 1afb75ca6 finishes its unchanged broad push. Retained Session 152 logs identify a 1327.87-second single atlas-composite test as one possible source of an indivisible tail; current quiet output cannot prove the active node. Keep scheduling unchanged until the new receipts support a diagnosis.

Completed instrumentation reading from the frozen primary a2b8e696cc2dce562abedcecb9456229d57a9168 push (run receipt 6085bce8a0eb46a287d2cd1a1b52cccb): ten separate normal-worker JSONL streams, a normal JUnit XML, a separate pool-main JSONL and pool JUnit XML were retained under efficiency-repaired-artifacts. Every stream binds the same source and parent run ID and reports effective PACK_JOBS and xdist worker count. All ten normal streams have session_finish; the pool stream has session_finish after the canonical atlas node. Normal pytest: 7750 passed, 9 skipped, 416.24s. Pool pytest: 1 passed, 7819 deselected, 140.99s (132.83s test call). Reachable wrapper: 559.41s; entire named push: 51/82 steps passed in 623.04s. The receipts exposed the normal-lane worker tail and the exact pool node without mutating test selection. This is one completed run; publish/CI is still pending, so keep the bead open.
