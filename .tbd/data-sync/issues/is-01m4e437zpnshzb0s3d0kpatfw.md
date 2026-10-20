---
type: is
id: is-01m4e437zpnshzb0s3d0kpatfw
title: "Import Francisco Couzo: eight exact rational refinements (#451)"
kind: task
status: in_progress
priority: 2
version: 6
delegate: codex-import-refinement-worker
labels:
  - result-import
dependencies: []
child_order_hints:
  - is-01m4egpftfmkrdfn0ygnhdkeqy
hold: null
hold_until: null
created_at: 2026-10-08T16:03:45.269Z
updated_at: 2026-10-12T23:40:33.966Z
started_at: 2026-10-08T16:04:43.643Z
---
GitHub issue https://github.com/jlevy/squares/issues/451 created2026-10-08T15:53:07Z reports eight complete exact rational certificates at105,108,127,131,155,180,228,306, from franciscouzo/square-packing@ffd900dfff6d2674ad995359208c2f0714915c82. Read-only first slice: acquire all eight certificates and decimal poses with immutable provenance, inspect licensing/format/source checker relations, compare both current exact frontier lanes, and price a complete existing-maintained dual-native positive/duplicate/outside protocol. Preserve Ryan Xu, Nate Chaoweeraprasit, Gupta refinement and Couzo/Evan construction credit and every superseded source/history. No author code, local native execution, clone, registry edits, confirmation or publication until coordinator's next scoped slice. Retained issue/comment inventory is /Volumes/spud-ext1/source-worktrees/squares-import-resume/review-notes/result-intake-2026-10-08T1600Z.json. Related419 update will be compared to already-retained f58a017 source; its existing think-8sm2 owner is preserved. New413 pattern33 status is source-only with no generated certificate and grants no exclusion credit.

## Notes

Coordinator continuation checkpoint 2026-10-08: all eight complete source packets and original serial24-job/48-outcome replay plus actual private custody are retained as source-only T128 V0/C0/S3 in draft intake PR https://github.com/jlevy/squares/pull/460 at e1c4fa8d38cfe8f45448d492979bc19e6f17c0a0, formal430 after459. Complete packet/adapters/tests unchanged from independently reviewedef826; all parent selected cases/houses/atlas exact. Native398.40s and custody38.36s (call8.91) are original executions, not new merge runs. Normal parent merge, generated evidence465 total and separate maintained DATApin34dc145e23f4.49/107 records PASS49.64s wrapper50.15, unchanged300s unarmed nonreference10CPU2jobs1inner. Live=Git199834532B under201326592 unchanged cap. Source-house history integration and standing adoption remain open; exact-head CI/published reviews and lower page fixes pending. No author programs executed.


## Stage 7 draft from main at c6bf2d46f, 2026-10-11 — not posted (owner: leave as drafts)

Ledger: closeable (`check_requests --report` at c6bf2d46f: both results settled, the credit ask done). Replaces the 10 October draft in think-mtwe, which reported T-128 and T-130 at V0/C0: PR #487 raised both to V3/C3 on the 10 October review, and the 11 October final review accepted them again. Raw `--draft 451` names `devtools.evand_exact_certificates` and `devtools.evand_arrangement_reports` among the re-verifiers; they check premises and decide nothing (verifiers.yaml), so this text names only the deciding routes, and it keeps RD-4 (one maintained route is the author's copied checker). No case ceiling moved.

@franciscouzo, thank you. Both of your reports are registered on `main` at the exact sides they state, and both are now confirmed, independently re-implemented:

