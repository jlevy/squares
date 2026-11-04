---
type: is
id: is-01m4xe5txp3t3t4xczs1swedc9
title: Judge the census control's axis refusal against the sweep's enclosure, not AXIS_ROUNDING (F-1 of the 14 October wand125 review; T-142, T-175 to T-177)
kind: task
status: closed
priority: 2
version: 8
delegate: bold-ritchie-l34
labels:
  - result-import
  - validation
dependencies:
  - type: blocks
    target: is-01m4xpvk3p35kqfqcrszjw9zp6
parent_id: is-01m4wsqt2sjrksybyz375sarb3
hold: null
hold_until: null
created_at: 2026-10-14T14:48:32.438Z
updated_at: 2026-11-04T10:28:12.350Z
started_at: 2026-11-03T05:05:02.326Z
closed_at: 2026-11-04T10:28:12.350Z
close_reason: "Shipped in https://github.com/jlevy/squares/pull/898 (merged a565aef2e): T-262 V3/C3, n-094 verified lower bound 1993/200; axis rule confirmed on n94; #892 review nits addressed."
resolution: null
duplicate_of: null
---
Finding F-1 of the 14 October review (docs/project/reviews/review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md), major for the records lane and not a defect of any certificate.

`packing/devtools/sqverify_fast_census.py` holds the axis vertex sweep's refusal to a constant, `AXIS_ROUNDING = 1/10^9` (the axis branch of `refusal_record`). The gap the rule measures is half the sweep's enclosure width, which varies by a factor of twenty across the s(37), s(39) and s(44) certificates and exceeds the constant at n = 39, so the n = 39 whole-net control cannot end `CONTROLS_REFUSED` under this rule although its refusal is sound. It bears on T-142 as well.

Fix: one of the review's section 5 options 1 to 3, as a change to control logic read by a reviewer. Not a small importer change, so the records lane of the 14 October intake did not make it: T-175 to T-177 are registered at V0/C1 and their C3 waits on the control. Done when the axis refusal is judged against the sweep's own enclosure, a reviewer has read the change, and the n = 39 control can end CONTROLS_REFUSED.

## Notes

## Validation

2026-10-14, validation backlog (owner's cap: hold anything > 40 CPU-h). This bead is the AXIS_ROUNDING item of jlevy/squares#543.

- Claim: the census control's axis refusal (packing/devtools/sqverify_fast_census.py, refusal_record's axis branch, AXIS_ROUNDING = 1/10^9) is sound for the check2 certificates when judged against the sweep's own enclosure: at n = 39 the exact capture of the 99/100 mutant at the least vertex is 0.99207124979... < 1, inside the domain, with F - l = u - F = 1.264e-9 (enclosure width 2.55e-9), so the control ends CONTROLS_REFUSED; it decides T-142's control too (gap 2.15e-9). Review: docs/project/reviews/review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md, section 5 and F-1.
- Run: option 2 of the review's section 5 (the control recomputes the enclosure, no crate change): walk the column as packing/resources/web/wand125-fine-net-n37-n39-n44-2026-10-13/review/programs/sweep_emulation.py does, require l' = b (the transcription walked the crate's path) and l' <= F <= u'; then rerun the census `--control` at n = 37, 39, 44 and T-142 (the `fine_net_followup control-sample` diagnostic exists only on the unmerged branch claude/wand125-confirmations-2026-10-11, review F-6). Option 1 (the crate reports u) is a new source_sha256 and needs a re-review; option 3 (one-sided b <= F) is the smallest sound change.
- Cost: about 1 CPU s per certificate for the enclosure recomputation (review, option 2); the code change and a reviewer's read are the real cost. The whole-net controls it unblocks are priced on their own beads (n = 39: think-567s).
- Budget status (owner, 2026-10-14): runnable (<= 40 CPU-h) once decided.
- Possible <= 40 CPU-h subset: n/a.
- Depends on: the owner's choice of option on jlevy/squares#543 (for T-142, which decides n = 39 as well); a reviewer for the control-logic change.
- Done when: the axis refusal is judged against the sweep's enclosure, a reviewer has read the change, and the n = 39 (and T-142) whole-net control can end CONTROLS_REFUSED; n = 37 and n = 44 still count.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. Seconds.
2026-11-03 (bold-ritchie-l33, think-2agl): a fourth certificate waits on this rule. The whole-net control of #890's mixed_n94_L9965 (T-262, s(94) >= 1993/200, 600-direction declared net) refused the 99/100 mutant on coverage at all 600 directions, each in the per-bin domain with exact capture below 1, and the near-threshold mutant; it failed closed only at the axis, where the exact capture 0.99308601380750 sits 1.123e-9 above the sweep's certified bound 0.9930860126842824 (AXIS_ROUNDING 1e-9). Receipt kept as packing/benchmarks/measure-verifier/census-mixed/ozden-s94-lower-bound-2026-11-03/mixed_n94_L9965.control-failed-v2.json on branch claude/bold-ritchie-xo28us-l33. Once the rule is fixed and reviewed, rerun `sqverify_fast_census --family mixed --control --only mixed_n94_L9965` (about two minutes of wall at two threads).
2026-11-03 (bold-ritchie-l34, intake lane L34): fixed on PR #892 (branch claude/bold-ritchie-xo28us-l34, head adc153fcc), draft, labelled S2, awaiting a reviewer's read of the control-logic change. Option 2 of the review's section 5: new packing/devtools/sqverify_fast_axis.py (`column_enclosure`) walks the axis vertex's column as axis.rs does with interval.rs's directed steps; `refusal_record`'s axis branch now requires the recomputed lower end l' = the crate's bound to the bit and l' <= F <= u' (`axis_captures_agree`); AXIS_ROUNDING is gone and the receipt's axis item keeps `sweep_enclosure`. The walk reproduces the crate's bound to the bit at s(37) (original and mutant), s(39) and s(94); enclosure widths 1.37e-10, 2.53e-9 and 2.25e-9. Red-first tests in packing/tests/test_sqverify_fast_census.py and test_sqverify_fast_axis.py. n = 39 rerun at adc153fcc (binary 567a0fd5, source d97758bb, 05:17-05:28Z at two threads): CONTROLS_REFUSED, axis F in [0.9920712485323058, 0.992071251060881]; receipt sha256 d8a21aa2f11a17e043948846d0c069c0f0aa3813d300a42b806f07da4f12ece3 kept outside the tree, not recorded here (T-176's lane writes mixed_n39_L66625.control.json after #892 merges). n = 94's numbers pass in the tests; T-262's lane reruns its control after the merge. Remaining before close: the reviewer's read and the merge.
