---
type: is
id: is-01m1wb5xeb8qgz52gchdv5ddr3
title: Preserve workflow evidence in negative-control snapshots
kind: task
status: closed
priority: 2
version: 3
spec_path: packing/campaign/agendas/agenda-024-post-381-24h-portfolio.md
labels: []
dependencies: []
parent_id: is-01m1w140k75zvvqpvj55e8k9my
created_at: 2026-09-06T21:49:49.386Z
updated_at: 2026-09-06T22:06:47.710Z
closed_at: 2026-09-06T22:06:47.709Z
close_reason: Reference-only workflow snapshot correction and clean-baseline/mutation regressions retained with H105 prospective checkpoint.16tests pass8.32s wall7.65CPU, one slow deselected; root source review and31recordchecks passed.
resolution: null
duplicate_of: null
---
Read-only diagnosis think-h264 found worker snapshots omit .github/workflows/deep-gate.yml and branch-mergeability.yml even though frozen SYNOPSIS links to them. This is separate from the empty environment cause of67 failed controls. Narrow proposed follow-up: include referenced workflow evidence in ROOT_DOCUMENTS and add a clean-snapshot link regression in run_negative_controls.py/test_negative_controls.py. Do not relax expected mutation outcomes. Supporting fix stays integratedPR101 if selected; currently unallocated.
