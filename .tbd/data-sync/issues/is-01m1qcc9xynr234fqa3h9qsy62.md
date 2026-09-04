---
type: is
id: is-01m1qcc9xynr234fqa3h9qsy62
title: Branch off main after PR 78 merges; re-measure the fast suite and the exhaustive tier
kind: task
status: open
priority: 0
version: 1
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:34:35.198Z
updated_at: 2026-09-04T23:34:35.198Z
---
Prerequisite for every port. Branch name claude/port-pr80-findings. Re-measure the fast suite and the exhaustive tier on main with the integer sweep in place (PR 80 measured 1,789 s and 4,866 s on the Fraction sweep; this branch runs the fast suite in 1,031 s on four cores). Then set the push-step and exhaustive budgets deliberately, closing D-432, which already prescribes the push-step budget.
