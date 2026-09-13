---
type: is
id: is-01m229am4r6vrcj7djyt78e85w
title: Split Pack and Animate cleanly in the workbench prototype
kind: task
status: open
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - packing
  - workbench-roadmap
  - workbench-phase-3
dependencies:
  - type: blocks
    target: is-01m28p88qyq83eek30pja3np54
  - type: blocks
    target: is-01m291gkje2c7x07x2ah4fdpxn
parent_id: is-01m2b7n9tyq13n0zw4tkq4rfss
created_at: 2026-09-09T05:12:53.143Z
updated_at: 2026-09-13T05:43:47.957Z
---
Phase 3 app composition within packages/workbench. Preserve and verify already delivered prototype mode separation, then wire Pack and Animate to the extracted kernel, timeline and data contracts. Pack shows all active squares at rest and only run settings; Animate owns range, correspondence, phase timing and presentation settings. Switching modes preserves intended mode-local state and cannot carry a stale result or attach a repaired score to raw geometry. Acceptance includes both mode transitions and a fixed-seed replay. think-uhqw owns the subsequent arbitrary-n workflow; do not duplicate it here.
