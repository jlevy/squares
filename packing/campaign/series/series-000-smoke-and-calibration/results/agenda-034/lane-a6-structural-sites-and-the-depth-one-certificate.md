# Agenda 034, lane A6: structural site placement at L = 153/40, and the certificate that closes the site side

Retained measurement-lane report for
[X-024](../../../../explorations/X-024-two-lines-at-eleven.md), carrying bead
`think-q0f4`, run 2026-09-10 against `claude/n-11-stronger-result-d730ds` at `67ccd16b`,
read-only on the repository.
The report is reproduced as delivered, with its own findings table and status labels;
only its file references were rewritten to say where each file now is, and the file list
at the end now separates what is retained here from what stayed in scratch.
X-024 carries the coordinator’s reading, and §5 of that document now carries this lane’s
correction of the site-versus-atom inference.

Labels: **EXACT** (a rational decision by a repository primitive or by a float proposal
whose every ambiguous entry was decided in `Fraction`s), **CHECKED** (a float LP or
float sweep reading), **RECORD** (retained files), **OPEN**.

## 0. The answer

|  |  |
| --- | --- |
| **LP before** — 17,389 sites in 2,250 orbits, 2,566 atom orbits, 15,021 rows | **`10.999999999999945`** (lane A4’s control, same checkpoint and code path) |
| **LP after** — +1,400 structural site orbits, **28,237 sites in 3,650 orbits**, same atoms, same rows | **`11.000000000`** (33,473 iterations, 404.9 s) |
| **LP after, round two** — +3,999 structural site orbits (1 duplicate), **48,253 sites in 6,249 orbits**, 63,575,252 nonzeros | **still in simplex at 71 minutes** when the lane closed, against 405 s for round one; left running, and nothing depends on it |
| **LP with the six certificate atoms as columns** — round one’s 28,237 sites plus 6 atom orbits | **`11.000000000`** (39,582 iterations, 934.5 s), the six columns at primal weight exactly zero |
| **Outcome** | **The second of the two: the value stays at eleven** — and G8 proves no site set can move it |
| **Where the excess ended up** | exact depth `36458333/31250000 = 1.166666656` at `(1.065518, 1.912500)`, on the container’s centre line `y = L/2`, **`0.000125` from the nearest of the 28,237 sites** — a third place, deeper than before and 34 to 60 times closer to a site |
| **Rows** | all 15,021 carried unchanged and previously checked exactly; none added, none dropped |

## 1. Findings

| # | Finding | Status |
| --- | --- | --- |
| G1 | **The depth-one ceiling family does not settle the question, and the reason is the atoms.** The `191/50` ceiling family scaled to `153/40` (88 placements, total exactly 11, exact maximum depth exactly 1 — lane A3’s S3) has depth at most one at *every* point, so it satisfies the site-orbit dual constraint of **every** site set whatsoever. Were it also feasible for the atom columns it would bound the rows-complete LP below by eleven for all time and close this question outright. It is not: **226 of the 2,566 atom orbits are violated by it, at charge-to-budget exactly `5/4`**. Measured twice, at float screens `1e-9` (0 ambiguous memberships) and `1e-6` (48 ambiguous, every one decided by `Placement.contains` in `Fraction`s, 0 float verdicts corrected). So the site question is genuinely open on this column set, and it is the atoms that keep it open. | EXACT ([`lane-a6-ceiling-atoms-153-40.json`](lane-a6-ceiling-atoms-153-40.json), [`lane-a6-ceiling-atoms-153-40-screen1e6.json`](lane-a6-ceiling-atoms-153-40-screen1e6.json), 1 s) |
| G2 | **A structural scan reads the deep region two orders of magnitude faster than the vertex oracle, at a 100 % hit rate.** The generator (§2) scans the seven retained duals of the `153/40` optimal face along a structured line net — the midpoints of consecutive distinct placement-corner ordinates, one line strictly inside every horizontal slab, and the same in `x` — and emits the midpoint of every maximal run of the exact depth profile above one. **37,368 raw candidates, 37,055 distinct, and all 37,055 have exact depth above one** (17,885 distinct D4 orbits), in **14.6 s**. The record’s oracle screened 60,000 arrangement vertices for 59,608 deep ones, kept the 300 deepest and cost **204 s a round** (A3, S1). Nothing here is an argmax: a midpoint is interior to its cell, so it stays a separating site when the dual moves. | EXACT (all 37,055 depths in `Fraction`s, 0 memberships ambiguous at screen `1e-9`) |
| G3 | **The deep region is three structures, not the two the readings named.** Folded into the D4 fundamental domain, the 17,885 deep orbits fall as: **wall-column seam 46.7 %** (8,361), **interior 30.1 %** (5,391), **neither 22.0 %** (3,926, a band off both), wall band below `0.55` 1.0 %, diagonal 0.2 %. The 22 % that is neither the mid-wall seam nor a clean interior blob is the third structure, and it carries more deep cells than the diagonal point and the wall band together by a factor of twenty. | EXACT depths; CHECKED census |
| G4 | **The mid-wall “sliver `0.0006` wide” is one cell of a full-height column.** Across the face the seam structure has **1,123 distinct deep abscissae spanning `[0.990018, 1.009624]`, a width of `0.0196`**, and its ordinates span **`[0.0663, 3.7631]`** — the whole container height. S2 measured the width of one cell; the structure it belongs to is thirty times wider and runs from wall to wall. This is why the excess “retreats by `0.0006` per round”: each round closes one cell of a column that has of order a thousand of them at every height. | EXACT points; CHECKED extent |
| G5 | **The deep cells are not needles, and that prices the whole approach.** Median deep-cell width along the scan net: `4.68e-3` on the round-0 dual, `1.43e-2` on the round-3 dual, `2.63e-3` on the `1/25`-integral family. Split by structure: seam cells median `9.7e-4`, `9.4e-4` and `3.1e-4`; interior cells median `5.6e-3`, `1.2e-2` and `2.9e-3`. A site net that meets every deep cell therefore needs a spacing near `1e-3` over a region of area order one — of order `10^6` sites, against the `10^4` the LP can carry. | CHECKED ([`lane-a6-cell-widths.json`](lane-a6-cell-widths.json)) |
| G6 | **The structural set samples the deep region three times better than the vertex set, with 38 % fewer points, and still misses two thirds of it.** Nearest-site distance from the 17,885 deep orbits: to the base 17,389 sites, median `0.0069`, mean `0.0121`, **85.9 % more than `1e-3` away**; to the 10,848 structural sites, median `0.0022`, mean `0.0032`, **68.4 % more than `1e-3` away**. The generator does what it was designed to do, and the region is still larger than any affordable net. | CHECKED (float `cKDTree`; the underlying points EXACT) |

