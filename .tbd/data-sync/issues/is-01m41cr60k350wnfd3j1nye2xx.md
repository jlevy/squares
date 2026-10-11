---
type: is
id: is-01m41cr60k350wnfd3j1nye2xx
title: "#298: restack onto rebased #292 and current main without rewriting history"
kind: task
status: closed
priority: 1
version: 4
labels:
  - merge
dependencies:
  - type: blocks
    target: is-01m41crc9rnphq77swdexdmgtx
  - type: blocks
    target: is-01m41crar5hfkvrr67d483me0s
parent_id: is-01m41cr1mz526vz5b2a5e4z100
created_at: 2026-10-03T17:24:52.371Z
updated_at: 2026-10-03T17:51:15.989Z
closed_at: 2026-10-03T17:51:15.988Z
close_reason: null
resolution: null
duplicate_of: null
---
Records lane. (1) push the c831b4ee0 main merge (62fe71fb3 + README/intro fixes); (2) merge origin/main ff48face5+ (SYNOPSIS, document-map via render_document_map); (3) git merge -s ours f40260d50; (4) merge #292's fix commits normally; validate; push; re-pin; dispatch; confirm gh pr view 298 mergeable.
