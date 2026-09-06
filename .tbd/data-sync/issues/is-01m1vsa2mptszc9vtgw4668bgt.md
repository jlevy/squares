---
type: is
id: is-01m1vsa2mptszc9vtgw4668bgt
title: Remove needless hashes from pending research handoffs
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
hold: null
hold_until: null
created_at: 2026-09-06T16:37:31.413Z
updated_at: 2026-09-06T16:45:16.717Z
started_at: 2026-09-06T16:37:53.236Z
---
Apply tbd general-coding-rules Cryptographic Hash Checks and development.md Hashes and Repository-Owned Artifacts to pending work. Use Git revision plus path for trusted repository-owned artifacts. Preserve hashes only for named trust boundaries such as independently checked downloaded sources or portable proof certificates. Remove duplicate prose manifests and same-process save/read checks without rewriting frozen historical evidence or proof contracts.

## Notes

Read tbd general-coding-rules Cryptographic Hash Checks and development.md Hashes and Repository-Owned Artifacts. Added OR-16 and generated AGENTS summary; current handoff supersedes blanket per-file SHA requirements. Removed pending coordinator/fractional/closure output checksum manifests and BC243 local-source hash. New BC241 checker uses Git revision+path and full content/semantic comparisons, while frozen legacy scientific inputs and replay receipts are preserved. Final validation and publication pending.
