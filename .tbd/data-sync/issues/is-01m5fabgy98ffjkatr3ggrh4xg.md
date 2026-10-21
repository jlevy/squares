---
type: is
id: is-01m5fabgy98ffjkatr3ggrh4xg
title: "Snapshot: extend UNREAD_WORKER_OUTPUTS with 223 unread historical outputs (option b, unchanged cap)"
kind: task
status: in_progress
priority: 1
version: 3
delegate: c-lane-snapshot-prune
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-21T13:28:04.297Z
updated_at: 2026-10-21T13:37:00.349Z
started_at: 2026-10-21T13:28:09.142Z
---
main 51ac9d7ee reads 232,783,862 B, 10 under the 222 MiB cap; #712 (+17,031), #704 (+139,378) and #706 (+167,357) cannot land. Read-only analysis (scratchpad/snapshot-analysis.md, set C in snap/data-final.txt) finds 223 historical outputs in packing/campaign and packing/benchmarks (2,974,471 B) that no control reads, the class UNREAD_WORKER_OUTPUTS already covers. Extend it under the unchanged cap with the traced evidence the #464/#692 entries record (all 174 controls fire mutated; the 50 distinct commands print the same unmutated output with and without them), and a dated comment. Not in scope: the 39 on-request tools (a new family, the owner's assent), the atlas-print fonts (read by test_emission_precision), and the cap.

## Notes

2026-10-21 c-lane-snapshot-prune: branch claude/snapshot-unread-outputs-2026-10-21 (worktree scratchpad/wt-prune from 51ac9d7ee). Pushed 3763cbb9e: UNREAD_WORKER_OUTPUTS gains the 223 set-C files as 8 directory entries and name groups; an in-memory check shows the entries prune exactly snap/data-final.txt (223 files, 2,974,471 B, no other file). --source-bytes 232,783,862 -> 229,821,817 (2,962,055 under 222 MiB, comment counted). Baseline with entries running; controls, baseline without, tests and validation pending.
