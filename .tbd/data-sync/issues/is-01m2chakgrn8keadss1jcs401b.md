---
type: is
id: is-01m2chakgrn8keadss1jcs401b
title: Retire obsolete spike probes and duplicate entry points by consumer audit
kind: task
status: open
priority: 2
version: 8
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-4
dependencies:
  - type: blocks
    target: is-01m2b7nakccj4tf1tgs4k86nar
  - type: blocks
    target: is-01m2cm03rtrjcg98ejb9y56jn6
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T04:45:05.422Z
updated_at: 2026-09-15T02:41:47.216Z
---
Phase 4 deletion only. The early consumer/assertion inventory is think-a9gt and is completed before extraction. After think-zisr migrates live sources and unique coverage, remove only obsolete spike entry points, duplicate/revision probes, and temporary devtools wrappers whose consumers have migrated. Acceptance: every deletion cites the inventory disposition and replacement coverage or no-consumer evidence; no build/CI/capture/benchmark/documented invocation depends on the old tree. Retain research records, source archives, negative experiments and their reproduction tools. Consolidate workbench-specific surviving tools under packages/workbench.

## Notes

2026-09-13 PR #160 checkpoint: package build uses package-owned sources; focused browser checks replace current Pack/Search/Animate/accessibility semantics. Historical check_workbench pair-Pack assertions are documented as exploratory and fail against independent Pack; inventory unique legacy coverage and retire obsolete paths before closing.

2026-09-14, PR #160 review lane D-tools: `probes/candidate/facts_opacities.js` is retired (D67, 9baad048), and `check_candidate` no longer claims the generated spike views, which are frozen historical output. `animation_from_trace.py`'s summary CLI is retired: it printed the frame, square and distinct-side counts, and `muting_from_animation` and `trajectory_from_animation` survive in `animation_render.py` (D88, think-9hky).
