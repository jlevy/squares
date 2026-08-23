---
type: is
id: is-01m0r7r9k8dcz960yqpx69vwnm
title: Profile and reduce negative-control latency
kind: bug
status: open
priority: 0
version: 3
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T21:17:17.799Z
updated_at: 2026-08-23T23:47:52.776Z
---
Profile the serial negative-control lane first, identify measured startup or duplicate-work costs, and reduce them with the smallest design that preserves exact mutation-to-failure matching. Parallelize only if a simple implementation shows a material repeated speedup and identical control ids, outcomes, restoration behavior, and output; do not require worktrees, repository copies, or a generalized lease. Acceptance: retain per-control and aggregate timings; compare at least three representative runs before/after; every serial control has the same parallel verdict if parallelism is chosen; interruption remains bounded by think-97pp's focused cooperative recovery, but this performance bead does not depend on redesigning that recovery.
