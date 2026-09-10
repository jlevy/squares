---
type: is
id: is-01m24r3sgyw8hj7k7cfd8spmxg
title: Iterate LP support and atom set together, separating from the depth-one certificate
kind: task
status: open
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-10T04:09:46.782Z
updated_at: 2026-09-10T06:29:02.057Z
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
    exactly for that fixed-support program: a family of total 325657893/31250000 feasible for
    that program's selected finite rows -- depth at most one at the structural sites, the atom
    orbits, the six seeded atoms -- against an exact dual bound 2605263163/250000000 with
    A^T u >= cost verified in Fractions. That family is NOT feasible for the depth-one program
    (its exact maximum depth is 105263157/100000000, and the reader refuses it at K2), so
    10.4210526 is a value of the restricted program and not a bound on the depth-one one. The
    dual side is serialized as lane-a6-dual-bracket-10-42.json. Lane A4's 24 atoms separated from a dual vertex
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
as run), lane-a6-lp-struct.py.txt (lane A4's LP driver plus --seed-sites), lane-a6-dual-
bracket.py.txt with lane-a6-dual-bracket-10-42.json (the dual side of the 10.42 bracket, its
seven priced rows and their multipliers), lane-a6-atoms-2566-orbits.json (the atom set the
certificate is a statement about), and the six separated atoms in both reader shape and
freeze-record shape.

Done when either a rows-complete value below eleven at 153/40 is frozen and decided by the
two-route gate, or the loop is shown to stall for a named reason with its own certificate.

## Notes

Author source is retained through 6ed45816bc176170bdaa008248d22a6d09956a00,
following ee98c4ba's A6 and H157/exp154 handoff. The second handoff supplies the
2,566-orbit atom file, seven priced upper-dual rows, the second structural LP's
terminal disposition, and the allocation boundary exp154/H157/session125. Author
idea154 and think-yc80 own the joint support/atom continuation proposal; reconcile
that existing work with the new overnight agenda rather than duplicate it.

A6: independent_ceiling_reader passed K0-K3 and D4 for the 64-placement family,
14,344 arrangement vertices, and three negative controls. A maintained exact
threshold-atom reader then checked all 2,566 orbits, 20,524 images and 14,949 sites,
with no violation. Ratio one is attained by 935 orbits, with strict slack on 1,631;
the delivered 'every ratio equals one' wording is corrected. Receipts are at
/private/tmp/pr139-ee98-a6-independent-ceiling.json and
/private/tmp/pr139-a6-2566-exact-membership.json, being adopted with Git bindings.
The seven-row upper certificate is supplied and Sol xhigh independently recomputes
its exact geometric coefficients under think-aocp. Its lower family is not
depth-one feasible; an admitted upper still applies to the stronger full-depth
program on the same support. No global bound follows.

H157: Astra Max independently reproduced survivor counts and reviewed corrections.
Six refined subclasses remain at ten, two improve to 19/2. The maximum-based
rejection is supported; two intersecting cases invalidate the original positive
distance explanation. Patch-subset survival is at least ten; equality needs a
common-mark premise. Isolated parents are contained, but full-packing compatibility
and unavoidable neutral owner selection remain unproved. A Sol xhigh maintained
geometry replay and meaningful controls are being integrated under think-9zc9.

The second structural LP was unfinished beyond 4,260 seconds and ended in a
container restart with an empty scratch log. It has no final value. No further
target allocation was reported beyond exp154, H157 and session125.

The full d21 checkpoint completed but does not validate these later files. New
source plus corrections require the final matching checkpoint under think-yl6y.
No new scientific target has been run in this intake. V3 alignment remains tracked
in think-i1fr pending the owner's exact specification path; no compliance claimed.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
