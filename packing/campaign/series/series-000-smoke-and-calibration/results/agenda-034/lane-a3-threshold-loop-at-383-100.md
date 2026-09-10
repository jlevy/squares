# Agenda 034, lane A3: the threshold loop at 383/100, and where it plateaus

Retained measurement-lane report for
[X-024](../../../../explorations/X-024-two-lines-at-eleven.md), written by a Fable
sub-agent on 2026-09-09, read-only on the repository at
`claude/n-11-stronger-result-d730ds`. The report is reproduced as delivered, with its
own status labels and both of its addenda; only its file references were rewritten to
say where each file now is, and the site-run trajectory table, which the delivered text
left as a placeholder, is rendered here from the run’s own `trajectory.json`. X-024
carries the coordinator’s reading.

**Nothing here is a bound and nothing here is a registered round.** No frozen file was
produced and the gate was never run: the LP value never went below eleven, so there was
nothing to freeze.
The one statement with a sign is negative (F1): on this column set the
method does not reach `383/100`.

Retained beside this report: the plateau duals, the `1/25`-integral family the site
chase produced, the plateau-reader verdicts, the three trajectories and the five driver
scripts, listed under [Files](#files).
The LP checkpoints (`sites.json`, `atoms.json`, `rows.json`, `x.npy`, `duals.npy`,
together about 60 MB), the symmetrised families above 150 KB and the run logs are not
retained (scratch only).

Labels: EXACT (a rational decision by a repository primitive), CHECKED (a float LP or
sweep reading), RECORD (retained files), OPEN.

## 1. Findings

| # | Finding | Status |
| --- | --- | --- |
| F1 | On the accepted `191/50` columns scaled to `L = 383/100` (1,950 site orbits, 2,566 two-of-three atom orbits; `B = 9977/10000`, 181 directions), the covering LP under the 15,021 carried rows alone has value **`11.017916787`** (HiGHS, 6,676 iterations, 100 s; reproduced to the digit on the resumed run). Every carried row passed the exact centre-domain check, so each is a constraint the full placement set imposes: the rows-complete value of this column set is at least this, and **no threshold certificate exists on the scaled `191/50` site and atom set at `383/100`**. The plateau the theory lane expected (its F5) is confirmed, `0.018` above eleven rather than at it. No sweep was needed for this reading and none was run; no completeness claim is made. | CHECKED (LP float); the admissibility of every row EXACT |
| F2 | The plateau dual (117 rows, total `11.017916787`, D4-symmetrised to 936 placements of total `1377239541/125000000`) is **not a fractional packing of the plane**: the plateau reader decides K0, K1, K3 in its favour and refuses it at K2 with exact maximum depth **`56217397/50000000 = 1.124347940`** over 4,202,976 arrangement vertices, at `(0.41722, 0.99953)`, where 47 placements meet: the corner square, the `0.26°` corner squares and the square above them in the corner column. It is the seam between the corner square and its upper neighbour; the nearest site of the scaled `191/50` set is `0.019` away. So the value `11.018` is the restricted LP’s and not a ceiling for any method at `383/100`; site separation, which the brief withholds, would cut this dual at once. | EXACT (`lane-a3-reader-383-100-round0.json`, 630 s) |
| F3 | One round of two-of-three atom separation (spike B’s interior-vertex generator, `vertex_cap = 24`, run on the 52 rows of dual weight at least `0.05`, 416 placements; Section 3 for why) finds **803 violated orbits**, top charge `244252553/200000000 = 1.2213` against budget 1 on the restricted weights and `1.2963` under the full dual (all 400 added orbits violated by it, CHECKED on the coefficient matrix); after adding 400 as columns the LP re-solves to **`11.017916784`** (24,677 warm iterations, 234 s): a move of `3e-9`. The dual relocates (129 rows, 46 in common with the old support, `L1` move `11.4` of a total `11.0`) and satisfies all 400 new columns with maximum charge-to-cost ratio exactly `1.0`; the new atoms carry no primal weight. **The plateau is robust to one round of two-of-three cuts on these sites.** The value did not drop below eleven, so by the brief no site separation was run. | CHECKED |
| F4 | Both plateau duals are fractional and interior: no weight within `1e-6` of an integer; weights from `0.0009` to `1.46` (`1.74` after the atom round), median `0.04`, the eleven heaviest carrying `5.5` (`5.2`); 81 (76) of the 181 directions in the support. No row centre lies exactly on its direction’s wall line (rows are snapped placements; the smallest gap is `0.0013`, the axis and `0.26°` wall squares up to snapping). Weight by class: axis `5.86` (`5.95`), the `25°`-`35°` class `2.33` (`2.46`), other `2.83` (`2.60`); by angle `0.26°` leads (`2.34`, `2.28`), then `0°`, `1.05°`, `29.89°`. The tilted `29°` rows sit `0.6`-`0.9` inside the centre domain. This is not the near-integral 9-14-row family of the `191/50` refills; it is a wide optimal face (F3’s relocation at equal value). | RECORD (`lane-a3-dual-383-100-round0.json`, `lane-a3-dual-383-100-round1.json`) |
| F5 | Slope on the fixed column set: from `10.967300462` at `u = L/B = 3.828806` to `11.017916787` at `u = 3.838829`, **`5.05` per unit of `u`** (`5.06` per unit of `L`), `0.37` of the point LP’s floor of `13.6` (theory F5); the linear crossing of eleven is `u = 3.83528`, `L = 3.82646`. The restricted value bounds the true value from above at every side, so reaching `3.83` needs columns the loop did not have (F2 names the missing ones) to be worth at least `0.018`. The linear model itself is superseded by the addendum (A1): the measured value at `3.825` is already eleven, so the restricted value is concave in the side and its crossing lies at or below `3.825`, inside F5’s `3.822`-`3.825` window after all. | CHECKED arithmetic on CHECKED values; not a bound |
| F6 | The dual after the atom round (129 rows, 1,032 placements, total `1377239531/125000000`) is refused by the reader at K2 as well: exact maximum depth **`561637353/500000000 = 1.123274706`** over 5,018,736 vertices, at `(0.99831, 0.99901)`, the far corner of the corner square, where 69 placements meet (the `0.26°` corner squares at `(0.5028, 0.5054)` with `0.218` each, the axis corner squares at `(0.5002, 0.5002)` and `(0.5007, 0.5007)`). The atom round relocated the dual but left the same corner-seam excess of `0.12`: the site gap, not the atom family, carries the plateau. | EXACT (`lane-a3-reader-383-100-round1.json`, 900 s) |
| F7 | Whether the two-of-three method with its own sites and atoms reaches `383/100` is undecided: the loop tested the fixed columns (closed: no) and one atom round (closed: no move), not site separation. The next measurement is named by F2: add the seam vertices of the plateau dual as sites (the reader’s depth witnesses), complete rows, and read the dual again. | OPEN |

## 2. What was measured, and how

The driver maps the accepted `191/50` checkpoint (spike B’s resume run: 15,085 sites in
1,950 D4 orbits, 2,566 two-of-three atom orbits, 15,021 rows, the rows-complete `x`)
into the `383/100` container by the homothety `q -> (383/382) q`. The scaled site orbits
and atom orbits are asserted to be D4 orbits at the new side (the homothety commutes
with the container’s D4 group); every scaled row centre passes the exact check
`e <= c' <= L' - e` in both coordinates (`e = B(cos + sin)/2`), so all 15,021 rows are
carried and none dropped.
`B` and the net are unchanged.
The scaled `191/50` weights violate 1,880 of the carried rows (least LP-coefficient
charge `0.6888`): the container grows under fixed `B`-squares.

The covering LP (site-orbit columns at cost `|orbit|`, atom-orbit columns at cost
`|orbit| * floor(3/2)`, coefficients by `cutting.coverage_matrix` and
`sepcore.atom_columns` with the record’s `1e-9` loosening) is solved cold in one HiGHS
handle (`parallel off`); later columns go in by `addCols` and would-be rows by
`addRows`, re-solved from the old basis.
The sweep is the resume run’s (weights rounded up at `1e9`, `rectangle_terms` +
`sweep_slabs`, `least_charged_slabs(keep = 40, below = 1 - 1e-6)`, two forked workers)
with the deadline checked between phases only; it was never reached, because the value
was above eleven at round 0 and the protocol stops there.

Deviation from the brief, recorded in the lane’s protocol before the run: the rows were
carried (scaled and exactly checked) rather than started from none.
A carried row is an admissible placement, so it cannot make the LP report a value the
full placement set would not, and it saves rounds; here it made the round-0 value itself
the reading (F1). Second deviation, recorded in the addendum during the run: the
separation family was restricted to the heavy rows (Section 3).

At the plateau the driver dumps the dual (every positive row with its exact weight at
`1e-9`, direction, half-tangent, folded angle, class, centre, wall gap,
near-integrality) and the D4-symmetrised family (the ceiling-family format of
[`ceiling-family-191-50.json`](ceiling-family-191-50.json), weights `y/8` on the eight
images rounded down at `1e-9`; `verify_ceiling` in-driver only below 400 placements,
which both families exceed, hence the reader).

## 3. Trajectory

Run 1 (killed inside its atom round; its `at-n` checkpoint is the resume point):

| stage | rows | objective | site / atom support (atom budget) | dual support | LP |
| --- | ---: | ---: | --- | ---: | ---: |
| rows-0 | 15,021 | 11.017916787 | 51 / 14 of 2,566 (1.404643) | 117 | 99.8 s, 6,676 it, cold |
| atom round on the full 936-placement family |  |  | geometry 194 s (162,588 edges), vertex candidates 180 s (4.2M vertices, deepest 1.1243); the triangle stage printed nothing for 20 min at 6.7 GB; killed at 10:46 |  |  |

Run 2 (resumed from run 1):

| stage | rows | objective | site / atom support (atom budget) | dual support | LP |
| --- | ---: | ---: | --- | ---: | ---: |
| rows-0 | 15,021 | 11.017916787 | 51 / 14 of 2,566 (1.404643) | 117 | 106.1 s, 6,676 it, cold |
| atom separation |  |  | family restricted to 52 rows with `y >= 0.05` (weight 9.635, 416 placements, 31,396 edges, 822k vertices, deepest 1.0670); 1,193,776 triangles, 4,976 rechecked exactly and vertex-refined, 803 violated orbits, 400 added (classes: 29-axis-axis 104, 29-axis-other 141, axis-axis-other 95, axis-axis-axis 22, axis-other-other 22, 29-29-axis 8, other-other-other 7, 29-other-other 1) |  | 94 s |
| atoms-1 | 15,021 | 11.017916784 | 93 / 42 of 2,966 (1.404643) | 129 | 233.7 s, 24,677 it, warm |

No sweep row: the protocol sweeps only while the value is below eleven, and it never
was. Least charges, violated cells and per-direction readings therefore do not exist for
this measurement, and “rows complete” is neither claimed nor needed for F1.

Why the restriction: a two-of-three atom violated by the restricted weights (a
sub-measure of the dual) is violated by the full dual, since the charge is monotone in
the weights; the restriction loses candidates, never soundness, and every added orbit
was re-checked against the full dual afterwards (F3: all 400 violated, up to `1.296`).

## 4. The plateau dual

Section 1’s F2 and F4 describe it; the anatomy in full is in the two retained dual files
(rows sorted by weight).
The reader’s depth witness for the first dual lies at
`(37284064805326194904541377807162889729 /
89362596674531174902816825645541540000, 2234135755703/2235192780000)`; its 47 members
(the two axis images of the corner square at `(0.5007, 0.5007)` with `0.182` each, the
`0.26°` corner squares with `0.146` each, the `0.26°` square at `(0.5045, 1.4979)` with
`0.084`, then a tail of light tilted squares) can be regenerated in seconds from the
symmetrised family with `Placement.contains`. The reader’s K4 (two-of-three search), K5
(cliques) and lines were not run because the reader refuses a family above depth one by
design; on a depth-one rescaling the family would weigh `11.018 / 1.124 = 9.80` and
decide nothing.

The second dual is refused at K2 in the same place: depth `1.123274706` at
`(0.99831, 0.99901)`, the corner square’s far corner, 69 members, 5,018,736 vertices,
900 s. Its K4-K6 were likewise not run.

## 5. What failed

- The first launch crashed after the round-0 solve on a `numpy.bool_` in the dual dump;
  fixed with `bool(...)`, relaunched; 130 s lost.
  The dump had not been exercised before the run.
- The atom round on the full 936-placement dual did not finish: the generator’s cost is
  in the triangle enumeration and per-triangle vertex refinement, which spike B ran on
  88-to-400-placement families; at 162,588 edges it had no progress line and no bound.
  Killed after 20 min; the restricted round (416 placements) took 94 s. The driver’s
  `--edge-cap` now refuses such a round up front.
- In-driver `verify_ceiling` was skipped by its 400-placement cap on both duals; the
  reader took 630 s for the 4.2M-vertex depth of the first, nearly all of it the
  arrangement. Fine for one family, not for a loop.
- The theory lane’s picture of the base case (a plateau *at* eleven with a near-integral
  dual to read) did not occur: the plateau is above eleven, the dual is fractional and
  wide, and it is not a point packing, so the reader’s K4-K6 never applied.
  The reading that matters turned out to be the site gap (F2), not the atom family.

## 6. Timings (wall)

| stage | seconds |
| --- | ---: |
| reload and scale (sites, atoms, rows; exact checks) | 2 |
| matrices 15,021 x 4,516, 31.6M nonzeros | 27 |
| HiGHS model pass | 7-8 |
| cold LP (run 1 / run 2) | 100 / 106 |
| dual dump (117 and 129 rows, family files) | about 1 |
| restricted atom round: geometry / vertices / separation / total | 27.5 / 15.3 / 66 / 94 |
| warm re-solve with 400 new columns | 234 |
| plateau reader on the first symmetrised family (K0-K3, refused) | 630 |
| plateau reader on the second symmetrised family (K0-K3, refused) | 900 |
| killed full-family atom round (geometry / vertices / triangles) | 194 / 180 / > 1,200 |
| driver totals (run 1 to the kill / run 2) | about 1,760 / 465 |

Deadline use: the loop ended at 10:55 UTC, 54 minutes before its deadline; nothing was
cut by it.

## Addendum (11:00-11:20 UTC): the same protocol at L = 153/40 = 3.825

Requested by the coordinator after F5 put the linear crossing of eleven on the fixed
columns at `3.8265`. The driver’s `--new-side 153/40` (the side and the homothety are
now arguments; nothing else changed): the accepted `191/50` columns scaled by `765/764`,
`B` and the net unchanged, the 15,021 rows carried after the same exact centre-domain
check (0 dropped; the argument of Section 2 holds at any larger side), one cold HiGHS
solve, rows-only, no atom round.

| # | Finding | Status |
| --- | --- | --- |
| A1 | At `L = 153/40` the covering LP on the scaled `191/50` columns under the carried rows has value **`11.000000000000158`** (HiGHS, 8,199 iterations, 148 s): eleven within solver tolerance. Rows can only raise the value, so no rows-complete value below eleven exists on these columns at `3.825`; nothing was frozen (a bumped candidate would exceed eleven) and the gate was not run. The linear model of F5 was off by `0.0015` in `L`: the restricted value is concave in the side here, `6.54` per unit of `L` from `3.82` to `3.825` (`6.52` per unit of `u`) and `3.58` per unit of `L` from `3.825` to `3.83` (`3.57` per unit of `u`); the crossing of eleven on these columns is at or below `3.825`. | CHECKED (LP float); admissibility EXACT |
| A2 | The dual at `3.825` (88 rows, total `11.000000000000423`, 51 directions) is fractional: no weight within `1e-6` of an integer, weights from `0.0083` to `2.580` with median `0.053`, the eleven heaviest carrying `6.23`; three rows above `0.5`: a `0°` wall square at `(0.5000, 3.3250)` with `2.580`, a `0.26°` wall square at `(2.3267, 0.5018)` with `0.660`, a `2.90°` square at `(1.5220, 0.5428)` with `0.590`. By class: axis `5.60` (27 rows), other `3.56` (43), the `29°` class `1.84` (18); the `29°` rows sit `0.64` inside the centre domain, the interior `8°` rows at `(1.55, 2.1)` about `1.0` inside. No row exactly on a wall (smallest gap `0.0007`). D4-symmetrised: 704 placements of total `1374999961/125000000 = 10.999999688` (rounded down at `1e-9`). | RECORD (`lane-a3-dual-153-40-round0.json`) |
| A3 | The symmetrised family is **refused by the plateau reader at K2**: exact maximum depth **`548760309/500000000 = 1.097520618`** over 2,146,172 arrangement vertices, at the diagonal point `(1.71652, 1.71652)` where 96 placements meet, led by the `29.89°` and `29.40°` pair squares at `(1.39, 1.32)` and their mirror images and the `7.90°` interior squares at `(1.55, 2.14)`; the nearest site of the scaled set is `0.013` away. K0, K1 hold; K3 fails by the `1e-9` rounding (`10.999999688`). As at `383/100` (F2), the plateau dual is not a fractional packing of the plane; here the unsampled spot is interior, at the meeting of the tilted pair and the `8°` squares, not the corner seam. | EXACT (`lane-a3-reader-153-40-round0.json`, 315 s) |
| A4 | So the fixed `191/50` column set reaches eleven between `3.82` and `3.825`, and no side at or above `3.825` is certifiable on it. Whether the method with its own sites and atoms certifies `3.825` is OPEN for the same reason as F7: the loop did not add sites, and F2 shows the sites are what these duals exploit. | OPEN |

Timings: reload and scale 2 s, matrices 25 s (31.9M nonzeros), model pass 8 s, cold LP
148 s, dual dump 1 s; driver total 176 s. Reader (K0-K3 only, refused): 315 s.

Reading of the addendum: the fixed column set crosses eleven between `3.82` and `3.825`,
both plateau duals exceed depth one at points no site samples (a corner seam at `3.83`,
an interior meeting of the tilted pair at `3.825`), and the atom family did not move the
`3.83` value at all.
The sites, not the atoms, are what the next run must add; the two witnesses are the
first two to add.

## Addendum (11:11-12:50 UTC): site separation at L = 153/40 (F7/A4)

Requested by the coordinator.
The site driver is the same LP, sweep and warm HiGHS handle plus a site oracle.

Site oracle: the dual (every positive row, D4-symmetrised) goes to
`sepcore.FamilyGeometry.vertex_candidates`, the exact arrangement vertices of the family
screened in floats with the 60,000 deepest kept and their containment decided exactly
where ambiguous; every kept vertex whose exact depth (`Fraction` weights) exceeds
`1 + 1e-9` is a candidate, the deepest 300 per round become site orbits (`d4_orbit`, one
per orbit, re-verified exactly before entry), added as columns to the warm handle.
The reader’s K2 is then run on the dual the oracle produced, as the exact check.
Rows carried and columns scaled as in the 153/40 addendum; round 0 reproduces
`11.000000000` (8,199 iterations, 125 s).

| # | Finding | Status |
| --- | --- | --- |
| S1 | Oracle round 1 on the round-0 dual (88 rows, 704 placements, 87,052 edges): 2,146,196 arrangement vertices, of the 60,000 deepest **59,608 exceed depth one** (float; the deepest `1.097520618` exact, the reader’s A3 value), so the deep region is not a few seams but a large part of the arrangement. The 300 deepest orbits (2,304 sites) entered; the warm re-solve took **825 s and 60,673 simplex iterations** and returned **`11.000000071`** (columns cannot raise the value; the `7e-8` is solver tolerance). The value did not move. | CHECKED (`lane-a3-trajectory-153-40-sites.json`) |
| S2 | The dual after round 1 is structured: of its 131 positive rows, 96 are below `1e-6` and the remaining **35 rows carry weights that are all multiples of `1/25`** (`68/25, 26/25, 17/25, 14/25, 12/25, 11/25, 11/25, 10/25, ...`, largest float deviation `3e-7`), summing to **exactly 11**: a `0°` wall square at `(0.5000, 3.3250)` with `68/25`, the `29.89°` interior square at `(1.3900, 1.3228)` with `26/25`, a `5.53°` square at `(3.1807, 0.6264)` with `17/25`, then wall squares of the `0.26°`-`2.9°` family at the wall slots `y = 0.5, 1.5, 1.64, 2.18, 3.3`, four `28°`-`30°` squares, and interior `3°`-`20°` squares at `(1.5-1.7, 1.5-2.1)`; 18 axis-class rows, 4 in the `29°` class, 13 other. Symmetrised exactly (the retained `lane-a3-family-153-40-sites-round1-exact25.json`, 280 placements, total `11`), the reader refuses it at K2: **exact maximum depth `28/25`** (30 s, 283,832 vertices) at `(0.99964, 1.82788)`, the right edge of the left-wall column at mid-height, where the mirror pair of `0.26°` wall squares at `(0.5025, 1.6418)` and `(0.5025, 2.1832)` (`7/100` each), the `2.90°`, `0.79°`, `2.37°` wall squares of both slots and the `29.89°` square meet, 39 placements in all. The nearest site is `0.0006` away (one added this round at `x = 1.00018`): the excess moved from the vertex the round sampled to the next cell of a sliver `0.0006` wide, where the right edges of wall squares at `0.26°`, `0.79°`, `1.58°`, `2.37°`, `2.90°` interleave. The `1e-9`-rounded heavy family gives the same depth (`1120000013/1000000000`). | EXACT (`lane-a3-reader-153-40-sites-round1-exact25.json`); RECORD |
| S3 | The `191/50` ceiling family (88 cores, weight `1/8`) scaled by the homothety to `153/40` and to `383/100` (`B`, net, weights unchanged) is a **depth-one family of total 11 at both sides** (reader K0-K3: max depth exactly `1`, 20,480 and 20,504 vertices, 3-4 s each), so the point-method ceiling holds at both sides, as the point-extension lemma predicts. Its two-of-three maximum is **`5/4` at both sides** (K4 complete, 144 maximisers; K5: 16 maximal cliques above one, heaviest `5/4` with `tau* = 3/2`): the two-of-three cut of the ceiling family survives the homothety, so the exact eleven of the threshold LP is *not* the scaled ceiling family, and no theorem capping the two-of-three method at `3.825` follows from it. | EXACT (`lane-a3-reader-ceiling-153-40.json`, `lane-a3-reader-ceiling-383-100.json`) |
| S4 | The site chase did not reach a decision in the budget: each round costs about 200 s of oracle and 800 s of warm LP (the 300 new columns re-pivot the whole basis), and S2 shows the excess retreating into a sliver by `0.0006` per round, with at least 59,608 deep vertices behind it. No rows-complete value below eleven and no dual accepted by the reader; nothing frozen; `383/100` not attempted. The reading is that at `3.825` on these atom columns the value is pinned at exactly eleven by a `1/25`-integral family whose excess lives in the mid-wall sliver, and closing it needs either sites placed by the sliver’s structure (the interleaved wall-square edges, not vertex by vertex) or the atom that cuts the `1/25` family (its K4 is unknown because the reader refuses above depth one; the two-of-three generator of F3 could be run on it directly). | OPEN |

Site-run trajectory, rendered from the run’s `trajectory.json` after the report text was
written; rounds 2 and 3 ran past the report’s cut-off and returned eleven as well, which
is the reading S4 records:

| stage | sites (orbits) | objective | site / atom support (atom budget) | dual support | LP | oracle |
| --- | ---: | ---: | --- | ---: | ---: | --- |
| rows-0 | 15,085 (1,950) | 11.000000000 | 42 / 17 (1.701786) | 88 | 125 s, 8,199 it |  |
| sites-1 |  |  | family 704 placements, 87,052 edges; 60,000 vertices kept, 59,608 above 1 + 1e-9, deepest exact 1.097520618; 300 orbits added |  |  | 204 s |
| sites-1 | 17,389 (2,250) | 11.000000071 | 141 / 40 (1.467304) | 131 | 825 s, 60,673 it |  |
| sites-2 |  |  | family 1048 placements, 204,448 edges; 60,000 vertices kept, 59,984 above 1 + 1e-9, deepest exact 1.120000054; 300 orbits added |  |  | 619 s |
| sites-2 | 19,765 (2,550) | 11.000000000 | 108 / 31 (1.500192) | 45 | 690 s, 36,732 it |  |
| sites-3 |  |  | family 360 placements, 19,060 edges; 60,000 vertices kept, 16,816 above 1 + 1e-9, deepest exact 1.091452429; 300 orbits added |  |  | 51 s |
| sites-3 | 22,149 (2,850) | 11.000000017 | 148 / 45 (1.372402) | 163 | 552 s, 26,857 it |  |

Timings: reload 2 s, matrices 25 s, cold LP 125 s; oracle round 1 = geometry 110 s +
vertices 65 s + exact recheck 29 s = 204 s; warm LP with 300 site columns 825 s; reader
on the heavy family 30 s (`exact25`) and about 30 s (`heavy`); reader on the two scaled
ceiling families 4 s each; building the scaled families under 1 s.

## The protocol, as pre-registered

The lane wrote its protocol before its first solve and kept it in scratch; its substance
is recorded here, because the file itself is not retained.
Two were written. The first attempt (07:19 UTC) got no further than the protocol before
an API outage; the second (10:09 UTC) kept its object, its rows decision and its labels
and restated the timing, and is the one the run followed.
The first is superseded and not retained.

What the protocol fixed in advance was the object (Section 2), the rows deviation
(Section 2), the stop rules and what each outcome would produce.
The stop rules: a full sweep finding no cell below `1 - 1e-6` (rows complete), the
objective reaching `11 - 1e-9`, or the loop deadline.
The deadline is checked only between phases, so a sweep is never interrupted, a sweep is
not started unless the previous sweep’s wall time fits before the deadline, and a
partial sweep is never reported as complete.

Three branches were declared before the first solve, which is what makes F1 a reading
rather than a choice made once the number was known:

- **Rows complete below eleven**: freeze the checkpoint with `freeze383.py` (every
  positive weight times `1 + 2e-6`, rounded up at scale `1e-9`, D4-expanded, budget
  declared) and decide the frozen bytes with
  `PACK_JOBS=2 uv run --frozen --all-extras --group dev python -m devtools.decide_threshold_certificate --workers 2 CANDIDATE.json`,
  reporting verdict, least charge, total budget and SHA-256. Nothing is a bound until
  the gate accepts the frozen bytes.
- **Objective at eleven**: dump the dual at once, then one round of atom separation if
  at least 40 minutes remain before the loop deadline, then rows-only completion.
  This is the branch that ran.
- **Deadline without either**: OPEN, with the trajectory and no completeness claim.

The gate command above was never run in this lane, because the first branch was never
reached; it is recorded so that the unrun step is as legible as the run ones.
The plateau reader was invoked as
`plateau_reader.py FAMILY.json --out OUT.json --time-limit SECONDS --cg-thresholds 2,3`,
so every `K6` reading here searched thresholds 2 and 3 only.

## Files

Retained beside this report:

- [`lane-a3-dual-383-100-round0.json`](lane-a3-dual-383-100-round0.json) and
  [`lane-a3-dual-383-100-round1.json`](lane-a3-dual-383-100-round1.json): the two
  plateau duals of F2, F4 and F6, every positive row with its exact weight, direction,
  class, centre, wall gap and near-integrality.
- [`lane-a3-dual-153-40-round0.json`](lane-a3-dual-153-40-round0.json): the `3.825` dual
  of A2.
- [`lane-a3-family-153-40-sites-round1-exact25.json`](lane-a3-family-153-40-sites-round1-exact25.json):
  S2’s `1/25`-integral family, 280 placements of total exactly 11, the object the reader
  refuses at depth `28/25`.
- The plateau-reader verdicts:
  [`lane-a3-reader-383-100-round0.json`](lane-a3-reader-383-100-round0.json),
  [`lane-a3-reader-383-100-round1.json`](lane-a3-reader-383-100-round1.json),
  [`lane-a3-reader-153-40-round0.json`](lane-a3-reader-153-40-round0.json),
  [`lane-a3-reader-153-40-sites-round1-exact25.json`](lane-a3-reader-153-40-sites-round1-exact25.json),
  and S3’s two on the scaled ceiling family,
  [`lane-a3-reader-ceiling-153-40.json`](lane-a3-reader-ceiling-153-40.json) and
  [`lane-a3-reader-ceiling-383-100.json`](lane-a3-reader-ceiling-383-100.json).
- The three trajectories:
  [`lane-a3-trajectory-383-100.json`](lane-a3-trajectory-383-100.json),
  [`lane-a3-trajectory-153-40.json`](lane-a3-trajectory-153-40.json) and
  [`lane-a3-trajectory-153-40-sites.json`](lane-a3-trajectory-153-40-sites.json).
- The five driver scripts:
  - [`lane-a3-lp383.py.txt`](lane-a3-lp383.py.txt) — the rows-only threshold LP of
    Section 2: it scales the `191/50` checkpoint into the new container, checks every
    carried row exactly, runs the sweep-and-solve loop in one warm HiGHS handle, dumps
    the dual at a plateau, and runs the optional atom-separation round of F3. F1 through
    F6 and the first addendum are its output.
  - [`lane-a3-lp-sites.py.txt`](lane-a3-lp-sites.py.txt) — the same LP, sweep and solver
    with the site oracle of the second addendum added: arrangement vertices of the dual
    family screened in floats, exact depth decided in `Fraction`s, the deepest orbits
    entered as columns. S1, S2 and S4 are its output; S3 reads the plateau reader on the
    scaled ceiling families, which were built outside these five scripts.
  - [`lane-a3-atoms-on-family.py.txt`](lane-a3-atoms-on-family.py.txt) — the same
    interior-vertex two-of-three generator `lp383.py` calls for F3, as a standalone
    runner over any family file.
    It is retained as the instrument for the measurement S4 names rather than for a
    reading of its own: pointed at the `1/25`-integral family it logged its geometry and
    vertex stages (280 placements, 11,252 edges, 283,832 vertices) and was stopped
    before it returned atoms.
  - [`lane-a3-freeze383.py.txt`](lane-a3-freeze383.py.txt) — the freezer of the
    protocol’s first branch: it turns a checkpoint into a threshold-certificate record
    with the bump, the upward rounding, the D4 expansion and the declared budget.
    It was never run here, because the value never went below eleven.
  - [`lane-a3-trajectory-table.py.txt`](lane-a3-trajectory-table.py.txt) — renders a
    run’s `trajectory.json` as the Markdown table of Section 3.

The five scripts are retained with a `.py.txt` extension, as
[lane X3](lane-x3-containment-atoms-do-not-cut.md) and
`agenda-032/unrun-independent-audit/` already do: they are scratch measurement scripts,
not importable project modules, and the repository’s Python surface is held at zero Ruff
and BasedPyright findings over every tracked `.py` file.
Their bytes are as delivered; nothing was reformatted.

They are **a record of how the measurement was made, not a supported tool.** Each was
run from a scratch directory against the repository at commit `7ccb679c`, and each takes
its inputs as command-line arguments but resolves its imports from the scratch layout it
ran in: `lp383.py`, `lp_sites.py` and `atoms_on_family.py` reach a sibling `spike-b/`
directory for `sepcore`, which is retained beside lane B’s report as
[`lane-b-sepcore.py.txt`](lane-b-sepcore.py.txt), so the three are runnable from this
directory. Nothing in the repository imports any of them, and nothing should.

Not retained (scratch only): the three LP checkpoints with their sites, atoms, rows and
solution arrays (about 60 MB), the symmetrised families above 150 KB, the 400 added atom
orbits, every run log, the two protocol files (their substance is above), and the three
shell wrappers around the freeze, the gate and the reader (their commands are above).
The instrument this lane leans on is retained: `packing/devtools/plateau_reader.py`,
promoted by lane T2 and reported in
[`lane-t2-plateau-reader.md`](lane-t2-plateau-reader.md).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
