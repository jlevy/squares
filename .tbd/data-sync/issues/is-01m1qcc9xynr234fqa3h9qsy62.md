---
type: is
id: is-01m1qcc9xynr234fqa3h9qsy62
title: Branch off main after PR 78 merges; re-measure the fast suite and the exhaustive tier
kind: task
status: closed
priority: 0
version: 7
labels: []
dependencies:
  - type: blocks
    target: is-01m1qcnnz9mfwn7jcg8eemddq4
  - type: blocks
    target: is-01m1qcnpbkcj1npasye0hzg9pd
  - type: blocks
    target: is-01m1qcnppk7e67rxdhn9h3ddbe
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:34:35.198Z
updated_at: 2026-09-05T00:43:24.955Z
closed_at: 2026-09-05T00:43:24.954Z
close_reason: "Branch claude/port-pr80-findings off main at b93efe5c; fast suite 1034 s / 1781 tests locally, 996 s on CI; exhaustive tier 930 s locally, 892 s on CI (eight seconds under the 900 s cap). Budgets set at 1800 s for both whole-suite steps and the push step when it runs the whole suite; D-432 closed. Commit 'gate: the push tier takes the fast suite's budget...'."
resolution: null
duplicate_of: null
---
Prerequisite for every port. Branch claude/port-pr80-findings off main after PR 78 merges. Re-measure the fast suite and the exhaustive tier on main with the integer sweep in place: PR 80 raised the fast-tier budget to 2,700 s on a 1,791 s measurement and the exhaustive tier to 14,400 s on a 4,866 s one, both of the Fraction sweep; the code lane measured the n = 12 and n = 20 exact decisions at 25.5 s and 28.4 s, and 2,700 s sits above CI's 1,800 s. Drop both numbers. Port only the _push_test_step budget_seconds line, at 1,800, which is the fix D-432 already prescribes; close D-432.
