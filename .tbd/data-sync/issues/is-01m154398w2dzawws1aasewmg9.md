---
type: is
id: is-01m154398w2dzawws1aasewmg9
title: TEST DELETE ME
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m15219m6eh8fww5pm9sc2sqd
created_at: 2026-08-28T21:23:31.227Z
updated_at: 2026-08-28T21:23:56.026Z
closed_at: 2026-08-28T21:23:56.025Z
close_reason: test bead, created in error
resolution: null
duplicate_of: null
---
Delete the stale remote branches and local worktrees before the rename commit lands.

Only six unmerged remote branches carry commits (1-6 each, all from closed or superseded
PRs), but there are 13 local worktrees. A 1,160-file rename makes every one of them a
conflict minefield for anyone who later rebases, and the conflicts are the useless kind:
git resolves renames well, but only when the other side has not also moved.

Doing this first costs minutes and removes the whole class of problem.
