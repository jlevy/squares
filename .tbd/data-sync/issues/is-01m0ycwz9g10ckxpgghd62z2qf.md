---
type: is
id: is-01m0ycwz9g10ckxpgghd62z2qf
title: "Spike: fast PR lane and dedicated control workers"
kind: task
status: in_progress
priority: 0
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0y081bfavkgmmjsq9qx6aeq
created_at: 2026-08-26T06:42:40.558Z
updated_at: 2026-08-26T07:12:02.669Z
---
Implement the smallest production slice that tests the measured speed hypothesis: exclude only declared exhaustive exact modules from packing-validate --fast, run that surface on pull requests, retain full Linux and full/deep macOS on main/manual/scheduled integration events, add a stable packing-required aggregator, and give full negative controls two dedicated workers. Acceptance: workflow and validator contract tests fail first; full collection is unchanged; fast exclusion is exact; full assurance remains direct; local fast and full receipts pass; hosted PR critical path improves materially.

## Notes

Implemented fast PR lane and stable aggregator; marked four measured slow exact modules; added disjoint 101-core/30-exact validator steps; set full controls to two workers. Local fast gates: 27.38s and 33.85s. Controls: 62 pass in 100.32s versus 158.54s baseline. Focused contracts: 38 pass. Corrected full attempt: all 30 exact pass in 254.16s; concurrent core hit ENOSPC with 359 MiB free, then 101 core pass alone in 15.26s. Next: commit/push PR 41 and record hosted timing.
