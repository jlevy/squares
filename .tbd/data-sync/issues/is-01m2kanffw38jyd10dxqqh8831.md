---
type: is
id: is-01m2kanffw38jyd10dxqqh8831
title: "[task] Lane 1: Certificate page PR wall under OR-14 (parallel check jobs, scoped halves, apt cache, geometry split, parallel determinism render, sparse checkout, one PDF draw, cancellable loops, Pages budgets)"
kind: task
status: in_progress
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m2k0eqwj7en422j33wtvw5dt
created_at: 2026-09-15T20:03:22.746Z
updated_at: 2026-09-16T03:09:01.102Z
---
Lane 1 of epic think-xfqk. Branch claude/ci-pages-parallel in worktree lane-d-tools, PR into main. Items P1-P5 and the Pages section of gate-budgets.yaml (G4 with lane 3), from attic/ci-review/pages.md and synthesis.md in the squares-viz-explanations worktree. Before: 472 s median on stack PRs, about 381 s on PRs into main. Target: a full run in about 3 min and no browser work on PRs outside the workflow's inputs.

## Notes

**2026-09-16:** pushed as PR #183. Wall 472 s → 200.3 s over runs 35040456480, 35039923396 and 35039248281; the fifteen pull-request jobs now carry recorded costs and ceilings in `gate-budgets.yaml`'s `pages` section (`e2a53642`), which the workflow test demanded and the branch had not written. Still open: 200 s is above `OR-14`'s target (each browser job spends 60 to 100 s on one core of four), `prepare` still gates the rest, sparse checkout is not done, and lane 3's `pr-wall` job has a commented place here but is not wired. #184 is the scope demonstration and should be closed when this lands.
