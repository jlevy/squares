---
type: is
id: is-01m1qjfcmb6rh95ssx4xh55hkz
title: "Certificate page: K-net buttons scoped to the figure copy, not the removed article"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1qgrj2q8kmrbqrgvkaksn87
created_at: 2026-09-05T01:21:07.722Z
updated_at: 2026-09-05T01:21:55.576Z
closed_at: 2026-09-05T01:21:55.575Z
close_reason: Commit 77c441c4, verified in the browser.
resolution: null
duplicate_of: null
---
Two console errors after the single-body change: the per-certificate script scoped .knet to #cert-{{SLUG}}, which no longer exists; scope to .cert-figure[data-cert].
