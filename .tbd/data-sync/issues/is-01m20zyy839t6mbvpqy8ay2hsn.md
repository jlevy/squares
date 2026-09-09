---
type: is
id: is-01m20zyy839t6mbvpqy8ay2hsn
title: "[epic] Move-set campaign: which annealing physics recovers non-grid s(n) records"
kind: epic
status: open
priority: 1
version: 14
labels: []
dependencies: []
child_order_hints:
  - is-01m20zzqjwygewaj8wkyt57shq
  - is-01m20zzsft1e4fg2370kjhp26d
  - is-01m20zztsqytk9pzr8cj930m0y
  - is-01m216ssa7nnm70z56gwgdts1a
  - is-01m216ssx3jqszgssgvymnn6fg
  - is-01m216trdrcrb87d6h4nhzkw4f
  - is-01m216trt4hkdx53q6d94v2phs
  - is-01m216ts6c7gt2qm8xpc5nm4st
created_at: 2026-09-08T17:09:58.636Z
updated_at: 2026-09-09T00:20:14.513Z
---
Umbrella for the campaign answering the repository owner's question: with the right physics or annealing model, which method recovers best-known non-grid packings for n < 100 to high accuracy?

Design input: docs/project/research/research-2026-09-08-annealing-for-square-packing.md, the 2026-09-08 annealing survey. Its central claims this campaign tests:

- "Solve to n = 100" is 36 non-grid cases, not 100. Re-derived here from the frontier register: 36 non-grid at n <= 100, of which 15 hand-construction, 10 simulated annealing, 6 diagonal-strip, 3 extension, 2 unknown.
- required_side is a max over the two to four extreme squares, so most single-square moves are exact no-ops on the objective. That is the structural reason a plain annealer sticks just above the trivial size.
- The fixes used by engines that get close: simultaneous perturbation (Gensane layer 3), inflation or wall pressure or contract-act-re-expand, and replica exchange over a pressure ladder.
- The currency is refined local optima per record, not moves (Ellsworth: 4 of 3,004 at n = 51).

Round-1 registry: H-135 simultaneous perturbation, H-136 wall pressure, H-137 basin hopping over the LP quench.
Round-1 rounds: exp-134 calibration, exp-135 arm B, exp-136 arm C, exp-137 arm D.

## Notes

Round 1 complete. Verdict, in one line: no arm passes the pre-declared accept rule, and the reason is not that the arms are weak.

Accept rule declared before measuring: median best_side at least 0.01 below the control with disjoint seed ranges on at least 6 of the 11 non-grid cells, five seeds each, every pose re-verified by sqpack.verify in a separate process.

Cells improved by at least 0.01 (of 11), and with disjoint ranges:
- control (stock sqsearch): baseline
- collective move alone (--p-perturb 1.0 --perturb-scale 2): 4, of which 3 disjoint. H-135 refuted.
- long anneal alone (--steps 4000000): 3, all disjoint. H-138 refuted.
- both: 5, of which 3 disjoint.
- wall pressure (--mu0 5 --mu1 5): 1 improves and 3 regress. H-136 refuted, and the arm is harmful.
- basin hopping over the LP quench against multistart at equal refined optima: 4 of 5 cells. H-137 confirmed.

Best side reached anywhere, against the record: n=5 +2.5e-9, n=10 +1.4e-8, n=11 +9.7e-3, n=17 +2.15e-3, n=19 +7.3e-2, n=26 +8.6e-2, n=27 +1.2e-1, n=29 +6.6e-2 (the grid), n=37 +1.7e-1, n=50 +3.6e-1, n=52 +2.9e-1 (the grid).

Where it stops working, and why, measured rather than argued: at the trivial grid no single-square proposal lowers required_side at all for any cell of the subset except n=5, at any proposal scale tried; the grid is a strict local minimum under the whole single-square move set. Collective proposals do lower it, but the rate collapses with n -- about 0.004 at n=11, 0.0008 at n=17, and 0.0000 at n>=26. That is the wall, and it is why every arm dies between n=27 and n=29.

Nothing reported a side below any standing best: 5,384 scored lines checked, 0 below.
