---
type: is
id: is-01m2cv9cfmxer0nqaefywnmkbn
title: "PR #157 review DOC-06: the threshold-mutation explanation overclaims what budget detects"
kind: bug
status: open
priority: 3
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T07:39:11.219Z
updated_at: 2026-09-13T07:39:11.219Z
---
session-127 line 296 says a wrong threshold is caught by its budget. With seven tokens, thresholds four through seven all have budget one; the retained test checks the particular mutation 4->3, which changes the budget to two. Fix: describe that concrete mutation and retain threshold as an input checked for consistency through charges and placement lists.
