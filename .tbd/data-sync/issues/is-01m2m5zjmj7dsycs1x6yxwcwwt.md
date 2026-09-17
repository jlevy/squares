---
type: is
id: is-01m2m5zjmj7dsycs1x6yxwcwwt
title: Reconcile CI topology PRs 183, 185, and 186 after the no-JS stack
kind: task
status: in_progress
priority: 1
version: 18
labels: []
dependencies:
  - type: blocks
    target: is-01m2mm43z5rhrhwg1ac775r1sc
parent_id: is-01m2k0eqwj7en422j33wtvw5dt
child_order_hints:
  - is-01m2mr9j6bs6xhve2eg1q4zdvg
  - is-01m2nf99em5gccxeaeynqzapm5
  - is-01m2nf9a0cvj36jvzep9mx7wta
  - is-01m2nf9ahn8sf67khhfcwqhxrc
  - is-01m2nhy9mwrebga1xzw3dq98bp
  - is-01m2nhy9nsqpwzpdgccyah2myd
  - is-01m2nz2awrxeaa1pgh6e7x1vjt
  - is-01m2p1yw0f08dvqdapngmdn25w
  - is-01m2pgxc5nk9hprqqt1v5xrzj3
  - is-01m2pgxe49n88xf9jaapk3rxxe
  - is-01m2phfjztg9q7vckn8he9jb9e
  - is-01m2phtqcr35drpbd01xrh0g8q
created_at: 2026-09-16T04:00:45.195Z
updated_at: 2026-09-17T02:06:18.006Z
---
After PRs 175, 178, 179, 181, and 180 reach main, reconcile rather than wholesale-merge the three overlapping CI branches. Preserve PR 183 parallel Pages architecture after fixing its critical-path checkout and remeasuring; selectively port PR 185 fixture, browser-floor, standalone typecheck, and per-file-cost improvements without replacing the admitted suite-a/suite-b sharder; preserve PR 186 wall-measurement framework after fixing its Python 3.14 Ruff syntax and rewiring it to the final topology. Require exact-head hosted measurements, one consistent 180-second wall authority, and clean fast/Page gates.

## Notes

Independent senior reviews and a separate reconciliation audit agree: do not rebase/merge obsolete #185/#186 heads. After #180, create one replacement PR from new main, cross-link both old PRs, and supersede them only after replacement merge. Preserve public suite-a/suite-b and packing-required, but replace internal item-count post-collection sharding with #185's reviewed measured pre-collection selector; port fixture/performance work, standalone typecheck, frontend-owned browser liveness, exact-verification concurrency, verified-tree reuse, and Rust cache key repair. Then port #186 wall machinery into the existing packing-required/pages-required aggregates. Fix think-pu7l first; rebuild active budgets/medians from final-topology hosted runs, keep 180s authority, satisfy think-3919 variance evidence, and require CLEAN exact-head ordinary/Page/deferred/wall gates.


2026-09-16 recovery (Claude session after both Codex continuation threads stopped at ~22:17Z): local head da2259fb is 15 commits ahead of GitHub (remote c5a33270, stale CI, shows CONFLICTING only because it predates the main merge; local is 0 behind origin/main 035d84c6). cb705c67 (review gaps, think-f5cc) was independently approved; 27a53a8a differs from it only by the 192 MiB cap; da2259fb restores 160 MiB with a dated note. Gate receipts: 27a53a8a pre-push 6,558 passed / 28 skipped, browser floor unrun (no node_modules); da2259fb pre-push running. Remaining: exact-head pre-push pass, push, PR body refresh, green hosted Packing+Pages aggregates under 180 s, fresh independent review of that head, merge, then think-lop3 (#185) and think-z74z (session record). Child bead evidence audit in progress.
