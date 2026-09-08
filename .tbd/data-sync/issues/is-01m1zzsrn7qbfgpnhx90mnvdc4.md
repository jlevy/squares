---
type: is
id: is-01m1zzsrn7qbfgpnhx90mnvdc4
title: Math fallback remains visible while enhanced fonts are loading
kind: bug
status: in_progress
priority: 1
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01m1zzjddp742vysds0fzm3fe8
parent_id: is-01m1zzjddp742vysds0fzm3fe8
created_at: 2026-09-08T07:47:54.663Z
updated_at: 2026-09-08T08:08:24.889Z
---
KPress components.css displays semantic MathML until KaTeX rendered stamp; font-ready wait prolongs native MathML then KaTeX transition. Suppress visual intermediate rendering only during successful JS enhancement, preserving no-JS/error fallback and accessibility. Verify slow-font/slow-JS first visible rendering through a retained browser probe.
