---
type: is
id: is-01m24r3sgyw8hj7k7cfd8spmxg
title: Iterate LP support and atom set together, separating from the depth-one certificate
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-10T04:09:46.782Z
updated_at: 2026-09-10T04:09:46.782Z
---
From agenda-034 lane A6, finding G15. The site side at 153/40 is closed on this atom set and
the atom side converges on a fixed support, so the remaining work is a loop over both
together rather than a column count on either.

What lane A6 established, and why one-sided separation stalls.

  * A D4-symmetric family of 64 admissible placements, total exactly 11, exact maximum depth
    exactly 1 everywhere, charging all 2,566 atom orbits at ratio exactly 1, is dual-feasible
    for EVERY site set. So no site set can bring the rows-complete LP below eleven at 153/40
    on this atom set. Retained as lane-a6-saturated-symmetric-153-40.json.
  * Six atoms separated from THAT family -- not from a dual vertex -- take the fixed-support
    maximum on the 280-placement 1/25 support from exactly 11 to 10.4210526, bracketed
    exactly between a feasible 325657893/31250000 and an exact dual bound 2605263163/250000000
    with A^T u >= cost verified in Fractions. Lane A4's 24 atoms separated from a dual vertex
    moved the LP by 2.2e-13; these six move their support by 0.579.
  * Fed to the LP as columns, those same six enter at primal weight exactly zero and the value
    stays at 11.000000000 (39,582 iterations, 934.5 s). The LP moves to a support they do not
    cut, exactly as it moved to a new deep cell after every site round. One atom round on one
    support is to the atom side what one vertex round on one dual was to the site side.

The loop to build. Solve the LP; take its dual's support; run the fixed-support maximum on
that support under depth-one-everywhere plus every atom so far; read the optimum with
devtools.plateau_reader; add every uniform-multiplicity atom it returns; repeat on that
support until it falls below eleven; feed every atom found back as columns; re-solve the LP.
Repeat.

Costs, measured: each LP solve 400 to 950 s, each fixed-support round about 20 s, each reader
run 13 to 80 s. The loop is affordable.

Two things it needs.

  1. Lane A4's gate bypass. The fixed-support optima stop being packings after the first
     round -- the 10.42 optimum has exact maximum depth 105263157/100000000 = 1.05263157 --
     so the reader refuses them at K2 and the loop cannot continue without the bypass. Every
     reading taken past that point is a separation-oracle reading, and no non-violation there
     is a cap.
  2. The reader's completeness conditions, carried rather than assumed: its budget-one
     procedure descends into sub-cliques wherever tau* >= 2, because tau* is monotone under
     inclusion and an overweight sub-clique can carry the violated atom; and its higher-budget
     separation is a bounded integer program whose zero result is the solver's claim within
     its threshold range and time limit, never a feasibility proof.

The freeze path is not a blocker here. All six atoms of G13 are (S, k) threshold atoms with
uniform multiplicity -- two-of-three is |S| = 3, k = 2 and three-of-five is |S| = 5, k = 3 --
which ThresholdAtom already carries, so this route is freezable and gateable today. think-g3j7
blocks only the K5 clique atoms and the K6 floor atoms, and the loop deliberately discards
those.

Instruments are retained beside the lane report: lane-a6-symmetric-max.py.txt (the
fixed-support maximum that produced the certificate), lane-a6-run-atom-loop.sh.txt (the loop
as run), lane-a6-lp-struct.py.txt (lane A4's LP driver plus --seed-sites), and the six
separated atoms in both reader shape and freeze-record shape.

Done when either a rows-complete value below eleven at 153/40 is frozen and decided by the
two-route gate, or the loop is shown to stall for a named reason with its own certificate.
