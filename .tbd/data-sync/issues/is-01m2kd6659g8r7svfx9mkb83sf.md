---
type: is
id: is-01m2kd6659g8r7svfx9mkb83sf
title: Restore the PR quick suite to its declared feedback band
kind: task
status: in_progress
priority: 1
version: 3
delegate: Codex PR175 cost-fix sub-agent
labels:
  - efficiency
dependencies: []
parent_id: is-01m2k77cev2mj85dkb88nxedp8
created_at: 2026-09-15T20:47:27.395Z
updated_at: 2026-09-16T00:15:06.347Z
---
PR 175 passes all 6,096 quick tests but the single suite runner took 280.83s and 278.93s against the 275s ceiling. Preserve every test and timing diagnostic while splitting the quick suite into two explicit, independently budgeted jobs using deterministic whole-file sharding; prove the shards are complete, disjoint, stable, and aggregated by packing-required. Do not relax the existing unsplit budget or remove checks from CI.

## Notes

Rejected local scheduling-only variants: loadscope 318.54s and worksteal 323.69s versus 302.70s default. The reviewed design uses two explicit suite jobs with deterministic whole-file sharding, separately declared budgets, preserved xdist and duration guards, and packing-required aggregation; independent review requires union/disjointness and workflow-contract tests. A 2026-09-15 machine restart erased the uncommitted implementation worktree before commit or push. The exact PR head remained ef907d8c, recovery found no staged or committed sharding work, and reconstruction resumed from the durable design and audit record on a fresh exact-head worktree. The old aggregate --suite tier will be retired rather than preserved as a known-red third execution shape.
