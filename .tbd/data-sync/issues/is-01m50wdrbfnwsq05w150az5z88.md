---
type: is
id: is-01m50wdrbfnwsq05w150az5z88
title: "Regularization audit and repair: find every unregularized drawing (e.g. n = 176), explain how it happened, regularize all, make it part of intake, and make the record show regularization status"
kind: epic
status: open
priority: 1
version: 25
labels:
  - regularization
dependencies: []
child_order_hints:
  - is-01m50wds4q4nzbdkzrcy6t3ja4
  - is-01m50wdsq4sdh0btevdfmay252
  - is-01m50wdta5k1jk1cvjx7hw5bjv
  - is-01m50wdv3taw3k5gt76mhzx8mm
  - is-01m50wdvvpwz9asfq2gvaxfz5w
  - is-01m50wdwfc7a00s5yxqqq4p30r
  - is-01m50xqm2f4t3jb74z1sjnx5x9
  - is-01m50xqnsqj449s8rz91s61rdn
  - is-01m50xqqjr60wtgjhqbwayj10m
  - is-01m50xqsa4f5tfq632b71bj3cv
  - is-01m50xqv6vf8tjpb3b879n1mxp
  - is-01m50zdc2fkmvw3hdzvqe4xn43
  - is-01m514y11gd146dzhmnf7ke508
  - is-01m51568exrdg1j7267aj1kvhh
  - is-01m519myr0379ay5npb670sfat
  - is-01m51ah8z1rrf0ax7pbsfg7qpq
  - is-01m51hy396vnjkxe4726egs8x5
  - is-01m51pj9kng0mjpdpsw877d6v4
  - is-01m51wa1heq5bfskfrqyyeyjd7
  - is-01m5279qrmrrbgygjevvr1ppcq
  - is-01m529gqcg7xfzs5bn921bmvhz
  - is-01m52d2s55c771k2jw7ek4sm4w
created_at: 2026-10-15T22:55:15.306Z
updated_at: 2026-10-16T13:41:38.777Z
---
Owner, 2026-10-15 ~22:40Z: 'fully review to what degree regularization has been done. Right now, for example, number 176 looks highly unregularized. How did that happen, and what's necessary to regularize everything again? Let's map that out, make sure it's part of the standard intake process, and run it for all the ones where it's necessary. The records should make it evident which things are regularized, and if not, we should fix the record-keeping process as well. Create beads for all of this work.' Sequenced after the 15 October intake PRs merge (owner: 'After that').

## Notes

HANDOFF 2026-10-16 ~04:35Z (coordinator session claude/ecstatic-edison-8en33t; beads synced)

Task: continue the intake passes and the regularization repair, landing small reviewed PRs. Owner rules in force: merge a PR only after the full review process (pr-review-requirements standard: senior review + an addressing pass with dispositions + dedicated correctness review where sensitive), stacks via gh stack with merge commits only (DATA_REVISION/PUBLICATION_REVISION pin merge commits; never rebase or gh stack sync); replies post only after the PR carrying the change merges and main + the deployed site agree (stage 7).

DONE (on main e2e018f32): stack #632 (#627 T-188..T-192 + 267 beyond-horizon rows, #628 residual reads/#622 entry/#613 intake, #631 #624 triage), #626 #625 #630 (15 Oct reply records), #637 (16 Oct replies held for the stack; #596 follow-up posted + closed; 4 replies corrected in place), #636 (regularization record + gate: per-count state in packing/atlas/known-best/default-drawings.json, lapse recording, default_drawings --check-state in fast/records tiers, PENDING_ALLOWED = the 20 pending counts each with its bead; site v0.7.14). #616 closed as superseded by #627.

IN FLIGHT (worktrees under .claude/worktrees/, branches not yet pushed unless noted):
- think-la7h (epic think-sfas): branch claude/ecstatic-edison-8en33t-regularize-3a, re-running grid-slack (0.5/1/5 deg) + Evan Daniel driver + regularize_select + layer on 176, 105, 129, 146, 156, 204, 271, 272, 303 at <=2 workers nice; takes them off PENDING_ALLOWED; PR to main, cut next free site edition (after v0.7.14) last. Needs a senior review before merge.
- think-g3q7 (epic think-sfas): branch claude/ecstatic-edison-8en33t-regularization-intake: result-import.md step + adopt_houses output so every re-housing is re-regularized or allowlisted with a bead; small PR; needs review.
- think-phyb / think-a4x3 / think-xik9 (epic think-mdnn): branch claude/ecstatic-edison-8en33t-intake-1016: triage + request entries for #639 (evand, exact algebraic sides for 22 packings) and #640 (ofitzharding Lean proof of s(19) = 3 + 4 sqrt2/3, ofitzharding/sq19 v1.0.0 @ 34fb2b7; also announced at https://x.com/ofitzharding/status/2110935681597874374), read BuddenPing's #622 reply (AI statement) into think-30n2; sq19 into intake-watch.yaml. One draft PR, review, merge; then post acknowledgements from main.

NEXT after those: think-kpm3 (153, 154, 207, 211, 237, 241, 302, 304) and think-3zi3 (175, 232, 264) re-runs, one PR each, removing their counts from PENDING_ALLOWED; think-0ut1 leftovers; think-290l, think-4ov9, think-k09z; think-tk0u (check v0.7.11 first_published vs deploy date); think-nhut (#544 follow-up names the 13 Oct n17 suspension).

OWNER DECISIONS: think-l3oo lists all 11 (incl. #574/T-174 which would re-house 35 counts — hold until regularization runs or allowlist with beads; #570; #557/#565; #624; case labels n-59/n-76/n-95/n-19; #557's n-18 label).

GOTCHAS: (1) site edition race — other sessions cut editions too; cut last, merge immediately on green. (2) bead-tree gate reads origin/tbd-sync: close child beads before parents or every PR's CI fails. (3) release-impact: any result-requests.yaml change needs the methods-survey no-change entry backed by a byte-identical render at link revision = main sha (helper: scratchpad render/survey_render.sh; re-create if lost). (4) #538 animate-view >400 ms timing flake: re-run once with a one-line PR comment. (5) shared 4-core host: --push tier exceeds wall caps; rely on hosted CI plus --records and focused tests. (6) gh needs NO_PROXY for github hosts; Python 3.14 via uv run --frozen from packing/; tbd via npm get-tbd@0.10.0.

2026-10-16 ~13:45Z HANDOFF from the overnight coordinator user-eb: the full handoff (merge order, per-PR state, owner decisions 12-28, open beads) is in think-hg5s's notes. Nothing is merged; nothing was posted to issues except the new tracking issue #643. Regularization: #641 -> #650 (intake step; fix think-cmj7 first); stack #644 -> #653 -> #654 -> #656 -> #657; PENDING_ALLOWED is empty through #656; #657's adoption re-allowlists 7-8 counts under think-r3cl and needs the owner's word at 176 (think-l3oo 27).
