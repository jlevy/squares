---
type: is
id: is-01m0rbwsmtzm17qhrpjqcm66bg
title: "D068: eliminate live negative-control recovery takeover"
kind: bug
status: closed
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:29:39.609Z
updated_at: 2026-08-23T22:51:36.096Z
closed_at: 2026-08-23T22:51:36.096Z
close_reason: "Resolved by eliminating live-worktree sabotage entirely: negctl now runs controls in a stable snapshot of current tracked and non-ignored bytes, checker children are stopped and reaped before sandbox cleanup, every gate/runner critical section uses the shared atomic activity lease, writer capabilities are stripped from descendants, and real simultaneous-acquisition plus SIGTERM/SIGKILL rehearsals cover the lifecycle. The full normal ./test.sh gate passed in 129 seconds with all 27 isolated controls, 74 reconciled defect records, three activity checks, and three isolation/crash checks."
---
A second negctl or explicit recovery can currently restore and delete a transaction whose owner is still running. Remove live-worktree transactions by isolating controls, and retain an executable refusal regression.
