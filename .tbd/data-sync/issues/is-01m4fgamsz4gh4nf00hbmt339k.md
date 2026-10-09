---
type: is
id: is-01m4fgamsz4gh4nf00hbmt339k
title: Resolve custody reachability and snapshot gate failures
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m4e36h18crs5ws6c0fm80afy
created_at: 2026-10-09T04:56:45.118Z
updated_at: 2026-10-09T04:56:45.118Z
---
Full push at818c4c372 reported six linked-proof certification failures, importlib.metadata alias reachability classification failure, and snapshot counted-cache/worker-tree contract failure. Strong correctness lane diagnoses baseline-vs-branch and minimal safe fixes; preserve custody/refusal evidence and exact tests. No broad reruns or source edits until original gate stops; coordinator commits and syncs.
