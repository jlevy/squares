---
type: is
id: is-01m0zn43r70spqaakb9d6tz8tt
title: Evaluate every allowed free-square count before classifying narrow partition budget
kind: bug
status: in_progress
priority: 1
version: 3
labels:
  - packing
  - pr-45-review
dependencies: []
created_at: 2026-08-26T18:25:37.530Z
updated_at: 2026-08-26T23:19:46.579Z
---
PR #45's minimal_lattice_partition stops after the first free-square count with any partition, even when that partition exceeds the declared C<=6 budget. It then marks higher allowed free-square counts not-evaluated. Exact replay at the retained 10,000-state cap shows n=26 changes from outside-registered-budget (F=1,C=7) to established (F=2,C=6). It also shows n=65,66,82,85,89 must be search-limit/indeterminate because later allowed free-count slices hit the cap; only n=38 and n=40 remain conclusively outside among the current eight. Fix selection/classification, add a regression for n=26 and capped later slices, and regenerate chunk-partitions, chunk-evidence-profile, SVG/prose/session/PR aggregates.

## Notes

Implemented in the reviewed PR 45 draft candidate: every F=0,1,2 slice is evaluated; in-budget solutions are preferred; earlier/later cap semantics are typed; n=26 and natural/synthetic capped-slice regressions pass; the dependent 3/2/23/8 corpus is regenerated. Focused and audit suites pass. Leave open until fresh strict and CI receipts complete integration.
