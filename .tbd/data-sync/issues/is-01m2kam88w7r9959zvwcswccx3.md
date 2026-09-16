---
type: is
id: is-01m2kam88w7r9959zvwcswccx3
title: "Lane 2: Packing validation PR wall under OR-14 (shard suite, split checks, cargo cache, fixtures, sweeps, sparse checkout, per-file cost, post-merge skip)"
kind: task
status: in_progress
priority: 1
version: 7
labels: []
dependencies:
  - type: blocks
    target: is-01m2m5ad594cv9k37w6nm9e533
  - type: blocks
    target: is-01m2m5zjmj7dsycs1x6yxwcwwt
parent_id: is-01m2k0eqwj7en422j33wtvw5dt
created_at: 2026-09-15T20:02:42.587Z
updated_at: 2026-09-16T20:39:21.043Z
---
Lane 2 of think-xfqk, branch claude/ci-validation-shard in the consolidate-stack worktree. Scope V1-V4, V6, V7, G5, G6 from attic/ci-review/synthesis.md; V5 is stack-only. Before: PR wall 284 s (main PRs) and 298 s (stack), set by suite in 34 of 35 runs. Target about 160 s with nothing leaving the PR surface. Folds in think-jblb (suite at its 275 s ceiling).

## Notes

Senior review of PR #185 exact head f462ccbb against current main b1b2d30f: REQUEST CHANGES. GitHub is CONFLICTING/DIRTY across eight workflow/validation/budget/test files; its green run 35052543153 used obsolete base 21a68102. The substantive choice is PR185 measured pre-collection file-cost sharding versus main post-collection whole-module suite-a/suite-b sharding. Reviewer recommends retaining the measured pre-collection approach, preserving current no-JS/workbench changes and packing-required rollup, removing the superseded suite_shard.py path, regenerating costs/ceilings, refreshing body claims, and requiring fresh exact-head CI. Implementation itself passed Ruff, diff check, and 315 focused tests; no second defect found.

2026-09-16 reconciliation: PR #188 now owns the integrated Packing lane. The Rust engine cache is keyed by the tracked packing/sqsearch tree and rustc identity. Only exact hits backdate sources; misses explicitly build the current tree before validation, and an explicit successful post-gate save binds that build to the primary key. This prevents a verified-main skip from promoting a partially restored stale target. Closure still requires hosted exact-head cache-hit evidence and the coherent two-run suite-cost cohort.
