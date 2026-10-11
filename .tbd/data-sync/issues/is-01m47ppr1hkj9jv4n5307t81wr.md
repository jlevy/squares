---
type: is
id: is-01m47ppr1hkj9jv4n5307t81wr
title: "audit_wand125_declared_net rectangle_block: bound each enclosure's width, not containment alone (DR-7)"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m47hea1vkqx8h5wzdzcyqs5k
created_at: 2026-10-06T04:14:17.649Z
updated_at: 2026-10-06T04:14:17.649Z
---
DR-7 of docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md (note, source-checker route only). devtools/audit_wand125_declared_net.py rectangle_block requires each input line's ten hexadecimal ends to contain the image's exact coordinates and density, but bounds no enclosure's width: a line with very wide enclosures passes. Fix: require each end to be within a few units in the last place of the exact value, or its directed binary64 rounding, as an input generated from the exact candidate would be. Does not affect the sqverify-fast census route.
