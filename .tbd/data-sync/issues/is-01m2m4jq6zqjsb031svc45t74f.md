---
type: is
id: is-01m2m4jq6zqjsb031svc45t74f
title: "PR #175 lane L5: typeof is the whole function test in inspect-probes.mjs"
kind: bug
status: open
priority: 3
version: 1
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:36:15.325Z
updated_at: 2026-09-16T03:36:15.325Z
---
A class expression passes the checker and fails in the page with 'Class constructor cannot be invoked without new'. The criterion is a type tag rather than callability. Found by the review lane; not in the published review.
