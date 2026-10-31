---
type: is
id: is-01m687bfrjjekhpb89tv186htv
title: Review Couzo's 232, 260, 307 certificates (#844, a5a5d76) and adopt at 232 and 307 with both regularizations
kind: task
status: open
priority: 1
version: 2
labels:
  - validation
  - regularization
dependencies: []
parent_id: is-01m685nejvjntazeebg3zn18mt
created_at: 2026-10-31T05:36:38.162Z
updated_at: 2026-10-31T07:29:24.205Z
---
Stage 4 review of Francisco Couzo's a5a5d76 certificates at 260 and 307 (T-254 on the lane's branch) and his #844 certificates at 232, 260 and 307 (T-255), and the adoption at 232 and 307, where #844's are the smallest reported sides. At 260 Evan Daniel's #845 certificate (T-256) is lower and is adopted instead if validated (think-17wo's validation bead).

## Validation
- Claim: s(232) <= 7617348902520572307222120733/483283363059000000000000000, s(260) <= 104381051573626493618357957479/6274019722347000000000000000 and s(307) <= 2707897969116659515550794271467451840032974544063449693/150612387934832692306604131393579915999000000000000000 at franciscouzo/square-packing 712c6a6 (packet couzo-issue844-2026-10-28), and a5a5d76's 260 and 307 (packet couzo-a5a5d76-2026-10-28); checkers: the two maintained exact routes (done, with sharp controls) and a clean-room exact checker written by the reviewer.
- Run: a tbd-strong-max review sub-agent in its own worktree reading both packets as data; then the adoption at 232 and 307 with both strong generators (regularize_evand run; regularize_grid_slack at 0.5, 1 and 5 degrees), regularize_select and layer, the render step and the flip, in one pull request.
- Cost: the review about 0.05 CPU-hours for five certificates; the regularization 10 to 50 CPU-minutes for two counts; an estimate.
- Budget status: runnable, under the owner's standing 40 CPU-hour item cap.
- Possible subset under the cap: not needed.
- Depends on: a strong-tier review lane the coordinator launches.
- Done when: the review is mapped on both entries, check_results derives V3/C3, and 232 and 307 are adopted and regularized with default_drawings --check-state --base-ref origin/main and flip_regularization --check passing.
- Machine note: minutes of CPU for the review; run the regularization apart from a gate.

## Notes

2026-10-31: renumbered after #851's T-252: a5a5d76 is T-255 and #844 is T-256 (were T-254, T-255).
