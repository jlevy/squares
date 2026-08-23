---
type: is
id: is-01m0rbwtxwgqpmmwa0r7891xfy
title: "D071: prevent inherited activity tokens from authorizing descendant writers"
kind: bug
status: closed
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:29:40.923Z
updated_at: 2026-08-23T22:51:36.120Z
closed_at: 2026-08-23T22:51:36.120Z
close_reason: "Resolved by eliminating live-worktree sabotage entirely: negctl now runs controls in a stable snapshot of current tracked and non-ignored bytes, checker children are stopped and reaped before sandbox cleanup, every gate/runner critical section uses the shared atomic activity lease, writer capabilities are stripped from descendants, and real simultaneous-acquisition plus SIGTERM/SIGKILL rehearsals cover the lifecycle. The full normal ./test.sh gate passed in 129 seconds with all 27 isolated controls, 74 reconciled defect records, three activity checks, and three isolation/crash checks."
---
Runner experiment children inherit the owner token and can currently start a second mutating runner CLI under the first lease. Top-level writers must never borrow, and experiment environments must drop capabilities.
