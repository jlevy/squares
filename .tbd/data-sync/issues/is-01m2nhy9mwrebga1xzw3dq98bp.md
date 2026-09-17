---
type: is
id: is-01m2nhy9mwrebga1xzw3dq98bp
title: Restore negative-control snapshot headroom without raising its cap
kind: bug
status: closed
priority: 1
version: 5
labels:
  - ci
  - validation
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T16:49:00.571Z
updated_at: 2026-09-17T16:07:42.419Z
closed_at: 2026-09-17T16:07:42.396Z
close_reason: "Landed with PR #188 (merge 042e791c, 2026-09-17T15:54Z): hosted aggregates and the Deferred checkpoint passed on 7f387990; review dispositions in https://github.com/jlevy/squares/pull/188#issuecomment-5714064819. The first main push deployed GitHub Pages at 042e791c with verify-deployment passing."
resolution: null
duplicate_of: null
---
PR #188 exact-head suite-b run 35123561888 measured 167,998,531 snapshot bytes against the 167,772,160 cap. Identify retained generated evidence unused by mutation controls, prune it from private worker snapshots with explicit tests and dependency copy-back preserved, and rerun the exact head. Do not raise the cap.

## Notes

Reopened: The 'canceled' close reason used main's unpruned measurement (168,058,379 bytes). The #188 branch implemented this bead's remedy: c302b330 pruned the unused agenda 031-035 and exp-201/202 output roots from private snapshots, and da2259fb restores the 160 MiB cap after merging main's 192 MiB raise. Reopened to close as fixed once the exact head passes hosted CI.


2026-09-16 recovery: measured at #188 da2259fb (merged with origin/main 035d84c6) the snapshot is 144,637,123 bytes (137.9 MiB), 22.1 MiB under 160 MiB; tests/test_negative_controls.py passes 20/20. Main still carries 192 MiB from b86d6fec (#189) until #188 merges. Close as fixed, citing c302b330 and da2259fb, after the exact-head hosted Packing aggregate is green.
