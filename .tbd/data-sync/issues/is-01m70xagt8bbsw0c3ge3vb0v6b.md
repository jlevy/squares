---
type: is
id: is-01m70xagt8bbsw0c3ge3vb0v6b
title: regularize_evand.current_view takes the layer index's view without checking it belongs to the current witness (stale comparison at adoption)
kind: bug
status: open
priority: 2
version: 1
labels:
  - regularization
dependencies: []
created_at: 2026-11-09T19:42:21.512Z
updated_at: 2026-11-09T19:42:21.512Z
---
From the senior review of PR #937 (finding 3). regularize_evand.current_view (regularize_evand.py ~1827) returns the layer index's view without checking it was drawn from the case's current witness. After an adoption, until the new house is layered, row 7 compares candidate views against the previous house's view, so 270 (T-283) was wrongly settled decided-no-better at first. Fix: ignore an index entry whose witness differs from the house's, or make regularize_select refuse to settle on a candidate flagged 'measured against another drawing than the tree's'. Add a test.
