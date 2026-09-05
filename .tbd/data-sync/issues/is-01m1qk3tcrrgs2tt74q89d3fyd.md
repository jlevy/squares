---
type: is
id: is-01m1qk3tcrrgs2tt74q89d3fyd
title: "Certificate page: the claim line is not kpress's claim container, which adds a marker"
kind: bug
status: closed
priority: 3
version: 2
labels:
  - explainer
  - pr-79
dependencies: []
parent_id: is-01m1qgrj2q8kmrbqrgvkaksn87
created_at: 2026-09-05T01:32:17.175Z
updated_at: 2026-09-05T01:32:20.171Z
closed_at: 2026-09-05T01:32:20.170Z
close_reason: Commit 335cbfe1.
resolution: null
duplicate_of: null
---
A spurious bullet after the conditions trailer: the ::: claim container is kpress's semantic 'claim' block, which carries its own marker and collides with the page's .claim rules. The display statement is wrapped in the page's own cert-claim class instead.
