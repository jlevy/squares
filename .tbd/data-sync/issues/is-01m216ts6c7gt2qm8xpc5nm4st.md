---
type: is
id: is-01m216ts6c7gt2qm8xpc5nm4st
title: Make quench_bracket honour its wall budget, and profile it above n = 19
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m20zyy839t6mbvpqy8ay2hsn
created_at: 2026-09-08T19:10:02.443Z
updated_at: 2026-09-08T23:57:16.962Z
---
exp-133 measured basin hopping over the LP-in-cell quench against multistart at exactly 500 quench calls each, and basin hopping won on four cells of five (n = 10, 11, 17, 19) by 0.086 to 0.133, with disjoint seed ranges at n = 10 and n = 19. Its best n = 11 result, 3.897231, is better than the annealer control's 3.922761 at a budget four orders of magnitude smaller in raw operations.

Two instrument problems bound that result and both are cheap to fix.

1. quench_bracket does not honour its time_budget. A declared 4 s produced individual calls of up to roughly 30 s, because the budget is tested between solver operations and one fixed-point solve can run past it. The two conditions got equal calls but unequal work per call. Add a CPU bound that the inner loops check, or report the overrun so a round can price it.

2. Cost. One quench call at n = 27 or above does not finish inside any budget round 1 could afford, which is why exp-133 stops at n = 19. Profile solve_cell and solve_to_fixed_point at n = 17 to 30 and find out whether the wall is the LP size, the number of cell re-reads, or the angle bracketing.

Both matter because refined local optima are the currency the record engines spend: Ellsworth's published n = 51 statistics are 4 record basins in 3,004 classified refinements, and exp-133 could afford 20 per seed.
