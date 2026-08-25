---
type: is
id: is-01m0tyqh36cegypksg5f4rbdj2
title: Remove redundant source hashes and document the trust-boundary test
kind: task
status: in_progress
priority: 1
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
delegate: codex@spud10
labels:
  - packing
  - cleanup
  - focus-process
dependencies: []
parent_id: is-01m0typjn7s866m042zsemybj6
hold: null
hold_until: null
created_at: 2026-08-24T22:37:18.821Z
updated_at: 2026-08-25T02:21:37.343Z
started_at: 2026-08-25T02:21:37.342Z
---
Remove hashes recomputed from first-party sources already retained in Git, including local identity checks and reader-facing fields that add no independent assurance. Retain a checksum only when compared with an independently supplied value across a real trust boundary; record provenance with source, retrieval date, retained content, and Git history instead.
