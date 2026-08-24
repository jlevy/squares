---
type: is
id: is-01m0tpn9ej3z97jr6nq97fb9gt
title: Classify complete first-order cones around the n=5 exact sheet
kind: task
status: in_progress
priority: 0
version: 8
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
updated_at: 2026-08-24T21:00:55.620Z
started_at: 2026-08-24T20:16:21.613Z
---
Bounded 30-minute BC-010 slice after exp-034. At the sheet endpoint/interior/end strata, enumerate every active wall-corner inequality and every SAT owner/support branch in the 15 pose variables with ds=0. Acceptance: exact branch inventory and coefficients; distinguish equality-kernel rank from the full union/intersection feasible cone; retain either a normalized non-sheet feasible direction with exact replay or a complete zero/contained-cone certificate; independently test second-order realization or record an explicit unresolved obstruction. No claim about basin mass, full component completeness, or unequal-side clearance.

## Notes

2026-08-24 initial orientation: at an interior exp-033 point, the committed candidate used an exact non-sheet direction with diagonal angle motion. It was paused before preregistration or execution for PR 21 review; checker commit 8aa0cbb was static-only. Resumed after PR 19 merged under a four-hour campaign horizon. Semantic audit found two pre-measurement soundness defects: D-194, the (0,4) contact differential changes with slide stratum but the checker reused endpoint A's coefficient; and D-195, tied support derivatives at pair (3,4) are a conjunction within each owner-axis branch, not four alternative branches. Beads think-5hh9 and think-s41l track the corrections. A partial exact-derivative refactor is saved in the named WIP stash before rebasing onto merged main; it has not been linted, preregistered, or scientifically run. Resume by restoring the stash on the fresh branch, finish semantic validation, commit the corrected instrument, then preregister exp-035 before any target execution.
