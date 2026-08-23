---
type: is
id: is-01m0rbww0qr3daqcs4ar198z8h
title: "D074: correct premature D035 closure and gate evidence claims"
kind: bug
status: closed
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-process
dependencies: []
parent_id: is-01m0r7q3zk8x6cg4e30d149698
created_at: 2026-08-23T22:29:42.038Z
updated_at: 2026-08-23T22:51:36.141Z
closed_at: 2026-08-23T22:51:36.141Z
close_reason: "Resolved by eliminating live-worktree sabotage entirely: negctl now runs controls in a stable snapshot of current tracked and non-ignored bytes, checker children are stopped and reaped before sandbox cleanup, every gate/runner critical section uses the shared atomic activity lease, writer capabilities are stripped from descendants, and real simultaneous-acquisition plus SIGTERM/SIGKILL rehearsals cover the lifecycle. The full normal ./test.sh gate passed in 129 seconds with all 27 isolated controls, 74 reconciled defect records, three activity checks, and three isolation/crash checks."
---
Documentation currently claims full crash safety and updates a 108-second historical gate run from 24/65 to 29/67 without executing that new gate. Revert unsupported evidence and narrow closure language until end-to-end tests pass.
