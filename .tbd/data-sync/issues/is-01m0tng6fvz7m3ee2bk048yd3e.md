---
type: is
id: is-01m0tng6fvz7m3ee2bk048yd3e
title: Certify a two-parameter exact n=5 optimal sheet
kind: task
status: closed
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
hold: null
hold_until: null
created_at: 2026-08-24T19:56:01.402Z
updated_at: 2026-08-24T20:13:11.109Z
started_at: 2026-08-24T19:56:09.554Z
closed_at: 2026-08-24T20:13:11.108Z
close_reason: Completed by exp-034 on instrument 329b848 under preregistration 7c6fe96. Exact Q(sqrt(2)) inequalities certify the full declared two-parameter angle-and-slide strip at side 1+5sqrt(2)/4; four boundary fixtures pass, the exp-033 dual remains uniform because it avoids square 0, five mutations fail, retained generation/replay takes 0.27s, and the post-integration normal gate passes 30/30 in 35s. D-186 and D-187 record the pre-run proof-bound correction and integration-anchor miss. Parent think-1q3g stays open for complete nonsmooth cones and continuation.
resolution: null
duplicate_of: null
---
Bounded child of think-1q3g. Certify an explicit two-parameter sheet through exp-033: t=tan(theta0/2), |t|<=1/100; e(t)=|t|(1-|t|)/(1+t^2); u in [e(t), 3sqrt(2)/2-2-e(t)]; square 0 has center (1/2+u,5/2-sqrt(2)/4+u) and angle 2 atan(t), while squares 1..4 remain fixed. Acceptance: prove the parameter strip nonempty; exact uniform containment and SAT margins for all pairs; exact Q(sqrt2) verification of all four t=±1/100 boundary fixtures; replay the unchanged six-row LP dual whose support avoids square 0; independent retained replay and mutations for excessive angle, unshrunk endpoints, signed-vs-absolute support, and dual drift. Scope only a fixed-cell optimal sheet, not full stationarity or component completeness.

## Notes

2026-08-24 exp-034 met the frozen criterion. On corrected instrument 329b848, exact arithmetic proves the whole declared strip |t|<=1/100 and e(t)<=u<=3sqrt(2)/2-2-e(t) feasible at side 1+5sqrt(2)/4; the exp-033 dual support avoids square 0 and certifies every orientation-indexed LP cell optimal. Four signed-angle/slide boundary fixtures validate exactly, five mutations fail, and generation plus replay took 0.27s. Retained result sha256 a718d64f705612eb4c4fde66a8119921aa45262f0c4994bcfffa0f3653c9d73e. D-186 records the pre-prereg universal-bound correction; D-187 records the stale aggregate controls caught on first integration. Scope remains one exact 2D sheet, not the complete stationary component or basin.
