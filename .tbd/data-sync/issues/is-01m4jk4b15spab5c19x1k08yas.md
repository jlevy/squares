---
type: is
id: is-01m4jk4b15spab5c19x1k08yas
title: "Import Francisco Couzo: certificates at n = 132, 237, 263, 267, 270, 303 (#476)"
kind: task
status: closed
priority: 1
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
hold: null
hold_until: null
created_at: 2026-10-10T09:43:27.525Z
updated_at: 2026-10-12T23:39:28.519Z
started_at: 2026-10-10T09:49:25.990Z
closed_at: 2026-10-12T23:39:28.519Z
close_reason: "Completed: #476 imported, registered as T-134, answered and closed (issue closed 2026-10-12); request entry closed on main."
resolution: null
duplicate_of: null
---
Issue https://github.com/jlevy/squares/issues/476 (opened 2026-10-09). Five exact optima from Evan Daniel's exact contact solver (132, 237, 267, 270, 303) and a rational witness at 263, in franciscouzo/square-packing certificates/ at 02f969075f79d5e13fa21e09e381a44e8647b452, Evan Daniel's .cert format. Overlaps #465 (T-131) at 132, #481 at 237, 263, 270, 303, and #470 at 132 and 267. Stages 1-3 and maintained exact replays.

## Notes

2026-10-10 (sub-agent lane, commit 1f9ee1606): stage 2 packet packing/resources/web/couzo-exact-certificates-2026-10-09/ at 02f969075f79 (no licence; all 65 certificates retained as factual data under the 2026-10-09 owner decision; READMEs and 65 decimal poses pinned only). All six #476 sides round up to the issue's 12-place prints; all six first committed in 02f9690 (2026-10-09T20:28:52Z), so attribution.published 2026-10-09. claims.json compares all 65: smallest at 132 and 267 is this certificate; at 237, 263, 270 and 303 issue #481's sides are smaller. Of the 59 unnamed certificates: 23 equal their case ceiling (22 T-098, 1 T-127), 11 are byte-identical to T-128 (7) or T-130 (4) certificates and below their cases, 5 are above their cases (68, 102, 103, 272, 292), 20 are beyond the horizon (15 below the tracked row, including 375 by 4.29e-5 and 378 by 4.00e-4; 5 rational witnesses above it, 327, 335, 342, 364, 372). Replay of 17 counts (the six plus 68-131): 51 jobs, all pass/refuse as required; receipt receipts/exact-certification.json.xz. register-plan printed; nothing registered. Remaining: stage 3 records (coordinator), and any beyond-horizon updates under think-1545.

## Stage 7 draft (2026-10-10, to post after PR #487 merges; not posted)

