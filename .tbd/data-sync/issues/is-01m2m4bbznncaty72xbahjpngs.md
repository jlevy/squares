---
type: is
id: is-01m2m4bbznncaty72xbahjpngs
title: "PR #175 review R7: rule 3 accepts a script body spliced from a name-bound literal"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:32:14.451Z
updated_at: 2026-09-16T03:32:14.451Z
---
check_no_embedded_js.py:433 (_string_rule). Fix: in text(), resolve a Name whose every binding is text before applying rule 3. (PR #175, review 5218208204)
