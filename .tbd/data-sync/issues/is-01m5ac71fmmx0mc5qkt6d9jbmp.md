---
type: is
id: is-01m5ac71fmmx0mc5qkt6d9jbmp
title: Audit and safely stage inactive Squares disk artifacts on internal drive
kind: chore
status: in_progress
priority: 1
version: 2
assignee: internal-disk-reclamation
delegate: internal-disk-reclamation
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-19T15:24:22.387Z
updated_at: 2026-10-19T15:24:43.103Z
started_at: 2026-10-19T15:24:43.102Z
---
User requested thorough cleanup of disk space no longer needed from our Squares work, especially the nearly full internal drive. Audit existing metadata, all registered worktrees, and generated/temp artifacts; preserve source, unique research and logs, active environments and sessions. Trash-only staging with plan, dry-run, activity recheck and exact manifest. No whole active worktree removal or Trash emptying. Evidence: .codex/intake-resume-20261019/disk-audit-20261019 and external task scratch.
