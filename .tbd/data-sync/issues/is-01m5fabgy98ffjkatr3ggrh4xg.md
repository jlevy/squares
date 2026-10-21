---
type: is
id: is-01m5fabgy98ffjkatr3ggrh4xg
title: "Snapshot: extend UNREAD_WORKER_OUTPUTS with 223 unread historical outputs (option b, unchanged cap)"
kind: task
status: in_progress
priority: 1
version: 2
delegate: c-lane-snapshot-prune
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T13:28:04.297Z
updated_at: 2026-10-21T13:28:09.142Z
started_at: 2026-10-21T13:28:09.142Z
---
main 51ac9d7ee reads 232,783,862 B, 10 under the 222 MiB cap; #712 (+17,031), #704 (+139,378) and #706 (+167,357) cannot land. Read-only analysis (scratchpad/snapshot-analysis.md, set C in snap/data-final.txt) finds 223 historical outputs in packing/campaign and packing/benchmarks (2,974,471 B) that no control reads, the class UNREAD_WORKER_OUTPUTS already covers. Extend it under the unchanged cap with the traced evidence the #464/#692 entries record (all 174 controls fire mutated; the 50 distinct commands print the same unmutated output with and without them), and a dated comment. Not in scope: the 39 on-request tools (a new family, the owner's assent), the atlas-print fonts (read by test_emission_precision), and the cap.
