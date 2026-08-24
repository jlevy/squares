---
type: is
id: is-01m0tng6fvz7m3ee2bk048yd3e
title: Certify a two-parameter exact n=5 optimal sheet
kind: task
status: in_progress
priority: 0
version: 3
spec_path: explorations/packing/campaign/agendas/agenda-001-basin-confidence-ladder.md
delegate: unknown@spud10.local
labels:
  - packing
  - basin-cartography
  - research
dependencies: []
parent_id: is-01m0tn3kqe19evm1r40wgnpb61
hold: null
hold_until: null
created_at: 2026-08-24T19:56:01.402Z
updated_at: 2026-08-24T20:12:26.028Z
started_at: 2026-08-24T19:56:09.554Z
---
Bounded child of think-1q3g. Certify an explicit two-parameter sheet through exp-033: t=tan(theta0/2), |t|<=1/100; e(t)=|t|(1-|t|)/(1+t^2); u in [e(t), 3sqrt(2)/2-2-e(t)]; square 0 has center (1/2+u,5/2-sqrt(2)/4+u) and angle 2 atan(t), while squares 1..4 remain fixed. Acceptance: prove the parameter strip nonempty; exact uniform containment and SAT margins for all pairs; exact Q(sqrt2) verification of all four t=±1/100 boundary fixtures; replay the unchanged six-row LP dual whose support avoids square 0; independent retained replay and mutations for excessive angle, unshrunk endpoints, signed-vs-absolute support, and dual drift. Scope only a fixed-cell optimal sheet, not full stationarity or component completeness.

## Notes

2026-08-24 exp-034 met the frozen criterion. On corrected instrument 329b848, exact arithmetic proves the whole declared strip |t|<=1/100 and e(t)<=u<=3sqrt(2)/2-2-e(t) feasible at side 1+5sqrt(2)/4; the exp-033 dual support avoids square 0 and certifies every orientation-indexed LP cell optimal. Four signed-angle/slide boundary fixtures validate exactly, five mutations fail, and generation plus replay took 0.27s. Retained result sha256 a718d64f705612eb4c4fde66a8119921aa45262f0c4994bcfffa0f3653c9d73e. D-186 records the pre-prereg universal-bound correction; D-187 records the stale aggregate controls caught on first integration. Scope remains one exact 2D sheet, not the complete stationary component or basin.
