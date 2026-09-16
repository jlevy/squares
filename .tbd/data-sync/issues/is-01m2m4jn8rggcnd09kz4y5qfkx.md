---
type: is
id: is-01m2m4jn8rggcnd09kz4y5qfkx
title: "PR #175 lane L4: Node-only probes are unsupportable and used is forgeable"
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T03:36:13.330Z
updated_at: 2026-09-16T04:10:22.715Z
---
check_probes.callers() collects only .py, so a probe exercised by a .mjs test reads unused; and a dead constant or a docstring counts a probe used. Found by the review lane; not in the published review.

## Notes

Half fixed on PR #175 in commit 0ab75b7c: a probe a Node script beside the tree names is no longer read as dead ('check_probes.node_callers'), with a contract test. The second half -- 'used' being forgeable by a dead constant or a docstring -- is deferred to think-13m7 with the argument on the record: the literal search is deliberate (the module docstring: a name that reaches the loader through a tuple, a loop or a helper still counts), so tightening it needs a dataflow pass and would trade an unexploitable forgery for false dead-probe reports.
