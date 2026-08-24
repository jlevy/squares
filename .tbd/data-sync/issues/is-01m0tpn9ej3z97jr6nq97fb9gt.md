---
type: is
id: is-01m0tpn9ej3z97jr6nq97fb9gt
title: Classify complete first-order cones around the n=5 exact sheet
kind: task
status: in_progress
priority: 0
version: 4
spec_path: explorations/packing/campaign/agendas/agenda-001-basin-confidence-ladder.md
delegate: unknown@spud10.local
labels:
  - packing
  - basin-cartography
  - research
dependencies: []
parent_id: is-01m0tn3kqe19evm1r40wgnpb61
hold: paused
hold_until: null
created_at: 2026-08-24T20:16:16.849Z
updated_at: 2026-08-24T20:24:08.161Z
started_at: 2026-08-24T20:16:21.613Z
---
Bounded 30-minute BC-010 slice after exp-034. At the sheet endpoint/interior/end strata, enumerate every active wall-corner inequality and every SAT owner/support branch in the 15 pose variables with ds=0. Acceptance: exact branch inventory and coefficients; distinguish equality-kernel rank from the full union/intersection feasible cone; retain either a normalized non-sheet feasible direction with exact replay or a complete zero/contained-cone certificate; independently test second-order realization or record an explicit unresolved obstruction. No claim about basin mass, full component completeness, or unequal-side clearance.

## Notes

2026-08-24 10-minute orientation complete. At an interior exp-033 point let r=sqrt(2), delta=3r/2-2. The exact direction dx0=delta, dx4=delta/2, dtheta3=dtheta4=1, all other coordinates zero, satisfies every common active wall inequality and all seven active SAT derivatives (04,14,24 plus both owners and both tied features for 34). Endpoint variants are A: dx4=delta/2, dy0=-delta, dtheta3=dtheta4=1; B: dx0=delta, dx4=delta/2, dtheta3=dtheta4=1. It is outside exp-034 because that sheet keeps theta3=theta4 fixed. Exp-035 should retain exact branch inventory/ranks and these witnesses, while declaring nonlinear continuation unresolved; a later child may solve rotating contacts in half-angle coordinates.

Paused: Paused at user-requested PR #21 review boundary. Candidate checker is committed and pushed at 8aa0cbb; frozen Ruff, BasedPyright, py_compile, and diff checks pass. It has NOT been scientifically executed, preregistered, or integrated into the gate, and therefore supports no result. Resume by semantic review of geometry_inventory/contact-row completeness, commit any correction, create exp-035 with the bead's frozen first-order criterion, then generate/replay under separate 30s caps. Current branch was clean when paused.
