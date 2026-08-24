---
type: is
id: is-01m0tn3kqe19evm1r40wgnpb61
title: Test angle-active stationarity along the exact n=5 face
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
parent_id: is-01m0r3zv2hh2jj64rb8mhqbtre
child_order_hints:
  - is-01m0tng6fvz7m3ee2bk048yd3e
hold: null
hold_until: null
created_at: 2026-08-24T19:49:08.973Z
updated_at: 2026-08-24T19:56:09.976Z
started_at: 2026-08-24T19:49:21.117Z
---
Bounded BC-010 second slice, capped at 30 agent-minutes. Starting from exp-033 exact Q(sqrt(2)) endpoints and interior, enumerate every locally active wall/SAT feature branch in open real angle charts; compute the full pose-angle fixed-side linearized cone exactly or retain an explicit unresolved bound. Acceptance: exact branch inventory and coefficients, one-to-one retained replay, known-rigid/flexible mutations, and an asymmetric verdict: all zero cones may certify local isolation in that stratum, while a nonzero linearized direction only triggers nonlinear continuation and never proves a feasible motion. Do not infer basin mass, global component identity, or census completeness.

## Notes

2026-08-24 bounded orientation complete. Exact full fixed-side first-order inventory from exp-033 has 15 pose variables. The common contacts are 04,14,24,34; pair 34 has four owner/support branches. Retaining tied wall features gives exact equality ranks/nullities interior 12/3 and endpoints 14/1 across all branches. This alone does not decide the nonsmooth feasible cone or stationarity. A second-order feature is tractable immediately: theta0 is first-order invisible at its 45-degree contact, and rotating square 0 opens that contact by sqrt(2)(1-cos theta0)/2. Child think-7pn0 preregisters an exact two-parameter fixed-cell optimal sheet with a uniform parameter strip and the unchanged exp-033 dual. Keep this bead open afterward for the complete wall-release/SAT branch cone and certified continuation.
