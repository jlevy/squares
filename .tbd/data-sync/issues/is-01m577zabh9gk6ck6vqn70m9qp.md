---
type: is
id: is-01m577zabh9gk6ck6vqn70m9qp
title: "PR671 A3: restore hosted overview page-size budgets"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m573m7c33z407xbx74ytf0jt
hold: null
hold_until: null
created_at: 2026-10-18T10:12:31.728Z
updated_at: 2026-10-18T10:12:50.999Z
started_at: 2026-10-18T10:12:50.998Z
---
Own the A3 hosted page-size failure at PR #671 head 1b2cf7cfe15c4eec90d447bf3977a683d96dec1d: results.html 1,141,207 bytes exceeds 1,100,000 and result/t-174.html 305,917 exceeds 300,000. Scope is site rendering/budget surface with evidence, no frontier or release records, local commit only for coordinator integration. Separate external checkout squares-671-pages-20261018; reduce accidental repetition where possible and preserve content/accessibility.
