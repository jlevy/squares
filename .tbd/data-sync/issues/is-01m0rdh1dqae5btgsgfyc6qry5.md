---
type: is
id: is-01m0rdh1dqae5btgsgfyc6qry5
title: "Attic: inherited-path audit for abandoned isolation prototype"
kind: bug
status: closed
priority: 0
version: 3
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:58:11.510Z
updated_at: 2026-08-23T23:23:41.466Z
closed_at: 2026-08-23T23:23:41.466Z
close_reason: "Canceled after the scope reset: this finding belongs to the stashed hostile-isolation prototype, not the stable branch. The prototype remains recoverable in stash@{0}; no claim is made that its fixes landed. Reuse only narrowly useful timeout or crash-recovery patterns if a measured cooperative-workflow need justifies them."
resolution: canceled
duplicate_of: null
---
NEGCTL_SANDBOX_PATH_FILE was intended only for the crash selftest, but every normal negctl invocation honored it and opened the inherited arbitrary path for writing before any control. This directly violates the no-live-write guarantee. Remove path-based reporting, communicate selftest sandbox identity without opening caller-selected paths, and add an adversarial regression.

## Notes

Canceled after the scope reset: this finding belongs to the stashed hostile-isolation prototype, not the stable branch. The prototype remains recoverable in stash@{0}; no claim is made that its fixes landed. Reuse only narrowly useful timeout or crash-recovery patterns if a measured cooperative-workflow need justifies them.
