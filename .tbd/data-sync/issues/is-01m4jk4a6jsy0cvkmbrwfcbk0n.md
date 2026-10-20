---
type: is
id: is-01m4jk4a6jsy0cvkmbrwfcbk0n
title: "Import ebdeleeuw: s(70) <= 888096037156625096037155737/10^26, an exact refinement of Ryan Xu's packing (#483)"
kind: task
status: closed
priority: 1
version: 7
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T09:43:26.674Z
updated_at: 2026-10-12T23:39:06.548Z
started_at: 2026-10-10T09:49:27.373Z
closed_at: 2026-10-12T23:39:06.548Z
close_reason: "#483 imported and answered: T-137 registered and reviewed, issue closed 2026-10-12 with the final reply."
resolution: null
duplicate_of: null
---
Issue https://github.com/jlevy/squares/issues/483 (opened 2026-10-10). Refinement 1.4263e-10 below Ryan Xu's exact certificate side 88809603717088809603717/10^22. Source ebdeleeuw/square-packing-n70 at 24221d5e51244ca5290d5b1c43f1fbe36f9749e0; certificate.json SHA-256 eeebf55cf3c1614a96f51339695f28443e35f33b0195bfc24ef0549b50550cb1, centres in [-S/2,S/2]^2, half-angle tangents. Stages 1-3 and a maintained exact replay (seconds).

## Notes

2026-10-10 stage 1-2 lane (intake W1, branch worktree-agent-af22382952a5d839e, packet commit 17deb32be).

