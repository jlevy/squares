---
type: is
id: is-01m0rbwt0g5rvmws92605j38f3
title: "Attic: subprocess-reaping audit for abandoned isolation prototype"
kind: bug
status: closed
priority: 0
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:29:39.983Z
updated_at: 2026-08-23T23:23:41.408Z
closed_at: 2026-08-23T23:23:41.408Z
close_reason: "Canceled after the scope reset: this finding belongs to the stashed hostile-isolation prototype, not the stable branch. The prototype remains recoverable in stash@{0}; no claim is made that its fixes landed. Reuse only narrowly useful timeout or crash-recovery patterns if a measured cooperative-workflow need justifies them."
resolution: canceled
duplicate_of: null
---
Signal handling currently restores state before a slow or TERM-ignoring checker process has exited. Terminate, wait, escalate, and reap before cleanup; exercise the real child path.

## Notes

Canceled after the scope reset: this finding belongs to the stashed hostile-isolation prototype, not the stable branch. The prototype remains recoverable in stash@{0}; no claim is made that its fixes landed. Reuse only narrowly useful timeout or crash-recovery patterns if a measured cooperative-workflow need justifies them.
