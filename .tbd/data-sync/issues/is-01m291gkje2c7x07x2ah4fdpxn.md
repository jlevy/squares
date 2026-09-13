---
type: is
id: is-01m291gkje2c7x07x2ah4fdpxn
title: "Make the physics optional: a direct animation between records"
kind: feature
status: open
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-3
dependencies:
  - type: blocks
    target: is-01m2cm03rtrjcg98ejb9y56jn6
  - type: blocks
    target: is-01m28p88qyq83eek30pja3np54
parent_id: is-01m2b7n9tyq13n0zw4tkq4rfss
created_at: 2026-09-11T20:11:01.581Z
updated_at: 2026-09-13T05:43:47.992Z
---
Phase 3/4 package Animate adapter: choose direct interpolation of retained endpoints or playback of a physically generated trace, with labels describing the actual source and guidance. Reuse think-ywj4 timeline and think-883t trace IO; the draw path does not run a solver. Acceptance: direct illustrations work with solver unavailable, physical traces retain run receipts, seek/capture preserve source and evidence labels, and guided landing cannot be presented as discovered packing. All implementation and tests live in packages/workbench.