## 2. The generator

[`lane-a6-gen-sites.py.txt`](lane-a6-gen-sites.py.txt), four stages, all of them over
*every* dual given rather than one.

**Stage 1, a structured scan net.** Depth is piecewise constant on the cells of the
arrangement of the family’s placement edge lines.
A horizontal line `y = c` meets each placement in one interval, so the depth along it is
an exact step function computable from `2m` events.
The scan levels are the **midpoints of consecutive distinct corner ordinates** of the
family — one line strictly inside every horizontal slab of the placement-corner
decomposition — and the same in `x`. That is a net read off the family’s own structure,
not a sample of it, and it costs one sort of `2m` numbers per line.

**Stage 2, one site per deep cell.** Every maximal run of the profile above depth one
contributes its **midpoint**: a point in the *interior* of a deep cell, not a vertex on
its boundary, so it remains a separating site when the dual moves within the optimal
face. Floats locate the runs; each emitted point’s depth is then decided exactly, its
membership set proposed by float slab margins and every entry inside the margin decided
by `Placement.contains` in `Fraction`s.

**Stage 3, structural extension.** Deep points are clustered by abscissa (a vertical
seam), by ordinate (its mirror) and by proximity (an interior blob); each cluster is a
structure and the generator emits a ladder along it — the cluster’s distinct transversal
offsets crossed with a ladder of levels spanning its extent.
**This stage was written and then not needed**: stage 2 already returned 37,055
exactly-deep points against a column budget of 1,400 orbits, so the run used
`--ladder-steps 0`. The code is retained and the switch is one argument.

**Stage 4, the face rather than a vertex.** Lane A4’s P9 showed the optimal face at
`153/40` is wide and that a separation tuned to one of its vertices generalises only in
part. The generator therefore runs over all seven retained duals of that face at once —
`family-at-n-{0,1,2,3}` of the site loop, the `1/25`-integral family, and A4’s control
and seeded duals — and keeps a point deep for any of them.

**Selection is spatial, not by depth.** The cap is filled by round robin over coarse
`0.02` cells, deepest first within a cell, so 1,400 orbits spread across 1,400 of the
2,955 occupied cells instead of piling onto the deepest structure.
Taking the 1,400 deepest points instead would have put nearly all of them in the seam.

## 3. What was measured, and how

**The LP.** [`lane-a6-lp-struct.py.txt`](lane-a6-lp-struct.py.txt) is lane A4’s
[`lane-a4-lp-atoms.py.txt`](lane-a4-lp-atoms.py.txt) with one addition, `--seed-sites`:
a JSON of D4 orbits from the generator, each re-derived by `d4_orbit` from its own
representative and asserted equal before entry, appended to the site column block before
the matrix is built.
Nothing else changed, so the “before” number is lane A4’s control run of the same code
path on the same checkpoint.

**The column set.** The base is the record’s own `sites-1` checkpoint at `153/40` —
17,389 sites in 2,250 D4 orbits, 2,566 two-of-three atom orbits, 15,021 carried rows —
which is the LP whose dual is the `1/25`-integral family, and exactly the configuration
lane A4 solved cold at `10.999999999999945`. The 1,400 structural orbits add 10,848
sites; **none of them duplicated an existing site**, so the vertex oracle over four
rounds had sampled no point of the structural net.

