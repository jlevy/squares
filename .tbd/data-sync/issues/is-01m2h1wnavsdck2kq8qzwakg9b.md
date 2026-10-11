---
type: is
id: is-01m2h1wnavsdck2kq8qzwakg9b
title: Refresh the workbench PR stack onto main so its checks can run
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-14T22:51:32.055Z
updated_at: 2026-10-06T08:30:42.740Z
closed_at: 2026-10-06T08:30:42.740Z
close_reason: "Done: the stack it asked to refresh landed on main. PRs #125, #155, #160 and #171 merged 2026-09-15 (gh pr view: MERGED 20:05-20:08Z), so the inherited conflicts and missing pull_request runs no longer exist."
resolution: null
duplicate_of: null
---
PR #171 (claude/workbench-defaults-and-bounds) fails merges-into-main, so GitHub creates no other pull_request run for it. The conflicts are inherited: #160's head 4a1bf3b8 conflicts with main 80bcdbb0 in the same five files (README.md, SYNOPSIS.md, docs/project/document-map.yaml, packing/campaign/ledger.md, packing/devtools/controls.yaml); none is touched by #171. Needs main merged down the stack #125 -> #155 -> #160 -> #171 (the merge-upstream shortcut), with owner confirmation since #160's branch is checked out in a Codex worktree.
