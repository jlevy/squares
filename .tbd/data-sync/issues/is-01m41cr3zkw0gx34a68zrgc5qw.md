---
type: is
id: is-01m41cr3zkw0gx34a68zrgc5qw
title: "#292: fix red CI after GitHub's rebase (stale data pin; n = 29 intro example 5.79 vs 5.7975)"
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
    target: is-01m41cr60k350wnfd3j1nye2xx
parent_id: is-01m41cr1mz526vz5b2a5e4z100
created_at: 2026-10-03T17:24:50.290Z
updated_at: 2026-10-03T17:46:28.768Z
closed_at: 2026-10-03T17:46:28.768Z
close_reason: null
resolution: null
duplicate_of: null
---
Local stack-merge lane. Merge-only on claude/import-2026-10-01-requests at f40260d50; merge main if moved (ff48face5, #313); root-cause the intro test; re-pin; validate; push; CI green.
