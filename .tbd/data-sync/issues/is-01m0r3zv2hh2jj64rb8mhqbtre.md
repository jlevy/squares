---
type: is
id: is-01m0r3zv2hh2jj64rb8mhqbtre
title: Measure terminal flatness and connectivity before defining basin identity
kind: bug
status: in_progress
priority: 0
version: 27
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
updated_at: 2026-08-26T01:23:13.871Z
---
D-034, blocking the census. Exact evidence: the n=3 side-2 sliding family is a connected positive-dimensional terminal set that one contact certificate and many geometric keys split into quantum-dependent rows. The n=5 golden adds an unresolved pair: equal side, short form, contact certificate, angle signature and contact count but different geometry. Those facts do not prove the n=5 rows are connected or establish a five-dimensional family; raw constraint counting is not a rank certificate. Acceptance: archive both n=5 poses and their active cells; compute the fixed-cell optimal-face rank/nullity from the active LP matrix and objective; compute the full pose/angle active-constraint Jacobian; continue every null direction with independent validity checks; test whether the two endpoints are path-connected across cell/contact strata; report certified dimension or unresolved bounds; and feed the evidence to think-0yo9 rather than choosing identity from side/contact hashes.

## Notes

2026-08-25 session-015 checkpoint 31e0abe is published on origin/codex/packing-4h-research-loop-2026-08-25. Exp-042 remains accepted from engine 2980fdc. Exp-043 remains terminal unresolved with no result JSON after two audits rejected its hand-written second-order instrument.

Phase 6 W7 completed: src/sqpack/research/exact_jets.py now provides case-free exact value/gradient/Hessian jets, z0+t*v+t^2*a substitution, strict and tied feature-sign handling, wall/SAT gap builders, and weighted combinations. tests/test_exact_jets.py has 6 source-bound tests that match complete A/interior/B x both-owner n=5 row keys and gradients. Focused checks and the 15-step fast gate pass. The helper explicitly does not enumerate feasible subsequences, route non-t^2 scales, or prove obstruction.

Current bounded slice: session-015 phase 7, deadline 2026-08-25T18:49:44-07:00. Exp-044 is frozen at 31e0abe before pure-W case edits. It requires all production rows to use exact_jets, full +/-W and sheet jets, weighted actual rowwise curvature with all correction columns canceled, checked exp-034 sheet witness, executable bounded/unbounded abs(delta)/t^2 routing, independent scientific/mechanism dispositions, 12 typed production mutations, 13 refusals, and deterministic replay. Prereg audits are running before implementation. No basin-frequency work.

Portable resume: fetch the branch and read session-015, exp-044, H-023, and BC-010. Repository files and this bead are authoritative; chat history, Codex memories, native goals, and scheduled wakeups are optional controllers only.
