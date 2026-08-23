---
type: is
id: is-01m0rfbfrwtexvw63m42ngkx6g
title: "D068: elapsed wall time was labeled as CPU time"
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-efficiency
  - measurement
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T23:30:06.747Z
updated_at: 2026-08-23T23:30:06.747Z
---
ledger.py summed effort.wall_seconds but rendered cpu/cpu-minutes, making an elapsed-time measure look like processor consumption. Correct generator, living summaries, historical labels, and reconciliation checks.