**Rows.** All 15,021 rows are carried unchanged from the checkpoint.
They were checked exactly against the centre domain when that checkpoint was built (A3,
Section 2: `e <= c
<= L' - e` in both coordinates, 0 dropped), and this run adds no row and drops none, so
every row here is an admissible placement and the LP is a relaxation of the certificate
problem, never a strengthening of it.
**Columns can only lower a covering LP’s value**, so any movement is the columns’ and
not a row artefact.

**Discipline.** Every depth, every membership and every atom charge in this lane is
decided in rational arithmetic; floats propose the scan runs, the LP value and the
nearest-site distances, and decide nothing.
Where a float screen was used the ambiguous entries are counted and decided exactly, and
the count is reported.

## 4. The deep region, measured

The census below is over the 17,885 distinct D4 orbits of exactly-deep points the
generator returned from the seven duals, folded into the fundamental domain.

| structure | deep orbits | share | what it is |
| --- | ---: | ---: | --- |
| wall-column seam, `x` or `y` within `0.01` of `1.0` | 8,361 | 46.7 % | the right edge of the left-wall column and its three images |
| interior, both folded coordinates above `1.05` | 5,391 | 30.1 % | the `29°` tilted pair against the `8°` interior squares |
| neither | 3,926 | 22.0 % | **the third structure** |
| wall band, a folded coordinate below `0.55` | 174 | 1.0 % | inside the wall column itself |
| diagonal, `|x - y| < 0.01` | 33 | 0.2 % | A3’s `(1.71652, 1.71652)` |

Two readings follow directly.

The **seam is a column, not a sliver** (G4): 1,123 distinct deep abscissae over a width
of `0.0196`, ordinates from `0.0663` to `3.7631`. Lane A3’s S2 measured one cell of it
and priced the round at `0.0006` of retreat; the structure that cell belongs to is
thirty times wider and runs the full height of the container.

The **diagonal point is not a structure at all** — 33 of 17,885 orbits.
A3’s round-0 witness `(1.71652, 1.71652)` and A4’s `(1.294501, 1.843441)` are two points
of the interior structure, and the migration between them is movement inside one
5,391-orbit region, not migration between two things.

## 5. The LP, and the theorem that explains it

