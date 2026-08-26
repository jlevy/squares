---
type: is
id: is-01m0r7r9k8dcz960yqpx69vwnm
title: Profile and reduce negative-control latency
kind: bug
status: in_progress
priority: 0
version: 6
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - review
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T21:17:17.799Z
updated_at: 2026-08-26T06:42:51.754Z
---
Profile the serial negative-control lane first, identify measured startup or duplicate-work costs, and reduce them with the smallest design that preserves exact mutation-to-failure matching. Parallelize only if a simple implementation shows a material repeated speedup and identical control ids, outcomes, restoration behavior, and output; do not require worktrees, repository copies, or a generalized lease. Acceptance: retain per-control and aggregate timings; compare at least three representative runs before/after; every serial control has the same parallel verdict if parallelism is chosen; interruption remains bounded by think-97pp's focused cooperative recovery, but this performance bead does not depend on redesigning that recovery.

## Notes

2026-08-26 direct 62-control measurements: j1 158.54s, j2 98.17s, j4 90.19s; two workers are the full-lane efficiency knee, but job sharding is required for one-minute CI. Add per-control JSON timing, deterministic shard index/count, checked-in LPT assignment, exact union/no duplicates, and four one-worker CI shards with p95 <=45s. Preserve ordered ids, expected diagnostics, private trees, restoration, interruption, and cleanup.
