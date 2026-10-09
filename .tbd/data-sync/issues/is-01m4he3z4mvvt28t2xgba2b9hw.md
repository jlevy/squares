---
type: is
id: is-01m4he3z4mvvt28t2xgba2b9hw
title: Repair Linux retained atlas font alias matching
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
created_at: 2026-10-09T22:56:38.034Z
updated_at: 2026-10-09T22:57:05.334Z
started_at: 2026-10-09T22:57:05.331Z
---
Hosted Packing run 38000264420 at d19d01f18 reports 16 atlas native-font failures. Retained italic metadata family is Squares Atlas Print while Cairo receives PostScript face SquaresAtlasPrint-BoldItalic; Linux Fontconfig toy selection falls back and violates retained metrics. Add process-local exact face mapping, preserve bundled fonts and fallback refusal, and qualify on Linux. Independent private worker owns atlas_print_font.py and focused atlas/composite tests; no generated artifact change intended.
