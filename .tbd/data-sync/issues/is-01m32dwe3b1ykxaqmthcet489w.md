---
type: is
id: is-01m32dwe3b1ykxaqmthcet489w
title: boxes_are_distinct is sound but its stated reason is false (PR 205 new Low)
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m32dvmtc77znp14556p7c5w2
created_at: 2026-09-21T16:48:12.907Z
updated_at: 2026-09-21T16:48:12.907Z
---
m6_model.py:620-630 and the module docstring at :42-48 say 'A box of a packing of this configuration holds one point of each colour', which under one spare is exactly what a box may do -- 77 of 110 structures per colour are doubles. The predicate is sound for a different reason: _charge returns uncovered/frozen with rect None, so a counted box's own end point is provably singly covered. Same defect shape as F6, which the same commit fixed. Documentation, not soundness: a strict double-aware variant agreed on all 145,456 evaluations.
