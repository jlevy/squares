---
type: is
id: is-01m3w776pxjag9f4yy1xrh0hdz
title: "Merging stacks: use gh stack merge per the tbd stacked-prs shortcut"
kind: task
status: closed
priority: 3
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T17:12:00.988Z
updated_at: 2026-10-01T18:15:50.588Z
closed_at: 2026-10-01T18:15:50.578Z
close_reason: "Done 2026-10-01: read the stacked-prs shortcut and gh stack merge help; landed #266 and #271 with gh stack merge; procedure recorded in the bead and in memory."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'you have full control you have gh access and gh stack is installed'; 'read the tbd github stack instructions and github cli instructions'. Read (tbd shortcut stacked-prs; gh stack merge --help) and applied: 'gh stack merge 271 --yes --merge' landed #266 and #271 atomically (main c1f1b2751); #270 was not linked into the stack on GitHub (its base had been set with gh pr edit), so it was retargeted to main and merged with gh pr merge (main 7f1ad844e). For later stacks: create and link them with gh stack so gh stack merge covers every layer; never the bare REST merge call.
