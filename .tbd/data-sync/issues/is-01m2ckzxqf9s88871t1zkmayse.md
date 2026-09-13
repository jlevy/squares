---
type: is
id: is-01m2ckzxqf9s88871t1zkmayse
title: Make Pack independent of atlas transition pairs
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-phase-4
  - workbench-roadmap
dependencies:
  - type: blocks
    target: is-01m2cm03rtrjcg98ejb9y56jn6
parent_id: is-01m2b7n9tyq13n0zw4tkq4rfss
created_at: 2026-09-13T05:31:41.166Z
updated_at: 2026-09-13T05:43:48.754Z
---
Use the packaged run API for one chosen n without requiring an n-1 to n atlas pair. Provide generic grid/random/given starts, optional known-best start when a record exists, all n active squares at rest, direct manipulation, explicit Run/Pause/Restart/Reset/Resolve semantics, visible editable seed and run receipt import/export. Reject unsupported n with measured resource limits visible in UI. Reuse think-8cti mode separation and think-rdee start controls. Acceptance: n with and without a catalogue entry works; same seed/config replays; raw and repaired geometry/score stay paired; cancelled/restarted runs cannot publish stale state.
