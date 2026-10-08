---
type: is
id: is-01m4et6dna71rz90ezeghw5nc0
title: Try a narrower poster with the last four grid segments on separate lines
kind: task
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T22:29:58.047Z
updated_at: 2026-10-08T22:30:07.763Z
started_at: 2026-10-08T22:30:07.762Z
---
Render a reviewable 324-packing PDF variant: from n=197 onward, keep each non-grid prefix left aligned and move the complete regular-grid suffix onto its own second, right-aligned physical line. Make the poster approximately as wide as the logical row starting at n=170, keeping drawing scale, half-drawing separation, clear outer margins and dimension labels. Move and fit the upper-right information block inward so its right edge follows the final drawing. Preserve the current poster in Git for comparison. Acceptance: all 324 drawings remain complete and unchanged internally; canonical segment membership is correct; grid suffixes and final information align at the right edge; text and markers do not overlap or clip; maintain the latest names-only credits and four-line closing block. Update declared layout metadata, existing regressions, measured documentation, exports and preview; independently review the actual PDF before PR validation.
