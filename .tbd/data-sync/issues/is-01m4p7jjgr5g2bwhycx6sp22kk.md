---
type: is
id: is-01m4p7jjgr5g2bwhycx6sp22kk
title: "PR #493 A1: tracker changes applied outside merge gate, 71 beads on branch-only paths"
kind: bug
status: closed
priority: 1
version: 6
delegate: claude-reconcile-coordinator-0vpobe
labels: []
dependencies: []
parent_id: is-01m4p7jhpbzwqvtq6set506v4b
hold: null
hold_until: null
created_at: 2026-10-11T19:38:28.759Z
updated_at: 2026-10-13T05:45:06.257Z
started_at: 2026-10-11T19:44:59.771Z
closed_at: 2026-10-13T05:45:06.257Z
close_reason: "Fixed in c60db5740: status addendum in review-2026-10-10-tbd-coordination.md and a 'What merging decides' section in the PR body; reconcile_work --branch-only-paths measures move-dependent repairs (453 beads, 62 not closed, 22 plans, all from specs/active/ under the same name); round 2's repeat steps require such repairs after the merge or a kept listing. Owner accepted round 1's applied set on 2026-10-11. Confirmed by test_branch_only_paths_finds_beads_that_dangle_on_the_base."
resolution: null
duplicate_of: null
---
PR body lacks a What merging decides section; 71 beads' spec_path exist only on this branch; record that move-dependent path repairs are applied after the move merges. docs/project/reviews/review-2026-10-10-bead-reconciliation-applied.json; PR body. Severity: High. Review: https://github.com/jlevy/squares/pull/493#pullrequestreview-5484428701

## Notes

2026-10-13 ownership transfer (OR-19): claimed by claude-tbd-moderate-pr493-address-a on 2026-10-11T19:44Z with no notes, commits or replies since; the user in session asked this session to take Review A over ('Take it over'). New delegate: claude-reconcile-coordinator-0vpobe, working on codex/bead-spec-reconciliation at 2d21b36e3.
