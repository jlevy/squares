---
type: is
id: is-01m2ymzy4tz2n47g8ttd8qspv0
title: "PR 200: restack, repair evidence and queue ownership, regenerate its atlas"
kind: task
status: open
priority: 1
version: 3
labels:
  - correctness
dependencies:
  - type: blocks
    target: is-01m2yn0dnnwcy69jb14mzznmga
parent_id: is-01m2ymyd4zef0ckcx8gvq3p5dx
created_at: 2026-09-20T05:35:29.945Z
updated_at: 2026-09-20T05:43:47.481Z
---
Restack PR200 on the repaired PR199 head, preserving its incremental work. Port its owning-layer PR202 corrections: keep unconverged and stalled outcomes unresolved; distinguish numerical-f64 experiment subjects from exact certificate decisions; restore structured T027 produced_by; reconcile the n<=100 census to 35 proved/65 open and direction counts; acquire output leases before dispatch, preserve ownership through orphaned generator lifetime, and exercise competing walkers and exceptions. Use the permitted project interpreter in queue tests. Regenerate this layer’s atlas exports against T028 at s(18)>=4.675, not the later 4.679 value; port the cheap visible-label drift guard where applicable. Preserve T027/T028 certificates and historical decisions. Done when incremental review approves all applicable findings and current head/repaired-base have a complete passing fast+deferred checkpoint, including the slow composite test and canonical atlas rebuild. Save exact run/head/base identities and update PR readiness. Hand the new head to PR201. Do not merge.
