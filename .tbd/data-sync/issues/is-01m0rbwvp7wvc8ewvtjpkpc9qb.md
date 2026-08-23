---
type: is
id: is-01m0rbwvp7wvc8ewvtjpkpc9qb
title: "D073: remove target alias and snapshot overwrite hazards from negative controls"
kind: bug
status: closed
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:29:41.702Z
updated_at: 2026-08-23T22:51:36.134Z
closed_at: 2026-08-23T22:51:36.134Z
close_reason: "Resolved by eliminating live-worktree sabotage entirely: negctl now runs controls in a stable snapshot of current tracked and non-ignored bytes, checker children are stopped and reaped before sandbox cleanup, every gate/runner critical section uses the shared atomic activity lease, writer capabilities are stripped from descendants, and real simultaneous-acquisition plus SIGTERM/SIGKILL rehearsals cover the lifecycle. The full normal ./test.sh gate passed in 129 seconds with all 27 isolated controls, 74 reconciled defect records, three activity checks, and three isolation/crash checks."
---
Resolved target paths defeat the symlink guard, and the read-read-replace sequence can overwrite an unrelated edit. An isolated current-worktree snapshot should make the live target unreachable and preserve exact test inputs.
