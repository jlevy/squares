---
type: is
id: is-01m4w0c72ck6ee2gz5xd6ny4dj
title: "Regularization follow-up: unify tilt angles in tilted blocks (176, 232 and the worst residual counts)"
kind: task
status: in_progress
priority: 1
version: 10
delegate: codex-drawing-follow-up
labels:
  - stack-498-followup
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-14T01:28:06.988Z
updated_at: 2026-11-23T15:14:35.386Z
started_at: 2026-11-23T04:30:30.105Z
---
Owner, 14 Oct 2026: 'some like 176 and 232 still look irregular'. After stack 498 merges: (1) rank every count by residual irregularity in its default drawing (tilt-angle classes and hues within tilted blocks, block misalignment, isolated tilted squares); (2) build an angle-unification generator: cluster each connected tilted block's angles, snap each cluster to one angle, re-solve positions exactly at s_W or U, admit only if exactly valid on both routes and the improvement rule (policy section 11) passes; (3) run Evan Daniel's re-solve where not yet tried on the ranked counts; (4) owner decisions: symmetry, sub-block alignment and point contacts as goals; the row-7 review queue (232, 297, 154, 175). Grid-slack keeps witness rotations and the axis tool only straightens near-axis squares, so neither can fix mixed angles.

## Notes

Prototype (14 Oct, scratchpad irreg/proto/rotation_aware.py): rotation-aware re-solve of Daniel's views is exactly valid at s_W on both routes at 176 and 232 (conservative and fewest), keeping his group counts. 176: 38->8 groups, beats house and today's grid-slack drawing under the improvement rule, but decision table row 7 review (6 per-square contact counts fall). 232: valid but not an improvement (uneven 134 vs house 131); its ~10 near-equal band angles need a level-3 change. Blockers fixed: unmatched-rotation (one free 45-degree square: give unmatched groups a fresh rational, denominator >= 1e17) and literal-too-large (Python int_max_str_digits from Gaussian elimination; use LP or dilation positions, literals <= 163 digits). Small denominators do not close (room ~1e-31). Corpus estimate: ~45-80 counts hit these refusals; ~10-30 new row-10 admissions plus a similar number of row-7 reviews; measure by running the stage over a full run (< 1 CPU-hour).

Carried from #580 review C (14 Oct): C4, the process guide should say that replacing one of the seven above-U exceptions makes `layer` exit 1 until the count leaves `ABOVE_U`, policy question 13 and the atlas README. C2, `regularize_evand.reclassify`'s docstring still says "T-151 moved 60 ceilings" (the batch is T-155).

Carried from #580 review D (14 Oct): D1, extend T-155's alias sentence to the provisional ids 'T-151' and 'T-147' as well (both are main's results now).

22 Nov 2026 intake follow-up, n=232. The homepage atlas and case page currently select the axis-component fallback (270 degrees, no flip). The retained Daniel certificate exceeds the exact T-340 side by 1.576e-19. Exact contraction still exceeded it by 1.7870798633155325e-34 (binding pair 3,11). The 50-digit author pose with rationalized angles and exact uniform reboxing exceeded it by 8.24717520806e-48 (binding pair 66,76). The witness-frame conservative rerun refused for overlap; the grid variants already screened were also infeasible. A numerical fixed-angle position repair had negative clearance. The exploratory group-spin exact check was interrupted by the memory guard before a verdict. There is no admitted replacement. Keep the current view and retain this bead for a different exact same-side candidate and its per-square drawing review.

The preceding drawing audit also checked T-336 at n=305. Its exact axis fallback is in the live case and atlas (270 degrees, no reflection). The retained strong regularizer result is 1.795e-19 above U and the retained aligned variants regress on contact shading or full shared sides. Keep the fallback and include n=305 in the same-side angle-unification follow-up. Evidence: external agent-evidence/squares-intake-20261121-01a1fb/drawing-audit-20261122/audit.md and n232-exact-follow-up receipts. The new intake review and public visual checks shipped in #1095.

305 follow-up on the uneven greens reported by the owner. Verified the current live compact atlas rendering. All 212 greens are one axis angle class. Darkest to lightest, the 120, 56, 29, and 7 squares have four, three, two, and one full shared sides respectively. The overall drawing still has 32 angle classes and 63 uneven squares by the selector. Guarded exact screens of the cleaner Daniel pose: uniform contraction of the retained certificate still exceeds the registered bound by 1.83499824111e-34 (binding pair 52,99); reboxing the retained original decimal centers and 70-place rationalized half-angle tangents still exceeds it by 1.47407228650e-47 (binding pair 59,91). Both guards finished. No admitted replacement from either screen. Evidence in drawing-audit-20261122/n305-green-shades-followup on the external evidence volume. The next search needs a distinct exact same-side pose or an exact center/angle re-solve, not further uniform reboxing of these inputs.

23 November follow-up across n=127, 131, 232, 259 and 305. Live atlas SVG bytes matched the canonical renders for all five. All 691 axis-colored squares use one hue and shade follows full-side contacts. All 936 aligned shared edges remain coincident after compact SVG rounding. Live uneven axis counts were 15, 21, 112, 65 and 63 respectively.

At 305 a 100-digit nonlinear restart from the cleaner coincidence layout gave a rational certificate with padding 1e-84. It passes the two exact GMP routes plus the separate half-angle area route, and lies 5.40623344416e-81 below T-336 and 2.20196672468e-81 below T-336 shrunk to first contact. Uneven axis squares 63 -> 13, near-axis 1 -> 0. Three old per-square contacts fall, with both totals higher. This is a smaller exact result under option D and follows the house rule. The old-bound drawing-only path would need owner review. Independent review and retained integration work are in progress in codex/axis-regularization-adoption-20261123, T-342.

At 259, exact contraction of the retained cleaner T-337-based regularizer pose stops 2.02057286662e-34 above the verified side, binding pair 22 and 26. At 131 the bounded 0.05 degree frozen-tilt grid-slack pass on the published view hit its 70-second wall cap without an exact result. 232 remains on the exact fallback with its prior no-fit findings. The n127 conservative replay restored the cleaner exact certificate, independently checked, tracked for adoption as T-341 under think-4z8z. Audit, mathematical receipts, and memory-guard logs are retained on spud-ext2 under agent-evidence/squares-intake-20261121-01a1fb/drawing-audit-20261122.
