---
type: is
id: is-01m35fyaba20n7rs0h60s1hs94
title: Shorten the move beat to 0.4 s
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T21:21:55.049Z
updated_at: 2026-09-22T21:21:55.049Z
---
The owner (2026-09-22): 'let's change the move timing to 0.4 instead of 0.5'. DEFAULT_STEP_TIMING.move and build_candidate.TIMING both go to 0.4, so the moving span is 0.6 s (move plus the 0.2 s correction) rather than 0.7 s. n = 2..100 falls from 153.39 s to 140.01 s, all of it in the 44 matched steps; the 55 grid fills are on the static beat and do not move.
