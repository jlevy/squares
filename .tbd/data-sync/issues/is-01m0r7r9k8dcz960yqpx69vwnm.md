---
type: is
id: is-01m0r7r9k8dcz960yqpx69vwnm
title: Isolate and parallelize mutation controls without repository residue
kind: bug
status: open
priority: 0
version: 1
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - review
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T21:17:17.799Z
updated_at: 2026-08-23T21:17:17.799Z
---
Replace in-place mutation of tracked files with isolated per-control workspaces or an equivalently safe transaction boundary, then run independent controls concurrently. This is the remediation path for D-035 and must survive interruption, timeout, and worker failure.

Acceptance: every control starts from a declared revision, cannot expose mutations to another worker or the working tree, cleans up after normal and forced termination, preserves exact expected-failure matching, passes serial-versus-parallel differential tests, and shows a reproducible throughput improvement.
