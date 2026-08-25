---
type: is
id: is-01m0tyqh36cegypksg5f4rbdj2
title: Remove redundant source hashes and document the trust-boundary test
kind: task
status: closed
priority: 1
version: 10
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
updated_at: 2026-08-25T03:18:22.840Z
started_at: 2026-08-25T02:21:37.342Z
closed_at: 2026-08-25T03:02:48.727Z
close_reason: Repository-local integrity hashes are removed and the trust-boundary rule is documented in development.md. A cryptographic checksum is now reserved for an independently supplied value across a real trust boundary; internal goldens use Git diffs, complete comparisons, or semantic regeneration. Full 31-step validation passed in 99.43 seconds.
resolution: null
duplicate_of: null
---
Classify digest use site by site. Remove reader-facing SHA restatements and checks that merely repeat the identity of first-party sources already retained in Git. Prefer parsing retained source over embedding a second transcription. Where a checker still embeds hand-transcribed tuples, retain or replace its expected-source digest only as a documented mechanical staleness guard that detects corrected archive bytes no longer matching the embedded data. No hash supplies mathematical evidence.

## Notes

2026-08-24: Removed redundant SHA fields and checksum controls from first-party golden records, retained source fixtures, predecessor chains, and exact matrix records. Replaced them with Git-tracked paths and retrieval metadata, complete regenerated-result equality, direct structural comparison, and exact semantic replay. Trump branch deduplication uses complete exact tuple keys and recorded branch/selection coverage. Canonical basin keys and BasinEvent event IDs remain only for named deduplication and append-only identity roles. The final stack preserves PR 22 base f49b3c4 and its D-225 record; this stack's CI defects are D-226 through D-228, for 228 defects total. The exact combined stack passed all 31 packing-validate steps in 81.99 seconds with 289 Python files at the lint/type floor, 56 negative controls, and all 128 Trump branch certificates replayed.
