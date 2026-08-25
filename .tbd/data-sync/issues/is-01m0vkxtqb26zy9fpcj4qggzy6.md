---
type: is
id: is-01m0vkxtqb26zy9fpcj4qggzy6
title: Record and prevent unfrozen validation from rewriting the packing lockfile
kind: bug
status: open
priority: 2
version: 1
labels:
  - packing
  - defect
  - focus-process
dependencies: []
created_at: 2026-08-25T04:47:45.386Z
updated_at: 2026-08-25T04:47:45.386Z
---
An unfrozen uv run used only for linting re-resolved explorations/packing/uv.lock under the host global exclude-newer policy and downgraded unrelated packages. Restore the exact HEAD lockfile, record the defect, and use frozen or direct project-environment validation for this branch.
