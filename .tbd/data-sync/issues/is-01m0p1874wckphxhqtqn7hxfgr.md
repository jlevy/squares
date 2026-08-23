---
type: is
id: is-01m0p1874wckphxhqtqn7hxfgr
title: LP-in-cell refinement stage (R-2/H-2)
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0nym4keyvqar7my3z1vxh9m
parent_id: is-01m0nym0701fv1qq9fbqq9qz0w
created_at: 2026-08-23T00:45:10.668Z
updated_at: 2026-08-23T00:45:13.882Z
---
For fixed angles and a fixed per-pair axis choice, min s is a LINEAR PROGRAM -- verified numerically in review-2026-08-23: a 1,056-constraint LP at Trump's angles reproduces s(11) to solver precision and all centres to 9e-16. Build the polish loop: per-cell LP alternating with local angle moves; the active set gives the angle-space gradient. Output is rational per cell. Untested part: the loop and cell-boundary behaviour (H-2's kill criteria).
