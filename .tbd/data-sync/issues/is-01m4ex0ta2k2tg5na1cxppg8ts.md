---
type: is
id: is-01m4ex0ta2k2tg5na1cxppg8ts
title: Use shared upper lower and optimality accents in the 100-packing PDF
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
created_at: 2026-10-08T23:19:20.115Z
updated_at: 2026-10-08T23:37:43.520Z
started_at: 2026-10-08T23:21:20.843Z
---
Final actual-PDF review found that the current dated 100-packing export retains a legacy lower-only recency restriction, leaving n11 optimality neutral despite the user request for red new optimality proofs. Grid geometry does not require this restriction. Supply canonical contribution flags to both production composite modes and the shared legend, update accessible description and legacy playbook statements, add focused production-path regressions, and regenerate the current export family. Keep all Grid geometry, scientific records, schemas and the 324 layout unchanged. Delegate to the PDF lane and independently review before final validation.

## Notes

Source, documentation and regressions are frozen and independently reviewed clear. Legacy lower-only restriction removed for the current100GridPDF; both production modes use one contribution map for independent upper/lower/optimality marks and star legend counts. Three red checks confirmed the old failure. ENOSPC initially prevented even a tiny TMPDIR; root safely removed only inactive task caches/fixture while preserving unique evidence and restored tiny allocation. Six bounded focused checks now pass; scoped lint found a new bool-parameter signature issue, being corrected and rerun. No export/scientific record/schema changes; 100asset/alias refresh follows green verification and sufficient bounded allocation. Full pre-push gate remains blocked pending externalspace.
