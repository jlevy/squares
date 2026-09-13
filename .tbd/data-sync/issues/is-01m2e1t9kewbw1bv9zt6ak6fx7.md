---
type: is
id: is-01m2e1t9kewbw1bv9zt6ak6fx7
title: "R4: compare source closure against the current staged index"
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels: []
dependencies: []
parent_id: is-01m2dzxy2qg4x28a66x0gw3r0t
created_at: 2026-09-13T18:52:31.209Z
updated_at: 2026-09-13T18:52:31.209Z
---
Exact-head verifier review at 878e18d0 found source-closure accepts the stale execution tree while the current Git index stages a changed helper. Bind the candidate tree to the actual staged index before the evidence commit.
