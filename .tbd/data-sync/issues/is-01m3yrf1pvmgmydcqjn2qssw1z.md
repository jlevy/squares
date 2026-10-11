---
type: is
id: is-01m3yrf1pvmgmydcqjn2qssw1z
title: Import the ten wand125 certificates at b00fc70 (rect n20, 42, 70; linear n82; mixed n83, 85, 87, 91, 92, 96)
kind: task
status: closed
priority: 1
version: 11
labels:
  - result-import
dependencies: []
parent_id: is-01m3yrdxte02c7bnygkke34ct4
created_at: 2026-10-02T16:51:52.667Z
updated_at: 2026-10-10T22:43:28.574Z
closed_at: 2026-10-10T22:43:28.570Z
close_reason: "All ten certificate imports are integrated; the later n82 follow-up is owned by think-4qga. Reconciled under think-p2z4; evidence: tbd show think-r7yt version 10: status=open; fresh notes: T-075, T-076, and T-077 are V3/C3; mixed and linear scope needs nothing more from this bead; tbd show think-r7yt version 10: child_order_hints is empty"
resolution: null
duplicate_of: null
---
Lane V: retain at b00fc70, extend audit tools, exact preflights, blind review (review-2026-10-02-wand125-afternoon-certificates.md). Then register at V0 (records lane), push, replay on cloud runners (~74 CPU-h), merge receipts, record. Also: what upstream 23e2284's re-hash of retained bundles and the withdrawal of mixed_n50_L7318 mean for retained packets. Issues #282, #294, #308; the three rectangles have no issue.

## Notes

2026-10-03 06:05 runner survey: m4 done (claude/replay-wand125-afternoon-m4 @6dfa6b9e): n92-L975 and n96 201/201 FULL_REPLAY_MATCHES_SHIPPED; n83 136-200 RANGE_REPLAYED 65/65. m6 (afternoon-m6 @8c889f2d): n83 0-86 RANGE_REPLAYED 87/87; 87-135 running, then n87, n91 with merges. n83's merge and control wait on m6, then run anywhere from both branches. r5 (afternoon-r5 @b829406d): n42 PASS; n70, n20 died on container restarts, r5 at its restart limit, so new runner r6 (session_01La3mEtT5gbHYcfBWYyM4EZ, branch claude/replay-wand125-afternoon-r6, --resume from r5's transfer) runs n70, n20. n82: n82b running 124-152 (nothing pushed yet); n82a ran 0-51 to exit 0 and 52-90 is running, but its commit/push was DENIED by the auto-mode classifier (Sensitive-Source Provenance) at 05:51Z: receipts are uncommitted in its container and need the user's go-ahead in session_015CiPn4iFQWzpznZyFdwuZL. Not worked around.
2026-10-03 16:45 All six b00fc70 mixed certificates replayed FULL_REPLAY_MATCHES_SHIPPED and pushed on #298 (d9f0266d5, f824659bd): n83 (four ranges across m4 and m6), n85-L946 (m5), n87 and n91 (m6, n91 finished at bcacffbe), n92-L975 and n96 (m4). The records lane is raising T-075 to V3/C3 as a whole (as T-071 was), moving the verified bound at 83, 85-88, 91-93, 96. Remaining in this import: rect n70, n20 (r6; n42 PASS on r5) for T-077, linear n82 (n82a/n82b blocked on classifier denials; needs the user) for T-076.
2026-10-03 17:40 n82 unblocked by the owner: n82a pushed claude/replay-wand125-n82-a @18eb4c39f (0-51 RANGE_REPLAYED 52/52, 13,868 CPU-s; 52-90 39/39, 17,073 CPU-s), now running 91-123; n82b pushed claude/replay-wand125-n82-b @0ce15aeab (124-152 29/29, 18,474 CPU-s; 153-178 26/26, 19,723; 179-200 22/22, 23,620), finished. After 91-123: linear-merge n82 and linear-control n82 from both branches, then T-076 to V3/C3.
2026-10-03 21:05 Follow-up PR #327 (182776349): T-076 n82 linear V3/C3 (six ranges, 30.74 CPU-h; n82 verified 233/25) and T-073 n83 linear V3/C3 (26.15 CPU-h; no case moves, T-075 higher), plus think-sfbj reply records. After merge: final note on #294 to @wand125 (n82, n83 confirmed) and close #294.
2026-10-04 01:05 Afternoon rectangles replayed in full: n42 (r5), n70 and n20 (r6, done 23:13), each stdout status VERIFIED, receipts on claude/replay-wand125-afternoon-r6 @c2be1d247 (transfer/wand125-rect-afternoon-r5/). Neither r5 nor r6 is merged; T-077 is still V0 on main. Next: one batched records lane (with T-081 and T-046 leftovers) moves T-077 to V3/C3.
2026-10-04 reconciliation (think-75ti, origin/main e5a48b310): done on main - six mixed certificates T-075 V3/C3; n82 T-076 V3/C3; n83 linear T-073 V3/C3 (n101 T-080 V3/C3); #294 closed 2026-10-03T22:35Z with the final reply; 23e2284 re-hash and mixed_n50_L7318 withdrawal answered by review-2026-10-02-wand125-afternoon-certificates.md AF-7. Remaining (real): T-077 (rect n20, n42, n70) is still V0 on main; its full-replay receipts are on claude/replay-wand125-afternoon-r5 @b829406d (n42) and claude/replay-wand125-afternoon-r6 @c2be1d247 (n70, n20), neither merged. Needs one records lane: merge those receipts, add the source-replay evidence, move T-077 to V3/C3 via devtools.check_results. Close this bead then.

