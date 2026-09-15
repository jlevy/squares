---
type: is
id: is-01m2heyv03k74ezzacjp323hag
title: "PR #160 review D15: the ascent writes a stale feasible flag on padded frames"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:54.882Z
updated_at: 2026-09-15T02:40:54.765Z
closed_at: 2026-09-15T02:40:54.764Z
close_reason: "Fixed on #160 at e90187c8: padded frames get feasible = False; test_ascent_and_strategies.py renders a small ascent and requires every padded frame infeasible and unchecked on export (fails with the fix reverted)."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

The ascent wrote a stale `feasible: true` on padded frames (waiting squares parked after feasibility was computed), and no test exported an ascent and checked padded frames. The export half was fixed at 15d97a59.

Source: #125 F4. Related: think-cttv.

Files: `packages/workbench/tools/workbench_tools/ascent.py:141`, `:166-173`; `packages/workbench/tests/test_python_contract_repairs.py`.
