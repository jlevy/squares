---
type: is
id: is-01m3qygbtayj0vy2v8y2ajf8ps
title: "W5: keep mutation-worker inputs bounded as proof evidence grows"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/reviews/review-2026-09-29-validation-parallelism.md
labels: []
dependencies: []
parent_id: is-01m3p5wj25knm7rbx0g4a4tpvg
child_order_hints:
  - is-01m3qzn1k3708fhtrsw1mqdgvk
created_at: 2026-09-30T01:22:46.217Z
updated_at: 2026-09-30T01:51:01.936Z
closed_at: 2026-09-30T01:51:01.935Z
close_reason: Duplicate of existing think-t1lk; new evidence and ancestry-cost child think-9b01 consolidated there.
resolution: null
duplicate_of: null
---
Supporting efficiency follow-up, not a prerequisite for T-060 proof checks. The n11 source/receipt intake and necessary atlas regeneration repeatedly crossed the160MiB private mutation-worker snapshot cap; current scoped fix excludes only four proven historical non-input byproducts while preserving Git evidence and dependency copy-back. Measure worker bytes/copy time and identify a durable input-selection contract with explicit required dependencies and adequate measured growth margin, instead of successive file-by-file exclusions or an arbitrary cap increase. Preserve all unique research evidence, link checks, mutation semantics and adversarial copy-back tests. Run a bounded comparison on identical controls; do not run general slow repository suites or delay mathematical validation.
