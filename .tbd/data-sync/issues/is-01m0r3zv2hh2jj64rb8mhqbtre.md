---
type: is
id: is-01m0r3zv2hh2jj64rb8mhqbtre
title: Measure terminal flatness and connectivity before defining basin identity
kind: bug
status: in_progress
priority: 0
version: 25
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
updated_at: 2026-08-26T00:40:02.769Z
---
D-034, blocking the census. Exact evidence: the n=3 side-2 sliding family is a connected positive-dimensional terminal set that one contact certificate and many geometric keys split into quantum-dependent rows. The n=5 golden adds an unresolved pair: equal side, short form, contact certificate, angle signature and contact count but different geometry. Those facts do not prove the n=5 rows are connected or establish a five-dimensional family; raw constraint counting is not a rank certificate. Acceptance: archive both n=5 poses and their active cells; compute the fixed-cell optimal-face rank/nullity from the active LP matrix and objective; compute the full pose/angle active-constraint Jacobian; continue every null direction with independent validity checks; test whether the two endpoints are path-connected across cell/contact strata; report certified dimension or unresolved bounds; and feed the evidence to think-0yo9 rather than choosing identity from side/contact hashes.

## Notes

2026-08-25 session-015 published checkpoint d589b05 on origin/codex/packing-4h-research-loop-2026-08-25. Earlier exact evidence remains: exp-033/034 give the fixed-angle segment and angle sheet; exp-035/036 expose and obstruct +W; exp-038 gives the complete branchwise linearized-cone inventory; exp-039 gives twelve exact R1/R2/R3/R6 paths in one five-dimensional cell-local LP-optimal polytope.

Exp-042 is accepted from clean engine commit 2980fdc. Retained generation and replay certify all six (R4,R5) x (A,interior,B) paths, both owner-branch positive first-order stresses, case-indexed base/open/endpoint inventories, and 20 typed semantic controls. The stress-only control preserves criterion_met feasibility and leaves the combined result unresolved. This is pathwise first-order nonlinear realization only, not exhaustive R4/R5 realization, an A-to-B stationary connection, whole-component stationarity, -W or mixed realization, terminality, quench selection, basin identity/mass, census completeness, or unequal-side clearance.

Current bounded slice: session-015 phase 5, deadline 2026-08-25T17:59:27-07:00. Exp-043 is frozen and independently accepted for soundness and portability before its checker exists. Implement only explorations/packing/cases/n5/minus_w_obstruction.py without changing the criterion. It tests canonical pure -W at A/interior/B with universal second-order-correction elimination, independent obstruction/sign-symmetry results, both owner branches and tied rows, a production exp-034 sheet-curve anti-overobstruction oracle, eight typed production mutations, deterministic replay, and explicit invalid/unresolved routing. If the checker cannot meet the frozen guards by the deadline, terminalize a finite exact blocker; do not infer a -W obstruction from checker failure and do not begin basin-frequency work.

Portable resume is repository-owned: read explorations/packing/campaign/agent-sessions/session-015-four-hour-r4-r5-loop.md and its directly linked exp-043 criterion after fetching the recorded remote branch. Chat history, Codex memories, native goals, and scheduled wakeups are optional controllers only.
