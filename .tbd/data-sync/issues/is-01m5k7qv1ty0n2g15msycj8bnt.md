---
type: is
id: is-01m5k7qv1ty0n2g15msycj8bnt
title: assess_frontier_rigidity prints a negative zero in slide directions, e.g. 'along (-0, 1)' (n-051, n-177, n-303)
kind: bug
status: open
priority: 3
version: 1
labels:
  - tooling
dependencies: []
created_at: 2026-10-23T01:59:19.866Z
updated_at: 2026-10-23T01:59:19.866Z
---
The rigidity scope text formats direction components with a sign on zero: n-051.md 'along (-0, 1)', n-177.md 'along (1, -0)', and #731's n-303.md 'along (-0, -1)'. Normalize -0.0 to 0 in the formatter and re-derive the affected blocks with --update (a records change; check_release_impact may need a no-change record).
