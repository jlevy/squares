---
type: is
id: is-01m15ny48mkts23tt8ttyvwpz8
title: Restructure the README results-first, with an established-results section
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m15nqq3kzzant2e41c4wfy2e
created_at: 2026-08-29T02:35:16.626Z
updated_at: 2026-08-29T02:44:03.669Z
closed_at: 2026-08-29T02:44:03.668Z
close_reason: Landed on docs/top-down-review (26e9397).
resolution: null
duplicate_of: null
---
The merged README front-loads ~240 lines of agent process (Operating Principles through Autonomous Work Loop, lines 60-297) between Start Here and any mathematical content; Reports sits at line 463 and Exact Verification at 533. Reorder: results, inventory, reading path, reports, try-it-yourself verification, the defect story; then the work model; layout and figure-rendering last.

Add a results section the README currently lacks: T-1 (Trump n=11 verified exactly), T-4 with exp-016/017 (the Stromquist printed-proof gap and its certified repair -- a headline that the front-door rewrite in PR 58 dropped from the intro), T-2/T-3 (the LP cell decomposition and the corner at the record), the verified s(29) rational bound, and the El Moumni n=7 printed-route defects D-344-D-347 with the result standing on independent proofs. Each line links to its owner (SYNOPSIS results section, frontier cases); no volatile aggregates.

Constraint: check_readme pins the layout tree, the six-report table, the W1-W7 rows matching SYNOPSIS, and no repeated defect aggregates -- reorder within the README, do not move those out.
