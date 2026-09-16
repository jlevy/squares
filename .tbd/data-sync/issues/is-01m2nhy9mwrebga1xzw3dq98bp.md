---
type: is
id: is-01m2nhy9mwrebga1xzw3dq98bp
title: Restore negative-control snapshot headroom without raising its cap
kind: bug
status: open
priority: 1
version: 1
labels:
  - ci
  - validation
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T16:49:00.571Z
updated_at: 2026-09-16T16:49:00.571Z
---
PR #188 exact-head suite-b run 35123561888 measured 167,998,531 snapshot bytes against the 167,772,160 cap. Identify retained generated evidence unused by mutation controls, prune it from private worker snapshots with explicit tests and dependency copy-back preserved, and rerun the exact head. Do not raise the cap.
