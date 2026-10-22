---
type: is
id: is-01m5hmvdtrcyqn7954db9bbnkd
title: REGULARIZATION_TOOLS comment says nothing imports them; select_houses, adopt_houses and default_drawings do, so none imports in a worker
kind: bug
status: in_progress
priority: 3
version: 3
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
delegate: c-lane-tooling-1022
labels: []
dependencies: []
parent_id: is-01m1sx5m1p5868jhwcdzfkvada
hold: null
hold_until: null
created_at: 2026-10-22T11:10:00.024Z
updated_at: 2026-10-22T14:11:04.598Z
started_at: 2026-10-22T11:14:09.398Z
---
Owner note from review A of #721 (not a finding against that PR).

The `REGULARIZATION_TOOLS` comment in `packing/devtools/run_negative_controls.py` (line ~1380 at e6a1e026) says "nothing else in the repository imports them". That has been stale since at least f817bf191: `select_houses`, `adopt_houses` and `default_drawings` import the pruned regularization tools, so none of the three can be imported in a mutation worker. It is harmless while no control runs them, but the comment misstates the invariant and a future control on any of the three would fail at import inside the worker rather than at review.

Fix: correct the comment to name the importers, and either add a guard that no control runs a module whose import closure reaches a pruned tool, or rescue the tools those three need. Decide with think-d2he (stub copy-back) in view.

Review: https://github.com/jlevy/squares/pull/721#issuecomment-6339260683

## Notes

2026-10-22 c-lane-tooling-1022: done in jlevy/squares#723 (draft, head de5179c76).

- The `REGULARIZATION_TOOLS` comment now names the importers and the consequence. One correction to this bead's text: `default_drawings` does import in a worker; its imports of `regularize_evand` and `regularize_select` are function-local. Measured by importing each module with all 31 pruned `.py` files set to `None` in `sys.modules`.
- What fails at load: `algebraic_witness_reports` imports `regularize_evand` at module level, so it, `select_houses` and `adopt_houses` fail, and so do `tests/test_exact_sides.py` and `tests/test_improvement_rule.py`.
- What loads but fails when called: `default_drawings`, `register_regularized_bounds`, `regularize_axis_components` and `select_houses` import the tools inside functions. `check_results` (via `upper_bound_houses`) and `validate_schemas` (via `overview_sections` -> `default_drawings`) reach such calls and never make them.
- Decision taken: guard, not rescue. `test_no_control_loads_a_pruned_tool` (think-wtso's optional check) fails any control whose program loads a pruned file, so a future control on `select_houses` or `adopt_houses` fails at review rather than in a worker. Rescuing the tools those modules need stays open with think-d2he (stub copy-back), if the owner wants it.
