---
type: is
id: is-01m52709yrrmhkftp8bap8ph4x
title: "PR #653 A4: regularize_select records its tree's revision and a dirty flag"
kind: task
status: in_progress
priority: 3
version: 3
delegate: user-eb-addr-653
labels:
  - regularization
  - pr-653
dependencies: []
parent_id: is-01m50xqnsqj449s8rz91s61rdn
hold: null
hold_until: null
created_at: 2026-10-16T11:19:23.352Z
updated_at: 2026-10-16T12:18:21.266Z
started_at: 2026-10-16T11:19:37.364Z
---
Review A on jlevy/squares#653 (Low), https://github.com/jlevy/squares/pull/653#pullrequestreview-5546818072: selection-3b.json (retained at packing/cases/regularized_drawings/think-kpm3-2026-10-16/) records its tree only as a worktree path (/home/user/squares/.claude/worktrees/reg-3b3c-select) that no longer exists, so the drawing each view was judged against is attested only by the PR body (#644's head 780d81b82). Change packing/devtools/regularize_select.py so its JSON report records `git rev-parse HEAD` of the tree it read and whether that tree was dirty (git status --porcelain non-empty), and show both in the Markdown report; add a test in packing/tests/test_regularize_select.py. Deferred from #653: a tool change outside that PR's data slice; it does not alter any committed decision.

## Notes

2026-10-16 ~12:20Z coordinator user-eb: also covers #653 follow-up review B2 (https://github.com/jlevy/squares/pull/653#pullrequestreview-5547437307): selection-3b.json names its run directories by scratch paths that will not resolve, and the atlas README does not map retained directories to run ids; regularize_select should record the tree's revision and portable run references.
