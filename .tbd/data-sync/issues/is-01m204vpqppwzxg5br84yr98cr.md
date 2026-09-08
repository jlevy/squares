---
type: is
id: is-01m204vpqppwzxg5br84yr98cr
title: Keep math glyphs and metrics consistent when composite font declarations are missing
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01m1zzjddp742vysds0fzm3fe8
parent_id: is-01m1zzjddp742vysds0fzm3fe8
created_at: 2026-09-08T09:16:21.102Z
updated_at: 2026-09-08T10:26:58.104Z
closed_at: 2026-09-08T10:26:58.104Z
close_reason: "Merged in Squares #128 with KPress #59/#60. Final pre-merge browser/PDF gates and post-merge Pages run 34214731528 passed. The live v0.2.4-33cd4760 page passes delayed-font checks in Chromium, Firefox, and WebKit and actual-font/metric checks on screen and in print; caption and PDF visuals reviewed. Failure paths and negative controls are covered by retained regressions. Detailed evidence is in think-z7ab; full numerical post-merge CI remains tracked by think-h31m."
resolution: null
duplicate_of: null
---
Final KPress review reproduced a failure path: when katex-text-face.css is unavailable, composite warmups return no faces, but actual stock-family loads pass and renderMathNode exposes stock KaTeX glyphs with PT Serif metrics (fraction height1.389em versus stock1.3214em). Correct readiness/selection so missing selected composite declarations yield coherent stock fonts and metrics or preserve semantic fallback. Keep failures of unused weights nonfatal. Add a focused browser regression upstream, merge its CI-green PR, then advance the Squares pin and verify Pages.
