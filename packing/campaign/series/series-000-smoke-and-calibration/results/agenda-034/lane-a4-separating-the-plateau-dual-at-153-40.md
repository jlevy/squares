# Agenda 034, lane A4: separating the 1/25-integral dual at 153/40, K4, K5 and K6 with the depth gate bypassed

Retained measurement-lane report for
[X-024](../../../../explorations/X-024-two-lines-at-eleven.md), written by a sub-agent
on 2026-09-09, read-only on the repository at `claude/n-11-stronger-result-d730ds`. The
report is reproduced as delivered, with its own findings table and status labels; only
its file references were rewritten to say where each file now is.
X-024 carries the coordinator’s reading.

This is the measurement [lane X1](lane-x1-corner-conditioning-is-mass-neutral.md) named
as the one worth taking instead of the conditioning ladder, and it is X-024 slice A4’s
instrument pointed at a second dual.

> ## Read this warning before any number below

> The object measured, the `1/25`-integral plateau dual after one round of site
> separation, has exact maximum depth `28/25`, **above one**.
> [`devtools/plateau_reader.py`](../../../../../devtools/plateau_reader.py) refuses such
> a family at `K2` by design, because on a family that is not a fractional packing of
> the plane a `K4`/`K5`/`K6` verdict is not a statement about the method.
> **The gate was bypassed here** on a scratch driver that imports the reader’s exact
> searches unchanged, and **every reading below is a separation-oracle reading**:
> 
> - a **violation** is sound: the atom is a valid inequality of the packing problem,
>   this dual violates it exactly, so the atom is a legal column of the covering LP and
>   adding it strictly cuts this dual.
>   That is the whole purpose, and it survives the bypass intact.
> - **a non-violation is not a cap.** Nothing here says the two-of-three method, the
>   budget-one class or the rank-one closure stops at `153/40`. A bypassed gate does not
>   become a claimed cap, and **no statement in this report may be quoted as one.**

