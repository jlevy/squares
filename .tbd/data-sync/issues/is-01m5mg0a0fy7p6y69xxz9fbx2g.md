---
type: is
id: is-01m5mg0a0fy7p6y69xxz9fbx2g
title: "census --control: the axis tolerance is a constant (AXIS_ROUNDING 1e-9); derive it from the sweep's enclosure (F-1 of the 14 October review)"
kind: task
status: in_progress
priority: 2
version: 8
delegate: bold-ritchie-l42
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-23T13:43:00.366Z
updated_at: 2026-11-04T16:22:47.464Z
started_at: 2026-11-04T15:02:55.163Z
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
2026-11-04 (bold-ritchie-l34, review A of #892): n26's kept receipt would now pass. Under the enclosure rule the axis refusal of packing/benchmarks/measure-verifier/census-mixed/wand125-fine-net-lower-bounds-446-release-2026-10-08/mixed_n26_L5555.control-failed-v2.json holds: the walk reproduces the crate's bound 0.9909807799642721 to the bit, and the exact capture, 3.28e-9 above it, lies in the enclosure [0.9909807799642721, 0.9909807865315093] (width 6.57e-9; the upper end equals a build of d97758bb instrumented to report it). Its 2,072 oblique refusals already held, so `captures_agree` at r = 0 was the only failing clause. #892 holds this in CI (test_each_retained_axis_refusal_is_the_crates_enclosure[mixed_n26_L5555.control-failed-v2.json]); the fine-net auditor (V-audit-fine-net-receipt) accepts it re-judged too. After #892 merges, T-233's lane can rerun or re-judge it and write mixed_n26_L5555.control.json.

2026-11-04 bold-ritchie-l32 (PR #889, b3caa7d61): the n39 (T-176) part of the done-when is met on the branch. Its control, rerun under #892's rule on 3 November, ends CONTROLS_REFUSED and is retained as mixed_n39_L66625.control.json beside the failed v2 receipt, and T-176 is V3/C3 there. Two parts stay open under this bead: n26 (T-233, write mixed_n26_L5555.control.json; that is T-233's lane, not L32's) and n28 (T-142, think-i85v). Not closed.

2026-11-04 coordinator: when the n26 lane writes its passing control, also refresh packing/benchmarks/.../wand125-fine-net-lower-bounds-446-release-2026-10-08/README.md lines 26-36, which still say the axis fix is to come (noted by the #892 confirming review).

2026-11-04 bold-ritchie-l42 (intake lane L42, think-3guf; branch claude/bold-ritchie-xo28us-l42): the n26 (T-233) part of the done-when is met on the branch. The kept receipt's axis refusal passes main's rule (test_each_retained_axis_refusal_is_the_crates_enclosure), but nothing on main re-judges a receipt into a new one and --evidence reads only a passing CERT.control.json, so the control was rerun rather than a receipt assembled by hand: `sqverify_fast_census --family mixed --control --only mixed_n26_L5555 --threads 2` under nice -n 19, 15:05:31Z to 15:16:15Z, 644 s of wall and 1,022 CPU-seconds, binary 567a0fd5 from reviewed source d97758bb, ends CONTROLS_REFUSED (r = 905; 99/100 mutant refused at 2,073 of 2,073; axis capture in [0.9909807799642721, 0.9909807865315093], lower end the crate's bound to the bit). Written as mixed_n26_L5555.control.json beside the kept control-failed-v2 receipt (commit 05939963b); apart from timings, status, the axis item's captures_agree and the new sweep_enclosure field it equals the kept one. The folder README's lines 26-41 now say so. T-233's four replays are evidence entries (one per count; census --evidence learned to split #446's three-count report, commit fc10bc2a5), T-233 is V3/C3, and both lower lanes at n = 19, 20, 26 and 27 take its values. One part stays open: n28 (T-142, think-i85v), which needs a review that reads its certificate first (think-4ul6), retained release members and a census packet before its census and control (3.3 to 4.5 CPU-hours); its axis gap of 2.15e-9 no longer holds it. Not closed. Owed after merge: #446's follow-up on T-233's move, rendered from main with `check_requests --draft 446` (think-ndvg is #446's answer bead and is not this lane's).
