---
type: is
id: is-01m4eem8ymx3yrp7jezjypkv85
title: Mark regular-grid thresholds and separate triangle row groups
kind: task
status: closed
priority: 2
version: 8
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T19:07:49.075Z
updated_at: 2026-10-09T13:44:10.806Z
started_at: 2026-10-08T19:09:38.751Z
closed_at: 2026-10-09T13:44:10.806Z
close_reason: Implemented, independently reviewed and qualified for PR474 source 6ccbbf000f0c9b48f2985c07c9893f98fe73ba92 against main 6a0499ba4; combined tree c65da41410e89a8dedffe93d3c1e153adb05096d. Local named push 65/65 and hosted 93 fast + 13 actual deferred (106) plus Pages passed; final readiness receipts recorded.
resolution: null
duplicate_of: null
---
Identify the first regular axis-aligned grid among the current best-known packings in each square-bound row. Model each row as explicit non-grid and grid segments, derived from retained construction facts, rather than assuming a universal square-minus-side formula. On wide renderings, place both segments side by side with an extra gap equal to half a packing drawing width. If a row cannot fit, move its whole grid segment to a separate right-aligned row; wrapped grid lines also align right while non-grid lines align left. Mark the first grid count n. Apply to both the website Triangle view and the 1–324 PDF, as confirmed by the user. Preserve drawing scale, clean typography and compatibility with cropped renderings. Refresh exports and focused layout checks.

## Notes

Canonical thresholds remain 1,2,6,12,20,30,42,56,72,90,111,133,157,183,212,242,274,308. Explicit non-grid/grid segments and half-drawing gaps are implemented in both views, with right-aligned narrow grid rows. Latest user refinement stacks dimensions such as 15×15 above uppercase GRID, derived from the square-bound row; keep packing n and canonical threshold metadata separately. Website and PDF refinements proceed in parallel.
