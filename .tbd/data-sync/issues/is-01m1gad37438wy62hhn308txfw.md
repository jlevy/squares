---
type: is
id: is-01m1gad37438wy62hhn308txfw
title: BC-140 declared-bound check allowlists unnamed refusal guards contrary to its criterion
kind: bug
status: open
priority: 0
version: 1
labels:
  - packing
  - agenda-015
  - trust-boundary
dependencies: []
created_at: 2026-09-02T05:45:22.915Z
updated_at: 2026-09-02T05:45:22.915Z
---
Agenda-015 BC-140 requires every declared parser or recursion bound to have a named bound-exceeding mutation and refuses unnamed bounds. devtools.check_declared_bounds instead passes 8 of 10 through ALLOWLIST, including MAX_COVER_NODES, MAX_COVER_DEPTH, MAX_NUMBER_TOKEN_BYTES and MAX_STABLE_ID_BYTES, whose own reasons admit their refusal guards are unreached. Keep BC-140 partial and add real bound-exceeding controls before claiming the repair complete.
