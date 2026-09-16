---
type: is
id: is-01m2m4jkpetf189mh8trf866gw
title: "PR #175 lane L3: add_init_script(path=...) and read_text() to a non-.js file are unconstrained"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:36:11.718Z
updated_at: 2026-09-16T03:36:11.718Z
---
check_no_embedded_js.py:75. A .txt holding JavaScript loaded with path= or read_text() passes. Constrain the blessed indirection to a .js or .ts path under a probe tree. Found by the review lane; not in the published review.
