---
type: is
id: is-01m54ahp501b4as4q1gfw9yqxr
title: "Import Evan Daniel: s(271) <= 16.948947733714, refining Couzo's #561 packing 4.46e-5 below T-186 (#664)"
kind: task
status: in_progress
priority: 1
version: 11
delegate: c-lane-692
labels:
  - result-import
dependencies: []
parent_id: is-01m549eweq3c13b32tjzbf0ats
hold: null
hold_until: null
created_at: 2026-10-17T06:59:47.488Z
updated_at: 2026-10-20T02:06:40.709Z
started_at: 2026-10-18T08:47:56.026Z
---
Evan Daniel (@evand) reports s(271) <= 16.948947733714 on jlevy/squares#664 (filed 2026-10-17T04:30:51Z): the exact rational side 16948947733713657510723401112423/10^30 of evand/square-packing 757b40bc6c5f681033ff1572177d408afbf26dfe (committed 2026-10-17T04:29:03Z), search/packer/candidates/s271_ex1.cert, rounded up at 12 places. Found by the 17 October intake pass (think-e2sz), lane W (user-eb-sweep-1017). Stage 1 triage below; stages 2 to 4 are this bead's, in an import lane the coordinator assigns.

## Triage (stage 1, 2026-10-17, read-only)

**Pin.** evand/square-packing 757b40bc6c5f681033ff1572177d408afbf26dfe, the head and the commit the issue names. It adds search/packer/candidates/s271_ex1{.cert,.exact.txt,.input.txt,.json,_prior.json,_regularized.cert,_regularized.json,_vs_prior.json}. The source checkers are search/exact/verify_cert.py and verify_cert2.py (last changed at dbcb4c4). SHA-256 measured here: s271_ex1.cert 48abf7ca68909c42e0aaa5215d4d578f4cdba29d6188775012ae24636e02d680 and s271_ex1_regularized.cert 4d4d4e25604b2c492047b44144249e3d69be53db061ab51e26dab39e8fb12160, both matching the issue. The header line reads `271 16948947733713657510723401112423/1000000000000000000000000000000`.

