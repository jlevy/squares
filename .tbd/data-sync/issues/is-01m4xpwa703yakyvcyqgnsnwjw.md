---
type: is
id: is-01m4xpwa703yakyvcyqgnsnwjw
title: "Validate: Fang's six rectangles (R, R' and four more) in both dimensions on a maintained rectangle-container route (<1 CPU-min once written; needs W7 code)"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wv278cdppm9155311gb6y5
created_at: 2026-10-14T17:20:37.600Z
updated_at: 2026-10-14T17:20:37.600Z
---
Validation part of think-0esw (Kevin Fang's Theorems 1 and 2, T-178 in the 14 October records PR #602; tracked in jlevy/squares#603): the premises of Lemma 3 on a maintained route. Gated on code, not on budget.

## Validation
- Claim: the six rectangle certificates of rectangles/ at TheSnakeFang/squarepack-certs 078789a are valid in both dimensions: R = r17x16_n0257 (257 squares in (17 - d) x (16 - d), d >= 7.436e-4), R' = r22x21_n0443 (443 squares, d >= 0.0094), and r18x17_n0290, r19x18_n0325, r21x20_n0401, r22x21_n0442 (digests in the packet README's table; retained under source/rectangles/).
- Run: a first-party rectangle-container route (an `n W H` container) for devtools.upper_bound_reports or a sibling reader, both routes, with duplicate-square and outside-container controls, over packing/resources/web/fang-excess-theorem-2026-10-13/source/rectangles/. No first-party checker reads an `n W H` container today, and Daniel's checker reads only the width.
- Cost: under 1 CPU-min for all six once written (packet README). The 14 October review decided all six in both dimensions with its own bucketed and all-pairs programs (checks 4-6: all strict-valid, controls refused; 32,896 and 97,903 pairs for R and R'), which is review evidence, not a maintained route.
- Budget status (owner, 2026-10-14): runnable (<= 40 CPU-h) once the route exists.
- Possible <= 40 CPU-h subset: n/a.
- Depends on: the rectangle route, a W7 code slice with its own review (no bead owns it yet).
- Done when: all six pass both routes at their exact width and height with the controls refused, the receipt is kept in the packet, and T-178's evidence names it; noted on think-0esw.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. Seconds.
