---
type: is
id: is-01m2dvhzr8f87mgtghjv28rn55
title: Resolve reports its termination truthfully at tolerance zero and on cancellation
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m2b7na7psnnn1j62g1yjdtta
created_at: 2026-09-13T17:03:07.527Z
updated_at: 2026-09-13T17:03:07.527Z
---
Review 2026-09-13 of src/simulation/resolve.ts (committed 12b4ed6c): (1) at tolerance 0, 992 of 2000 perturbed inputs report stalled or budget-exhausted although the repaired output passes the shared validity check, because resolve.ts ~168-174 demands exactly zero overlap including rounding from the lower-left fit (pack-runner allows tolerance 0); (2) on cancellation resolve.ts ~237-248 returns the raw assessment as repaired and resolve.test.ts ~145 asserts it, contradicting think-nals ('a repaired score never labels a raw frame'); (3) Search receipts do not carry the repair termination reason. Also: probes/bench-annealing.ts ~133 keeps its own resolveOverlaps, and the page does not consume the shared resolver yet.
