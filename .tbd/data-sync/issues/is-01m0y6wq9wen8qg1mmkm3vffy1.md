---
type: is
id: is-01m0y6wq9wen8qg1mmkm3vffy1
title: Parse and validate native Codex turn timings
kind: task
status: closed
priority: 0
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - focus-efficiency
dependencies: []
parent_id: is-01m0y6wad9gxebve4cs7sz3jqy
created_at: 2026-08-26T04:57:40.923Z
updated_at: 2026-08-26T05:13:15.172Z
closed_at: 2026-08-26T05:13:15.170Z
close_reason: Native timing parsing, compatibility, replay filtering, compaction accounting, and cutoff tests are implemented and green.
resolution: null
duplicate_of: null
---
Add red-green fixtures for task_complete duration_ms and time_to_first_token_ms, including missing and invalid fields. Preserve exact client-reported timing separately from log-envelope reconstruction. Acceptance: focused tests prove parsing and compatibility behavior, and static checks pass.

## Notes

Completed red-green parser correction. CodexEfficiencyRollup/v2 consumes finite nonnegative task_complete.duration_ms and time_to_first_token_ms, reports coverage/distributions, reconciles reported duration to event intervals, excludes compressed legacy replay tasks when native duration and local interval differ by more than max(1s, 5%), counts current ContextCompaction items with legacy deduplication, and freezes live scans at scan start or --through. Focused suite: 8 passed.
