---
type: is
id: is-01m1qcc9xynr234fqa3h9qsy62
title: Branch off main after PR 78 merges; re-measure the fast suite and the exhaustive tier
kind: task
status: open
priority: 0
version: 5
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
updated_at: 2026-09-04T23:41:12.285Z
---
Prerequisite for every port. Branch claude/port-pr80-findings off main after PR 78 merges. Re-measure the fast suite and the exhaustive tier on main with the integer sweep in place: PR 80 raised the fast-tier budget to 2,700 s on a 1,791 s measurement and the exhaustive tier to 14,400 s on a 4,866 s one, both of the Fraction sweep; the code lane measured the n = 12 and n = 20 exact decisions at 25.5 s and 28.4 s, and 2,700 s sits above CI's 1,800 s. Drop both numbers. Port only the _push_test_step budget_seconds line, at 1,800, which is the fix D-432 already prescribes; close D-432.
