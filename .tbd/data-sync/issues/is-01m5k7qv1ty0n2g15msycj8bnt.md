---
type: is
id: is-01m5k7qv1ty0n2g15msycj8bnt
title: assess_frontier_rigidity prints a negative zero in slide directions, e.g. 'along (-0, 1)' (n-051, n-177, n-303)
kind: bug
status: open
priority: 2
version: 2
labels:
  - tooling
dependencies: []
created_at: 2026-10-23T01:59:19.866Z
updated_at: 2026-10-23T02:41:33.152Z
---
The rigidity scope text formats direction components with a sign on zero: n-051.md 'along (-0, 1)', n-177.md 'along (1, -0)', and #731's n-303.md 'along (-0, -1)'. Normalize -0.0 to 0 in the formatter and re-derive the affected blocks with --update (a records change; check_release_impact may need a no-change record).

## Notes

2026-10-23 02:45Z coord-intake-1021b: #731 review A4: the printed slide is rounded to nearest, so n-303.md says square 5 translates 0.220024 while the exact slide is 0.220023657159277; moving it by exactly 0.220024 overlaps square 41 (gap -3.16e-7). Round the printed slide down (toward the valid side), with the -0 fix, and re-derive the blocks.
