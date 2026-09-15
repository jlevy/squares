---
type: is
id: is-01m2hf4b7raa0yecm3dcepmgb7
title: squares-workbench-ascent cannot import devtools without PYTHONPATH
kind: bug
status: open
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2h2zv3xg1w4gdy1svjsv1tx
created_at: 2026-09-15T02:42:55.351Z
updated_at: 2026-09-15T04:55:11.928Z
---
Found 2026-09-14 by PR #160 review lane D-tools (D15, D53, D61), not fixed.

The `squares-workbench-ascent` console script fails with `ModuleNotFoundError: No module named 'devtools'` unless `PYTHONPATH=.` is set. `workbench_tools.ascent` imports `devtools.known_structure`, `devtools.lock_order` and `devtools.run_projection_ratchet`, and `devtools` is not an installed package. The rebuild command in `packing/strategies/preview/README.md` fails for the same reason.

Also noticed: `strategy_execution --trace` still writes its file in place, the pattern #125 F35 (D84) fixed for capture, export and the ascent.

Related: the review's suggestion to decide whether the strategy executor belongs in `sqpack` (#160 review, Suggestions).

## Notes

2026-09-14, PR #160 review suggestion S4 ("Rethink where the strategy executor lives"), deferred here, because the location decision and this bug have one root. `workbench_tools/strategy_execution.py:14-26` imports `devtools.divide_and_concur`, `devtools.known_structure`, `devtools.run_projection_ratchet` and `devtools.sweep_structure_hints`: a general projection-solver executor housed in the browser package and reaching back into an uninstalled tree. The shared-language plan (`plan-2026-09-09-packing-strategies-as-a-shared-language.md:133-140` at `91cf28d6`) says Python algorithms belong under `packing/src/sqpack/` and general research orchestration stays outside the package, and names the package executor as an extraction candidate, but records no decision. Decide before think-qx88 (the strategy evaluation loop) imports it from `workbench_tools`; fixing these `devtools` imports is the natural moment.
