---
type: is
id: is-01m4gykr0d2fe2g4abpgffevma
title: Rotate print grid-group labels beside their drawings
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
created_at: 2026-10-09T18:25:37.797Z
updated_at: 2026-10-09T18:36:55.754Z
started_at: 2026-10-09T18:36:55.739Z
---
Rotate the print-only dimension/GRID two-line labels by90degrees and position them closer to, and clearly at the left of, each regular-grid group. Preserve the requested half-drawing gap, all case positions/drawing sizes, complete right-aligned triangle rows, Grid100 layout and absence of these labels on web. Retain legible upright-independent geometry metadata and test rotated ink bounds/clearance through actual PDF rendering. Root integrates this disjoint print request with the pending credits/subtitle changes and PR474; no scientific-record edits.
