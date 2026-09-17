---
type: is
id: is-01m2pgxgakm0tfz0dce8cnmmf9
title: Two agent threads mutated the same PR worktree concurrently
kind: bug
status: open
priority: 2
version: 1
labels:
  - process
  - focus-process
dependencies: []
created_at: 2026-09-17T01:50:20.498Z
updated_at: 2026-09-17T01:50:20.498Z
---
On 2026-09-16 two Codex threads worked in /private/tmp/squares-ci-topology-reconcile (PR #188) at the same time: a crash-recovery continuation and the older #188/workbench thread. Each read the other's uncommitted edits as corruption. The recovery thread lowered SNAPSHOT_MAX_BYTES to 160 MiB and committed cb705c67; the other amended it to 27a53a8a with 192 MiB restored, then the first re-applied 160 uncommitted. One pre-push gate was stopped after nine minutes because its source changed mid-run, and the surviving gate certified the reverted cap. Both threads stopped at about 22:17Z with the conflict unresolved. The gate marker only guards validator runs; nothing prevents a second agent from editing, committing or amending a worktree another agent owns. Decide on an ownership guard (e.g. a worktree owner marker checked before commit/amend, or a rule that recovery always uses a fresh worktree) and record it in operating-rules.md or tooling.
