---
type: is
id: is-01m216trdrcrb87d6h4nhzkw4f
title: Seed off the grid at n >= 27, where the collective escape rate measures zero
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m20zyy839t6mbvpqy8ay2hsn
created_at: 2026-09-08T19:10:01.654Z
updated_at: 2026-09-08T19:10:01.654Z
---
Round 1's failure is sharp and localized: every arm leaves the trivial grid at n <= 26 and none of them does at n = 29, 50, 52, while only the both-factors arm reaches n = 27 and n = 37.

The mechanism is measured, not guessed. devtools/measure_objective_sparsity.py draws proposals from the engine's own two distributions at the trivial grid and counts what each does to required_side. Over 8,000 proposals per kind per cell at scales 0.01, 0.05 and 0.2:

- No single-square proposal LOWERS the side at any cell of the subset except n = 5. A quarter to a third change it and every one of those raises it. The grid is a strict local minimum of required_side under the whole single-square move set, because the binding span is attained by a whole row or column of m squares and no one of them is the unique extremum.
- Collective proposals do lower it, but the rate collapses with n: 0.0034-0.0051 at n = 11, 0.0006-0.0009 at n = 17, and 0.0000 at n >= 26.

So escaping the grid is a rare collective event whose probability falls with n, and a fixed budget buys escapes up to some n and not beyond. Two things follow for round 2.

1. Seed off the grid rather than trying to leave it. The catalogue's own record-holders do this: neighbour transfer (registered here as H-004, instrument not built), remove-and-straighten from n+1, an analytically constructed state. This is the cheapest way to test whether the wall is the escape or the search.
2. Measure the escape rate directly as a function of n and budget, rather than inferring it from best_side. The instrument already exists; what is missing is a round that sweeps it.
