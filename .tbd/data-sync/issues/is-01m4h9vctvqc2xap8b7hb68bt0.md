---
type: is
id: is-01m4h9vctvqc2xap8b7hb68bt0
title: "E3: close Playwright context before returning captured atlas readings"
kind: bug
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-09T21:42:02.815Z
updated_at: 2026-10-09T21:42:12.805Z
started_at: 2026-10-09T21:42:12.793Z
---
Independent senior review at b4b127c54 confirmed test-order fragility: the seen module fixture yields captured readings inside a live sync_playwright context and control_readings opens a second context. Geometry then centering selection reports12passed plus one setup error; isolated centering and default source order pass. Exit the existing context before returning collected readings and rerun the exact combined selection. No product-layout change.
