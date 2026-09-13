---
type: is
id: is-01m2dtw210cvav449h9hkhj8fr
title: Restore the native TypeScript compiler for tsc programs while typescript-eslint keeps 6.x
kind: task
status: open
priority: 2
version: 1
labels:
  - workbench-roadmap
dependencies: []
created_at: 2026-09-13T16:51:08.960Z
updated_at: 2026-09-13T16:51:08.960Z
---
PR #160 CI: the browser floor grew from ~6s to ~40s. Part of it is that typescript-eslint 8.68 pins typescript <6.1.0, so the root typescript moved from native 7.0.2 to 6.0.2 and every tsc -p program slowed about 2.8x (locally 7.79s over 15.0 cpu-s vs 2.80s over 5.5 at 15d97a59). Proposed: root package.json typescript 7.0.2 for tsc, packages/workbench keeps 6.0.2 nested for typescript-eslint; verify npm lockfile resolves, ESLint loads the nested 6.0.2, and api-contract.test.ts (spawns root tsc, matches diagnostic text) passes on 7.0.2. Record the before/after browser-floor step time. OR-14. Readings in packing/devtools/gate-budgets.yaml checks entry.
