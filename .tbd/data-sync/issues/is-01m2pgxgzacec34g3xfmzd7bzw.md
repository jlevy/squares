---
type: is
id: is-01m2pgxgzacec34g3xfmzd7bzw
title: Remove stale review worktrees and refresh the primary checkout
kind: chore
status: open
priority: 3
version: 1
labels:
  - bookkeeping
dependencies: []
created_at: 2026-09-17T01:50:21.160Z
updated_at: 2026-09-17T01:50:21.160Z
---
Measured 2026-09-16 18:47 local with 3.0 GiB free on /: /private/tmp/squares-pr175-integration (683 MB, merged), /private/tmp/squares-pr180-fix.i2Lb4b (713 MB, merged), /private/tmp/squares-pr186-review (648 MB, PR closed) still hold node_modules/.venv; nine further worktree entries are prunable (directories gone). .claude/worktrees/pr177-ci-fix holds unmerged a318f016 'Render the session close report for session 133' with no PR, superseded by later close reports on main. Codex worktrees 2e14, 88e2, 97ff, c969, ec2e and d57a are on merged branches (d57a has an uncommitted .tbd/config.yml). The primary checkout /Users/levy/wrk/github/squares is detached at 1d9c49c4 with vendor/kpress checked out at 0c9e251, 89 commits behind its recorded 515f4a08 (stale checkout, not new work). Get the owner's approval, then remove the worktrees with git worktree remove, prune, and update the primary checkout and its submodule.
