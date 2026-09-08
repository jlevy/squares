---
type: is
id: is-01m216ssx3jqszgssgvymnn6fg
title: Sweep the cooling-schedule length axis properly, and separate it from restart count
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m20zyy839t6mbvpqy8ay2hsn
created_at: 2026-09-08T19:09:30.403Z
updated_at: 2026-09-08T19:09:30.403Z
---
Round 1 (exp-130, exp-133) ran the first factorial crossing of cooling-schedule length with move set that could be found for this problem, at two levels each, and both factors moved the result. Cells of eleven improved by at least 0.01: control 0, long schedule alone 3, collective move alone 4, both 5.

The schedule axis was never swept. --steps already existed, the round changed no code, and a tenfold length change recovered three quarters of what the new move family recovered. So sweep it before building anything else.

What round 2 should vary, and why the two are confounded now: at a fixed pair-test budget, longer anneals mean proportionally fewer restarts. This round cannot separate "slower cooling helps" from "fewer, deeper descents help". Vary anneal length and restart count independently -- for instance hold the number of restarts fixed and change the budget, or hold steps fixed and change p_reseed and max_restarts.

Depends on the pair-test budget granularity fix, because the long-schedule arms overshot their declared budget by 2 to 74 percent and the interaction cell by up to 4x at large n.

Cells and seeds as in exp-130: n in {5, 10, 11, 17, 19, 26, 27, 29, 37, 50, 52}, seeds 1-5, and the accept rule frozen before the round.
