---
type: is
id: is-01m0rbwvp7wvc8ewvtjpkpc9qb
title: "D073: remove target alias and snapshot overwrite hazards from negative controls"
kind: bug
status: open
priority: 0
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-efficiency
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-23T22:29:41.702Z
updated_at: 2026-08-23T22:29:41.702Z
---
Resolved target paths defeat the symlink guard, and the read-read-replace sequence can overwrite an unrelated edit. An isolated current-worktree snapshot should make the live target unreachable and preserve exact test inputs.
