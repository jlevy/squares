---
type: is
id: is-01m2m4jkpetf189mh8trf866gw
title: "PR #175 lane L3: add_init_script(path=...) and read_text() to a non-.js file are unconstrained"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:36:11.718Z
updated_at: 2026-09-16T04:10:14.074Z
closed_at: 2026-09-16T04:10:14.074Z
close_reason: "Fixed on PR #175 in commit 0ab75b7c, each with a check watched failing on the pre-fix source first."
resolution: null
duplicate_of: null
---
check_no_embedded_js.py:75. A .txt holding JavaScript loaded with path= or read_text() passes. Constrain the blessed indirection to a .js or .ts path under a probe tree. Found by the review lane; not in the published review.
