---
type: is
id: is-01m2kanffw38jyd10dxqqh8831
title: "[task] Lane 1: Certificate page PR wall under OR-14 (parallel check jobs, scoped halves, apt cache, geometry split, parallel determinism render, sparse checkout, one PDF draw, cancellable loops, Pages budgets)"
kind: task
status: in_progress
priority: 1
version: 8
labels: []
dependencies:
  - type: blocks
    target: is-01m2m5ad594cv9k37w6nm9e533
  - type: blocks
    target: is-01m2m5zjmj7dsycs1x6yxwcwwt
parent_id: is-01m2k0eqwj7en422j33wtvw5dt
child_order_hints:
  - is-01m2m59rqzb3m4qjs4h3qca405
created_at: 2026-09-15T20:03:22.746Z
updated_at: 2026-09-16T04:18:36.232Z
---
Lane 1 of epic think-xfqk. Branch claude/ci-pages-parallel in worktree lane-d-tools, PR into main. Items P1-P5 and the Pages section of gate-budgets.yaml (G4 with lane 3), from attic/ci-review/pages.md and synthesis.md in the squares-viz-explanations worktree. Before: 472 s median on stack PRs, about 381 s on PRs into main. Target: a full run in about 3 min and no browser work on PRs outside the workflow's inputs.

## Notes

2026-09-16 review repair: PR #183 respects if: always() in pull-request job reachability, budgets pages-required, and records three final-shape wall readings: 185 s, 173 s, and exact-head 281 s (geometric mean 208.0 s). Commit 7712a103 records the unfavorable exact-head result. The exact-head checks are functionally green, but the 281 s wall exceeds the 250 s branch budget and OR-14's 120-150 s target. The 234 s workbench job spent about 174 s in checkout. Remaining: reduce checkout/cache setup and remeasure; prepare still gates most work and sparse checkout is not implemented. PR #184 remains closed evidence only.
