---
type: is
id: is-01m51e5r3sg4h1wcrh7c826v7b
title: "Intake pass 2026-10-16: #639 (evand exact sides for 22 packings), #640 (ofitzharding Lean proof of s(19) optimality), #622 author reply"
kind: epic
status: open
priority: 1
version: 6
labels:
  - result-import
dependencies: []
child_order_hints:
  - is-01m51e5rvjrd61yaww8djj1nzz
  - is-01m51e5sp1t03c20hqp7d3wajm
  - is-01m51fbdcwtq331pn8jre1w2bp
  - is-01m51h4p1g0t1pr0zdy42d0258
created_at: 2026-10-16T04:05:27.288Z
updated_at: 2026-10-16T04:58:41.086Z
---

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
