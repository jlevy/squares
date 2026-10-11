---
type: is
id: is-01m47ppnptcx8ezs50ecs4jqxk
title: "sqverify-fast census --control: the 99/100 mutant at the least-certified-bound direction can be a true certificate (FC-1); choose by slack or run all directions, then review"
kind: task
status: closed
priority: 2
version: 4
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m47hea1vkqx8h5wzdzcyqs5k
hold: null
hold_until: null
created_at: 2026-10-06T04:14:15.257Z
updated_at: 2026-10-06T22:10:05.082Z
started_at: 2026-10-06T21:48:04.955Z
closed_at: 2026-10-06T22:10:05.082Z
close_reason: FC-1 fixed in sqverify_fast_census --control (9f36ede38, f1ddc2379, 03174112b), two reviews accepted; n96_L997 re-controlled v2 CONTROLS_REFUSED; merging via lane R4
resolution: null
duplicate_of: null
---
FC-1 of docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-fix-check.md (non-blocking, fails closed). sqverify_fast_census --control runs the 99/100 mutant at one direction, the oblique row with the least min_certified_lower_bound, which on a verified direction is only the branch and bound's termination margin and says nothing about slack. On mixed_n18_L470 (declared net, step 1/1001) that is index 408, where the 99/100 mutant is a true certificate: main's build (d97758bb) verifies it there (least bound 1.0000002639721404), so the receipt is CONTROL_FAILED with captures_agree true (receipt kept, uncommitted, at lane R1's scratchpad r1/recheck/mixed_n18_L470.control.json). The mutant is refused at 230 of 416 directions, each with an exact witness below 1. Lane R2 reports CONTROLS_REFUSED for mixed_n18_L4704 (node 797) and mixed_n19_L48229 (node 198) with the step fix, so this does not block them. Fix proposed by the re-check: keep the near-threshold run at the least-bound leaf; replace the fixed-index 99/100 run by the 99/100 mutant at all directions with --confirm, requiring at least one refusal and an exact witness below 1 (re-evaluated by mixed_exact) at every refused direction, as check_sqverify_fast's declared-net group does at 0.985. A change of control logic: a reviewer must read it before a receipt made with it counts. Also FC-4/FC-6 notes if touched.

## Notes

2026-10-06 21:58Z lane R4 (think-wyf4, branch claude/ecstatic-pascal-pothtx-r4): the ask is done, and the bead can close.

- Fix: devtools.sqverify_fast_census --control now runs the 99/100 mutant at every net direction with --confirm, writing receipt kind sqverify-fast-control/v2. A sweep holds only when each refusal is a coverage refusal (counterexample-candidate) at a centre in the per-bin domain whose exact capture, re-evaluated apart from the crate, is below 1, at least one direction refuses, and the rows agree with the summary. The near-threshold run must be confirmed below threshold with agreeing captures, and only format M is accepted. Commits 9f36ede38, f1ddc2379 (CC-1 to CC-8) and 03174112b (CR-2 to CR-7), with tests.
- Existing v1 CONTROLS_REFUSED receipts validate under the new rule and were not regenerated. Both reviews agree, and a new test assertion holds every v1 receipt.
- Reviews were separately prompted with claude -p --agent tbd-strong --model claude-opus-5-5 in a detached worktree, and are stored byte-identical (e02e0557e):
  - docs/project/reviews/review-2026-10-06-sqverify-fast-census-control-fc1.md: accept with fixes, CC-1 blocking.
  - docs/project/reviews/review-2026-10-06-sqverify-fast-census-control-fc1-recheck.md: accept with one fix, CR-1, the VERIFIERS.md regeneration, done in da07cbbe1.
- mixed_n96_L997 was re-controlled with 03174112b at 2 threads: CONTROLS_REFUSED. The sweep refused 187 of 201 directions; the mutant verifies at the other 14, which is slack. Admitted in 2a6585a9d as E-n096-wand125-mixed-997-sqverify-fast-replay, so n = 96's verified lower bound is 997/100. The failed v1 receipt is kept as mixed_n96_L997.control-failed-v1.json.
- Not done here: FC-1 for mixed_n18_L470 (declared net, lane R1's scratch receipt). It can be re-controlled with the same code if anyone needs that row.
