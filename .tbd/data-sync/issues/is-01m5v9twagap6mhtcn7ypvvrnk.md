---
type: is
id: is-01m5v9twagap6mhtcn7ypvvrnk
title: Review Evan Daniel's s(299) update certificate (T-258, stage 4) and adopt it at 299 with both regularizations (#824 update)
kind: task
status: in_progress
priority: 1
version: 7
delegate: bold-ritchie-l2
labels:
  - validation
  - regularization
dependencies: []
parent_id: is-01m5v9gnfdsstsbyk92bb6nk8e
hold: null
hold_until: null
created_at: 2026-10-26T05:09:52.080Z
updated_at: 2026-10-31T08:38:43.940Z
started_at: 2026-10-31T08:37:27.888Z
---
The stage 4 mathematical review of Evan Daniel's s(299) certificate of the 29 October update on #824 (T-258), and of T-248's, which it continues, then the adoption at 299 with both regularizations, which the house rule puts in one pull request. The update's certificate is registered as T-258 on #852 (lane L2, think-3guf) with the replay on both maintained exact routes, gross and sharp controls and the pose-by-pose measurement retained in packing/resources/web/evand-n299-update-2026-10-29/; T-248's is in packing/resources/web/evand-n299-2026-10-26/.

## Validation
- Claim: s(299) <= 17801238549388584084680137655023/10^30 = 17.801238549388584..., search/packer/candidates/s299_1028.cert at evand/square-packing 0e76d9f, packet evand-n299-update-2026-10-29 (T-258); checkers: the two maintained exact routes (done, receipts/exact-certification.json.xz, receipts/sharp-controls.json) and a clean-room exact checker written by the reviewer. T-248's s299-1025.cert at 1be69ca is reviewed beside it and stays recorded only.
- Run: a review sub-agent in its own worktree, reading the packets as data (result-import.md, stage 4, "Who reviews, and when"); then the adoption: select_houses, upper_bound_houses, adopt_houses, build_known_best_atlas --update --n 299, regularize_axis_components --update-atlas --n 299, both strong generators (regularize_evand run; regularize_grid_slack at 0.5, 1 and 5 degrees), regularize_select and layer, render_regularized_atlas, default_drawings --update, flip_regularization --update, regularized_drawings, render_results --update, stamp_landed --apply, the rigidity block at 299 (screen_translation_escape --update --n 299, assess_frontier_rigidity --update), and the withdrawal of the case's conjectured optimum 17.82287565553229, which the new house is below.
- Cost: the review about 0.02 to 0.04 CPU-hours; the regularization 5 to 25 CPU-minutes by the runbook's receipts; an estimate, not a receipt.
- Budget status: runnable, under the owner's standing 40 CPU-hour item cap.
- Possible subset under the cap: not needed.
- Depends on: a review lane (a sub-agent the coordinator launches); nothing else.
- Done when: the review is mapped on T-258 (and T-248) with verdict accepted or defects-resolved, check_results derives V3/C3, and one pull request adopts the house at 299 with default_drawings --check-state --base-ref origin/main (0 pending) and flip_regularization --check passing.
- Machine note: the review needs minutes of CPU; the regularization runs share a 4-core host with a gate badly, so run them before or after the --edit tier.

## Notes

2026-10-31: renumbered after #851's T-252: the #824 update is T-258 (was T-257).

2026-10-31 (bold-ritchie-l2): M-3 of docs/project/reviews/review-2026-10-31-daniel-824-299-update.md fixed: the title, Claim and pins now name the update's certificate (T-258), not T-248's. The review (lane bold-ritchie-rv-daniel, tbd-strong at xhigh) accepted both certificates for finite feasibility, T-258 for adoption and T-248 as recorded only; it is mapped on both on #852 (359ed1687), which raises both to V3/C3. The adoption at 299 and its regularization run in the same pull request.