Supports posting after merge: yes (facts checked against PR #487's head 6fb495b3a; post once the merge's Pages deployment shows the T-134 row, and recheck the id if anything else merges first). Ledger: closeable (check_requests --report: the one result settled, no ask queued; house adoption at 267 waits on PR #403 under think-fvz4, the project's own round, not an ask of the author).

@franciscouzo, thank you. Your six certificates are registered on `main` as **[T-134](https://jlevy.github.io/squares/all-results.html#t-134), V3/C3**, confirmed, through [PR #487](https://github.com/jlevy/squares/pull/487), at the exact sides they state:

- s(132) ≤ 11.986954193640392741450366579623
- s(237) ≤ 15.903670905580623014470917594172
- s(263) ≤ 7488939206954142477014939239/447356905819500000000000000, which is 16.7404126538191566 rounded up at 16 places
- s(267) ≤ 16.838815269948262260434481342204
- s(270) ≤ 16.936720031121015799532991452837
- s(303) ≤ 17.917443925494235891916989336536

**Which cases they hold.** Each side is below its case's verified ceiling: by 4.37e-03 at 132, 5.33e-06 at 237, 7.03e-06 at 263, 1.67e-05 at 267, 1.09e-03 at 270 and 2.87e-03 at 303. At 267 yours is still the smallest side known, below Ryan Xu's certificate that the case holds (T-125). At the other five, certificates that arrived after yours are smaller:
- SQUISH's #481 (T-136) at 237, 263, 270 and 303;
- your own #488 (T-140) at 132, 237 and 270;
- Evan Daniel's #489 (T-141) at 132.

The case records, for example [n = 267](https://github.com/jlevy/squares/blob/main/packing/frontier/n-267.md), are unchanged for now. House adoption waits for [PR #403](https://github.com/jlevy/squares/pull/403), which rewrites every case record, and for a custody record of the replay workers; each case's house is chosen in that later adoption round. The reviews recommend T-134 as the house at 267. At the other five it stays verified and is not selected.

**How it was checked.**
- All 51 jobs of the packet's 17-count replay were decided again by both maintained exact routes, `sqpack.verify` and `devtools.check_rational_witness_independent`, and equal their retained rows. The 17 counts are the six you name and eleven others from the same commit, each a positive with a duplicate-square and an outside-container control; together they make 1,486,686 pair decisions.
- A third exact route, `devtools.check_half_angle_area` (half-extent containment and exact intersection area), decided the six with six controls each, four of them sharp: exact contact accepted, and 10^-40 to 10^-30 past it refused.
- Your issue reports a pass from a copy of this repository's `sqpack` verifier, so one maintained route is your own check. The independent re-implementation rests on the rational corner checker and the third route. The two maintained routes share one parse, the half-angle conversion and the separating-axis method, and all three share Fraction arithmetic.
- Evan Daniel's `verify_cert.py` did not run here, and the KKT and no-descent statements were not checked.
- A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-upper-bound-imports-476-481-483-484.md) reproduced the replay and found no blocking defect. No human review is claimed.

This confirms finite feasibility only, not optimality.

**Credit.** As you ask, T-134 credits the packings each certificate started from: Mishapolk's at 132, Nate Chaoweeraprasit's SQUISH packings at 237, 263 and 303 (237 through Siddharth Gupta's refinement), Ryan Xu's at 267 and Evan Daniel's at 270. The issue quotes Mishapolk's sides at 132 and 267 as 11.986956226077 and 16.838828608311, which match neither of his files. The record compares the 12-place prints of his README, 11.986956226066 and 16.838828608296, and your certificates are below both.

**The rest of the commit.** The 65 certificates at 02f9690 are retained as factual data; the READMEs and decimal pose files are pinned by digest only, since the repository states no licence. The 59 certificates the issue does not name are compared with the record in the packet, and each is an import of its own. Twenty of them lie beyond n = 324, and fifteen of those are below the beyond-horizon rows the record tracks; updating those rows is a separate queued item.

Nothing you asked for is queued, so this issue is closed with this comment. If the adoption round changes what this comment says, a follow-up will note it.

---
_Generated by [Claude Code](https://claude.ai/code)_


## Stage 7 draft from main at c6bf2d46f, 2026-10-11 — not posted (owner: leave as drafts)

Ledger: closeable (`check_requests --report` at c6bf2d46f: the one result settled, no ask queued). Supersedes the 10 October draft above: T-146 is now also smaller at 263 and 303; the 11 October final review is a second accepted review; links point at `results.html`. The confirmation wording keeps RI-4 (one maintained route is the author's own copied checker), which raw `--draft 476` drops (think-ri84 defect 5). No case ceiling moved.

@franciscouzo, thank you. Your six certificates are registered on `main` as **[T-134](https://jlevy.github.io/squares/results.html#t-134), V3/C3**, confirmed, independently re-implemented, through [PR #487](https://github.com/jlevy/squares/pull/487), at the exact sides they state:

- s(132) ≤ 11.986954193640392741450366579623
- s(237) ≤ 15.903670905580623014470917594172
- s(263) ≤ 7488939206954142477014939239/447356905819500000000000000, which is 16.7404126538191566 rounded up at 16 places
- s(267) ≤ 16.838815269948262260434481342204
- s(270) ≤ 16.936720031121015799532991452837
- s(303) ≤ 17.917443925494235891916989336536

**Which cases they hold.** Each side is below its case's verified ceiling: by 4.37e-03 at 132, 5.33e-06 at 237, 7.03e-06 at 263, 1.67e-05 at 267, 1.09e-03 at 270 and 2.87e-03 at 303. At 267 yours is still the smallest side known, below Ryan Xu's certificate that the case holds (T-125). At the other five, certificates that arrived after yours are smaller:
- SQUISH's #481 (T-136) at 237, 263, 270 and 303;
- your own #488 (T-140) at 132, 237 and 270;
- Evan Daniel's #489 (T-141) at 132;
- Evan Daniel's regularized certificates (T-146) at 263 and 303.

No case ceiling has moved: the case records, for example [n = 267](https://github.com/jlevy/squares/blob/main/packing/frontier/n-267.md), are unchanged for now. House adoption waits for [jlevy/squares#403](https://github.com/jlevy/squares/pull/403), which rewrites every case record, and for a custody record of the replay workers; each case's house is chosen in that later adoption round. The reviews recommend T-134 as the house at 267. At the other five it stays verified and is not selected.

**How it was checked.**
- All 51 jobs of the packet's 17-count replay were decided again by both maintained exact routes, `sqpack.verify` and `devtools.check_rational_witness_independent`, and equal their retained rows. The 17 counts are the six you name and eleven others from the same commit, each a positive with a duplicate-square and an outside-container control; together they make 1,486,686 pair decisions.
- A third exact route, `devtools.check_half_angle_area` (half-extent containment and exact intersection area), decided the six with six controls each, four of them sharp: exact contact accepted, and 10^-40 to 10^-30 past it refused.
- Your issue reports a pass from a copy of this repository's `sqpack` verifier, so one maintained route is your own check. The independent re-implementation rests on the rational corner checker and the third route. The two maintained routes share one parse, the half-angle conversion and the separating-axis method, and all three share Fraction arithmetic.
- Evan Daniel's `verify_cert.py` did not run here, and the KKT and no-descent statements were not checked.
- A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-upper-bound-imports-476-481-483-484.md) reproduced the replay and found no blocking defect, and the [11 October final review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-11-final-upper-bounds.md), by a distinct AI reviewer, accepted the entry again. No human review is claimed.

This confirms finite feasibility only, not optimality.

**Credit.** As you ask, T-134 credits the packings each certificate started from: Mishapolk's at 132, Nate Chaoweeraprasit's SQUISH packings at 237, 263 and 303 (237 through Siddharth Gupta's refinement), Ryan Xu's at 267 and Evan Daniel's at 270. The issue quotes Mishapolk's sides at 132 and 267 as 11.986956226077 and 16.838828608311, which match neither of his files. The record compares the 12-place prints of his README, 11.986956226066 and 16.838828608296, and your certificates are below both.

**The rest of the commit.** The 65 certificates at 02f9690 are retained as factual data; the READMEs and decimal pose files are pinned by digest only, since the repository states no licence. The 59 certificates the issue does not name are compared with the record in the packet, and each is an import of its own. Twenty of them lie beyond n = 324, and fifteen of those are below the beyond-horizon rows the record tracks; updating those rows is a separate queued item.

Nothing you asked for is queued, so this issue is closed with this comment. If the adoption round changes what this comment says, a follow-up will note it.

---
_Generated by [Claude Code](https://claude.ai/code)_
