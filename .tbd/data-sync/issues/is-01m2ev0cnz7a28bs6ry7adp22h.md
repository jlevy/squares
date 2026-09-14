---
type: is
id: is-01m2ev0cnz7a28bs6ry7adp22h
title: Draw the stage's grid bound black and its best known side bold green
kind: feature
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-14T02:12:45.327Z
updated_at: 2026-09-14T03:01:07.448Z
---
Owner request 2026-09-13, corrected the same day. On the catalogue stage black (1.5 px) is the obvious upper bound ceil(sqrt(n)), the side of the grid that always packs n; green (4 px, the page's --met, the best known upper bound's colour on the gap bar) is the best known side, drawn on top. Where the best known packing is the grid they coincide as one bold green line. Both share the lower-left corner, so bounds open up and to the right.
On a step n -> n+1 both lines open to ceil(sqrt(n+1)) over the first fifth of the move and ride out together wherever the moving container breathes past it; over the settle green shrinks to s(n+1) while black stays. The view widens to hold the black square. An open-ended optimize run draws green on its walls and no black. #container stays as undrawn geometry for the scene and probes.
The first version drew black at the proved lower bound, inside the packing; the owner rejected it.
Done when check_animation_editor asserts green stroke and draw order, n = 10 at 3.707 inside 4, both at max(4, box) mid-move, n = 11 at 3.877 inside 4, and a grid fill as one line at 3; and the change is on the PR branch.

## Notes

2026-09-13: work moved from a detached HEAD onto local branch claude/workbench-defaults-and-bounds (worktree .claude/worktrees/pr160-workbench), created at PR #160 head 4a1bf3b8 with upstream origin/codex/review-workbench-stack. Still uncommitted and unpushed pending owner review.
