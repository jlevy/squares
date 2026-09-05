---
type: is
id: is-01m1qcchmasjppsb50npxmkhbd
title: "Keep minimal_verify.py: pin its SHA-256 in one place the other copies read"
kind: task
status: open
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-04T23:34:43.081Z
updated_at: 2026-09-04T23:46:12.904Z
---
Keep minimal_verify.py: the code lane found it is not redundant with thirdparty/verify.py -- the package verifier is general-purpose, CPython-3.8 compatible and ships against the 19/5 rung; minimal_verify.py is pinned by SHA-256 to the retained 381/100 bytes, checks every declared field, and cross-checks the prefix-sum minimum against a direct summation at each direction's witness. What to trim: it shares about eighty percent of its algorithm with verify.py, and it is the seventh copy of one SHA-256 on the stack, of which two are recomputed. Pin the hash in one place that the others read.
