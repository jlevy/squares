---
type: is
id: is-01m4zadqmvec406fz3m5p3bvk9
title: Unify News and Explanations article headings with original publication dates
kind: feature
status: closed
priority: 1
version: 4
delegate: codex@spud10.local
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-15T08:21:25.778Z
updated_at: 2026-10-15T11:15:51.112Z
started_at: 2026-10-15T08:22:02.556Z
closed_at: 2026-10-15T11:15:51.112Z
close_reason: Delivered and reviewed in PR617, merge f97bc0b199e2493b0d84ba51f512e2b406b73021. Pages run38722914631 and full main Packing38722914629 succeeded; hosted verify-deployment succeeded10:59:54UTC. Live index/news/papers HTTP200 v0.7.5 smoke retained in news-live-v075-smoke.json. Includes shared article headers/original dates, compact filters/topics/meters, site fonts, concurrent adoption news and bookmark oracle.
resolution: null
duplicate_of: null
---
Use the existing Explanations paper-title design for News headings. Shared article heading structure: optional eyebrow, title, prominent date, optional tags. Explanations papers also display authoritative original publication dates, independent of latest edition date. Preserve links, component histories, tutorial sections and News metadata. Delegate markup/date implementation and coordinate shared stylesheet edits; review and verify rendered headings on desktop and mobile.

## Notes

Shared article_header implemented on focused895637 for News and Explanations using existing paper-title typography, optional eyebrow/title/prominent original date/metadata. Dates use earliest retained paper editions; basic tutorial original deployment Oct1 and advanced Oct14 verified against GitHub deployment receipts. New regression prevents a future edition from changing original date. Native desktop/mobile preview issues[] and66focused tests pass. Design guide updated. Final prepush/review/PR/deploy pending; no claim live yet.
