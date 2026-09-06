---
type: is
id: is-01m1sp9zws6twqngzdsphwnbm7
title: Resume the retained 3.82 primal-dual state
kind: task
status: in_progress
priority: 1
version: 6
delegate: claude-code@spud10.local
labels:
  - research
dependencies: []
parent_id: is-01m1sp7k7txpwp2y4pbhen30jv
hold: null
hold_until: null
created_at: 2026-09-05T21:06:34.008Z
updated_at: 2026-09-06T05:54:48.863Z
started_at: 2026-09-06T03:21:56.559Z
---
BC-232: resume the retained 3.82 cutting state from its warm JSON with run_fractional_cutting --warm, not the incompatible NPZ column-generation checkpoint. Apply the fixed four-CPU-hour shrinkage rule. If the row-converged primal drops below 11, require a tested rationalize/freeze bridge before treating it as an exact certificate.

## Notes

T+2 leg 1 terminal, zero exit, no restart or leg 2. Four frozen outputs: state f91999b452bf89f49e2d4cda9827efbf57623a4196688b5feba0819bc7e851e2; log 431737c54034c97ed9fdd51bd2991852d793b96b56486df4cfe2c0e9b19f2e7c; summary d8c50db8770b12d43baa6d9e2c7384a52a0f250f8cee26b6a036c99b3cb3350e; family 4cfbdce5cb659d77d652c011854de74ddcad94c903eff30af07bbcb5d8d9cc3f. Runner seconds 6560.285289; 14 iterations; best exact lower endpoint iter10 21342289572/2055263195 = 10.384212408377214; only row-converged upper endpoint iter0 11.055616942909783. Family depth verifier failed solely total >=11, so no formulation closure or bound. Provisional bracket width ~0.671404535, ~41.5% narrower than pre-resume; frozen rule defers routing until the full four-CPU-hour budget, leaving 135 one-core minutes after landing. State has documented pre-add serialization limitation; summary/family authoritative. Exp-070 terminal record SHA-256 36d546ca6c00b042cd1751a491bb5d787db0987e8a26a41dfbdd404109b1ebda; remain in progress for leg 2.
