---
type: is
id: is-01m4b1ahjs14a68bbrgtxyt1gm
title: Refresh family and contact-shade censuses after SQUISH import
kind: task
status: in_progress
priority: 1
version: 3
delegate: codex@17e132e9b179
labels:
  - result-import
dependencies: []
parent_id: is-01m4ajdxfkfqyr1yj5d4wm5npt
hold: null
hold_until: null
created_at: 2026-10-07T11:17:35.448Z
updated_at: 2026-10-07T11:21:26.767Z
started_at: 2026-10-07T11:20:49.153Z
---
The full confirmation checkpoint at 9ce8ac8ea found a stale generated family census
after the eleven imported poses replaced the previous known-best witnesses. The
n107 shared-with-next diagnostic and n108 axis/grid classifications retain old
geometry. Diagnose and refresh both family and contact-shade censuses, including
all imported counts and affected preceding neighbors, on both import layers.

GPT-6.1 Sol prepares regeneration and verifies output scope; Astra independently
reviews classification semantics and invariance of the certified geometry, source
sides and receipts. Keep the ongoing full-run source frozen until it finishes.
After adoption, rerun affected census checks and the meaningful incremental gate.
Do not relax budgets, schemas, retention policies or integrity rules. Parent owns
blocked publication and the author reply.

## Notes

Claimed local engineering follow-up after read-only diagnosis of the frozen full
checkpoint at confirmation 9ce8ac8ea. Family --check failed because its retained
X049 census still describes earlier known-best geometry; n107 next-pair sharing
and n108 axis/angle diagnostics were the first reported differences. Companion
contact-shade --check did not run because the first command aborted its combined
step. Exact, translation, invalid-control, atlas, reader, and other completed
phases passed; the ongoing fast shards retain the four-core budget.

Both existing generators offer --update/--check and write one JSON each. Full324
regeneration is required: families reads direct poses, predecessor sides, next
pairs, all global L candidates/chains and every summary; contact shading reads
all witnesses/rendered SVGs and three rule summaries. Astra agrees that neighbor
and downstream L-child changes are expected derived metadata, not pose changes.
Schemas, tolerances, bounds and deciding code will remain unchanged.

Copied tracked tool/src context and manifest-referenced witnesses/SVGs to
/workspace/squares-401-census-candidates/reported/packing and confirmed/packing:
783 files and 66,042,769 bytes per side, staged in0.26s. Current candidate JSONs
are copies of OLD baselines. No regeneration/replay has started; documented
8.8/7.6s generators are deferred until the frozen full checkpoint ends to avoid
CPU contention. Preserve X049/H272 dated measurements/targets as historical;
any reader addition should state baseline versus live-file refresh provenance.

Await full-run completion, then generate candidates outside checkouts, compare
reported/confirmed outputs, verify certified fact/witness/receipt/pose invariance,
obtain Astra review, adopt only generated views/provenance note, and run affected
checks plus the meaningful incremental gate. Parent owns publication blocked by
HTTP403. Keep this follow-up open until outputs are integrated and checked.
