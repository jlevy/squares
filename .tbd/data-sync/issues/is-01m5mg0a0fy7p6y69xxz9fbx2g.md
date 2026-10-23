---
type: is
id: is-01m5mg0a0fy7p6y69xxz9fbx2g
title: "census --control: the axis tolerance is a constant (AXIS_ROUNDING 1e-9); derive it from the sweep's enclosure (F-1 of the 14 October review)"
kind: task
status: open
priority: 2
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T13:43:00.366Z
updated_at: 2026-10-23T13:43:00.366Z
---
The census control's axis check (`packing/devtools/sqverify_fast_census.py`, `AXIS_ROUNDING = 1/10^9` and the axis branch of `refusal_record`) requires the 99/100 mutant's exact capture at the vertex sweep's least vertex to lie within a constant 1e-9 of the sweep's certified lower bound. The gap is half the sweep's enclosure width, which varies by certificate, so a sound refusal can fail closed.

Evidence of 23 October (c-lower-1023, branch claude/intake-2026-10-23-lower-bounds, commit 37ba3479d): `mixed_n26_L5555` (T-233) wrote CONTROL_FAILED. The 99/100 mutant was refused at all 2,073 directions; the 2,072 oblique refusals pass every predicate; at r = 0 the mutant's exact capture 0.99098078325 (below 1, pose (3499236353508641/10^15, 1011/200), in the per-bin domain) sits 3.28e-9 above the sweep's certified bound 0.99098077996, beyond 1e-9, so `captures_agree` is false. Receipt: packing/benchmarks/measure-verifier/census-mixed/wand125-fine-net-lower-bounds-446-release-2026-10-08/mixed_n26_L5555.control.json.

The same constant holds T-142 (n28, gap 2.15e-9; think-i85v, owner question on jlevy/squares#543) and T-176 (n39, 1.26e-9; think-u0av). The 14 October review (docs/project/reviews/review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md, F-1 and its section 5) states the fix: one of section 5's options 1 to 3, derive the allowance from the sweep's enclosure rather than a constant, as a change to control logic read by a reviewer (result-import.md stage 4: any other change of direction or scale is a change of control logic and needs a review).

Done when: the control logic is fixed and reviewed, the n26, n28 and n39 controls rerun or re-judged from their retained receipts end CONTROLS_REFUSED, and the n26 count of T-233 can take its replay evidence.
blocked_on: none
