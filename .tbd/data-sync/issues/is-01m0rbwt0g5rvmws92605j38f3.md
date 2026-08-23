---
type: is
id: is-01m0rbwt0g5rvmws92605j38f3
title: "D069: stop and reap control subprocesses before cleanup"
kind: bug
status: open
priority: 0
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:29:39.983Z
updated_at: 2026-08-23T22:29:39.983Z
---
Signal handling currently restores state before a slow or TERM-ignoring checker process has exited. Terminate, wait, escalate, and reap before cleanup; exercise the real child path.
