---
type: is
id: is-01m4fm98aj8x6nkkakpcaqy6se
title: "Import evand: s(132) <= 11.98709933224506, s(155) <= 12.95249894401401 (#465)"
kind: task
status: closed
priority: 2
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4ekeq41zfgtf5dp8r462n05
hold: null
hold_until: null
created_at: 2026-10-09T06:05:53.874Z
updated_at: 2026-10-12T23:39:25.363Z
started_at: 2026-10-09T20:40:49.776Z
closed_at: 2026-10-12T23:39:25.363Z
close_reason: "#465 imported and answered: T-131 registered, n155 on T-128, issue closed 2026-10-12; beyond-corpus tilings moved to think-jtlq and Lean closed forms to think-63vx."
resolution: null
duplicate_of: null
---
New result reported on jlevy/squares#465 by Evan Daniel, certificates at evand/square-packing e008180. Also owns the unread evand/square-packing history dbcb4c4..ed01e0d (61 commits: #465 records; beyond-corpus s(964), s(1092), s(1228) at 49907ec; Lean closed forms for 62 quadratic register sides 7d047a9; Lean tiling statements; s12 flatten). Ledger entry for #465 with triage: pending names this bead.

## Notes

2026-10-09 cloud (post-430): import in progress on branch claude/import-evand-465 (from main d3860c97a).

2026-10-09: PR #478 (head c54fb4531, CI green): T-131 V0/C0 pending adoption at n132; n155 maps to T-128 (identical exact side, 152/155 poses shared); exact replay receipt retained; reply to #465 drafted (post after merge); evand watch read through ed01e0d (think-iyij named interim owner of the beyond-corpus tilings; swap to the follow-up bead before closing).


## Stage 7 draft from main at c6bf2d46f, 2026-10-11 — not posted (owner: leave as drafts)

Ledger: closeable (`check_requests --report` at c6bf2d46f: all three results settled, no ask queued; T-131's next rung says no house move is due, and adoption at 155 waits on #403 under think-fvz4, the project's own round). First draft for #465 (think-iyij's notes record a reply drafted on PR #478's branch, not kept in a bead); written from main. No case ceiling moved.

@evand, thank you. Both of your record-hunt certificates (e008180) are on `main`, confirmed, independently re-implemented.

- **n = 132** is registered as **[T-131](https://jlevy.github.io/squares/results.html#t-131), V3/C3**, through [PR #478](https://github.com/jlevy/squares/pull/478) and [PR #487](https://github.com/jlevy/squares/pull/487): s(132) ≤ 11.987099332245063227179742877435, the exact side your certificate states. It is below the ceiling the [n = 132 case record](https://github.com/jlevy/squares/blob/main/packing/frontier/n-132.md) holds, your exact optimum of Francisco Couzo's packing (T-098), by 84571108928763690161985083/20000000000000000000000000000, about 4.23e-03.
- **n = 155** states exactly the n = 155 side of Francisco Couzo's #451 certificate, s(155) ≤ 12.95249894401400738196585056694, registered as **[T-128](https://jlevy.github.io/squares/results.html#t-128), V3/C3**. Your certificate shares 152 of its 155 exact poses and differs exactly at the free square and the two flat-motion squares your report lists. It is recorded as further evidence on T-128, not as an entry of its own; no connecting motion or equivalence of the two local minima has been verified. T-128 is 4.26e-06 below the case's ceiling at 155.
- **Not registered:** the KKT, reduced-Hessian and corner-to-corner MILP statements are numerical evidence of local optimality, not a bound on s(n). They are recorded as your report and were not checked here.

**What came after.** At 132, later certificates are smaller than T-131: Francisco Couzo's #476 (T-134) and #488 (T-140), by 1.45e-04 and 1.46e-04, and your own Hunt 3 certificate of #489 (T-141), by 1.42e-03. The review of #488 and #489 recommends T-141 as the house at 132, so T-131 stays verified and no house move is due for it. At 155 the review recommends T-128 as the house, with Couzo's certificate, committed nine hours before yours, holding the case and yours kept as its equal-side confirmation.

No case ceiling has moved: the case records are unchanged for now. House adoption waits for [jlevy/squares#403](https://github.com/jlevy/squares/pull/403), which rewrites every case record; each case's house is chosen in that later adoption round.

**How it was checked.**
- All six retained jobs, the n = 132 and n = 155 positives each with a duplicate-square and an outside-container control, were decided again by both maintained exact routes, `sqpack.verify` and `devtools.check_rational_witness_independent`, and equal their retained rows: 123,486 pair decisions. Each positive clears its nearest wall by exactly 1/(2·10^20) and every pair by just under 1e-20.
- A third exact route, `devtools.check_half_angle_area` (half-extent containment and exact intersection area), decided both certificates with six controls each, with its own reader of your format.
- No route here is your code, so the confirmation is independently re-implemented. The two maintained routes share one parse and the half-angle conversion, which the third route's own reader closes, and all three share Fraction arithmetic. Your `verify_cert.py` and `verify_cert2.py` did not run here.
- A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-couzo-daniel-refinement-replays.md) reproduced the replay and accepted both certificates, and the [11 October final review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-11-final-upper-bounds.md), by a distinct AI reviewer, accepted T-131 and T-128 again. No human review is claimed.

This confirms finite feasibility only, not optimality.

**Credit.** T-131 credits you, from Francisco Couzo's packing, as your report says the certificate was reached from his packing by an uphill excursion. Your certificates, KKT points, inputs and solver reports are retained under your MIT licence.

Nothing you asked for is queued, so this issue is closed with this comment. If the adoption round changes what this comment says, a follow-up will note it.

---
_Generated by [Claude Code](https://claude.ai/code)_
