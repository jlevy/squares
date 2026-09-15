---
type: is
id: is-01m2et4sraq7jn688ygk2v87n8
title: Decide whether the independent Pack panel adopts the new law and annealing scale
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-14T01:57:41.249Z
updated_at: 2026-09-15T02:59:21.534Z
---
The independent Pack panel (pack-controller.ts, pack-panel.ts) keeps its own hardcoded pair and wall law (0.15 / 2500 / 0 / 0) and a Shake slider 0..10, default 3, mapped linearly to amplitude = level / 3, which differs from the retained dial's curve above level 3. The 2026-09-13 defaults change touched only the retained controls. Needs an owner decision: align Pack (and the Search preview, which runs Pack trials) with the new law and a 0..20 dial on the same curve, or keep them separate. Attraction without a relationship mask changes Pack behaviour, so aligning needs its own measurement.

## Notes

2026-09-14, PR #160 review lane C (D46): benchmark trials now record the pair law, wall law, beat and annealed span (AnnealingConfiguration/v2; 89250df8, ab10fab8), so trials under different laws are never pooled. Whether Pack adopts the new law is still open, per the coordinator's decision.
