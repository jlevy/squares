---
type: is
id: is-01m0rbwsmtzm17qhrpjqcm66bg
title: "D068: eliminate live negative-control recovery takeover"
kind: bug
status: open
priority: 0
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:29:39.609Z
updated_at: 2026-08-23T22:29:39.609Z
---
A second negctl or explicit recovery can currently restore and delete a transaction whose owner is still running. Remove live-worktree transactions by isolating controls, and retain an executable refusal regression.