Retained beside this report: the small violated atoms, the before/after duals and the
eight scripts that produced every reading, listed under [Files](#8-files).
Not retained (scratch only): the two oracle reports, the five `K6` seed files, the two
LP run directories with their site, row and atom matrices, and the abandoned second
round. The lane also kept a working method note in scratch; it is not retained because
its substance is already here — the bypass and the mask reduction in Section 2, the warm
and cold duals of the same optimal face in P9, and the freeze-reach gap in P10.

Labels: **EXACT** (a rational decision by a repository primitive, script retained),
**CHECKED** (a float LP reading, script retained), **RECORD** (retained files),
**OPEN**.

## 0. The answer in three lines

|  |  |
| --- | --- |
| **LP at `L = 153/40` before** | `10.999999999999945` (11,881 simplex iterations, 310 s) |
| **LP at `L = 153/40` after** | `11.000000000000167` (4,348 iterations, 168 s) — a move of `2.2e-13` |
| **Atoms fed back** | 24 distinct D4 orbits, every one violated exactly: 18 two-of-three at `33/100`, one budget-one clique atom at `1/2`, five Chvátal–Gomory floor atoms at `5.545`, `7.105`, `7.255`, `8.27`, `8.18` |
| **Weight the LP gave them** | exactly zero, all 24 |
| **Outcome** | the second of lane X1’s three: **the LP stays at eleven and the dual relocates** |

## 1. Findings

| # | Finding | Status |
| --- | --- | --- |
| P1 | The gate is what stood between the reader and this family, and nothing else does. With the K2 refusal bypassed, K0, K1 and K3 hold (280 placements admissible, all inside, total exactly 11) and the arrangement reads in 48 s: 283,832 vertices, **22,201 distinct membership sets**, weight scale `1/200`, exact maximum depth `28/25`. Reducing to the sets **maximal under inclusion** — exact for every charge in the module, by monotonicity — leaves **965**, and every K4/K5/K6 search below runs on those. | EXACT |
| P2 | **K4 two-of-three is violated, and by more than the depth.** Exact maximum charge **`133/100`** against budget 1 over all triples of distinct membership sets (complete by the reader’s own pair bound, 77,356 pairs expanded, 96 maximisers, 56 s): violation **`33/100`**. The maximum exceeds the family’s depth `28/25 = 1.12`, so this is not the point constraint restated — a two-of-three atom charges strictly more here than any single point can. The 64 witnesses kept collapse to **18 distinct D4 orbits**; the sparsest sits at `(1.9014, 1.0554)`, `(1.9940, 1.0032)`, `(1.8279, 1.0031)` and charges 40 of the 280 placements. | EXACT (separation-oracle) |
| P3 | **K5 gives the hardest small cut: violation `1/2`.** The closed-intersection graph has 11,252 edges; enumeration of maximal cliques above weight one is **complete** at 1,080 cliques, 363 piercing programs decided exactly, 320 descended for `tau* >= 2` (29 s). The heaviest rank-one clique has **42 members, weight `3/2`, `tau* = 7/4`** (a float proposal certified by an exact primal-dual pair). Its piercing measure rationalises to the atom `a = (1, 2, 2, 1, 1)`, `t = 4`, `a(S) = 7`, budget `floor(7/4) = 1`, floor charge **`3/2`**: violation **`1/2`**, charging all 42 members. Again `3/2 > 28/25`. | EXACT (separation-oracle) |
| P4 | **K6 returns a violated Chvátal–Gomory floor atom at every threshold tried, and they are the largest raw violations — but they are dense global cuts, not local ones.** Five thresholds, 90 s each, all five violated and verified exactly: `t=2` **`1109/200 = 5.545`** (279 points, all multiplicity 1, budget 139); `t=3` **`1421/200 = 7.105`** (304 points, budget 187); `t=4` **`1451/200 = 7.255`** (313, budget 216); `t=5` **`827/100 = 8.27`** (312, budget 231); `t=6` **`409/50 = 8.18`** (315, budget 243). Each uses multiplicity `t-1` on most of its points — the `(t-1)/t` rounding of nearly the whole point system — and each charges the same 264 of 280 placements. Every solver run hit its 90 s limit, so the reported violation is a feasible cut, not the optimum for its threshold (bounds `5.855`, `7.97`, `9.065`, `9.72`, `10.265`). **The threshold form of the same point sets is not violated at all** (threshold charge `201/25 = 8.04` against budgets 139 to 243): only the floor form cuts. | EXACT for each returned atom (separation-oracle); the per-threshold optimum OPEN |
| P5 | The violated atoms live in the sliver lane A3’s S2 named, not somewhere new. The 36 distinct points of the 19 small atoms lie between **`3.7e-4` and `3.0e-2`** from the nearest of the 17,389 LP sites (median `8.7e-4`), and the closest of them is **`3.7e-6`** from a D4 image of the S2 depth witness `(0.99964, 1.82788)`. The three points of the sparsest K4 maximiser sit at `(1.8279, 1.0031)`, `(1.9940, 1.0032)` and `(1.9014, 1.0554)`, and the first of those is `3.7e-6` from the diagonal mirror `(1.82788, 0.99964)` of the S2 witness, so the tightest small atoms are reading exactly the interleaved wall-square edges S2 measured at `0.0006` wide, and the rest fan out to `0.03`. | EXACT points, CHECKED distances |
| P6 | **The LP did not move: `11.000000000` before, `11.000000000` after.** Re-solving the `sites-1` LP (17,389 sites in 2,250 orbits, 2,566 threshold-atom orbits, 15,021 carried rows) cold gives **`10.999999999999945`** (HiGHS, 11,881 iterations, 310 s). Adding the **24 distinct D4 orbits** of violated atoms (18 two-of-three, 1 clique, 5 K6 floor atoms; 168 images; costs 4, 8 and 1,112 to 1,944) and re-solving gives **`11.000000000000167`** (4,348 iterations, 168 s) — a move of `2.2e-13`, five orders below the `7e-8` lane A3’s S1 itself called solver tolerance, and eleven below the `0.018` the `383/100` plateau would need. **Every one of the 24 new columns carries primal weight exactly `0.0`** in the saved `x.npy`, not merely below a threshold. Columns can only lower a covering LP’s value, so this is the value, not a tolerance artefact. | CHECKED (LP float); every atom’s admissibility EXACT |
| P7 | **The dual relocated, and the atoms became tight.** Before: 64 dual rows, 512 placements after D4 symmetrisation. After: **42 rows, 336 placements**, total `1374999981/125000000`. Exactly **0 of the 24 seeded atoms** are violated by the new dual, and several are tight to the last digit — the clique atom at floor charge `999999981/1000000000` against budget 1, four two-of-three atoms at `499999989/500000000` and `49999999/50000000`, i.e. the `1e-9` family rounding below exactly 1. The cut was added, the dual walked onto the face where the cut is active, and the objective did not follow. | EXACT |
| P8 | **The excess did not shrink; it moved inward, deepened, and got further from the sites.** Exact maximum depth of the LP’s own dual: `1.096307560` at `(1.300943, 1.847007)` before the atoms (71 placements, 1,089,288 vertices, nearest of the 17,389 sites **`0.004230`** away), and `557273381/500000000 = 1.114546762` at `(1.294501, 1.843441)` after (56 placements, 496,848 vertices, nearest site **`0.007740`** away). Both witnesses are led by the `29°`-class tilted pair squares near `(1.389, 1.328)` and their mirror images — lane A3’s interior meeting of the tilted pair, not S2’s mid-wall sliver. Adding the atom columns pushed the excess **0.0035 further from the sampled sites and 0.018 deeper**. | EXACT |
| P9 | The dual at eleven is not a single object, and that matters for reading S2. The record’s `sites-1` dual — the `1/25`-integral, 35-row, 280-placement family this task was pointed at — came from a **warm** re-solve. The **cold** re-solve of the identical column set reaches a different vertex of the same optimal face (64 rows, 512 placements, no near-integral weight). Both have value eleven; the 19 small atoms separated from the `1/25` family are violated by the cold dual too (violations `0.044` to `0.184`), but all five K6 giants are satisfied by it, by `9.5` to `17.4`. The optimal face at `153/40` is wide, and a separation tuned to one of its vertices generalises only in part. | EXACT |
| P10 | A gap worth recording independently: **what the reader can separate is wider than what the pipeline can freeze.** The freeze path writes `atoms` (point atoms) and `threshold_atoms` (`ThresholdAtom.to_record()`), and `devtools.decide_threshold_certificate` parses exactly those. The two-of-three atoms are `ThresholdAtom`s and would freeze as they stand; the K5 clique atom carries multiplicities `(1, 2, 2, 1, 1)` at `t = 4`, and every K6 atom charges `floor(a(P)/t) > 1` on some cores — neither is expressible as a `ThresholdAtom`, so neither could be frozen into a certificate today even if it had moved the LP. Had the value dropped on a K5 or K6 column, the freeze-and-gate step the brief specifies would have had nothing to write. | RECORD |

**P10 is the blocker on turning any of this separation work into a bound**, and it is
carried as its own bead: the certificate format cannot express what the reader can
separate.

## 2. What was measured, and how

The driver is a scratch file, not a fork: it imports `load_family`, `read_arrangement`,
`two_of_three_maximum`, `clique_scan`, `cg_separation`, `shape_atom` and `verify_atom`
from `devtools.plateau_reader` unchanged and calls them itself, skipping the two places
`read_plateau` refuses a family — the explicit `verdict.max_depth > 1` return and the
`failures` filter below it, which keeps the K2 failure while dropping K3’s.

**Mask reduction, and why it is exact rather than a heuristic.** The family’s
arrangement carries **22,201 distinct membership sets** — far past what K4’s pair
enumeration or K6’s integer program can take.
Every charge in the module is nondecreasing in each point’s membership set, so replacing
a point by one whose membership set contains it never lowers a charge: the maximum is
attained on the sets **maximal under inclusion**, moving a K6 multiplier to a dominating
vertex cannot weaken its cut (the module docstring’s own argument), and a piercing
measure over dominating traces is at least as good.
There are **965** such sets, found in 0.7 s. Every atom returned is then re-verified
against the family geometrically, in rationals, by the reader’s own `verify_atom`.

**The LP.** The solver driver is a copy of the site loop with two additions:
`--seed-atoms`, which loads Chvátal–Gomory floor atoms, D4-expands them into orbits and
adds them as a third column block, and `--solve-only`, which stops after the first solve
and the dual dump. Floor-atom columns carry the same float geometry and the same
`COVER_SLACK` loosening `sepcore.atom_columns` uses: coefficient
`sum_images floor(a(P)/t)`, cost `|orbit| * floor(a(S)/t)` — the orbit’s budget, so the
column is priced exactly as a `ThresholdAtom` column is.
The generalisation is needed because the reader’s K5 and K6 return atoms with integer
multiplicities, which `ThresholdAtom` cannot carry; validity is the same one-line
argument, `sum_P floor(a(P)/t) <= floor(a(S)/t)` for disjoint cores, since the floor is
superadditive and disjoint cores have disjoint traces on `S`.

**The driver was validated against the record before it was trusted.** The control run
is the same driver with `--seed-atoms` absent, i.e. the unmodified site-loop code path
with a zero-width floor block: it reports `10.999999999999945` where the record’s
`sites-1` stage reports `11.000000071098183`. Both are eleven — the record’s is a warm
re-solve carrying its predecessor’s basis, this one a cold one — and the `7e-8` lane
A3’s S1 called solver tolerance is 300,000 times the `2.2e-13` the atoms then moved it
by.

**Which LP.** The re-solve resumes the record’s own `153/40` site checkpoint, trimmed to
its **`sites-1`** state (the first 2,250 site orbits = 17,389 sites, 2,566
threshold-atom orbits, 15,021 rows), because that is the LP whose dual *is* the
`1/25`-integral family.
The later rounds’ 600 extra site orbits are dropped: they would only lower the value
further, and they move the dual away from the object under study.

## 3. The outcome, in lane X1’s own terms

**Outcome 2: the LP stays at eleven and the dual relocates.** Not outcome 1 — nothing
was frozen, the two-route gate was not run, and no bound is claimed.
Not outcome 3 either: the family is emphatically *not* rank-one feasible apart from its
depth excess. Twenty-four distinct atom orbits cut it, and **every one of them by more
than its whole depth excess** of `28/25 - 1 = 3/25`: `33/100` for each of the 18
two-of-three orbits, `1/2` for the clique, and `5.545` to `8.27` for the five K6 giants.

So the reading, stated plainly: **the atom language is not what pins `3.825`.** Every
atom class the reader knows separates this dual, the separations are exact, the columns
are priced at their true budgets, and the restricted LP does not move by so much as a
solver tolerance.
The value at `153/40` on this column set is held at eleven by something
the rank-one point-atom language cannot express, and adding more of that language moves
the dual rather than the objective.

The corollary for the site chase is sharper than lane A3’s S4. S4 read the excess
retreating into a mid-wall sliver at `0.0006` per round and concluded that sites must be
placed by the sliver’s structure.
What P8 shows is that the excess is not pinned to that sliver at all: the LP has optimal
duals whose excess sits in the **interior**, at the `29°` tilted pair near
`(1.29, 1.85)`, `0.004` to `0.008` from any sampled site, and adding atoms moves it
there and deepens it.
Chasing the mid-wall sliver would have chased one vertex of a wide optimal face.

**That is the argument for generating sites by structure rather than by arrangement
vertex**, and it is carried as its own bead: vertex-by-vertex separation costs about 825
s a round, moves nothing, and the obstruction migrates between rounds.

## 4. Trajectory

| stage | object | result | wall |
| --- | --- | --- | ---: |
| probe | arrangement of the `1/25` family | 283,832 vertices, 22,201 masks, 965 maximal | 48 s |
| K0-K3 (bypassed at K2) | same | total 11, depth `28/25`, K0/K1/K3 hold | 36-45 s |
| K4 two-of-three | 965 maximal masks | max `133/100`, complete, 96 maximisers | 56 s |
| K5 budget-one atoms | 11,252-edge intersection graph | 1,080 maximal cliques above one, complete; heaviest rank-one `3/2`, `tau* = 7/4`; atom violation `1/2` | 29 s |
| K6 `t = 2` | 965 candidate points | violation `1109/200`, solver time-limited (bound `5.855`) | 94 s |
| K6 `t = 3` | " | violation `1421/200` (bound `7.97`) | 95 s |
| K6 `t = 4` | " | violation `1451/200` (bound `9.065`) | 95 s |
| K6 `t = 5` | " | violation `827/100` (bound `9.72`) | 96 s |
| K6 `t = 6` | " | violation `409/50` (bound `10.265`) | 94 s |
| LP control | `sites-1` resumed, no seeds | **`10.999999999999945`**, 64 dual rows, 11,881 it | 367 s total (matrices 54, model 14, LP 310) |
| LP seeded | same + 24 floor-atom orbits | **`11.000000000000167`**, 42 dual rows, floor support 0, 4,348 it | 226 s total (matrices 55, model 11, LP 168) |
| excess, control dual | 512 placements | depth `1.096307560`, nearest site `0.004230` | 200 s |
| excess, seeded dual | 336 placements | depth `1.114546762`, nearest site `0.007740` | 68 s |
| round 2, K4 (abandoned) | relocated dual: 48,013 masks, 1,705 maximal | killed inside the pair expansion | 4 min |
| round 2, K5 (abandoned) | same | killed inside the clique scan, no verdict | 14 min |

Two workers at a time throughout; the two oracle runs and the two LP runs each
overlapped one other job.
About 28 minutes of CPU in the measurement proper — 13 in separation, 10 in the two LP
solves, 4.5 in the two exact depth readings — plus 18 minutes spent on the abandoned
second round, and about 42 minutes of wall clock at two workers on 4 cores.
Lane X1 priced the measurement at twenty minutes end to end.
The measurement proper came in near that; what it did not budget for was the control
solve, which turned out to matter (P9), or the cost of separating a *generic* dual
rather than the `1/25`-integral one, which is what the abandoned second round measured
the hard way.

## 5. What the bypass does and does not license

The reader refuses a family above depth one at

```python
if verdict.max_depth > 1:
    return PlateauReport(verdict, None, f"depth {verdict.max_depth} exceeds one: ...")
```

and again at the `failures` filter below it, which drops only names starting with `K3`.
The scratch driver skips both.
It does **not** fork the reader: `read_arrangement`, `two_of_three_maximum`,
`clique_scan`, `cg_separation`, `shape_atom` and `verify_atom` are imported from
`devtools.plateau_reader` and called unchanged, so every exact search above is the
reader’s own code on the reader’s own data structures.

What survives the bypass:

- **Soundness of a violation.** Two-of-three, budget-one clique and rank-one floor atoms
  are valid for every packing, whatever family is used to find them.
  `verify_atom` decides charge and budget in rationals against the family.
  So “this dual violates this valid inequality by `v`” is exact, and the atom is a legal
  LP column at cost equal to its budget.
- **Completeness of the K4 and K5 searches** *as searches over this family*. The pair
  bound `y(T_i ∩ T_j) + min(y(T_i Δ T_j), D)` uses the arrangement’s own `D`, so it
  stays an upper bound at `D = 28/25`; the clique argument for K5 is about the
  intersection graph and does not use the depth at all.

What does not survive, and must never be quoted:

- **Any “feasible” verdict as a cap.** On a depth-one family, “no violated two-of-three
  atom exists” is a theorem that the two-of-three method stops at that side.
  Here it would mean only that one infeasible dual is not cut by that class.
  This report contains no such reading anyway — every class searched returned a
  violation — but the rule is the rule.
- **The docstring’s dismissal of repeated membership sets.** It argues a triple with a
  repeated set charges `y(T) <= D <= 1`. At `D = 28/25` that argument fails, and such a
  triple charges exactly the depth: a valid but uninteresting cut, because it *is* the
  point constraint at that vertex, which is what the site oracle already adds.
  K4 here searches distinct sets only, and its maximum `133/100` exceeds `28/25`, so
  nothing it found is a disguised point constraint.

## 6. What failed, and what was not done

- The three-of-five shape search (K4’s other shape) and the line-chord scan were not
  run. Line chords are a theorem only for depth-one families and would have decided
  nothing here; three-of-five is subsumed by K5’s complete decision for the budget-one
  class.
- Every K6 program hit its 90 s limit with an open gap, so the per-threshold optimum is
  unknown. Raising the limit was not worth it once the LP had not moved on cuts of
  violation `5.5` to `8.3`.
- The seeded LP was run once, on the union of all 24 orbits, rather than separately for
  the small atoms and the K6 giants.
  Attribution was recovered instead from the primal solution (all 24 at zero) and from
  the exact charges on the new dual (all 24 satisfied), which is stronger than two
  separate values would have been.
- The first launch of the K6 job died instantly on a shell quoting error that left a
  stray log in the repository root; it was deleted within the minute and `git status`
  re-checked. No tracked file was touched at any point.
- **A second separation round on the relocated dual did not finish in the budget, and
  the reason is worth recording as an instrument reading.** That dual has 336
  placements, 496,848 vertices, **48,013 distinct membership sets and 1,705 maximal
  ones** — nearly twice the `1/25` family’s 965 — and, because `family_from_dual` rounds
  weights at `1e-9`, its weights fall in hundreds of distinct classes rather than the
  `1/25` family’s fifteen.
  `MaskTable.weighted` costs one popcount pass per weight class, so both K4’s pair
  enumeration and K5’s piercing programs slow by more than an order of magnitude.
  K4 was killed after four minutes of pair expansion; K5 was relaunched alone and was
  killed after fourteen minutes of clique scan, without a verdict.
  **The `1/25`-integral dual is cheap to separate precisely because it is
  `1/25`-integral**; a generic vertex of the same optimal face is not.
  Anyone planning a separation *loop* here should budget for the generic dual, not for
  this one.

## 7. Uncertainties, and what would decide each

- **Is the plateau at eleven a plateau of the method or of these columns?** Unchanged
  and OPEN. Everything here is a restricted LP on one column set.
  The value bounds the true value from above at `153/40`, so eleven is not a lower bound
  on anything.
- **Does the atom language still separate the relocated dual?** OPEN, and it is the
  question a second round would answer: if it does, the loop is a treadmill (each round
  cuts a vertex and the dual walks to the next one at the same value); if it does not,
  the relocated dual is rank-one feasible apart from its `0.1145` depth excess and the
  whole obstruction is the sliver, which is lane X1’s third outcome arriving one round
  late.
- **Would the atoms bite with the sites?** Untested.
  The atoms were added to a fixed site set; a joint round — sites at the new interior
  witness `(1.294501, 1.843441)` *and* the atoms — is one warm re-solve away and is the
  obvious next measurement.
  P8 is the argument for it: the excess now sits `0.0077` from any site, which is more
  than a site round has ever had to close here.
- **Is the K6 optimum much larger than what was found?** OPEN. Every threshold was
  time-limited with a gap of `0.3` to `2.1`. But the direction of the evidence is that
  raw K6 violation is not the currency: the largest violation found, `8.27`, moved the
  LP by nothing, while a violation of `1/2` on a budget-one clique atom did the same
  nothing.
- **Do the K6 giants ever help?** They were satisfied by both cold duals by wide margins
  and carried zero weight.
  They are cuts tuned to one vertex of a wide face.
  A cut that only bites at one vertex of an optimal face cannot move the optimum, and
  this is a clean instance.
- **Is `1080` maximal cliques above weight one a large number for a depth-one family?**
  Not compared here. Lane X1’s survivor family reported 16 maximal cliques above one at
  depth exactly 1; this family has 1,080 at depth `28/25`. How much of that is the depth
  excess and how much is real structure is one reader run on a repaired depth-one
  version of this family away — and that repaired family is the object lane X1’s third
  outcome named.

## 8. Files

Retained beside this report:

- [`lane-a4-seed-atoms-k4k5.json`](lane-a4-seed-atoms-k4k5.json) — the 19 small violated
  atom orbits (18 two-of-three and the K5 clique atom), deduplicated on D4 orbit, as fed
  back to the LP.
- [`lane-a4-dual-153-40-control.json`](lane-a4-dual-153-40-control.json) — the dual of
  the control solve, 64 rows, before the atoms.
- [`lane-a4-dual-153-40-seeded.json`](lane-a4-dual-153-40-seeded.json) — the dual of the
  seeded solve, 42 rows, after the atoms.
  P7 is the comparison of these two files.
- The eight scripts, in the order the run used them:
  - [`lane-a4-probe-arrangement.py.txt`](lane-a4-probe-arrangement.py.txt) — builds the
    family’s arrangement and reports its size: the 283,832 vertices and 22,201 distinct
    membership sets of P1.
  - [`lane-a4-oracle-reader.py.txt`](lane-a4-oracle-reader.py.txt) — the driver this
    whole report rests on: `K4`, `K5` and `K6` run as separation oracles with the `K2`
    depth gate bypassed, on the 965 inclusion-maximal membership sets, every returned
    atom re-verified by the reader’s own `verify_atom`. P1 through P4 are its output,
    and its module docstring restates the warning above.
  - [`lane-a4-summarise.py.txt`](lane-a4-summarise.py.txt) — the compact tables of what
    the oracle reader found, as Section 1’s numbers were read off them.
  - [`lane-a4-flooratoms.py.txt`](lane-a4-flooratoms.py.txt) — the Chvátal–Gomory floor
    atom as an LP column: the `(S, a, t)` record, the superadditivity argument in its
    docstring, and a column builder using the same float geometry and `COVER_SLACK`
    loosening as `sepcore.atom_columns`.
  - [`lane-a4-split-seeds.py.txt`](lane-a4-split-seeds.py.txt) — splits the oracle
    reports’ violated atoms into seed files by source, deduplicated on D4 orbit; it
    produced the 19 small atoms and, separately, the five `K6` giants.
  - [`lane-a4-lp-atoms.py.txt`](lane-a4-lp-atoms.py.txt) — the solver driver of Section
    2: lane A3’s site loop plus `--seed-atoms`, which D4-expands floor atoms into a
    third column block priced at the orbit budget, and `--solve-only`. P6 and P7 are its
    output, and the control run is the same file with `--seed-atoms` absent.
  - [`lane-a4-charge-on-dual.py.txt`](lane-a4-charge-on-dual.py.txt) — the exact charge
    of each seeded atom on a dual family, so that violation is decided rather than
    inferred: the zero-of-24 reading in P7 and the 19-of-24 reading in P9.
  - [`lane-a4-excess-and-sites.py.txt`](lane-a4-excess-and-sites.py.txt) — exact maximum
    depth of a dual family, its witness, and the exact distance from that witness to the
    nearest LP site: P8.

The scripts are retained with a `.py.txt` extension, as
[lane X3](lane-x3-containment-atoms-do-not-cut.md) and
`agenda-032/unrun-independent-audit/` already do: they are scratch measurement scripts,
not importable project modules, and the repository’s Python surface is held at zero Ruff
and BasedPyright findings over every tracked `.py` file.
Their bytes are as delivered; nothing was reformatted.

They are **a record of how the measurement was made, not a supported tool.** Each was
run from a scratch directory against the repository at commit `7ccb679c`; five of them
put the repository on `sys.path` by its absolute path, and `lp_atoms.py` resolves the
scratch layout around it, including spike B’s `sepcore`, which is not retained.
`oracle_reader.py` deliberately bypasses a gate the supported reader enforces, which is
exactly why it must not be mistaken for the reader:
`packing/devtools/plateau_reader.py`, whose exact searches it calls unchanged, is the
supported instrument.
Nothing in the repository imports any of them, and nothing should.

Not retained (scratch only): the two oracle reports (`K4`/`K5` at 180 KB and `K6` at 2.7
MB), the five `K6` floor-atom seed files (1.3 MB — their violations, point counts,
budgets and charges are in P4 and every one carried primal weight zero), the two LP run
directories with their site, row and atom matrices and their primal vectors, the trimmed
`sites-1` checkpoint, the exact depth-and-nearest-site logs behind P8, the working
method note, and the two abandoned second-round jobs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
