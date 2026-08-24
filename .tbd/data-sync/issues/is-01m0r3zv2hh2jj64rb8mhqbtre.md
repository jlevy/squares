---
type: is
id: is-01m0r3zv2hh2jj64rb8mhqbtre
title: Measure terminal flatness and connectivity before defining basin identity
kind: bug
status: in_progress
priority: 0
version: 19
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
created_at: 2026-08-23T20:11:30.757Z
updated_at: 2026-08-24T19:46:35.253Z
---
D-034, blocking the census. Exact evidence: the n=3 side-2 sliding family is a connected positive-dimensional terminal set that one contact certificate and many geometric keys split into quantum-dependent rows. The n=5 golden adds an unresolved pair: equal side, short form, contact certificate, angle signature and contact count but different geometry. Those facts do not prove the n=5 rows are connected or establish a five-dimensional family; raw constraint counting is not a rank certificate. Acceptance: archive both n=5 poses and their active cells; compute the fixed-cell optimal-face rank/nullity from the active LP matrix and objective; compute the full pose/angle active-constraint Jacobian; continue every null direction with independent validity checks; test whether the two endpoints are path-connected across cell/contact strata; report certified dimension or unresolved bounds; and feed the evidence to think-0yo9 rather than choosing identity from side/contact hashes.

## Notes

2026-08-24 exact correction and handoff. Exp-014 fully classifies the n=3 side-2 physical configuration space: the open sliding stratum has one contact certificate, the two endpoint wall strata share a second certificate, and all lie in one connected family. This strengthens rather than removes D-034: endpoint keys and contact certificates are observations, not component identity. Six proposals producing six endpoint rows still establish no saturation and no five-dimensional family.\n\n2026-08-24 exp-033 completes the fixed-angle portion for the equal-side n=5 pair. After a declared D4 action and relabelling, the two source poses are exact endpoints of one Q(sqrt(2)) side-constant segment. Both endpoints verify exactly; one common 30-row cell contains the segment; an exact LP dual proves side 1+5sqrt(2)/4 optimal in that cell; fixed-side active nullities are 0/1/0. Generation plus independent replay takes 0.24s and the full 30-step gate passes in 30s. This closes child think-r29v only. The parent remains open for the full pose/angle active Jacobian, stationary continuation, and unequal-side minimax-clearance bounds, which then feed think-0yo9 and think-nvde.
