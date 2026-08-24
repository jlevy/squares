---
type: is
id: is-01m0s80qk6qxyb4p6w8e5p219p
title: "PR #17 review E12: bound and measure non-APFS negative-control snapshots"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - packing
  - focus-infrastructure
dependencies: []
parent_id: is-01m0rwwt8912eq5f3507d581e1
created_at: 2026-08-24T06:41:08.709Z
updated_at: 2026-08-24T07:13:45.819Z
closed_at: 2026-08-24T07:13:45.818Z
close_reason: "Merged in PR #18 at b3545d0: portable snapshots are source-only, 2.9 MiB today, capped at 32 MiB, and APFS/plain-copy setup was measured over five trials; D-124."
resolution: null
duplicate_of: null
---
The stacked negctl uses APFS clone copies but falls back to unrestricted cp -R per worker. Limit the copied surface, make fallback cost visible or bounded, and measure both the normal and forced-fallback path so the fast loop does not assume APFS.
