---
type: is
id: is-01m2kd6659g8r7svfx9mkb83sf
title: Restore the PR quick suite to its declared feedback band
kind: task
status: in_progress
priority: 1
version: 6
delegate: Codex PR175 cost-fix sub-agent
labels:
  - efficiency
dependencies: []
parent_id: is-01m2k77cev2mj85dkb88nxedp8
created_at: 2026-09-15T20:47:27.395Z
updated_at: 2026-09-16T02:13:42.450Z
---
PR 175 passes all 6,096 quick tests but the single suite runner took 280.83s and 278.93s against the 275s ceiling. Preserve every test and timing diagnostic while splitting the quick suite into two explicit, independently budgeted jobs using deterministic whole-file sharding; prove the shards are complete, disjoint, stable, and aggregated by packing-required. Do not relax the existing unsplit budget or remove checks from CI.

## Notes

Rejected local scheduling-only variants: loadscope 318.54s and worksteal 323.69s versus 302.70s default. The reviewed implementation replaces the red aggregate suite with two deterministic whole-module jobs; independent audits proved post-marker union/disjointness, workflow aggregation, unchanged coverage, and the unchanged 12s per-test guard. Recovery after the 2026-09-15 restart reconstructed the lost work and commit 02767281. A predecessor-hosted shard-B attempt exposed a borderline divide-and-concur quick test: 12.76s with research-scale overrides versus 10.97-11.36s before sharding. Commit dee68bc8 removes only those overrides and retains both beta cases, the 30-seed sweep, the same seed-3 solutions, and independent verification. Corrected exact-head run 35044761025 was green: shard A 151.11/149.97s, 3,050 passed plus 6 skipped each; shard B 133.13/107.34s, 3,055 passed each. Commit 3d8ef13c records geometric baselines 150.54s and 119.54s under unchanged 180s ceilings and updates the validation guide/spec to 6,111 selected tests. Locked records validation passed 32/78 steps in 61.66s; focused final set passed 128 tests; required pre-push validation passed 48/78 steps, including 6,249 behavioral tests with 9 skips, in 1,010.82s. Two independent final audits found no defect. Final exact-head CI is required before closing and propagating the stack.
