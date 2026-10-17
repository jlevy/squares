---
type: is
id: is-01m50xqsa4f5tfq632b71bj3cv
title: "Regularization leftovers: grid-slack 1 and 5 deg on 102, 236, 258, 263, 269; record outcomes for 110, 123, 155, 179, 180; 39, 55, 290, 291 under think-yk2h"
kind: task
status: closed
priority: 1
version: 17
delegate: user-eb-reg-leftovers
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
hold: null
hold_until: null
created_at: 2026-10-15T23:18:12.547Z
updated_at: 2026-10-17T01:42:47.225Z
started_at: 2026-10-16T05:22:35.967Z
closed_at: 2026-10-17T01:42:47.225Z
close_reason: "Landed in the regularization stack, merged into main on 16-17 Oct (#644 b35a6289f, #653 3301a1cf6, #654 5012a97d6, #656 76cb5cbdb, #657 c593e2bfd); PENDING_ALLOWED is empty on main."
resolution: null
duplicate_of: null
---

## Notes

2026-10-16T05:28Z user-eb-reg-leftovers: started. Branch claude/intake-2026-10-16-regularize-leftovers at e2e018f32 (main). Grid-slack at 0.5/1/5 deg running on 102 110 123 155 179 180 236 258 263 269 (run dirs laneD/runs/leftovers-deg{05,1,5}-1016, two lanes, nice 10); Evan Daniel driver (evand-regularize-leftovers-1016) next on the same ten; then selection.

2026-10-16T05:53Z user-eb-reg-leftovers: grid-slack done (runs grid-slack-leftovers-deg05-1016 / -deg1-1016 / -deg5-1016 on 102 110 123 155 179 180 236 258 263 269 270 301 305; 39 invocations, 1,613 CPU-s user+sys, 05:28-05:52Z, two lanes nice 10; timing in scratch laneD/logs/grid-timing.tsv). At 102 236 258 263 269 every threshold gives the house back (max move ~1e-19, no change). Evan Daniel driver evand-regularize-leftovers-1016 started 05:52Z on the twelve (not 301) at --workers 2. Next: regularize_select. Branch still at main e2e018f32, nothing committed.

2026-10-16T07:02Z user-eb-reg-leftovers: evand-regularize-leftovers-1016 11 of 12 done (102 258 263 269 no change; 110 123 179 row 7 refuse; 155 270 row 4 held; 180 236 row 10 admit, to be judged by the selection); 305 still in its same-side stage. Selection is chained to start when the run ends. Coordinator: lane J stacks on this branch, so the infographics cut is not mine; data commits are pushed as soon as made and never rewritten.

