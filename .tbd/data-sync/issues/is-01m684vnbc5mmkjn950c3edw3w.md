---
type: is
id: is-01m684vnbc5mmkjn950c3edw3w
title: "Intake pass 2026-10-31: #836-#847 new reports, #816, open drafts #817 #833-#835, watched repos, replies owed, n=39/55/290/291 exemptions"
kind: epic
status: in_progress
priority: 1
version: 36
delegate: bold-ritchie-l2
labels:
  - result-import
dependencies: []
child_order_hints:
  - is-01m685br2zhdy2p5x9fv387m0g
  - is-01m685brzc3k2t7n7fjy3ahzb0
  - is-01m685msgkcqe67s8cwkqy116j
  - is-01m685nejvjntazeebg3zn18mt
  - is-01m685ngekhjw1cxgta3763s3s
  - is-01m685njhfc113wb8prbg15npb
  - is-01m685tapg46244xgj0cmsd3x2
  - is-01m685wqakx05engdrvf9s4789
  - is-01m685wzp4h0xvh1qv6pn93we4
  - is-01m685xayb6rmzxwj5c5vrt8p2
  - is-01m686kknmrk1xt97vne82cnea
  - is-01m687rz8hpgevyt6xe2j9p4bb
  - is-01m68d0t3gpq5ftvzkakhjmm3h
  - is-01m68f02ycck4713n6e6pbexf6
  - is-01m68g3cp9a4ap3mmnecyzzrhj
  - is-01m68g3f8bda4are97wk6tf31k
  - is-01m68g3hqcfvxxbpxaxmxpemac
  - is-01m68j95k4h00b9dwww5sz44jc
  - is-01m68kzzdeghkzk36hzescemmd
  - is-01m68mknga9mx8s5cgrq3c3j1z
  - is-01m68tpnq7ase66t9wk9g7bnmk
hold: null
hold_until: null
created_at: 2026-10-31T04:53:02.444Z
updated_at: 2026-10-31T11:22:45.552Z
started_at: 2026-10-31T08:37:28.427Z
---

## Notes

