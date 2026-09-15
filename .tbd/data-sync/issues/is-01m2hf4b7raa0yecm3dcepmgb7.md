---
type: is
id: is-01m2hf4b7raa0yecm3dcepmgb7
title: squares-workbench-ascent cannot import devtools without PYTHONPATH
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2h2zv3xg1w4gdy1svjsv1tx
created_at: 2026-09-15T02:42:55.351Z
updated_at: 2026-09-15T04:05:13.106Z
---
Found 2026-09-14 by PR #160 review lane D-tools (D15, D53, D61), not fixed.

The `squares-workbench-ascent` console script fails with `ModuleNotFoundError: No module named 'devtools'` unless `PYTHONPATH=.` is set. `workbench_tools.ascent` imports `devtools.known_structure`, `devtools.lock_order` and `devtools.run_projection_ratchet`, and `devtools` is not an installed package. The rebuild command in `packing/strategies/preview/README.md` fails for the same reason.

Also noticed: `strategy_execution --trace` still writes its file in place, the pattern #125 F35 (D84) fixed for capture, export and the ascent.

Related: the review's suggestion to decide whether the strategy executor belongs in `sqpack` (#160 review, Suggestions).
