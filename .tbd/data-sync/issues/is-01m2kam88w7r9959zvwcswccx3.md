---
type: is
id: is-01m2kam88w7r9959zvwcswccx3
title: "Lane 2: Packing validation PR wall under OR-14 (shard suite, split checks, cargo cache, fixtures, sweeps, sparse checkout, per-file cost, post-merge skip)"
kind: task
status: open
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2k0eqwj7en422j33wtvw5dt
created_at: 2026-09-15T20:02:42.587Z
updated_at: 2026-09-16T03:09:01.670Z
---
Lane 2 of think-xfqk, branch claude/ci-validation-shard in the consolidate-stack worktree. Scope V1-V4, V6, V7, G5, G6 from attic/ci-review/synthesis.md; V5 is stack-only. Before: PR wall 284 s (main PRs) and 298 s (stack), set by suite in 34 of 35 runs. Target about 160 s with nothing leaving the PR surface. Folds in think-jblb (suite at its 275 s ceiling).

## Notes

**2026-09-16:** pushed as PR #185. `suite` is two shards partitioned by recorded per-file cost, the type floor has its own runner, the browser floor's liveness tests moved to `frontend` (which already has Node), and the quick lane's two costliest fixtures are cut. `verified_merge_tree.py` proves a merge commit's tree matches the pull-request head that passed, but the post-merge skip is not wired to the push surface. The new ceilings are provisional until hosted runs of this shape record them. `sweeps` is untouched. A step left unreachable by any probe pattern was caught by CI and fixed in `9fc36b5f`.
