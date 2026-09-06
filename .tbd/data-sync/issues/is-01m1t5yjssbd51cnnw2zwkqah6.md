---
type: is
id: is-01m1t5yjssbd51cnnw2zwkqah6
title: Restore PR 89 CI and close the stabilization tree
kind: task
status: open
priority: 1
version: 6
labels:
  - ci
  - stabilization
dependencies: []
parent_id: is-01m1t5xm3xv343zpxen49r7m5g
child_order_hints:
  - is-01m1t71b4k2x0fjcyfb8qq2h6r
  - is-01m1t71bf6rqbsd14afyvp2b7y
  - is-01m1t71bsncn7adg02er2hyk6d
  - is-01m1t71c4hyfw28d5nc5m6jv6b
  - is-01m1t7f9tt6fm2vmbvbsrjm19p
created_at: 2026-09-06T01:39:57.368Z
updated_at: 2026-09-06T02:06:33.805Z
---
Run the repository's documented edit, push, and hosted CI gates on the reconciled branch. Diagnose every failure to its exact owner; fix in-scope regressions, preserve truthful active-session state, push coherent commits, wait for the final required-check summary, then close and sync the completed stabilization beads with evidence.
