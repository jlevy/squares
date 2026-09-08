---
type: is
id: is-01m1tcw4q98vj6rme1bbatbg2a
title: Exclude retained fractional solver state from mutation-control snapshots
kind: bug
status: closed
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m1t71c4hyfw28d5nc5m6jv6b
hold: null
hold_until: null
created_at: 2026-09-06T03:40:57.448Z
updated_at: 2026-09-06T03:54:53.172Z
started_at: 2026-09-06T03:41:04.990Z
closed_at: 2026-09-06T03:54:53.170Z
close_reason: "Commit 15514b50 prunes only retained BC-200 state/family and Agenda 024-026 evidence roots while preserving linked and registered dependencies. Four focused tests passed locally; hosted run 34009724046 passed the snapshot test and failed only on two separately tracked per-test duration ceilings (think-anw1). Measured snapshot: 64,318,020 bytes, 2,790,844 below the fixed 64 MiB cap."
resolution: null
duplicate_of: null
---
PR #89 CI run 34009208360 failed because snapshot_source_bytes reached 67,129,316 bytes, 20,452 above the 64 MiB portable cap. BC-200 retained state/family and live Agenda 024-026 result roots are evidence, not mutation targets. Add evidence-based prunes, retain linked/registered dependencies through the existing copy-back rules, and run the focused snapshot/control tests before rerunning CI.
