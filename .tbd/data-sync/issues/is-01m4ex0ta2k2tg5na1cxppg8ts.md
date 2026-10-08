---
type: is
id: is-01m4ex0ta2k2tg5na1cxppg8ts
title: Use shared upper lower and optimality accents in the 100-packing PDF
kind: bug
status: in_progress
priority: 2
version: 4
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T23:19:20.115Z
updated_at: 2026-10-08T23:48:59.507Z
started_at: 2026-10-08T23:21:20.843Z
---
Final actual-PDF review found that the current dated 100-packing export retains a legacy lower-only recency restriction, leaving n11 optimality neutral despite the user request for red new optimality proofs. Grid geometry does not require this restriction. Supply canonical contribution flags to both production composite modes and the shared legend, update accessible description and legacy playbook statements, add focused production-path regressions, and regenerate the current export family. Keep all Grid geometry, scientific records, schemas and the 324 layout unchanged. Delegate to the PDF lane and independently review before final validation.

## Notes

Source, docs and meaningful production regressions are independently reviewed and frozen. Both production PDF modes now receive one canonical map of independent upper, lower and optimality contributions. Six focused tests pass in 7.45 seconds, including actual PDF colors and upper-only legend/star behavior; scoped Ruff, formatting and types pass with zero findings. Canonical 100 exports remain stale: the existing exporter rebuilds both families, offers no supported 100-only family command, and uses sibling atomic partials. The PDF-only CLI reads the old SVG and cannot apply the source fix. External volume has about 50 MiB; full export and required broad pre-push validation await restored headroom. Do not overwrite the 324 footer while think-h0xi awaits the user order choice. No scientific records, schemas or Grid geometry changed.
