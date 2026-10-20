---
type: is
id: is-01m4w0c72ck6ee2gz5xd6ny4dj
title: "Regularization follow-up: unify tilt angles in tilted blocks (176, 232 and the worst residual counts)"
kind: task
status: open
priority: 1
version: 5
labels:
  - stack-498-followup
dependencies: []
created_at: 2026-10-14T01:28:06.988Z
updated_at: 2026-10-14T02:54:38.016Z
---
Owner, 14 Oct 2026: 'some like 176 and 232 still look irregular'. After stack 498 merges: (1) rank every count by residual irregularity in its default drawing (tilt-angle classes and hues within tilted blocks, block misalignment, isolated tilted squares); (2) build an angle-unification generator: cluster each connected tilted block's angles, snap each cluster to one angle, re-solve positions exactly at s_W or U, admit only if exactly valid on both routes and the improvement rule (policy section 11) passes; (3) run Evan Daniel's re-solve where not yet tried on the ranked counts; (4) owner decisions: symmetry, sub-block alignment and point contacts as goals; the row-7 review queue (232, 297, 154, 175). Grid-slack keeps witness rotations and the axis tool only straightens near-axis squares, so neither can fix mixed angles.

## Notes

Prototype (14 Oct, scratchpad irreg/proto/rotation_aware.py): rotation-aware re-solve of Daniel's views is exactly valid at s_W on both routes at 176 and 232 (conservative and fewest), keeping his group counts. 176: 38->8 groups, beats house and today's grid-slack drawing under the improvement rule, but decision table row 7 review (6 per-square contact counts fall). 232: valid but not an improvement (uneven 134 vs house 131); its ~10 near-equal band angles need a level-3 change. Blockers fixed: unmatched-rotation (one free 45-degree square: give unmatched groups a fresh rational, denominator >= 1e17) and literal-too-large (Python int_max_str_digits from Gaussian elimination; use LP or dilation positions, literals <= 163 digits). Small denominators do not close (room ~1e-31). Corpus estimate: ~45-80 counts hit these refusals; ~10-30 new row-10 admissions plus a similar number of row-7 reviews; measure by running the stage over a full run (< 1 CPU-hour).

Carried from #580 review C (14 Oct): C4, the process guide should say that replacing one of the seven above-U exceptions makes `layer` exit 1 until the count leaves `ABOVE_U`, policy question 13 and the atlas README. C2, `regularize_evand.reclassify`'s docstring still says "T-151 moved 60 ceilings" (the batch is T-155).

Carried from #580 review D (14 Oct): D1, extend T-155's alias sentence to the provisional ids 'T-151' and 'T-147' as well (both are main's results now).
