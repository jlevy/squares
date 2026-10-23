---
type: is
id: is-01m4qjdm5hbj0m43ymvkcjr2jm
title: "Import Rio Calle: s(102) <= 10.605828696455852 (#529)"
kind: task
status: open
priority: 1
version: 9
delegate: null
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T08:07:15.376Z
updated_at: 2026-10-23T06:15:50.382Z
started_at: 2026-10-12T08:07:43.538Z
---
https://github.com/jlevy/squares/issues/529 (2026-10-12T04:32:54Z). riocalle/my-repo at 831368623f2d4dcef2e9434fd85c3e154083c97d: n102_s10.605828696455852.txt (decimal centres and radian angles), JSON and SVG copies, verify_exact.py (60-digit decimal, not exact). The author's exact certificate comes from a private engine; the record's exact certificate must be built here from the layout. Stages 1-2 and the stage 4 replay through devtools.upper_bound_reports.

## Notes

Issue: https://github.com/jlevy/squares/issues/529 (opened 2026-10-12T04:32:54Z by riocalle, label intake). New contributor.

## Stage 1 triage, 2026-10-12 lane U (branch intake-528-529 from l4 dead83f0e; not pushed)

Pin: riocalle/my-repo 831368623f2d4dcef2e9434fd85c3e154083c97d (tree 4895d7e9), its only commit, committed 2026-10-12T04:23:19Z (authored 04:18:55Z), the head when cloned at 2026-10-12T08:03Z and the commit the issue names. No licence file and no reuse terms: derived-only custody. The JSON and SVG copies state the same 102 binary64 triples as the .txt, in the same order (measured in scratch).

