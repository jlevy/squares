---
type: is
id: is-01m0rbwtxwgqpmmwa0r7891xfy
title: "D071: prevent inherited activity tokens from authorizing descendant writers"
kind: bug
status: open
priority: 0
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:29:40.923Z
updated_at: 2026-08-23T22:29:40.923Z
---
Runner experiment children inherit the owner token and can currently start a second mutating runner CLI under the first lease. Top-level writers must never borrow, and experiment environments must drop capabilities.
