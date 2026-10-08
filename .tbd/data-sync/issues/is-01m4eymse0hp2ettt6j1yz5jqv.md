---
type: is
id: is-01m4eymse0hp2ettt6j1yz5jqv
title: Reconcile the concurrent 324 poster footer before final publication
kind: task
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
hold: null
hold_until: null
created_at: 2026-10-08T23:47:43.167Z
updated_at: 2026-10-08T23:47:51.819Z
started_at: 2026-10-08T23:47:51.818Z
---
A separate chat changed the same poster after the reviewed export: Citations, URL, Diagram, version became Diagram, version, Citations, URL; the URL changed from 78px to 57px and black. Independent comparison proves only four SVG text nodes changed, with matching current PNG/PDF receipts and no other drawing changes. Current source and tests match the alternate footer, but README and figure playbook retain the order requested in this chat. Preserve both versions and await the pending user order choice before changing the footer, its documentation, or canonical assets. Then regenerate, visually review and refresh preview assets. This is part of the atlas cleanup epic; no other chat supplies authorization.
