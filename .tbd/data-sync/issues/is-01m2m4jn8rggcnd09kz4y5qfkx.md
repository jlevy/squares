---
type: is
id: is-01m2m4jn8rggcnd09kz4y5qfkx
title: "PR #175 lane L4: Node-only probes are unsupportable and used is forgeable"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:36:13.330Z
updated_at: 2026-09-16T03:36:13.330Z
---
check_probes.callers() collects only .py, so a probe exercised by a .mjs test reads unused; and a dead constant or a docstring counts a probe used. Found by the review lane; not in the published review.
