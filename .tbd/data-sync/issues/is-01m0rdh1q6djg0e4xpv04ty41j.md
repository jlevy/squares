---
type: is
id: is-01m0rdh1q6djg0e4xpv04ty41j
title: "Attic: Git-environment audit for abandoned isolation prototype"
kind: bug
status: closed
priority: 0
version: 3
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:58:11.813Z
updated_at: 2026-08-23T23:23:41.473Z
closed_at: 2026-08-23T23:23:41.473Z
close_reason: "Canceled after the scope reset: this finding belongs to the stashed hostile-isolation prototype, not the stable branch. The prototype remains recoverable in stash@{0}; no claim is made that its fixes landed. Reuse only narrowly useful timeout or crash-recovery patterns if a measured cooperative-workflow need justifies them."
resolution: canceled
duplicate_of: null
---
Snapshot, init, reset, and clean Git subprocesses inherited GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE, global config, templates, and hooks. These can redirect operations outside the temporary repository or execute external hooks, invalidating isolation and potentially touching live Git state. Sanitize all Git environment/config boundaries and rehearse poisoned redirection plus hook settings.

## Notes

Canceled after the scope reset: this finding belongs to the stashed hostile-isolation prototype, not the stable branch. The prototype remains recoverable in stash@{0}; no claim is made that its fixes landed. Reuse only narrowly useful timeout or crash-recovery patterns if a measured cooperative-workflow need justifies them.
