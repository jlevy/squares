---
type: is
id: is-01m0rrhwd2zzyj0x0jwa8cqwtw
title: The quench is ~95% Python/scipy overhead, and it gates the basin census
kind: task
status: open
priority: 0
version: 1
labels: []
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-08-24T02:10:53.473Z
updated_at: 2026-08-24T02:10:53.473Z
---
Measured on this branch, n=11, warm:
- solve_cell LP is 99 rows x 23 cols.
- scipy.optimize.linprog(method='highs') with the required tolerance options: 1456 us/solve.
- The same model passed straight to HiGHS via highspy: 380 us/solve, identical objective to the last digit.
- Actual simplex time inside that is a small fraction again; a 99x23 dense LP is single-digit-microsecond work.

Per quench: ~1,600 solves, ~2.5s. tools/perimeter_test.py alone issued 19,466 linprog calls in one gate step.

So roughly 3.8x is available by dropping scipy's linprog wrapper for highspy (a real dependency, not scipy's private _highspy, which does not export the Highs class), and roughly another order beyond that by moving solve_cell + choose_cell + solve_to_fixed_point into sqsearch, where the geometry kernel already lives and already has the closed form for the pair half-extent.

Why it is worth doing rather than tolerating: the stated next critical path (H-021, H-023) is an endpoint census. At 2.5s/quench, 10k endpoints is ~7h single-threaded; in Rust it is minutes. This is the single highest-leverage engineering investment in the directory.

Sequencing note: do NOT do this before the basin-stability bug is settled. Any change to the quench's floating-point evaluation order currently changes the golden map, and today nothing can tell an improvement from a regression.
