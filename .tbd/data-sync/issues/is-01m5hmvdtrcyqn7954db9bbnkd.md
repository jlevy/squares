---
type: is
id: is-01m5hmvdtrcyqn7954db9bbnkd
title: REGULARIZATION_TOOLS comment says nothing imports them; select_houses, adopt_houses and default_drawings do, so none imports in a worker
kind: bug
status: open
priority: 3
version: 1
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
created_at: 2026-10-22T11:10:00.024Z
updated_at: 2026-10-22T11:10:00.024Z
---
Owner note from review A of #721 (not a finding against that PR).

The `REGULARIZATION_TOOLS` comment in `packing/devtools/run_negative_controls.py` (line ~1380 at e6a1e026) says "nothing else in the repository imports them". That has been stale since at least f817bf191: `select_houses`, `adopt_houses` and `default_drawings` import the pruned regularization tools, so none of the three can be imported in a mutation worker. It is harmless while no control runs them, but the comment misstates the invariant and a future control on any of the three would fail at import inside the worker rather than at review.

Fix: correct the comment to name the importers, and either add a guard that no control runs a module whose import closure reaches a pruned tool, or rescue the tools those three need. Decide with think-d2he (stub copy-back) in view.

Review: https://github.com/jlevy/squares/pull/721#issuecomment-6339260683
