---
type: is
id: is-01m2heyyn9t55xkm5f79rggk6h
title: "PR #160 review D61: tools print or store a side for unchecked arrangements"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:58.632Z
updated_at: 2026-09-15T02:40:57.855Z
closed_at: 2026-09-15T02:40:57.854Z
close_reason: 'Fixed on #160 at e90187c8: FairReach carries packing_valid with null side and excess when the settle fails the geometry check (Python, schema, browser decoder); ascent and strategy_execution print "not a packing" instead of a side; Python and Node tests with overlapping settles.'
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

Tools printed or stored a side for unchecked arrangements: `ascent.py` recorded `fair_side`/`excess_pct` from an unchecked settle (`FairReach` had no validity field), and `strategy_execution` printed "reached ... (excess %)" without validity. Owner rule: an unchecked arrangement is never presented as a packing.

Source: #160 R12 (tool items). Related: think-o4pj, think-e74w.

Files: `packages/workbench/tools/workbench_tools/ascent.py:110-122`, `:239-244`; `animation_records.py:50-54`; `packages/workbench/src/data/animation.ts:54`; `packing/strategies/packing-animation.schema.yaml` `fair_reach`; `strategy_execution.py:566`.
