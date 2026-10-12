---
type: is
id: is-01m4r8g0xxbe0b4eys838qxb08
title: "Import Evan Daniel: s(154) <= 12922566401934059503377267965457/10^30, 5.04e-4 below T-136 (#552)"
kind: task
status: in_progress
priority: 1
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T14:33:02.652Z
updated_at: 2026-10-12T15:56:03.561Z
started_at: 2026-10-12T14:33:16.971Z
---
Evan Daniel reports s(154) <= S' = 12922566401934059503377267965457/10^30 = 12.922566401934059503377267965457 in evand/square-packing 597e660c9a078a552991ab893cda3ab693cb5ac8, search/packer/candidates/tt_n154.cert (format of #375/#399/#465/#489), 5.04e-4 below T-136 (SQUISH, #481), the house at 154 on layer 6. Stages 1, 2 and the stage 4 replay of the 2026-10-12 intake continuation (think-mq0k, #544).

## Notes

GitHub issue: https://github.com/jlevy/squares/issues/552 (lineage comment https://github.com/jlevy/squares/issues/552#issuecomment-6126041137).

**Lane.** 2026-10-12 continuation of the intake pass (think-mq0k, #544), branch `intake-552` from local `layer6` at 92649a2eb, worktree agent-a2005bc0419561660. Stages 1, 2 and the stage 4 replay done; no register, case, request or intake-watch record edited.

**Pin.** evand/square-packing 597e660c9a078a552991ab893cda3ab693cb5ac8 (2026-10-12T13:58:36Z, tree a52316fa), the commit the issue names; it adds search/packer/candidates/tt_n154{.cert,.exact.txt,.input.txt,.json} and tt_n154_regularized.{cert,json} and the packer log's submission entry. Head 31523f8 (13:59:32Z, also the tag exact-data-2026-10-12 of #545) adds one PACKER.md line only. Issue filed 13:59:25Z.

**Claims at the pin (stage 1 table).**
1. s(154) <= S' = 12922566401934059503377267965457/10^30 (tt_n154.cert): a bound the record does not hold, so a new entry (planned T-156). S' = ceil_30(S* (1 + 1e-20)) with S* the 80-digit KKT point (checked here).
2. tt_n154_regularized.cert, same packing, same S': no entry; retained beside, not a separate claim. 112 of 154 poses equal, 42 moved (largest 0.135), all moved squares rattlers or flat squares of the solver report, only the 8 rattlers turn; the regularizer report's angle_changes list is empty.
3. KKT / reduced Hessian PSD modulo 45 flat motions / 98 jammed corner-corner branches / 8 rattlers: numerical evidence, no entry.
4. Commits 7d5cc3f..c3655cc (census v4, time-travel test: 9 h of chaining from the 5 Oct register recovers ~7% of later gains; only 154 overshoots): search methodology, nothing to import (intake-watch read).

**Who holds 154.** layer6 case n-154: T-136 (SQUISH, #481) 12.9230702023011407...; main case (4a4910524): T-127 (Gupta) 12.9265622458523469.... Pending/older at 154: T-127, #470 (Mishapolk) 12.926562245853, T-115 12.9265622458535389..., T-113 12.9282936576777576..., T-098 12.9316637211668470..., T-056 prints 12.931663721169976. This certificate is below all: T-136 by 5.04e-4, T-127/#470/T-115 by 4.00e-3, T-113 by 5.73e-3, T-098/T-056 by 9.10e-3. No other open issue (through #552) and no 2026-10-11 stack layer (T-147..T-155) reports 154.

**Retained.** packing/resources/web/evand-n154-2026-10-12/ (9 files retained, checkers pinned identical to the issue-399 packet, PACKER.md and timetravel.py by digest); source key [Daniel n154 2026-10-12]; HOUSES reader added; tests/test_upper_bound_reports_552.py (6) and EVERY in test_upper_bound_reports.

**Stage 4 replay (done).** certify --workers 1: 3 jobs, positive passes both maintained routes, both controls refused on both; 70,686 pair decisions, 40.97 route CPU s, 91 s wall (load 13-17). check --replay: 3 jobs equal, 75 s. Wall clearance exactly 5e-21, pair gap just under 1e-20 on both routes. Third route run from scratch with the #552 roster line added in-process (code not edited): passed, 6/6 controls, least distance 1.00e-20, upstream bytes held to the pin, no disagreement, 41 s. Regularized drawing decided the same way (diagnostic, no receipt): passes all three routes, controls refused.

**Lineage (measured, third route's tools from scratch).** arrangement_gap: no one-to-one nearest match against T-136 or Couzo's 154 (T-098). patch_lineage: 32 of T-136's squares within 1e-9 under the best placement it finds (1 to the digit): another arrangement than T-136. Upright blocks reappear to the digit from both Couzo starts (43 of the 155, 45 of the 154), so the tool cannot tell the starts apart. A scratch float optimal matching (not a repo tool, OR-1) gave corner RMS 0.318 vs T-136 and 0.393 vs Couzo's 154 (the author's 0.319, 0.396) and 0.181 vs Couzo's 155 less one square: consistent with the comment. chain_lineage.py, which the comment names, is not in the tree at 597e660 or 31523f8.

**Credit.** Evan Daniel (size-chaining QD explorer of #465/#489, time-travel test from the 5 Oct register); start credited to Francisco Couzo's 5 Oct n = 155 packing less one square (comment 14:13Z). AI: search code, run and request done with Claude (Claude Code), directed and reviewed by Evan Daniel; MIT, CREDITS.md.

**Priced plan (remaining).** W2 review of the replay and certificate (one review lane, under an agent-hour, as for #489); records lane: register T-156 (register-plan output in the lane report), add the third route's roster lines (IMPORTS_552, CREDITED (#552,154): T-136, T-098; LINEAGE (#552,154): T-098 155), decide adoption at 154 over T-136. No CPU-hour item.

**Draft acknowledgement (not posted).** "Thank you for s(154) <= 12922566401934059503377267965457/10^30 (evand/square-packing 597e660). We retained tt_n154.cert with its KKT point, input, solver report and the regularized drawing at 597e660. Both of our maintained exact routes accept the certificate and refuse its controls, and so does our third route; it is 5.04e-4 below T-136 and below every other report at 154. We will credit the start to Francisco Couzo's 5 October packing of 155 squares, as your comment asks. One request: chain_lineage.py, which the comment names, is not in the tree at 597e660 or 31523f8; could you publish it, or the round-by-round trace? We will reply with the register entry once it is on main."


**W2 review (done, 12 October; branch `review-552` from `intake-552` at 6a913c1c6, worktree agent-a5e938b4cf9effee0, not pushed).** Review at docs/project/reviews/review-2026-10-12-upper-bound-import-552.md, mapped in document-map.yaml, SYNOPSIS.md document table re-rendered. Commits: 3d914f762 (third route: IMPORTS_552, CREDITED (#552, 154): T-136, T-098; LINEAGE (#552, 154): T-098 155; seven tests in test_check_half_angle_area.py, three slow), a2588a797 (review, document map, synopsis). Verdict: accepted, finite feasibility only; seven findings RD-1 to RD-7, none blocking; V3/C3 once registered with the confirming atom E-evand-552-exact-feasibility and this review; S3 confirmed (a new arrangement moving the ceiling by 5.04e-4, as T-149, T-136, T-154); house at 154 to move from T-136 to T-156, start credited to Couzo's 155 as the author asks.

**Replays here (12 October, load 7-14, one worker).** check-claims rebuilt equal (7 s); check --replay all 3 jobs equal, "1 certificates and 3 jobs admitted" (51 s, 15:31:12Z-15:32:03Z); decide-imports --workers 1 --imports '#552' --upstream evand-n154-2026-10-12 DIR --json: passed, 11,781 pairs, 338 clipped, 6/6 controls, wall 5e-21, far wall 5.0000000007e-21 both axes, least Euclidean distance equal to the maintained gap exactly (9.99999999999998961e-21), 1 upstream check, no disagreement, 25.05 s (15:35:18Z-15:35:44Z). All 13 files of the pinned tree fetched at 597e660 at the manifest's digests (15:30:13Z-15:30:19Z). Receipts: scratchpad/lane-552-review/third-route/decide-imports-552.{json,log}, replays/maintained-replay.log, upstream-597e660.sha256. Certificate checked to be the KKT point scaled by 1 + 1e-20 about the origin (centres within 5e-36 at 35 places; S' - S*(1+1e-20) = 7.45e-31); 103 upright squares, 51 tilted.

**Findings.** RD-1: the issue's 0.396 is the matching distance to Couzo's 154 (scratch 0.393), not to the 155 the comment names (0.181); the log's submission entry says "from the 10-05 start (Couzo)". RD-2: chain_lineage.py absent at 597e660, 31523f8 and the head when checked at 15:35Z (still 31523f8); chain.py, lineage.py, lineage_reach.py, parent_retro.py present, unread. RD-3: tt_n154_regularized.json at the pin lists `by: ["Francisco Couzo"]`; the record follows the issue. RD-4: the plan's next_rung dates T-136's adoption 12 October; the case record and coverage say 11 October (adoption layer), #518 to main at 15:11Z on 12 October. RD-5, RD-7: "the chain never saw T-136's packing" and the descent from the 155 are the author's statements, to be attributed; the record's own voice says only "another arrangement than T-136's" (no one-to-one match; 32 within 1e-9, 1 to the digit under the best placement found). RD-6: kernel controls gross (unchanged). Lineage at a tenth of a unit (patch_lineage, repo tool): Couzo's 155 lands 114 of 155 (24 turned), Couzo's 154 lands 87 (10), T-136 lands 123 (32): the coarse count separates the two Couzo starts and says nothing about descent; to the digit 43 / 45 / 1, all the Couzo hits upright. The record states the start as the author's statement, consistent and not established.

**Reviewed plan.** scratchpad/lane-552/register-plan-T-156-reviewed.yaml: the T-156 entry (claim, notes, next_rung rewritten; reviews; controls both test files; artifacts with check_half_angle_area.py and the review; significance by the review), the reported atom with external_review, the confirming atom, coverage with the selected override at 154 (T-136's row to superseded_by evand-n154-2026-10-12), bibliography, resources/README line, house-adoption (front matter, priority note for T-136), case-record prose guidance, request-record changes (register T-156; reply adds RD-1, RD-2, RD-3). Custody sentences marked ADOPTION LANE for upper_bound_houses custody. Reply additions for the author: RD-1 (0.396 is to the 154), RD-2 (publish chain_lineage.py or the trace), RD-3 (the regularizer's by field).

**Validation.** pytest tests/test_check_half_angle_area.py tests/test_upper_bound_reports_552.py: 220 passed in 900.5 s (slow included; the #552 credit test 65 s), the split 552 subset 6 passed; ruff check, ruff format --check and basedpyright clean on both files; packing-validate --records: the first run failed only on the stale SYNOPSIS.md document map (re-rendered with devtools.render_document_map, in a2588a797); second run on the committed tree: 49 of 107 STEPS PASSED (a named tier; this is not the full gate), exit 0, 97.51s  wall of a 300s ceiling (33%), never recorded at this shape; failed steps: none.
