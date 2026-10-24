---
type: is
id: is-01m4h9p55gh7pe3zfsjyp83qbx
title: "Import evand beyond-corpus tilings: s(964), s(1092), s(1228) at evand/square-packing 49907ec"
kind: task
status: open
priority: 3
version: 2
labels:
  - result-import
dependencies: []
created_at: 2026-10-09T21:39:11.152Z
updated_at: 2026-10-24T08:28:41.023Z
---
evand/square-packing 49907ec search/tilings/ reports s(964) <= 31.859493881559810546..., s(1092) <= 33.840529687178261..., s(1228) <= 35.847313543154434... (n > 324, outside the case corpus). Register them as source-only beyond_horizon_claims once the (n, source_id) schema change (PR #479, think-1545) lands, in a derived or retained packet per the evand licence (MIT). Then take over the evand intake-watch row's bead from think-iyij.

## Notes

2026-10-24 coord-intake-1024: think-1545's schema landed. s(964) is inside the ledger's reach to 1024; 1092 and 1228 are above 1024 and join think-llit's walk. Resume with the evand watch read (15 commits past the last read, 659ee62) in this pass's records lane.
blocked_on: none
