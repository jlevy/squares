---
type: is
id: is-01m2m5zjmj7dsycs1x6yxwcwwt
title: Reconcile CI topology PRs 183, 185, and 186 after the no-JS stack
kind: task
status: in_progress
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m2k77cev2mj85dkb88nxedp8
child_order_hints:
  - is-01m2mr9j6bs6xhve2eg1q4zdvg
created_at: 2026-09-16T04:00:45.195Z
updated_at: 2026-09-16T09:31:43.363Z
---
After PRs 175, 178, 179, 181, and 180 reach main, reconcile rather than wholesale-merge the three overlapping CI branches. Preserve PR 183 parallel Pages architecture after fixing its critical-path checkout and remeasuring; selectively port PR 185 fixture, browser-floor, standalone typecheck, and per-file-cost improvements without replacing the admitted suite-a/suite-b sharder; preserve PR 186 wall-measurement framework after fixing its Python 3.14 Ruff syntax and rewiring it to the final topology. Require exact-head hosted measurements, one consistent 180-second wall authority, and clean fast/Page gates.

## Notes

Independent senior reviews completed for PRs #185 and #186 after the no-JS stack. Both are CONFLICTING/DIRTY and their old green checks do not apply to current main. #185 requires an explicit shard-authority choice; review recommends porting its measured pre-collection file-cost sharder while preserving current workbench/no-JS and rollup topology. #186 targets obsolete suite/Pages graphs, has real 316s/416s wall failures against 180s, and must be ported onto final suite-a/b plus pages-required topology. New P1 think-pu7l tracks its NaN/Inf fail-open. Begin reconciliation only after #180 merges; require one wall authority, current-base measurements, CLEAN state, and fresh exact-head checks.
