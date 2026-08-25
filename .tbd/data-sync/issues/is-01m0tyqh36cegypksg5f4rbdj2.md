---
type: is
id: is-01m0tyqh36cegypksg5f4rbdj2
title: Remove redundant source hashes and document the trust-boundary test
kind: task
status: in_progress
priority: 1
version: 6
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
delegate: codex@spud10
labels:
  - packing
  - cleanup
dependencies: []
parent_id: is-01m0typjn7s866m042zsemybj6
hold: null
hold_until: null
created_at: 2026-08-24T22:37:18.821Z
updated_at: 2026-08-25T02:58:06.146Z
started_at: 2026-08-25T02:21:37.342Z
---
Classify digest use site by site. Remove reader-facing SHA restatements and checks that merely repeat the identity of first-party sources already retained in Git. Prefer parsing retained source over embedding a second transcription. Where a checker still embeds hand-transcribed tuples, retain or replace its expected-source digest only as a documented mechanical staleness guard that detects corrected archive bytes no longer matching the embedded data. No hash supplies mathematical evidence.
