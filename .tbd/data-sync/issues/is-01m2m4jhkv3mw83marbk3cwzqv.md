---
type: is
id: is-01m2m4jhkv3mw83marbk3cwzqv
title: "PR #175 lane L2: inspect-probes.mjs runs probe bodies with no timeout"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:36:09.592Z
updated_at: 2026-09-16T03:36:09.592Z
---
packing/devtools/node/inspect-probes.mjs:23. A probe whose top level busy-loops hangs check_probes forever. Pass a timeout to runInContext. Found by the review lane; not in the published review.
