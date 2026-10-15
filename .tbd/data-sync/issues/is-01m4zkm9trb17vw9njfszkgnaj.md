---
type: is
id: is-01m4zkm9trb17vw9njfszkgnaj
title: "J2: cover the required-checkpoint workflow roster and recovery contracts"
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zhkc4z66ywdsxw20sjcmg7
hold: null
hold_until: null
created_at: 2026-10-15T11:02:18.199Z
updated_at: 2026-10-15T11:15:09.430Z
started_at: 2026-10-15T11:15:09.429Z
---
Senior review J2: proposed required producer and packing-required roster change omits existing contracts in test_module_boundaries.py, test_validation_cli.py and test_rerun_starved.py, including expected 3-of-10 infrastructure classification. Extend the durable workflow-consumption and supported-rerun regression tests to the new required obligation, preserving negative tests for absent/skipped/failed receipts. Run the affected existing modules before any activation; do not merely change a count without proving the new consumer edge.