| # | Finding | Status |
| --- | --- | --- |
| G7 | **The LP does not move.** The `sites-1` checkpoint with 1,400 structural site orbits added — **28,237 sites in 3,650 orbits**, 2,566 atom orbits, the same 15,021 carried rows, 15,021 x 6,216 with 44,292,847 nonzeros — solves cold to **`11.000000000`** (HiGHS, 33,473 iterations, **404.9 s**; matrices 34.5 s, model 10.3 s, driver total 441 s), against lane A4’s control **`10.999999999999945`** on the identical checkpoint and code path. Every one of the 1,400 orbits was new: **0 duplicated a site the vertex oracle had ever sampled** over four rounds. The dual does move, and hard: its support falls from A4’s 64 rows (512 placements) to **16 rows (128 placements)**. | CHECKED (LP float); rows carried unchanged and admissibility EXACT |
| G8 | **No site set can ever move it, and here is the certificate.** Maximising total weight over the 280-placement support of the `1/25`-integral family, with weights tied across its 35 D4 orbits, subject to depth at most one at **every one of the 139,521 structural sites** and to all 2,566 atom orbits, returns **exactly 11**. The optimum is a D4-symmetric family of **64 admissible placements of total exactly 11** whose **exact maximum depth is exactly `1`** over all 14,344 arrangement vertices — `devtools.plateau_reader` reads K0, K1, K2, K3 all holding and does not refuse it — and which charges **every one of the 2,566 atom orbits at ratio exactly `1`, none violated** (independent check, 80 ambiguous memberships all decided by `Placement.contains` in `Fraction`s, 0 float verdicts corrected). A family of depth at most one everywhere satisfies the site-orbit dual constraint of *every* site set; this one also satisfies every atom column. **So the rows-complete certificate LP at `L = 153/40` on this atom set has value at least eleven for every site set whatsoever** — structural, vertex-driven, or exhaustive. `sqpack.fractional.ceiling.verify_ceiling` proves the same family independently, with no failed condition: *“no D4-symmetric measure of mass below 11 captures mass 1 in every closed B-square at a net angle in the container”*. Three routes, three primitives, one verdict. | EXACT ([`lane-a6-saturated-symmetric-153-40.json`](lane-a6-saturated-symmetric-153-40.json), [`lane-a6-reader-saturated-symmetric.json`](lane-a6-reader-saturated-symmetric.json), [`lane-a6-ceiling-atoms-saturated-symmetric.json`](lane-a6-ceiling-atoms-saturated-symmetric.json)) |
| G9 | **So the premise inverts: it is the atom language, not the site set, that pins `153/40` at eleven.** The same reader run on the certificate of G8 reports the **complete** two-of-three search at maximum charge **`11/8`** against budget 1 — violation `3/8` — and violated budget-one and rank-one floor atoms besides. The family that blocks every site set is itself cut by two-of-three atoms **outside the LP’s 2,566 orbits**. Lane A4’s P6 read “adding atoms moves the LP by `2.2e-13`” as the atoms being spent; what it actually measured is that the 24 atoms separated from *one dual vertex* miss the family that holds the face. The columns the method is short of are atoms, and they are nameable: the reader names one at violation `3/8` in 80 s. | EXACT |
| G10 | **Where the excess ended up, and it is a third place.** The dual after the structural round has exact maximum depth **`36458333/31250000 = 1.166666656`** at **`(1.065518, 1.912500)`**, 24 placements meeting it, over 53,132 arrangement vertices in 6.5 s. That is **`y = L/2` exactly**, on the container’s horizontal centre line at `x = 1.0655` — neither S2’s mid-wall sliver at `x = 0.99964` nor A4’s interior tilted-pair meeting at `(1.2945, 1.8434)`, and it is led by the `25°`-`30°` inner pair at `(1.330, 1.392)`, the `2.6°` squares at `(1.532, 1.542)` and a `0.79°` wall square at `(0.547, 2.149)`. **The nearest of the 28,237 sites is `0.000125` away** — against A3’s `0.013`, A4’s `0.004230` before its atoms and `0.007740` after. The excess got 34 to 60 times closer to a sampled site *and `0.05` deeper* (`1.1667` against `1.1145`). And the site it is `0.000125` from is a **base** site the vertex oracle had already placed: the nearest of the 10,848 structural sites is `0.0097` away. The dual did not move away from the sites it was avoiding; it stepped into the cell next door to one of them, in a corner of the container the structural net covered thinly. | EXACT ([`lane-a6-excess-round1.log`](lane-a6-excess-round1.log)) |
| G11 | **The migration is inside one region, not between two.** Every witness the record reports and the one measured here — `(1.71652, 1.71652)`, `(0.99964, 1.82788)`, `(1.300943, 1.847007)`, `(1.294501, 1.843441)`, `(1.065518, 1.912500)` — lies in the deep region the generator maps as one connected structure census (G3): a `0.02`-wide full-height seam column, a large interior region, and 22 % that is neither. The excess is not hopping between two special points; it is moving inside an area whose finest cells are `3e-4` wide and whose typical cells are `5e-3`, and G8 says it will keep doing so at any site density, because a weight-eleven family survives every site. | EXACT points; CHECKED census |

## 6. Reading

The discriminating question was: **does structural site placement drop the restricted LP
below eleven at `153/40`?** The answer is **no**, and G8 upgrades that from a
measurement to a theorem for this column set: **no site set can**, because a
D4-symmetric fractional packing of the plane of total exactly eleven exists at this side
which satisfies every one of the LP’s 2,566 atom columns at ratio exactly one.
Whatever sites are added, that family is dual-feasible and the value cannot fall below
its weight. §9 states precisely what that bounds — the rows-complete value, the one the
method needs — and what it does not.

That inverts the premise the brief carried over from A3’s S4 and A4’s P8. The site chase
was reading a real signal — the excess does migrate, the deep region is far larger than
the record’s readings suggested (G3, G4), and the vertex oracle samples it 3 times worse
than a structural net at 1.3 times the cost in columns (G6) — but it was chasing the
wrong quantity. **The obstruction is not that the sites miss the excess; it is that a
weight-eleven family exists which has no excess at all** once the deep region is
sampled, and it is invisible to the atom columns the LP carries.

What A4’s P6 measured is narrower than it reads.
Twenty-four atom orbits separated from one vertex of the optimal face moved the LP by
`2.2e-13`; the family of G8, which holds the whole face against every site set, is cut
by two-of-three atoms at violation `3/8` that were never in the column set and that the
plateau reader names in 80 s. **The method’s shortfall at `153/40` is atom columns, and
they are separable from the right object.** The right object is not a dual vertex: it is
a maximiser of the fixed-support program under depth-one-everywhere plus the atom class,
which is what [`lane-a6-symmetric-max.py.txt`](lane-a6-symmetric-max.py.txt) computes
and what [lane A5](lane-a5-the-fixed-support-maximum-under-the-atom-classes.md) was
already building (its F1, F10) without pointing it at the LP’s own atom set.

**And the corrected recipe works.** Section 10 runs the obvious loop — solve the
fixed-support maximum, read the optimum with the plateau reader, add what it returns,
re-solve — and **six atom orbits take the blocking support from exactly eleven to
`10.4210526`**, bracketed exactly between a feasible family and a priced dual (G13).
Twenty-four atoms separated from a dual vertex moved the LP by `2.2e-13`; six separated
from the family that actually blocks it move their support by `0.579`. The scarce
resource was never the atoms’ number, and never the sites.

