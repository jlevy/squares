---
type: is
id: is-01m2b7nakccj4tf1tgs4k86nar
title: Search as a third mode, with its own controls and readout
kind: feature
status: open
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-5
dependencies:
  - type: blocks
    target: is-01m229c25xgrtk9hh5nd1brnxn
parent_id: is-01m2b7n9tyq13n0zw4tkq4rfss
created_at: 2026-09-12T16:36:56.555Z
updated_at: 2026-09-13T21:08:29.034Z
---
Phase 5 after the clean Pack/Animate package and reusable scheduler: add Search as a tab over the same single-run API as Pack. Expose n/start/configuration, trial/seed/work budgets and parameter cells. Show attempted/completed/accepted/rejected/interrupted counts, valid-run rate, absolute/relative excess, labelled prefix observations and disjoint-block distributions, and the best valid arrangement with its receipt. Handle empty populations and zero grid-to-reference gap. Progress and cancellation remain responsive. Acceptance: identical Pack/Search/headless receipts for same seed/config; no invalid ranking; saved manifests reproduce aggregates. Prior overnight numerical tables remain historical until evidence repair verifies them. Calibrate is a preset, not a fourth engine/tab.

## Notes

2026-09-13 PR #160 checkpoint: experimental Search tab runs bounded grid/random seeded trials and can export/import/resume a ledger; focused browser check passes. It is not the released Search outcome. Best-pose views, cohort distributions, calibration/held-out controls, complete replay parity and partial-failure behavior remain.
