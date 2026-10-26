---
type: is
id: is-01m5v9twagap6mhtcn7ypvvrnk
title: Review Evan Daniel's s(299) certificate (stage 4) and adopt it at 299 with both regularizations (#824)
kind: task
status: open
priority: 1
version: 2
delegate: null
labels:
  - validation
  - regularization
dependencies: []
parent_id: is-01m5v9gnfdsstsbyk92bb6nk8e
created_at: 2026-10-26T05:09:52.080Z
updated_at: 2026-10-26T05:10:06.190Z
---
The stage 4 mathematical review of Evan Daniel's s(299) certificate (#824), then the adoption at 299 with both regularizations, which the house rule puts in one pull request. Registered at V0/C0 by w-imports-1026 (think-3xn9) with the replay on both maintained exact routes, gross and sharp controls and the pose-by-pose measurement retained in packing/resources/web/evand-n299-2026-10-26/.

## Validation
- Claim: s(299) <= 8901847717666168847717657266821/(5*10^29) = 17.8036954353323377..., search/packer/candidates/s299-1025.cert at evand/square-packing 1be69ca (unchanged at 6067db5, the packet's pin); checkers: the two maintained exact routes (done, receipts/exact-certification.json.xz, receipts/sharp-controls.json) and a clean-room exact checker written by the reviewer.
- Run: a tbd-strong-max review sub-agent in its own worktree, reading the packet as data (result-import.md, stage 4, "Who reviews, and when"); then the adoption: select_houses, upper_bound_houses, adopt_houses, build_known_best_atlas --update --n 299, regularize_axis_components --update-atlas --n 299, both strong generators (regularize_evand run; regularize_grid_slack at 0.5, 1 and 5 degrees), regularize_select and layer, render_regularized_atlas, default_drawings --update, flip_regularization --update, regularized_drawings, render_results --update, stamp_landed --apply, the rigidity block at 299 (screen_translation_escape --update --n 299, assess_frontier_rigidity --update), and the withdrawal of the case's conjectured optimum 17.82287565553229, which the new house is below.
- Cost: the review about 0.02 to 0.04 CPU-hours (T-243's clean-room checker at 182, scaled to 299 squares); the regularization 5 to 25 CPU-minutes by the runbook's receipts; an estimate, not a receipt.
- Budget status: runnable, under the owner's standing 40 CPU-hour item cap.
- Possible subset under the cap: not needed.
- Depends on: a strong-tier review lane (a sub-agent the coordinator launches); nothing else.
- Done when: the review is mapped on T-NNN (the #824 entry) with verdict accepted or defects-resolved, check_results derives V3/C3, and one pull request adopts the house at 299 with default_drawings --check-state --base-ref origin/main (0 pending) and flip_regularization --check passing.
- Machine note: the review needs minutes of CPU; the regularization runs share a 4-core host with a gate badly, so run them before or after the --edit tier.
