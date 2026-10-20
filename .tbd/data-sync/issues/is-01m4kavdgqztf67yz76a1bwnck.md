---
type: is
id: is-01m4kavdgqztf67yz76a1bwnck
title: "Import Evan Daniel: Hunt 3 packings at 132, 308, 343, 344 (#489)"
kind: task
status: closed
priority: 1
version: 8
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T16:38:00.983Z
updated_at: 2026-10-12T23:39:36.786Z
closed_at: 2026-10-12T23:39:36.785Z
close_reason: "Completed: #489 imported, registered as T-141, answered and closed (issue closed 2026-10-12); request entry closed on main."
resolution: null
duplicate_of: null
---
Issue https://github.com/jlevy/squares/issues/489 (2026-10-10T14:47Z). Quality-diversity basin explorer with a two-parent crossover (as #465). s(132) <= 11.985680198845808811522231964102, s(308) <= 17.998269879526255875387992744507, s(343) <= 18.978232523635611279730512106023, s(344) <= 18.994450514277401521114135796864; each below #488 (132) or #484 (308, 343, 344). evand/square-packing head 76a529bc6f36 (2026-10-10). 343 and 344 are beyond the n <= 324 horizon. Stages 1-3 through devtools.upper_bound_reports.

## Notes

2026-10-10 import lane (stages 1-2 and the replay), worktree branch worktree-agent-af1304354bf317e13, commit 46fe607cc (after the #488 packet at 9f0dbb8a7):

- Pin: evand/square-packing main head 76a529bc6f36ed05827cae3d1412d6acb5be00fc (committed 2026-10-10T14:48:25Z, tree c1f66266), parent c013f43cefd006f007a6f37bc3a56aadead815d6, the commit the issue names; the head changes only search/packer/PACKER.md and search/packer/pk/pending.yaml, so every retained byte is the same at both. MIT; packet packing/resources/web/evand-record-hunt3-2026-10-10 retains the five Hunt 3 certificates (132, 305, 308, 343, 344) with .exact.txt, .input.txt and .json, plus LICENSE, CREDITS.md and search/exact/README.md; verify_cert*.py pinned identical_to the issue-399 packet; PACKER.md digest only.
- Claims (read at main af17208c0): 132 smallest, below #488 by 1.27e-3 and below the case (T-098) by 5.65e-3; 308 smallest, below #484 by 1.04e-3 and the grid by 1.73e-3; 343 and 344 beyond the horizon, below #484 by 1.67e-2 and 1.04e-3 (beyond-horizon-claims.json holds only them). Unnamed 305: exactly #488's side; printed comparison undecided; same arrangement up to a quarter turn; the log at the pin drops it as Couzo's.
- Replay: certify --workers 2, 15 jobs, 1,319,598 pair decisions, 308.35 route CPU s, 3 min 33 s wall at load ~7; all 5 positives pass both routes, all 10 controls refused; check --replay serial 5 min 33 s, exit 0. Third route: decide-imports --imports '#488' '#489' --upstream, the four requested certificates pass with all 24 controls, retained files equal to upstream bytes, no disagreement; the unnamed 305 measured by arrangement_gap against #488's: one side, a quarter turn apart, 34 squares moved beyond 1e-9 (largest 1.77e-2).
- Register plan printed (T-NNN for 132 and 308; beyond-horizon rows at 343 and 344 that supersede #484's once both are registered); shared records not edited, proposed YAML handed to the coordinator.
- Validation at 46fe607cc: packing-validate --records 49/49 steps passed (59.7 s); --edit 65/65 passed (252.5 s at load ~10, over the 240 s ceiling, reported not enforced); touched tests 229 passed.

2026-10-10 records lane R3: registered #489 as T-141 (11179cb77, V0/C0), raised to V3/C3 on review-2026-10-10-upper-bound-imports-488-489.md (b05bc4b26) with E-evand-489-exact-feasibility; 343 and 344 are verified beyond-horizon rows and #484's rows there are superseded; the claim record is refrozen with exact readers, so 305 reads as a tie with #488, cited by no entry. Branch worktree-agent-a45d986d0210d7ec5 (records lane R3, merged into nothing yet). Ids provisional until merged.

## Stage 7 draft (2026-10-10, to post after PR #487 merges; not posted)

Supports posting after merge: yes (facts checked against PR #487's head 6fb495b3a; post once the merge's Pages deployment shows the T-141 row, and recheck the id if anything else merges first). Ledger: closeable (check_requests --report: all three results settled, no ask queued; house adoption at 132 and 308 waits on PR #403 under think-fvz4, the project's own round, not an ask of the author).

@evand, thank you. Your Hunt 3 certificates are imported on `main` through [PR #487](https://github.com/jlevy/squares/pull/487), retained at your branch head 76a529bc6f36ed05827cae3d1412d6acb5be00fc, whose files are byte-identical to c013f43's.

- **n = 132 and 308** are registered as **[T-141](https://jlevy.github.io/squares/all-results.html#t-141), V3/C3**, confirmed: s(132) ≤ 11.985680198845808811522231964102 and s(308) ≤ 17.998269879526255875387992744507. Each is the smallest side known. At 132 it is below the case's ceiling (T-098) by 5.65e-03, and below Francisco Couzo's #488 (T-140) and #476 by 1.27e-03. At 308 it is below the grid's 18, which the case holds in both lanes, by 1.73e-03, and below Kevin Fang's #484 (T-135) by 1.04e-03.
- **n = 343 and 344** lie beyond the case corpus, so they have no case record or register entry. Your sides, 18.978232523635611279730512106023 and 18.994450514277401521114135796864, are verified beyond-horizon rows in the source register, from the same evidence. They supersede Kevin Fang's #484 rows there, which the record keeps.
- **The unnamed hunt3_n305** has exactly the side of Francisco Couzo's #488 certificate at 305, and the two are one arrangement up to a quarter turn. Your log gives it to him; the record keeps 305 under #488, and no entry cites yours.
- **Not registered:** the KKT, reduced-Hessian and jamming statements are numerical evidence of local optimality, not a bound on s(n). They are recorded as your report and were not checked here.

The case records, [n = 132](https://github.com/jlevy/squares/blob/main/packing/frontier/n-132.md) and [n = 308](https://github.com/jlevy/squares/blob/main/packing/frontier/n-308.md), are unchanged for now. House adoption waits for [PR #403](https://github.com/jlevy/squares/pull/403), which rewrites every case record, and for a custody record of the replay workers; each case's house is chosen in that later adoption round. The review recommends T-141 as the house at 132 and 308, crediting Kevin Fang's construction at 308 as you ask.

**How it was checked.**
- All 15 jobs, over the five certificates (132, 305, 308, 343 and 344), each a positive with a duplicate-square and an outside-container control, were decided again by both maintained exact routes, `sqpack.verify` and `devtools.check_rational_witness_independent`. They equal their retained rows: 1,319,598 pair decisions.
- A third exact route, `devtools.check_half_angle_area` (half-extent containment and exact intersection area), decided the four you name with six controls each, four of them sharp, and every retained file was held to its bytes fetched at the pin.
- No route here is your code, so the replay is independently re-implemented. The two maintained routes share one parse, the half-angle conversion and the separating-axis method, and all three share Fraction arithmetic. Your `verify_cert.py` and `verify_cert2.py` did not run here.
- A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-upper-bound-imports-488-489.md) reproduced the replay and found no blocking defect. No human review is claimed.

This confirms finite feasibility only, not optimality.

**Credit.** T-141 credits you and your quality-diversity basin explorer with its two-parent crossover move. As you ask, the packings at 308, 343 and 344 are credited as built on Kevin Fang's #484 packings in the Arslanov–Mustafin–Shangitbayev two-wedge family, and 132 as your own lineage from #465. For credit, the review measured your 308 and 344 as Fang's arrangements moved, and found your 343 has no one-to-one matching with his under any symmetry, a different basin, as you say.

Nothing you asked for is queued, so this issue is closed with this comment. If the adoption round changes what this comment says, a follow-up will note it.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-10 coordinator: the records branch was merged into claude/determined-rubin-yjfy2a at 4ce817db5 and is on draft PR https://github.com/jlevy/squares/pull/487 (CI on that branch is being driven to green); the ids are final once that PR merges to main. The stage 7 reply draft, where there is one, is in this bead or its answer bead.


## Stage 7 draft from main at c6bf2d46f, 2026-10-11 — not posted (owner: leave as drafts)

Ledger: closeable (`check_requests --report` at c6bf2d46f: all three results settled, no ask queued). Supersedes the 10 October draft above only in form: the facts at 132, 308, 343 and 344 are unchanged at the merge (T-146 shares none of these counts); the 11 October final review is a second accepted review; links point at `results.html`. No case ceiling moved.

@evand, thank you. Your Hunt 3 certificates are imported on `main` through [PR #487](https://github.com/jlevy/squares/pull/487), retained at your branch head 76a529bc6f36ed05827cae3d1412d6acb5be00fc, whose files are byte-identical to c013f43's.

- **n = 132 and 308** are registered as **[T-141](https://jlevy.github.io/squares/results.html#t-141), V3/C3**, confirmed, independently re-implemented: s(132) ≤ 11.985680198845808811522231964102 and s(308) ≤ 17.998269879526255875387992744507. Each is the smallest side known. At 132 it is below the case's ceiling (T-098) by 5.65e-03, and below Francisco Couzo's #488 (T-140) and #476 by 1.27e-03. At 308 it is below the grid's 18, which the case holds in both lanes, by 1.73e-03, and below Kevin Fang's #484 (T-135) by 1.04e-03.
- **n = 343 and 344** lie beyond the case corpus, so they have no case record or register entry. Your sides, 18.978232523635611279730512106023 and 18.994450514277401521114135796864, are verified beyond-horizon rows in the source register, from the same evidence. They supersede Kevin Fang's #484 rows there, which the record keeps.
- **The unnamed hunt3_n305** has exactly the side of Francisco Couzo's #488 certificate at 305, and the two are one arrangement up to a quarter turn. Your log gives it to him; the record keeps 305 under #488, and no entry cites yours.
- **Not registered:** the KKT, reduced-Hessian and jamming statements are numerical evidence of local optimality, not a bound on s(n). They are recorded as your report and were not checked here.

No case ceiling has moved: the case records, [n = 132](https://github.com/jlevy/squares/blob/main/packing/frontier/n-132.md) and [n = 308](https://github.com/jlevy/squares/blob/main/packing/frontier/n-308.md), are unchanged for now. House adoption waits for [jlevy/squares#403](https://github.com/jlevy/squares/pull/403), which rewrites every case record, and for a custody record of the replay workers; each case's house is chosen in that later adoption round. The review recommends T-141 as the house at 132 and 308, crediting Kevin Fang's construction at 308 as you ask.

**How it was checked.**
- All 15 jobs, over the five certificates (132, 305, 308, 343 and 344), each a positive with a duplicate-square and an outside-container control, were decided again by both maintained exact routes, `sqpack.verify` and `devtools.check_rational_witness_independent`. They equal their retained rows: 1,319,598 pair decisions.
- A third exact route, `devtools.check_half_angle_area` (half-extent containment and exact intersection area), decided the four you name with six controls each, four of them sharp, and every retained file was held to its bytes fetched at the pin.
- No route here is your code, so the replay is independently re-implemented. The two maintained routes share one parse, the half-angle conversion and the separating-axis method, and all three share Fraction arithmetic. Your `verify_cert.py` and `verify_cert2.py` did not run here.
- A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-upper-bound-imports-488-489.md) reproduced the replay and found no blocking defect, and the [11 October final review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-11-final-upper-bounds.md), by a distinct AI reviewer, accepted the entry again. No human review is claimed.

This confirms finite feasibility only, not optimality.

**Credit.** T-141 credits you and your quality-diversity basin explorer with its two-parent crossover move. As you ask, the packings at 308, 343 and 344 are credited as built on Kevin Fang's #484 packings in the Arslanov–Mustafin–Shangitbayev two-wedge family, and 132 as your own lineage from #465. For credit, the review measured your 308 and 344 as Fang's arrangements moved, and found your 343 has no one-to-one matching with his under any symmetry, a different basin, as you say.

Nothing you asked for is queued, so this issue is closed with this comment. If the adoption round changes what this comment says, a follow-up will note it.

---
_Generated by [Claude Code](https://claude.ai/code)_
