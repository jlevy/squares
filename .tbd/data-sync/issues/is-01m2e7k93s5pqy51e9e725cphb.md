---
type: is
id: is-01m2e7k93s5pqy51e9e725cphb
title: Pack best changes with step batching
kind: bug
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
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T20:33:32.791Z
updated_at: 2026-09-13T21:03:10.243Z
---
The live Pack optimizer can record a different best arrangement when the same fixed-seed steps are grouped into different UI batches. Preserve one best-admission decision per simulation step, independent of render/yield chunk size. Acceptance: fixed seed/config and equal total steps produce identical retained best pose, side, validation and receipt across multiple batch sizes and browser/headless execution; cancellation and restart cannot publish a stale best.

## Notes

2026-09-13 checkpoint: fixed observation cadence and batch-invariant retained-best Node control implemented in PR #160. Keep open until browser/headless acceptance on pinned commit and review disposition.
