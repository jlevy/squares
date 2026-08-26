---
type: is
id: is-01m0ypc5cd4z6ktb1vejj1td3n
title: "W7: deterministic chunk partitions and contact-assembly grammar"
kind: feature
status: in_progress
priority: 1
version: 16
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-26-overnight-constructive-enumeration.md
labels: []
dependencies: []
child_order_hints:
  - is-01m0zt27jnvzpg665ds23j4qw9
created_at: 2026-08-26T09:28:15.500Z
updated_at: 2026-08-26T23:19:46.234Z
---
BC-019. The bounded lattice splitter now evaluates every allowed exact free-square count F=0,1,2 before classification, prefers a registered-budget certificate when one exists, emits canonical certificates, and types unresolved caps. Calibration result: all 64 grids and 3/36 non-grid cases fit the narrow six-chunk/two-free budget; 2 non-grid cases are conclusively outside that budget, 23 have no partition in the registered universe, and 8 are search-capped and indeterminate. n=26 is established at F=2,C=6. The inspected n=1..100 corpus remains calibration-only; no H-044 verdict. PR 45 review corrections are implemented in a draft candidate, but strict validation and fresh cross-platform CI are still required before merge readiness.

## Notes

2026-08-26 session-018 completed its fixed four-hour checkpoint with R1-R5 and the standard experiment-loop guidance implemented. Focused tests, schema/generator checks, Ruff, BasedPyright, and independent audits pass. Strict was not admitted before the frozen 15:36 cutoff because free space was below 4 GiB; capacity recovered during finalization. Keep PR 45 draft and all merge-readiness findings open until a fresh bounded continuation produces strict plus Linux/macOS receipts.
