---
type: is
id: is-01m2m66z2th383fhep5zh67yfe
title: CI proves the two quick shards partition the lane, not each shard alone
kind: task
status: deferred
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4aptpzqgmmhqxgxz3vba5
created_at: 2026-09-16T04:04:47.316Z
updated_at: 2026-09-16T05:10:31.429Z
---
PR #175 review, non-blocking suggestion: the two shards compute their partition independently from their own collection. Both jobs run the same commit on the same image, so it holds today, but nothing in CI proves that A union B is the whole quick lane and A intersect B is empty across the two runs. Each shard job could upload its module list and packing-required could check the union and the disjointness. Deferred from #175; it belongs in the workflow, not in the guard.

## Notes

Deferred from PR #175: both hosted shard jobs run the same exact commit/image and the stable packing-required context requires both. Cross-job union/disjointness artifacts would strengthen the proof but do not correct a present coverage defect. Revisit as CI-hardening work after the stack lands.
