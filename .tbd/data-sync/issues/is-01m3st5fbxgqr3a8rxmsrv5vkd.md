---
type: is
id: is-01m3st5fbxgqr3a8rxmsrv5vkd
title: Rebaseline checks tier from two complete PR250 readings after 54-step expansion
kind: task
status: closed
priority: 2
version: 4
labels: []
dependencies: []
created_at: 2026-09-30T18:45:23.962Z
updated_at: 2026-09-30T18:54:07.148Z
closed_at: 2026-09-30T18:54:07.146Z
close_reason: Measured record 114.34 s from two complete PR250 attempts was merged at 3687d9cba3033d6fdd5942150566b5fca4846c5c. Final PR250 head 461b0f5d5 passed all required checks; checks tier passed 54/85 in 84.20 s against unchanged 140 s ceiling. Old PR185 record and both budget-only failures remain attributed in gate-budgets.yaml.
resolution: null
duplicate_of: null
---
PR250 run 36758687712 at 150f8b0dd passed all 54 of 85 selected checks on both hosted attempts, but walls 113.94s and 114.74s failed the inherited 75.67s × 1.5 relative band. Compare with PR185 historical 50 of 80 selection, attribute step/corpus growth, update the measured-cost record only, preserve 140s absolute ceiling and relative policy, and retain both budget-only failures. Validate the register with focused controls.

## Notes

Implemented and pushed 461b0f5d5 on codex/rectangle-frontier-admission. PR250 run 36758687712 at 150f8b0dd supplied complete checks readings 113.94 s (attempt 1/job 110035367595) and 114.74 s (attempt 2/job 110037623536), 54/85 steps each passing; only inherited relative cost band failed. New geometric-mean record 114.34 s, attributed to 50→54 selected checks and measured step growth; previous75.67 retained in history. Absolute140 s ceiling and1.5× relative policy unchanged. Focused budget/log-parser tests65 passed, check_gate_budgets passed, diff-check clean. Await hosted verification of new head before closing.
