---
type: is
id: is-01m4t0vsew8g1zpf71sw59s0ax
title: "Defect: numerical receipts record tolerance-blurred minima"
kind: bug
status: open
priority: 2
version: 1
labels:
  - verification
dependencies: []
created_at: 2026-10-13T06:58:08.475Z
updated_at: 2026-10-13T06:58:08.475Z
---
The numerical-feasibility receipts' minimum_containment_clearance and minimum_best_pair_gap come from _margin_summary's tolerance-aware sign, so they are not true minima: n = 10's receipt says 0/0 while its exact pair gap is -6.86e-30 (docs/project/reviews/review-2026-10-13-verification-gaps.md, gap 2). Fix the summary, regenerate the 92 receipts, and log the defect in packing/defects.yaml.
