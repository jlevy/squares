---
type: is
id: is-01m687befj0g6hrrfg6jxz126x
title: Review Couzo's s(130) certificate (stage 4) and adopt at 130 with both regularizations (#843)
kind: task
status: open
priority: 1
version: 2
labels:
  - validation
  - regularization
dependencies: []
parent_id: is-01m685msgkcqe67s8cwkqy116j
created_at: 2026-10-31T05:36:36.849Z
updated_at: 2026-10-31T07:29:23.596Z
---
Stage 4 review of Francisco Couzo's s(130) certificate (#843, T-253 on the lane's branch) and the adoption at 130. The house rule adopts the smallest validated side: Mykhailo Polkovskyi's #846 certificate at 130 (T-258 on the branch), a 2e-14 dilation of this packing 2.08e-12 below it, is adopted in its place if its review accepts it too (think-pg1y's validation bead), credited to Couzo's packing.

## Validation
- Claim: s(130) <= 466915711841738962256077475351530705109199164124122993/39228601764570445403995003040207131754000000000000000, certificates/n130.cert at franciscouzo/square-packing 3a4d95c (unchanged at the pin 712c6a6), packet couzo-issue843-2026-10-28; checkers: the two maintained exact routes (done: receipts/exact-certification.json.xz, receipts/sharp-controls.json) and a clean-room exact checker written by the reviewer.
- Run: a tbd-strong-max review sub-agent in its own worktree reading the packet as data (result-import.md, stage 4, "Who reviews, and when"); then the adoption at 130 (select_houses, upper_bound_houses, adopt_houses) with both strong generators (regularize_evand run; regularize_grid_slack at 0.5, 1 and 5 degrees), regularize_select and layer, the render step and the flip, in one pull request.
- Cost: the review about 0.02 CPU-hours (T-243's clean-room checker at 182, scaled); the regularization 5 to 25 CPU-minutes for the count; an estimate.
- Budget status: runnable, under the owner's standing 40 CPU-hour item cap.
- Possible subset under the cap: not needed.
- Depends on: a strong-tier review lane the coordinator launches; the #846 review decides which certificate re-houses 130.
- Done when: the review is mapped on the entry with verdict accepted or defects-resolved, check_results derives V3/C3, and 130 is adopted and regularized with default_drawings --check-state --base-ref origin/main and flip_regularization --check passing.
- Machine note: minutes of CPU for the review; run the regularization apart from a gate.

## Notes

2026-10-31: renumbered after #851's T-252: Couzo's 130 is T-254 (was T-253); Polkovskyi's #846 refinement at 130 is in T-259.
