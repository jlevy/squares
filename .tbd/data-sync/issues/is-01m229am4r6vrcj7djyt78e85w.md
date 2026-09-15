---
type: is
id: is-01m229am4r6vrcj7djyt78e85w
title: Split Pack and Animate cleanly in the workbench prototype
kind: task
status: open
priority: 2
version: 7
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
updated_at: 2026-09-15T03:33:24.491Z
---
Phase 3 app composition within packages/workbench. Preserve and verify already delivered prototype mode separation, then wire Pack and Animate to the extracted kernel, timeline and data contracts. Pack shows all active squares at rest and only run settings; Animate owns range, correspondence, phase timing and presentation settings. Switching modes preserves intended mode-local state and cannot carry a stale result or attach a repaired score to raw geometry. Acceptance includes both mode transitions and a fixed-seed replay. think-uhqw owns the subsequent arbitrary-n workflow; do not duplicate it here.

## Notes

2026-09-14, lane D-page (PR #160 review D48, think-i4jm): the retained controller's mode, range and run invariants now live in enterAspect, keepStageInRange and endRun (fa53f158), and the capture baseline enters Animate first (fc8079df, think-z9gm). The wider Pack/Animate split this bead describes is not closed by that.
