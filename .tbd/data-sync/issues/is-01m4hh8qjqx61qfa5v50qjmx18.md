---
type: is
id: is-01m4hh8qjqx61qfa5v50qjmx18
title: Diagnose local atlas hover pixel sampling failure
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-09T23:51:39.861Z
updated_at: 2026-10-09T23:51:47.614Z
started_at: 2026-10-09T23:51:47.613Z
---
Final H54153ad81 full push completed957.84s exit1:65 editchecks passed; twelve site_drawing_hover cases fail at their shared screenshot fixture because sampled frame ink is(28,37,47) instead of expected(23,32,42). Hosted Fast passes. Diagnose default Small drawing geometry, antialiasing, probe sampling and baseline behavior with retained actual images. Correct only the established defect without weakening true fixed-ink/white-canvas/hover behavior, skipping tests, or broadening production tolerances. Delegate narrow repair; root commits, updates PR and repeats required qualification. Preserve failed H receipt; no GitHub merge.
