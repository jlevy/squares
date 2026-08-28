---
type: is
id: is-01m15441mc3v07taypnqeycjqc
title: Prune stale branches and worktrees before the move
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01m15441zgw9e4ez6g7v8d1mrm
parent_id: is-01m15219m6eh8fww5pm9sc2sqd
created_at: 2026-08-28T21:23:56.171Z
updated_at: 2026-08-28T23:46:53.053Z
closed_at: 2026-08-28T23:46:53.052Z
close_reason: "Not required by the move, and not done: deleting branches is destructive and the reorg landed without it. The six unmerged remote branches carry 1-6 commits each and are all stale closed-PR branches; they can be deleted whenever you want, independently of this epic."
resolution: null
duplicate_of: null
---
Delete the stale remote branches and local worktrees before the rename commit lands.

Only six unmerged remote branches carry commits (1-6 each, all from closed or superseded
PRs), but there are 13 local worktrees. A 1,160-file rename makes every one of them a
conflict minefield for anyone who later rebases, and the conflicts are the useless kind:
git resolves renames well, but only when the other side has not also moved.

Doing this first costs minutes and removes the whole class of problem.
