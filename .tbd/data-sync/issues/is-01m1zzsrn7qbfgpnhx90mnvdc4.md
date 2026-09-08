---
type: is
id: is-01m1zzsrn7qbfgpnhx90mnvdc4
title: Math fallback remains visible while enhanced fonts are loading
kind: bug
status: closed
priority: 1
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01m1zzjddp742vysds0fzm3fe8
parent_id: is-01m1zzjddp742vysds0fzm3fe8
created_at: 2026-09-08T07:47:54.663Z
updated_at: 2026-09-08T10:26:58.071Z
closed_at: 2026-09-08T10:26:58.071Z
close_reason: "Merged in Squares #128 with KPress #59/#60. Final pre-merge browser/PDF gates and post-merge Pages run 34214731528 passed. The live v0.2.4-33cd4760 page passes delayed-font checks in Chromium, Firefox, and WebKit and actual-font/metric checks on screen and in print; caption and PDF visuals reviewed. Failure paths and negative controls are covered by retained regressions. Detailed evidence is in think-z7ab; full numerical post-merge CI remains tracked by think-h31m."
resolution: null
duplicate_of: null
---
KPress components.css displays semantic MathML until KaTeX rendered stamp; font-ready wait prolongs native MathML then KaTeX transition. Suppress visual intermediate rendering only during successful JS enhancement, preserving no-JS/error fallback and accessibility. Verify slow-font/slow-JS first visible rendering through a retained browser probe.