2026-10-31 (bold-ritchie-l2, #852 at 359ed1687): the five stage 4 reviews of #852 are mapped (docs/project/reviews/review-2026-10-31-*.md). Each reviewer line now names the tier and reasoning setting it ran at, tbd-strong at xhigh, and so do the reviews' verifier and evidence records (V-couzo-1031-review-check, V-evand-1031-review-check, V-mishapolk-1031-review-check); each review discloses the deviation from tbd-strong-max (N-6, N-6, N-7, N-10, RV-11). T-248 and T-254 to T-259 at V3/C3. The fourteen Polkovskyi sub-print counts are held for the owner's question on think-ikku (T-253, and #846's five split into T-260), below the stage 4 exit; T-259 holds 130 alone. Adoption of the eight counts (130, 172, 204, 232, 260, 293, 299, 307) in progress on the same branch.

2026-10-31 L2 (bold-ritchie-l2), branch claude/bold-ritchie-xo28us-upper: #843 (think-big9), #844 + Couzo a5a5d76 (think-n61j), #845 (think-17wo), #824 update (think-3xn9), #846 + Mishapolk 23 October e386aab-fbc1749 (think-pg1y): seven packets, ledger upper-bounds-843-846-20261031, T-252..T-258 at V0/C0 (positions from main 3978a7f61; renumber if another lane registers first), both exact routes + gross and sharp controls + identity on every certificate. Validation beads (reviews, then adoption with both regularizations at 22 counts): think-oy8d, think-dwzb, think-nkt1, think-8hjz, think-ikku. intake_ledger.tree_members now reads pending adoption count by count (T-193 at 88, 126). Reads: evand 0e76d9f, franciscouzo 712c6a6, Mishapolk 52aa267, wand125 7a47ab9, TheSnakeFang d56c9a0. Owner decisions: 152 undecided vs T-122; whether in-corpus sub-print re-certifications are restatements.

2026-10-31 06:53 hourly check: #835 merged (32ef0861b) after review A + addressing pass; think-j83l closed. #833 (c884c37d2) and #834 (41cbe77c1) reviewed, all findings addressed, CI running; #848 being re-merged with main by L4. #666/#715/#719 now record blocked: owner-decision (D3/D4/D5); labels restored after #833 merges. No new GitHub issues since 05:50. L2, L3, L5 running.
2026-10-31 lane L5 (bold-ritchie-l5) report. PRs (draft, none merged): #817 (claude/friendly-einstein-gf9z0h-s29-validation, head 20ba351ec: main 3978a7f61 and 32ef0861b merged, step 6 review written, #816's ask source fixed; --records 54/54; hosted green at bfb16dc53); #849 (claude/bold-ritchie-xo28us-regularize, head fd03d7c89: 39 regularized, 55/290/291 decided, UNRATIFIED empty; --records 54/54; hosted green at 20c0e2c45); #850 (claude/bold-ritchie-xo28us-evidence, head fea8351b2: packets for s76 0699398, sq19 c86a991, 11SquaresOptimal 4262f07; --records 54/54; hosted at 40df512a1 red only on a crashed frontend worker). Beads: think-ojr9 and think-zn7s waits rewritten (memory; cap/owner) and released; think-6gti blocked_on think-10m1; think-10m1 carries #817's verdict (accepted with one Monte Carlo step; C1 proposed) and #816's draft reply; think-yk2h, think-osvq, think-a4x3, think-3i74, think-fddm updated (fddm triaged, packet not made).

2026-10-31 08:00 deviation, disclosed: the three stage-4 reviews of #852's upper-bound certificates (Couzo, Daniel, Polkovskyi) ran at tbd-strong (xhigh), not tbd-strong-max as result-import.md 'Who reviews, and when' asks. Kept rather than re-run because each certificate is decided by two maintained exact routes plus each reviewer's clean-room exact checker; each review's reviewer line must name the tier it ran at. Owner may overrule. #851 (s(44)=7, a lower-bound proof) did get an independent tbd-strong-max review. Daniel review returned: 172/204/260/293/299-update accept for adoption, minor fixes only.

2026-10-31 07:55 hourly: sweep re-run on main 37ede3936+ (scratchpad/intake2.txt): no new issues past #847, no new watched-repo heads; remaining items are owned by open branches (#833, #849, #850, #851, #852, #853, #817). Merged so far: #835, #848, #834. #613 closed with final comment.

2026-10-31 08:53 hourly: merged #833 (b95c5f69c), #853 (c94df7cef), #850 (84ba6fa9c); total this pass 6 (#835 #848 #834 #833 #853 #850). Posted: #613 final, follow-ups #316 #797 #799 #804 #824, acks #836 #847. Labels restored #666/#715/#719. Queue: #854 (re-merging main), #849 (fixes pushed), #851 (fixes in progress), #817 (fixes in progress), #852 (landing 3 stage-4 reviews + adopting 8 counts: 130 172 204 232 260 293 299 307). Owner decisions open: Polkovskyi 14 near-restatements (think-ikku), s(152) tie vs T-122, s(29) S* registration and identity funding, exactness-only regularization (think-j68m), zenodo access, D4 hosting, Q-847a, #744/#599/#809. Beads filed: think-t9uj (closing keywords), release.py append-conflict efficiency bead. No new issues since 07:50.

2026-10-31 09:54 hourly: merged #849 (15450a44d); 7 merged this pass. Main's scheduled slow-lane red at c94df7cef diagnosed: 1800 s budget kill on a slow runner, standing since 24 Oct, not today's merges (think-m2th, owner options); 1 s floor flake fixed in #855 (in review fixes). #854 frontend timeout = standing contention flake (think-yriz). Rerun-failed-jobs is 403 for this integration; no empty commits (note: #850 used one earlier, before review). Queue: #854 (CI running at bfa050ffa), #851 (green incl. deep gate, needs one main merge), #855, #817, #852. No new issues since 08:50.

2026-10-31 10:55 hourly: merged #854 (5b4484fe0) and #855 (49dac4354); 9 merged this pass. Closed think-8krd, think-6m6e. Sweep on main 49dac4354 (scratchpad/intake3.txt): 11 unowned (all on open PRs #851/#852), 0 closeable open, 0 regularization owed, 73 stalled-bead items -> lane L6 triage (claude/bold-ritchie-xo28us-quiet). #851 re-running CI after slow-runner timeouts; #852 in senior+correctness review (strong-max); #817 waiting its turn.

2026-10-31 11:35: #851 merged (90b79dbe1): s(44)=7 T-252, n=44 proved; 10 merged this pass. L6 triage (think-ztcy): stalled 73 -> 16; 34 items owner-decision (13 new owner questions listed in think-ztcy: D5 credit naming beyond horizon, D3 #715 335, think-kzme deletion rows, #732 N=10000 cap, #593 joint credit, #573 T-173 credit, #529 T-159, #574 merge/close, #521 replayed annotation, #522 strategy catalogue, #524-#527 Summins requests, #317 umbrella close, #543 check2 retention/tolerance), 20 standing-hold, 7 author, 3 dependency, 9 actionable. Actionable now: replies #375/#522/#763 -> lane L7. After #852 merges: think-4rzl (#804 T-244 172/263, ~3 CPU-h), think-7scz (#545 grade-C registration), think-flxm (sqverify_continuous v4 replay ~1.4-5.2 CPU-h), think-63vx (Lean build 41 modules ~2.1 h + remeasure).
