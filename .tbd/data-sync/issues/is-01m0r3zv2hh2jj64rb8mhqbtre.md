---
type: is
id: is-01m0r3zv2hh2jj64rb8mhqbtre
title: Measure terminal flatness and connectivity before defining basin identity
kind: bug
status: open
priority: 0
version: 9
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels: []
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
parent_id: is-01m0p49s01h862tq6wp0dd085c
created_at: 2026-08-23T20:11:30.757Z
updated_at: 2026-08-23T20:45:32.606Z
---
D-034, blocking the census. Exact evidence: the n=3 side-2 sliding family is a connected positive-dimensional terminal set that one contact certificate and many geometric keys split into quantum-dependent rows. The n=5 golden adds an unresolved pair: equal side, short form, contact certificate, angle signature and contact count but different geometry. Those facts do not prove the n=5 rows are connected or establish a five-dimensional family; raw constraint counting is not a rank certificate. Acceptance: archive both n=5 poses and their active cells; compute the fixed-cell optimal-face rank/nullity from the active LP matrix and objective; compute the full pose/angle active-constraint Jacobian; continue every null direction with independent validity checks; test whether the two endpoints are path-connected across cell/contact strata; report certified dimension or unresolved bounds; and feed the evidence to think-0yo9 rather than choosing identity from side/contact hashes.

## Notes

Reconciled after PR #14 merged. The earlier description subtracted 11 contacts from 16 variables and called the result an exact five-dimensional family. That was an unsupported inference: active constraints may be dependent, the fixed-cell LP has a different variable space from the full angle-moving quench, and equal side/contact data do not prove connectedness. This bead now owns the measurement; think-0yo9 owns the definition. D-034 and the review document preserve the correction.
