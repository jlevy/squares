---
type: is
id: is-01m2cv7zsdz2559mpr6b10kkws
title: "PR #157 review MATH-01: direct token-count paint can overflow int64"
kind: bug
status: open
priority: 2
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:38:25.452Z
updated_at: 2026-09-13T07:38:25.452Z
---
packing/src/sqpack/fractional/threshold.py:575-589 paints token counts into int64 without bounding them. Repro: two sites carrying 2**62 tokens each, threshold 2**63, weight 1. Charge headroom passes because absolute expansion mass is 1; a reachable core containing both sites then gets direct-grid charge 0 instead of 1. Fix: bound token-count intermediates separately before arithmetic, or use exact arithmetic; retain a compact overflow regression.
