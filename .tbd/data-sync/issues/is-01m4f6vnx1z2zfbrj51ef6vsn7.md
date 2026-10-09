---
type: is
id: is-01m4f6vnx1z2zfbrj51ef6vsn7
title: Reorder the poster information and align the final project URL
kind: task
status: in_progress
priority: 2
version: 7
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T02:11:17.535Z
updated_at: 2026-10-09T04:20:36.971Z
started_at: 2026-10-09T02:13:50.740Z
---
Unify all poster body typography after the unchanged 57px two-line problem definition: eight legend entries, three ordered credit lines, diagram credit, date/version, project name and address use the same 48px font family, bold weight and 1.50em normalized line height. Keep explicit blank section breaks. The project and address differ only by black instead of gray and remain plain unlinked right-aligned text. Preserve title, triangle geometry, margins, scientific records and edition pin. Regenerate and inspect the actual PDF, then finish the ready-to-merge PR.

## Notes

Latest human correction supersedes the a7accd24 typography: its legend1.60em/closing1.75em and special regular400 Arial-first project/address remain inconsistent. Replace separate settings with one shared48px/body700/1.50em style (72px intra-block advance), preserving explicit blank section breaks and57px/1.50em problem type. Root deliberately interrupted obsolete full --push a7accd24 after the correction (exit130), verified parent and isolated pytest process group reaped; no green gate claim. atlas_pdf owns source/tests/regeneration/actual QA; atlas_web owns two docs/preview-copy/draft; atlas_review independently checks final requirement. New full pre-push/current-head publication checks are required. No GitHub merge authorized.
