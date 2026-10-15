---
type: is
id: is-01m4zadqmvec406fz3m5p3bvk9
title: Unify News and Explanations article headings with original publication dates
kind: feature
status: in_progress
priority: 1
version: 3
delegate: codex@spud10.local
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-15T08:21:25.778Z
updated_at: 2026-10-15T09:11:48.271Z
started_at: 2026-10-15T08:22:02.556Z
---
Use the existing Explanations paper-title design for News headings. Shared article heading structure: optional eyebrow, title, prominent date, optional tags. Explanations papers also display authoritative original publication dates, independent of latest edition date. Preserve links, component histories, tutorial sections and News metadata. Delegate markup/date implementation and coordinate shared stylesheet edits; review and verify rendered headings on desktop and mobile.

## Notes

Shared article_header implemented on focused895637 for News and Explanations using existing paper-title typography, optional eyebrow/title/prominent original date/metadata. Dates use earliest retained paper editions; basic tutorial original deployment Oct1 and advanced Oct14 verified against GitHub deployment receipts. New regression prevents a future edition from changing original date. Native desktop/mobile preview issues[] and66focused tests pass. Design guide updated. Final prepush/review/PR/deploy pending; no claim live yet.
