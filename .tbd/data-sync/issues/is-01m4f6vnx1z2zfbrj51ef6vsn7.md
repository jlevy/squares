---
type: is
id: is-01m4f6vnx1z2zfbrj51ef6vsn7
title: Reorder the poster information and align the final project URL
kind: task
status: in_progress
priority: 2
version: 8
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-09T02:11:17.535Z
updated_at: 2026-10-09T04:44:07.225Z
started_at: 2026-10-09T02:13:50.740Z
---
Unify all poster body typography after the unchanged 57px two-line problem definition: eight legend entries, three ordered credit lines, diagram credit, date/version, project name and address use the same 48px font family, bold weight and 1.50em normalized line height. Keep explicit blank section breaks. The project and address differ only by black instead of gray and remain plain unlinked right-aligned text. Preserve title, triangle geometry, margins, scientific records and edition pin. Regenerate and inspect the actual PDF, then finish the ready-to-merge PR.

## Notes

Completed shared typography in 7b734f8bd and final exports in 818c4c372. All 15 body lines use one Arial-first 48px/700/1.50em style and 72-unit intra-block pitch; explicit blank section breaks remain. Actual PDF XML confirms every body line embeds Arial-BoldMT at36pt,54pt pitch,108pt blank break;13gray/two final black. The last project/address pair is plain unlinked text. Actual ink ends at7280.75–7281.0, within0.25unit. Problem57px/1.50,title,7435×5270geometry and every packing card unchanged. Ten targeted cases passed by honest union after fixing a stale font-size clearance assertion; Ruff/format/BasedPyright clean. Maintained export/postflight56.76s and independent/rootactual crop review clear. Final full push currently running; PR/CI/checkpoint pending. No GitHub merge authorized.
