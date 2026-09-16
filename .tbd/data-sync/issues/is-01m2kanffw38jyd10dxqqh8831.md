---
type: is
id: is-01m2kanffw38jyd10dxqqh8831
title: "[task] Lane 1: Certificate page PR wall under OR-14 (parallel check jobs, scoped halves, apt cache, geometry split, parallel determinism render, sparse checkout, one PDF draw, cancellable loops, Pages budgets)"
kind: task
status: closed
priority: 1
version: 10
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
updated_at: 2026-09-16T05:03:07.645Z
closed_at: 2026-09-16T05:03:07.644Z
close_reason: "PR #183 final head is green, mergeable, and measured at 173 s, meeting the lane objective."
resolution: null
duplicate_of: null
---
Lane 1 of epic think-xfqk. Branch claude/ci-pages-parallel in worktree lane-d-tools, PR into main. Items P1-P5 and the Pages section of gate-budgets.yaml (G4 with lane 3), from attic/ci-review/pages.md and synthesis.md in the squares-viz-explanations worktree. Before: 472 s median on stack PRs, about 381 s on PRs into main. Target: a full run in about 3 min and no browser work on PRs outside the workflow's inputs.

## Notes

2026-09-16 completed review repair: PR #183 final head 4e25f5f5 is mergeable/CLEAN and all exact-head checks are green. Sparse/blobless checkout cut the adverse exact-head run from 281 s (workbench 234 s; checkout about 171-174 s) to 186 s, then a final exact-head run to 173 s (workbench 53 s; checkout 8 s). The slowest browser cell is 92 s. Focused 103 tests, 19 workflow tests, edit tier, records tier, page budgets, and deterministic build all pass. think-sqi7 remains intentionally separate because its future probe trees/files do not exist on this branch.
