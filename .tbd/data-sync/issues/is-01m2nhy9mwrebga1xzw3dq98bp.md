---
type: is
id: is-01m2nhy9mwrebga1xzw3dq98bp
title: Restore negative-control snapshot headroom without raising its cap
kind: bug
status: closed
priority: 1
version: 2
labels:
  - ci
  - validation
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T16:49:00.571Z
updated_at: 2026-09-16T21:24:24.608Z
closed_at: 2026-09-16T21:24:24.607Z
close_reason: "The proposed no-cap-raise remedy was rejected by measurement: the tracked snapshot reached 168,058,379 bytes because of ordinary retained source and compact kinetics records, not disposable generated evidence. Merged PR #189 reset the cap from 160 MiB to 192 MiB, preserving roughly 32 MiB of operating headroom and a 576 MiB bound for three portable workers. The validation failure is fixed, but not by this bead's prescribed mechanism."
resolution: canceled
duplicate_of: null
---
PR #188 exact-head suite-b run 35123561888 measured 167,998,531 snapshot bytes against the 167,772,160 cap. Identify retained generated evidence unused by mutation controls, prune it from private worker snapshots with explicit tests and dependency copy-back preserved, and rerun the exact head. Do not raise the cap.
