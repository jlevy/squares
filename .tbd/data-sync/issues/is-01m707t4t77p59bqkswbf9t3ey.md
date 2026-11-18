---
type: is
id: is-01m707t4t77p59bqkswbf9t3ey
title: Decide/register the held Daniel-regularizer KKT points 3.30-3.53e-12 below T-275..T-279 (232, 268, 299, 303, 307)
kind: task
status: open
priority: 3
version: 4
labels:
  - result-import
dependencies: []
hold: blocked
hold_until: null
created_at: 2026-11-09T13:26:24.838Z
updated_at: 2026-11-18T08:46:41.605Z
---
From L63 (#932): Evan Daniel's regularizer reached certified KKT points 3.37e-12 (232), 3.30e-12 (268), 3.53e-12 (299), 3.48e-12 (303), 3.48e-12 (307) below each new house; held as candidates in the think-463r-2026-11-09 regularization README, not registered. These gains are of the same size as the robust-rational promotion padding (L65 measured a uniform contraction of #929/#930 at ~3.40e-12), so whether they are new results at all is the owner's open RV-3 question (think-ruu2, think-ikku). Wait for that answer before registering.

## Notes

2026-11-09 coordinator: waits on the owner's RV-3 answer (whether a gain inside the predecessor's rounding-padding contraction margin is a new result), carried by think-ruu2 and think-ikku; think-463r only produced these candidates.
blocked_on: think-ruu2, think-ikku

2026-11-17 coord-intake-1117: OWNER DECIDED (think-b0w5): "Only if it beats the gap-free original (Recommended)" = option D at every count: a re-certification is a new result only if its side is below its predecessor shrunk to first contact (devtools.contraction_margin); else a restatement credited to the original finder. Apply and close.

2026-11-18T08:46Z w7r2-optd-1118 (think-8yyy, #1030 review A5): option D applied to the five held points (cases/regularized_drawings/think-463r-2026-11-09/README.md, 'The Held Points Under Option D'): 232 is 1.1251 of T-275's margin and 268 1.0321 of T-276's (receipts option-d/contraction-n232-t275.json, contraction-n268-t276.json; both routes accept), new against those houses but 1.88e-3 above T-307 and 6.02e-4 above T-320, so no candidate; 303 1.0234 of T-278's, below the house: candidate; 299 and 307 the points 6.20e-15 and 1.34e-15 below T-325/T-326: candidates, credit by think-frl5. Candidates' registration is think-4z8z's. tests/test_restatements.py holds 232/268/303. Close after #1030 merges (--before-close).
