---
type: is
id: is-01m68f02ycck4713n6e6pbexf6
title: "Intake PR descriptions must not use GitHub closing keywords (closes/fixes #N): #834's merge auto-closed #613 before its final comment"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: bold-ritchie-l12
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-10-31T07:50:13.196Z
updated_at: 2026-11-01T15:39:40.477Z
started_at: 2026-11-01T15:39:40.477Z
---
2026-10-31: jlevy/squares#834's body said 'closes #613'; merging it at 07:35:19Z closed #613 automatically, 14 minutes before the pass posted its final comment (issuecomment-6540803366). The runbook (stage 7, Close an Answered Issue) closes an issue only with its final comment. Fix: the create-or-update-pr shape for intake PRs should write 'answers #N' / 'records #N' instead, and a records-tier check could refuse closing keywords in intake PR bodies (if PR bodies are checkable) or the runbook should say so explicitly.
