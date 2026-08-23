---
type: is
id: is-01m0p49s8z0nmtqagkbfw9mtpb
title: "quench: LP-in-cell refinement loop"
kind: task
status: closed
priority: 0
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies:
  - type: blocks
    target: is-01m0p49sjar1s9ga85vn3wyhj4
  - type: blocks
    target: is-01m0p4asaeypn1nn54frxj3cx9
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T01:38:27.742Z
updated_at: 2026-08-23T04:01:41.517Z
closed_at: 2026-08-23T04:01:41.516Z
close_reason: "Built as sqpack/quench.py: LP-in-cell + cell fixed point + class-bracketing angle search. Reaches the analytic optimum to 1e-15 at n=5 and n=10 (exp-007, exp-008)."
---
Registry H-002, the register's own top priority. Fix angles and each pair's separating axis, solve the cell LP for the exact cell optimum, alternate with local angle moves until termination at a genuine cell-optimum. The single-cell half is verified already (1056-constraint LP at Trump's angles reproduced s(11) to solver precision, centres to 9e-16); the loop is untested. Watch for cycling between cells and behaviour at cell boundaries. Test: polish annealer output at n=5,10,11 from perturbed starts against known algebraic values. Directly fixes exp-001's n=10 result, which found the right basin and stopped 4.19e-04 short.
