---
type: is
id: is-01m0r3zv2hh2jj64rb8mhqbtre
title: Measure terminal flatness and connectivity before defining basin identity
kind: bug
status: in_progress
priority: 0
version: 33
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-correctness
dependencies:
  - type: blocks
    target: is-01m0pw86qg81x5qnjvzge42f4v
  - type: blocks
    target: is-01m0pw8698kc2bqm7d7fy0xydy
  - type: blocks
    target: is-01m0p4asxdaenzfkx53j4vh6qs
  - type: blocks
    target: is-01m0qxpb7634zbzt638d239jks
  - type: blocks
    target: is-01m0r50mrppgcvsp2ewrac0x6z
  - type: blocks
    target: is-01m0snvvpwxt2z0efp3r89scxk
parent_id: is-01m0p49s01h862tq6wp0dd085c
child_order_hints:
  - is-01m0t4phe1905yy2jk7czp1391
  - is-01m0tkxd8xsmw435t9f8srm6sz
  - is-01m0tn3kqe19evm1r40wgnpb61
  - is-01m0vyhtzd0j8gnfwm5k040ff1
created_at: 2026-08-23T20:11:30.757Z
updated_at: 2026-08-26T02:47:59.579Z
---
D-034, blocking the census. Exact evidence: the n=3 side-2 sliding family is a connected positive-dimensional terminal set that one contact certificate and many geometric keys split into quantum-dependent rows. The n=5 golden adds an unresolved pair: equal side, short form, contact certificate, angle signature and contact count but different geometry. Those facts do not prove the n=5 rows are connected or establish a five-dimensional family; raw constraint counting is not a rank certificate. Acceptance: archive both n=5 poses and their active cells; compute the fixed-cell optimal-face rank/nullity from the active LP matrix and objective; compute the full pose/angle active-constraint Jacobian; continue every null direction with independent validity checks; test whether the two endpoints are path-connected across cell/contact strata; report certified dimension or unresolved bounds; and feed the evidence to think-0yo9 rather than choosing identity from side/contact hashes.

## Notes

Full finalization checkpoint 3629bf4 pushed on origin/codex/packing-4h-research-loop-2026-08-25. The full 32-step packing-validate gate passed in 437.71s (119 behavioral tests, 62 negative controls, exact replays, Rust, provenance, schemas, ledger, synopsis). Session-016 remains in finalization-only state until 20:08:08-07:00; no target, JSON, exp045 artifact, or implementation has opened.
