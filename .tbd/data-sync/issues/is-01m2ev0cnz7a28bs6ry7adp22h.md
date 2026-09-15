---
type: is
id: is-01m2ev0cnz7a28bs6ry7adp22h
title: Draw the stage's box with a black trace, green when locked, and a gap-bar pointer
kind: feature
status: in_progress
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-14T02:12:45.327Z
updated_at: 2026-09-15T04:49:50.838Z
---
Owner request 2026-09-13, revised four times the same day. The stage draws the box a step packs into as a bold (4 px) line: black while it is on its way, the page's --met green once it locks at the best known side of the n on show (within 1e-9 of it). A thin (1.5 px) black trace marks where the box just was. A small triangle above the gap bar's rail points down at the box's current side on that scale every frame, black until the box locks and green when it does, so it lands green on the best known rule. The geometric #container stays undrawn for the scene and probes.
Step n -> n+1: over the dwell's last 30% the previous step's outer trace clears. Over the first 20% of the move the box grows up and to the right to max(ceil(sqrt(n+1)), s(n+1)), riding further wherever the moving container breathes past it, leaving a trace inside at s(n). Over the next 12% that inner trace fades. The timeline's boxFirst (0.32 of every move) holds the new square's arrival and all block and physics motion until then. Over the settle the box contracts to s(n+1), turning green as it locks, and the trace stays outside at the grown size until the next step. Grid fills never change the box and stay green. The view holds the largest box of the step so it does not zoom as traces come and go.
Rejected earlier versions: black at the proved lower bound (inside the packing); black fixed at the grid bound with green shrinking inside it; an always-green box.
Verified 2026-09-13 on branch claude/workbench-defaults-and-bounds: package check (115 Node tests) and check_frontend pass; check_animation_editor asserts each beat of 10 -> 11 (rest locked green at 3.707 inside a trace at 4; black box at max(4, container) over a trace at 3.707 with a black pointer; trace gone and new square unseen at 32%; settled locked green at 3.877 inside a trace at 4 with the green pointer over the record rule) and an unchanged grid fill. Remaining: commit on the branch after owner review.

## Notes

2026-09-13: work moved from a detached HEAD onto local branch claude/workbench-defaults-and-bounds (worktree .claude/worktrees/pr160-workbench), created at PR #160 head 4a1bf3b8 with upstream origin/codex/review-workbench-stack. Still uncommitted and unpushed pending owner review.

2026-09-14 review of PR #171 (lane E): the box and pointer locked mid-move on 17 steps (D18, think-dujz, fixed in ac49b452); Pack and the animation studio kept a stale catalogue box and drew no container (D17, think-1ge6, fixed in 5bb067a0); the stage height was retuned on drawn geometry to 979 px with 41 px above and below the headline (D16, think-ejry, fixed in 8fe4749e), an owner look to review. Open owner question: boxFirst on steps whose box does not change size.

2026-09-14, correction: the stage height is 971 px (b7627cef), the size the owner accepted, not the 979 px of 8fe4749e; 45 px above and below the headline, 7 px clearance to clipped geometry.
