---
type: is
id: is-01m53ztmtemm14341aga7gesrz
title: "PR #658: land T-193's house-gate change after #660 merges (review A2 to A5)"
kind: task
status: closed
priority: 1
version: 8
delegate: lane-658
labels:
  - result-import
dependencies: []
parent_id: is-01m51e5r3sg4h1wcrh7c826v7b
hold: null
hold_until: null
created_at: 2026-10-17T03:52:26.702Z
updated_at: 2026-10-19T22:24:27.915Z
started_at: 2026-10-17T03:52:33.493Z
closed_at: 2026-10-19T22:24:27.915Z
close_reason: "Landed in PR #658, merged 2026-10-19T22:22:34Z as 926cd764a (head fc071e082, site v0.7.34): T-193 V3/C3 at its 16 counts after its stage 4 review (think-7qxm), the house-gate change staging T-193 under think-ot5c with CORRECTIONS_OWED holding the nine RE-1 counts (think-3q9x), and T-194 V0/C1 from the s(19) review (think-9e3w). Reviews A-D dispositioned; hosted CI green at the final head. think-o40t stays open until the #640 reply record removes it from #640's beads; think-8ido, think-ot5c, think-nqnl, think-phyb and think-a4x3 stay open."
resolution: null
duplicate_of: null
---
PR #658's review A (findings A2 to A5) asks that T-193's exemption from the house gate be bounded, per count and owned by `select_houses`. Under the owner's house rule of 16 October 2026, implemented by PR #660, no exemption is allowed at all, and #660's guard tests fail if #658's `deferred_results` merges. The fix needs #660's mechanism (`ALGEBRAIC_READERS`, `PENDING_ADOPTION` with `STAGING_REASONS`, `devtools.exact_sides`), so it lands on #658 after #660 merges to main.

What lands, as rehearsed on a local merge of #658 with #660's head f76706d17 (not pushed):
- `select_houses`: drop `deferred_results` and its test; add `evand_exact_side`, reading packing/campaign/issue-intake/upper-bounds-20261016/exact-sides.json, and register it in `ALGEBRAIC_READERS` under T-193's source key.
- `select_houses --all` then makes T-193 the house at all 16 of its counts. Stage all 16 in `PENDING_ADOPTION` as `no writer` under think-ot5c: re-point 88, 102, 123, 126, 199, 258, 259, 266, 267, 292, 295 and 301 from T-174 (think-3mry, which leaves it 38 counts), and add 175, 204, 232 and 302, which are T-186's houses since #657.
- `adopt_houses`: a held sentence at a count re-staged for a smaller house names that house, its bead and the side it passes (`_keeps_until`), and `held_history` matches it. `adopt_houses --refresh` rewrites the twelve records.
- Tests: #660's tests that hard-code the staged set take T-193's counts. New tests cover the reader, its refusals and the re-staged sentence.
- Records: T-193's citation deferral moves to think-ot5c, worded as #660 words T-174's. T-193's next_rung and notes, E-evand-639-verify-exact-replay and the #639 request entry say the house rule stages the adoption. The papers' release record is re-taken.

## Validation
- Run: on main with #660 merged, `select_houses --all --check` exits 0, and so do `pytest tests/test_house_adoption.py`, `adopt_houses --check`, `check_certificate_citations` and `packing-validate --records`. The site edition is the coordinator's.
- Waits on: PR #660 merging to main.
- Cost: under 0.2 CPU-h.

## Notes

2026-10-17 user-eb-addr-658: prepared commit 7a51693af on local branch scratch/addr-658-post660 (in /home/user/squares/.git; parent 5d0b8455e = local merge of #658 head 764cf17ed with #660 head a776a24c6, not pushed). Patch: /tmp/claude-0/-home-user-squares/497b954f-f1d7-5565-9258-beec4cbe400c/scratchpad/post660-v2/0001-fix-houses-read-T-193-s-exact-sides-and-stage-its-si.patch. On that tree: select_houses --all --check exit 0 (57 of 70 move, all staged), packing-validate --records passes, 23 test files 941 passed / 28 skipped, ruff and basedpyright clean. To land: merge origin/main (with #660) into #658, cherry-pick 7a51693af, re-run adopt_houses --refresh and select_houses --all --check, re-render the papers from main and the branch and update the release record's SHAs, re-pin, push.

2026-10-17 ~05:55Z user-eb-sweep-1017 (intake pass think-e2sz, stage 0): the sweep lists this wait as resolved: jlevy/squares#660 merged into main at 804eff369 on 2026-10-17. The wait is over; PR #658's house-gate change (review A2 to A5) can resume on main.
blocked_on: none

2026-10-17 user-eb-addr-658: #660 merged (804eff369); merged into #658 (1af453321), prepared fix landed as 8f46741ad (tree identical to the rehearsed 7a51693af), papers' record re-rendered (a0f762262), re-pinned (a0c9087d5), pushed. select_houses --all --check exit 0; 23 test files 941 passed; records tier passes except the site edition. Dispositions update: pullrequestreview-5556772214. think-3q9x can close at merge.

2026-10-19 lane-658: taken over by the 19 October handoff (issue #684) to land PR #658. Worktree branch lane-658/records-193-194: fast-forwarded #658 head 3022eb984 to checkpoint codex/handoff-20261019/658 d0b9ec2f9, merged origin/main 14fd9e27f (#685, v0.7.32) cleanly as c41eb33ec. Next: paper decision (AM1), re-pin, review round D, edition last, merge; then stage 7 replies.
