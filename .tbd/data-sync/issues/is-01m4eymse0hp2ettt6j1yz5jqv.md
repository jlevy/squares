---
type: is
id: is-01m4eymse0hp2ettt6j1yz5jqv
title: Reconcile the concurrent 324 poster footer before final publication
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: blocked
hold_until: null
created_at: 2026-10-08T23:47:43.167Z
updated_at: 2026-10-08T23:48:59.867Z
started_at: 2026-10-08T23:47:51.818Z
---
A separate chat changed the same poster after the reviewed export: Citations, URL, Diagram, version became Diagram, version, Citations, URL; the URL changed from 78px to 57px and black. Independent comparison proves only four SVG text nodes changed, with matching current PNG/PDF receipts and no other drawing changes. Current source and tests match the alternate footer, but README and figure playbook retain the order requested in this chat. Preserve both versions and await the pending user order choice before changing the footer, its documentation, or canonical assets. Then regenerate, visually review and refresh preview assets. This is part of the atlas cleanup epic; no other chat supplies authorization.

## Notes

Strong read-only review confirms current source, tests and all three 324 exports agree on Diagram, version, Citations, URL at 57px; SVG receipt matches PNG/PDF. Compared with the preserved reviewed SVG, only four footer text nodes changed; the URL additionally changed from 78px to 57px and from #17202a to black. All packing cards, geometry, markers, legend, names and scientific metadata are byte-identical outside these nodes. README lines 79–80 and playbook lines 388–389 and 409–411 retain the earlier requested order/78px URL. The unrelated task preserved before and prospective exports under attic/n17-merge-readiness-20261008/atlas-footer-poster-only. Pending async user choice is required before reconciliatory edits. No other-chat messaging or consent inference; preserve both versions.
