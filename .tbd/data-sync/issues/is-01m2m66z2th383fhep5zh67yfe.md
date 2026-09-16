---
type: is
id: is-01m2m66z2th383fhep5zh67yfe
title: CI proves the two quick shards partition the lane, not each shard alone
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T04:04:47.316Z
updated_at: 2026-09-16T04:04:47.316Z
---
PR #175 review, non-blocking suggestion: the two shards compute their partition independently from their own collection. Both jobs run the same commit on the same image, so it holds today, but nothing in CI proves that A union B is the whole quick lane and A intersect B is empty across the two runs. Each shard job could upload its module list and packing-required could check the union and the disjointness. Deferred from #175; it belongs in the workflow, not in the guard.
