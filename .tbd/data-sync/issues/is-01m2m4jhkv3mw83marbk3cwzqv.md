---
type: is
id: is-01m2m4jhkv3mw83marbk3cwzqv
title: "PR #175 lane L2: inspect-probes.mjs runs probe bodies with no timeout"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:36:09.592Z
updated_at: 2026-09-16T04:10:14.051Z
closed_at: 2026-09-16T04:10:14.051Z
close_reason: "Fixed on PR #175 in commit 0ab75b7c, each with a check watched failing on the pre-fix source first."
resolution: null
duplicate_of: null
---
packing/devtools/node/inspect-probes.mjs:23. A probe whose top level busy-loops hangs check_probes forever. Pass a timeout to runInContext. Found by the review lane; not in the published review.
