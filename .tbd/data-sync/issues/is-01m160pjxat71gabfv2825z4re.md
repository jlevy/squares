---
type: is
id: is-01m160pjxat71gabfv2825z4re
title: "Block 9: exact solve and round trip"
kind: task
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-08-29T05:43:23.818Z
updated_at: 2026-08-29T07:44:46.391Z
closed_at: 2026-08-29T07:44:46.391Z
close_reason: "Closed in session-042, with one answer and one refusal. At n=11 the frozen margin rule recovers Trump's published degree-8 minimal polynomial from digits alone (C=12420, B=36.85, M=200; residual 4.99e-338 at B+M falling to 3.38e-412 at 2B+2M) and discharges it as irreducible over Q with an isolating interval. At n=29, on 1000 digits with reported residual bound 1.09829e-1039, pslq returns nothing at any degree 2..20 below 1e22 — not one degree reached a clause. The planning probe on ~98 digits had found relations at almost every degree 8..21, so the contrast is evidence about the number: if s(29) is algebraic of degree <=20, some coefficient is at least 1e22. Two devtools retain both measurements."
resolution: null
duplicate_of: null
---
agenda-006 BC-061, advancing BC-044. The exact route's phase 4, now that assembly exists: minimal polynomial by elimination or integer relation, under the spec's frozen margin rule, discharged by back-substitution.
