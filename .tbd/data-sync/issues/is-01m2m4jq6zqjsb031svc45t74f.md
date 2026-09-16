---
type: is
id: is-01m2m4jq6zqjsb031svc45t74f
title: "PR #175 lane L5: typeof is the whole function test in inspect-probes.mjs"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:36:15.325Z
updated_at: 2026-09-16T04:10:14.084Z
closed_at: 2026-09-16T04:10:14.084Z
close_reason: "Fixed on PR #175 in commit 0ab75b7c, each with a check watched failing on the pre-fix source first."
resolution: null
duplicate_of: null
---
A class expression passes the checker and fails in the page with 'Class constructor cannot be invoked without new'. The criterion is a type tag rather than callability. Found by the review lane; not in the published review.
