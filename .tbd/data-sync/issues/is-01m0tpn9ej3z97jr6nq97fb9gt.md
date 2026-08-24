---
type: is
id: is-01m0tpn9ej3z97jr6nq97fb9gt
title: Classify complete first-order cones around the n=5 exact sheet
kind: task
status: closed
priority: 0
version: 12
spec_path: explorations/packing/campaign/agendas/agenda-001-basin-confidence-ladder.md
delegate: unknown@spud10.local
labels:
  - packing
  - basin-cartography
  - research
dependencies: []
parent_id: is-01m0tn3kqe19evm1r40wgnpb61
child_order_hints:
  - is-01m0trwxvyta9c3xeqrg6khzfk
  - is-01m0trxw9xh8q7tjnte4zjbk7d
  - is-01m0tt1zq35w141mz8mn61tb5p
hold: null
hold_until: null
created_at: 2026-08-24T20:16:16.849Z
updated_at: 2026-08-24T21:23:55.263Z
started_at: 2026-08-24T20:16:21.613Z
closed_at: 2026-08-24T21:23:55.262Z
close_reason: "Exp-035 completes the bounded first-order slice under the frozen criterion: six exact owner-axis matrices cover A/interior/B, both tied support rows are retained, one exact non-sheet direction satisfies every active row, all seven controls reject, and generation/replay pass. Nonlinear realization is deliberately unresolved and split to think-imav; H-023 and parent think-1q3g remain open."
resolution: null
duplicate_of: null
---
Bounded 30-minute BC-010 slice after exp-034. At the sheet endpoint/interior/end strata, enumerate every active wall-corner inequality and every SAT owner/support branch in the 15 pose variables with ds=0. Acceptance: exact branch inventory and coefficients; distinguish equality-kernel rank from the full union/intersection feasible cone; retain either a normalized non-sheet feasible direction with exact replay or a complete zero/contained-cone certificate; independently test second-order realization or record an explicit unresolved obstruction. No claim about basin mass, full component completeness, or unequal-side clearance.

## Notes

2026-08-24 exp-035 terminal checkpoint: after the criterion was frozen at 26411ae, generation (0.063s internal) and independent replay (0.070s internal) met it. Six exact matrices cover A/interior/B; each of the two owner branches retains both tied support rows, and an exact non-sheet direction makes every active derivative zero at every stratum. All seven controls reject. D-194/think-5hh9 and D-195/think-s41l are fixed and closed. Keep this parent open: first-order feasibility is not a nonlinear/Bouligand motion. Next bounded slice must realize or obstruct the direction without changing exp-035.
