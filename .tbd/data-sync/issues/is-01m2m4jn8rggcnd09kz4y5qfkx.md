---
type: is
id: is-01m2m4jn8rggcnd09kz4y5qfkx
title: "PR #175 lane L4: Node-only probes are unsupportable and used is forgeable"
kind: bug
status: closed
priority: 2
version: 4
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:36:13.330Z
updated_at: 2026-09-16T05:10:37.835Z
closed_at: 2026-09-16T05:10:37.833Z
close_reason: Node-only probe callers are now supported; the separate dataflow-precision question is tracked as deferred think-13m7.
resolution: null
duplicate_of: null
---
check_probes.callers() collects only .py, so a probe exercised by a .mjs test reads unused; and a dead constant or a docstring counts a probe used. Found by the review lane; not in the published review.

## Notes

Resolved split: reconciled PR #175 head 0dfcd70b extends probe callers to tracked .mjs/.cjs files and adds a Node-only caller contract. The remaining dead-constant/docstring reachability question is intentionally separated into think-13m7 because it requires a dataflow pass and is not a merge blocker.
