---
type: is
id: is-01m0tpn9ej3z97jr6nq97fb9gt
title: Classify complete first-order cones around the n=5 exact sheet
kind: task
status: in_progress
priority: 0
version: 9
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
hold: null
hold_until: null
created_at: 2026-08-24T20:16:16.849Z
updated_at: 2026-08-24T21:11:20.862Z
started_at: 2026-08-24T20:16:21.613Z
---
Bounded 30-minute BC-010 slice after exp-034. At the sheet endpoint/interior/end strata, enumerate every active wall-corner inequality and every SAT owner/support branch in the 15 pose variables with ds=0. Acceptance: exact branch inventory and coefficients; distinguish equality-kernel rank from the full union/intersection feasible cone; retain either a normalized non-sheet feasible direction with exact replay or a complete zero/contained-cone certificate; independently test second-order realization or record an explicit unresolved obstruction. No claim about basin mass, full component completeness, or unequal-side clearance.

## Notes

2026-08-24: resumed after PR19 merge under the four-hour campaign horizon. The earlier checker at 8aa0cbb remained unexecuted and unpreregistered. Audit found D-194 (the pair 0,4 differential is stratum-dependent) and D-195 (tied supports are a conjunction within each owner-axis choice). The corrected instrument now derives contact rows from each exact endpoint/interior pose, retains two owner-axis branches with two tied-support rows per branch, uses corrected non-sheet witnesses, and includes explicit missing-row and stale-coefficient controls. Static-only validation passed Ruff, BasedPyright, py_compile, and diff-check without importing or executing the checker. Next: commit the instrument, preregister exp-035, then run generation and replay under separate 30-second caps.
