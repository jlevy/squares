---
type: is
id: is-01m2m4bbznncaty72xbahjpngs
title: "PR #175 review R7: rule 3 accepts a script body spliced from a name-bound literal"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:32:14.451Z
updated_at: 2026-09-16T04:10:13.954Z
closed_at: 2026-09-16T04:10:13.954Z
close_reason: "Fixed on PR #175 in commit 0ab75b7c, each with a check watched failing on the pre-fix source first."
resolution: null
duplicate_of: null
---
check_no_embedded_js.py:433 (_string_rule). Fix: in text(), resolve a Name whose every binding is text before applying rule 3. (PR #175, review 5218208204)
