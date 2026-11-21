# Plan Amendment 1 (C5), Before Checker Freeze 2

Lane r1050, 2026-11-20. Written before `r1050_refute` ran on any case at the source's cap
$U = 4.822876$, and before any source program was opened or run. The plan
(`review-plan.md`, frozen at 16:54:02Z) stands except as stated here.

## What Changed in C5 During Development

- **Adaptive slices.** With fixed angle slices the refuter could not refute four squares
  in a box of side 1.99: at 32 slices the inner squares lose about 0.024 per pair, more
  than the instance's 0.01 margin, so no branching helps. An angle branch on a tile with
  one live slice now bisects that slice and re-seeds both halves (R1 to R3) inside the
  parent's polygon, so the inner squares grow as the slices narrow. Initial slices
  $K = 32$, at most 60 propagation rounds per node, branch depth at most 400.
- **Self-test.** Five squares in a box of side 2.70 (below $s(5) = 2 + 1/\sqrt2$) must be
  refuted, and five in 2.71 (feasible) must not. All six synthetic instances now give
  the expected outcome.

## Calibration, Disclosed

To judge the refuter's power, it ran on the source's lattice at caps 4.40 and 4.70, never
at $U$, on three orbits chosen by hand before the sample was drawn:

| Unoccupied marks | Cap 4.40 | Cap 4.70 (120 s) |
| --- | --- | --- |
| (617,617), (1000,1000), (1383,1383) | refuted at the root | undecided |
| (390,390), (390,1610), (1610,390) | refuted at the root | refuted at the root |
| (1000,716), (1000,1000), (1000,1284) | refuted at the root | undecided |

## Budget

Each sampled case, and the witness orbit as a control, runs for 20 CPU-minutes (the plan
said one CPU-hour): calibration suggests a case is decided early or not within any budget
this lane can spend. The sample rule is unchanged.

## Results Already Obtained After Checker Freeze 1

C1 to C4 ran on the source's data after freeze 1 (17:00:45Z), before this amendment: the
construction is valid, the covering lemma holds at $\varepsilon = 1/100000$, the five
covering controls fail as stated, there are 187 orbits, and the construction reaches only
the orbit with unoccupied marks (617,617), (1000,1000), (1383,1383). The witness orbit
therefore enters the sample rule as stated in the plan.
