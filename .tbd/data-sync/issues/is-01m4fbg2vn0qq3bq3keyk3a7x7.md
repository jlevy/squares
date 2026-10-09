---
type: is
id: is-01m4fbg2vn0qq3bq3keyk3a7x7
title: Make scoped atlas refresh leave files unchanged on refusal
kind: bug
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T03:32:20.443Z
updated_at: 2026-10-09T03:32:34.218Z
started_at: 2026-10-09T03:32:34.205Z
---
The final senior review found that update_selected writes the complete composite figure before rejecting unselected record changes or a failed selected build. Stage the figure and selected outputs in memory, validate everything before publication, and add meaningful regressions proving refused refreshes leave all retained files unchanged. Preserve the current scientific records and publication data pin.
