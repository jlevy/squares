---
type: is
id: is-01m2m4b6x0t593cq2zvvwnv09m
title: "PR #175 review R1: a bytes literal carries a signature-bearing script past both rules"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:32:09.247Z
updated_at: 2026-09-16T04:10:13.762Z
closed_at: 2026-09-16T04:10:13.759Z
close_reason: "Fixed on PR #175 in commit 0ab75b7c, each with a check watched failing on the pre-fix source first."
resolution: null
duplicate_of: null
---
check_no_embedded_js.py:301 (_text reads str only) and :324 (_method_result). page.evaluate(b"() => document.title".decode()) passes both rules. Fix: decode bytes in _text; treat a method call on a built/loader receiver as built. (PR #175, review 5218208204)