2026-10-06 08:50Z lane R4 of think-wyf4 (branch claude/ecstatic-pascal-pothtx-r4): the mixed and linear parts were already done on main: T-075 V3/C3 (n83-L937, n85-L946, n87-L948, n91-L970, n92-L975, n96-L996, source-checker full replays) and T-076 V3/C3 (n82-L932 linear); all seven are VERIFIED rows of the 149-certificate sqverify-fast census (reviewed build 9985c465, rows of 3 Oct). Under the same rules as T-091/T-097 the six format M ones now have control receipts (CONTROLS_REFUSED, 6 Oct, 42 CPU-s, commit 2bda0d5a4) and independent replay entries E-n0NN-wand125-mixed-*-sqverify-fast-replay on T-075 (commit b3e917247, re-pin b2d94b082): no rung moves, T-075's code attribute becomes independently re-implemented. n82 is format L, outside the route's reviewed scope, so it takes no sqverify-fast entry without another review. The rectangle parts (T-077, n20/42/70) are lane R5's.

2026-10-06 (lane R5, think-wyf4), rectangle part only: rect_n20_L49, rect_n42_L68275, rect_n70_L86275 replays (afternoon-r5 b829406d, afternoon-r6 c2be1d247) merged into the 2 October packet's receipts/replay; new E-wand125-rectangle-2026-10-02-source-replay; verified bound raised at n20 (49/10) and n42 (2731/400). Also controlled on the sqverify-fast format T route (3 entries E-n020/042/070-wand125-rect-*-sqverify-fast-replay). T-077 raised in place V0/C1 -> V3/C3, confirmed both reproduced with the producer's code and independently re-implemented. Commits d07884498, 942473b60. The mixed and linear parts belong to lane R4.

2026-10-06 22:00Z lane R4: two of this bead's mixed counts have moved on in the verified lane. T-082's certificates of 3 October, decided by sqverify-fast on 6 October, are higher at n = 92 (977/100 over mixed_n92_L975) and n = 96 (997/100 over mixed_n96_L996, admitted under the repaired v2 control, think-0uia); commits da07cbbe1 and 2a6585a9d. T-075 keeps n = 83 and 85. The mixed and linear parts of this bead need nothing more from R4. n82 (format L) stays with think-4qga.
