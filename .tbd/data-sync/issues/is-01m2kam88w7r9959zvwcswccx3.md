---
type: is
id: is-01m2kam88w7r9959zvwcswccx3
title: "Lane 2: Packing validation PR wall under OR-14 (shard suite, split checks, cargo cache, fixtures, sweeps, sparse checkout, per-file cost, post-merge skip)"
kind: task
status: open
priority: 1
version: 5
labels: []
dependencies:
  - type: blocks
    target: is-01m2m5ad594cv9k37w6nm9e533
  - type: blocks
    target: is-01m2m5zjmj7dsycs1x6yxwcwwt
parent_id: is-01m2k0eqwj7en422j33wtvw5dt
created_at: 2026-09-15T20:02:42.587Z
updated_at: 2026-09-16T04:18:36.239Z
---
Lane 2 of think-xfqk, branch claude/ci-validation-shard in the consolidate-stack worktree. Scope V1-V4, V6, V7, G5, G6 from attic/ci-review/synthesis.md; V5 is stack-only. Before: PR wall 284 s (main PRs) and 298 s (stack), set by suite in 34 of 35 runs. Target about 160 s with nothing leaving the PR surface. Folds in think-jblb (suite at its 275 s ceiling).

## Notes

2026-09-16 review repair: PR #185 now records every hosted PR-tier measurement and regenerates suite-file-costs.json from run 35050021006's retained shard artifacts (f462ccbb). The typecheck and checks ceilings were tightened to remain within 2x. verified_merge_tree.py is already wired on the post-merge push surface, and per-file reports are emitted/uploaded; the prior notes and PR body saying otherwise were stale. Focused validation passed (131 tests). Remaining optimizations outside this PR's delivered shard/split scope: sweeps is not further parallelized and sparse checkout is not implemented. The PR needs its new hosted run green and a fresh body before merge.
