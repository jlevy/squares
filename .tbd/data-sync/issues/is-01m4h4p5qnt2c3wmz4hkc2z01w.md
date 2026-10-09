---
type: is
id: is-01m4h4p5qnt2c3wmz4hkc2z01w
title: Project algebraic witness sides correctly for atlas web scaling
kind: bug
status: in_progress
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T20:11:48.843Z
updated_at: 2026-10-09T20:12:48.929Z
started_at: 2026-10-09T20:12:42.815Z
---
Main integration exposed atlas_enclosing_sides treating algebraic-number-field coefficient vectors as decimal strings. These lists encode exact scalar side lengths, not rectangular dimensions. Use the same witness parser and projection as the renderer for every selected witness scalar mode, add an algebraic-vector regression, rerun affected web/consumer checks. Keep mathematical records unchanged. Initial rectangle diagnosis corrected after inspecting witness schema.
