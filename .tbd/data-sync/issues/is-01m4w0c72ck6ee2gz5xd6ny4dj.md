---
type: is
id: is-01m4w0c72ck6ee2gz5xd6ny4dj
title: "Regularization follow-up: unify tilt angles in tilted blocks (176, 232 and the worst residual counts)"
kind: task
status: open
priority: 1
version: 1
labels:
  - stack-498-followup
dependencies: []
created_at: 2026-10-14T01:28:06.988Z
updated_at: 2026-10-14T01:28:06.988Z
---
Owner, 14 Oct 2026: 'some like 176 and 232 still look irregular'. After stack 498 merges: (1) rank every count by residual irregularity in its default drawing (tilt-angle classes and hues within tilted blocks, block misalignment, isolated tilted squares); (2) build an angle-unification generator: cluster each connected tilted block's angles, snap each cluster to one angle, re-solve positions exactly at s_W or U, admit only if exactly valid on both routes and the improvement rule (policy section 11) passes; (3) run Evan Daniel's re-solve where not yet tried on the ranked counts; (4) owner decisions: symmetry, sub-block alignment and point contacts as goals; the row-7 review queue (232, 297, 154, 175). Grid-slack keeps witness rotations and the axis tool only straightens near-axis squares, so neither can fix mixed angles.
