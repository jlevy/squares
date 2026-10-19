---
type: is
id: is-01m5adzvqf5zgn89ha5kz56sz7
title: Preserve older managed Squares worktrees for machine handoff
kind: task
status: in_progress
priority: 1
version: 2
assignee: internal-disk-reclamation
delegate: internal-disk-reclamation
labels: []
dependencies: []
parent_id: is-01m5adjbykkfkammcx2jfymx28
hold: null
hold_until: null
created_at: 2026-10-19T15:55:24.270Z
updated_at: 2026-10-19T15:55:33.186Z
started_at: 2026-10-19T15:55:33.185Z
---
Read-only point-in-time preservation of six older app-managed Squares worktrees: exact HEAD/tree, staged and unstaged binary diffs, selected small untracked source files, explicit exclusions, credential checks without printing values, and before/after race detection. Store external durable evidence; leave originals and owners untouched. Broader archival refs and issues are coordinated by parent.
