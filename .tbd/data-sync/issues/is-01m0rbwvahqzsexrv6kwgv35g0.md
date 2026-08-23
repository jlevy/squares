---
type: is
id: is-01m0rbwvahqzsexrv6kwgv35g0
title: "D072: exercise the real crash and concurrency lifecycle"
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:29:41.328Z
updated_at: 2026-08-23T22:51:36.127Z
closed_at: 2026-08-23T22:51:36.127Z
close_reason: "Resolved by eliminating live-worktree sabotage entirely: negctl now runs controls in a stable snapshot of current tracked and non-ignored bytes, checker children are stopped and reaped before sandbox cleanup, every gate/runner critical section uses the shared atomic activity lease, writer capabilities are stripped from descendants, and real simultaneous-acquisition plus SIGTERM/SIGKILL rehearsals cover the lifecycle. The full normal ./test.sh gate passed in 129 seconds with all 27 isolated controls, 74 reconciled defect records, three activity checks, and three isolation/crash checks."
---
The current crash selftest bypasses the standalone lease and checker subprocess, while the atomic control tests an already-held marker rather than simultaneous acquisition. Replace these with end-to-end process death and exactly-one-winner rehearsals.
