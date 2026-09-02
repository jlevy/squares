---
type: is
id: is-01m1gad37438wy62hhn308txfw
title: BC-140 declared-bound check allowlists unnamed refusal guards contrary to its criterion
kind: bug
status: open
priority: 2
version: 3
labels:
  - packing
  - agenda-015
  - trust-boundary
dependencies: []
created_at: 2026-09-02T05:45:22.915Z
updated_at: 2026-09-02T19:06:39.272Z
---
Agenda-015 BC-140 requires every declared parser or recursion bound to have a named bound-exceeding mutation and refuses unnamed bounds. The annotation-aware checker now discovers 24 bounds and names all 14 n54 author/verifier caps, but still passes 8 of 24 through ALLOWLIST, including MAX_COVER_NODES, MAX_COVER_DEPTH, MAX_NUMBER_TOKEN_BYTES and MAX_STABLE_ID_BYTES, whose own reasons admit their refusal guards are unreached. Keep BC-140 partial and add real bound-exceeding controls before claiming the repair complete.
