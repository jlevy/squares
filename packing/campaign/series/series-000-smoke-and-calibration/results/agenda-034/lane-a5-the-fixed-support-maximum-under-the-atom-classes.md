# Agenda 034, lane A5: the fixed-support maximum under the atom classes, and how far it is from a cap

Retained measurement-lane report for
[X-024](../../../../explorations/X-024-two-lines-at-eleven.md), written by a sub-agent
on 2026-09-09, read-only on the repository at `claude/n-11-stronger-result-d730ds`. The
report is reproduced as delivered, with its own findings table and status labels; only
its file references were rewritten to say where each file now is.
X-024 carries the coordinator’s reading.

The question is X-024 slice A5’s in its sharpest form: **the family that caps the point
method at `191/50` — does it also cap the threshold method at `153/40` and `383/100`,
and if not, by how much does it miss?**

**Headline: `nu_S = 32/3` at both sides, exact, under depth-one plus the complete
budget-one class, falling to exactly `10` once the floor atoms are imposed.
So no cap at either side, and real room rather than a nearly-capped method.**

Retained beside this report: the two exact results with their tight rows and priced
duals, the two no-atom controls, the two `32/3` optima as ceiling records, the two
sharpening loops, and the ten scripts that produced them, listed under [Files](#files).
Not retained (scratch only): the clique census output with every `tau*` (0.4 s to
rebuild from the retained script), the reader’s verdicts on the two optima, and the
union-support working set’s rounds.

Labels: **EXACT** (decided in rational arithmetic by repository primitives), **CHECKED**
(float computation, script retained), **RECORD** (read from a retained file), **OPEN**.

## 0. Findings in one page

| # | Finding | Status |
| --- | --- | --- |
| F1 | **`nu_S(153/40) = 32/3 = 10.666…`** on the 88-placement support of the `153/40` ceiling family, under depth at most one at every arrangement vertex together with every budget-one rank-one atom inequality. Exact primal `32/3` on a family checked feasible on every row in `Fraction`s, exact dual bound `32/3` on four priced rows: primal meets dual, so this is the optimum, not a bracket. | EXACT |
| F2 | **`nu_S(383/100) = 32/3`**, the same number by the same route on the `383/100` ceiling family. | EXACT |
| F3 | **The shortfall is `11 - 32/3 = 1/3` at both sides**, and it is the whole cost of the atoms: with the atom rows dropped, the same program has optimum exactly `11` at both sides, so the uniform `1/8` family *is* an optimal solution of the point-method fixed-support program and the atom inequalities take exactly one third off it. | EXACT |
| F4 | **Neither side is capped.** `nu_S < 11` at both, so this support does not witness the plateau and the theorem’s hypothesis is not met here. A larger support could still reach 11; nothing below proves otherwise about the true maximum. | EXACT |
| F5 | The imposed atom family is **complete for every rank-one atom of budget one** — which includes every two-of-three and every three-of-five atom — by an inclusion argument given in §2, and independently confirmed: the plateau reader run on the optimum reports the complete two-of-three search at maximum exactly `1` and **zero** maximal cliques above weight one. | EXACT |
| F6 | It is **not** complete for atoms of budget two or more. The reader’s K6 separation finds violated Chvátal–Gomory floor atoms at the `32/3` optimum at both sides — `t = 2, 3, 4`, each verified exactly at violation `1/3`. Feeding them back and re-solving until the separator stops takes the support to **exactly `10` at both sides** (exact primal = exact dual on the final row set), so the optimum under the *whole* rank-one class is at most `10` and the shortfall is at least `1`. This only deepens the negative; it cannot rescue a cap. | EXACT (bound); OPEN (whether `10` is the optimum) |
| F7 | **One atom row does all the work.** The exact dual prices four rows: three depth rows (`u = 4`, `8/3`, `8/3`) and a single atom row at `u = 4/3` — the 10-member clique with `tau* = 3/2` the reader had already flagged on the uniform family at charge `5/4`. `4 + 8/3 + 8/3 + 4/3 = 32/3`. The clique is **central**, not a corner clique: six near-centre 0.79-degree squares with the 29.15- and 25.67-degree inner pairs, pierced by three points around `(1.81, 1.81)`, `(1.81, 1.22)`, `(1.22, 1.81)` against a container centre of `(1.9125, 1.9125)`. | EXACT |
| F8 | **The optimum abandons seven of the eleven orbits.** Uniform `1/8` on all 88 placements becomes `1/2` on two axis-aligned orbits (a wall square and a corner square), `1/4` on the 29.15-degree inner-corner orbit, `1/12` on the 0.79-degree near-centre orbit, and `0` on the other seven — including every 1.32-degree wall slot, the 0.26-degree corner pair and the 25.67-degree inner orbit. Orbit totals `4, 4, 2, 2/3`. | EXACT |
| F9 | Tying the weights over D4 orbits loses nothing (both row families are D4-invariant, so averaging preserves feasibility and objective), and the 88-column program agrees: its float optimum is `10.666666666666668` at both sides against the 11-column `32/3`. | EXACT (argument); CHECKED (88-column solve) |
| F10 | **Enlarging the support does not reach eleven either.** The union with the 280 placements of the `1/25`-integral plateau family (344 distinct, D4-closed, 43 orbits) has an exact dual bound of `21749/1980 = 10.9843… < 11` on a row set of valid inequalities, and the float continuation reaches `10.85`. Its *point*-method optimum is still exactly `11` (a depth-one family of weight 11 on 32 of the 344, verified by `verify_ceiling`), so again it is the atoms that cut. | EXACT (the bound); CHECKED (the continuation) |

## 1. The program

Fix the support — the 88 placements of the record, geometry only — and maximise
`sum_P y_P` over `y >= 0` subject to two row families.

**(D) Depth at most one.** One row `sum_{P in T} y_P <= 1` per distinct membership set
`T` of the arrangement cut by the placements’ edge lines and the four container walls.
This is complete for depth at *every* point of the container by the candidate-point
argument proved in the module docstring of
[`packing/devtools/plateau_reader.py`](../../../../../devtools/plateau_reader.py): every
charge here is nondecreasing in a point’s membership set, and every point’s membership
set is contained in some arrangement vertex’s.

**(C) Budget-one rank-one atoms.** One row `sum_{P in C} y_P <= 1` per maximal clique
`C` of the closed-intersection graph that is *not* contained in any membership set and
whose fractional piercing number satisfies `tau*(C) < 2`. §2 shows this family implies
every rank-one atom of budget one on this support, and that each of its rows is itself
such an atom (so no invalid row is imposed).

Both families are enumerated in full and both are weight-independent, so no separation
loop is needed for them and none was used.
Weights are tied over the D4 orbits: the support is D4-closed (11 orbits of 8, no
duplicate placement, checked exactly), both row families are D4-invariant, so averaging
an optimal solution over the group keeps feasibility and the objective and a symmetric
optimum exists. In orbit coordinates a row and all eight of its D4 images are literally
the same row, so the reduction also keeps the row set D4-closed automatically.

Floats propose, rationals decide, as in `polish_ceiling_family`: HiGHS solves the
11-column program, the optimum is rationalised and then checked against **every** row in
`Fraction`s (so its total is an exact lower bound on `nu_S`), and the solver’s duals are
rationalised and checked for `A^T u >= c`, `u >= 0` (so `sum u` is an exact upper
bound). Here the two meet, so `nu_S` is exact rather than bracketed — the
[lane M0](lane-m0-fixed-support-polish-191-50.md) discipline (its F1–F4) with the
degenerate case it hit not arising.

## 2. Why the atom rows are complete for budget one, and why that is not everything

An atom is `(S, a, t)` with integer multiplicities `a` on a finite point set `S`; its
Chvátal–Gomory floor form is `sum_P floor(a(P)/t) y_P <= floor(a(S)/t)` and it dominates
the threshold form. Call it a *budget-one* atom when `floor(a(S)/t) = 1`, that is
`t <= a(S) < 2t`. Every two-of-three atom (`|S| = 3, k = 2`) and every three-of-five
atom (`|S| = 5, k = 3`) is one.

1. **Its charged set is a clique, with every coefficient one.** If `a(P) >= t` and
   `a(Q) >= t` then `a(P) + a(Q) >= 2t > a(S)`, so `P` and `Q` hold a common point of
   `S` and are adjacent in the closed-intersection graph.
   And `a(P) <= a(S) < 2t` gives `floor(a(P)/t) = 1`. So the atom *is* the clique
   inequality `y(K) <= 1` for a clique `K` with `tau*(K) <= a(S)/t < 2`.
2. **Every clique is dominated by a row imposed here.** `K` lies in some maximal clique
   `M`. If `M` is contained in a membership set `T`, then `y(K) <= y(M) <= 1` is the
   depth row at `T`, which is in family (D). Otherwise `M` is one of the non-Helly
   maximal cliques, and at both sides **every one of them has `tau* < 2`** (measured
   below), so `y(M) <= 1` is in family (C) and `y(K) <= y(M) <= 1`.
3. **Conversely each imposed row is a genuine atom.** For a maximal clique `M` with
   `tau*(M) < 2`, the exact piercing measure `lambda` rationalises to integer
   multiplicities `a = lambda * t` with `a(S) < 2t`, the atom charges exactly `M` (the
   charged set is a clique containing the maximal clique `M`, hence equals it) at budget
   one. `plateau_reader.piercing_atom` builds it and `verify_atom` checks it against the
   family by exact containment; all rows pass.

So (D) + (C) imply every budget-one rank-one atom inequality on this support.
**They do not touch atoms of budget two or more** — the rest of the rank-one
Chvátal–Gomory closure of the point system, which is the reader’s K6 language.
That gap is stated as a gap in F6 and §7, and it is one-directional: imposing more valid
rows can only *lower* `nu_S`, so it can only widen the shortfall, never create a cap.

## 3. Exact numbers

Both records: `n = 11`, `B = 9977/10000`, the 181-direction net of the `191/50` run, 88
placements at uniform weight `1/8`, total weight exactly `11`, D4-closed in 11 orbits of
8 with no repeated placement.
They are the homothetic images of
[`ceiling-family-191-50.json`](ceiling-family-191-50.json) (centres scaled by `765/764`
and `383/382`).

|  | `L = 153/40` | `L = 383/100` |
| --- | --- | --- |
| arrangement vertices | 20,480 | 20,504 |
| distinct membership sets | 1,489 | 1,517 |
| depth rows after the orbit tie | 170 | 172 |
| closed-intersection graph | 744 edges | 744 edges |
| maximal cliques | 233 | 233 |
| non-Helly maximal cliques | 152 | 168 |
| their `tau*` | `3/2` (128), `5/3` (24) | `3/2` (120), `5/3` (40), `7/4` (8) |
| all `tau*` decided exactly | yes | yes |
| atom rows after the orbit tie (new) | 12 (9) | 12 (10) |
| program | 11 columns, 179 rows | 11 columns, 182 rows |
| **`nu_S`** | **`32/3`** | **`32/3`** |
| exact primal / exact dual | `32/3` / `32/3` | `32/3` / `32/3` |
| shortfall `11 - nu_S` | **`1/3`** | **`1/3`** |
| same program without the atom rows | `11` | `11` |
| 88-column float control | `10.666666666666668` | `10.666666666666668` |
| wall time | 3.0 s | 3.1 s |

Every `tau*` was decided exactly — a float proposal certified by an exact primal–dual
pair, or the exact rational simplex — so the classification of the 152 (168) cliques as
budget-one atoms rests on no float.

## 4. The optimum, and where the weight goes

The optimal weight vector is identical at both sides (the families are homothetic and
the whole row structure transports):

| orbit | uniform | optimum | orbit total | tilt (folded) | representative centre at `153/40` | position |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | `1/8` | **`1/2`** | `4` | `0.000` | `(3.3255, 2.3265)` | wall, `B` inside the right wall |
| 7 | `1/8` | **`1/2`** | `4` | `0.000` | `(3.3255, 0.4995)` | corner |
| 5 | `1/8` | **`1/4`** | `2` | `29.152` | `(2.4985, 1.3887)` | inner-corner tilted square |
| 4 | `1/8` | **`1/12`** | `2/3` | `0.791` | `(1.5163, 1.5251)` | near-centre |
| 0 | `1/8` | `0` | `0` | `0.000` | `(3.3180, 2.2655)` | wall |
| 1 | `1/8` | `0` | `0` | `0.000` | `(0.5070, 0.5520)` | corner |
| 2 | `1/8` | `0` | `0` | `1.318` | `(1.5099, 0.5168)` | wall slot |
| 3 | `1/8` | `0` | `0` | `1.318` | `(1.5346, 3.3081)` | wall slot |
| 8 | `1/8` | `0` | `0` | `0.264` | `(3.3231, 3.3203)` | corner |
| 9 | `1/8` | `0` | `0` | `25.668` | `(2.4792, 1.3925)` | inner-corner tilted square |
| 10 | `1/8` | `0` | `0` | `0.000` | `(0.5000, 3.3250)` | corner |

`8 x (1/12 + 1/4 + 1/2 + 1/2) = 32/3`. The redistribution is not a gentle reweighting:
it **empties seven of the eleven orbits** and doubles two.
What survives is the axis-aligned skeleton (a wall square and a corner square at `1/2`)
plus one tilted inner-corner orbit at `1/4` and a whisker of the near-centre orbit at
`1/12`. Every 1.32-degree wall slot, the 0.26-degree corner pair and the 25.67-degree
inner orbit — the near-mirror partners of the orbits that survive — go to zero.
Those near-duplicate pairs are exactly what the clique inequalities forbid: two
almost-coincident squares can both carry `1/8` under depth alone but not under a clique
budget of one.

**Tight rows.** 28 rows are tight at the optimum: 25 depth rows and 3 atom rows.
The three tight atom rows, as orbit-coefficient vectors, are `[0,0,0,0,6,2,0,0,0,2,0]`
(10 members), `[0,2,0,0,0,2,1,0,2,0,0]` (7 members) and `[0,2,1,0,0,2,1,0,0,2,0]` (8
members). The same three at both sides.

**The dual, which is the certificate.** Four rows carry positive multiplier, at both
sides:

| row | multiplier | orbit coefficients | a point carrying it (at `153/40`) |
| --- | --- | --- | --- |
| depth | `4` | `[0,2,0,0,0,0,0,2,2,0,2]` (8 placements) | `(2.8266, 2.8266)`, one `B`-side in on the corner diagonal |
| depth | `8/3` | `[1,0,1,1,0,2,1,0,0,2,0]` (8 placements) | `(0.8045, 1.4178)` |
| depth | `8/3` | `[2,0,2,2,0,0,2,0,0,0,0]` (8 placements) | `(0.0271, 1.9125)`, on the left wall at mid-height |
| **atom** | `4/3` | `[0,0,0,0,6,2,0,0,0,2,0]` (10 placements) | central clique; pierced at `(1.8138, 1.8138)`, `(1.8057, 1.2236)`, `(1.2236, 1.8057)` |

`4 + 8/3 + 8/3 + 4/3 = 32/3`. **Exactly one atom row is priced**, and it is the clique
the reader had already named on the uniform family.
The support has exactly one D4 orbit of 10-member cliques (8 cliques, every one with
`tau* = 3/2`), and this is it: the reader reports “heaviest rank-one clique: 10 members,
weight 5/4, `tau*` 3/2” — charge `5/4` against budget `1`, exact violation `1/4`. That
single clique orbit, at multiplier `4/3`, is the whole of the `1/3` the atoms cost.

Clique sizes against `tau*` at `153/40`, over the 152 non-Helly maximal cliques: size 7
— 80 at `3/2`, 16 at `5/3`; size 8 — 32 at `3/2`, 8 at `5/3`; size 9 — 8 at `3/2`; size
10 — 8 at `3/2`. Nothing reaches 2, which is why the whole budget-one class collapses to
these 152 rows.

The priced clique is worth naming, because it is **not** the corner clique that
[lane M0](lane-m0-fixed-support-polish-191-50.md) found binding at `191/50` (its F7:
eleven entries at a container corner).
Here it is central: its ten members are the six D4 images of the 0.79-degree near-centre
square together with the 29.15- and 25.67-degree inner-corner pairs, all sitting between
`(1.32, 1.32)` and `(2.31, 2.31)` around a container centre of `(1.9125, 1.9125)`, and
its exact piercing measure of mass `3/2` sits at `(1.8138, 1.8138)`, `(1.8057, 1.2236)`
and `(1.2236, 1.8057)`. The corner cliques are present (the `u = 4` depth row is a
corner-diagonal point of depth 8) but they are carried by the depth constraint, not by
an atom.

## 5. Independent verification of the optimum, and what lies past budget one

The `32/3` optimum was written out as a ceiling record (32 placements, the four
surviving orbits) and read by the unmodified
[`packing/devtools/plateau_reader.py`](../../../../../devtools/plateau_reader.py).
Both sides give the same verdict:

- `verify_ceiling`: total `32/3`, **maximum depth exactly `1`** over 3,104 vertices.
- **K4 two-of-three: maximum exactly `1`, complete** over all triples of distinct
  membership sets (241 sets, 16,560 pairs expanded, complete by the exact pair bound).
  No two-of-three atom is violated.
- **K5 budget-one atoms: `0` maximal cliques above weight one**, so no budget-one atom
  is violated — complete, by the same clique argument.
  This is the independent confirmation of §2: the rows imposed really did close the
  whole budget-one class.
- K4 three-of-five: nothing found (branch and bound to the 200,000-node limit, plus an
  integer program reporting no violated cut — a solver claim, not a theorem; the
  complete decision for that shape is K5’s, and K5 is clean).
- Line chords: never violated (theorem); tight on 8 of the 12 direction/threshold pairs.
- **K6: violated.** Rank-one Chvátal–Gomory floor atoms at `t = 2` (5 points,
  `a(S) = 5`, budget 2, floor charge `7/3`), `t = 3` (7 points, `a(S) = 11`, budget 3,
  floor charge `10/3`) and `t = 4` (12 points, `a(S) = 23`, budget 5, floor charge
  `16/3`) — each verified exactly, each at violation exactly `1/3`.

So `32/3` is the optimum under depth and the budget-one class, and the *whole* rank-one
class cuts it further.
Pushing that with the reader’s own separator — add every atom it verifies as a row on
the 88-placement support (coefficient `floor(a(P)/t)` per placement, right-hand side
`floor(a(S)/t)`), re-solve, repeat — the sequences are

- `153/40`: `32/3 -> 32/3 -> 180/17 -> 180/17 -> 180/17 -> 116/11 -> 10`, seven rounds,
  196 rows (170 depth, 9 budget-one clique, 17 Chvátal–Gomory floor rows of budget 2 to
  9). **The separator is then exhausted**: at `10` the reader finds no violated atom of
  any class it can decide — two-of-three complete at maximum `1`, zero cliques above
  weight one, and nothing from the K6 integer programs at `t = 2, 3, 4` within 60 s
  each.
- `383/100`: `32/3` for six rounds, then `21/2 -> 31/3 -> 72/7`, ten rounds (the loop’s
  round limit). Its last round separated three more atoms that were never re-solved
  against, so the final 208-row set was rebuilt and re-solved separately: it gives
  **`10`** as well. Different atoms, same destination.
  The separator was **not** run to exhaustion here — the round limit stopped it — so
  more cuts may exist and the value may fall further.

**Both sides land on exactly `10`**, and both are certified: on the final row set the
exact feasible primal and the exact dual bound agree at `10`.

Read that as: **the fixed-support optimum under the whole rank-one class is at most `10`
at both sides** — EXACT, since every imposed row is a valid inequality and so the
program’s value bounds the true optimum from above.
Whether it is exactly `10` is **OPEN**: the K6 separator is a time-limited integer
program over `t = 2, 3, 4`, and its silence (at `153/40`) or its interruption (at
`383/100`) is not a theorem.

The shortfall therefore reads **`1/3` for the complete budget-one class, and `1` on the
strongest row set measured**: eleven becomes ten.
On the scale that matters that is not “a few hundredths”; **there is real room, and the
barrier to a threshold certificate at these sides is not this family.**

## 6. Enlarging the support: the union with the 1/25 plateau family

The `1/25`-integral plateau family
([`lane-a3-family-153-40-sites-round1-exact25.json`](lane-a3-family-153-40-sites-round1-exact25.json))
is **not** a depth-one family — `verify_ceiling` refuses it at maximum depth `28/25`
(its own retained log says so), so only its *placements* were taken.
Union of the two supports at `153/40`: `88 + 280 = 344` distinct placements (24 of the
280 coincide with ceiling placements), D4-closed, 43 orbits of 8.

The union program was run as a working set, the way `polish_ceiling_family` runs one,
but with the depth check on the arrangement of the *active* support — the placements the
current solution actually uses — which `verify_ceiling` decides completely and which is
two orders of magnitude smaller than the union’s own arrangement.
Rows are added from the vertices where the incumbent’s depth exceeds one and from every
atom the plateau reader verifies on the incumbent.
Every row is valid, so the value at every round is an upper bound on the union’s
fixed-support optimum.

| round | rows | float value | **exact dual bound** | active placements | note |
| --- | --- | --- | --- | --- | --- |
| 0 | 535 | `11.6667` | `25/2` | 64 | depth `4/3`: not yet feasible |
| 1 | 560 | `11.0` | `11` | 32 | `verify_ceiling`: total exactly `11`, **depth exactly 1** — a genuine point-method ceiling on the union support |
| 2 | 565 | `10.9487` | **`21749/1980 = 10.98434…`** | 80 | five atom rows added; **below eleven** |
| 3-5 | 573-583 | `10.92` | (rationalisation failed) | 56-72 |  |
| 6-7 | 588-589 | `10.8495` | (rationalisation failed) | 72-80 | run cut off by its own wall-clock limit before the row dump |

**The union does not reach eleven.** `21749/1980 < 11` is an exact dual bound on a row
set every one of whose rows is a valid inequality, so it bounds the union’s
fixed-support optimum from above: `nu_S(union) <= 21749/1980 = 10.9843…`, and the
uncertified continuation puts it at or below `10.85`. Since the union contains the
ceiling support, `32/3 <= nu_S(union) <= 21749/1980`. (The dual rationalisation failed
on the later rounds and the run was cut off by its wall-clock limit before dumping its
rows, so those rounds are float-only; the round-2 certificate is what carries the claim,
and it suffices.)

Two readings worth keeping.
First, the union’s *point*-method optimum is still exactly eleven — round 1 is a
depth-one family of total weight `11` on 32 of the 344 placements, verified by
`verify_ceiling` — so the enlargement does not break the point cap; it is the atoms that
cut, again. Second, the enlargement does raise the answer (it must: a larger support can
only help) but not to eleven.
Note the row sets are not comparable in strength — on the 88-placement support the
*whole* budget-one class is imposed, on the union only the rows the separator produced —
so the union’s own optimum is bracketed loosely, `32/3 <= nu_S(union) <= 21749/1980`,
and could be anywhere in that interval.
What is decided is the only thing that matters here: it is **not** eleven.
Column generation on this pair of supports is not the missing ingredient.

## 7. Exactly which inequalities were imposed, and which were not

**Imposed, and complete for their class:**

- Depth at most one, at every point of the container.
  Enforced at every distinct membership set of the full arrangement — 1,489 sets at
  `153/40`, 1,517 at `383/100` — complete by the candidate-point argument (PROVED,
  `plateau_reader` module docstring).
- Every rank-one atom of budget one: `y(C) <= 1` for all 152 (168) non-Helly maximal
  cliques, each with `tau*` decided exactly and each below 2. Complete by the inclusion
  argument of §2, and independently confirmed by the reader at the optimum (K4
  two-of-three complete at maximum 1; zero maximal cliques above weight one).
  This class contains **all two-of-three atoms and all three-of-five atoms**, so the K4
  searches’ results are subsumed rather than approximated.

**Not imposed:**

- Rank-one atoms of budget two or more — the rest of the Chvátal–Gomory rank-one closure
  of the point system (the reader’s K6 language).
  Not imposed in the `32/3` program; a further 17 of them, separated by the reader’s own
  time-limited integer programs at `t = 2, 3, 4`, were imposed in the sharpening loop of
  §5, which is where the value falls to `10`. That separator is bounded: its silence at
  `10` is a solver’s claim within its thresholds and its 60-second budget, not a
  theorem, so `10` is an exact upper bound and not a proved optimum.
- Line-chord (collinear, continuum) atoms.
  Not needed: a depth-one family can never violate one (theorem, `plateau_reader`
  docstring), and the reader confirms slack or tightness but no violation at every
  optimum measured here.
- Anything of Chvátal rank two or above, and any cut outside the point system.
  Out of the method’s language, and out of scope.

**Why the gap is harmless here.** Adding valid rows can only lower a maximisation’s
value. `nu_S = 32/3 < 11` is therefore already decisive for the negative direction, and
every row not imposed can only push it further down.
The gap would matter only for a *cap* claim — `nu_S >= 11` — and no such claim is made
at either side. **No cap is established.**

## 8. Method

The tool is an extension of a **copy** of
[`packing/devtools/polish_ceiling_family.py`](../../../../../devtools/polish_ceiling_family.py),
taken unmodified; the tracked file was not touched.
The copy was compared byte for byte when the code was retained and is **identical** to
the tracked file as committed at `7ccb679c` — the commit that added the tool, made just
over an hour after the copy was taken from the then-uncommitted working tree — so the
copy itself is not retained: it holds nothing the repository does not already carry.
The extension is a separate module, [`lane-a5-cap-lp.py.txt`](lane-a5-cap-lp.py.txt),
which imports `placement_orbits` from the tracked tool and rebuilds the program around
the atom rows. It reuses the repository’s own primitives throughout:
`plateau_reader.read_arrangement` for the exact arrangement and its membership sets,
`plateau_reader.intersection_graph` / `piercing_number` / `piercing_atom` /
`verify_atom` for the clique atoms, `polish_ceiling_family.placement_orbits` for the D4
tie, and `sqpack.fractional.ceiling.verify_ceiling` (through the reader) for the depth
verdict. Run as `packing/.venv/bin/python3` (Python 3.14) from `packing/`, never the
`python3` on `PATH`. At most two worker processes at a time.

## 9. Timings and what did not work

| step | time |
| --- | --- |
| arrangement + membership sets (88 placements, 20k vertices) | 0.9-1.1 s |
| all 233 maximal cliques (Bron–Kerbosch, no weight prune) | 0.03 s |
| `tau*` on 152 non-Helly cliques, all exact | 0.4 s |
| the `nu_S` program end to end, per side | ~3 s |
| the reader on the `32/3` optimum (32 placements, K6 included) | 6.9 s |
| the K6 sharpening loop at `153/40`, 7 rounds to `10` | ~9 min |
| the K6 sharpening loop at `383/100`, 10 rounds to `10` | ~18 min |
| the union working set, 344 placements, to the certified bound | 25 s (round 2) |
| re-solving and certifying a final row set exactly | ~3 s |

Four things went wrong and are worth recording.

- The first exact primal rebuild accepted the **zero vector**: it checked feasibility
  but not the objective, and `y = 0` is feasible.
  Fixed by targeting the exact dual bound and keeping the best feasible rationalisation,
  with a tight-row Gaussian rebuild behind it.
  **A feasibility check is not an optimality check.**
- Rationalising the dual is not always possible at a small denominator: two rounds of
  the sharpening loop (and one union round) returned a valid but weak bound (`11`, `12`)
  rather than the float optimum.
  Those rounds are reported as they came; the rounds that matter (`32/3`, `116/11`,
  `10`, `21749/1980`) all closed exactly.
- The `1/25`-integral plateau family is not a depth-one family (`verify_ceiling` refuses
  it at depth `28/25`). Only its placements were used.
  Reading it as a family would have been a category error.
- The certified union run was cut off by its own wall-clock limit inside a reader call
  and never wrote its row dump, so the later union rounds have float values but no exact
  certificate. The round-2 certificate (`21749/1980`) is what the claim rests on, and it
  is enough: it is already below eleven.
  Dump the rows *before* the deadline check, not after the loop.

## 10. Verdict

The question was whether the family that caps the point method also caps the threshold
method, and if not, by how much it misses.

**It misses, at both sides, by exactly one third under the complete budget-one class,
and by one under the strongest row set measured.**

- `nu_S(153/40) = 32/3` — **EXACT**.
- `nu_S(383/100) = 32/3` — **EXACT**.
- `11 - nu_S = 1/3` at both — **EXACT**.
- Under the whole rank-one class: `<= 10` at both sides — **EXACT** as a bound, with
  `10` attained; whether it is the optimum is **OPEN** (bounded K6 separator).
- **Neither side is capped.** No threshold certificate is ruled out at `153/40` or at
  `383/100` by this family.
  The theorem’s hypothesis — a depth-one family satisfying every rank-one threshold-atom
  inequality with total weight at least 11 — is **not** met on this support, and the
  branch should not stop pushing either side on this evidence.

The shortfall is not a rounding error and it is not a few hundredths.
`1/3` is the cost of the budget-one atoms alone; adding the floor atoms takes the
support to `10`, a shortfall of `1` out of `11`. The support that saturates the point
method at exactly 11 keeps `10.67` of it once the cliques are charged and `10` once the
floor atoms are, and the obstruction is concrete and local: **a single D4 orbit of
10-member central cliques** with `tau* = 3/2`, on which the uniform family carries `5/4`
against a budget of `1`.

Enlarging the support does not rescue it either: the union with the `1/25` plateau
family’s 280 placements (344 distinct, 43 orbits) is bounded above by
`21749/1980 = 10.984… < 11`, exactly.
So on the supports measured here the barrier is not column generation — it is that the
atoms genuinely bite, and biting is what a certificate needs them to do.

This is the complement of [lane A4](lane-a4-separating-the-plateau-dual-at-153-40.md)’s
reading and it points the same way.
A4 says the restricted LP at `153/40` does not move when every atom the reader can find
is added as a column; A5 says the family that would have explained that as a cap does
not reach eleven under those same atoms.
Neither side is capped, and what holds the LP at eleven is the site set rather than the
atom language.

## Files

Retained beside this report:

- [`lane-a5-nu-153-40.json`](lane-a5-nu-153-40.json) and
  [`lane-a5-nu-383-100.json`](lane-a5-nu-383-100.json) — the two `32/3` results, each
  with its tight rows and its priced dual.
  F1, F2, F7 and §4 read from these.
- [`lane-a5-noatoms-153-40.json`](lane-a5-noatoms-153-40.json) and
  [`lane-a5-noatoms-383-100.json`](lane-a5-noatoms-383-100.json) — the same program with
  the atom rows dropped, optimum exactly `11`. This is F3’s control.
- [`lane-a5-nu-optimum-153-40.json`](lane-a5-nu-optimum-153-40.json) and
  [`lane-a5-nu-optimum-383-100.json`](lane-a5-nu-optimum-383-100.json) — the two `32/3`
  optima written as ceiling records, which is what the unmodified plateau reader was
  then pointed at in §5.
- [`lane-a5-k6-loop-153-40.json`](lane-a5-k6-loop-153-40.json) and
  [`lane-a5-k6-loop-383-100.json`](lane-a5-k6-loop-383-100.json) — the sharpening
  sequences of §5 and every atom each round added, down to `10`.
- The ten scripts:
  - [`lane-a5-cap-lp.py.txt`](lane-a5-cap-lp.py.txt) — the `nu_S` program itself, and
    the extension §8 describes: the fixed-support maximisation under the depth rows and
    the complete budget-one atom rows, solved in floats, rebuilt exactly in `Fraction`s
    and closed against an exact rational dual bound.
    F1, F2, F3, F7 and F8 are its output.
  - [`lane-a5-tau-scan.py.txt`](lane-a5-tau-scan.py.txt) — the clique census the atom
    rows are built from: every maximal clique by Bron–Kerbosch with no weight prune, the
    Helly test, and exact `tau*` on every non-Helly clique.
    The 233 and 152 of §9 are its counts.
  - [`lane-a5-orbits.py.txt`](lane-a5-orbits.py.txt) — checks that each ceiling family
    is D4-closed and reports its orbit sizes and distinct weights, which is the fact
    F9’s averaging argument needs.
  - [`lane-a5-build-optimum.py.txt`](lane-a5-build-optimum.py.txt) — writes an optimum
    as a ceiling record and describes the redistribution off `1/8`, so that the
    unmodified reader could be pointed at it in §5.
  - [`lane-a5-diagnose.py.txt`](lane-a5-diagnose.py.txt) — where the tight and priced
    rows sit and where the weight goes: §4 and the central clique of F7.
  - [`lane-a5-k6-loop.py.txt`](lane-a5-k6-loop.py.txt) — the sharpening loop of §5:
    solve exactly, rebuild the optimum as a family, run the plateau reader on it, turn
    every violated floor atom into a row on the full support, repeat.
    F6’s descent to exactly `10` at both sides is its output.
  - [`lane-a5-final-family.py.txt`](lane-a5-final-family.py.txt) — writes the last
    family of a `K6` loop as a ceiling record, for a deeper reader pass over it.
  - [`lane-a5-certify-k6.py.txt`](lane-a5-certify-k6.py.txt) — reconstructs a loop’s
    final row set and bounds it with an exact rational dual, which is what makes F6’s
    `10` an exact upper bound rather than a float reading.
  - [`lane-a5-union-support2.py.txt`](lane-a5-union-support2.py.txt) — the union working
    set of §6 on the 344 placements: the round loop with an exact dual bound taken each
    round.
  - [`lane-a5-certify-union.py.txt`](lane-a5-certify-union.py.txt) — certifies the union
    program’s value on the row set the working set closed on: F10’s `21749/1980` rests
    on it.

The scripts are retained with a `.py.txt` extension, as
[lane X3](lane-x3-containment-atoms-do-not-cut.md) and
`agenda-032/unrun-independent-audit/` already do: they are scratch measurement scripts,
not importable project modules, and the repository’s Python surface is held at zero Ruff
and BasedPyright findings over every tracked `.py` file.
Their bytes are as delivered; nothing was reformatted.

They are **a record of how the measurement was made, not a supported tool.** Each was
run from a scratch directory against the repository at commit `7ccb679c`, and every one
hard-codes the absolute scratch path twice over: its own directory, so that `cap_lp` can
be imported, and lane A3’s run directory, where the two ceiling families were read from.
Nothing in the repository imports any of them, and nothing should.
`cap_lp.py` is the one that could become a tool; promoting it needs its own tests and
review, and is carried as `think-p1sf` rather than done here.

Two earlier versions were superseded during the run, checked rather than assumed, and
are not retained:

- `union_support.py`, superseded by `union_support2.py`. The later file is the earlier
  one plus an exact rational dual bound taken every round and a row dump, and F10’s
  `21749/1980` is read from the later file’s output.
- `cliques.py`, superseded twenty-three seconds later by `tau_scan.py`. The later file
  keeps the same Bron–Kerbosch enumeration and Helly test, drops the diagnostic prints,
  and adds the exact `tau*` and the JSON census the atom rows are built from.

Also not retained: `show_record.py`, a pretty-printer for the fields of a ceiling
record, which stands behind no finding; and `polish_copy.py`, the 39 KB copy §8
describes, which is byte-identical to the tracked
`packing/devtools/polish_ceiling_family.py` at `7ccb679c`, is imported by none of the
ten retained scripts — the ones that need `placement_orbits` import the tracked module —
and would duplicate tracked code and nothing else.

Not retained (scratch only): the clique census output with every `tau*` (0.4 s to
rebuild from `lane-a5-tau-scan.py.txt`), the unmodified reader’s two verdict reports on
the `32/3` optima and their logs, and the union working set’s rounds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
