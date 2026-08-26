---
type: is
id: is-01m0ycwz9g10ckxpgghd62z2qf
title: "Spike: fast PR lane and dedicated control workers"
kind: task
status: in_progress
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0y081bfavkgmmjsq9qx6aeq
created_at: 2026-08-26T06:42:40.558Z
updated_at: 2026-08-26T06:42:51.217Z
---
Implement the smallest production slice that tests the measured speed hypothesis: exclude only declared exhaustive exact modules from packing-validate --fast, run that surface on pull requests, retain full Linux and full/deep macOS on main/manual/scheduled integration events, add a stable packing-required aggregator, and give full negative controls two dedicated workers. Acceptance: workflow and validator contract tests fail first; full collection is unchanged; fast exclusion is exact; full assurance remains direct; local fast and full receipts pass; hosted PR critical path improves materially.
