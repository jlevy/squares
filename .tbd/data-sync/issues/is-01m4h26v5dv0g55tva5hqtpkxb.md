---
type: is
id: is-01m4h26v5dv0g55tva5hqtpkxb
title: Apply final PDF black typography, single-line grid markers, and measured tighter spacing
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T19:28:29.355Z
updated_at: 2026-10-09T19:46:20.443Z
started_at: 2026-10-09T19:28:49.335Z
---
User October 9 clarification supersedes pending row-direction question: make title and problem subtitle black, increase problem subtitle 10% from current 60-unit triangle size (grid proportional), rotate single-line k×k GRID marker and place left of first grid box with clearance comparable to normal horizontal inter-box gap. Reduce actual horizontal box-to-box gaps by about 20% and vertical clearance from last annotation text below one box to next row box by about 40%, systematically for both 324 Triangle and 100 Grid PDFs. Preserve full rows, separator distinction, shared legend/credits styling, no PDF scaling. Measure rendered ink clearances and visually verify both; regenerate canonical release after integration.

## Notes

Latest user refinement: grid labels should move slightly closer; marker-specific clearance is 90% of normal stroke-edge box gap (49.365 vs54.85 units), preserving214-column/307-row pitches. Latest PDFs are being refreshed. Geometry/style accepted independently; print release waits on lossless SVG budget fix think-9v51 and main integration think-4iv5.
