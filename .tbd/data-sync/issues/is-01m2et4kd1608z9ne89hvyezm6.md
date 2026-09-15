---
type: is
id: is-01m2et4kd1608z9ne89hvyezm6
title: Adopt the owner's 2026-09-13 workbench defaults
kind: task
status: in_progress
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies:
  - type: blocks
    target: is-01m2et4qhaset54bd7ce0239nx
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-14T01:57:34.750Z
updated_at: 2026-09-15T04:27:53.884Z
---
Owner-chosen defaults for the retained workbench controls, on PR #160's head 4a1bf3b8:
- pair law: rigidity 0.35, repulsion 950, attraction 80, range 0.15 (was 0.15 / 2500 / 0 / 0; wall law unchanged)
- annealing dial: default 9 (was 3), range widened to 0..20 (was 0..10). Levels 0..10 keep their meaning; above 10 amplitude and span keep their linear slopes and the decay power holds at 0.35, since a power at or below zero never lets the shake die.
- beat: dwell 0.6, move 0.5, correct 0.4, settle 0.3 (was 0.8 / 0.55 / 0.25 / 0.8), both the builder's single-step TIMING and the continuous beat
- desaturation floor: 0.08 (was 0.15)
The benchmark CLI, trial-record admission and timeline span helper accept anneal 0..20.
Done when the package check, workbench pytest, check_frontend pass on a rebuilt page and the change is on the PR branch.

## Notes

2026-09-13: work moved from a detached HEAD onto local branch claude/workbench-defaults-and-bounds (worktree .claude/worktrees/pr160-workbench), created at PR #160 head 4a1bf3b8 with upstream origin/codex/review-workbench-stack. Still uncommitted and unpushed pending owner review.

2026-09-14 review of PR #171 (lane E): H-211 and X-034 no longer imply level 9 sits in a measured range; the cells ran under the previous law and beat (D70, think-fhj8, fixed in 1ef0e4e8). Trials record their law and beat from #160 (D46, 89250df8).
