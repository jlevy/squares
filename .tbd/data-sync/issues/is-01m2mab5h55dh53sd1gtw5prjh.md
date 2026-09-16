---
type: is
id: is-01m2mab5h55dh53sd1gtw5prjh
title: Reclaim stale PR review worktrees and bound temporary storage
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m2k77cev2mj85dkb88nxedp8
created_at: 2026-09-16T05:16:59.299Z
updated_at: 2026-09-16T05:17:22.204Z
closed_at: 2026-09-16T05:17:22.199Z
close_reason: The reversible cleanup and preservation audit are complete; the remaining physical reclamation is intentionally the owner's Trash review/empty step.
resolution: null
duplicate_of: null
---
Audit the squares repository, Claude/Codex worktrees, temporary PR checkouts, and package caches under the trash-only macOS cleanup contract. Preserve session state, local-only commits, active writers, current PR worktrees, and the unpublished PR #175 amendment. Stage only explicit inactive reconstructible paths, measure logical and physical effects, and leave Trash unemptied for owner review.

## Notes

2026-09-15 storage checkpoint: staged 13,764,828 KiB (about 13.13 GiB logical) in macOS Trash and did not empty it. The staged set comprises 11 generated PR-review tree copies, six generated artifacts from merged PR #155, eight clean remote-recoverable old worktrees/copies, and two clean temporary PR worktrees. The squares checkout fell from about 20 GiB to 8,671,108 KiB; .claude/worktrees is now 7,163,024 KiB. Stopped five obsolete squares validation roots and verified their children exited. Preserved root vendor/kpress modification, current Route S worktree, active PR #175/#183/#185/#186 trees, unpublished e4d96b6f worktree, all local-only or dirty trees, all agent session/history stores, a live #180 repair writer, and the globally locked uv cache. Remaining squares temp trees total 8,451,572 KiB and are retained because they contain local-only/uncommitted work, current amendment state, or a live writer. Physical free space is 11,996,360 KiB; staged files will not release their remaining APFS allocation until the owner inspects and empties Trash.