Three consequences worth carrying forward.

- **Stop adding sites at `153/40`.** G8 is a certificate that the site side is closed on
  this atom set. Site rounds cost 200 to 800 s each and cannot move the value.
- **Separate atoms from the saturated family, not from the LP dual.** The reader accepts
  it (depth one, so no gate bypass is needed, unlike lane A4) and returns violated atoms
  in every class it knows in about 80 s.
- **A4’s P10 freeze gap does not block this route.** All six atoms of G13 have uniform
  multiplicity — two two-of-three and four three-of-five — and `ThresholdAtom` carries
  both shapes, so every one of them could be frozen into a threshold certificate as it
  stands. The loop deliberately discards the reader’s non-uniform budget-one atoms and
  its Chvátal–Gomory giants, which P10 showed cannot be frozen; it reaches `10.42`
  without them.

## 7. Timings (wall)

| stage | seconds |
| --- | ---: |
| ceiling-family atom check, 2,566 orbits against 88 placements (twice, screens `1e-9` and `1e-6`) | 0.7 / 1.0 |
| structural generator, 7 duals, 900 scan levels per axis, 37,368 candidates, exact depths | 14.6 |
| generator at `--orbit-cap 4000` (round two’s set) | 15.4 |
| deep-cell width measurement, 3 families, both axes | 22 |
| site-coverage k-nearest-neighbour, 17,885 deep orbits against two site sets | 3 |
| fixed-support maximum, 4 supports, depth rows only | 0.7-5.6 each |
| fixed-support maximum with the 2,566 atom rows, 139,521 sites | 10.2 |
| D4-tied symmetric fixed-support maximum, same rows | 7.5 |
| plateau reader on the 37-placement optimum (K0-K6) | 11.6 |
| plateau reader on the 64-placement symmetric certificate (K0-K6) | 80.0 |
| **LP round one**: matrices / model / cold solve / driver total | 34.5 / 10.3 / **404.9** / 441 |
| exact excess of the round-one dual (128 placements, 53,132 vertices) | 6.5 |
| exact excess of the atom-column dual (296 placements, 307,096 vertices) | 26.7 |
| **LP round two** (8,815 columns, 63,575,252 nonzeros): matrices / model / cold solve | 56.3 / 16.4 / **> 4,260 and unfinished** |
| atom loop, 3 rounds: fixed-support solves / reader runs | 5.7 + 5.5 + 4.8 / 12.8 + 14.6 + 1 (refused) |
| exact dual bracket on the `10.42` optimum | 5.7 |
| **LP with the six atoms as columns** (6,222 columns, 44,330,151 nonzeros): matrices / model / cold solve | 31.6 / 8.2 / **934.5** |

Round two’s cost is itself a reading: **1.43 times the nonzeros bought more than ten
times the simplex time**, and it had not converged when the lane closed.
Scaling the site side is superlinear in exactly the range where it stops being
affordable, which is a second, independent argument for G8’s conclusion — even if a site
set could work, this one could not be solved.

Two workers throughout, on four cores.
The measurement that decided the question — G8 — cost **18 seconds of linear programming
and 80 seconds of plateau reader**, against the 441 s of the LP round it predicted and
the 825 s a single vertex-oracle round costs in the record.

## 8. What failed

- The generator’s first full run was **OOM-killed** at 15 GB: the exact filter allocated
  a `candidates x placements` float matrix per family, 37,055 x 1,304 twice over.
  Chunked to 4 M entries at a time; the run then took 14.6 s. The kill cost about 4
  minutes and produced no output at all, because the invocation piped through `tail` — a
  second, self-inflicted cost worth recording.
- **Round two did not finish.** The 4,000-orbit configuration (8,815 columns, 63.6 M
  nonzeros) was still in its cold solve after 71 minutes against round one’s 405 s, and
  the lane closed with it running.
  Nothing depends on it — G7 measured the LP and G8 settles it for every site set — but
  it cost the second worker for the whole session and should have been sized from round
  one’s timing rather than launched beside it.
  It is **OPEN**, not a result.
- The **ladder stage** (stage 3) as first written called the scalar `depth_exact` per
  point per family and was projected at hours.
  It is now vectorised through the same screened path and capped by `--ladder-clusters`,
  and it was not needed: stage 2 returned 26 times more exactly-deep points than the
  column budget could take.
- The first attempt at a certificate was the **scaled ceiling family** (G1), which would
  have closed the question in one second had it been atom-feasible.
  It is not — 226 of the 2,566 orbits cut it at `5/4`. The certificate that works had to
  be *computed* under the atom rows, not inherited.
- `CeilingCertificate.from_record` rejects a record whose `half_tangents` are not
  strictly increasing, so the dumped optimum needed its parent’s half-tangent list
  rather than the set of its own.
  One minute.
