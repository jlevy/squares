---
type: is
id: is-01m5mg0a0fy7p6y69xxz9fbx2g
title: "census --control: the axis tolerance is a constant (AXIS_ROUNDING 1e-9); derive it from the sweep's enclosure (F-1 of the 14 October review)"
kind: task
status: open
priority: 2
version: 4
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T13:43:00.366Z
updated_at: 2026-11-03T05:51:05.514Z
---
The census control's axis check (`packing/devtools/sqverify_fast_census.py`, `AXIS_ROUNDING = 1/10^9` and the axis branch of `refusal_record`) requires the 99/100 mutant's exact capture at the vertex sweep's least vertex to lie within a constant 1e-9 of the sweep's certified lower bound. The gap is half the sweep's enclosure width, which varies by certificate, so a sound refusal can fail closed.

Evidence of 23 October (c-lower-1023, branch claude/intake-2026-10-23-lower-bounds, commit 37ba3479d): `mixed_n26_L5555` (T-233) wrote CONTROL_FAILED. The 99/100 mutant was refused at all 2,073 directions; the 2,072 oblique refusals pass every predicate; at r = 0 the mutant's exact capture 0.99098078325 (below 1, pose (3499236353508641/10^15, 1011/200), in the per-bin domain) sits 3.28e-9 above the sweep's certified bound 0.99098077996, beyond 1e-9, so `captures_agree` is false. Receipt: packing/benchmarks/measure-verifier/census-mixed/wand125-fine-net-lower-bounds-446-release-2026-10-08/mixed_n26_L5555.control.json.

The same constant holds T-142 (n28, gap 2.15e-9; think-i85v, owner question on jlevy/squares#543) and T-176 (n39, 1.26e-9; think-u0av). The 14 October review (docs/project/reviews/review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md, F-1 and its section 5) states the fix: one of section 5's options 1 to 3, derive the allowance from the sweep's enclosure rather than a constant, as a change to control logic read by a reviewer (result-import.md stage 4: any other change of direction or scale is a change of control logic and needs a review).

Done when: the control logic is fixed and reviewed, the n26, n28 and n39 controls rerun or re-judged from their retained receipts end CONTROLS_REFUSED, and the n26 count of T-233 can take its replay evidence.
blocked_on: none

## Notes

2026-10-23 (c-lower-1023): the n26 receipt named above was renamed to keep it outside the receipts the census tests hold to CONTROLS_REFUSED, following mixed_n96_L997.control-failed-v1.json. Its path is now packing/benchmarks/measure-verifier/census-mixed/wand125-fine-net-lower-bounds-446-release-2026-10-08/mixed_n26_L5555.control-failed-v2.json (content unchanged; branch claude/intake-2026-10-23-lower-bounds, PR #745). When the fixed control re-judges or reruns n26 and ends CONTROLS_REFUSED, write the new receipt as mixed_n26_L5555.control.json beside it.

2026-11-02 bold-ritchie-l32 (intake lane L32, think-567s; PR #889): a second receipt now waits on this fix. T-176's mixed_n39_L66625 whole-net control (receipt kind v2) failed closed on the axis allowance alone: the 99/100 mutant refused at all 2,073 directions, 2,072 refusals passing every predicate, and at r = 0 the exact capture 0.99207... < 1 (in the domain) sits 1.26e-9 above the sweep's certified bound 0.9920712485323058, beyond AXIS_ROUNDING 1e-9 (the 14 October review's F-1 measurement). Kept as packing/benchmarks/measure-verifier/census-mixed/wand125-fine-net-n37-n39-n44-2026-10-13/mixed_n39_L66625.control-failed-v2.json; when the fixed control re-judges or reruns it and ends CONTROLS_REFUSED, write mixed_n39_L66625.control.json beside it. Its capture (VERIFIED, 881,271,470 nodes, equal to the source's log at every direction) is spent and need not rerun. Done-when should now name n26 (T-233), n39 (T-176) and n28 (T-142, not yet captured).
2026-11-03 (bold-ritchie-l34): duplicate of think-4uun for the code fix (same defect, F-1 of the 14 October review, same file and fix). The fix is PR #892 (draft, awaiting review): the axis refusal is judged against the sweep's own enclosure, recomputed and tied to the crate's bound to the bit, not AXIS_ROUNDING. n39 (T-176) reran there and ended CONTROLS_REFUSED. What this bead adds beyond think-4uun is its done-when's reruns: n26 (T-233, re-judge or rerun mixed_n26_L5555 and write mixed_n26_L5555.control.json) and n28 (T-142, think-i85v). Not closed here.
