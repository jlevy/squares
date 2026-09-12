---
type: is
id: is-01m29hy2bcnwej20dfv7c9ydrp
title: The workbench's visual pass of 2026-09-11
kind: chore
status: closed
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-12T00:57:59.915Z
updated_at: 2026-09-12T00:58:06.304Z
closed_at: 2026-09-12T00:58:06.303Z
close_reason: Landed across 2e808d11, 09c458da, 826ec5b2, d45d639c, 17c2bd05 and 483d4835; recorded for the reasoning rather than for the work.
resolution: null
duplicate_of: null
---
The owner's visual corrections to the bar, the headline and the PROVEN block, landed across 2026-09-11. Recorded together because they are one pass over the same surface and the reasoning is worth keeping.

**The bar.**
- Bold black rules on the two bounds, quieter grey on the reference marks; the arrows dropped, colour doing the "which bound" job (483d4835, 2e808d11).
- Spans whole integers, anchored one below the GRID bound `ceil(sqrt(n))`. At a perfect square that is the difference between the record sitting in the middle of the bar and hard against its left end: n = 36 ran 6..8, runs 5..7 (09c458da, 483d4835).
- `sqrt(n)` and `sqrt(n) + 1` are marks inside it and COLLAPSE onto the integers at a perfect square: three marks at n = 16, five at n = 26.
- Two rows of labels, decided by the kind of value rather than by collision -- the integers a unit apart on the first, the two irrationals on the second, since `sqrt(26)` is thirty pixels from the integer 5 against labels twice that wide.
- Every number one size; colour and weight say what kind it is. Ticks reach their own labels. No rounded corners: it is a number line.

**The headline.** Anchored to the diagram's floor, bold like the panel's mathematics, 37 px clear of the container where it had been 13.8 (826ec5b2, d45d639c).

**The PROVEN block.** One chained inequality rather than two lines; the star hangs in the margin so nothing is indented; "new lower bound" in the star's scarlet (17c2bd05, 483d4835).

Each of these was measured rather than eyeballed, and the numbers are in the commits. Two defects came out of the pass: a redeclared variable that broke the page, caught by the type gate, and the mode moving the stage, caught by `check_workbench`.