- [`lane-a6-atom-loop.py.txt`](lane-a6-atom-loop.py.txt), the single-process version of
  §10’s loop, calls `two_of_three_maximum` directly and gets witnesses back as
  **membership-set indices**, not points; turning them into atoms needs `shape_atom`,
  which the loop did not wire up.
  Replaced by [`lane-a6-run-atom-loop.sh.txt`](lane-a6-run-atom-loop.sh.txt), which
  drives the reader’s CLI and reads its `violated_atoms`. About 8 minutes, and the
  direct-call version is retained unrun.

## 9. The certificate, in full

[`lane-a6-saturated-symmetric-153-40.json`](lane-a6-saturated-symmetric-153-40.json):
**8 D4 orbits, 64 placements, total exactly 11**, all weights dyadic with denominator
32\.

| folded angle | orbit representative | orbit weight | total |
| ---: | --- | ---: | ---: |
| `0.000°` | `(0.50002, 0.50002)` corner square | `13/32` | `13/4` |
| `0.000°` | `(0.49958, 1.64190)` wall slot | `1/8` | `1` |
| `0.264°` | `(0.50283, 2.32436)` wall slot | `1/16` | `1/2` |
| `0.527°` | `(0.50449, 1.63749)` wall slot | `1/16` | `1/2` |
| `0.791°` | `(0.50676, 2.31949)` wall slot | `1/4` | `2` |
| `1.318°` | `(1.51170, 1.51544)` interior | `1/8` | `1` |
| `7.111°` | `(0.57268, 3.17515)` near-corner | `3/32` | `3/4` |
| `29.892°` | `(1.32278, 2.43504)` inner pair | `1/4` | `2` |

Only **8 of its 64 placements** are shared with the scaled `191/50` ceiling family’s
support, so this is a different depth-one family and not that one reweighted — which is
what S3 predicted would be needed and what G1 confirmed by refutation.

**Precision on what G8 does and does not say.** It bounds the **rows-complete** value —
the value the method actually needs, every admissible core a row — from below by eleven,
for every site set and this atom set.
It does not forbid a *restricted-row* LP from reading below eleven with more sites: the
restricted program is a relaxation, so its value only ever bounds the rows-complete one
from below. What G8 says about that case is sharper than a prohibition: **any
restricted-row value below eleven at `153/40` on this atom set is a rows-incompleteness
artefact**, and the sweep is guaranteed to find a cell below one.
That is the same trap the brief named, now with a certificate behind it rather than a
caution.

## 10. What it would take on the atom side

Since G8 closes the site side, the remaining question is how many atom columns the LP is
short of. The instrument is
[`lane-a6-symmetric-max.py.txt`](lane-a6-symmetric-max.py.txt) plus the plateau reader
in a loop: solve the D4-tied fixed-support maximum under the structural sites and every
atom so far, read the optimum with `devtools.plateau_reader`, add every
uniform-multiplicity atom it returns, re-solve.
Because the optimum has depth exactly one, **the reader accepts it outright** — no gate
bypass, unlike lane A4, so every verdict here is a statement about the family and not
only a separation oracle’s proposal.

| # | Finding | Status |
| --- | --- | --- |
| G12 | **One atom is not enough, and the support migrates the same way the sites did.** Adding the reader’s own two-of-three atom on the certificate family (3 points, budget 1, charge `11/8`, violation `3/8`) as a 2,567th atom row leaves the fixed-support maximum at **exactly 11** on a *different* family — 7 orbits, 56 placements, in place of 8 orbits and 64. The 280-placement support has enough freedom to absorb one cut, exactly as the optimal face absorbed A4’s 24. | EXACT ([`lane-a6-saturated-symmetric-plus1.json`](lane-a6-saturated-symmetric-plus1.json)) |
| G13 | **Six atoms separated from the right object break eleven, where twenty-four separated from a dual vertex moved nothing.** Two loop rounds add **6 atom orbits** — two two-of-three and four three-of-five, budget 1 each, floor charges `11/8`, `11/8`, `33/32`, `5/4`, `5/4`, `5/4` — and the fixed-support maximum falls from exactly `11` to **`10.4210526`**, bracketed exactly: an exactly-feasible family of total `325657893/31250000 = 10.421052576` against an exact dual bound `2605263163/250000000 = 10.421052652` on 7 priced rows with `A^T u >= cost` verified in `Fraction`s. Round 1 read `k4` max charge `11/8` (complete), round 2 `5/4` (complete), each in 13 to 15 s. The loop then stops for a reason worth recording rather than for lack of atoms: **the `10.42` optimum has exact maximum depth `105263157/100000000 = 1.05263157`**, above one, so the reader refuses it at K2 as it refused every dual in lanes A3 and A4 — once the atoms bite, the optimum stops being a packing and starts exploiting the site gap again, and the loop would need lane A4’s gate bypass to continue. **Lane A4’s 24 atoms moved the LP by `2.2e-13`; these 6 move the blocking support by `0.579`.** The difference is not the number of atoms but the object they were separated from. | EXACT ([`lane-a6-loop-family-3-recheck.json`](lane-a6-loop-family-3-recheck.json), [`lane-a6-atom-loop.log`](lane-a6-atom-loop.log)) |
| G14 | **The drop is a statement about one support, and the LP has others.** Adding the 6 orbits as columns to the round-one LP — 15,021 x 6,222, 44,330,151 nonzeros, the same 28,237 sites — re-solves to **`11.000000000`** (39,582 iterations, 934.5 s), and **all six new columns carry primal weight exactly zero** while the two-of-three block’s budget rises from `1.034274` to `1.114765` and the dual support from 16 rows to 37. The LP does not use the atoms that break the `1/25` support; it moves to a support they do not cut, exactly as it moved to a new deep cell after every site round. **One atom round on one support is to the atom side what one vertex round on one dual was to the site side.** The atoms do bite on the excess even so: the new dual (296 placements) has exact maximum depth `53703703/50000000 = 1.074074060` at `(1.048581, 1.912500)`, `0.000221` from the nearest site — the **same third structure on the centre line**, `0.017` to the left of G10’s witness and `0.09` shallower. Six atoms take `0.09` off the depth and nothing off the objective. | CHECKED (LP float); the excess and every atom’s validity EXACT |
| G15 | So the shape of the remaining work is now legible, and it is a loop rather than a column count. Each side of the LP has a wide face and a cheap separation, and separating from one point of either face moves the dual rather than the objective. What §10 shows is that the **fixed-support** program *does* converge — six atoms, `0.579` — so the route is to iterate support and atoms together: solve the LP, take its dual’s support, run the fixed-support loop on that support until it falls below eleven, feed every atom back, re-solve. Each LP solve is 400 to 950 s and each fixed-support round about 20 s, so the loop is affordable; what it needs is lane A4’s gate bypass, because the fixed-support optima stop being packings after the first round (their depth reaches `1.0526`). | OPEN |

