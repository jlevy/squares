---
type: is
id: is-01m4fbg2vn0qq3bq3keyk3a7x7
title: Make scoped atlas refresh leave files unchanged on refusal
kind: bug
status: in_progress
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T03:32:20.443Z
updated_at: 2026-10-09T03:42:50.123Z
started_at: 2026-10-09T03:32:34.205Z
---
The final senior review found that update_selected writes the complete composite figure before rejecting unselected record changes or a failed selected build. Stage the figure and selected outputs in memory, validate everything before publication, and add meaningful regressions proving refused refreshes leave all retained files unchanged. Preserve the current scientific records and publication data pin.

## Notes

Accepted fix plan: remove early full-figure publication, preflight retained manifest/source scope, complete strict selected builds, derive figure in memory, compare unselected per-entry facts without treating global identity/header totals as unselected data changes, and serialize every output before publishing. Regression snapshots cover unselected source changes, unselected figure changes, selected-build failure and serialization failure; selected-only success must preserve every unselected output. Writer owns builder/tests; strong reviewer will independently confirm. Current9c3442 PDF artifacts are unaffected by the old failure path. Final source fix and tests are in progress.
