---
type: is
id: is-01m1qcnnz9mfwn7jcg8eemddq4
title: "test_rung_figures.py: port the cross-record contract, derive every literal from the artifact"
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:39:42.441Z
updated_at: 2026-09-05T01:45:53.879Z
closed_at: 2026-09-05T01:45:53.879Z
close_reason: Ported/delivered (cherry-picked onto claude/port-pr80-findings from the sub-agent worktree commits 9618ba31, aac1bf57, 4c2053f9, 7356f0e8, 2e1a0c28; the last renumbered to D-452 and hand-merged with the concurrent synopsis check).
resolution: null
duplicate_of: null
---
PR 80 adds 193 lines to test_rung_figures.py. The cross-record contract (a result's figures must match its own artifacts, D-470's shape) is right; the literals are not: six reach-table rows, 'about 6.9 times tighter', 'about 1.77 times', '2097 atoms took 4866 s', 'Eight rungs are retained', three exact_form == '459/100' -- all hand-written in a test that already opens the artifact it could derive them from. As written, four new instances of D-439. Port the mechanism; compute the figures from the loaded artifacts.
