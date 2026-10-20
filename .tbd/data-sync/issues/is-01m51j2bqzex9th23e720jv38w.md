---
type: is
id: is-01m51j2bqzex9th23e720jv38w
title: "Review: retained replays of T-185 to T-190 (stage 4 review lane, upper bounds registered 15 October)"
kind: task
status: in_progress
priority: 1
version: 20
delegate: user-eb-review-185-190
labels:
  - validation
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
hold: null
hold_until: null
created_at: 2026-10-16T05:13:30.623Z
updated_at: 2026-10-16T08:20:04.218Z
started_at: 2026-10-16T05:13:42.512Z
---
Stage 4 review lane (W2) for the upper-bound entries registered on 15 October at V0/C0 whose next rung is "independently review the retained replay": T-185 (#506, 175), T-186 (#593, twelve counts), T-187 (#606, 146), T-188 (211), T-189 (#607, 237) and T-190 (237). Model: docs/project/reviews/review-2026-10-14-upper-bound-imports-561-593.md (the review of T-161 to T-183). Deliverable: docs/project/reviews/review-2026-10-16-upper-bound-imports-<issues>.md on its own branch and draft PR, which reproduces each packet's retained replay (devtools.upper_bound_reports PACKET check --replay), runs the third exact route, re-fetches each pinned scope and checks digests, measures credit, grades findings, and says per entry whether V3/C3 is supported and what each count's adoption should be. It moves no rung; the records lane that follows (a separate bead) writes the rungs and adoptions.

## Validation
- Claim: the finite upper bounds T-185 to T-190 state, their retained rational certificates and replays in their packets, the maintained exact routes and the third route.
- Run: upper_bound_reports check --replay per packet, the third route's citations check, pinned-scope fetch and digest checks.
- Cost: the 14 October review of 28 certificates replayed in minutes per packet on this host; estimate under 1 CPU-h here.
- Budget status: runnable (under the 40 CPU-h cap; small).
- Depends on: nothing; all on main e2e018f32.
- Done when: the review document is on a pushed branch with its PR, findings graded, and per-entry verdicts stated.
- Machine note: serial, one process; shares the 4-core host with the regularization lane (2 workers).

## Notes

2026-10-16 05:29Z user-eb-review-185-190: replay evand-n146-2026-10-14 check --replay (T-187, n=146): 3 jobs decided again, every one equal to its retained row, exit 0, 20 s wall (05:27:50Z-05:28:10Z), worktree review-185 at e2e018f32.

2026-10-16 05:29Z user-eb-review-185-190: replay couzo-verified-bounds-2026-10-14 check --replay (T-188, n=211): 3 jobs equal to retained rows, exit 0, 45 s wall (05:28:10Z-05:28:55Z).

2026-10-16 05:32Z user-eb-review-185-190: replay couzo-n237-2026-10-15 check --replay (T-190, n=237): 3 jobs equal to retained rows, exit 0, 43 s (05:28:55Z-05:29:37Z).

2026-10-16 05:32Z user-eb-review-185-190: replay couzo-certificates-2026-10-14 check --n 237 --replay (T-189's in-scope count): 3 jobs equal, exit 0, 36 s (05:29:37Z-05:30:13Z); the packet's other 22 counts (beyond-horizon, no entry here cites them) queued after the in-scope work.

2026-10-16 05:32Z user-eb-review-185-190: replay couzo-certificates-2026-10-11 check --n 175 --replay (T-185): 3 jobs equal, exit 0, 31 s (05:30:13Z-05:30:45Z); the packet's other 14 counts (T-152's and beyond-horizon rows) queued after.

2026-10-16 05:53Z user-eb-review-185-190: replay mishapolk-kkt-refinements-2026-10-14 check --n <T-186's 12 counts> --replay: 36 jobs equal to retained rows, exit 0, 1,337 s (05:30:45Z-05:53:01Z). In-scope replays of all six packets done; custody re-fetched (blobless git clones at the six pins, 05:37Z): 802 manifest lines, 752 pinned_only and 50 retained files all at their digests, every tree as recorded. Next: check-claims x6, third route (scratch driver), then the out-of-scope remainder of the Mishapolk and #506 packets.

2026-10-16 06:00Z user-eb-review-185-190: check-claims rebuilt all six frozen claim records equal (1.7-16.5 s each, 05:53Z). Third route (devtools.check_half_angle_area at e2e018f32, unchanged since e1fc548d9, driven by a scratch roster driver): 17 certificates the six entries cite, 422,712 pairs (8,138 clipped), 102/102 controls at their required outcome, 32 upstream checks, no disagreement, exit 0, 179.8 s (05:53:37Z-05:56:37Z). Credit measured pose by pose; writing the review next while the Mishapolk and #506 out-of-scope remainders replay.

2026-10-16 06:13Z user-eb-review-185-190: replay mishapolk-kkt-refinements-2026-10-14 check --n <the other 12 counts> --replay: 36 jobs equal, exit 0, 943 s (05:56:37Z-06:12:20Z); the whole 72-job receipt is now reproduced here. Next: couzo-certificates-2026-10-11's other 14 counts (running). Review draft at docs/project/reviews/review-2026-10-16-upper-bound-imports-506-607.md (uncommitted).

2026-10-16 06:29Z user-eb-review-185-190: replay couzo-certificates-2026-10-11 check --n <the other 14 counts, T-152's 304/305 and beyond-horizon rows> --replay: started 06:12:20Z, STOPPED by me at 06:28:24Z unfinished (exit 143) when the host load reached 17 on 4 cores and the process was getting ~0.25 core; no difference raised before the stop, but no reproduction claimed. Out of scope (no entry here cites them), decided twice by the import lane on 11 Oct (certify + complete check --replay); priced at 2,484.89 route CPU s, not run. In-scope 175 reproduced at 05:30Z.

2026-10-16 06:36Z user-eb-review-185-190: review committed and pushed: claude/intake-2026-10-16-review-185-190 at 6c10c865e (docs/project/reviews/review-2026-10-16-upper-bound-imports-506-607.md + document-map line + SYNOPSIS render). Next: site edition cut for the SYNOPSIS row (check_release_impact flags SYNOPSIS.md as a site input), packing-validate --records, draft PR.

2026-10-16 user-eb-review-185-190, VERDICTS for the records lane (review docs/project/reviews/review-2026-10-16-upper-bound-imports-506-607.md, branch claude/intake-2026-10-16-review-185-190 at 9bd813b2b (review commit 6c10c865e), draft PR #648 (https://github.com/jlevy/squares/pull/648, labels S2 and intake)). All six accepted for finite feasibility only; V3/C3 supported for every entry with its confirming evidence entry and this review; none V4/C4; no blocking or major finding.
- T-185 (175): accepted, V3/C3; confirming entry to write E-couzo-506-n175-exact-feasibility (scope 175; E-couzo-506-exact-feasibility covers only #506's 11 requested counts); no house: above the case (T-158) by 2.94e-3, superseded; significance S1 -> S2.
- T-186 (12 counts): accepted, V3/C3; E-mishapolk-70a033f-exact-feasibility; house at 129, 154, 156, 175, 176, 204, 232, 264, 271, 302, 303, 304; S1 stays.
- T-187 (146): accepted, V3/C3; E-evand-606-n146-exact-feasibility; house at 146; S2 stays.
- T-188 (211): accepted, V3/C3; E-couzo-487b058-exact-feasibility; house at 211; S1 -> S2.
- T-189 (237): accepted, V3/C3; E-couzo-607-exact-feasibility (scope 237; may cover its 15 beyond-horizon rows on the import lane's two replays); no house (T-190 smaller by 2.40e-11), history; S2 -> S3.
- T-190 (237): accepted, V3/C3; E-couzo-4e4c8ce-n237-exact-feasibility; house at 237; S1 -> S2.
Findings: RT-1 minor (T-188's regularization of T-182 is no refinement: 5 squares beyond 0.1; follow T-182 154 / T-173 153 precedent); RT-2 minor (T-185 claim calls T-140 a refinement of Xu's packing; by pose no 1:1 pairing, 86/175 within 0.1); RT-3 minor (T-186/T-187 notes name 9b32da04d houses; current houses listed in the review); RT-4 minor (T-186 credit stops at Couzo at 154/156/271/302; at 271 T-161 lacks a regularization of T-151, owner/records lane); RT-8 minor (this review's third-route run and custody check are in scratch, not retained: add the six keys/rosters/credit lines to check_half_angle_area with tests and run --receipts third-route-2026-10-16.json.xz, ~3 min; until then do not list V-check-half-angle-area); notes RT-5 (T-187 lineage measured: Xu's design, 9 squares beyond 0.1), RT-6 (T-190 also refines T-189: 198 squares within 1e-9), RT-7 (moved 72/42 vs 70/41 by method), RT-9 (compute priced low), RT-10 (T-185 next rung), RT-11 (T-188 seed label #501 vs #575 digest; author question), RT-12 (#639 bears at 175/204/232/302, undecided at its print), RT-13 (PR #641 regularization debt per re-housed count).

2026-10-16 user-eb-review-185-190, ADOPTION TABLE (exact, sides rounded up at 16 places; case = verified ceiling on main e2e018f32). n: case house -> recommended house (margin below case; credit):
129: T-162 -> T-186 (1.19e-19; Polkovskyi after PingYou after Ostashev). 146: T-168 -> T-187 (1.38e-8; Daniel after Xu). 154: T-182 -> T-186 (1.29e-19; Polkovskyi after Couzo). 156: T-161 -> T-186 (1.30e-19; after PingYou after Couzo after Ostashev). 175: T-158 -> T-186 (1.38e-19; after PingYou after Ostashev; T-185 above the case by 2.94e-3). 176: T-165 -> T-186 (1.18e-2; after PingYou, Ostashev's #575 packing). 204: T-162 -> T-186 (1.48e-19). 211: T-182 -> T-188 (9.29e-6; Couzo after Ostashev, see RT-1). 232: T-158 -> T-186 (1.58e-19). 237: T-183 -> T-190 (1.01e-4; Couzo after Polkovskyi; T-189 2.40e-11 above T-190). 264: T-158 -> T-186 (1.68e-19). 271: T-161 -> T-186 (1.69e-19; ... after Chaoweeraprasit, RT-4). 302: T-181 -> T-186 (1.79e-19; after Couzo after PingYou). 303: T-162 -> T-186 (1.79e-19). 304: T-175 -> T-186 (1.79e-19; after Ostashev).
Other open reports: T-174 (PR #574, held for the owner) is above T-186 at all 9 counts they share (1.10e-21 to 1.25e-94), so the hold decides none of these houses; #639's algebraic sides bear at 175, 204, 232, 302 (agree with T-186 to the 25 digits printed; undecided; algebraic = no candidate until RP-3), decided nothing here. If PR #641 merges first, each of the 15 re-housed counts owes a regularization run or a deferral. Witness size: T-186's 12 facts 1.73 MB uncompressed vs 1.56 MB of current witnesses (no OR-18 concern like T-174's 18.5 MB).

2026-10-16 06:45Z user-eb-review-185-190: site edition: mapping the review changes SYNOPSIS.md (a site output), so the branch cuts site v0.7.15 (commit 9bd813b2b; claim documents byte-identical to main's with PUBLICATION_REVISION read back; explainer no-change record; README). PR #646 (codex/news-chooser-states) also cuts v0.7.15, so whichever merges second re-cuts. packing-validate --records --jobs 2 at 9bd813b2b: 52/52 steps, exit 0, 272 s. Hosted CI pending on PR #648.

2026-10-16 06:55Z user-eb-review-185-190: DONE. Draft PR #648 (https://github.com/jlevy/squares/pull/648, S2 + intake), head 9bd813b2b. Hosted CI green at 9bd813b2b: Packing validation (run 38862532632, 06:40Z-06:52Z) and Certificate page (run 38862532727) passed, Branch mergeability passed; 31 checks success, 52 deferred/deep-gate skipped, none failed. Site v0.7.15 collides with PR #646's v0.7.15: second to merge re-cuts. Not merged (not mine to merge). Records lane next (no bead yet).

2026-10-16T07:48Z user-eb-addr-648: addressing review A on PR #648 (worktree .claude/worktrees/addr-648, branch at 9bd813b2b). A1: keeping lane C's programs and outputs in packing/resources/web/mishapolk-kkt-refinements-2026-10-14/review/review-2026-10-16/ (adoption table re-run identical; third route re-running from the kept driver). Next: README, review-text fixes A2-A9, PR description.

2026-10-16T08:02Z user-eb-addr-648: pushed 885ee47a7 (kept lane C programs/outputs in packing/resources/web/mishapolk-kkt-refinements-2026-10-14/review/review-2026-10-16/; kept third-route driver re-run equal in every field but times) and 2ea1d00bb (review text: A1-A3, A5-A9 + fix-round addendum). Running packing-validate --records; next: PR description (A3, A4), disposition reply, CI watch.

2026-10-16T08:16Z user-eb-addr-648: review A on PR #648 addressed, A1-A9 all fixed (885ee47a7 kept programs/outputs; 2ea1d00bb review text; A4 in the PR description). Head 2ea1d00bb; records tier 52/52 exit 0; hosted CI green (Packing validation 38871024727, Certificate page 38871024676, Branch mergeability 38871018781). Disposition reply: https://github.com/jlevy/squares/pull/648#pullrequestreview-5544859331. Records lane (think-z7wn) branch is built on 9bd813b2b and does not yet have these two commits.

2026-10-16 ~08:25Z coordinator user-eb: PR #648 MERGE-READY at 2ea1d00bb (senior Review A 0/0/3/6, all nine fixed by user-eb-addr-648, disposition review https://github.com/jlevy/squares/pull/648#pullrequestreview-5544859331; the larger fix commit 885ee47a7, 37 files of the review lane's kept programs and logs under packing/resources/web/mishapolk-kkt-refinements-2026-10-14/review/review-2026-10-16/, checked inline by the coordinator: README states what decides what, largest file < 200 KB, precedent followed). Hosted CI green. Site v0.7.15 collision: lands through the records lane's PR (think-z7wn) or re-cuts at merge. Waits for the owner's word.
