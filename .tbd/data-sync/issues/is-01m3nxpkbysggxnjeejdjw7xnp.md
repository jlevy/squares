---
type: is
id: is-01m3nxpkbysggxnjeejdjw7xnp
title: Record the existing reviews as external_review on the report entries so T-046, T-048 and T-055 derive C1
kind: task
status: in_progress
priority: 2
version: 2
delegate: w-t046-review-1026
labels:
  - packing
  - results-register
dependencies: []
parent_id: is-01m3nrt5zy2g6dpegq1fbczpzg
hold: null
hold_until: null
created_at: 2026-09-29T06:30:13.118Z
updated_at: 2026-10-26T04:02:53.538Z
started_at: 2026-10-26T04:02:53.538Z
---
The reviews review-2026-09-27-wand125-rectangle-scaling, review-2026-09-28-wand125-n50-mixed-verifier and review-2026-09-28-wand125-point-only-s21-s45 read the reported claims but are recorded only on replay entries or not at all; add an external_review block (state, date, reviewed_by, note) to E-wand125-rectangle-report, E-wand125-rectangle-2026-09-28-report, E-n050-wand125-mixed-740-report and E-n021-wand125-point-endpoint-report, then raise the declared C in results.yaml. Data commit, so re-pin DATA_REVISION.