Claims the release makes, and their register map:
1. s(102) <= 10.605828696455852 from n102_s10.605828696455852.txt (centres in [0, s]^2, rotations in radians, 18 significant digits). A bound the record already beats: T-146 (Evan Daniel's regularization of ry-xu's packing, 10.6058286964315784) is 2.43e-11 below it, registered on main since 10 October (V3/C3), the case's house on layer 4 (#518) and pending adoption on main. Below T-125 (main's house, 10.6058286965106059) by 5.48e-11, as the issue says. Whether to register a certificate of a distinct arrangement that moves no case is a records-lane/owner decision; the register plan is prepared either way.
2. "Solved to the bottom of its valley ... s = 10.605828696431638" (README): an author report with no layout at that side; not certified here and not registerable. It is 6.0e-14 above T-146's side.
3. earlier/n102_s10.605828708.*: the previous layout (Davidebyzero/packing_squares_in_squares__tools#6, opened 2026-10-08T17:34:14Z, confirmed by the API). Above every ceiling; stays in the packet.
4. Lineage: same design as ry-xu's T-125; 40 of 102 squares coincide with ry-xu's turned 180 degrees, 62 moved, 7 by up to half a square; found independently ~10 h after ry-xu's 2026-10-08 00:03 UTC publication. Priority is ry-xu's, as the author says. To be measured with the third route's arrangement_gap/patch_lineage.
5. A private engine's exact rational-interval certificate: not public, cannot be replayed.
6. AI assistance: Claude wrote and ran the search, finishing, refinement and both checkers, under the author's direction.
7. T-120 (#419) is Evan Daniel's degree-8 algebraic side, 10.607174680176051125342523..., of Francisco Couzo's 26 September configuration, a different design (T-098 holds its rational ceiling 10.60717468017605112545...). #529 is 1.346e-3 below it; it says nothing about #529's arrangement, whose exact algebraic side nobody has computed.

Credit name: "Rio Calle", as asked. GitHub profile riocalle: name Rio Calle, bio names the University of New Hampshire; twitter_username is null and the listed social accounts are LinkedIn and Instagram only, so no Twitter/X handle found.

Validation plan (priced): the author's checker verify_exact.py was read (json, sys, decimal only; reads its argument, writes nothing) and run once from scratch on the .txt and once on the JSON: both print min wall clearance 2.002e-12, min pair gap 1.932e-12 over 931 close pairs, LEGAL. It rounds at 60 digits, so it is a diagnostic. The record's certificate is derived here by a new calle-txt adapter (every decimal exact as printed, side as printed, tan(theta/2) rounded down at 40 places by a decided interval enclosure) and decided on both maintained exact routes with controls, --workers 1: 3 jobs, priced by a scratch prototype at 35 s for the positive. Third route: needs an upstream reader for calle-txt (proposed to the records layer). W2 review.

## Stage 2 and the stage 4 replay, 2026-10-12 lane U (commit fda34049d on intake-528-529, not pushed)

Packet packing/resources/web/riocalle-n102-2026-10-12 (source key [Calle n102 2026-10-12]): derived-only, 11 files pinned, facts/n-102.yaml.gz written by upper_bound_reports derive from the checkout (calle-txt adapter, half_angle_places 40); acquire_source --check passes. The printed side 10.605828696455852 certifies, so no smaller side was searched for.

certify --workers 1: 3 jobs, the positive passes and both controls are refused on both routes, 30,906 pair decisions, 1 min 48 s; least wall clearance 2.002066e-12 and pair gap 1.932818e-12 on both routes. check --replay: equal, 2 min 20 s.

claims.json frozen against layer 4 dead83f0e: above T-146 (the house on layer 4) by 2.427e-11; below T-125 by 5.475e-11; below T-120 by 1.346e-3; the smallest is T-146.

Lineage (the third route's arrangement_gap/patch_lineage from a scratch driver): one to one with T-125 under a half turn, 40 squares within 1e-9 and none turned (the issue's 40), 62 moved, 19 beyond a tenth, the largest 0.494, 11 turned. Another arrangement of ry-xu's design, not a refinement.

Open: whether to register a certificate that moves no case; attribution.published 2026-10-12 (first commit) against the README's 11 October and the Davidebyzero#6 comment of 2026-10-11T23:06:09Z. Register plan: scratchpad lane-u/register-plan-529.yaml (its template wording "improvement" and the evidence's performed_by source-author need the records lane's rewording).

## Draft acknowledgement (not posted)

Thank you, Rio, and welcome. We received the layout at riocalle/my-repo 8313686 (n102_s10.605828696455852.txt, with its JSON and SVG copies). Since your engine's exact certificate is not public, we will build an exact certificate from the layout itself, every number exactly as printed and each square's half-angle tangent rounded to 40 places, and decide it on our exact routes with controls; we ran your verify_exact.py too, which reproduces your two gaps. We will also measure the packing against ry-xu's for the credit, which we will give as Rio Calle with ry-xu credited for the design and width, as you ask. One thing you should know first: since 10 October the record also holds Evan Daniel's exact regularization of ry-xu's packing at 10.6058286964315784, about 2.4e-11 below your side, so the comparison will name it.

## Stage 4 review (W2), 2026-10-12 review lane (branch review-528-529 from intake-528-529 fda34049d; commit 18843516c, not pushed)

Review: docs/project/reviews/review-2026-10-12-upper-bound-imports-528-529.md (shared with #528), mapped in the document map. Verdict: accepted, finite feasibility only, for the certificate derived here from the 8313686 layout; eleven findings, none blocking; V3/C3 once registered (as T-138 holds V3 on derived witnesses); S2 confirmed (the claim's side is above T-146's; T-120, T-137, T-150 are the comparators); the house at 102 stays T-146, this certificate retained and not selected, T-125 after it.

Replayed here: check --replay all 3 jobs equal (2 min 0 s, 10:11:34Z to 10:13:34Z); check-claims rebuilt equal as JSON. Third route: new reader read_calle_txt and decimal_literal (plain or scientific decimals, exact), half_angle_floor_radians (Taylor series in decimal arithmetic, no pi; refuses |theta| >= 3), derive_calle_txt (printed side undilated, options exactly half_angle_places), dispatched through DERIVED_READERS beside #470's derive_decimal_pose; CREDITED at 102 against T-125 and T-146. The certificate passes, 5,151 pairs (240 clipped), 6/6 sharp controls, wall clearance 2.002066e-12 at near and far walls, least Euclidean distance 1.932818e-12 = the maintained routes' pair gap, side 2651457174113963/(25*10^13) = the printed 10.605828696455852 exactly; --upstream derived the certificate again from the layout fetched at the pin (all 11 files at the manifest digests) and found it the fact basis for basis; the third route's floor equals the importer's interval floor at the layout's angles at 32 and 40 places. Credit measured: one to one with T-125 under a half turn, 40 within 1e-9 and none turned, 62 moved (61 beyond 1e-3, 42 beyond 1e-2, 19 beyond 1e-1, largest 0.494), 11 turned by up to a sine of 0.683; against T-146 under a quarter turn, 61 moved, 25 beyond a tenth. Another arrangement of ry-xu's design, not a refinement or regularization; no regularizations item.

Answers for the records lane (review, "Whether #529 Is Registered" and "The Dates and the Plan's Wording"): register it as T-155 (the scope clause of epistemics "Results by Others" is met: replayed and reviewed here; the stage 1 "no work" exclusion does not fit a filed request below main's house; the standing is derived: pending adoption on main, superseded by T-146 on layer 4; precedents Casson, #505's five, think-9fjl each turned on the author's request), with the lighter alternative stated for the owner (RX-1). attribution.published 2026-10-11, the date the source gives (README history and issue), not the first commit's 2026-10-12; bibliography dated stays 2026-10-12 (RX-2). Plan wording: "improvement" and the negative "below" reworded; E-calle-529-certificate-report typed as the source's numerical report (numerical-multiprecision, 60 digits, certificate = acquisition/sources.json) and the derived fact cited by E-calle-529-exact-feasibility only (performed_by repository, origin replayed-here), as E-mishapolk-470-pose-report does (RX-3). README says 17 significant digits, the file prints 18 (RX-9); the stated ~2e-12 margin is approximate for the pair gap (RX-10). The Davidebyzero#6 comment date (2026-10-11T23:06Z) could not be read from this session (API access not attached; the HTML page is 403); the published date rests on the source's own date, not on it. Corrected register plan (T-155 placeholder): scratchpad lane-u/register-plan-528-529-reviewed.yaml.

Validation: shared with #528's note (56 new test cases; packing-validate --records passes every step but the stale SYNOPSIS.md document map).

2026-10-16 ~06:45Z user-eb-intake-residue (lane A, think-mu5v): #529's final comment, rendered from main e2e018f32 with check_requests --draft 529 (greeting added). Checked first: the last reply is more than a day old with no author comment since, nothing the author asked for is queued, no think-l3oo decision touches it, and main and the deployed site (result pages read 06:30Z, deployment e2e018f32) state what it states. NOT POSTED: this session's permission system refused the GitHub comment and the close (auto-mode classifier, external system writes), so the post, the close and the record of the reply under #529's replies (kind final, with state/closed) are owed by whoever posts it. To post: gh api repos/jlevy/squares/issues/529/comments -X POST -F body=@FILE, then gh api repos/jlevy/squares/issues/529 -X PATCH -f state=closed -f state_reason=completed. Draft:

@riocalle, thank you. Where this request stands in the record on `main`.

**What is registered.**

- s(102) <= 10.605828696455852, the side of the layout as printed, certified here by an exact certificate derived from it; 5.5e-11 below T-125:
  - T-159, confirmed at V3/C3: re-verified here by an independent implementation (sqpack.verify, run by each case's verify_exact module and the packing-witness command, devtools.check_rational_witness_independent, devtools.evand_arrangement_reports, devtools.upper_bound_reports, devtools.check_half_angle_area, devtools.evand_exact_certificates).
  - E-calle-529-exact-feasibility, confirmed here: re-verified here by an independent implementation (sqpack.verify, run by each case's verify_exact module and the packing-witness command, devtools.check_rational_witness_independent, devtools.evand_arrangement_reports, devtools.upper_bound_reports, devtools.check_half_angle_area, devtools.evand_exact_certificates).

**Not registered.**

- Solved to the bottom of its valley the arrangement reaches s = 10.605828696431638 (README): No layout at that side is published; an author report, not certified here, and above T-146's side by 6.0e-14.
- s = 10.605828708, the author's earlier layout (earlier/, and Davidebyzero/packing_squares_in_squares__tools issue 6 of 2026-10-08): Above every ceiling at 102; retained by digest in the packet.
- The author's search engine's exact rational-interval certificate accepts the layout, and refuses it in a box 1e-11 smaller: Not public and not replayable; the record's certificate is derived from the layout instead.

**On `main`.** [`packing/frontier/RESULTS.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/RESULTS.md), [`docs/project/reviews/review-2026-10-12-upper-bound-imports-528-529.md`](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-12-upper-bound-imports-528-529.md), [`packing/frontier/n-102.md`](https://github.com/jlevy/squares/blob/main/packing/frontier/n-102.md).

Nothing you asked for is queued, so this issue is closed with this comment.

---
_Generated by [Claude Code](https://claude.ai/code)_

Correction (user-eb-intake-residue, 2026-10-16T05:47Z by date -u): the '~06:xxZ' times in this lane's notes of 16 October are about an hour late; they were written between 05:30Z and 05:47Z. The site pages were read at about 05:35Z. No condition changes: every last reply named is still more than a day old.
