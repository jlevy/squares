---
type: is
id: is-01m2ev0cnz7a28bs6ry7adp22h
title: Draw the stage's upper bound bold green and its lower bound black
kind: feature
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-14T02:12:45.327Z
updated_at: 2026-09-14T02:13:27.211Z
---
Owner request 2026-09-13. On the catalogue stage the container, which is the best known upper bound on s(n), is a bold line (4 px) in the page's --met green, the same green as the best known upper bound on the gap bar's number line. The proved lower bound (facts.lower; the record's side when proved) is a 1.5 px black line inside it, anchored lower-left so the gap opens up and to the right. Proved n (59 of 324) show one green line; open n (265) show a band of 0.03 to 0.54 sides.
On a step the black line joins the green over the first fifth of the move, rides with the container while it opens and closes, and shrinks inside to n + 1's lower bound over the settle. An open-ended optimize run hides the lower line.
Done when check_animation_editor asserts the green stroke, draw order, one line for a proved n, coincident lines mid-move and n = 11 resting at 3.826447 inside 3.87708359 on a built page, and the change is on the PR branch.

## Notes

2026-09-13, uncommitted in .claude/worktrees/pr160-workbench on 4a1bf3b8: template adds #lower-bound and moves #container above #squares (both pointer-events none); application.js draws the container in --met and adds lowerBound/drawBounds after the scene render. Package check (114 Node tests) and check_frontend pass on a fresh build with Chrome; screenshots of 10->11 and 37->38 at rest, mid-move and mid-settle are in the worktree's attic/pr160-review/screens. Remaining: commit and push after owner review.
