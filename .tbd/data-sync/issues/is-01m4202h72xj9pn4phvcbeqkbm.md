---
type: is
id: is-01m4202h72xj9pn4phvcbeqkbm
title: "Review: the significance stacked branch before its PR opens"
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m41d7edgm9wc99zdrkaa5ehy
created_at: 2026-10-03T23:02:34.466Z
updated_at: 2026-10-03T23:31:45.156Z
closed_at: 2026-10-03T23:31:45.156Z
close_reason: null
resolution: null
duplicate_of: null
---
Read-only strong-tier review of origin/claude/amazing-bohr-ytjim9...claude/amazing-bohr-ytjim9-significance (577ccf2cd): markup, S sort value, star placement, S3 default, legend wiring, phone card, forced colours, accessibility, the colour-token check's coverage, vacuous tests, stale numbers in paper-design.md. Findings to be fixed or answered before the stacked PR is opened.

## Notes

Done 2026-10-03: one blocking (phone card cases collapsed to 0px on 34 of 70 cards) fixed in 9897ae38c by moving S to the card's second line, with an overflow assertion that fails on the old grid. Colour-check gaps (fallbacks, nested rules, painting properties) fixed with negative controls; light ink tokens moved before the dark block; stale prose fixed; held_by covered in test_site_preview_checks. Left open: per-page token declaration, think-wviw.