PIN: ebdeleeuw/square-packing-n70 24221d5e51244ca5290d5b1c43f1fbe36f9749e0 (tree 60b3fba53a2b752e13370c2c096e2851859122e6, committed 2026-10-10T02:04:48Z, the repository's only commit). Retrieved 2026-10-10T09:54Z. certificate.json SHA-256 eeebf55cf3c1614a96f51339695f28443e35f33b0195bfc24ef0549b50550cb1 = the issue's; verification.json's recorded digests match the certificate, export, log and checker. No licence file: derived-only custody.
PACKET: packing/resources/web/ebdeleeuw-n70-refinement-2026-10-10 (6 files pinned only; acquire_source --check: PACKET_MATCHES_ITS_CONTRACT).

CLAIM MAP: the release makes one claim. s(70) <= 888096037156625096037155737/10^26 = 8.880960371566251 (15 places, up). Case n-070 reported and verified ceiling: Ryan Xu 88809603717088809603717/10^22 = 8.880960371708881 (T-125, E-ryxu-432-rational-feasibility). Below by exactly 14263000000014263/10^26 = 1.4263e-10, as the issue states. No other pending report at 70 (#465, #470, #476, #481, #484 checked). Smallest: #483.
Register action proposed: a new upper-bound entry at n = 70, published 2026-10-10, crediting Ryan Xu's arrangement and ebdeleeuw's refinement.

FORMAT (for the importer's centred-JSON adapter): JSON {schema: "sqpack-rational-v1" (the source's own label, not a repository format), n: 70, coordinate_system: "centered", side "p/q", squares: [{x, y, t}, ...]} rational strings, box [-S/2, S/2]^2, cos=(1-t^2)/(1+t^2), sin=2t/(1+t^2).

PRICE: a timing probe of sqpack.verify.verify_packing found the certificate valid, 2,415 pairs in 0.18 s. A two-route replay with two controls: seconds. Not a recorded replay.

## Draft acknowledgement (2026-10-10, not posted; the owner posts it)

Thank you. We received the n = 70 certificate and pinned ebdeleeuw/square-packing-n70 at 24221d5e51244ca5290d5b1c43f1fbe36f9749e0; `certificate.json` has the SHA-256 you give. Its side is exactly 14263000000014263/10^26 below Ryan Xu's certificate, which the case holds in both lanes today, and no other pending report names n = 70. The repository has no licence, so we keep digests and derived facts rather than the files. Next we will replay the certificate exactly (centred box, rational half-angle tangents) by two maintained exact routes with duplicate-square and outside-container controls, and review the replay. Credit will read Ryan Xu's arrangement, refined by you, with the Codex assistance you disclose.

## Stage 7 draft (2026-10-10, to post after PR #487 merges; not posted)

Supports posting after merge: yes (facts checked against PR #487's head 6fb495b3a; post once the merge's Pages deployment shows the T-137 row, and recheck the id if anything else merges first). Ledger: closeable (check_requests --report: the one result settled, no ask queued; house adoption at 70 waits on PR #403 under think-fvz4, the project's own round, not an ask of the author).

@ebdeleeuw, thank you. Your n = 70 certificate is registered on `main` as **[T-137](https://jlevy.github.io/squares/all-results.html#t-137), V3/C3**, confirmed, through [PR #487](https://github.com/jlevy/squares/pull/487).

- **The bound:** s(70) ≤ 888096037156625096037155737/10^26 = 8.88096037156625096037155737, the exact side `certificate.json` states. The record pins ebdeleeuw/square-packing-n70 at 24221d5e51244ca5290d5b1c43f1fbe36f9749e0, and the file has the SHA-256 your issue gives.
- **Against the case:** it is below the ceiling the [n = 70 case record](https://github.com/jlevy/squares/blob/main/packing/frontier/n-070.md) holds, Ryan Xu's certificate (T-125), by exactly 14263000000014263/10^26, as you state. No other pending report names n = 70.

The case record is unchanged for now. House adoption waits for [PR #403](https://github.com/jlevy/squares/pull/403), which rewrites every case record, and for a custody record of the replay workers; the case's house is chosen in that later adoption round. The review recommends T-137 as the house at 70, crediting Ryan Xu's arrangement as refined by you, with Ryan Xu's certificate kept as history.

**How it was checked.**
- Your repository has no licence, so the record keeps digests and an exact fact derived from the pinned certificate rather than your files. The fact moves every centre by exactly half the side, from your centred box to [0, S]^2.
- Both maintained exact routes, `sqpack.verify` and `devtools.check_rational_witness_independent`, decided the positive with a duplicate-square and an outside-container control, and equal their retained rows: 3 jobs and 14,490 pair decisions. The certificate clears every wall by at least 6.01e-13 and every pair by at least 1.20e-12.
- A third exact route, `devtools.check_half_angle_area` (half-extent containment and exact intersection area), decided it with six controls, four of them sharp. It also held the derived fact to the packing your pinned file states.
- No route here is your code, so the replay is independently re-implemented. The two maintained routes share one parse, the half-angle conversion and the separating-axis method, and all three share Fraction arithmetic. Neither your `verify_exact.py` nor David Ellsworth's `check_packing.py` ran here.
- A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-upper-bound-imports-476-481-483-484.md) reproduced the replay and found no blocking defect. No human review is claimed.

This confirms finite feasibility only, not optimality, and no lower bound changes.

**Credit.** T-137 credits you for the refinement and the rational certificate, after Ryan Xu's arrangement and his published warm-start coordinates (#432), as you ask.

Nothing you asked for is queued, so this issue is closed with this comment. If the adoption round changes what this comment says, a follow-up will note it.

---
_Generated by [Claude Code](https://claude.ai/code)_


## Stage 7 draft from main at c6bf2d46f, 2026-10-11 — not posted (owner: leave as drafts)

Ledger: closeable (`check_requests --report` at c6bf2d46f: the one result settled, no ask queued). Supersedes the 10 October draft above: since PR #487's head 6fb495b3a, T-146 holds a smaller side at 70 (by 1.07e-11) and the house recommendation at 70 moved to it, crediting Ryan Xu, with T-137 named as the smallest side the record held (owner's credit decision of 11 October); the 11 October final review is a second accepted review; links point at `results.html`. No case ceiling moved.

@ebdeleeuw, thank you. Your n = 70 certificate is registered on `main` as **[T-137](https://jlevy.github.io/squares/results.html#t-137), V3/C3**, confirmed, independently re-implemented, through [PR #487](https://github.com/jlevy/squares/pull/487).

- **The bound:** s(70) ≤ 888096037156625096037155737/10^26 = 8.88096037156625096037155737, the exact side `certificate.json` states. The record pins ebdeleeuw/square-packing-n70 at 24221d5e51244ca5290d5b1c43f1fbe36f9749e0, and the file has the SHA-256 your issue gives.
- **Against the case:** it is below the ceiling the [n = 70 case record](https://github.com/jlevy/squares/blob/main/packing/frontier/n-070.md) holds, Ryan Xu's certificate (T-125), by exactly 14263000000014263/10^26, as you state. When T-137 was registered, no other report named n = 70.
- **Since then:** Evan Daniel's regularized certificate at 70 (T-146) is smaller than yours, by 1.07e-11. It regularizes Ryan Xu's packing, and its sixty unmoved squares sit at Ryan Xu's poses to 1e-9 and at yours to 1e-8, so T-146 credits the packing to Ryan Xu and names your refinement as the smallest side the record held before it. T-137 stays verified.

No case ceiling has moved: the case record is unchanged for now. House adoption waits for [jlevy/squares#403](https://github.com/jlevy/squares/pull/403), which rewrites every case record, and for a custody record of the replay workers; the case's house is chosen in that later adoption round. The house recommendation at 70 now goes to T-146, with Ryan Xu's certificate kept as history.

**How it was checked.**
- Your repository has no licence, so the record keeps digests and an exact fact derived from the pinned certificate rather than your files. The fact moves every centre by exactly half the side, from your centred box to [0, S]^2.
- Both maintained exact routes, `sqpack.verify` and `devtools.check_rational_witness_independent`, decided the positive with a duplicate-square and an outside-container control, and equal their retained rows: 3 jobs and 14,490 pair decisions. The certificate clears every wall by at least 6.01e-13 and every pair by at least 1.20e-12.
- A third exact route, `devtools.check_half_angle_area` (half-extent containment and exact intersection area), decided it with six controls, four of them sharp. It also held the derived fact to the packing your pinned file states.
- No route here is your code, so the replay is independently re-implemented. The two maintained routes share one parse, the half-angle conversion and the separating-axis method, and all three share Fraction arithmetic. Neither your `verify_exact.py` nor David Ellsworth's `check_packing.py` ran here.
- A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-upper-bound-imports-476-481-483-484.md) reproduced the replay and found no blocking defect, and the [11 October final review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-11-final-upper-bounds.md), by a distinct AI reviewer, accepted the entry again. No human review is claimed.

This confirms finite feasibility only, not optimality, and no lower bound changes.

**Credit.** T-137 credits you for the refinement and the rational certificate, after Ryan Xu's arrangement and his published warm-start coordinates (#432), as you ask.

Nothing you asked for is queued, so this issue is closed with this comment. If the adoption round changes what this comment says, a follow-up will note it.

---
_Generated by [Claude Code](https://claude.ai/code)_