2026-10-16T08:01Z user-eb-reg-leftovers: runs and selection done. evand-regularize-leftovers-1016: 4,212 s wall, 2,917.2 CPU-s (receipt), 2 workers, 05:52-07:02Z; grid-slack 1,613 CPU-s; regularize_select --workers 2 at e2e018f32, 3,007 s wall (07:03-07:53Z): 0 chosen, 0 register candidates, 13 counts with no adoptable view. Per count: 102 258 263 269 no change everywhere; 236 evand +1 class/hue, grid no change; 180 all tie the axis view; 123 evand row 7, grid ties; 155 evand row 4 (9.9e-31 above U), grid worse on light/uneven; 179 all row 7 (stage falls); 110 all row 7 (fewer sides). SETTLED rewritten on the four new runs with per-count outcomes, every owed dropped; README paragraph; guide sentence; test updated; record regenerated; --check-state and test_default_drawings/test_bead_tree pass (uncommitted, waiting to stack on lane B's push, per brief).

2026-10-16T09:54Z user-eb-reg-leftovers: INTERIM. Data commit prepared LOCALLY (not pushed) on #644's branch 780d81b82: 7fb79b461 (SETTLED per-count outcomes on the four 16 Oct runs, no owed left; README paragraph; guide; test; record regenerated; --check-state and test_default_drawings/test_bead_tree pass there). Waiting for lane B's 3b/3c push to rebase onto it, then re-pin, release-impact record, validate, push, PR. Evidence tarball laneD/evidence/leftovers-1016-runs.tar.gz (sha256 6142cb07...13dc4e). Audit bead think-drze opened and claimed.

2026-10-16T11:28Z user-eb-reg-leftovers: stacked on regularize-3c e757f04f4 and PUSHED claude/intake-2026-10-16-regularize-leftovers (a6cf7810b data + evidence in packing/atlas/known-best/regularization-runs/, b0f32042e test fix for empty PENDING_ALLOWED in test_bead_tree, 6e8e2ae6d re-pin, b787baf05 papers'+site no-change record). Remaining irregular drawings, the 25 worst by light + uneven + near-axis on the stacked tree (no count pending any more):
| # | n | L+U+N | light / uneven / near-axis | classes / hues | house / stage sides | state | drawn | decided tonight by | owner now |
| --: | --: | --: | --- | --- | --- | --- | --- | --- | --- |
| 1 | 292 | 36 | 6 / 30 / 0 | 4 / 4 | 899 / 899 | regularized | regularize_grid_slack/1 | - | think-drze (opened by this audit) |
| 2 | 176 | 35 | 11 / 24 / 0 | 6 / 6 | 457 / 475 | regularized | evand-regularize | think-la7h (#644) | think-drze (opened by this audit) |
| 3 | 290 | 35 | 4 / 31 / 0 | 2 / 2 | 1018 / 1018 | exempt | house | - | think-yk2h |
| 4 | 291 | 35 | 4 / 31 / 0 | 2 / 2 | 1024 / 1024 | exempt | house | - | think-yk2h |
| 5 | 131 | 28 | 7 / 21 / 0 | 14 / 14 | 284 / 296 | regularized | regularize_grid_slack/1 | - | think-drze (opened by this audit) |
| 6 | 272 | 27 | 9 / 18 / 0 | 28 / 19 | 700 / 732 | decided-no-better | regularize_axis_components/2 | think-la7h (#644) | think-drze (opened by this audit) |
| 7 | 232 | 26 | 4 / 22 / 0 | 3 / 3 | 756 / 756 | regularized | evand-regularize | think-3zi3 (3c) | think-drze (opened by this audit) |
| 8 | 273 | 26 | 8 / 18 / 0 | 22 / 19 | 688 / 724 | regularized | evand-regularize | - | think-drze (opened by this audit) |
| 9 | 126 | 25 | 4 / 21 / 0 | 2 / 2 | 385 / 385 | regularized | evand-regularize | - | think-drze (opened by this audit) |
| 10 | 204 | 25 | 5 / 20 / 0 | 17 / 17 | 554 / 570 | decided-no-better | regularize_axis_components/2 | think-la7h (#644) | think-drze (opened by this audit) |
| 11 | 264 | 25 | 5 / 20 / 0 | 17 / 17 | 705 / 709 | regularized | regularize_grid_slack/1 | think-3zi3 (3c) | think-drze (opened by this audit) |
| 12 | 259 | 24 | 4 / 20 / 0 | 4 / 4 | 789 / 793 | regularized | evand-regularize | - | think-drze (opened by this audit) |
| 13 | 238 | 22 | 7 / 15 / 0 | 13 / 13 | 656 / 664 | regularized | regularize_grid_slack/1 | - | think-drze (opened by this audit) |
| 14 | 239 | 22 | 6 / 16 / 0 | 19 / 19 | 607 / 625 | regularized | regularize_grid_slack/1 | - | think-drze (opened by this audit) |
| 15 | 263 | 21 | 3 / 18 / 0 | 5 / 5 | 723 / 753 | decided-no-better | house | think-0ut1 (this PR) | think-drze (opened by this audit) |
| 16 | 307 | 21 | 7 / 14 / 0 | 27 / 19 | 768 / 812 | regularized | regularize_grid_slack/1 | - | think-drze (opened by this audit) |
| 17 | 171 | 19 | 4 / 15 / 0 | 3 / 3 | 510 / 510 | regularized | evand-regularize | - | think-drze (opened by this audit) |
| 18 | 175 | 19 | 4 / 15 / 0 | 3 / 3 | 502 / 502 | regularized | evand-regularize | think-3zi3 (3c) | think-drze (opened by this audit) |
| 19 | 198 | 19 | 4 / 15 / 0 | 3 / 3 | 612 / 612 | regularized | evand-regularize | - | think-drze (opened by this audit) |
| 20 | 303 | 19 | 3 / 16 / 0 | 43 / 19 | 806 / 818 | decided-no-better | regularize_axis_components/2 | think-la7h (#644) | think-drze (opened by this audit) |
| 21 | 308 | 18 | 3 / 15 / 0 | 32 / 19 | 743 / 803 | regularized | regularize_grid_slack/1 | - | think-drze (opened by this audit) |
| 22 | 123 | 17 | 1 / 16 / 0 | 2 / 2 | 329 / 329 | decided-no-better | regularize_axis_components/2 | think-0ut1 (this PR) | think-drze (opened by this audit) |
| 23 | 182 | 17 | 5 / 12 / 0 | 15 / 15 | 443 / 457 | regularized | evand-regularize | - | think-drze (opened by this audit) |
| 24 | 271 | 16 | 6 / 10 / 0 | 21 / 19 | 738 / 760 | regularized | evand-regularize | think-la7h (#644) | think-drze (opened by this audit) |
| 25 | 180 | 15 | 5 / 10 / 0 | 16 / 16 | 483 / 489 | decided-no-better | regularize_axis_components/2 | think-0ut1 (this PR) | think-drze (opened by this audit) |

2026-10-16T11:38Z user-eb-reg-leftovers: draft PR #656 (https://github.com/jlevy/squares/pull/656), base claude/intake-2026-10-16-regularize-3c, head 3f78058fe, labels project + S2. Local: records 51/52 at b787baf05, the one failure (check_documentation: unmapped retained selection.md) fixed in 3f78058fe and the step passes alone; --check-state, 244 focused tests, release_pin --check, check_release_impact vs 3c pass; --verify-atlas running. think-0ut1 can close once #656 merges (no record names it); think-co6o and think-zjmt can close now.

2026-10-16T12:22Z user-eb-reg-leftovers: PR #656 head 7e44e4bdb = merge of 3c head 97d513032 (3b's A1 credit fix + A2 evidence layout) + re-pin to 5a6f333b. Evidence moved to packing/cases/regularized_drawings/think-0ut1-2026-10-16/ (receipt, gzip reports, run.json per grid run, selection-leftovers.json/.md, tree, timing). Local at 7e44e4bdb: records --jobs 2 52/52 (141 s), --check-state, 245 focused tests, release_pin --check, check_release_impact vs 3c, check_retained_json, check_documentation all pass; --verify-atlas n=1..210 passed (570 s), 211..324 running. Hosted at 7e44e4bdb: Packing validation + Certificate page green, mergeable clean. think-0ut1 closes after #656 merges; think-co6o/think-zjmt can close now; think-drze (owner question) stays open.

2026-10-16T12:44Z user-eb-reg-leftovers: --verify-atlas n=211..324 passed (1,350 s); with n=1..210 (570 s) the whole atlas verifies at 7e44e4bdb. Lane D done; final report to the coordinator.

2026-10-16 ~12:50Z coordinator user-eb: PR #656 green at 7e44e4bdb; the ten owed counts decided on fresh runs (nothing admitted; SETTLED names the four new runs); evidence in packing/cases/regularized_drawings/think-0ut1-2026-10-16/; --verify-atlas passed in two parts. Review of #656 (with #644's final head) running. Closes at #656's merge.

2026-10-16T13:04Z user-eb-reg-leftovers: review A of #656 addressed at 6ecb4c810 (merge of 3c 9edc15a5c + A1 la7h evidence dir in _README_3A + A3 README names the 307 probe and timing file; A2 body fixed; A4 deferred to think-e533; re-pin 4013ba06). COMMENT reply posted.

2026-10-16 ~13:05Z coordinator: PR #656 MERGE-READY at 6ecb4c810 pending hosted CI on that head (Review A 0/0/0/5 'layer correct'; A1-A3, A5 fixed, A4 deferred to think-e533). Stacks on #654.

2026-10-16 19:57Z user-eb-stack: handover. The owner handed the regularization stack (#644 -> #653 -> #654 -> #656 -> #657) to lane S (user-eb-stack); claim skipped (held by its earlier lane), carrying on per the brief.

20:07Z user-eb-stack: #656 merged #654's head e2940d406 at 36b56127e; review G2 of #644 fixed at e0dcf511b (orphaned_copies check in --check-state, five settled-runs copies deleted); no-change record corrected b83170e20; re-pin c93ae8e8d; pushed. State 74/232/14/4/0, step-7 262 passed. Next #657 (think-r3cl).
