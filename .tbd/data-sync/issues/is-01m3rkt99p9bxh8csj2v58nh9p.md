---
type: is
id: is-01m3rkt99p9bxh8csj2v58nh9p
title: Measure PR gate sensitivity to proof-corpus growth and hosted load
kind: task
status: closed
priority: 2
version: 22
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3ra1hjvn4bdh3h13aggqgvb
child_order_hints:
  - is-01m3s98kgj0s9pg4ybk685nc7t
  - is-01m3sefkn12n7fzy6gx1ss13nh
created_at: 2026-09-30T07:35:11.413Z
updated_at: 2026-09-30T16:08:32.038Z
closed_at: 2026-09-30T16:08:32.035Z
close_reason: Measured shard capacity and hosted runner variability are addressed without weakening coverage or raising limits. Three-way assignment and explicit observed timing bands pass all required checks at 180326e81. Remaining historical cost-accounting work is separately owned by think-wvwx.
resolution: null
duplicate_of: null
---
Hosted run36684000513 at6c1c713af passed all logical checks but failed cost controls: checks127.39s against75.67s baseline (1.68x), suiteB153.34s and two reachable-graph tests12.97/12.93s above12s. Previous4c826f8 run36683159180 passed. Separate runner variance from repository corpus/graph growth using existing hosted receipts; improve measured hotspot without weakening thresholds or delaying T060 geometry. One same-head failed-job replay is authorized as diagnosis; no broad local suites.

## Notes

At b6c97667b run36735084578, all suite-B 4408 behavioral tests passed but wall165.06s exceeded154s (1.60x102.91 baseline); A passed. The live wall fix worked and reported conservative265s, then correctly refused the failed prerequisite. Sol compares multiple same-cohort shard profiles to select a durable repartition or extra parallel shard without weakening coverage or budgets. This is integration cost debt, not a mathematical gap.
