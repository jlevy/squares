---
type: is
id: is-01m2ph0tx2ewqc6ndt013j8zy0
title: Every tbd sync dirties .tbd/config.yml in the worktree it runs in
kind: chore
status: open
priority: 2
version: 2
labels:
  - tooling
  - bookkeeping
dependencies: []
created_at: 2026-09-17T01:52:09.632Z
updated_at: 2026-09-17T02:36:37.609Z
---
With tbd 0.9.0 installed, tbd sync adds two docs_cache entries that the committed .tbd/config.yml lacks: shortcuts/standard/stacked-prs.md and guidelines/agent-run-operations-rules.md. Reproduced 2026-09-16 in the primary checkout. The uncommitted change appeared in the d57a workbench worktree and the PR #190 worktree, and the interrupted Codex thread spent turns patching it out before and after each sync. It is not workbench content. Fix: on a small branch, run tbd setup --auto (as tbd prime recommends after upgrades) or commit the two entries, review the resulting diff, and merge, so sync leaves worktrees clean. tbd also reports 2 forked docs with upstream updates (tbd docs update); decide those in the same change.

## Notes

2026-09-17: the committed .tbd/config.yml pins tbd_version 0.8.1 (fallback 0.8.1) while 0.9.0 is installed, so the proper fix is running tbd setup --auto under 0.9.0 on its own branch, which records the upgrade and may also refresh generated agent surfaces (AGENTS.md sections, skills). Review that diff as a tooling change; do not fold it into an unrelated PR.
