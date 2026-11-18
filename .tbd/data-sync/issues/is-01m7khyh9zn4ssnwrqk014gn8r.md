---
type: is
id: is-01m7khyh9zn4ssnwrqk014gn8r
title: "Import #1009: Polkovskyi's 13 exact certificates (lowered: 210, 260, 262, 268, 272, 292, 295; 12-place refinements: 147, 156, 180, 270, 299, 307) at Mishapolk/square-packing-records b637e6c (T-314 to T-326), adopt and regularize; merges after think-qag8's PR"
kind: task
status: in_progress
priority: 1
version: 21
delegate: w3r2-pass-1118
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-17T01:29:08.671Z
updated_at: 2026-11-18T06:24:14.433Z
started_at: 2026-11-17T01:29:10.698Z
---

## Notes

2026-11-17 02:00Z c-import-1009-1117 (progress): packet mishapolk-issue1009-2026-11-16 written at b637e6c (b9b7fa7 pushed 23:27:18Z with the same certificate bytes, force-pushed over at 23:32:03Z); all 13 .cert and Witness/v2 digests match the issue and both SHA256SUMS; every exact side rounds up to the issue's print. Algebraic-house reader for 295 committed alone as 9d02ee33e (for I1 to cherry-pick). certify: 39 jobs, 7m34s wall, 10.4 CPU-min, all accepted/refused as expected; least wall clearance 1e-28 at every count. Sharp controls plan written and hashed before any sharp control ran: scratchpad i2/controls-plan-1009.md, SHA-256 49270cac7d988a8d46078935256fc8bd9bffe9ef5d1eb6f6ea10f70dc8f97142, 2026-11-17T01:59:51Z.

2026-11-17T21:55Z coord-intake-1117r: reclaimed from silent c-*-1117 lanes; delegated to w3-pass-1117r (worktree /home/user/wt/w3): map review-1005 (82fb63e88) into #1011, adopt and regularize 262/292/295, merge; then #1009 (import-1009 83232579c, review-1009 6a4f56b3d).

2026-11-17T22:10Z w3-pass-1117r (coordinator approved): #1011 maps R1's review (T-310..T-313 confirmed V3/C3) and STAGES de Winter's adoptions in select_houses.PENDING_ADOPTION under THIS bead, why 'next pull request': 262 -> T-312, 292 -> T-311 (replacing T-193's no-writer staging there; 292 taken off CORRECTIONS_OWED), 295 -> T-313. Reason: both PRs land on 18 Nov, one day's prior-state archive holds one state per count (268, 25-26 Oct), and #1009 is lower at all three (262 and 295 by 1.58e-3; 292 by 3.62e-9 = 72x #1006's own contraction margin 5.0288e-11, a new result under option D). THIS BEAD NOW OWNS THE HOUSE MOVES AT 262, 292 AND 295: if import-1009 stalls or a #1009 certificate fails validation, de Winter's adoption (T-312/T-311/T-313) must still be done, with both strong generators' regularization, in the next PR this bead lands; it must not be lost. The six citation deferrals of #1005-#1007's evidence now name think-i38n.

2026-11-17T22:20Z w3-pass-1117r (coordinator decision, supersedes the 22:10Z staging note): staging dropped. #1011 lands the registration only (T-310..T-313 at V3/C3 on the replay); R1's review (#1013) is NOT mapped there. THIS BEAD OWNS (1) mapping R1's review (docs/project/reviews/review-2026-11-17-ozden-de-winter-1005-1007.md) into T-310..T-313 together with #1014's review of #1009, and adopting the smallest validated packing at each count in the import-1009 PR (Polkovskyi's at 262, 292, 295 where it is smaller: 262/295 by 1.58e-3, 292 by 3.62e-9 = 72 x #1006's own contraction margin 5.0288e-11, a new result under option D); and (2) IF #1009 STALLS OR FAILS REVIEW, adopting de Winter's packings (T-312 at 262, T-311 at 292, T-313 at 295) with both strong generators' regularization in its own PR, so they are not lost. Mapping draft kept at scratchpad w3/r1-mapping-and-staging.diff and w3/map_r1.py (staging and check_standing parts to be dropped).

