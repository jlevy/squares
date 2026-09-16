---
type: is
id: is-01m2m5zjmj7dsycs1x6yxwcwwt
title: Reconcile CI topology PRs 183, 185, and 186 after the no-JS stack
kind: task
status: in_progress
priority: 1
version: 10
labels: []
dependencies: []
parent_id: is-01m2k0eqwj7en422j33wtvw5dt
child_order_hints:
  - is-01m2mr9j6bs6xhve2eg1q4zdvg
  - is-01m2nf99em5gccxeaeynqzapm5
  - is-01m2nf9a0cvj36jvzep9mx7wta
  - is-01m2nf9ahn8sf67khhfcwqhxrc
  - is-01m2nhy9mwrebga1xzw3dq98bp
  - is-01m2nhy9nsqpwzpdgccyah2myd
created_at: 2026-09-16T04:00:45.195Z
updated_at: 2026-09-16T16:49:00.600Z
---
After PRs 175, 178, 179, 181, and 180 reach main, reconcile rather than wholesale-merge the three overlapping CI branches. Preserve PR 183 parallel Pages architecture after fixing its critical-path checkout and remeasuring; selectively port PR 185 fixture, browser-floor, standalone typecheck, and per-file-cost improvements without replacing the admitted suite-a/suite-b sharder; preserve PR 186 wall-measurement framework after fixing its Python 3.14 Ruff syntax and rewiring it to the final topology. Require exact-head hosted measurements, one consistent 180-second wall authority, and clean fast/Page gates.

## Notes

Independent senior reviews and a separate reconciliation audit agree: do not rebase/merge obsolete #185/#186 heads. After #180, create one replacement PR from new main, cross-link both old PRs, and supersede them only after replacement merge. Preserve public suite-a/suite-b and packing-required, but replace internal item-count post-collection sharding with #185's reviewed measured pre-collection selector; port fixture/performance work, standalone typecheck, frontend-owned browser liveness, exact-verification concurrency, verified-tree reuse, and Rust cache key repair. Then port #186 wall machinery into the existing packing-required/pages-required aggregates. Fix think-pu7l first; rebuild active budgets/medians from final-topology hosted runs, keep 180s authority, satisfy think-3919 variance evidence, and require CLEAN exact-head ordinary/Page/deferred/wall gates.
