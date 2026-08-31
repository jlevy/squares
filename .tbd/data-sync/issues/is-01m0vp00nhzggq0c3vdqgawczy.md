---
type: is
id: is-01m0vp00nhzggq0c3vdqgawczy
title: Reconcile packing mutation-control counts after merged cleanup
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m0vnq7t0x9ydha20bpdxmjzk
created_at: 2026-08-25T05:23:54.160Z
updated_at: 2026-08-25T05:37:41.986Z
closed_at: 2026-08-25T05:37:41.985Z
close_reason: Engineering plan and epic now remove stale inventory, report 58 controls, cite D-226 through D-228, and record merged PR 23 plus the post-merge validation receipt.
resolution: null
duplicate_of: null
---
The focused negative-control gate passes 58 controls, but the implemented engineering maturity plan and engineering epic say 56; the plan also has stale module/test inventory and miscites the CI integration defects as D-219–D-221 instead of D-226–D-228. Remove volatile inventory, reconcile current/final evidence and bead notes, retain historical baselines, and log the documentation bookkeeping defect.
