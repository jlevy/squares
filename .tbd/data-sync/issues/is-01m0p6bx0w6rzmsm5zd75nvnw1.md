---
type: is
id: is-01m0p6bx0w6rzmsm5zd75nvnw1
title: "PR #5 review F-2: exp-001 archive cannot regenerate its configurations"
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m0p6bwcyve6zdv41ezr08e3g
created_at: 2026-08-23T02:14:34.267Z
updated_at: 2026-08-23T02:14:34.267Z
---
Three holes: run_baseline.sh filtered output to summary lines, discarding the per-chain records that carry x/y/t and overlap; checked_by claims an overlap guard not auditable from the archive; engine_commit d6a1057 is unreachable after the rebase. Together these break invariants 9 and 10 and the rng.rs promise that a configuration can be regenerated from its artifact.
