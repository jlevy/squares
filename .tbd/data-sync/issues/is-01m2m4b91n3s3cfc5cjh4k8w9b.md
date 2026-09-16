---
type: is
id: is-01m2m4b91n3s3cfc5cjh4k8w9b
title: "PR #175 review R3: rule 1 accepts every unclassifiable direct argument"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:32:11.443Z
updated_at: 2026-09-16T03:32:11.443Z
---
check_no_embedded_js.py:356-383 (classify, _classify_call). Path().read_text(), open().read(), .lower(), subscripts, class attributes, parameter defaults, tuple-unpacked names, *args and **kwargs all pass. Fix: default-deny; accept loader calls, names bound only to loader values, parameters, IfExp of those. (PR #175, review 5218208204)
