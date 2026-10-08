---
type: is
id: is-01m4d4bfr63y61c4zymxkrn46d
title: Fix hosted paper layout shifts under the existing CLS budget
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
hold: null
hold_until: null
created_at: 2026-10-08T06:49:00.933Z
updated_at: 2026-10-08T06:51:38.110Z
started_at: 2026-10-08T06:51:38.108Z
---
C11: At exact head 104771851b6f68c6360365995394ec920730f782, Pages run 37739211469 reports paper CLS 0.251 on mobile and 0.161 on threshold desktop, above the unchanged 0.1 guard. Diagnose and fix production initialization or layout, preserve prepared math, fonts, image reservations and strict acceptance limits, and verify the next exact-head paper and full hosted checks. Astra performs focused performance diagnosis; moderate source owner implements the bounded repair.
