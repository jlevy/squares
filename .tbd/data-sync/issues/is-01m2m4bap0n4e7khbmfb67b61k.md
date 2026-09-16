---
type: is
id: is-01m2m4bap0n4e7khbmfb67b61k
title: "PR #175 review R5: add_script_tag(content=...) is not a script argument"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:32:13.119Z
updated_at: 2026-09-16T03:32:13.119Z
---
check_no_embedded_js.py:76 (SCRIPT_ARGUMENT). Fix: add add_script_tag with its content keyword and no positional index. (PR #175, review 5218208204)