- **[T-128](https://jlevy.github.io/squares/results.html#t-128), V3/C3:** the eight certificates at n = 105, 108, 127, 131, 155, 180, 228 and 306 (ffd900d), registered through [PR #460](https://github.com/jlevy/squares/pull/460): s(105) ≤ 10.790618268107144505815379335866, s(108) ≤ 10.904821012320356429055628704222, s(127) ≤ 11.810878787589179839642367108002, s(131) ≤ 11.951105389414677460694240669403, s(155) ≤ 12.95249894401400738196585056694, s(180) ≤ 13.916993522477832483558124720393, s(228) ≤ 15.604601475729674284720634102188 and s(306) ≤ 17.963433717491425739593840075522.
- **[T-130](https://jlevy.github.io/squares/results.html#t-130), V3/C3:** the five follow-up certificates from your comment on PR #460, at n = 84, 86, 105, 175 and 270 (2d32a6e), registered through [PR #469](https://github.com/jlevy/squares/pull/469): s(84) ≤ 9.697934799014921307163820128651, s(86) ≤ 9.820535407496742209971278280039, s(105) ≤ 10.789303783748158831034729697921, s(175) ≤ 13.767155163542549110085664417048 and s(270) ≤ 16.9367230228761834072968722597.

Both were confirmed through [PR #487](https://github.com/jlevy/squares/pull/487).

**Which cases they hold.** Each side is below the ceiling its case record holds. The review recommends T-130 as the house at 84, 86 and 105, and T-128 at 108, 127, 155, 180, 228 and 306. At the other counts a smaller certificate is known, and yours stays verified and not selected there:
- at 105, your own T-130 is smaller than T-128, by exactly 262896871797134956129927589/200000000000000000000000000000;
- at 131, SQUISH's #481 (T-136) is smaller than T-128;
- at 175, your own #488 (T-140) is smaller than T-130, by 3.44e-05;
- at 270, your #488 (T-140), SQUISH's #481 (T-136) and your #476 (T-134) are smaller than T-130.

Mishapolk's #470 (T-138) prints a larger side than yours at all ten counts you share. Evan Daniel's #465 certificate at n = 155 states exactly your T-128 side there and shares 152 of its 155 exact poses; it is recorded as further evidence on T-128, and your certificate, committed nine hours earlier, holds the count.

No case ceiling has moved: the case records, for example [n = 84](https://github.com/jlevy/squares/blob/main/packing/frontier/n-084.md) and [n = 108](https://github.com/jlevy/squares/blob/main/packing/frontier/n-108.md), are unchanged for now. House adoption waits for [jlevy/squares#403](https://github.com/jlevy/squares/pull/403), which rewrites every case record, and, for T-130, for a custody record of the replay workers; each case's house is chosen in that later adoption round, with the certificates it replaces kept as history: Ryan Xu's at 84, 86, 105, 108, 127 and 175, SQUISH's at 155, Siddharth Gupta's at 180, and Evan Daniel's at 228 and 306.

**How it was checked.**
- T-128: all 24 retained jobs, the eight positives each with a duplicate-square and an outside-container control, were decided again by both maintained exact routes, `sqpack.verify` and `devtools.check_rational_witness_independent`, and equal their retained rows. The private worker also passed complete stored-input admission with six late mutations.
- T-130: all 15 retained jobs, the five positives with their controls, were decided again by both routes and equal their retained rows: 384,846 pair decisions.
- A third exact route, `devtools.check_half_angle_area` (half-extent containment and exact intersection area), decided all thirteen certificates with six controls each. Every positive clears its nearest wall by exactly 1/(2·10^20) on all three routes.
- Your `verify.py` is a copy of this repository's `sqpack` verifier, so one maintained route is your own check. The independent re-implementation rests on the rational corner checker and the third route. The two maintained routes share one parse and the half-angle conversion, and all three share Fraction arithmetic. Evan Daniel's `verify_cert.py` did not run here.
- A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-couzo-daniel-refinement-replays.md) reproduced the replays and found no blocking defect, and the [11 October final review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-11-final-upper-bounds.md), by a distinct AI reviewer, accepted both entries again. No human review is claimed.

This confirms finite feasibility only, not optimality.

**Credit.** As you asked, the constructions you started from are credited: T-128 reads Couzo after Xu, Chaoweeraprasit, Gupta, Ellsworth, Daniel and Levy, and T-130 reads Couzo after Xu, Daniel, Ellsworth and Levy. Both name David Ellsworth's `refine_packing`, your basin hopping and Evan Daniel's `fq` and exact contact solver.

Nothing you asked for is queued, so this issue is closed with this comment. If the adoption round changes what this comment says, a follow-up will note it.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-12 reconciliation: #451 received its final reply (6127528255) and closed on 2026-10-12; T-128 is V3/C3 on main. Close this bead when think-0mlq (adoption) closes.
