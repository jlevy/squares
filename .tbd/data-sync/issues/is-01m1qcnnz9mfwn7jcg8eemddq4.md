---
type: is
id: is-01m1qcnnz9mfwn7jcg8eemddq4
title: "test_rung_figures.py: port the cross-record contract, derive every literal from the artifact"
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:39:42.441Z
updated_at: 2026-09-04T23:39:42.441Z
---
PR 80 adds 193 lines to test_rung_figures.py. The cross-record contract (a result's figures must match its own artifacts, D-470's shape) is right; the literals are not: six reach-table rows, 'about 6.9 times tighter', 'about 1.77 times', '2097 atoms took 4866 s', 'Eight rungs are retained', three exact_form == '459/100' -- all hand-written in a test that already opens the artifact it could derive them from. As written, four new instances of D-439. Port the mechanism; compute the figures from the loaded artifacts.
