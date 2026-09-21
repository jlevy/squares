---
type: is
id: is-01m31gq90jbqgvq1gxgxhwpcq1
title: boxes_are_distinct justification is wrong under one spare
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:35.153Z
updated_at: 2026-09-21T08:18:35.153Z
---
PR 205 re-review, new Low introduced by aed8638d - the same defect shape as F6, which that commit fixed. m6_model.py:620-630 and the module docstring at :42-48 state 'A box of a packing of this configuration holds one point of each colour, so one box cannot hold both.' Under one spare that is exactly what a box may do: with 32 boxes and 33 unavoidable points per colour, 77 of the 110 structures per colour are doubles. The predicate is sound anyway because _charge (:346-349) returns uncovered/frozen with rect is None, so a counted box's own end point is provably singly covered. Honest sentence: 'a counted box's own end point is never frozen, so it is singly covered.' Verified unreachable: the strict double-aware predicate agreed on all 145,456 evaluations.
