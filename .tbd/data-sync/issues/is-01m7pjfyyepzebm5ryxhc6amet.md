---
type: is
id: is-01m7pjfyyepzebm5ryxhc6amet
title: "Stage 4 review of T-144's mixed_n122_L1126 (wand125 s(122) >= 563/50, n = 122 to 126): the review that reads the linear certificate, owed before its replay evidence can be mapped"
kind: task
status: in_progress
priority: 2
version: 12
delegate: r144b-1118
labels:
  - result-import
  - validation
dependencies: []
parent_id: is-01m4kbxna1xdmjd8nkka3wax60
hold: null
hold_until: null
created_at: 2026-11-18T05:36:22.990Z
updated_at: 2026-11-18T08:55:07.746Z
started_at: 2026-11-18T05:37:37.484Z
---
T-144 (wand125's s(122) >= 563/50 = 11.26 by the linear certificate mixed_n122_L1126, raising n = 122 to 126; V0/C0 on main) has no review that reads its certificate: the 11 October final review (docs/project/reviews/review-2026-10-11-final-lower-bounds.md) read the record and premises only. result-import.md stage 4 needs a mapped mathematical review before the complete replay's evidence moves the verified lane (check_results verified_lane_review_problems), as the 14 October review did for T-179 and the 4/11 November reviews for T-142 and T-143.

## Review
- What: the stage 4 mathematical review of mixed_n122_L1126 (result-import.md, Stage 4: Validate, "The review"): re-derive the linear argument from the certificate to s(122) >= 563/50 and the monotone transfer to 123 to 126 (502 point, 1,268 segment and 3 rectangle orbits under D4, mass 12199999/100000, core 9977/10000, 201 net half-angles of step 83/40000, the net's endpoint and centre-domain argument), recompute every exact premise apart from the tools and the checker, give the trust boundary of code/unified_linear_verify.cpp (SHA-256 0249726a..., V-wand125-unified-linear-verify-cpp) and what the replay shares with the source, decide sampled angles or poses with the reviewer's own exact code, check the comparison with Green's and Nagamochi's values at 122 to 126, and confirm or change the draft significance S3. A summary for the author, findings graded blocking/major/minor/note with source file and line, questions; mapped under docs/project/reviews/; recorded as external_review on E-wand125-linear-n122-1126-report and in T-144's reviews.
- Who: a tbd-strong-max sub-agent at maximum reasoning in its own worktree, sharing no context with the replay lane; it reads the source as data, runs only code it writes, and does not read an earlier review of this or a sibling certificate (2 October T-080, 14 October T-179, 11 October final) until its findings are written.
- Inputs: packet packing/resources/web/wand125-linear-n122-2026-10-10/ on branch claude/intake-2026-11-18-t144-replay (candidate and certificate retained under release/, four documents under square-packing/, the proof bundle pinned in acquisition/release-assets.json and fetchable from release square-lower-bounds-v1, asset certificates__mixed_n122_L1126.tar.gz, 31,784,537 B, 6443eae0...5deb).
- Then: the replay lane (think-nd7g) maps it with the complete replay and control receipts; check_results derives the rungs.

## Notes

2026-11-18 06:25Z r144-1118: checker and controls plan frozen and pushed at ee66533d0f (branch claude/intake-2026-11-18-review-t144), packet packing/resources/web/wand125-linear-n122-review-2026-11-18/. Source fetched by this lane at a9f76c3 and the asset at 6443eae0...5deb (scratch only). Synthetic selftest passed. Next: run RC1-RC6 on the certificate.

2026-11-18 06:14Z r144-1118: correction, the freeze note's time was 06:03:49Z (commit ee66533d0f), not 06:25Z. Receipts of RC1 to RC6 pushed at 15d8a8ab8b: premises hold, 201 inputs encode the candidate, node 0 decided exactly (least capture 1.0039577044...), nodes 37, 108, 180, 200, 1 decided by the lane's branch and bound, 99/100 mutants refused with exact witnesses, no capture below 1 at 1,608 poses and a 24-node search. The coordinator approved deciding all 201 nodes (1 process, nice 19, stop at 2 CPU-hours): running from 06:14Z, receipts under out/bnb-all/.

2026-11-18 06:34Z r144-1118: nodes 0 to 125 decided by the lane's own programs (receipts pushed through 1cc50e6fe3); the run continues at nodes 126 to 200, 735 CPU-s so far. Checker read as data: sound by reading. Findings drafted (no blocking or major; M-1 release SHA256SUMS lacks the asset; M-2 README omits the centre domain; R-1 record: at n = 126 the reported lane is T-180's 11.3133 > 563/50, so T-144 raises the reported lane at 122-125 only). Next: finish the run, freeze the findings, read the earlier reviews, map, PR.

2026-11-18 07:08Z r144b-1118 (successor lane, delegated): resumed after the 06:59Z container restart. Range 176-200 had not completed (nodes 176 to 193 printed NODE_DECIDED, no .done, empty .time, no run.log line; the driver restarts a range without .done), so it is re-running from scratch through the frozen r144_run_all.sh (1 process, nice 19) from 07:07Z; the killed run's partial receipts are kept in scratch for a determinism comparison. Ranges 1-175 and node 0 are decided and committed at 1b9c98255. Next: commit range 176-200, summarize, freeze the findings.

2026-11-18 07:21Z r144b-1118: correction, the rerun of range 176-200 started at 07:05:32Z (not 07:07Z). It reproduces the killed run exactly at nodes 176 to 193 (boxes, margins) and has decided node 194; nodes 195-200 are running (one process, nice 19, host load ~11). Uncommitted in /home/user/wt/r144: review-text corrections (G11 margin 0.0307191244486..., M-2 wording, driver citation, node-0 infimum argument, disclosures of the checker read before the findings freeze and of think-nd7g's Oct notes), README updates, programs/r144b_compare_killed.py. The doc-map and synopsis lines are saved as a patch in scratch r144b/postfreeze-map.patch for after the freeze. Next: commit the range, second mutant, summarize, freeze.

2026-11-18 07:36Z r144b-1118: range 176-200 rerun complete (07:05:32Z to 07:29:15Z, 1,070 CPU-s), committed at e83890be42: ALL 201 NODES DECIDED by the lane's own programs (node 0 by r144_axis.py, nodes 1-200 by r144_bnb.py, 71,418,450 boxes vs the source's 71,476,052 nodes); the killed run's 18 finished nodes reproduced exactly. Second mutant (heaviest segment orbit removed) refused by both deciders with exact witnesses. FINDINGS FROZEN at 2026-11-18T07:35:35Z, commit 80405c86fe (frozen/findings-frozen-digest.txt, 67 files, verifies). Decision accept, no blocking or major; S3 confirmed. CPU about 0.93 h in all. Next: read the earlier reviews, write the comparison, map, draft PR.

2026-11-18 07:50Z r144b-1118: draft PR https://github.com/jlevy/squares/pull/1034 (labels intake, S2), head c5a905423d (main 86284ec20 merged in), base main 86284ec203. Post-freeze commit 526b710cfe adds the comparison with the 2 Oct T-080, 14 Oct T-179 and 11 Oct final reviews, the note on this copy, the doc-map entry and synopsis row. packing-validate --records passed locally (55 steps, 264 s). Scratch: the extracted bundle (634 MB) deleted; the asset and pinned documents kept in scratch r144/. Waiting on hosted CI, then a message to the coordinator for the senior review.

2026-11-18 08:19Z r144b-1118: correction, the previous note (PR opened) was written at about 07:45Z, not 07:50Z. PR #1034: hosted CI passed on a1c5348e3d (16 pass, 41 skipped, none failed); main then moved (#1032, records only, no overlap), so main 50962004c was merged in: head b71e72e8a0, base main 50962004c8. packing-validate --records passed on it (199 s). CI on b71e72e8a0 is running; the coordinator gets the number, head and base when it is green. The worktree /home/user/wt/r144 stays as it is for the senior review.

2026-11-18 08:57Z r144b-1118: handed to the coordinator for senior review. PR https://github.com/jlevy/squares/pull/1034 (draft, intake, S2), head cf89f10a8c (contains main d068c3fc04; main d068c3fc0 #1033 merged with the doc-map/synopsis conflict resolved by keeping both entries and re-rendering), base main; hosted CI green on the head (16 pass, 41 skipped); packing-validate --records passed on it. main has since moved to 1015fc175f (#1029); a trial merge is clean. Worktree /home/user/wt/r144 untouched until the review returns. Bead stays in progress (the mapping is think-nd7g's).
