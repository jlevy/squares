---
type: is
id: is-01m2et4qhaset54bd7ce0239nx
title: Disposition historical checker assertions tied to the pre-2026-09-13 defaults
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-14T01:57:38.985Z
updated_at: 2026-09-14T02:03:53.252Z
---
check_revision7 and check_workbench are manual (not in check_frontend or CI) and assume the old defaults: the anneal dial reporting (3, 0..10, 3) and the default reproducing the recorded free-run misses; LAW_DEFAULT reproducing the old 2500*min(p, 0.15) law and cached trajectories. The dial tuple and LAW_DEFAULT constant were updated with think defaults change. Run both against the rebuilt page and, for each failure, either set the legacy settings explicitly in the check or record the assertion as retired under think-cqfc.

## Notes

2026-09-13, worktree .claude/worktrees/pr160-workbench on 4a1bf3b8 plus the think-redh and think-jk0f edits:
- check_workbench fails before any default is asserted: its first atlasTransitions call throws "atlasTransitions controls catalogue animation; use packWorkbench or searchWorkbench for the active view", because the page now arrives in the independent Pack panel. This breakage predates the defaults change (the Pack panel landed in f08bee5c, after check_workbench last passed at 614ad255).
- check_revision7 launches Playwright's bundled Chromium without the SQUARES_BROWSER_EXECUTABLE override, so it cannot run on a machine without `playwright install`; it also drives atlasTransitions and will hit the same Pack-mode guard.
Both need an Animate-mode start (or the explicit legacy settings) before their default-dependent assertions can be judged.
