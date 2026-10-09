---
type: is
id: is-01m4fbg2vn0qq3bq3keyk3a7x7
title: Make scoped atlas refresh leave files unchanged on refusal
kind: bug
status: in_progress
priority: 2
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T03:32:20.443Z
updated_at: 2026-10-09T04:44:06.928Z
started_at: 2026-10-09T03:32:34.205Z
---
The final senior review found that update_selected writes the complete composite figure before rejecting unselected record changes or a failed selected build. Stage the figure and selected outputs in memory, validate everything before publication, and add meaningful regressions proving refused refreshes leave all retained files unchanged. Preserve the current scientific records and publication data pin.

## Notes

Resolved in a7accd24 and independently confirmed. Scoped refresh now preflights source/corpus scope, performs strict selected builds, derives the figure in memory, compares all unselected per-entry facts, and serializes every output before the first publication write. Seven meaningful contracts pass: six refusal scenarios preserve the entire retained-byte map, while selected success preserves unselected entries and allows legitimate global header refresh. Prior review R1/P2 is fixed; scientific data pin unchanged. Existing per-file atomic publication retains its prior I/O failure/retry semantics. Final 818c4c372 carries unchanged corrected code; full push/hosted checks pending.
