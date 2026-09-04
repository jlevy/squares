---
type: is
id: is-01m1q5nyqn2pz25fe9jc15kypf
title: "Efficiency block: the exact event-cell sweep, 68x-139x, same verdicts"
kind: task
status: open
priority: 0
version: 1
labels: []
dependencies: []
created_at: 2026-09-04T21:37:31.380Z
updated_at: 2026-09-04T21:37:31.380Z
---
W5 efficiency-loop block, entered on the operator's direction on 2026-09-04 evening with a measured baseline: the exact event-cell sweep that decides C4 at the retention gate took 1473 s at 1184 atoms (n = 17), 4866 s at 2097 (n = 12) and 5378 s at 2260 (n = 20), fitting atoms^2.00; one direction of the n = 20 certificate profiled at 39.35 s in the Fraction grid and 2.29 s in the reduction, of which a 16.6M-tuple cell list was most. Target: at least 10x, the operator's figure being under 100 s for the n = 20 decision. Guard: the identical least covered mass on every retained certificate, and the Fraction sweep kept unchanged as the reference and matched cell for cell.

Change: sweep.py decides in int64 on the weights' common scale (every retained certificate's weights are multiples of 1/200000; the scaled total is checked against 2**60 and the Fraction route decides above it); the reachable cells are held as one span per column, with reduce_to_cells defined as that expanded; certificate.verify runs the 181 directions in a process pool (fork on Linux -- Python 3.14's forkserver re-imports __main__ and dies for a stdin caller; serial below 400 atoms).

Measured on the same box with the Fraction replay running beside it: n = 17 in 21.8 s (68x), n = 20 in 38.7 s (139x), both returning the declared least. Equivalence: 181 directions of the 373-atom n = 11 rung, Fraction against integer, value and witness, no mismatch. Tests: tests/test_fractional_sweep_integer.py.
