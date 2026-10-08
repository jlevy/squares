---
type: is
id: is-01m4eem8ymx3yrp7jezjypkv85
title: Mark regular-grid thresholds and separate triangle row groups
kind: task
status: in_progress
priority: 2
version: 6
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T19:07:49.075Z
updated_at: 2026-10-08T20:55:31.763Z
started_at: 2026-10-08T19:09:38.751Z
---
Identify the first regular axis-aligned grid among the current best-known packings in each square-bound row. Model each row as explicit non-grid and grid segments, derived from retained construction facts, rather than assuming a universal square-minus-side formula. On wide renderings, place both segments side by side with an extra gap equal to half a packing drawing width. If a row cannot fit, move its whole grid segment to a separate right-aligned row; wrapped grid lines also align right while non-grid lines align left. Mark the first grid count n. Apply to both the website Triangle view and the 1–324 PDF, as confirmed by the user. Preserve drawing scale, clean typography and compatibility with cropped renderings. Refresh exports and focused layout checks.

## Notes

Canonical thresholds remain 1,2,6,12,20,30,42,56,72,90,111,133,157,183,212,242,274,308. Explicit segments are implemented in both views, with half-drawing inline and vertical gaps and right-aligned narrow grid rows. Latest request replaces GRID plus threshold count with dimension labels such as 9×9 grid, derived from square-bound row9, while retaining each packing n and source threshold metadata.