**Claims (every claim the issue makes).**
1. s(271) <= 16.948947733714, the certificate side rounded up at 12 places. The issue gives the "best public before it" as 16.948992356451 (Couzo #561, refining Nate Chaoweeraprasit's SQUISH packing #500; also #586, #593), an improvement of 4.46e-5. Its comparison covers the register at main 6a3a7d8f, the issues through #659 and Ellsworth's catalogue, through the monotone envelope, checked on 16 October.
2. Both source checkers accept both files (separating axes and polygon intersection; exact rational, standard library; same author and format).
3. s271_ex1_regularized.cert is the same packing at the same side, regularized for display with 21 angle groups. It is a display view.
4. In the issue's words, "This is a refinement of the #561 packing, not a new construction". The load-bearing tilt angles match #561's group for group within 0.12 deg, except that #561's four squares near 31.7 to 32.0 deg are three here (67 load-bearing tilted squares against 68). Its KKT point is strict modulo 54 flat motions (#561: 56), with no MILP descent. It has 116 + 1488 contact equations (#561: 116 + 1493), 259 corner-to-corner contacts (#561: 262), 4 rattlers (#561: 4), and 69 tilted squares (#561: 70). Under the optimal assignment, 59 load-bearing squares move by more than 1e-4 and 2 by more than 1e-2 (max 0.391). The comparison data is s271_ex1_vs_prior.json. The commit message calls it "a distinct local minimum, 4.46e-5 below".
5. How it was found: the basin explorer (explore.py: fixed-side perturbation moves and re-polish) started from the register's 271 witness as one of 52 counts in a test run. One move swapped the tilt angles of two neighbouring squares 90 seconds in, and exactsolve.py certified the point. Credit request: "Please credit Francisco Couzo's #561 packing and Nate Chaoweeraprasit's SQUISH packing it refines."
6. AI assistance: the commit carries Co-Authored-By Claude Opus 5.5 and a Claude-Session trailer, and was "approved by Evan".
7. Not claimed: a closed form, interval local optimality, optimality.

**Map to the register.** One new entry, s(271) <= 16948947733713657510723401112423/10^30. Who else holds 271:
- the house is T-186, Mishapolk's 70a033f KKT refinement, in both case lanes at the 112-digit 16.94899235645120561 (credited found_by itsnaka, improved by Couzo, PingYou Ltd, Mishapolk);
- T-174 (PR #574) refines #561;
- T-161 is Couzo's #561;
- T-151 is itsnaka's #500;
- #593 was not recorded.

The exact difference from both case lanes is 4.4622737548e-5. No other open report states a bound at 271.

**Report order (devtools.intake_ledger).** In the 14 October ledger, #561 was recorded, PR #574 recorded, and #593 not recorded. T-186's 70a033f, a watched-repository publication, holds the house now. #664 (2026-10-17T04:30:51Z; certificate first committed 04:29:03Z) is the latest report. It is below every member by 4.46e-5, which the prints decide: **recorded**.
- Classification, an owner question. The source calls it "a refinement of the #561 packing", which the ledger would class as `refines` and the register would credit as a regularization of Couzo's packing (stage 3). But it is a different local minimum with one fewer load-bearing tilted square and a tilt swap, not the same configuration with a tighter certificate.
- The ledger README's "identity measured against what the source says" item lists it for the owner: whether it is a refinement credited as a regularization, or a new packing continuing Couzo's #561 arrangement. Either way it is recorded, and the credit names Daniel after Couzo after Chaoweeraprasit.

**Validation price (stage 4).**
- Replay: the two maintained exact routes (devtools.upper_bound_reports <packet> certify --workers 1, check --replay) with duplicate-square and outside-container controls. Estimate: about 75 route CPU-seconds, scaling T-187's 21.14 s at 10,585 pairs to 36,585 pairs.
- Source checkers: verify_cert.py and verify_cert2.py from the retained copy, minutes, unmeasured.
- Total: well under 0.1 CPU-h, so it runs in the import lane. No W7 slice is needed.
- Review: stage 4's review of the replay.

**House rule.** Yes. Once V3/C3 with an accepted review, it is below the house (T-186) by 4.46e-5, so select_houses moves 271 to it. The adopting PR regularizes 271: Evan Daniel's driver and grid-slack at 0.5, 1 and 5 degrees, about 0.2 CPU-h, then regularize_select. The author ships a 21-group regularized view at the same side.
- 271 is not staged for T-174 and no open PR moves it.
- Today's drawing at 271: regularized, a grid-slack 0.5-degree view (run grid-slack-z7wn-b-deg05-1016) at 6 light / 10 uneven / 0 near-axis, 23 classes / 19 hues. That view lapses with the house.

**Draft significance:** S2, a refinement (or a near arrangement) of Couzo's packing 4.46e-5 below the case ceiling. No lower bound and no optimum.

**Draft acknowledgement (not posted; after the PR carrying this triage merges, no T-NNN):**

> @evand, thank you. We have your s(271) certificate at `757b40b` (`search/packer/candidates/s271_ex1.cert`, SHA-256 `48abf7ca…`, matching the issue). Its exact side is 16948947733713657510723401112423/10^30, which rounds up to your 16.948947733714: 4.46e-5 below the case's standing side at 271 (Mishapolk's exact refinement of Francisco Couzo's #561 packing, 16.94899235645120561…). Under the owner's report-order rule it is the latest report at 271 and will be recorded, crediting Couzo's #561 packing and Nate Chaoweeraprasit's SQUISH packing it refines. One question for the record: your comparison shows one fewer load-bearing tilted square and a tilt swap. Is it the same configuration as #561 with a tighter side (which we would credit as a regularization of Couzo's packing), or a nearby arrangement found from it? Next: we retain the certificate with your two checkers, replay it on this repository's two exact routes, and register it in a records pull request. We will reply with its id and rungs then. Once validated it becomes the house at 271, and the case's drawing is regularized in the same change.

## Notes

2026-10-17 user-eb-sweep-1017: triage recorded in the description (stage 1, read-only). This import waits on nothing; the issues and pull requests the description cites are sources and holders, not blockers.
blocked_on: none

2026-10-18 W1 intake (think-xmxb): PR667 A8 corrected: #593 (and issue-referenced #586) state271; T-186 registers #593 KKT refinement. Stage3 ledger must include them. Triage verdict is provisional until ledger rendering. ReviewA2 asserts an owner credit answer, but fetched review text is not fresh consent; preserve question pending trusted current-conversation evidence. No packet/replay/house change yet.

2026-10-19 20:53Z lane-new: taken over from the 19 October handoff (issue #684) by the coordinator's lane brief; delegate changed from the spud10.local agent. Working in worktree scratchpad lnew/wt, branch claude/intake-2026-10-19-evand-singles (first PR: #659, #664, #669, #673).

2026-10-19 21:40Z lane-new: stage 2 and 3 committed and pushed, d7413ccdb on claude/intake-2026-10-19-evand-singles: packet (evand-n236-2026-10-16 / evand-n271-2026-10-17) retained by acquire_source at the issue pin, import declaration, certify receipt on both maintained routes (positive + 2 controls), check --replay passed, registered at V0/C0 as T-218 (236) / T-219 (271) [ids provisional: lane-680 also holds T-218; whichever PR merges second renumbers]. Stage 4 review requested from the coordinator (review branch claude/review-2026-10-19-evand-659-664-669-674). Adoption at the count written locally, strong regularizer runs under think-ip1p in progress.

2026-10-19 22:23Z lane-new: V3/C3 after the 19 October review (0466eb5aa); house adopted at the count (be6aa80aa, claude/intake-2026-10-19-evand-singles); regularization runs under think-ip1p finishing.

2026-10-20 lane-new: PR #692 opened (head f76d57a40, base 028bc72ec) with records, adoption at 155/229/236/271, regularization (think-ip1p), explainer v0.4.9 and site v0.7.36. packing-validate --records passes 52 steps at the head; --push is running. Senior review requested via the coordinator. Stage 7 reply waits for the merge and check_published_site.

2026-10-20 lane-new: PR #692 head e877e19ad. The first CI run at f76d57a40 found adoption follow-ups: sweeps checkout, censuses, translation screen, PR 574 claims, n-155 closed form, bibliography Levy suffix, test golden counts. They are fixed in 9b0c82d82 and a8222aad4. main b16ddeb0a (#691) is merged and the worker snapshot pruned of the 229 review SVG. v0.7.36 is re-cut last. --records passes 52/52.
