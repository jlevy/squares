---
type: is
id: is-01m0ye7m6b87a4vpn4j99bdrys
title: "W7: glued-chunk equality rows for the fixed-cell LP"
kind: feature
status: open
priority: 1
version: 2
labels: []
dependencies:
  - type: blocks
    target: is-01m1b2ac6fw0dw674sd1tz5q7q
created_at: 2026-08-26T07:05:58.218Z
updated_at: 2026-08-31T04:47:53.039Z
---
Add optional linear equality rows that glue intra-chunk relative offsets in the fixed-angle cell LP (hard-chunk mode), plus the soft re-solve path that drops them. Small addition to the existing quench LP assembly; validate on n=5/n=10 proved controls where glued and soft optima must agree at the analytic value. See X-003 pipeline stage 2.
