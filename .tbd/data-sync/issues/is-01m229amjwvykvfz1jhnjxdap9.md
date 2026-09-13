---
type: is
id: is-01m229amjwvykvfz1jhnjxdap9
title: Add restart, a best-known start, and a re-randomising random to the workbench
kind: task
status: open
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - packing
  - workbench-roadmap
  - workbench-phase-3
dependencies:
  - type: blocks
    target: is-01m28p88qyq83eek30pja3np54
parent_id: is-01m2b7n9tyq13n0zw4tkq4rfss
created_at: 2026-09-09T05:12:53.595Z
updated_at: 2026-09-13T05:43:47.984Z
---
Phase 3 package start/transport controls. Preserve existing restart and best-known behavior after checking the refreshed source; finish effective seed display/editing and a new random draw on request. Restart reproduces the current initial state/configuration, reset restores defaults, and random selects and records a new seed. Known-best start is optional and reports provenance/drift. Acceptance: shared Pack API receives effective configuration, restart is exact, repeatable random seeds replay, and controls do not inherit Animate transition semantics. Location: packages/workbench.