## 11. Files

**Instruments retained here**, all with a `.py.txt` (or `.sh.txt`) extension, as
[lane X3](lane-x3-containment-atoms-do-not-cut.md) and
`agenda-032/unrun-independent-audit/` already do: they are scratch measurement scripts,
not importable project modules, and the repository’s Python surface is held at zero Ruff
and BasedPyright findings over every tracked `.py` file.
Their bytes are as delivered; nothing was reformatted.

- [`lane-a6-gen-sites.py.txt`](lane-a6-gen-sites.py.txt) — the structural site generator
  of §2.
- [`lane-a6-support-max.py.txt`](lane-a6-support-max.py.txt),
  [`lane-a6-support-max-atoms.py.txt`](lane-a6-support-max-atoms.py.txt),
  [`lane-a6-symmetric-max.py.txt`](lane-a6-symmetric-max.py.txt) — the fixed-support
  maxima; the last is the one that produced the certificate of G8.
- [`lane-a6-ceiling-atoms.py.txt`](lane-a6-ceiling-atoms.py.txt) — is a family feasible
  for a set of threshold-atom orbits, exactly.
- [`lane-a6-cell-widths.py.txt`](lane-a6-cell-widths.py.txt),
  [`lane-a6-site-coverage.py.txt`](lane-a6-site-coverage.py.txt),
  [`lane-a6-analyse-deep.py.txt`](lane-a6-analyse-deep.py.txt) — the deep-region
  measurements G3 to G6.
- [`lane-a6-lp-struct.py.txt`](lane-a6-lp-struct.py.txt) — lane A4’s
  [`lane-a4-lp-atoms.py.txt`](lane-a4-lp-atoms.py.txt) plus `--seed-sites` (§3).
- [`lane-a6-run-atom-loop.sh.txt`](lane-a6-run-atom-loop.sh.txt) — the loop that
  produced G13, driving the reader’s CLI.
- [`lane-a6-atom-loop.py.txt`](lane-a6-atom-loop.py.txt) — a single-process version of
  the same loop, retained unrun: it calls `two_of_three_maximum` directly rather than
  the reader’s CLI, which is faster but returns witnesses as membership-set indices that
  still need `shape_atom` to become points.

**Instruments carried unchanged from the lanes that wrote them**, and therefore already
retained in this directory rather than a second time here:
[`lane-a4-lp-atoms.py.txt`](lane-a4-lp-atoms.py.txt),
[`lane-a3-lp-sites.py.txt`](lane-a3-lp-sites.py.txt),
[`lane-a3-lp383.py.txt`](lane-a3-lp383.py.txt),
[`lane-b-sepcore.py.txt`](lane-b-sepcore.py.txt),
[`lane-a4-flooratoms.py.txt`](lane-a4-flooratoms.py.txt) and
[`lane-a4-excess-and-sites.py.txt`](lane-a4-excess-and-sites.py.txt).

**Results retained here.**

- [`lane-a6-saturated-symmetric-153-40.json`](lane-a6-saturated-symmetric-153-40.json) —
  **the certificate**: 64 admissible placements, D4-symmetric, total exactly 11, depth
  exactly 1, every atom orbit at ratio exactly 1.
