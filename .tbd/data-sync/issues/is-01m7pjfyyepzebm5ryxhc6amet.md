---
type: is
id: is-01m7pjfyyepzebm5ryxhc6amet
title: "Stage 4 review of T-144's mixed_n122_L1126 (wand125 s(122) >= 563/50, n = 122 to 126): the review that reads the linear certificate, owed before its replay evidence can be mapped"
kind: task
status: in_progress
priority: 2
version: 5
delegate: r144-1118
labels:
  - result-import
  - validation
dependencies: []
parent_id: is-01m4kbxna1xdmjd8nkka3wax60
hold: null
hold_until: null
created_at: 2026-11-18T05:36:22.990Z
updated_at: 2026-11-18T06:33:31.390Z
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
