---
type: is
id: is-01m707t4t77p59bqkswbf9t3ey
title: Decide/register the held Daniel-regularizer KKT points 3.30-3.53e-12 below T-275..T-279 (232, 268, 299, 303, 307)
kind: task
status: open
priority: 3
version: 3
labels:
  - result-import
dependencies: []
hold: blocked
hold_until: null
created_at: 2026-11-09T13:26:24.838Z
updated_at: 2026-11-17T03:07:33.647Z
---
From L63 (#932): Evan Daniel's regularizer reached certified KKT points 3.37e-12 (232), 3.30e-12 (268), 3.53e-12 (299), 3.48e-12 (303), 3.48e-12 (307) below each new house; held as candidates in the think-463r-2026-11-09 regularization README, not registered. These gains are of the same size as the robust-rational promotion padding (L65 measured a uniform contraction of #929/#930 at ~3.40e-12), so whether they are new results at all is the owner's open RV-3 question (think-ruu2, think-ikku). Wait for that answer before registering.

## Notes

2026-11-09 coordinator: waits on the owner's RV-3 answer (whether a gain inside the predecessor's rounding-padding contraction margin is a new result), carried by think-ruu2 and think-ikku; think-463r only produced these candidates.
blocked_on: think-ruu2, think-ikku

2026-11-17 coord-intake-1117: OWNER DECIDED (think-b0w5): "Only if it beats the gap-free original (Recommended)" = option D at every count: a re-certification is a new result only if its side is below its predecessor shrunk to first contact (devtools.contraction_margin); else a restatement credited to the original finder. Apply and close.