- [`lane-a6-reader-saturated-symmetric.json`](lane-a6-reader-saturated-symmetric.json),
  [`lane-a6-reader-sym.log`](lane-a6-reader-sym.log) — the plateau reader’s verdict on
  it, K0 to K6.
- [`lane-a6-ceiling-atoms-saturated-symmetric.json`](lane-a6-ceiling-atoms-saturated-symmetric.json)
  — the independent atom check on it.
- [`lane-a6-saturated-family-at-n-1-exact25.json`](lane-a6-saturated-family-at-n-1-exact25.json),
  [`lane-a6-reader-saturated-153-40.json`](lane-a6-reader-saturated-153-40.json),
  [`lane-a6-reader-saturated.log`](lane-a6-reader-saturated.log),
  [`lane-a6-ceiling-atoms-saturated.json`](lane-a6-ceiling-atoms-saturated.json) — the
  untied 37-placement optimum and its verdicts.
- [`lane-a6-ceiling-atoms-153-40.json`](lane-a6-ceiling-atoms-153-40.json),
  [`lane-a6-ceiling-atoms-153-40-screen1e6.json`](lane-a6-ceiling-atoms-153-40-screen1e6.json)
  — G1.
- [`lane-a6-cell-widths.json`](lane-a6-cell-widths.json) — G5.
- [`lane-a6-structural-sites-153-40.json`](lane-a6-structural-sites-153-40.json) — the
  1,400 structural orbits the LP of G7 actually carried.
- [`lane-a6-dual-round1-structural.json`](lane-a6-dual-round1-structural.json),
  [`lane-a6-dual-round1-structural-rows.json`](lane-a6-dual-round1-structural-rows.json),
  [`lane-a6-excess-round1.log`](lane-a6-excess-round1.log) — the round-one dual and its
  exact excess; [`lane-a6-excess-atoms.log`](lane-a6-excess-atoms.log) is the same for
  the atom-column dual of G14.
- The atom loop of §10: [`lane-a6-atom-loop.log`](lane-a6-atom-loop.log),
  `lane-a6-loop-family-{1,2,3}.json`,
  [`lane-a6-loop-family-3-recheck.json`](lane-a6-loop-family-3-recheck.json) (the
  exactly bracketed `10.42` optimum), `lane-a6-loop-reader-{1,2,3}.json`,
  `lane-a6-loop-atoms-{1,2}-{0,1,2}.json` (the six separated atoms),
  [`lane-a6-atom-from-certificate.json`](lane-a6-atom-from-certificate.json) and
  [`lane-a6-saturated-symmetric-plus1.json`](lane-a6-saturated-symmetric-plus1.json)
  (G12), and
  [`lane-a6-seed-atoms-from-certificate.json`](lane-a6-seed-atoms-from-certificate.json)
  (the six in the LP/freeze record shape).
- The run logs: [`lane-a6-gen.log`](lane-a6-gen.log),
  [`lane-a6-gen-all.log`](lane-a6-gen-all.log),
  [`lane-a6-gen-x4000.log`](lane-a6-gen-x4000.log),
  [`lane-a6-lp-struct.log`](lane-a6-lp-struct.log),
  [`lane-a6-lp-struct-atoms.log`](lane-a6-lp-struct-atoms.log) and
  [`lane-a6-lp-struct-x4000.log`](lane-a6-lp-struct-x4000.log).

**Not retained (scratch only), with the reason and the rebuild cost.** The retention
rule here is the one lane X3 used — retain the receipts the findings cite, leave behind
what a retained script rebuilds — and it is applied more sharply than usual because the
mutation-snapshot cap in `devtools.run_negative_controls` had 34,954,039 bytes of
headroom when this lane was retained.

| left in scratch | bytes | why |
| --- | ---: | --- |
| `deep-region-all.json`, the 17,885 deep orbits with exact depths | 11,597,001 | rebuilt by `lane-a6-gen-sites.py.txt` in 14.6 s; the census G3-G6 draws from it is tabulated in §4 |
| `structural-sites-flat.json`, the same points unfolded | 6,074,520 | a view of the file above, rebuilt with it |
| `structural-sites-153-40-x4000.json`, round two’s 4,000-orbit set | 2,567,953 | rebuilt in 15.4 s, and round two is OPEN, so nothing cites it |
| `lp-struct/`, `lp-struct-atoms/`, `lp-struct-x4000/`, the three LP checkpoints | 52,782,351 | each is dominated by copies of the pre-existing `atoms.json` and `rows.json` inputs; the dual dumps the findings cite are retained above as separate files |

**Inputs, all pre-existing scratch from the earlier lanes**: the `sites-1` checkpoint,
the seven `153/40` duals, the `191/50` ceiling family
([`ceiling-family-191-50.json`](ceiling-family-191-50.json)) scaled to `153/40`, and the
2,566-orbit atom set.

Nothing tracked was edited by the lane, and the lane committed nothing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