2026-11-17T23:20Z w3-pass-1117r (review A1 of #1014, option b): the 1009 review (#1014) measured no gains, padding, lineage, custody or author's checks and confirmed no significance (its after-the-freeze programs never ran). The significance scores and the padding/option-D judgments in the import-1009 PR rest on the import lane's own measurements (mishapolk-issue1009 packet measure/) and the owner's option D (think-b0w5), not on a blind review; the mapping must say so. Also: the replay entry's 'every wall clears by exactly 1e-28' must be corrected (right/top walls 1.0001e-28 to 1.0098e-28; top 1.073e-28 at 180, 5.6e-16 at 292). Owner answered think-bx2a: 262/292 credit de Winter, improved by Polkovskyi (applied).

2026-11-17T23:30Z w3-pass-1117r (review A1 of #1013): R1's review of #1005-#1007 likewise made none of its after-the-freeze measurements, no comparison, no author questions and no significance confirmation; the import-1009 mapping must cite the import lanes' measure/ receipts (#1011's packets; mishapolk packet) for identity/padding and keep the draft scores as the import's, not R1's.

2026-11-18T00:44Z w3-pass-1117r: regularization done (grid-slack 0.5/1/5 deg + evand driver on 13 counts; selection draws views at 11, decides 270 and 307; SETTLED drops 210/272; runs retained under packing/cases/regularized_drawings/think-i38n-2026-11-18/). Merged main (#1010, #1013, #908, #1011). Custody, exact-side register, case verifiers, certificate reach, URL amendments for T-310..T-313, no-public-change record (paper renders: only the explainer register count moved) done; test_house_adoption 92 passed. KKT register candidates at 260/268/270/272/292/295/299/307 (4e-19..1e-13 below) held for think-8yyy. Next: stamp, re-pin, draft PR, coordinator review.

2026-11-18T01:19Z w3r-pass-1118: took over from w3-pass-1117r (killed by a worker restart about 01:00Z). Resuming from c82c06859 plus six uncommitted files in /home/user/wt/w3-import-1009; #1013, #1011 and #1014 merged before the restart.

2026-11-18T02:13Z w3r-pass-1118: finished the branch and opened draft PR #1023 (intake, S3), head 91494623f. Committed the six uncommitted files (8dacbfa8a: each generator's check passes; test_house_adoption 92 passed) plus the runs' README in the document map; T-314..T-326 next_rung now reads adopted (5d6c40cbc); merged main #1016 (34dd6e1db, result-requests conflict: kept #1009 and #1012); no-public-change record re-measured against 2980557a2 (a460f62d6); rigidity blocks for 12 counts (a8f1ae9b4); stamp 5d382d34b, re-pin 91494623f. Announcement 262 credit gap -> think-gpni. Next: hosted CI, then the coordinator's senior review.

2026-11-18T02:46Z w3r-pass-1118: hosted CI on #1023 head 91494623f failed in suites a-d, sweeps and overview (about 25 tests and 3 sweep steps): stale derived records (composite figure, family and contact-shade censuses, rigidity blocks, site-urls) and pins the adoption moved (screen findings, unstable list, KNOWN_TILTS at 270, settlement tests on 272, page budgets for results.html, t-007, t-180, poster credits, superseded set, readoptions, 574 sides, l48/l51/l65 adoptions). Fixed in 948fbe135, 03683fed3; merged main #909 at e97b62f77. Re-running the failing modules locally, then compare_paper_renders against a1a8d0aae (site_urls.py and validate.py are now paper inputs), stamp, re-pin, push.

2026-11-18T03:38Z w3r-pass-1118: CI fixes done and pushed; head 0377a7f51 (merged main through #1025 at ac721bcee). Colorizer fix a3e92c5f0 (_class_pin: only 292's house frame changes, measured over 424 frames). No-public-change record re-measured against a1a8d0aae with 15 paths (007b19063). Local: records tier 55/55, 1,573 tests in the 22 affected modules pass, sweeps census fixed. Waiting for hosted CI on 0377a7f51, then the coordinator's senior review.

2026-11-18T04:58Z w3r2-pass-1118: took over from w3r-pass-1118 (killed by a worker restart about 04:30Z). Already on the branch from the dead lane: 57466324a (A1, render_announcement credits the case record's finder and improver, think-gpni) and ff07d4e69 (A5/A6, per-square pin plus retained reach test). Finished its uncommitted A2/A3 start with the owner's answer (think-frl5): 571bc0c80 pushed (five case records, ledger notes, packet README, runs' README, tests; A7 comment). Next: merge origin/main 3ac78a55f (#1026, #1027), stamp, re-pin, PR description, CI, dispositions, round-2 check.

2026-11-18T05:17Z w3r2-pass-1118: review A addressed. Head b003ae7c5 (merged main 3ac78a55f #1027 at 2d41cc5d2; stamp no-op; re-pin 0db1e5b4f to 571bc0c8; b003ae7c5 registers the A6 slow test's cost after hosted shard A failed on 0db1e5b4f). Description updated (announcement pasted unedited from the fixed tool; A3 row; A8 outputs). Dispositions https://github.com/jlevy/squares/pull/1023#issuecomment-6969700612. Next: hosted CI on b003ae7c5, round-2 check of A1/A5 by the coordinator, merge on 18 Nov.

2026-11-18T05:47Z w3r2-pass-1118: #1023 MERGED at 2026-11-18T05:46:46Z as merge commit 86284ec203b63097b0a51fd5dffe931852430335 (head 5f4943500, hosted CI 31 pass, up to date with main 0f191a2d2; round-2 check of A1/A5 passed by the coordinator). Next: Pages deploy check, replies on #1005/#1006/#1007/#1009 from main, closes, worktree removal.

2026-11-18T06:25Z w3r2-pass-1118: deploy verified. Pages run 44246610603 built 86284ec203b63097b0a51fd5dffe931852430335, success 06:10:05Z. check_published_site --commit 86284ec20: 6480 of 6482 (the two failures are the browser checks, Playwright's chromium headless shell missing at /opt/pw-browsers in this session); with --no-browser 6480 of 6480 passed. results.html rows T-310..T-326 V3/C3 at S as registered, T-310..T-313 data-current=false, T-314..T-326 true; case pages 147..307 credit as the records (e.g. 262/292 Found by Joost de Winter, improved by Mishapolk; 270/299 Daniel improved by Özden, Mishapolk), 292 shows T-323's 17.590016439231 with the regularized drawing. Posting replies from main 86284ec20 next.

2026-11-18T06:27Z w3r2-pass-1118: final reply on #1009 posted from main 86284ec20 after the verified deploy, https://github.com/jlevy/squares/issues/1009#issuecomment-6970909384 (T-314..T-326 V3/C3, each the house; credits as the case records; the held solves at 156/180/270/299/307 noted per think-frl5; the eight KKT candidates named under think-4z8z), issue closed 06:23:34Z. OWED: the records change recording the reply (kind final; reported ids, rungs, positions; beads think-4z8z) and #1009 state closed; close this bead only after it merges. think-gpni, think-p3g8, think-evxy closed.
