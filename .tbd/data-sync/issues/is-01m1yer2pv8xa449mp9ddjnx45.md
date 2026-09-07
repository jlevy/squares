---
type: is
id: is-01m1yer2pv8xa449mp9ddjnx45
title: Reconcile PR111 session093 ID with landed source session093
kind: bug
status: open
priority: 2
version: 2
assignee: unassigned
labels: []
dependencies: []
created_at: 2026-09-07T17:30:39.181Z
updated_at: 2026-09-07T21:55:00.668Z
---
Read-only paginated PR111 file inventory at 2026-09-07T17:30Z includes packing/campaign/agent-sessions/session-093-atlas-expansion-to-324.md. Main from PR109 already contains session-093-full-square-compatibility.md. Preserve the landed ID; the incoming atlas session must use a freshly inventoried sequential free ID before integration. Current separate PR110 continuation owns session096. No PR111 file or branch was modified.

## Notes

Updated 2026-09-07T21:56Z live-worktree survey: preserve landed full-square093, landed Stromquist096 and existing kernel-pricing097. PR110 now reserves098 for its former residual096. PR111's remote still has atlas093, and its local merge preparation has atlas097; both collide with earlier source ownership. Its integration must freshly inventory remote refs, live worktrees and shared tbd reservations before choosing the next free ID (099 at this snapshot, not reserved here). No PR111 files changed by this task.
