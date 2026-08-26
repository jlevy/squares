---
type: is
id: is-01m0r3zv2hh2jj64rb8mhqbtre
title: Measure terminal flatness and connectivity before defining basin identity
kind: bug
status: in_progress
priority: 0
version: 29
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
updated_at: 2026-08-26T01:47:29.224Z
---
D-034, blocking the census. Exact evidence: the n=3 side-2 sliding family is a connected positive-dimensional terminal set that one contact certificate and many geometric keys split into quantum-dependent rows. The n=5 golden adds an unresolved pair: equal side, short form, contact certificate, angle signature and contact count but different geometry. Those facts do not prove the n=5 rows are connected or establish a five-dimensional family; raw constraint counting is not a rank certificate. Acceptance: archive both n=5 poses and their active cells; compute the fixed-cell optimal-face rank/nullity from the active LP matrix and objective; compute the full pose/angle active-constraint Jacobian; continue every null direction with independent validity checks; test whether the two endpoints are path-connected across cell/contact strata; report certified dimension or unresolved bounds; and feed the evidence to think-0yo9 rather than choosing identity from side/contact hashes.

## Notes

Published conflict-safe checkpoint cb19cc1 on origin/codex/packing-4h-research-loop-2026-08-25. Exp-044 is terminal unresolved with no target run or JSON; its corrected criterion and repository-only handoff passed two audits. Production row-jet builder/tests are at a5a4ef0: 17 focused helper+builder tests pass, Ruff/BasedPyright clean, independent live audit accepted. Active documented phase is W7 correctness under BC-010 through 2026-08-25T19:13:20-07:00: build reusable weighted-stress and exp-034 sheet evaluators only; do not run a pure-W target or infer a disposition. Fresh agents must read session-015 Fresh-Agent Resume; repository artifacts and pushed branch are authoritative, Codex memory/heartbeat optional.
