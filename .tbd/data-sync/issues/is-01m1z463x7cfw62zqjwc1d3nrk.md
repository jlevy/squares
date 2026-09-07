---
type: is
id: is-01m1z463x7cfw62zqjwc1d3nrk
title: "Cost rollups: a delegate working in another worktree is attributed to the parent's branch"
kind: chore
status: open
priority: 3
version: 1
labels:
  - process
dependencies: []
created_at: 2026-09-07T23:45:19.270Z
updated_at: 2026-09-07T23:45:19.270Z
---
Seen on 2026-09-07 while opening squares#119 (claude/font-consistency): the delegate that built the branch worked in /private/tmp/squares-font-consistency on that branch, but its harness log records the git branch of the session's working directory, which is the parent session's worktree on claude/print-sans-faces, so log_rollup attributes all 357 of its turns to the parent branch and render_pr_rollup --branch claude/font-consistency finds no turns at all. The PR body carries the delegate's own rollup totals with a sentence explaining why. Fix options: let a session record declare the worktree or branch a delegate log belongs to (an explicit attribution field the rollup honours, which fits the rule that no attribution is inferred), or have log_rollup read the branch from the log's cwd changes when the harness records them. Same shape affected squares#118's rollup, where the parent's turns inside vendor/kpress were attributed to the submodule's branch name.
