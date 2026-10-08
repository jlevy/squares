---
type: is
id: is-01m4eem8ymx3yrp7jezjypkv85
title: Mark regular-grid thresholds and separate triangle row groups
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
created_at: 2026-10-08T19:07:49.075Z
updated_at: 2026-10-08T19:09:38.751Z
started_at: 2026-10-08T19:09:38.751Z
---
Identify the first regular axis-aligned grid among the current best-known packings in each square-bound row. Annotate its packing count n and insert an extra half-packing-drawing-width gap before the regular-grid group when the row contains an irregular prefix. Preserve readable card sizes and clean left alignment. Derive thresholds from retained packing facts rather than assuming a universal n-squared-minus-n formula; update records, exports and focused layout checks as needed. Scope question pending: apply to both website Triangle view and PDF, with both recommended.
