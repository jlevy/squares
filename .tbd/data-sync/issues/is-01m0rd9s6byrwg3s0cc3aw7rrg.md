---
type: is
id: is-01m0rd9s6byrwg3s0cc3aw7rrg
title: "Attic: ignored-state audit for abandoned isolation prototype"
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:54:13.707Z
updated_at: 2026-08-23T23:23:41.458Z
closed_at: 2026-08-23T23:23:41.458Z
close_reason: "Canceled after the scope reset: this finding belongs to the stashed hostile-isolation prototype, not the stable branch. The prototype remains recoverable in stash@{0}; no claim is made that its fixes landed. Reuse only narrowly useful timeout or crash-recovery patterns if a measured cooperative-workflow need justifies them."
resolution: canceled
duplicate_of: null
---
The isolated negctl reset used git reset --hard plus git clean -fd, which preserves ignored state such as __pycache__, generated caches, and other checker output. A mutation can therefore leave executable or measured state that contaminates later controls even though tracked bytes are reset. Change the sandbox reset to purge ignored artifacts, recreate only the explicitly trusted runtime link, and add a selftest that leaves an ignored poison artifact plus a tracked mutation and proves both are reset correctly.

## Notes

Canceled after the scope reset: this finding belongs to the stashed hostile-isolation prototype, not the stable branch. The prototype remains recoverable in stash@{0}; no claim is made that its fixes landed. Reuse only narrowly useful timeout or crash-recovery patterns if a measured cooperative-workflow need justifies them.
