---
type: is
id: is-01m4kavd06vjy2knrcgbd036pr
title: "Import Francisco Couzo: certificates at 132, 175, 209, 237, 270, 305 (#488)"
kind: task
status: closed
priority: 1
version: 8
labels:
  - result-import
dependencies: []
parent_id: is-01m4jk37jkzx9bzdws5jj72qg7
created_at: 2026-10-10T16:38:00.454Z
updated_at: 2026-10-12T23:39:03.701Z
closed_at: 2026-10-12T23:39:03.700Z
close_reason: "#488 imported and answered: T-140 registered, reviewed twice, issue closed 2026-10-12 with the final reply."
resolution: null
duplicate_of: null
---
Issue https://github.com/jlevy/squares/issues/488 (2026-10-10T14:08Z). franciscouzo/square-packing 3ef76349025bf4bfa99c9c3600bcc273f4c33e02 certificates/nN.cert (Evan Daniel's format). Below SQUISH's #481 at 209, 237, 270, 305; below this author's #476 at 132 and #460 at 175. Superseded at 132 by #489 (evand Hunt 3). Stages 1-3 through devtools.upper_bound_reports, comparing with #470, #476, #481, #489 and the register.

## Notes

2026-10-10 import lane (stages 1-2 and the replay), worktree branch worktree-agent-af1304354bf317e13, commit 9f0dbb8a7 (with the #489 packet at 46fe607cc):

- Pin: franciscouzo/square-packing 3ef76349025bf4bfa99c9c3600bcc273f4c33e02 (master head, committed 2026-10-10T13:52:27Z, tree 2978a99c), no licence; packet packing/resources/web/couzo-certificates-2026-10-10 retains the nine certificates the commit adds (209) or changes (132, 175, 237, 270, 303, 305, 338, 340) as factual data; the other 54 of the 63 are pinned by digest and identical_to the issue-476 packet's copies (9bf90e7 removed 102, 103, 272). certificates/README.md's SHA-256 column matches all 63.
- Claims (acquisition/claims.json, read at main af17208c0): every requested side is below its case ceiling. Smallest now: 132 #489 (Hunt 3, 1.27e-3 below); 175, 209, 237, 270, 305 this certificate (below #481 by 4.28e-7, 3.96e-5, 4.77e-6, 5.64e-5 at 209, 237, 270, 305; below T-130 at 175 by 3.44e-5). Unnamed: 303 above #481 by 4.30e-3; 338 and 340 below Couzo's own tracked beyond-horizon rows.
- Replay: certify --workers 2, 27 jobs, 1,899,504 pair decisions, 388.0 route CPU s, 3 min 30 s wall; all 9 positives pass both routes, all 18 controls refused; check --replay serial 6 min 42 s, exit 0. Third route: check_half_angle_area decide-imports --imports '#488' '#489' --upstream (both packets), 10 certificates, all 60 of its controls reach their required outcomes, retained files equal to upstream bytes, no disagreement, 19 s wall.
- 305: exactly the side of Hunt 3's hunt3_n305 (c013f43); same arrangement up to a quarter turn; the Hunt 3 log at 76a529b drops 305 as Couzo's.
- Register plan printed (T-NNN); shared records not edited, proposed YAML handed to the coordinator.
- Validation at 46fe607cc: packing-validate --records 49/49 steps passed (59.7 s); --edit 65/65 passed (252.5 s at load ~10, over the 240 s ceiling, reported not enforced); touched tests 229 passed.

2026-10-10 records lane R3: registered #488 as T-140 (ef1f6287e, V0/C0), raised to V3/C3 on review-2026-10-10-upper-bound-imports-488-489.md (b05bc4b26) with E-couzo-488-exact-feasibility; the declaration reads #481 and #489 by exact HOUSES readers and the claim record is refrozen (6d5951166, b05bc4b26); #488's request entry maps the six to T-140. Branch worktree-agent-a45d986d0210d7ec5 (records lane R3, merged into nothing yet). Ids provisional until merged to main.

## Stage 7 draft (2026-10-10, to post after PR #487 merges; not posted)

Supports posting after merge: yes (facts checked against PR #487's head 6fb495b3a; post once the merge's Pages deployment shows the T-140 row, and recheck the id if anything else merges first). Ledger: closeable (check_requests --report: all three results settled, no ask queued; house adoption waits on PR #403 under think-fvz4, and the 338/340 beyond-horizon rows (RL-9) are the owner's decision, neither an ask of the author).

@franciscouzo, thank you. Your six certificates are registered on `main` as **[T-140](https://jlevy.github.io/squares/all-results.html#t-140), V3/C3**, confirmed, through [PR #487](https://github.com/jlevy/squares/pull/487), at the exact sides they state:

- s(132) ≤ 11.986953587254420950497823747297
- s(175) ≤ 13.767120724692313217301436951952
- s(209) ≤ 14.946223226446451055256712327571
- s(237) ≤ 15.90294960767783168971278840528
- s(270) ≤ 16.929775353541359582336028215624
- s(305) ≤ 17.951139772206997545942513172626

**Which cases they hold.** Each side is below its case's verified ceiling: by 4.37e-03 at 132, 1.78e-03 at 175, 3.39e-03 at 209, 7.27e-04 at 237, 8.03e-03 at 270 and 1.82e-03 at 305.
- At 175, 209, 237, 270 and 305 yours is the smallest side known. It is below SQUISH's #481 (T-136) at 209, 237, 270 and 305, by 4.28e-07, 3.96e-05, 4.77e-06 and 5.64e-05, and below your own T-130 certificate at 175 by 3.44e-05.
- At 132 it is below your #476 side by 6.06e-07, but Evan Daniel's #489 (T-141) is smaller by 1.27e-03. The issue quotes Mishapolk's 132 as 11.986956226077; the record compares his README's 12-place print, 11.986956226066, and your certificate is below either.
- Evan Daniel's Hunt 3 commit also holds a certificate at 305 with exactly your side, the same arrangement up to a quarter turn. His log gives it to you, and no entry cites it.

The case records, for example [n = 175](https://github.com/jlevy/squares/blob/main/packing/frontier/n-175.md), are unchanged for now. House adoption waits for [PR #403](https://github.com/jlevy/squares/pull/403), which rewrites every case record, and for a custody record of the replay workers; each case's house is chosen in that later adoption round. The review recommends T-140 as the house at 175, 209, 237, 270 and 305, crediting the packings each started from. At 132 it stays verified and is not selected.

**How it was checked.**
- All 27 jobs, over the nine certificates your commit adds or changes (the six, and 303, 338 and 340), each a positive with a duplicate-square and an outside-container control, were decided again by both maintained exact routes, `sqpack.verify` and `devtools.check_rational_witness_independent`. They equal their retained rows: 1,899,504 pair decisions.
- A third exact route, `devtools.check_half_angle_area` (half-extent containment and exact intersection area), decided the six with six controls each, four of them sharp, and every retained file was held to its bytes fetched at the pin.
- Your issue reports a pass from a copy of this repository's `sqpack` verifier, so one maintained route is your own check. The independent re-implementation rests on the rational corner checker and the third route. The two maintained routes share one parse, the half-angle conversion and the separating-axis method, and all three share Fraction arithmetic. Evan Daniel's `verify_cert.py` did not run here.
- A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-upper-bound-imports-488-489.md) reproduced the replay and found no blocking defect. No human review is claimed.

This confirms finite feasibility only, not optimality.

**Not registered.**
- **The KKT and no-descent statements** are numerical evidence of local optimality, not a bound on s(n). They are recorded as your report and were not checked here.
- **303, 338 and 340**, which the commit changes and the issue does not name. 303 is above #481's exact side there, and your README marks it superseded. 338 and 340 lie beyond the case corpus, below your own earlier rows there by 1.48e-03 and 1.78e-04. All three were decided on all three routes. Whether the record's beyond-horizon rows at 338 and 340 move to these certificates is the owner's decision, and it is pending.

**Credit.** As you ask, T-140 credits the packings each started from: SQUISH's from #481 at 209, 237, 270 and 305, Mishapolk's at 132 and Ryan Xu's at 175. It also names Evan Daniel's `fq`, your basin hopping and David Ellsworth's `refine_packing`, and Evan Daniel's exact contact solver, which wrote all six.

Nothing you asked for is queued, so this issue is closed with this comment. If the adoption round changes what this comment says, a follow-up will note it.

---
_Generated by [Claude Code](https://claude.ai/code)_

2026-10-10 coordinator: the records branch was merged into claude/determined-rubin-yjfy2a at 4ce817db5 and is on draft PR https://github.com/jlevy/squares/pull/487 (CI on that branch is being driven to green); the ids are final once that PR merges to main. The stage 7 reply draft, where there is one, is in this bead or its answer bead.


## Stage 7 draft from main at c6bf2d46f, 2026-10-11 — not posted (owner: leave as drafts)

Ledger: closeable (`check_requests --report` at c6bf2d46f: all three results settled, no ask queued; the 338/340 beyond-horizon rows, RL-9, are the owner's decision, not an ask of the author). Supersedes the 10 October draft above: facts at T-140's six counts are unchanged at the merge (T-146 shares none of them); at 303 T-146 is also below the unnamed certificate; the 11 October final review is a second accepted review; links point at `results.html`. The confirmation wording keeps RL-5 (one maintained route is the author's own copied checker), which raw `--draft 488` drops (think-ri84 defect 5). No case ceiling moved.

@franciscouzo, thank you. Your six certificates are registered on `main` as **[T-140](https://jlevy.github.io/squares/results.html#t-140), V3/C3**, confirmed, independently re-implemented, through [PR #487](https://github.com/jlevy/squares/pull/487), at the exact sides they state:

- s(132) ≤ 11.986953587254420950497823747297
- s(175) ≤ 13.767120724692313217301436951952
- s(209) ≤ 14.946223226446451055256712327571
- s(237) ≤ 15.90294960767783168971278840528
- s(270) ≤ 16.929775353541359582336028215624
- s(305) ≤ 17.951139772206997545942513172626

**Which cases they hold.** Each side is below its case's verified ceiling: by 4.37e-03 at 132, 1.78e-03 at 175, 3.39e-03 at 209, 7.27e-04 at 237, 8.03e-03 at 270 and 1.82e-03 at 305.
- At 175, 209, 237, 270 and 305 yours is the smallest side known. It is below SQUISH's #481 (T-136) at 209, 237, 270 and 305, by 4.28e-07, 3.96e-05, 4.77e-06 and 5.64e-05, and below your own T-130 certificate at 175 by 3.44e-05.
- At 132 it is below your #476 side by 6.06e-07, but Evan Daniel's #489 (T-141) is smaller by 1.27e-03. The issue quotes Mishapolk's 132 as 11.986956226077; the record compares his README's 12-place print, 11.986956226066, and your certificate is below either.
- Evan Daniel's Hunt 3 commit also holds a certificate at 305 with exactly your side, the same arrangement up to a quarter turn. His log gives it to you, and no entry cites it.

No case ceiling has moved: the case records, for example [n = 175](https://github.com/jlevy/squares/blob/main/packing/frontier/n-175.md), are unchanged for now. House adoption waits for [jlevy/squares#403](https://github.com/jlevy/squares/pull/403), which rewrites every case record, and for a custody record of the replay workers; each case's house is chosen in that later adoption round. The review recommends T-140 as the house at 175, 209, 237, 270 and 305, crediting the packings each started from. At 132 it stays verified and is not selected.

**How it was checked.**
- All 27 jobs, over the nine certificates your commit adds or changes (the six, and 303, 338 and 340), each a positive with a duplicate-square and an outside-container control, were decided again by both maintained exact routes, `sqpack.verify` and `devtools.check_rational_witness_independent`. They equal their retained rows: 1,899,504 pair decisions.
- A third exact route, `devtools.check_half_angle_area` (half-extent containment and exact intersection area), decided the six with six controls each, four of them sharp, and every retained file was held to its bytes fetched at the pin.
- Your issue reports a pass from a copy of this repository's `sqpack` verifier, so one maintained route is your own check. The independent re-implementation rests on the rational corner checker and the third route. The two maintained routes share one parse, the half-angle conversion and the separating-axis method, and all three share Fraction arithmetic. Evan Daniel's `verify_cert.py` did not run here.
- A separately prompted AI [review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-10-upper-bound-imports-488-489.md) reproduced the replay and found no blocking defect, and the [11 October final review](https://github.com/jlevy/squares/blob/main/docs/project/reviews/review-2026-10-11-final-upper-bounds.md), by a distinct AI reviewer, accepted the entry again. No human review is claimed.

This confirms finite feasibility only, not optimality.

**Not registered.**
- **The KKT and no-descent statements** are numerical evidence of local optimality, not a bound on s(n). They are recorded as your report and were not checked here.
- **303, 338 and 340**, which the commit changes and the issue does not name. 303 is above #481's exact side there, and Evan Daniel's regularized certificate there (T-146) is smaller again; your README marks it superseded. 338 and 340 lie beyond the case corpus, below your own earlier rows there by 1.48e-03 and 1.78e-04. All three were decided on all three routes. Whether the record's beyond-horizon rows at 338 and 340 move to these certificates is the owner's decision, and it is pending.

**Credit.** As you ask, T-140 credits the packings each started from: SQUISH's from #481 at 209, 237, 270 and 305, Mishapolk's at 132 and Ryan Xu's at 175. It also names Evan Daniel's `fq`, your basin hopping and David Ellsworth's `refine_packing`, and Evan Daniel's exact contact solver, which wrote all six.

Nothing you asked for is queued, so this issue is closed with this comment. If the adoption round changes what this comment says, a follow-up will note it.

---
_Generated by [Claude Code](https://claude.ai/code)_
