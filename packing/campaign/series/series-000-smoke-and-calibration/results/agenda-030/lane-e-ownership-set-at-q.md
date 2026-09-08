# Agenda 030, lane E: A robust unavoidable set of at most eleven marks at 96/25

Retained lane report for BC-302 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md),
testing [H-134](../../../../hypotheses/H-134-eleven-mark-ownership-set.md) in
session-104 on 2026-09-08, written by a research lane at maximum effort in one 2.5-hour
block on a four-core machine shared with seven other agents (load average 4 to 9 beside
every wall time below; none is comparable with the planning lane’s). The report carries
its own status labels (proved, certified, exact-verified, search reading, open); nothing
here is a registered experiment or a new bound on `s(11)`.

## E — Is there a robust unavoidable set of at most eleven marks at 96/25?

Conventions.
`q = 96/25`, container `S = [0, q]²`, `δ = 3/500` (the transfer tolerance of
X-021’s Lemma T). A *mark* is a point or a closed segment; it is *thickened* by `δ`, so
a closed unit square `Q ⊂ S` *meets* the mark `m` iff `dist(Q, m) ≤ δ`. A mark set `M`
is *robustly unavoidable* iff every contained closed unit square, at every angle, meets
some mark of `M`. An *escape* of `M` is a contained closed unit square with
`dist(Q, m) > δ` for every `m ∈ M`. Poses are `(cx, cy, t)` with `t = tan(θ/2)`
rational, `cos θ = (1 − t²)/(1 + t²)`, `sin θ = 2t/(1 + t²)` (exp-121’s frame), corners
`(cx, cy) + ((a cos θ − b sin θ)/2, (a sin θ + b cos θ)/2)` for
`(a, b) ∈ {(−1,−1), (1,−1), (1,1), (−1,1)}`. Stromquist’s Figure-13 points at `q` are
`P10 = {(1, 1), (48/25, 1), (71/25, 1), (27/50, 48/25), (73/50, 48/25), (119/50, 48/25),
(33/10, 48/25), (1, 71/25), (48/25, 71/25), (71/25, 71/25)}`.

Thickening is on the hypothesis’s side: it enlarges every mark, so it makes covering
easier and escaping harder, and every escape below clears its marks by more than `δ`.

## 0. Findings in one page

- **A robust unavoidable set of ten marks exists, and its cover is certified** (Section
  6). Replace each point of `P10` by the horizontal segment of length `1/10` centred on
  it. Every contained closed unit square at `q` is within `δ` of one of these ten
  segments: an interval reader over the pose space `(t, cx, cy)` certifies the whole
  domain with `404 613` boxes and `184 756` certified leaves, no failure, in `13.5 s`;
  the same holds with the centre point added, and at segment length `9/100`. At length
  `8/100` the reader leaves `3 626` boxes uncertified; at `7/100` the `45°` square on a
  wall is a genuine escape again.
  The falsifier’s reading is stronger than the certified statement: at resolution `0.01`
  and `0.75°` and at `300` random poses every square actually meets a segment (distance
  `0`), which is not proved.
  The certification is floating point with an explicit `10⁻⁹` allowance against a
  rounding error below `10⁻¹²`; the exact re-check in `fractions.Fraction` of every
  certified leaf and every discarded box passed (`184 756` leaves, `17 551` discards, no
  failure, `79 s`), and 6 000 random poses inside 3 000 random certified leaves are
  within `δ` of a mark by the falsifier’s exact distance.
- **Every point set tested has an exactly verified escape, and the best point set found
  is `0.008` short of the tolerance** (Sections 4 and 5). The catalogue holds the
  escapes of the four sets the cell named — T-018’s eleven heaviest atoms scaled to `q`,
  a greedy cover from its 93 heaviest atoms, `P10`, and `P10` plus one point — and of
  the optimised sets: the best K4-symmetric eleven-point set leaves a `45°` square on
  the middle of a side wall at exact distance `0.01401` from every mark, and the free
  22-parameter search from it does no better (`0.01720`). Twenty-two catalogued escapes
  were re-read by an independent standard-library reader with no disagreement.
- **Why the atom skeleton fails.** T-018’s heavy atoms are the corners and the centre;
  the eleven heaviest leave the wall strips bare (an axis square there is `0.41` from
  every mark), and every set with rows `0.92` apart is escaped by a `45°` square resting
  on a wall between two row marks: it cuts the row line in a chord of half-length
  `√2 − 1 = 0.4142`, so point rows would need spacing at most
  `2(√2 − 1) + 2√2·δ = 0.845`. A segment of half-length `1/20` reaches `0.0354` towards
  that square and its clearance from the row points is `0.0319`; that `0.0035` is why
  length `1/10` works and `7/100` does not.
- **Three facts proved** (Section 3): no LP, pigeonhole or counting argument can refute
  H-134, because T-018 scaled by `384/381` is a fractional cover of mass `10.863675` for
  `δ`-rounded unit squares at `q`; ten marks of any robust unavoidable set are localised
  to the `δ`-neighbourhoods of the ten squares of the `n = 10` optimal packing scaled to
  `q`, and no eleven such squares exist; no D4-symmetric eleven-set exists and every K4-
  or C2-symmetric one contains the centre.
- **What it buys and what it does not.** H-134’s claim is met by ten short segments, so
  every square of every packing of eleven unit squares in `S` lies within `δ` of a known
  mark: the localisation that collapses route (a)'s tree.
  Exactly-one ownership does not follow: eleven squares and ten marks force one mark to
  serve two squares, and a segment can be shared by two squares touching along a line
  through it, which is why this is not a proof that eleven squares do not fit at `q`. An
  exact refutation engine for point sets was built and did not close (Section 5.2).
- **Recommended status for H-134: accepted for the segment form at length `1/10`,
  pending the exact re-check below and an independent replay; the point form is open
  with every tested set refuted.** The claim to freeze, which needs an experiment id and
  an independent reader run, is Theorem E.4 of Section 6.

## 1. Falsifiers, stated before the runs

- **Falsifier of a candidate set** (every run in Sections 4 and 5). A contained closed
  unit square at a rational pose with exact distance `> 3/500` to every mark, decided by
  two independent exact formulas that must agree (Section 2). A “no escape found” is a
  search reading at the stated resolution, never a theorem.
- **Falsifier of the hypothesis’s point form** (Section 5.2). A finite family of
  contained unit squares such that no eleven points are within `δ` of all of them,
  decided by an exact branch-and-bound whose relaxation is sound.
  A surviving branch is not evidence for the hypothesis; a dead tree is a theorem.
- **Falsifier of a survivor’s proof** (Section 6). A box of pose space that the reader
  cannot certify at its floor, reported with its centre pose; or a certified leaf that
  the exact re-check rejects; or an error in the Lipschitz bound of Section 6.1.

## 2. The engine and its verification

`escape_engine.py` (Appendix) has three stages.

1. **Grid.** Angles `0°, 1.5°, …, 88.5°`; for each, centres on a grid of step `0.02`
   over the exact containment box `[w/2, q − w/2]²`, `w = |cos θ| + |sin θ|`; the margin
   `g = min_m dist(Q, m) − δ` is evaluated in numpy for every pose (about 1.2 million
   poses for eleven marks in under a second).
   Segment marks are sampled at nine points for the float stage only.
2. **Refinement.** Nelder–Mead on `(cx, cy, θ)` from the best forty grid poses, with the
   centre projected onto the containment box at every evaluation; duplicates within
   `0.02` are merged.
3. **Exact decision.** The refined pose is snapped to rationals (`t` first, then the
   centre clipped into the exact containment box for that `t`, denominators `10³` to
   `10⁶` tried in turn) and verified: all four corners in the closed container, and for
   every mark `dist(Q, m) > δ` by two methods that must agree or the run aborts — (A)
   the local-frame formula `dist² = (|u| − ½)₊² + (|v| − ½)₊²`; (B) the separating-axis
   theorem for two convex polygons, with the square’s two edge normals, the segment’s
   normal, and every vertex-pair direction as candidates, the gap `> δ` decided as
   `gap > 0` and `gap² > δ²|d|²` in unnormalised direction `d`. For a segment mark (B)
   decides and (A) is checked at both endpoints.

Self-tests (`selftest.py`, Appendix), all passed:

| Test | Expected | Observed |
| --- | --- | --- |
| Lane C’s exact escape of P10 at `q`: centre `(73/50, 67/50)`, `t = 49/200` | escape, least margin `14979/1060025` | escape, `min dist 0.0141308` (equal to the retained value to 15 digits) |
| exp-121’s frozen square at `1939/500`, `t = 1/1000`, twelve points, `δ = 0` | strict escape | strict escape, least distance `0.000199`; against `δ = 3/500` it is *not* an escape |
| Search on P10 at `q` | finds an escape | finds four, the largest at the bottom wall (Section 4) |
| Control: points on a `0.3` grid | no escape | best float margin `−0.006`, none verified |
| Control: three full-width segments at `y = 1, q/2, q − 1` | no escape (every unit square has vertical extent `≥ 1 > 0.92`) | best float margin `−0.006`, none verified |
| Axis square `0.01` above a segment / `0.005` above it | escape / not | escape / not |

A third, independent reader (`reader.py`, standard library only, no import of the
engine: exp-121’s edge determinants for membership, point-to-edge distances otherwise,
and for a segment the minimum over its endpoints and the square’s corners, since the
distance between convex polygons is attained at a vertex) re-read all 22 catalogued
escapes of the point sets with no disagreement.

What was reused from exp-121: the rational half-angle frame, closed membership, and the
support-width containment test.
What is new: the search stages, the distance-above-`δ` decision (exp-121 decides strict
avoidance only), segment marks, the two-method agreement check, and the interval reader
of Section 6.

## 3. Structural facts proved in the block

**Lemma E.1 (no LP obstruction; proved).** The fractional relaxation of H-134 has value
at most `434547/40000 = 10.863675 < 11`. *Proof.* Scale T-018’s measure by `λ = 384/381`
from side `381/100` to `q`. Every closed square of side `λ` at any angle inside `S`
contains a `λB`-square at a net angle, hence carries mass `≥ 4001/4000`. The
`δ`-neighbourhood of a unit square `Q` contains the concentric square of side
`1 + √2·δ = 1.008485…` in `Q`’s frame (a point with `|u|, |v| ≤ ½ + δ/√2` is within
`√(2·(δ/√2)²) = δ` of `Q`), and `1 + √2·δ > λ = 1.007874…`, so every `δ`-rounded unit
square carries mass `≥ 4001/4000 ≥ 1`. ∎ Consequently no counting, pigeonhole or LP
argument can refute H-134; only the integrality gap can, and that needs a case analysis
over mark positions, which Section 5.2 mechanises.

**Lemma E.2 (ten forced marks; proved, exact-verified).** Let `G₁, …, G₁₀` be the
squares of the `n = 10` optimal packing (side `3 + 1/√2`) scaled to `q`, at the rational
poses of `tests-gobel.json` (the two `45°` squares at `t = 41/99`). They are contained
and pairwise at exact distance `> 2δ = 3/250` (`tests_gobel.py`, separating-axis
decision). Hence any robustly unavoidable set has ten distinct marks `m_i` with
`dist(m_i, G_i) ≤ δ`. Eleven such squares cannot exist: they would be eleven squares of
side `1 + 2δ` with disjoint interiors in a container of side `q + 2δ = 3.852`, that is
eleven unit squares at side `3.852/1.012 = 3.806 < 3.81`, against T-018. So a set of
eleven marks is *ten localised marks plus one free mark*, and a set of ten marks, such
as Theorem E.4’s, is entirely localised: each of its marks is within `δ` of its own
`G_i`.

**Lemma E.3 (symmetry; proved).** No D4-symmetric eleven-set exists: D4 orbits in `S`
have size 1 (the centre), 4 or 8, and `11 − 1 = 10` is not a sum of 4s and 8s. Every
K4-symmetric (two centreline reflections) or C2-symmetric (half-turn) eleven-set
contains the centre, because all other orbits have even size.
Stromquist’s ten-point scheme is K4-symmetric (`2 + 4 + 4`), so its only symmetric
eleven-point extension adds the centre.

## 4. Candidate sets and the escape catalogue

Coordinates are exact rationals in the `set-*.json` blocks of the Appendix, decimals
here. Search resolution for every row: grid step `0.02`, angle step `1.5°`, forty grid
poses refined, then exact decision; wall time per set `0.6` to `10 s` at load `4` to
`8`. Every escape listed was verified exactly by both methods, and the point-set rows by
the independent reader; the poses shown are the small-denominator forms of
`clean_pose.py`, each re-verified exactly.

| Set | Marks | Best escape: centre, `t`, angle | Least exact distance | Marks it clears least |
| --- | --- | --- | --- | --- |
| W11: T-018’s eleven heaviest atoms scaled by `384/381` (four corners, the centre `(48/25, 48/25)`, six of the eight atoms of the `33/500` orbit) | 11 points | `(48/25, 1/2)`, `t = 0`, `0°` | `0.41449` | both bottom corner atoms at `0.41449` |
| G11: greedy set cover of a pose sample (step `0.04`, `3°`) by the 93 heaviest atoms scaled to `q` | 11 points | `(3/2, 26473/8450)`, `t = 5/12`, `45.24°` | `0.06310` | `(1.0009, 2.8348)` at `0.0631`, `(2.0045, 2.8369)` at `0.0667` |
| P10: Stromquist’s Figure-13 points at `q` | 10 points | `(73/50, 239/338)`, `t = 5/12`, `45.24°` (and three K4 images) | `0.03188` | `(48/25, 1)` at `0.03188`, `(1, 1)` at `0.03287` |
| P10C: P10 plus the centre | 11 points | same as P10 | `0.03188` | same |
| P10 + one point optimised by the min–max (Section 5.1) | 11 points | same as P10 | `0.03188` | same; the added point at `(2.31, 2.73)` kills one of four symmetric images |
| K4 optimum, polished (Section 5.1) | 11 points | `(239/338, 48/25)`, `t = 5/12`, `45.24°` | `0.01634` (`0.01401` for the polished set) | `(1.0122, 1.4943)` at `0.0163`, `(1.0122, 2.3457)` at `0.0171` |
| Free optimum from the K4 optimum | 11 points | `(3.133, 171/89)`, `t = 403/972`, `45.04°` | `0.01720` | the right column’s two middle marks |
| K4S: the polished K4 optimum’s marks as segments of length `1/10`, `1/5`, `3/10` along their columns | 11 segments | `(1/2, 7/5)`, `t = 0`, `0°` | `0.01401` (all three lengths) | the left column’s marks, which sit at `x = 1.014 > 1 + δ` |
| S10C at length `7/100` and `6/100`: P10 as horizontal segments plus the centre | 11 | `(119/50, 178056263/56834450)`, `t = 408/985`, `45.00°` | `0.00763`, `0.01116` | the two top-row segments |
| S10 at length `1/10`, S10C at `1/10` and `9/100` | 10 or 11 segments | none found (best float margin `−0.006`: every refined pose meets a mark) | — | Section 6 |
| S10C at length `8/100` | 11 segments | none found; best pose at exact distance `0.00409 < δ` | — | unresolved: within `δ` at the search resolution, not certified |

W11 fails for a structural reason: the heavy atoms of the certificate are corner and
centre atoms, and the eleven heaviest leave the whole bottom and top wall strips
`[1.42, 2.42] × [0, 1]` bare.
G11’s greedy cover reproduces the three-row structure (rows at `y ≈ 1, 1.92, 2.84`) but
runs out of marks before the `45°` squares at the top and bottom walls are served.
P10’s four escapes are the K4 images of one `45°` square resting on a wall between two
row points `0.92` apart.
One added point cannot kill four symmetric escapes.
The K4 segment set fails because its outer columns sit `0.014` outside the wall’s unit
strip, so the axis squares along the wall are missed whatever the segment length.

## 5. The adversarial min–max and the exact branch-and-bound

### 5.1 The adversarial min–max

`minimax.py` minimises `φ(M) = max_pose (min_m dist(Q_pose, m) − δ)` over a fixed pose
grid (step `0.06`, angle step `4°`, 53 000 poses) with Powell then Nelder–Mead;
`polish.py` then refines the best set at full resolution by a pool cutting-plane (the
falsifier’s twenty best poses join a pool each round, the marks are moved to minimise
the pool’s largest margin, and the pool only grows).
Every number below is a search reading; the exact clearance is the falsifier’s verified
least distance for the final set.

| Family | Parameters | Starts | Coarse `φ` at the end | Exact least clearance of the best set’s escape | Wall, load |
| --- | --- | --- | --- | --- | --- |
| P10 plus one free point | 2 | 6 | `0.0234` | `0.03188` | `23 s`, `4.3` |
| K4-symmetric: centre, one midline pair, two generic orbits | 5 | 10 | `0.0064` (nine of ten starts below `0.0105`) | `0.01401` after 25 polish rounds (`0.01634` before) | `9.6 min` + `3 min`, `5` to `8` |
| K4-symmetric: centre, two vertical and one horizontal pair, one orbit | 5 | polish only, 20 rounds | — | `0.02376` | `3 min`, `7` |
| K4-symmetric: centre, three vertical pairs, one orbit | 5 | polish only, 20 rounds | — | `0.21` | `3 min`, `7` |
| Free, 22 coordinates, from the polished K4 optimum | 22 | 2 | `0.0059` | `0.01720` | `6 min`, `7` |
| Free, 22 coordinates, pool polish from the K4 optimum | 22 | 25 rounds | — | unstable, `0.15` to `0.33`: Nelder–Mead overfits the pool and opens holes elsewhere | `3 min`, `7` |

The polished K4 optimum (exact rationals in `set-POLISH-k4.json`, Appendix) is a
three-column arrangement rather than Stromquist’s three rows: a middle column
`x = 48/25` with three points (`y = 1.014, 1.92, 2.826`) and two outer columns with four
points each (`x ≈ 1.014` at `y = 1.50, 2.34`, `x ≈ 0.988` at `y = 0.818, 3.022`, and
their mirror images).
The outer columns serve the side walls’ `45°` squares with offset `a ≈ 0.31` from the
wall’s centre line `x = √2/2`, so each point serves a `cy`-interval of half-length
`√2/2 + √2·δ − a ≈ 0.41`, and four points cover the wall’s `cy`-range of length `2.426`
only if their gaps stay below `0.82`; the middle gap is `0.84`, which is the escape.
Closing that gap moves the two middle points onto the interior `45°` squares’ holes.
The trade-off is what the min–max measures, and the segment form of Section 6 is what
resolves it: a horizontal segment on a row reaches the wall square along the diagonal
direction that a point cannot.

### 5.2 The exact branch-and-bound

`branch.py` decides, for a finite family of contained unit squares `T_1, …, T_N`,
whether eleven points can be within `δ` of all of them, by a sound relaxation:

- the `δ`-neighbourhood of `T` is replaced by the octagon
  `O(T) = {|u| ≤ ½ + δ, |v| ≤ ½ + δ, |u| + |v| ≤ 1 + 17/2000}` in `T`’s frame, a
  superset because the support of the rounded square in the diagonal direction is
  `1 + √2·δ ≤ 1 + 17/2000`;
- each mark carries a feasible region, a convex polygon with rational vertices,
  initially the container; assigning `T` to a mark clips its region by `O(T)`
  (Sutherland–Hodgman, exact, closed half-planes, degenerate regions kept);
- the search assigns the most constrained test square first, branching over the marks
  whose regions meet its octagon (a float bounding-box prefilter with a `10⁻⁹` outward
  margin skips certain misses; every other decision is exact), and over at most one
  still-untouched mark, since marks are interchangeable;
- fewer than eleven marks is eleven marks with repeats, so eleven is without loss.

A dead tree is a theorem: no eleven points are within `δ` of every `T_j`, hence no
robust unavoidable eleven-point set exists.
A surviving branch is not evidence for H-134; it yields regions from which `loop.py`
builds a candidate (the vertex average of each region), runs the falsifier, and adds the
exact escapes as new test squares.

Run A (seed: the ten Göbel squares of Lemma E.2 plus the 19 catalogued escapes of the
named sets; up to six escapes added per round): 28 rounds in `4 min` at load `6`, 150
test squares, every tree alive, node count equal to the number of tests plus one at
every round (each test square had a unique possible server), the candidates’ escapes
clearing by `0.05` to `0.20`. The loop was stopped: its candidate generator does not
optimise inside the regions, so the finite family never approached infeasibility.
Its 155 test squares are retained (`tests-A.json`) for a session that wants the
point-form negative; the tree’s shape says the cost is in choosing test squares that
empty regions, and the min–max escapes are the natural choice.

### 5.3 Segment marks reduce to point marks for refutation

A segment of length at most `ℓ` thickened by `δ` lies in the disc of radius `δ + ℓ/2`
about its midpoint, so a point-mark refutation at tolerance `δ + ℓ/2` covers every mark
set with segments of length at most `ℓ`. Since segments of length `1/10` suffice
(Section 6), no such refutation can exist at tolerance `δ + 1/20 = 0.056`: the
branch-and-bound at that tolerance must stay alive, which is a consistency check the
next session can run.

## 6. Proved nonavoidance: the ten-segment set

### 6.1 The interval reader

`cover_reader.py` (Appendix) proves a statement of the form “every contained closed unit
square is within `δ` of some mark of `M`” by an adaptive cover of the pose space
`[0, 1] × [½, q − ½]²` in `(t, cx, cy)`; `t ∈ [0, 1]` is every orientation modulo a
quarter turn and every contained square has its centre in `[½, q − ½]²`.

For a point `p` with coordinates `(u, v)` in the square’s frame, let
`f(P, p) = max(|u| − ½, |v| − ½)`. Then `dist(Q(P), p)² = (|u| − ½)₊² + (|v| − ½)₊²
≤ 2·max(f, 0)²`, so `f ≤ τ := 2121/500000 < δ/√2` gives `dist ≤ √2·τ < δ`. For a segment
mark, `f_seg(P) = min_p f(P, p)` over the segment; `f(P, ·)` is convex and piecewise
linear along the segment, so the minimum is at an endpoint or at a breakpoint (`u = 0`,
`v = 0`, `u = ±v`), each the root of an affine equation.

*Lipschitz bound.* Over a box with half-widths `(ht, hx, hy)` about `P₀ = (t₀, x₀, y₀)`
and any pose `P` in it: the centre moves by at most `hx + hy` in Euclidean norm, and the
frame vectors `(cos θ, sin θ)`, `(−sin θ, cos θ)` move by at most
`2 sin(|Δθ|/2) ≤ |Δθ| = 2|atan t − atan t₀| ≤ 2·ht`. With `u = ⟨(cos θ, sin θ), p − c⟩`,
`|Δu| ≤ |Δc| + |Δ(cos θ, sin θ)|·|p − c| ≤ (hx + hy) + 2·ht·(R + hx + hy)`, where
`R ≥ |p − (x₀, y₀)|` is taken as the L1 distance, and the same for `v`. Hence

`f(P, p) ≤ f(P₀, p) + hx + hy + 2·ht·(R + hx + hy)` for every `P` in the box,

and for a segment the bound holds with `R` the larger endpoint’s L1 distance, because
the minimum of functions with a common Lipschitz bound has that bound.
A box is *certified* by a mark when the right-hand side is at most `τ`; then every pose
in the box is within `δ` of that mark.
A box is *discarded* only when it contains no contained pose: `x₂ < w_min` or
`x₁ > q − w_min` (or the same in `y`), where `w_min` is the least half-width
`(cos θ + sin θ)/2` over the box’s `t`-range, attained at an endpoint since `w` is
unimodal on `[0, 1]`. Otherwise the box is split along its widest scaled dimension
(`3·ht`, `hx`, `hy`). A box below the floor `2·10⁻⁴` that is neither certified nor
discarded is a failure, reported with its centre pose.

*Arithmetic.* The certification runs in IEEE doubles with an explicit allowance: a box
is certified only if the bound is at most `τ − 10⁻⁹`, and discarded only with the same
allowance on the conservative side.
Every certification is fewer than two hundred additions, multiplications, absolute
values and comparisons on quantities below ten, each with relative error at most `2⁻⁵³`,
so the accumulated absolute error is below `10⁻¹²`, four orders of magnitude inside the
allowance. Approximate breakpoints in `f_seg` can only raise the computed minimum, which
is the conservative direction.
The exact mode re-certifies every certified leaf in `fractions.Fraction` with the
rational `τ` and no allowance.

### 6.2 The certified sets and the threshold in the segment length

| Set | Marks | Falsifier (step `0.02`, `1.5°`) | Reader: boxes, certified leaves, discarded, failures, wall, load |
| --- | --- | --- | --- |
| S10 at length `1/10`: the ten horizontal segments `[x − 1/20, x + 1/20] × {y}`, `(x, y) ∈ P10` | 10 | no escape; every refined pose meets a mark | `404 613`, `184 756`, — , `0`, `13.5 s`, `7.7` |
| S10C at `1/10`: S10 plus the centre point `(48/25, 48/25)` | 11 | as above; also at step `0.01`, `0.75°` (`48 s`) and at 300 random contained poses, all at distance `0` | `349 507`, `157 203`, `17 551`, `0`, `8.3 s`, `6.9` |
| S10C at `9/100` | 11 | no escape; best pose at distance `0.00056` | `432 993`, `197 007`, — , `0`, `10.2 s`, `7.7` |
| S10C at `8/100` | 11 | no escape; best pose at distance `0.00409 < δ` | `659 921`, `292 913`, — , `3 626` failures at the floor, `14.1 s` — not certified |
| S10C at `7/100` | 11 | escape, clearance `0.00763` | — |

**Theorem E.4 (certified; exact re-check passed: every certified leaf and every
discarded box re-decided exactly).** Let `M₁₀` be the ten closed horizontal segments of
length `1/10` centred at the points of `P10` in `S = [0, 96/25]²`. Every closed unit
square contained in `S`, at any angle, is at Euclidean distance at most
`√2·2121/500000 < 3/500` from some segment of `M₁₀`. The same holds for `M₁₀` with the
centre point added and for the segments of length `9/100`.

*What is and is not proved.* The theorem is the thickened statement H-134 asks for.
The falsifier’s reading that every square actually meets a segment (distance `0`) is not
proved and cannot be by this reader, whose slack at a tangency is zero.
The certification is a floating-point computation with a documented error bound,
replayable in `14 s`; the exact re-check of every leaf is the standard the record asks
for, and an independent reader with its own bound is the standard the closing route
should demand before the theorem is used.
At length `8/100` the reader’s floor was too coarse for a slack of `0.002`; a finer
floor would decide it and was not run.

*A second reader, written and not completed.* `cover_reader2.py` (Appendix) certifies a
box by a different bound, the Hausdorff one on the Euclidean distance itself:
`dist(Q(P), m) ≤ dist(Q(P₀), m) + hx + hy + √2·ht`, decided exactly as
`dist² ≤ (δ − hx − hy − 14143/10000·ht)²` with the vertex formulas of `reader.py` and no
detour through `f` and `τ`. Its float cover did not finish within two bounded runs of
`9` and `7` minutes at load `10` to `14`: the bound’s L1 centre term is looser than the
frame bound’s, so it needs more boxes, and its per-box cost is about sixty
point-to-segment distances against the first reader’s ten frame evaluations.
The full exact pass it started at 05:30 was stopped after ten minutes.
It is the replay the next session runs first, with a vectorised cover or a coarser first
level.

### 6.3 What Theorem E.4 buys

- **Localisation for route (a).** In any packing of eleven unit squares in `S` each
  square is within `δ` of one of ten known segments, all lying on the three rows
  `y = 1, 48/25, 71/25`. Since a packing at any side `s ≤ q` dilates to a packing of
  unit squares in `S`, the statement holds for every side up to `q` with no further
  tolerance. This is the collapse X-021 priced: the branching over which mark each square
  sits near is at most `10¹¹` labelled choices before symmetry and exclusion, and the
  marks themselves were not taken from the certificate but from Stromquist’s rows with
  the one change that a chord argument demands.
- **Not exactly-one ownership.** Eleven squares and ten marks force one mark to serve
  two squares, and a segment can be shared by two squares touching along a line that
  crosses it; the pigeonhole that finishes Stromquist’s `n = 10` proof does not apply.
  The eleventh mark that H-134 allows is free; whether it can be placed so that some
  ownership argument survives is a question for the closing route, not for this lane.
- **The certificate’s shape.** T-018’s heavy atoms could not do this; the marks that
  work are Stromquist’s, thickened along their rows.
  The dual measure and the integral set live on different supports, which is the
  integrality gap of Lemma E.1 made concrete.

## 7. Obstructions, status of H-134, and what the next session does first

- **The atom skeleton is the wrong shape for an integral set.** T-018’s mass sits on the
  corners, the centre and near-wall orbits at row spacing `0.92`, which is the spacing
  the wall `45°` squares defeat; no set of eleven points built from its 93 heaviest
  atoms survives, and the greedy cover fails at the walls.
- **Point marks are `0.008` short at the search resolution.** The best point set found
  by the min–max (three columns, four marks in each outer column) still has a wall `45°`
  escape of clearance `0.014`; the point form of H-134 is neither refuted nor
  established, and the exact refutation engine did not close with its weak candidate
  generator.
- **The segment form is settled by a chord.** A wall `45°` square cuts a row in a chord
  of half-length `√2 − 1` and clears the row points by `0.0319`; a half-length of `1/20`
  reaches `0.0354` along the diagonal and closes it.
  The threshold lies in `(7/100, 9/100]`.
- **The proof is a computation.** Theorem E.4 rests on the Lipschitz bound of Section
  6.1 and a floating-point cover with an explicit allowance, re-checked exactly; it is
  not a hand proof by Stromquist’s Lemmas 1–4, which were not needed.

**Recommended status for H-134:** accepted for the segment form (ten segments of length
`1/10`, hence at most eleven marks), pending the exact re-check reported above and an
independent replay under a registered experiment; open for the point form, prior for
that form lowered from about thirty per cent to about ten.
A claim is frozen and needs an experiment id: Theorem E.4 with `set-S10-l0.1.json` as
its exact input and `cover_reader.py` as its reader.

**What the next session does first.** Replay Theorem E.4 under the experiment id with an
independent reader (a different bound, for instance the exact separating-axis distance
at the box corners with the same Lipschitz constant), then register it.
Then decide the two questions it opens: whether the free eleventh mark can restore an
ownership argument (a point that no two squares of a packing can share, placed where the
ten segments are most often shared), and whether ten segments can be shortened to points
by moving the rows, which the min–max says they cannot with eleven points at this
tolerance.
The point-form negative, if wanted, runs the branch-and-bound with the min–max
escapes as test squares and a candidate generator that polishes inside the regions.

## 8. Inputs and resources

- Container side `q = 96/25`; tolerance `δ = 3/500`; every mark set as exact rationals
  in the `set-*.json` blocks of the Appendix; atoms scaled from `381/100` to `q` by
  `384/381`.
- Search resolution for every catalogue row and every polish round: grid step `0.02`,
  angle step `1.5°` (60 angles), the forty best grid poses refined by Nelder–Mead
  (`xatol 10⁻⁹`), rationalised at denominators `10³` to `10⁶`; the min–max’s coarse grid
  is step `0.06`, angle step `4°`. Greedy cover sample: step `0.04`, angle step `3°`.
  Seeds: `numpy.random.default_rng(1)` for the random starts, `random.seed(3)` for the
  300 spot-check poses; the named sets have none.
- Reader: floor `2·10⁻⁴` on the scaled half-widths, node limit `4·10⁶`, `τ =
  2121/500000`, allowance `10⁻⁹`.
- Exact decisions: `fractions.Fraction` throughout the falsifier’s final stage, the
  independent reader, the Göbel distances and the reader’s exact mode; two independent
  distance methods that must agree; corners in the closed container.
- Wall times with the load average beside each (four cores shared with seven other
  agents, one worker per job, `PACK_JOBS=1`): engine self-test `2 s` at `4.3`; each
  named point set `0.6` to `1.0 s` at `4.3`; segment sets `6` to `10 s` at `7.7`;
  min–max and polish as tabulated in Section 5.1; the exact loop `4 min` at `6`; the
  reader `8` to `14 s` at `6.9` to `7.7`; the exact re-check `79` to `92 s` at `6` to
  `9`, and the leaf sanity sample `29 s` at `9`.
- Interpreter: the project’s Python 3.14.7 with numpy 2.5.2 and scipy 1.17.1 from the
  frozen environment; no repository code was modified; `sqpack.cover` and the exp-121
  instruments were read, and exp-121’s frame and containment conventions reused.

## Appendix: scripts and data as run

### `escape_engine.py`

```text
"""Escape engine for BC-302 (H-134): robust unavoidable sets of marks at side q.

Given a mark set (points or segments, exact rationals) in the container [0, q]^2 and a
thickening delta, search for a closed unit square Q, contained in the container, whose
Euclidean distance to every mark exceeds delta.  The search is float (numpy grid, then
Nelder-Mead); the result is a rational pose (cx, cy, t) with t = tan(theta/2), verified
exactly in two independent ways:

  (A) local frame: for a point mark, du = max(|u| - 1/2, 0), dv = max(|v| - 1/2, 0) with
      (u, v) the mark in the square's frame; dist^2 = du^2 + dv^2 > delta^2.  For a
      segment mark, the distance is the minimum of a convex function on the segment; it
      is computed exactly by (B) and cross-checked by (A) at the segment's endpoints and
      at the exact foot of the closest square feature.
  (B) separating axes: for two convex polygons (the square and the mark as a 1- or
      2-vertex polygon) the distance is max over candidate directions (both polygons'
      edge normals and all vertex-pair directions) of the separation gap; gap > delta is
      decided as (min_B <d,b> - max_A <d,a>) > 0 and its square > delta^2 |d|^2.

A pose is reported as an ESCAPE only if both (A) and (B) decide dist > delta for every
mark and all four corners lie in the closed container.  "No escape found" is a search
reading at the declared resolution, never a theorem.

Frame convention (exp-121's): cos = (1 - t^2)/(1 + t^2), sin = 2t/(1 + t^2), corners
centre + (a cos - b sin, a sin + b cos)/2 for (a, b) in (-1,-1), (1,-1), (1,1), (-1,1).

Run from packing/ with the project interpreter (Python 3.14, numpy, scipy).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from fractions import Fraction as F

import numpy as np
from scipy.optimize import minimize

Q_DEFAULT = F(96, 25)
DELTA_DEFAULT = F(3, 500)

# ---------------------------------------------------------------- mark parsing

def parse_marks(spec):
    """spec: list of {"kind": "point", "xy": [x, y]} or {"kind": "segment", "a": [..], "b": [..]}
    with rational strings; returns list of ('point', (F, F)) / ('segment', (F,F), (F,F))."""
    out = []
    for m in spec:
        if m["kind"] == "point":
            out.append(("point", (F(m["xy"][0]), F(m["xy"][1]))))
        elif m["kind"] == "segment":
            out.append(("segment", (F(m["a"][0]), F(m["a"][1])), (F(m["b"][0]), F(m["b"][1]))))
        else:
            raise ValueError(m)
    return out


def marks_to_spec(marks):
    spec = []
    for m in marks:
        if m[0] == "point":
            spec.append({"kind": "point", "xy": [str(m[1][0]), str(m[1][1])]})
        else:
            spec.append({"kind": "segment", "a": [str(m[1][0]), str(m[1][1])],
                         "b": [str(m[2][0]), str(m[2][1])]})
    return spec


def marks_float(marks):
    """Segments as (ax, ay, bx, by); points as degenerate segments (a == b)."""
    arr = []
    for m in marks:
        if m[0] == "point":
            x, y = float(m[1][0]), float(m[1][1])
            arr.append((x, y, x, y))
        else:
            arr.append((float(m[1][0]), float(m[1][1]), float(m[2][0]), float(m[2][1])))
    return np.array(arr, dtype=float)


# ---------------------------------------------------------------- float margin

def seg_square_dist(cx, cy, c, s, segs, nsamp=9):
    """Float distance from closed unit squares (arrays cx, cy, cos c, sin s; shape P) to
    each mark (segments array M x 4).  Returns P x M.  For segments the distance is the
    minimum over nsamp points of the segment followed by a golden refinement; exactness
    is not needed here, it is the search objective only."""
    ax, ay, bx, by = segs[:, 0], segs[:, 1], segs[:, 2], segs[:, 3]
    cx = cx[:, None]; cy = cy[:, None]; c = c[:, None]; s = s[:, None]

    def pdist(px, py):
        dx = px - cx; dy = py - cy
        u = c * dx + s * dy
        v = -s * dx + c * dy
        du = np.maximum(np.abs(u) - 0.5, 0.0)
        dv = np.maximum(np.abs(v) - 0.5, 0.0)
        return np.sqrt(du * du + dv * dv)

    is_seg = (ax != bx) | (ay != by)
    if not is_seg.any():
        return pdist(ax[None, :], ay[None, :])
    best = None
    lam = np.linspace(0.0, 1.0, nsamp)
    for l in lam:
        d = pdist((ax + l * (bx - ax))[None, :], (ay + l * (by - ay))[None, :])
        best = d if best is None else np.minimum(best, d)
    # golden-section refinement around the best sample is skipped: the exact stage
    # decides; nsamp keeps the search objective within ~ (seglen/nsamp)^2/(8 d) of exact.
    return best


def float_margin(poses, segs, q, delta):
    """poses: array P x 3 of (cx, cy, theta).  Returns margin g = min_m dist - delta,
    and the containment slack (>= 0 iff contained)."""
    cx, cy, th = poses[:, 0], poses[:, 1], poses[:, 2]
    c, s = np.cos(th), np.sin(th)
    w = (np.abs(c) + np.abs(s)) / 2
    slack = np.minimum(np.minimum(cx - w, q - w - cx), np.minimum(cy - w, q - w - cy))
    d = seg_square_dist(cx, cy, c, s, segs)
    return d.min(axis=1) - delta, slack


# ---------------------------------------------------------------- search

def grid_search(segs, q, delta, step, angle_step_deg, topk):
    """Dense grid over contained poses; returns the topk poses by margin."""
    angles = np.deg2rad(np.arange(0.0, 90.0, angle_step_deg))
    best = []
    for th in angles:
        c, s = math.cos(th), math.sin(th)
        w = (abs(c) + abs(s)) / 2
        lo, hi = w, q - w
        xs = np.arange(lo, hi + 1e-12, step)
        if xs[-1] < hi - 1e-9:
            xs = np.append(xs, hi)
        X, Y = np.meshgrid(xs, xs, indexing="ij")
        P = np.stack([X.ravel(), Y.ravel(), np.full(X.size, th)], axis=1)
        g, _ = float_margin(P, segs, q, delta)
        idx = np.argpartition(-g, min(topk, g.size - 1))[:topk]
        for i in idx:
            best.append((g[i], P[i]))
    best.sort(key=lambda t: -t[0])
    return best[:topk]


def refine(pose, segs, q, delta, iters=600):
    """Nelder-Mead on (cx, cy, theta) with projection onto the containment box."""
    def obj(x):
        cx, cy, th = x
        c, s = math.cos(th), math.sin(th)
        w = (abs(c) + abs(s)) / 2
        cxp = min(max(cx, w), q - w); cyp = min(max(cy, w), q - w)
        g, _ = float_margin(np.array([[cxp, cyp, th]]), segs, q, delta)
        return -g[0]
    r = minimize(obj, pose, method="Nelder-Mead",
                 options={"xatol": 1e-9, "fatol": 1e-12, "maxiter": iters, "initial_simplex": None})
    cx, cy, th = r.x
    c, s = math.cos(th), math.sin(th)
    w = (abs(c) + abs(s)) / 2
    return np.array([min(max(cx, w), q - w), min(max(cy, w), q - w), th]), -r.fun


# ---------------------------------------------------------------- exact stage

def frame(t):
    den = 1 + t * t
    return (1 - t * t) / den, 2 * t / den


def corners(cx, cy, c, s):
    return [(cx + (a * c - b * s) / 2, cy + (a * s + b * c) / 2)
            for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]


def contained(cs, q):
    return all(0 <= x <= q and 0 <= y <= q for x, y in cs)


def dist2_point_local(cx, cy, c, s, p):
    """Method (A): exact squared distance from a point to the closed unit square."""
    dx, dy = p[0] - cx, p[1] - cy
    u = c * dx + s * dy
    v = -s * dx + c * dy
    du = max(abs(u) - F(1, 2), 0)
    dv = max(abs(v) - F(1, 2), 0)
    return du * du + dv * dv


def sat_gap_exceeds(A, B, delta):
    """Method (B): does dist(conv A, conv B) > delta?  A, B lists of exact points.
    Candidate directions: edge normals of A and of B, and all vertex-pair directions.
    Returns (decision, best direction, best unnormalised gap, |d|^2)."""
    dirs = []
    for poly in (A, B):
        n = len(poly)
        if n >= 2:
            for i in range(n):
                x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
                if (x1, y1) != (x2, y2):
                    dirs.append((-(y2 - y1), x2 - x1))
                    dirs.append(((y2 - y1), -(x2 - x1)))
    for a in A:
        for b in B:
            d = (b[0] - a[0], b[1] - a[1])
            if d != (0, 0):
                dirs.append(d)
    delta2 = delta * delta
    best = None
    for d in dirs:
        maxA = max(d[0] * x + d[1] * y for x, y in A)
        minB = min(d[0] * x + d[1] * y for x, y in B)
        gap = minB - maxA
        dd = d[0] * d[0] + d[1] * d[1]
        if gap > 0 and gap * gap > delta2 * dd:
            return True, d, gap, dd
        # keep the best normalised gap for reporting
        key = (gap * abs(gap)) / dd
        if best is None or key > best[0]:
            best = (key, d, gap, dd)
    return False, best[1], best[2], best[3]


def exact_verify(cx, cy, t, marks, q, delta):
    """Exact decision: is the closed unit square at rational pose an escape?
    Returns a dict with per-mark results and the overall verdict."""
    c, s = frame(t)
    assert c * c + s * s == 1
    cs = corners(cx, cy, c, s)
    inside = contained(cs, q)
    delta2 = delta * delta
    per = []
    ok = inside
    for m in marks:
        if m[0] == "point":
            p = m[1]
            d2 = dist2_point_local(cx, cy, c, s, p)
            a_ok = d2 > delta2
            b_ok, d, gap, dd = sat_gap_exceeds(cs, [p], delta)
            if a_ok != b_ok:
                raise AssertionError(f"methods disagree on point {p}: A={a_ok} B={b_ok}")
            per.append({"mark": ["point", str(p[0]), str(p[1])], "dist2": str(d2),
                        "dist": float(d2) ** 0.5, "clears": a_ok})
            ok = ok and a_ok
        else:
            a, b = m[1], m[2]
            b_ok, d, gap, dd = sat_gap_exceeds(cs, [a, b], delta)
            # (A) cross-check: endpoint distances are upper bounds on the segment distance;
            # if (B) says > delta then both endpoints must be > delta as well.
            da, db = dist2_point_local(cx, cy, c, s, a), dist2_point_local(cx, cy, c, s, b)
            if b_ok and not (da > delta2 and db > delta2):
                raise AssertionError("SAT claims clearance but an endpoint is within delta")
            dist_lb = (float(gap) / float(dd) ** 0.5) if gap > 0 else 0.0
            per.append({"mark": ["segment", str(a[0]), str(a[1]), str(b[0]), str(b[1])],
                        "dist_lower_bound": dist_lb, "endpoint_dist": [float(da) ** 0.5, float(db) ** 0.5],
                        "clears": b_ok})
            ok = ok and b_ok
    return {"cx": str(cx), "cy": str(cy), "t": str(t), "cos": str(c), "sin": str(s),
            "theta_deg": math.degrees(2 * math.atan(float(t))),
            "corners": [[str(x), str(y)] for x, y in cs], "contained": inside,
            "marks": per, "escape": ok,
            "min_dist": min(float(pm.get("dist", pm.get("dist_lower_bound", 0.0))) for pm in per)}


def rationalise(pose, marks, q, delta, dens=(10**3, 10**4, 10**5, 10**6)):
    """Snap a float pose to rationals (t first, then the centre clipped into the exact
    containment box) and verify exactly; try increasing denominators."""
    cx, cy, th = pose
    tf = math.tan(th / 2)
    for D in dens:
        t = F(tf).limit_denominator(D)
        c, s = frame(t)
        w = (abs(c) + abs(s)) / 2
        rx = min(max(F(cx).limit_denominator(D), w), q - w)
        ry = min(max(F(cy).limit_denominator(D), w), q - w)
        res = exact_verify(rx, ry, t, marks, q, delta)
        if res["escape"]:
            return res
    return res


def find_escapes(marks, q=Q_DEFAULT, delta=DELTA_DEFAULT, step=0.02, angle_step=1.5,
                 topk=40, refine_top=12, verbose=True):
    segs = marks_float(marks)
    qf, df = float(q), float(delta)
    t0 = time.time()
    cands = grid_search(segs, qf, df, step, angle_step, topk)
    t1 = time.time()
    refined = []
    seen = []
    for g0, pose in cands[:refine_top]:
        p, g = refine(pose, segs, qf, df)
        # dedupe by pose distance
        if any(abs(p[0] - r[1][0]) < 0.02 and abs(p[1] - r[1][1]) < 0.02 and abs(p[2] - r[1][2]) < 0.02 for r in refined):
            continue
        refined.append((g, p, g0))
    refined.sort(key=lambda t: -t[0])
    t2 = time.time()
    results = []
    for g, p, g0 in refined:
        res = rationalise(p, marks, q, delta)
        res["float_margin"] = float(g)
        res["grid_margin"] = float(g0)
        results.append(res)
    if verbose:
        print(f"grid {t1 - t0:.1f}s ({len(cands)} cands), refine {t2 - t1:.1f}s, "
              f"best float margin {refined[0][0] if refined else float('nan'):.5f}, "
              f"escapes verified: {sum(r['escape'] for r in results)}", file=sys.stderr)
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--marks", required=True, help="JSON file with a list of marks")
    ap.add_argument("--q", default="96/25")
    ap.add_argument("--delta", default="3/500")
    ap.add_argument("--step", type=float, default=0.02)
    ap.add_argument("--angle-step", type=float, default=1.5)
    ap.add_argument("--topk", type=int, default=40)
    ap.add_argument("--refine-top", type=int, default=12)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    marks = parse_marks(json.load(open(a.marks)))
    q, delta = F(a.q), F(a.delta)
    res = find_escapes(marks, q, delta, a.step, a.angle_step, a.topk, a.refine_top)
    packet = {"q": str(q), "delta": str(delta), "step": a.step, "angle_step_deg": a.angle_step,
              "topk": a.topk, "refine_top": a.refine_top, "marks": marks_to_spec(marks),
              "results": res}
    text = json.dumps(packet, indent=1)
    if a.out:
        open(a.out, "w").write(text)
    best = res[0] if res else None
    if best and best["escape"]:
        print(f"ESCAPE centre=({best['cx']},{best['cy']}) t={best['t']} theta={best['theta_deg']:.3f} deg "
              f"min dist {best['min_dist']:.5f} > delta {float(delta)}")
        return 0
    print(f"NO ESCAPE FOUND at step {a.step}, angle step {a.angle_step}; best float margin "
          f"{best['float_margin'] if best else float('nan'):.5f}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

### `selftest.py`

```text
"""Self-tests of escape_engine: known exact escapes are reproduced, controls find none."""
import sys, json, time
from fractions import Fraction as F
sys.path.insert(0, sys.argv[1])
import escape_engine as E

q = F(96, 25); delta = F(3, 500)

def p10(L):
    C = L/2; U = F(3,2) - L/4; V = F(1,2) + L/4
    pts = [(F(1),F(1)),(C,F(1)),(L-1,F(1)),(U,C),(V,C),(L-V,C),(L-U,C),(F(1),L-1),(C,L-1),(L-1,L-1)]
    return [("point", p) for p in pts]

# (1) lane C's exact escape at q: centre (73/50, 67/50), t = 49/200, least margin 14979/1060025
r = E.exact_verify(F(73,50), F(67,50), F(49,200), p10(q), q, delta)
print("(1) lane C escape at q:", r["escape"], "min dist", r["min_dist"], "contained", r["contained"])
assert r["escape"] and abs(r["min_dist"] - 14979/1060025) < 1e-12

# (2) exp-121: q' = 1939/500, t = 1/1000, strip-midpoint centre, 12 points, delta = 0 (strict avoidance)
qq = F(1939, 500); t = F(1, 1000)
c, s = E.frame(t)
h = (c + s)/2; v_a = -s + c*(qq-3); v_g = -F(4,5)*s + c*(qq-2); mid = (v_a+v_g)/2
centre = (h, (mid + s*h)/c)
pts = [(F(1), qq-3), (qq/2, qq-3), (F(3,2), F(13,10)), (qq-1, F(1)), (qq-F(4,5), qq/2), (qq-1, qq-1),
       (qq/2, qq-F(4,5)), (F(1), qq-1), (F(4,5), qq-2), (F(17,10), F(11,5)), (F(11,5), F(11,5)), (F(11,5), F(17,10))]
r2 = E.exact_verify(centre[0], centre[1], t, [("point", p) for p in pts], qq, F(0))
print("(2) exp-121 frozen square strict escape:", r2["escape"], "min dist", r2["min_dist"], "contained", r2["contained"])
assert r2["escape"]
r2b = E.exact_verify(centre[0], centre[1], t, [("point", p) for p in pts], qq, delta)
print("    same square against delta=3/500:", r2b["escape"], "(min dist %.5f)" % r2b["min_dist"])

# (3) search rediscovers an escape for P10 at q
t0 = time.time()
res = E.find_escapes(p10(q), q, delta, step=0.02, angle_step=1.5, topk=40, refine_top=12)
b = res[0]
print("(3) P10 at q search: escape", b["escape"], "centre", b["cx"], b["cy"], "t", b["t"], "theta %.3f" % b["theta_deg"],
      "min dist %.5f" % b["min_dist"], "float margin %.5f" % b["float_margin"], "%.1fs" % (time.time()-t0))
assert b["escape"]

# (4a) control: dense grid spacing 0.3 -> no escape
grid = [("point", (F(k,10), F(j,10))) for k in range(3, 36, 3) for j in range(3, 36, 3)]
res = E.find_escapes(grid, q, delta, step=0.04, angle_step=3, topk=20, refine_top=6)
print("(4a) dense grid control: best float margin %.5f, escapes %d" % (res[0]["float_margin"], sum(r["escape"] for r in res)))
assert not any(r["escape"] for r in res) and res[0]["float_margin"] < 0

# (4b) control: three full-width segments at y = 1, q/2, q-1 -> no escape (every unit square meets one)
segs = [("segment", (F(0), y), (q, y)) for y in (F(1), q/2, q-1)]
res = E.find_escapes(segs, q, delta, step=0.04, angle_step=3, topk=20, refine_top=6)
print("(4b) three-line control: best float margin %.5f, escapes %d" % (res[0]["float_margin"], sum(r["escape"] for r in res)))
assert not any(r["escape"] for r in res)

# (4c) segment sanity: a short segment mark and a square placed just beside it, both methods
segm = [("segment", (F(1), F(1)), (F(3,2), F(1)))]
r4 = E.exact_verify(F(5,4), F(3,2)+F(1,100), F(0), segm, q, delta)   # square [0.75,1.75]x[1.01,2.01], dist to y=1 is 0.01
print("(4c) axis square 0.01 above a segment:", r4["escape"], r4["marks"][0])
assert r4["escape"]
r5 = E.exact_verify(F(5,4), F(3,2)+F(1,200), F(0), segm, q, delta)   # dist 0.005 < delta
print("     axis square 0.005 above:", r5["escape"])
assert not r5["escape"]
print("ALL SELF-TESTS PASSED")
```

### `reader.py`

```text
"""Independent reader for the escape catalogue: standard library only, no import of the
engine.  For each verified escape it rebuilds the frame from t, the corners from the
centre, checks the closed containment of all four corners, and decides dist(Q, m) > delta
for every point mark by a third method: the squared distance from the mark to the closed
square is zero if the mark is inside (all four edge determinants nonnegative for the
counterclockwise corners, exp-121's test) and otherwise the minimum over the four edges of
the point-to-closed-segment squared distance.  Segment marks are decided as the minimum
over the segment's endpoints and over the square's corners projected onto the segment of
the same quantity, with the four corner-to-segment distances and a convexity remark: the
distance between two convex polygons is attained at a vertex of one of them."""
import sys, json
from fractions import Fraction as F
delta = F(3, 500); q = F(96, 25); delta2 = delta * delta
def seg_dist2(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx - ax, by - ay
    L2 = dx*dx + dy*dy
    if L2 == 0:
        return (px-ax)**2 + (py-ay)**2
    lam = ((px-ax)*dx + (py-ay)*dy) / L2
    lam = min(max(lam, F(0)), F(1))
    cx, cy = ax + lam*dx, ay + lam*dy
    return (px-cx)**2 + (py-cy)**2
def inside(corners, p):
    for i in range(4):
        (x1, y1), (x2, y2) = corners[i], corners[(i+1) % 4]
        if (x2-x1)*(p[1]-y1) - (y2-y1)*(p[0]-x1) < 0:
            return False
    return True
def point_to_square2(corners, p):
    if inside(corners, p):
        return F(0)
    return min(seg_dist2(p, corners[i], corners[(i+1) % 4]) for i in range(4))
def segment_to_square2(corners, a, b):
    # distance between convex sets is attained at a vertex of one of them
    cands = [point_to_square2(corners, a), point_to_square2(corners, b)]
    cands += [seg_dist2(c, a, b) for c in corners]
    return min(cands)
total = 0; bad = 0
for name in sys.argv[1:]:
    esc = json.load(open(name))
    for r in esc:
        t = F(r["t"]); c = (1 - t*t)/(1 + t*t); s = 2*t/(1 + t*t)
        assert c*c + s*s == 1 and F(r["cos"]) == c and F(r["sin"]) == s
        cx, cy = F(r["cx"]), F(r["cy"])
        corners = [(cx + (a*c - b*s)/2, cy + (a*s + b*c)/2) for a, b in ((-1,-1), (1,-1), (1,1), (-1,1))]
        assert [[str(x), str(y)] for x, y in corners] == r["corners"]
        ok = all(0 <= x <= q and 0 <= y <= q for x, y in corners)
        for m in r["marks"]:
            if m["mark"][0] == "point":
                d2 = point_to_square2(corners, (F(m["mark"][1]), F(m["mark"][2])))
                if "dist2" in m: assert d2 == F(m["dist2"]), (name, m)
            else:
                d2 = segment_to_square2(corners, (F(m["mark"][1]), F(m["mark"][2])), (F(m["mark"][3]), F(m["mark"][4])))
            ok = ok and d2 > delta2
        total += 1; bad += (not ok) or (not r["escape"])
        print(f"{name.split('/')[-1]}: centre ({cx}, {cy}) t={t}: independent verdict {'ESCAPE' if ok else 'NOT'} (file says {r['escape']})")
print(f"{total} escapes re-read, {bad} disagreements")
```

### `candidates.py`

```text
"""Candidate mark sets for BC-302 and the escape catalogue.

Sets:
  W11  weight-ranked: the 4 corner atoms, the centre atom and 6 of the 8 atoms of the next
       orbit (61/100, 199/200) of T-018, scaled to q by 384/381 (ties broken by x then y).
  G11  greedy set cover: from the 93 heaviest atoms scaled to q, pick 11 marks greedily
       covering the most poses of a fixed sample (grid step 0.04, angle step 3 deg).
  P10C Stromquist's Figure-13 ten points at q plus the centre (q/2, q/2).
  P10S P10 plus one point chosen by the adversarial loop (11 points, 10 fixed).
Every set is written to JSON and run through escape_engine.find_escapes.
"""
import sys, json, time, math
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, sys.argv[1])
import escape_engine as E

OUT = sys.argv[1]
q = F(96, 25); delta = F(3, 500); scale = F(384, 381)
cert = json.load(open("cases/n11_fractional_certificate/certificate.json"))
atoms = sorted(((F(x) * scale, F(y) * scale, F(w)) for x, y, w in cert["atoms"]), key=lambda t: (-t[2], t[0], t[1]))
heavy = [a for a in atoms if a[2] > F(1, 50)]
assert len(heavy) == 93

def run(name, marks, step=0.02, angle=1.5):
    json.dump(E.marks_to_spec(marks), open(f"{OUT}/set-{name}.json", "w"), indent=1)
    t0 = time.time()
    res = E.find_escapes(marks, q, delta, step=step, angle_step=angle, topk=60, refine_top=16, verbose=False)
    dt = time.time() - t0
    esc = [r for r in res if r["escape"]]
    b = res[0]
    line = (f"{name}: {len(marks)} marks; escapes verified {len(esc)}/{len(res)}; best exact min dist "
            f"{b['min_dist']:.5f} at centre ({b['cx']},{b['cy']}) t={b['t']} theta={b['theta_deg']:.3f}; "
            f"float margin {b['float_margin']:.5f}; wall {dt:.1f}s")
    print(line)
    json.dump({"name": name, "results": res, "wall_s": dt, "step": step, "angle_step": angle},
              open(f"{OUT}/escapes-{name}.json", "w"), indent=1)
    return res

# W11
w11 = heavy[:5] + heavy[5:13][:6]
W11 = [("point", (x, y)) for x, y, w in w11]
print("W11 weights:", [str(w) for x, y, w in w11])
run("W11", W11)

# G11 greedy set cover over a pose sample
segs_all = E.marks_float([("point", (x, y)) for x, y, w in heavy])
qf, df = float(q), float(delta)
poses = []
for th in np.deg2rad(np.arange(0, 90, 3.0)):
    c, s = math.cos(th), math.sin(th); w = (abs(c) + abs(s)) / 2
    xs = np.arange(w, qf - w + 1e-9, 0.04)
    X, Y = np.meshgrid(xs, xs, indexing="ij")
    poses.append(np.stack([X.ravel(), Y.ravel(), np.full(X.size, th)], axis=1))
poses = np.concatenate(poses)
cx, cy, th = poses[:, 0], poses[:, 1], poses[:, 2]
D = E.seg_square_dist(cx, cy, np.cos(th), np.sin(th), segs_all)   # P x 93
hit = D <= df
covered = np.zeros(len(poses), bool); chosen = []
for k in range(11):
    gain = (hit & ~covered[:, None]).sum(axis=0)
    j = int(np.argmax(gain)); chosen.append(j); covered |= hit[:, j]
    print(f"  greedy pick {k}: atom {j} at ({float(heavy[j][0]):.4f},{float(heavy[j][1]):.4f}) w={float(heavy[j][2]):.4f} gain {gain[j]} covered {covered.mean():.4f}")
G11 = [("point", (heavy[j][0], heavy[j][1])) for j in chosen]
run("G11", G11)

# P10 + centre
def p10(L):
    C = L/2; U = F(3,2) - L/4; V = F(1,2) + L/4
    return [("point", p) for p in [(F(1),F(1)),(C,F(1)),(L-1,F(1)),(U,C),(V,C),(L-V,C),(L-U,C),(F(1),L-1),(C,L-1),(L-1,L-1)]]
run("P10", p10(q))
run("P10C", p10(q) + [("point", (q/2, q/2))])
```

### `minimax.py`

```text
"""Adversarial min-max over 11-point mark sets at q = 96/25, delta = 3/500.

phi(M) = max over a fixed pose grid of (min_m dist(Q_pose, m) - delta): the largest
escape margin the grid sees for the mark set M.  We minimise phi over M with Powell
from several starts, in three parametrisations:
  free  22 parameters (11 free points)
  k4    K4-symmetric: centre + a midline pair (q/2, y0), (q/2, q-y0) + two generic
        orbits {(x,y), (q-x,y), (x,q-y), (q-x,q-y)}: 5 parameters, 11 points
  p10p1 Stromquist's P10 at q plus one free point: 2 parameters
The optimised sets are then handed to escape_engine.find_escapes at full resolution
(step 0.02, angle 1.5 deg) for an exact escape.  Nothing here is a proof; it is the
search reading that says how small the best achievable escape margin appears to be.
"""
import sys, json, time, math
from fractions import Fraction as F
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, sys.argv[1])
import escape_engine as E

OUT = sys.argv[1]
mode = sys.argv[2]
nstarts = int(sys.argv[3])
seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
init = sys.argv[5] if len(sys.argv) > 5 else None   # JSON list of 11 points used as start 0 (free/c2)
q = F(96, 25); delta = F(3, 500); qf, df = float(q), float(delta)
rng = np.random.default_rng(seed)

def pose_grid(step, angle_step):
    ps = []
    for th in np.deg2rad(np.arange(0, 90, angle_step)):
        c, s = math.cos(th), math.sin(th); w = (abs(c) + abs(s)) / 2
        xs = np.arange(w, qf - w + 1e-9, step)
        if xs[-1] < qf - w - 1e-6: xs = np.append(xs, qf - w)
        X, Y = np.meshgrid(xs, xs, indexing="ij")
        ps.append(np.stack([X.ravel(), Y.ravel(), np.full(X.size, th)], axis=1))
    return np.concatenate(ps)

COARSE = pose_grid(0.06, 4.0)
CC, CS = np.cos(COARSE[:, 2]), np.sin(COARSE[:, 2])

def phi(pts):
    segs = np.concatenate([pts, pts], axis=1)
    d = E.seg_square_dist(COARSE[:, 0], COARSE[:, 1], CC, CS, segs)
    return float(d.min(axis=1).max() - df)

def unpack(x):
    if mode == "free":
        return x.reshape(11, 2)
    if mode == "k4":
        y0, x1, y1, x2, y2 = x
        pts = [(qf/2, qf/2), (qf/2, y0), (qf/2, qf - y0)]
        for (a, b) in ((x1, y1), (x2, y2)):
            pts += [(a, b), (qf - a, b), (a, qf - b), (qf - a, qf - b)]
        return np.array(pts)
    if mode == "c2":
        pts = [(qf/2, qf/2)]
        for i in range(5):
            a, b = x[2*i], x[2*i+1]
            pts += [(a, b), (qf - a, qf - b)]
        return np.array(pts)
    if mode == "p10p1":
        L = qf; C = L/2; U = 1.5 - L/4; V = 0.5 + L/4
        pts = [(1,1),(C,1),(L-1,1),(U,C),(V,C),(L-V,C),(L-U,C),(1,L-1),(C,L-1),(L-1,L-1),(x[0],x[1])]
        return np.array(pts)
    raise ValueError(mode)

def obj(x):
    pts = unpack(x)
    pen = np.sum(np.maximum(0, -pts)**2 + np.maximum(0, pts - qf)**2)   # keep inside the container
    return phi(np.clip(pts, 0, qf)) + 10 * pen

def start(k):
    if init and k == 0 and mode in ("free", "c2"):
        pts = json.load(open(init))
        if mode == "free":
            return np.array(pts).ravel()
        # c2: take the five points with x < q/2 or (x == q/2 and y < q/2), excluding the centre
        sel = [p for p in pts if not (abs(p[0]-qf/2) < 1e-9 and abs(p[1]-qf/2) < 1e-9)]
        half = [p for p in sel if p[0] < qf/2 - 1e-9 or (abs(p[0]-qf/2) < 1e-9 and p[1] < qf/2)]
        assert len(half) == 5, half
        return np.array(half).ravel()
    if mode == "c2":
        return rng.uniform(0.5, qf - 0.5, size=10)
    if mode == "free":
        if k == 0:   # P10 + centre
            return unpack(np.array([1.0, 1.0, 1.0, 1.0, 1.0])) if False else np.array(
                [(1,1),(1.92,1),(2.84,1),(0.54,1.92),(1.46,1.92),(2.38,1.92),(3.30,1.92),(1,2.84),(1.92,2.84),(2.84,2.84),(1.92,1.92)]).ravel()
        if k == 1:   # 3x3 grid + two extra
            g = [(x, y) for x in (0.95, 1.92, 2.89) for y in (0.95, 1.92, 2.89)]
            return np.array(g + [(1.42, 1.0), (2.42, 2.84)]).ravel()
        return rng.uniform(0.5, qf - 0.5, size=22)
    if mode == "k4":
        if k == 0:
            return np.array([1.0, 1.0, 1.0, 0.54, 1.92])          # P10 + centre
        return np.array([rng.uniform(0.5, 1.92), rng.uniform(0.5, 1.92), rng.uniform(0.5, 1.92),
                         rng.uniform(0.5, 1.92), rng.uniform(0.5, 1.92)])
    if mode == "p10p1":
        if k == 0: return np.array([1.92, 1.92])
        return rng.uniform(0.5, qf - 0.5, size=2)

results = []
for k in range(nstarts):
    x0 = start(k)
    t0 = time.time()
    f0 = obj(x0)
    r = minimize(obj, x0, method="Powell", options={"maxiter": 20, "xtol": 1e-4, "ftol": 1e-6})
    r2 = minimize(obj, r.x, method="Nelder-Mead", options={"maxiter": 4000, "xatol": 1e-5, "fatol": 1e-7})
    x = r2.x if r2.fun < r.fun else r.x
    f = obj(x)
    pts = np.clip(unpack(x), 0, qf)
    print(f"{mode} start {k}: coarse phi {f0:.4f} -> {f:.4f} ({time.time()-t0:.0f}s, {r.nfev + r2.nfev} evals)", flush=True)
    results.append((f, pts.tolist(), k))
results.sort(key=lambda t: t[0])
best = results[0]
json.dump({"mode": mode, "seed": seed, "coarse_grid": {"step": 0.06, "angle_step": 4.0, "poses": int(len(COARSE))},
           "results": [{"coarse_phi": f, "points": p, "start": k} for f, p, k in results]},
          open(f"{OUT}/minimax-{mode}-{seed}.json", "w"), indent=1)
# full-resolution falsifier on the best set, rationalised to 1/10000
marks = [("point", (F(x).limit_denominator(10000), F(y).limit_denominator(10000))) for x, y in best[1]]
json.dump(E.marks_to_spec(marks), open(f"{OUT}/set-OPT-{mode}-{seed}.json", "w"), indent=1)
res = E.find_escapes(marks, q, delta, step=0.02, angle_step=1.5, topk=60, refine_top=16, verbose=False)
json.dump({"name": f"OPT-{mode}-{seed}", "results": res, "step": 0.02, "angle_step": 1.5},
          open(f"{OUT}/escapes-OPT-{mode}-{seed}.json", "w"), indent=1)
b = res[0]
print(f"OPT-{mode}-{seed}: coarse phi {best[0]:.4f}; full-resolution escapes verified {sum(r['escape'] for r in res)}/{len(res)}; "
      f"best exact min dist {b['min_dist']:.5f} at ({b['cx']},{b['cy']}) t={b['t']} theta={b['theta_deg']:.3f}; float margin {b['float_margin']:.5f}")
print("points:", [(round(x,4), round(y,4)) for x, y in best[1]])
```

### `polish.py`

```text
"""Pool cutting-plane min-max at full resolution: minimise the largest escape margin.

Start from a mark set; repeat: run the falsifier (grid 0.02 / 1.5 deg + Nelder-Mead) and
add its best distinct refined poses to a pool; then move the marks (Nelder-Mead over the
parametrisation) to minimise max over the pool of (min_m dist(Q, m) - delta).  The pool
only grows, so the reported margin is the true full-resolution search reading of the
final set, re-verified exactly at the end.  Modes: free (22 params), k4 (5 params:
centre + vertical midline pair + two generic orbits), k4b (centre + two vertical pairs +
one horizontal pair + one orbit), k4c (centre + three vertical pairs + one orbit).
"""
import sys, json, time, math
from fractions import Fraction as F
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, sys.argv[1]); import escape_engine as E
S = sys.argv[1]; mode = sys.argv[2]; rounds = int(sys.argv[3]); init = sys.argv[4] if len(sys.argv) > 4 else None
q = F(96, 25); delta = F(3, 500); qf, df = float(q), float(delta)

def unpack(x):
    if mode == "free":
        return np.array(x).reshape(11, 2)
    pts = [(qf/2, qf/2)]
    if mode == "k4":
        y0, x1, y1, x2, y2 = x
        pts += [(qf/2, y0), (qf/2, qf - y0)]
        orbs = [(x1, y1), (x2, y2)]
    elif mode == "k4b":
        y0, y1, x0, x1, y2 = x
        pts += [(qf/2, y0), (qf/2, qf - y0), (qf/2, y1), (qf/2, qf - y1), (x0, qf/2), (qf - x0, qf/2)]
        orbs = [(x1, y2)]
    elif mode == "k4c":
        y0, y1, y2, x1, y3 = x
        pts += [(qf/2, y0), (qf/2, qf - y0), (qf/2, y1), (qf/2, qf - y1), (qf/2, y2), (qf/2, qf - y2)]
        orbs = [(x1, y3)]
    for a, b in orbs:
        pts += [(a, b), (qf - a, b), (a, qf - b), (qf - a, qf - b)]
    return np.array(pts)

def pool_margin(x, pool):
    pts = np.clip(unpack(x), 0, qf)
    segs = np.concatenate([pts, pts], axis=1)
    d = E.seg_square_dist(pool[:, 0], pool[:, 1], np.cos(pool[:, 2]), np.sin(pool[:, 2]), segs)
    return float(d.min(axis=1).max() - df)

if init:
    x = np.array(json.load(open(init)))
else:
    x = {"k4": np.array([1.0124, 1.0122, 1.4943, 1.0094, 0.9027]),
         "k4b": np.array([1.0, 1.9, 1.0, 1.0, 1.0]),
         "k4c": np.array([0.9, 1.5, 1.9, 1.0, 1.0]),
         "free": np.array([(1.92,1.92),(1.92,2.8276),(1.92,1.0124),(1.0122,2.3457),(2.8278,2.3457),(1.0122,1.4943),(2.8278,1.4943),(2.8306,2.9373),(1.0094,2.9373),(2.8306,0.9027),(1.0094,0.9027)]).ravel()}[mode]
pool = np.zeros((0, 3)); hist = []
for r in range(rounds):
    pts = np.clip(unpack(x), 0, qf)
    marks = [("point", (F(a).limit_denominator(10**6), F(b).limit_denominator(10**6))) for a, b in pts]
    res = E.find_escapes(marks, q, delta, step=0.02, angle_step=1.5, topk=60, refine_top=20, verbose=False)
    new = np.array([[float(F(t["cx"])), float(F(t["cy"])), math.radians(t["theta_deg"])] for t in res])
    pool = np.concatenate([pool, new]) if len(pool) else new
    best = res[0]
    hist.append({"round": r, "exact_min_dist": best["min_dist"], "escape": best["escape"], "float_margin": best["float_margin"],
                 "pool": int(len(pool)), "pose": [best["cx"], best["cy"], best["t"]]})
    print(f"{mode} round {r}: pool {len(pool)}, best exact min dist {best['min_dist']:.5f} (delta {df}), escape {best['escape']}, "
          f"float margin {best['float_margin']:.5f}", flush=True)
    if not best["escape"]:
        print("NO ESCAPE at full resolution -> candidate survivor", flush=True)
        break
    f0 = pool_margin(x, pool)
    rr = minimize(lambda z: pool_margin(z, pool), x, method="Nelder-Mead", options={"maxiter": 3000, "xatol": 1e-6, "fatol": 1e-8})
    if rr.fun < f0:
        x = rr.x
json.dump({"mode": mode, "x": list(map(float, x)), "points": [[float(a), float(b)] for a, b in np.clip(unpack(x), 0, qf)], "history": hist},
          open(f"{S}/polish-{mode}.json", "w"), indent=1)
pts = np.clip(unpack(x), 0, qf)
json.dump(E.marks_to_spec([("point", (F(a).limit_denominator(10**6), F(b).limit_denominator(10**6))) for a, b in pts]),
          open(f"{S}/set-POLISH-{mode}.json", "w"), indent=1)
```

### `branch.py`

```text
"""Exact branch-and-bound for point-mark sets at q = 96/25 (BC-302).

Claim tested: there are 11 points m_1..m_11 in [0, q]^2 such that every test square T_j
(a closed unit square contained in the container, rational pose) is within delta of
some m_i.  Sound relaxation: "within delta of T" is replaced by the SUPERSET octagon
O(T) = {|u| <= 1/2 + delta, |v| <= 1/2 + delta, |u| + |v| <= 1 + 17/2000} in T's frame
(1 + 17/2000 >= 1 + delta*sqrt(2) for delta = 3/500).  A branch keeps, for each mark,
its feasible region (a convex polygon, exact rationals); serving a test square clips the
region by the octagon.  A test square with no mark whose region meets its octagon kills
the branch.  Marks are interchangeable, so a test square is assigned to at most one
still-untouched mark.  If every branch dies, no 11-point set is within delta of all the
test squares -- and since every T_j is a contained unit square, no 11-point robust
unavoidable set exists.  A surviving branch yields regions from which a candidate set is
built and handed to the falsifier; its escape becomes a new test square (cutting plane).

Padding: a set of fewer than 11 marks is a set of 11 with repeats, so 11 is WLOG.
Segments: a segment of length <= l thickened by delta lies in the disc of radius
delta + l/2 about its midpoint; rerunning with delta' = delta + l/2 covers them.
"""
from __future__ import annotations
import json, sys, time, math
from fractions import Fraction as F

Q = F(96, 25)

def frame(t):
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d

def octagon_halfplanes(cx, cy, t, delta, k):
    """Half-planes a x + b y <= c describing O(T)."""
    c, s = frame(t)
    h = F(1, 2) + delta
    hp = []
    # u = c (x - cx) + s (y - cy) ; v = -s (x - cx) + c (y - cy)
    # |u| <= h : +-(c x + s y) <= h +- (c cx + s cy)
    u0 = c * cx + s * cy; v0 = -s * cx + c * cy
    hp.append((c, s, h + u0)); hp.append((-c, -s, h - u0))
    hp.append((-s, c, h + v0)); hp.append((s, -c, h - v0))
    # |u| + |v| <= k : (+-u) + (+-v) <= k
    for su in (1, -1):
        for sv in (1, -1):
            a = su * c + sv * (-s); b = su * s + sv * c; cc = k + su * u0 + sv * v0
            hp.append((a, b, cc))
    return hp

def clip(poly, a, b, c):
    n = len(poly)
    if n == 0:
        return []
    out = []
    for i in range(n):
        P = poly[i]; R = poly[(i + 1) % n]
        fp = a * P[0] + b * P[1] - c; fr = a * R[0] + b * R[1] - c
        if fp <= 0:
            out.append(P)
        if (fp < 0 < fr) or (fr < 0 < fp):
            lam = fp / (fp - fr)
            out.append((P[0] + lam * (R[0] - P[0]), P[1] + lam * (R[1] - P[1])))
    # remove consecutive duplicates
    ded = []
    for p in out:
        if not ded or ded[-1] != p:
            ded.append(p)
    if len(ded) > 1 and ded[0] == ded[-1]:
        ded.pop()
    return ded

def clip_all(poly, hps):
    for a, b, c in hps:
        poly = clip(poly, a, b, c)
        if not poly:
            return []
    return poly

def bbox(poly):
    xs = [float(p[0]) for p in poly]; ys = [float(p[1]) for p in poly]
    return min(xs) - 1e-9, max(xs) + 1e-9, min(ys) - 1e-9, max(ys) + 1e-9

class Test:
    def __init__(self, name, cx, cy, t, delta, k):
        self.name = name; self.cx, self.cy, self.t = cx, cy, t
        self.hps = octagon_halfplanes(cx, cy, t, delta, k)
        box = [(F(0), F(0)), (Q, F(0)), (Q, Q), (F(0), Q)]
        self.poly = clip_all(box, self.hps)            # octagon within the container
        self.bb = bbox(self.poly) if self.poly else None

def meets(region, test, rbb):
    if test.bb is None:
        return None
    a, b, c, d = rbb; e, f, g, h = test.bb
    if b < e or f < a or d < g or h < c:
        return None
    r = clip_all(region, test.hps)
    return r if r else None

class Solver:
    def __init__(self, tests, nmarks=11, node_budget=200000, time_budget=600):
        self.tests = tests; self.n = nmarks
        self.nodes = 0; self.budget = node_budget; self.t0 = time.time(); self.tb = time_budget
        self.deepest = 0; self.timed_out = False

    def solve(self, regions, touched, remaining):
        self.nodes += 1
        if self.nodes > self.budget or time.time() - self.t0 > self.tb:
            self.timed_out = True
            return ("timeout", regions)
        depth = self.n - sum(1 for t in touched if not t) 
        best = None
        bbs = [bbox(r) for r in regions]
        first_untouched = next((i for i in range(self.n) if not touched[i]), None)
        for T in remaining:
            servers = []
            for i in range(self.n):
                if not touched[i]:
                    continue
                r = meets(regions[i], T, bbs[i])
                if r is not None:
                    servers.append((i, r))
            if first_untouched is not None:
                r = meets(regions[first_untouched], T, bbs[first_untouched])
                if r is not None:
                    servers.append((first_untouched, r))
            if not servers:
                return ("dead", None)
            if best is None or len(servers) < len(best[1]):
                best = (T, servers)
                if len(servers) == 1:
                    break
        if best is None:
            return ("alive", regions)
        T, servers = best
        rem = [U for U in remaining if U is not T]
        for i, r in servers:
            regs = list(regions); regs[i] = r
            tch = list(touched); tch[i] = True
            status, out = self.solve(regs, tch, rem)
            if status != "dead":
                return (status, out)
        return ("dead", None)

    def run(self):
        box = [(F(0), F(0)), (Q, F(0)), (Q, Q), (F(0), Q)]
        regions = [box] * self.n
        touched = [False] * self.n
        return self.solve(regions, touched, list(self.tests))

def load_tests(path, delta, k):
    spec = json.load(open(path))
    return [Test(s["name"], F(s["cx"]), F(s["cy"]), F(s["t"]), delta, k) for s in spec]

def region_point(poly):
    """A representative point of a nonempty convex polygon: the vertex average."""
    n = len(poly)
    return sum(p[0] for p in poly) / n, sum(p[1] for p in poly) / n

if __name__ == "__main__":
    tests_path = sys.argv[1]; delta = F(sys.argv[2]); k = F(sys.argv[3])
    nb = int(sys.argv[4]) if len(sys.argv) > 4 else 200000
    tb = float(sys.argv[5]) if len(sys.argv) > 5 else 600
    tests = load_tests(tests_path, delta, k)
    S = Solver(tests, node_budget=nb, time_budget=tb)
    status, regions = S.run()
    print(json.dumps({"status": status, "nodes": S.nodes, "seconds": round(time.time() - S.t0, 1),
                      "tests": len(tests), "delta": str(delta), "k": str(k)}))
    if status == "alive":
        pts = [region_point(r) for r in regions]
        print(json.dumps({"regions": [[[str(x), str(y)] for x, y in r] for r in regions],
                          "points": [[str(x), str(y)] for x, y in pts]}))
```

### `tests_gobel.py`

```text
"""Ten pairwise-far test squares from the n = 10 optimal packing scaled to q, rational poses,
pairwise distance > 2 delta verified exactly with escape_engine's separating-axis test."""
import sys, json
from fractions import Fraction as F
sys.path.insert(0, sys.argv[1]); import escape_engine as E
q = F(96, 25); delta = F(3, 500)
lam = float(q) / (3 + 2 ** 0.5 / 2)
raw = [(0.5, 3.2071067811865475, 0), (1.5, 3.2071067811865475, 0), (0.5, 2.2071067811865475, 0),
       (3.2071067811865475, 3.2071067811865475, 0), (3.2071067811865475, 0.5, 0), (2.2071067811865475, 0.5, 0),
       (3.2071067811865475, 1.5, 0), (0.5, 0.5, 0), (2.2071067811865475, 2.2071067811865475, 45), (1.5, 1.5, 45)]
tests = []
for i, (x, y, a) in enumerate(raw):
    t = F(0) if a == 0 else F(41, 99)
    cx = F(x * lam).limit_denominator(1000); cy = F(y * lam).limit_denominator(1000)
    c, s = E.frame(t); w = (abs(c) + abs(s)) / 2
    cx = min(max(cx, w), q - w); cy = min(max(cy, w), q - w)
    tests.append({"name": f"G{i+1}", "cx": str(cx), "cy": str(cy), "t": str(t)})
# exact pairwise distance > 2 delta
sq = []
for T in tests:
    c, s = E.frame(F(T["t"])); sq.append(E.corners(F(T["cx"]), F(T["cy"]), c, s))
    assert E.contained(sq[-1], q)
for i in range(10):
    for j in range(i + 1, 10):
        ok, d, gap, dd = E.sat_gap_exceeds(sq[i], sq[j], 2 * delta)
        assert ok, (i, j)
print("ten Gobel squares at q: contained, pairwise distance > 2 delta = 3/250 (exact)")
json.dump(tests, open(f"{sys.argv[1]}/tests-gobel.json", "w"), indent=1)
```

### `loop.py`

```text
"""Cutting-plane loop: exact branch-and-bound over test squares <-> escape falsifier."""
import sys, json, time
from fractions import Fraction as F
sys.path.insert(0, sys.argv[1])
import escape_engine as E, branch as B

S = sys.argv[1]; tag = sys.argv[2]; delta = F(sys.argv[3]); k = F(sys.argv[4])
node_budget = int(sys.argv[5]); time_budget = float(sys.argv[6]); iters = int(sys.argv[7])
q = F(96, 25)
tests = json.load(open(f"{S}/tests-gobel.json"))
seen = {(t["cx"], t["cy"], t["t"]) for t in tests}
def add(name, cx, cy, t):
    key = (cx, cy, t)
    if key in seen: return False
    seen.add(key); tests.append({"name": name, "cx": cx, "cy": cy, "t": t}); return True
# seed with catalogued escapes
for name in ("W11", "G11", "P10", "P10C", "OPT-p10p1-1"):
    try:
        d = json.load(open(f"{S}/escapes-{name}.json"))
    except FileNotFoundError:
        continue
    for i, r in enumerate(d["results"]):
        if r["escape"]:
            add(f"{name}-{i}", r["cx"], r["cy"], r["t"])
print(f"seed tests: {len(tests)}", flush=True)
log = []
for it in range(iters):
    T = [B.Test(t["name"], F(t["cx"]), F(t["cy"]), F(t["t"]), delta, k) for t in tests]
    solver = B.Solver(T, node_budget=node_budget, time_budget=time_budget)
    status, regions = solver.run()
    entry = {"iter": it, "tests": len(tests), "status": status, "nodes": solver.nodes, "seconds": round(time.time() - solver.t0, 1)}
    if status == "dead":
        print(json.dumps(entry), flush=True); log.append(entry)
        print("REFUTED: no 11 point marks are within delta of all test squares", flush=True)
        break
    if status == "timeout":
        print(json.dumps(entry), flush=True); log.append(entry)
        print("branch-and-bound budget exhausted; last regions used for a candidate anyway", flush=True)
    pts = [B.region_point(r) for r in regions]
    marks = [("point", (F(x).limit_denominator(100000), F(y).limit_denominator(100000))) for x, y in pts]
    res = E.find_escapes(marks, q, delta, step=0.02, angle_step=1.5, topk=60, refine_top=16, verbose=False)
    esc = [r for r in res if r["escape"]]
    entry["candidate"] = [[str(x), str(y)] for x, y in pts]
    entry["escapes"] = len(esc); entry["best_min_dist"] = res[0]["min_dist"] if res else None
    entry["best_float_margin"] = res[0]["float_margin"] if res else None
    print(json.dumps({k2: v for k2, v in entry.items() if k2 != "candidate"}), flush=True)
    log.append(entry)
    if not esc:
        print("SURVIVOR: candidate with no verified escape at step 0.02 / 1.5 deg", flush=True)
        json.dump(E.marks_to_spec(marks), open(f"{S}/set-SURVIVOR-{tag}.json", "w"), indent=1)
        break
    added = 0
    for i, r in enumerate(esc[:6]):
        added += add(f"it{it}-{i}", r["cx"], r["cy"], r["t"])
    if added == 0:
        print("no new test squares; stopping", flush=True); break
    json.dump(tests, open(f"{S}/tests-{tag}.json", "w"), indent=1)
json.dump(log, open(f"{S}/loop-{tag}.json", "w"), indent=1)
json.dump(tests, open(f"{S}/tests-{tag}.json", "w"), indent=1)
```

### `clean_pose.py`

```text
"""Re-express a verified escape with small-denominator rationals: t with denominator <= 120,
centre coordinates with denominator <= 400 (snapped exactly to a wall when the float pose
touches it), keeping only poses that still verify exactly with distance > delta."""
import sys, json, math
from fractions import Fraction as F
S = sys.argv[1]; sys.path.insert(0, S); import escape_engine as E
q = F(96, 25); delta = F(3, 500)
def clean(r, marks):
    cxf, cyf = float(F(r["cx"])), float(F(r["cy"])); tf = float(F(r["t"]))
    best = None
    for D in (12, 25, 50, 99, 120):
        t = F(tf).limit_denominator(D)
        c, s = E.frame(t); w = (abs(c) + abs(s)) / 2
        for Dc in (50, 100, 200, 400):
            cands_x = [F(cxf).limit_denominator(Dc)]; cands_y = [F(cyf).limit_denominator(Dc)]
            if abs(cxf - w) < 2e-3: cands_x = [w]
            if abs(q - w - cxf) < 2e-3: cands_x = [q - w]
            if abs(cyf - w) < 2e-3: cands_y = [w]
            if abs(q - w - cyf) < 2e-3: cands_y = [q - w]
            for cx in cands_x:
                for cy in cands_y:
                    cx2 = min(max(cx, w), q - w); cy2 = min(max(cy, w), q - w)
                    v = E.exact_verify(cx2, cy2, t, marks, q, delta)
                    if v["escape"] and (best is None or v["min_dist"] > best["min_dist"] - 1e-4 and (best is None or len(str(t)) + len(str(cx2)) + len(str(cy2)) < best["_len"])):
                        v["_len"] = len(str(t)) + len(str(cx2)) + len(str(cy2)); best = v
        if best is not None:
            break
    return best
for name in sys.argv[2:]:
    d = json.load(open(f"{S}/escapes-{name}.json")); marks = E.parse_marks(json.load(open(f"{S}/set-{name}.json")))
    esc = [r for r in d["results"] if r["escape"]]
    out = []
    for r in esc[:4]:
        c = clean(r, marks)
        if c is None:
            print(f"{name}: no clean pose for {r['cx']},{r['cy']},{r['t']}"); continue
        near = sorted(c["marks"], key=lambda m: m["dist"])[:2]
        print(f"{name}: centre=({c['cx']},{c['cy']}) t={c['t']} theta={c['theta_deg']:.3f} min_dist={c['min_dist']:.5f} "
              f"nearest {[(m['mark'][1], m['mark'][2], round(m['dist'],5)) for m in near]}")
        c.pop("_len", None); out.append(c)
    json.dump(out, open(f"{S}/clean-{name}.json", "w"), indent=1)
```

### `segments.py`

```text
"""Segment-mark candidates: Stromquist's rows and the K4 optimum's columns as short segments."""
import sys, json, time
from fractions import Fraction as F
S = sys.argv[1]; sys.path.insert(0, S); import escape_engine as E
q = F(96, 25); delta = F(3, 500)
def run(name, marks):
    json.dump(E.marks_to_spec(marks), open(f"{S}/set-{name}.json", "w"), indent=1)
    t0 = time.time()
    res = E.find_escapes(marks, q, delta, step=0.02, angle_step=1.5, topk=60, refine_top=16, verbose=False)
    esc = [r for r in res if r["escape"]]; b = res[0]
    print(f"{name}: {len(marks)} marks; escapes {len(esc)}/{len(res)}; best exact min dist {b['min_dist']:.5f} at ({b['cx']},{b['cy']}) t={b['t']} "
          f"theta={b['theta_deg']:.3f}; float margin {b['float_margin']:.5f}; {time.time()-t0:.1f}s", flush=True)
    json.dump({"name": name, "results": res, "step": 0.02, "angle_step": 1.5}, open(f"{S}/escapes-{name}.json", "w"), indent=1)
def p10(L):
    C = L/2; U = F(3,2) - L/4; V = F(1,2) + L/4
    return [(F(1),F(1)),(C,F(1)),(L-1,F(1)),(U,C),(V,C),(L-V,C),(L-U,C),(F(1),L-1),(C,L-1),(L-1,L-1)]
for l in (F(1,10), F(1,5), F(3,10)):
    h = l/2
    segs = [("segment", (x-h, y), (x+h, y)) for x, y in p10(q)] + [("point", (q/2, q/2))]
    run(f"S10C-l{float(l):.1f}", segs)
k4 = json.load(open(f"{S}/set-POLISH-k4.json"))
pts = [(F(m["xy"][0]), F(m["xy"][1])) for m in k4]
for l in (F(1,10), F(1,5), F(3,10)):
    h = l/2
    marks = []
    for x, y in pts:
        if abs(x - q/2) < F(1,100):      # middle column: horizontal segments
            marks.append(("segment", (x-h, y), (x+h, y)))
        else:                              # outer columns: vertical segments along the wall
            marks.append(("segment", (x, y-h), (x, y+h)))
    run(f"K4S-l{float(l):.1f}", marks)
```

### `variants.py`

```text
"""Variants of the segment survivor: without the centre, and shorter segments; each run
through the falsifier (step 0.02 / 1.5 deg) and then the interval reader."""
import sys, json, subprocess, time
from fractions import Fraction as F
S = sys.argv[1]; sys.path.insert(0, S); import escape_engine as E, cover_reader as C
q = F(96, 25); delta = F(3, 500)
def p10(L):
    Cc = L/2; U = F(3,2) - L/4; V = F(1,2) + L/4
    return [(F(1),F(1)),(Cc,F(1)),(L-1,F(1)),(U,Cc),(V,Cc),(L-V,Cc),(L-U,Cc),(F(1),L-1),(Cc,L-1),(L-1,L-1)]
def trial(name, marks):
    json.dump(E.marks_to_spec(marks), open(f"{S}/set-{name}.json", "w"), indent=1)
    t0 = time.time(); res = E.find_escapes(marks, q, delta, step=0.02, angle_step=1.5, topk=60, refine_top=16, verbose=False)
    b = res[0]; esc = sum(r["escape"] for r in res); t1 = time.time() - t0
    json.dump({"name": name, "results": res, "step": 0.02, "angle_step": 1.5}, open(f"{S}/escapes-{name}.json", "w"), indent=1)
    line = f"{name}: {len(marks)} marks; escapes {esc}; best exact min dist {b['min_dist']:.5f} at ({b['cx']},{b['cy']}) t={b['t']} theta={b['theta_deg']:.2f}; float margin {b['float_margin']:.5f}; falsifier {t1:.1f}s"
    if esc == 0:
        t0 = time.time(); r = C.run(C.load_marks(f"{S}/set-{name}.json"), 2e-4, False, 4_000_000)
        line += f"; reader: nodes {r['nodes']} leaves {r['certified_leaves']} failed {r['failed']} {r['wall_s']}s"
        json.dump(r, open(f"{S}/cover-{name}.json", "w"), indent=1)
    print(line, flush=True)
h = F(1, 20)
trial("S10-l0.1", [("segment", (x-h, y), (x+h, y)) for x, y in p10(q)])
for l in (F(9,100), F(8,100), F(7,100), F(6,100)):
    h = l/2
    trial(f"S10C-l{float(l):.2f}", [("segment", (x-h, y), (x+h, y)) for x, y in p10(q)] + [("point", (q/2, q/2))])
```

### `spotcheck.py`

```text
import sys, json, random, math, time
from fractions import Fraction as F
S = sys.argv[1]; sys.path.insert(0, S); import escape_engine as E
q = F(96, 25); delta = F(3, 500)
marks = E.parse_marks(json.load(open(f"{S}/set-S10C-l0.1.json")))
print("marks:", [(m[0], str(m[1]), str(m[2]) if len(m) > 2 else "") for m in marks][:3], "...")
for label, cx, cy, t in [("laneC interior", F(73,50), F(67,50), F(49,200)), ("P10 wall", F(73,50), F(239,338), F(5,12)),
                         ("laneC at 3.82-type", F(291,200), F(27,20), F(11,50))]:
    r = E.exact_verify(cx, cy, t, marks, q, delta)
    near = sorted(r["marks"], key=lambda m: m.get("dist", m.get("dist_lower_bound")))[:2]
    print(f"{label}: escape={r['escape']} min={r['min_dist']:.5f} nearest={[(m['mark'][1:3], m.get('dist_lower_bound')) for m in near]}")
random.seed(3); pos = 0; mx = 0
for i in range(300):
    t = F(random.randint(0, 999), 1000); c, s = E.frame(t); w = (abs(c) + abs(s)) / 2
    cx = w + F(random.randint(0, 10000), 10000) * (q - 2*w); cy = w + F(random.randint(0, 10000), 10000) * (q - 2*w)
    r = E.exact_verify(cx, cy, t, marks, q, delta)
    md = min(m.get("dist", m.get("dist_lower_bound", 0.0)) for m in r["marks"])
    pos += md > 0; mx = max(mx, md)
print(f"300 random contained poses: {pos} with positive distance to all marks; largest min-distance {mx:.5f}")
t0 = time.time()
res = E.find_escapes(marks, q, delta, step=0.01, angle_step=0.75, topk=100, refine_top=24, verbose=False)
b = res[0]
print(f"fine search (0.01 / 0.75 deg): escapes {sum(r['escape'] for r in res)}/{len(res)}; best float margin {b['float_margin']:.5f}; "
      f"best exact min dist {b['min_dist']:.5f} at ({b['cx']},{b['cy']}) t={b['t']}; {time.time()-t0:.0f}s")
json.dump({"name": "S10C-l0.1-fine", "results": res, "step": 0.01, "angle_step": 0.75}, open(f"{S}/escapes-S10C-l0.1-fine.json", "w"), indent=1)
```

### `cover_reader.py`

```text
"""Interval reader: prove that every contained closed unit square at side q is within
delta of some mark of a given set, by an adaptive box cover of pose space.

Pose P = (t, cx, cy), t = tan(theta/2) in [0, 1] (all orientations mod 90 degrees),
centre in [1/2, q - 1/2]^2 (every contained square has its centre there).  For a mark
point p write (u, v) for p in the square's frame and f(P, p) = max(|u| - 1/2, |v| - 1/2);
then dist(Q(P), p)^2 = (|u|-1/2)_+^2 + (|v|-1/2)_+^2 <= 2 max(f, 0)^2, so f <= delta/sqrt2
implies dist <= delta.  For a segment mark f_seg(P) = min over the segment of f(P, .),
a convex piecewise-linear function of the segment parameter, whose minimum is at an
endpoint or a breakpoint (u = 0, v = 0, u = v, u = -v).

Lipschitz bound over a box with half-widths (ht, hx, hy) about P0 = (t0, x0, y0): the
centre moves by at most hx + hy (Euclidean <= L1) and the frame vectors (cos, sin),
(-sin, cos) by at most |dtheta| = 2|atan t - atan t0| <= 2 ht, so for every P in the box
   f(P, p) <= f(P0, p) + hx + hy + 2 ht (R + hx + hy),
with R >= |p - (x0, y0)|_2 taken as the L1 distance (for a segment, the larger of the
endpoints' L1 distances bounds every point of it).  A box is certified by a mark m when
this upper bound is <= tau = 2121/500000 < delta/sqrt(2) for delta = 3/500, minus a
rounding allowance EPS = 1e-9 that exceeds the accumulated IEEE double error (fewer than
two hundred operations on quantities below ten, each with relative error 2^-53) by more
than four orders of magnitude.  A box with no contained pose is discarded: it is
discarded only when x2 < wmin or x1 > q - wmin (same in y), with wmin the least
half-width (cos + sin)/2 over the box's t-range (attained at an endpoint since w is
unimodal on [0, 1]), again with the allowance on the conservative side.  Otherwise the
box is split along its widest scaled dimension.  Boxes below the floor that remain
uncertified are reported with their centre pose: they are near-escapes or a bug, and the
proof fails.

Exact mode (--exact) repeats the certification of every certified leaf with
fractions.Fraction and the rational tau, no allowance, as an independent check.
"""
import sys, json, math, time, argparse
from fractions import Fraction as F

Q = 96 / 25; DELTA = 3 / 500; TAU = 2121 / 500000; EPS = 1e-9
QF = F(96, 25); TAUF = F(2121, 500000)
T45 = math.sqrt(2) - 1

def load_marks(path):
    out = []
    for m in json.load(open(path)):
        if m["kind"] == "point":
            x, y = float(F(m["xy"][0])), float(F(m["xy"][1])); out.append(((x, y), (x, y), (F(m["xy"][0]), F(m["xy"][1])), (F(m["xy"][0]), F(m["xy"][1]))))
        else:
            a = (float(F(m["a"][0])), float(F(m["a"][1]))); b = (float(F(m["b"][0])), float(F(m["b"][1])))
            out.append((a, b, (F(m["a"][0]), F(m["a"][1])), (F(m["b"][0]), F(m["b"][1]))))
    return out

def frame(t):
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d

def f_point(c, s, cx, cy, px, py):
    dx, dy = px - cx, py - cy
    u = c * dx + s * dy; v = -s * dx + c * dy
    return max(abs(u) - 0.5, abs(v) - 0.5)

def f_segment(c, s, cx, cy, a, b):
    """min over the segment of f: endpoints and the breakpoints of the convex piecewise-linear
    function (u = 0, v = 0, u = v, u = -v), each an affine equation in the parameter."""
    ax, ay = a; bx, by = b
    if a == b:
        return f_point(c, s, cx, cy, ax, ay)
    dx0, dy0 = ax - cx, ay - cy; ex, ey = bx - ax, by - ay
    u0 = c * dx0 + s * dy0; du = c * ex + s * ey
    v0 = -s * dx0 + c * dy0; dv = -s * ex + c * ey
    lams = [0.0, 1.0]
    for num, den in ((u0, du), (v0, dv), (u0 - v0, du - dv), (u0 + v0, du + dv)):
        if den != 0:
            lam = -num / den
            if 0 < lam < 1:
                lams.append(lam)
    best = None
    for lam in lams:
        u = u0 + lam * du; v = v0 + lam * dv
        val = max(abs(u) - 0.5, abs(v) - 0.5)
        if best is None or val < best:
            best = val
    return best

def w_half(t):
    c, s = frame(t); return (c + s) / 2

def certify_box(marks, t1, t2, x1, x2, y1, y2):
    """Returns ('discard'|'ok'|'split', best slack)."""
    wmin = min(w_half(t1), w_half(t2))
    if x2 < wmin - EPS or x1 > Q - wmin + EPS or y2 < wmin - EPS or y1 > Q - wmin + EPS:
        return "discard", None
    t0, x0, y0 = (t1 + t2) / 2, (x1 + x2) / 2, (y1 + y2) / 2
    ht, hx, hy = (t2 - t1) / 2, (x2 - x1) / 2, (y2 - y1) / 2
    c, s = frame(t0)
    best = None
    for a, b, _, _ in marks:
        R = max(abs(a[0] - x0) + abs(a[1] - y0), abs(b[0] - x0) + abs(b[1] - y0))
        f0 = f_segment(c, s, x0, y0, a, b)
        ub = f0 + hx + hy + 2 * ht * (R + hx + hy)
        if best is None or ub < best:
            best = ub
        if ub <= TAU - EPS:
            return "ok", TAU - ub
    return "split", TAU - best

def exact_certify(marks, t1, t2, x1, x2, y1, y2):
    """Exact re-check of a certified box with Fractions (no allowance)."""
    t1, t2, x1, x2, y1, y2 = (F(v) for v in (t1, t2, x1, x2, y1, y2))
    t0, x0, y0 = (t1 + t2) / 2, (x1 + x2) / 2, (y1 + y2) / 2
    ht, hx, hy = (t2 - t1) / 2, (x2 - x1) / 2, (y2 - y1) / 2
    d = 1 + t0 * t0; c, s = (1 - t0 * t0) / d, 2 * t0 / d
    for _, _, a, b in marks:
        R = max(abs(a[0] - x0) + abs(a[1] - y0), abs(b[0] - x0) + abs(b[1] - y0))
        # exact f over the segment: endpoints and breakpoints
        dx0, dy0 = a[0] - x0, a[1] - y0; ex, ey = b[0] - a[0], b[1] - a[1]
        u0 = c * dx0 + s * dy0; du = c * ex + s * ey; v0 = -s * dx0 + c * dy0; dv = -s * ex + c * ey
        lams = [F(0), F(1)]
        for num, den in ((u0, du), (v0, dv), (u0 - v0, du - dv), (u0 + v0, du + dv)):
            if den != 0:
                lam = -num / den
                if 0 < lam < 1: lams.append(lam)
        f0 = min(max(abs(u0 + l * du) - F(1, 2), abs(v0 + l * dv) - F(1, 2)) for l in lams)
        if f0 + hx + hy + 2 * ht * (R + hx + hy) <= TAUF:
            return True
    return False

def run(marks, floor, exact, limit_boxes):
    stack = [(0.0, 1.0, 0.5, Q - 0.5, 0.5, Q - 0.5)]
    leaves = []; discarded = 0; discards = []; failed = []; nodes = 0; t_start = time.time()
    while stack:
        box = stack.pop(); nodes += 1
        if nodes > limit_boxes:
            failed.append(("budget", box)); break
        t1, t2, x1, x2, y1, y2 = box
        status, slack = certify_box(marks, *box)
        if status == "discard":
            discarded += 1; discards.append(box); continue
        if status == "ok":
            leaves.append(box); continue
        ht, hx, hy = (t2 - t1) / 2, (x2 - x1) / 2, (y2 - y1) / 2
        if max(3 * ht, hx, hy) < floor:
            failed.append(("floor", box, slack)); continue
        dim = max((3 * ht, "t"), (hx, "x"), (hy, "y"))[1]
        if dim == "t":
            tm = (t1 + t2) / 2; stack += [(t1, tm, x1, x2, y1, y2), (tm, t2, x1, x2, y1, y2)]
        elif dim == "x":
            xm = (x1 + x2) / 2; stack += [(t1, t2, x1, xm, y1, y2), (t1, t2, xm, x2, y1, y2)]
        else:
            ym = (y1 + y2) / 2; stack += [(t1, t2, x1, x2, y1, ym), (t1, t2, x1, x2, ym, y2)]
    wall = time.time() - t_start
    result = {"nodes": nodes, "certified_leaves": len(leaves), "discarded": discarded, "failed": len(failed),
              "wall_s": round(wall, 1), "floor": floor, "tau": TAU, "eps": EPS,
              "min_leaf_halfwidth": min((min((b[1]-b[0])/2, (b[3]-b[2])/2, (b[5]-b[4])/2) for b in leaves), default=None)}
    if failed:
        result["failures"] = [{"kind": f[0], "box": f[1], "slack": f[2] if len(f) > 2 else None} for f in failed[:20]]
    if exact and not failed:
        t0 = time.time(); bad = 0
        for b in leaves:
            if not exact_certify(marks, *b): bad += 1
        badd = 0
        for (t1, t2, x1, x2, y1, y2) in discards:
            # exact: no contained pose in the box.  w(t) = (1 + 2t - t^2) / (2 (1 + t^2)) is unimodal
            # on [0, 1], so its minimum over [t1, t2] is at an endpoint.
            ws = []
            for tt in (F(t1), F(t2)):
                ws.append((1 + 2 * tt - tt * tt) / (2 * (1 + tt * tt)))
            wmin = min(ws)
            if not (F(x2) < wmin or F(x1) > QF - wmin or F(y2) < wmin or F(y1) > QF - wmin):
                badd += 1
        result["exact_recheck"] = {"leaves": len(leaves), "failed": bad, "discards": len(discards),
                                   "discards_failed": badd, "wall_s": round(time.time() - t0, 1)}
    return result

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("marks"); ap.add_argument("--floor", type=float, default=2e-4)
    ap.add_argument("--exact", action="store_true"); ap.add_argument("--limit", type=int, default=5_000_000)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    marks = load_marks(a.marks)
    res = run(marks, a.floor, a.exact, a.limit)
    res["marks"] = a.marks
    print(json.dumps(res, indent=1))
    if a.out: json.dump(res, open(a.out, "w"), indent=1)
    sys.exit(0 if res["failed"] == 0 else 1)
```

### `reader_sanity.py`

```text
"""Sanity test of the reader's bound: random poses inside random certified leaves must be
within delta of some mark by the falsifier's exact distance."""
import sys, json, random
from fractions import Fraction as F
S = sys.argv[1]; sys.path.insert(0, S); import escape_engine as E, cover_reader as C
q = F(96, 25); delta = F(3, 500)
marks_spec = json.load(open(f"{S}/set-S10-l0.1.json")); marks = E.parse_marks(marks_spec)
cm = C.load_marks(f"{S}/set-S10-l0.1.json")
# rebuild the leaves (float run, 8 s)
stack = [(0.0, 1.0, 0.5, C.Q - 0.5, 0.5, C.Q - 0.5)]; leaves = []
while stack:
    box = stack.pop(); status, slack = C.certify_box(cm, *box)
    if status == "discard": continue
    if status == "ok": leaves.append(box); continue
    t1, t2, x1, x2, y1, y2 = box; ht, hx, hy = (t2-t1)/2, (x2-x1)/2, (y2-y1)/2
    dim = max((3*ht, "t"), (hx, "x"), (hy, "y"))[1]
    if dim == "t": tm=(t1+t2)/2; stack += [(t1,tm,x1,x2,y1,y2),(tm,t2,x1,x2,y1,y2)]
    elif dim == "x": xm=(x1+x2)/2; stack += [(t1,t2,x1,xm,y1,y2),(t1,t2,xm,x2,y1,y2)]
    else: ym=(y1+y2)/2; stack += [(t1,t2,x1,x2,y1,ym),(t1,t2,x1,x2,ym,y2)]
random.seed(7); checked = 0; bad = 0; worst = 0
sample = random.sample(leaves, 3000)
for (t1, t2, x1, x2, y1, y2) in sample:
    for _ in range(2):
        t = F(t1) + F(random.random()) * (F(t2) - F(t1)); cx = F(x1) + F(random.random()) * (F(x2) - F(x1)); cy = F(y1) + F(random.random()) * (F(y2) - F(y1))
        t = t.limit_denominator(10**6); cx = cx.limit_denominator(10**6); cy = cy.limit_denominator(10**6)
        r = E.exact_verify(cx, cy, t, marks, q, delta)
        # exact_verify reports per-mark: for segments a SAT lower bound on the distance and 'clears' (dist > delta)
        within = not all(m["clears"] for m in r["marks"])
        checked += 1; bad += (not within)
        worst = max(worst, min(m.get("dist", m.get("dist_lower_bound", 0.0)) for m in r["marks"]))
print(f"{len(leaves)} leaves rebuilt; {checked} random poses in {len(sample)} random leaves: {bad} not within delta of any mark; largest least-distance lower bound seen {worst:.6f}")
```

### `assemble_appendix.py`

```text
"""Embed the retained scripts and data of lane E into the lane document's appendix, in text fences."""
import sys, json
S = sys.argv[1]; doc = sys.argv[2]
parts = []
def fence(title, body, note=""):
    parts.append(f"### `{title}`\n\n{note}```text\n{body.rstrip()}\n```\n")
for f in ("escape_engine.py", "selftest.py", "reader.py", "candidates.py", "minimax.py", "polish.py", "branch.py", "tests_gobel.py", "loop.py", "clean_pose.py", "segments.py", "variants.py", "spotcheck.py", "cover_reader.py", "reader_sanity.py", "assemble_appendix.py"):
    fence(f, open(f"{S}/{f}").read())
for f in ("selftest.out", "candidates.log", "minimax-p10p1.log", "minimax-k4.log", "minimax-free-random.log", "minimax-free.log", "polish-k4.log", "polish-free.log", "polish-k4b.log", "polish-k4c.log", "loop-A.summary", "segments.log", "spotcheck.log", "variants.log", "cover-exact-S10-l0.1.log", "reader_sanity.log"):
    try:
        fence(f, open(f"{S}/{f}").read(), "Output as run.\n\n")
    except FileNotFoundError:
        pass
def marks_text(name):
    m = json.load(open(f"{S}/set-{name}.json"))
    return "\n".join(f"{x['kind']} {x['xy'][0]} {x['xy'][1]}" if x["kind"] == "point" else f"segment {x['a'][0]} {x['a'][1]} {x['b'][0]} {x['b'][1]}" for x in m)
for name in sys.argv[3:]:
    fence(f"set-{name}.json (marks, exact)", marks_text(name))
    try:
        c = json.load(open(f"{S}/clean-{name}.json"))
        lines = []
        for r in c:
            near = sorted(r["marks"], key=lambda m: m.get("dist", 9))[:3]
            lines.append(f"centre ({r['cx']}, {r['cy']})  t = {r['t']}  cos = {r['cos']}  sin = {r['sin']}  theta = {r['theta_deg']:.4f} deg")
            lines.append("  corners: " + "; ".join(f"({x}, {y})" for x, y in r["corners"]))
            lines.append(f"  contained: {r['contained']}  escape: {r['escape']}  least distance: {r['min_dist']:.6f}")
            for m in near:
                lines.append(f"  mark ({m['mark'][1]}, {m['mark'][2]}): dist^2 = {m['dist2']}  dist = {m['dist']:.6f}")
        fence(f"clean-{name}.json (verified escapes, exact poses)", "\n".join(lines))
    except FileNotFoundError:
        pass
fence("tests-gobel.json (the ten forced test squares)", "\n".join(f"{t['name']}: centre ({t['cx']}, {t['cy']}) t = {t['t']}" for t in json.load(open(f"{S}/tests-gobel.json"))))
text = open(doc).read()
assert "APPENDIX_PLACEHOLDER" in text
open(doc, "w").write(text.replace("APPENDIX_PLACEHOLDER", "\n".join(parts)))
print("appendix assembled:", len(parts), "parts")
```

### `selftest.out`

Output as run.

```text
(1) lane C escape at q: True min dist 0.014130798801915048 contained True
(2) exp-121 frozen square strict escape: True min dist 0.000198999801000199 contained True
    same square against delta=3/500: False (min dist 0.00020)
grid 0.6s (40 cands), refine 0.2s, best float margin 0.02638, escapes verified: 4
(3) P10 at q search: escape True centre 73/50 1607521/2273378 t 408/985 theta 45.000 min dist 0.03238 float margin 0.02638 0.8s
grid 0.8s (20 cands), refine 0.1s, best float margin -0.00600, escapes verified: 0
(4a) dense grid control: best float margin -0.00600, escapes 0
grid 0.1s (20 cands), refine 0.2s, best float margin -0.00600, escapes verified: 0
(4b) three-line control: best float margin -0.00600, escapes 0
(4c) axis square 0.01 above a segment: True {'mark': ['segment', '1', '1', '3/2', '1'], 'dist_lower_bound': 0.01, 'endpoint_dist': [0.01, 0.01], 'clears': True}
     axis square 0.005 above: False
ALL SELF-TESTS PASSED
```

### `candidates.log`

Output as run.

```text
W11 weights: ['917/6250', '917/6250', '917/6250', '917/6250', '27899/200000', '33/500', '33/500', '33/500', '33/500', '33/500', '33/500']
W11: 11 marks; escapes verified 15/15; best exact min dist 0.41449 at centre (48/25,1/2) t=0 theta=0.000; float margin 0.40849; wall 1.0s
  greedy pick 0: atom 21 at (1.4110,1.9150) w=0.0622 gain 19235 covered 0.1531
  greedy pick 1: atom 27 at (2.4290,1.9150) w=0.0622 gain 18404 covered 0.2996
  greedy pick 2: atom 37 at (2.0045,1.0031) w=0.0444 gain 15962 covered 0.4267
  greedy pick 3: atom 38 at (2.0045,2.8369) w=0.0444 gain 15739 covered 0.5519
  greedy pick 4: atom 45 at (1.0009,1.0052) w=0.0336 gain 13310 covered 0.6579
  greedy pick 5: atom 46 at (1.0009,2.8348) w=0.0336 gain 13110 covered 0.7622
  greedy pick 6: atom 59 at (2.9128,1.0028) w=0.0316 gain 10913 covered 0.8491
  greedy pick 7: atom 60 at (2.9128,2.8372) w=0.0316 gain 10683 covered 0.9341
  greedy pick 8: atom 29 at (0.6088,1.9200) w=0.0450 gain 3975 covered 0.9658
  greedy pick 9: atom 20 at (2.8372,2.0057) w=0.0641 gain 3427 covered 0.9931
  greedy pick 10: atom 4 at (1.9200,1.9200) w=0.1395 gain 421 covered 0.9964
G11: 11 marks; escapes verified 2/2; best exact min dist 0.06486 at centre (1501/999,1438/459) t=5/12 theta=45.240; float margin 0.05887; wall 0.6s
P10: 10 marks; escapes verified 4/4; best exact min dist 0.03238 at centre (73/50,1607521/2273378) t=408/985 theta=45.000; float margin 0.02638; wall 0.7s
P10C: 11 marks; escapes verified 4/4; best exact min dist 0.03238 at centre (73/50,1607521/2273378) t=408/985 theta=45.000; float margin 0.02638; wall 0.7s
```

### `minimax-p10p1.log`

Output as run.

```text
p10p1 start 0: coarse phi 0.0243 -> 0.0234 (4s, 112 evals)
p10p1 start 1: coarse phi 0.0234 -> 0.0234 (3s, 87 evals)
p10p1 start 2: coarse phi 0.0243 -> 0.0234 (5s, 112 evals)
p10p1 start 3: coarse phi 0.0243 -> 0.0243 (4s, 87 evals)
p10p1 start 4: coarse phi 0.0243 -> 0.0243 (3s, 88 evals)
p10p1 start 5: coarse phi 0.0243 -> 0.0234 (4s, 112 evals)
OPT-p10p1-1: coarse phi 0.0234; full-resolution escapes verified 4/4; best exact min dist 0.03238 at (73/50,1607521/2273378) t=408/985 theta=45.000; float margin 0.02638
points: [(1.0, 1.0), (1.92, 1.0), (2.84, 1.0), (0.54, 1.92), (1.46, 1.92), (2.38, 1.92), (3.3, 1.92), (1.0, 2.84), (1.92, 2.84), (2.84, 2.84), (2.3123, 2.7304)]
```

### `minimax-k4.log`

Output as run.

```text
k4 start 0: coarse phi 0.1831 -> 0.0103 (56s, 1818 evals)
k4 start 1: coarse phi 0.9140 -> 0.0077 (61s, 1494 evals)
k4 start 2: coarse phi 0.7409 -> 0.0104 (34s, 882 evals)
k4 start 3: coarse phi 0.5337 -> 0.2023 (41s, 1083 evals)
k4 start 4: coarse phi 0.3391 -> 0.0066 (67s, 1871 evals)
k4 start 5: coarse phi 0.5334 -> 0.0064 (33s, 1076 evals)
k4 start 6: coarse phi 0.2625 -> 0.0103 (45s, 1331 evals)
k4 start 7: coarse phi 0.3794 -> 0.0101 (109s, 3142 evals)
k4 start 8: coarse phi 0.2581 -> 0.0066 (77s, 2246 evals)
k4 start 9: coarse phi 0.6866 -> 0.0091 (52s, 1530 evals)
OPT-k4-1: coarse phi 0.0064; full-resolution escapes verified 11/11; best exact min dist 0.01669 at (1607521/2273378,48/25) t=408/985 theta=45.000; float margin 0.01069
points: [(1.92, 1.92), (1.92, 2.8276), (1.92, 1.0124), (1.0122, 2.3457), (2.8278, 2.3457), (1.0122, 1.4943), (2.8278, 1.4943), (2.8306, 2.9373), (1.0094, 2.9373), (2.8306, 0.9027), (1.0094, 0.9027)]
```

### `minimax-free-random.log`

Output as run.

```text
free start 0: coarse phi 0.0243 -> 0.0108 (261s, 6989 evals)
Tue Sep  8 05:05:26 UTC 2026
```

### `minimax-free.log`

Output as run.

```text
free start 0: coarse phi 0.0080 -> 0.0059 (62s, 1790 evals)
free start 1: coarse phi 0.1615 -> 0.0601 (298s, 7130 evals)
OPT-free-1: coarse phi 0.0059; full-resolution escapes verified 12/12; best exact min dist 0.01720 at (173435881/55359650,171/89) t=403/972 theta=45.039; float margin 0.01120
points: [(1.9234, 1.9072), (1.9208, 1.0119), (1.9206, 2.8283), (1.0115, 2.3453), (2.8281, 2.3481), (1.0114, 1.4959), (2.8283, 1.4946), (0.976, 0.6811), (2.8605, 0.6627), (0.9786, 3.041), (2.8559, 3.0363)]
```

### `polish-k4.log`

Output as run.

```text
k4 round 0: pool 16, best exact min dist 0.01675 (delta 0.006), escape True, float margin 0.01075
k4 round 1: pool 33, best exact min dist 0.04480 (delta 0.006), escape True, float margin 0.03880
k4 round 2: pool 48, best exact min dist 0.04887 (delta 0.006), escape True, float margin 0.04287
k4 round 3: pool 68, best exact min dist 0.13218 (delta 0.006), escape True, float margin 0.12618
k4 round 4: pool 88, best exact min dist 0.20827 (delta 0.006), escape True, float margin 0.20227
k4 round 5: pool 101, best exact min dist 0.12645 (delta 0.006), escape True, float margin 0.12045
k4 round 6: pool 119, best exact min dist 0.06338 (delta 0.006), escape True, float margin 0.05738
k4 round 7: pool 136, best exact min dist 0.05096 (delta 0.006), escape True, float margin 0.04496
k4 round 8: pool 153, best exact min dist 0.03030 (delta 0.006), escape True, float margin 0.02430
k4 round 9: pool 170, best exact min dist 0.02472 (delta 0.006), escape True, float margin 0.01872
k4 round 10: pool 186, best exact min dist 0.01718 (delta 0.006), escape True, float margin 0.01118
k4 round 11: pool 204, best exact min dist 0.01709 (delta 0.006), escape True, float margin 0.01109
k4 round 12: pool 220, best exact min dist 0.01476 (delta 0.006), escape True, float margin 0.00876
k4 round 13: pool 240, best exact min dist 0.01488 (delta 0.006), escape True, float margin 0.00889
k4 round 14: pool 245, best exact min dist 0.02789 (delta 0.006), escape True, float margin 0.02189
k4 round 15: pool 253, best exact min dist 0.01598 (delta 0.006), escape True, float margin 0.00998
k4 round 16: pool 270, best exact min dist 0.01412 (delta 0.006), escape True, float margin 0.00812
k4 round 17: pool 290, best exact min dist 0.01401 (delta 0.006), escape True, float margin 0.00801
k4 round 18: pool 310, best exact min dist 0.01401 (delta 0.006), escape True, float margin 0.00801
k4 round 19: pool 330, best exact min dist 0.01401 (delta 0.006), escape True, float margin 0.00801
k4 round 20: pool 350, best exact min dist 0.01401 (delta 0.006), escape True, float margin 0.00801
k4 round 21: pool 370, best exact min dist 0.01401 (delta 0.006), escape True, float margin 0.00801
k4 round 22: pool 390, best exact min dist 0.01401 (delta 0.006), escape True, float margin 0.00801
k4 round 23: pool 410, best exact min dist 0.01401 (delta 0.006), escape True, float margin 0.00801
k4 round 24: pool 430, best exact min dist 0.01401 (delta 0.006), escape True, float margin 0.00801
```

### `polish-free.log`

Output as run.

```text
free round 0: pool 16, best exact min dist 0.01675 (delta 0.006), escape True, float margin 0.01075
free round 1: pool 21, best exact min dist 0.43918 (delta 0.006), escape True, float margin 0.43318
free round 2: pool 23, best exact min dist 0.36362 (delta 0.006), escape True, float margin 0.35762
free round 3: pool 30, best exact min dist 0.27449 (delta 0.006), escape True, float margin 0.26849
free round 4: pool 41, best exact min dist 0.24330 (delta 0.006), escape True, float margin 0.23730
free round 5: pool 47, best exact min dist 0.41011 (delta 0.006), escape True, float margin 0.40411
free round 6: pool 52, best exact min dist 0.34064 (delta 0.006), escape True, float margin 0.33464
free round 7: pool 59, best exact min dist 0.26076 (delta 0.006), escape True, float margin 0.25476
free round 8: pool 61, best exact min dist 0.26669 (delta 0.006), escape True, float margin 0.26069
free round 9: pool 73, best exact min dist 0.26159 (delta 0.006), escape True, float margin 0.25559
free round 10: pool 83, best exact min dist 0.16283 (delta 0.006), escape True, float margin 0.15683
free round 11: pool 84, best exact min dist 0.27174 (delta 0.006), escape True, float margin 0.26574
free round 12: pool 93, best exact min dist 0.28427 (delta 0.006), escape True, float margin 0.27827
free round 13: pool 101, best exact min dist 0.17920 (delta 0.006), escape True, float margin 0.17320
free round 14: pool 103, best exact min dist 0.31838 (delta 0.006), escape True, float margin 0.31238
free round 15: pool 107, best exact min dist 0.21137 (delta 0.006), escape True, float margin 0.20537
free round 16: pool 111, best exact min dist 0.20563 (delta 0.006), escape True, float margin 0.19963
free round 17: pool 129, best exact min dist 0.33405 (delta 0.006), escape True, float margin 0.32805
free round 18: pool 133, best exact min dist 0.19066 (delta 0.006), escape True, float margin 0.18466
free round 19: pool 140, best exact min dist 0.16586 (delta 0.006), escape True, float margin 0.15986
free round 20: pool 144, best exact min dist 0.18150 (delta 0.006), escape True, float margin 0.17551
free round 21: pool 152, best exact min dist 0.13867 (delta 0.006), escape True, float margin 0.13267
free round 22: pool 172, best exact min dist 0.15591 (delta 0.006), escape True, float margin 0.14991
free round 23: pool 179, best exact min dist 0.15200 (delta 0.006), escape True, float margin 0.14600
free round 24: pool 190, best exact min dist 0.15479 (delta 0.006), escape True, float margin 0.14879
```

### `polish-k4b.log`

Output as run.

```text
k4b round 0: pool 4, best exact min dist 0.14351 (delta 0.006), escape True, float margin 0.13751
k4b round 1: pool 10, best exact min dist 0.10640 (delta 0.006), escape True, float margin 0.10040
k4b round 2: pool 14, best exact min dist 0.04545 (delta 0.006), escape True, float margin 0.03945
k4b round 3: pool 26, best exact min dist 0.06376 (delta 0.006), escape True, float margin 0.05776
k4b round 4: pool 40, best exact min dist 0.02343 (delta 0.006), escape True, float margin 0.01743
k4b round 5: pool 56, best exact min dist 0.04314 (delta 0.006), escape True, float margin 0.03714
k4b round 6: pool 71, best exact min dist 0.03867 (delta 0.006), escape True, float margin 0.03280
k4b round 7: pool 82, best exact min dist 0.04486 (delta 0.006), escape True, float margin 0.03886
k4b round 8: pool 91, best exact min dist 0.02641 (delta 0.006), escape True, float margin 0.02042
k4b round 9: pool 96, best exact min dist 0.03296 (delta 0.006), escape True, float margin 0.02696
k4b round 10: pool 100, best exact min dist 0.02916 (delta 0.006), escape True, float margin 0.02316
k4b round 11: pool 105, best exact min dist 0.03004 (delta 0.006), escape True, float margin 0.02404
k4b round 12: pool 117, best exact min dist 0.02740 (delta 0.006), escape True, float margin 0.02141
k4b round 13: pool 127, best exact min dist 0.02196 (delta 0.006), escape True, float margin 0.01596
k4b round 14: pool 144, best exact min dist 0.03043 (delta 0.006), escape True, float margin 0.02443
k4b round 15: pool 161, best exact min dist 0.02163 (delta 0.006), escape True, float margin 0.01563
k4b round 16: pool 168, best exact min dist 0.02380 (delta 0.006), escape True, float margin 0.01780
k4b round 17: pool 178, best exact min dist 0.02155 (delta 0.006), escape True, float margin 0.01555
k4b round 18: pool 195, best exact min dist 0.01940 (delta 0.006), escape True, float margin 0.01341
k4b round 19: pool 207, best exact min dist 0.02376 (delta 0.006), escape True, float margin 0.01776
```

### `polish-k4c.log`

Output as run.

```text
k4c round 0: pool 19, best exact min dist 0.42000 (delta 0.006), escape True, float margin 0.41400
k4c round 1: pool 39, best exact min dist 0.45753 (delta 0.006), escape True, float margin 0.45153
k4c round 2: pool 43, best exact min dist 0.22402 (delta 0.006), escape True, float margin 0.21802
k4c round 3: pool 63, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 4: pool 79, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 5: pool 98, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 6: pool 117, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 7: pool 136, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 8: pool 155, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 9: pool 174, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 10: pool 193, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 11: pool 212, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 12: pool 231, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 13: pool 250, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 14: pool 269, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 15: pool 288, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 16: pool 307, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 17: pool 326, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 18: pool 345, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
k4c round 19: pool 364, best exact min dist 0.21000 (delta 0.006), escape True, float margin 0.20400
Tue Sep  8 05:05:39 UTC 2026
```

### `loop-A.summary`

Output as run.

```text
"iter": 0, "tests": 32, "status": "alive", "nodes": 33, "seconds": 0.6, "escapes": 8, "best_min_dist": 0.3489399881453111
"iter": 1, "tests": 38, "status": "alive", "nodes": 39, "seconds": 1.1, "escapes": 3, "best_min_dist": 0.28946841994478006
"iter": 2, "tests": 41, "status": "alive", "nodes": 42, "seconds": 1.4, "escapes": 8, "best_min_dist": 0.3285683145009385
"iter": 3, "tests": 47, "status": "alive", "nodes": 48, "seconds": 2.3, "escapes": 2, "best_min_dist": 0.2604806874829838
"iter": 4, "tests": 49, "status": "alive", "nodes": 50, "seconds": 2.7, "escapes": 4, "best_min_dist": 0.2324546760064093
"iter": 5, "tests": 53, "status": "alive", "nodes": 54, "seconds": 2.9, "escapes": 3, "best_min_dist": 0.19964978016368035
"iter": 6, "tests": 56, "status": "alive", "nodes": 57, "seconds": 3.5, "escapes": 13, "best_min_dist": 0.17399117260725308
"iter": 7, "tests": 62, "status": "alive", "nodes": 63, "seconds": 4.1, "escapes": 4, "best_min_dist": 0.16415873235167167
"iter": 8, "tests": 66, "status": "alive", "nodes": 67, "seconds": 4.6, "escapes": 8, "best_min_dist": 0.18257776594234382
"iter": 9, "tests": 72, "status": "alive", "nodes": 73, "seconds": 5.3, "escapes": 1, "best_min_dist": 0.16840930883154487
"iter": 10, "tests": 73, "status": "alive", "nodes": 74, "seconds": 6.1, "escapes": 4, "best_min_dist": 0.16320512219943087
"iter": 11, "tests": 77, "status": "alive", "nodes": 78, "seconds": 6.8, "escapes": 2, "best_min_dist": 0.12394731599914567
"iter": 12, "tests": 79, "status": "alive", "nodes": 80, "seconds": 6.9, "escapes": 3, "best_min_dist": 0.20129960248845002
"iter": 13, "tests": 82, "status": "alive", "nodes": 83, "seconds": 8.2, "escapes": 5, "best_min_dist": 0.09760407886166178
"iter": 14, "tests": 87, "status": "alive", "nodes": 88, "seconds": 9.2, "escapes": 4, "best_min_dist": 0.08661947016028955
"iter": 15, "tests": 91, "status": "alive", "nodes": 92, "seconds": 10.8, "escapes": 4, "best_min_dist": 0.0792371272963277
"iter": 16, "tests": 95, "status": "alive", "nodes": 96, "seconds": 11.1, "escapes": 4, "best_min_dist": 0.0903680094858645
"iter": 17, "tests": 99, "status": "alive", "nodes": 100, "seconds": 11.2, "escapes": 1, "best_min_dist": 0.09354937107227554
"iter": 18, "tests": 100, "status": "alive", "nodes": 101, "seconds": 13.5, "escapes": 10, "best_min_dist": 0.18307051946885614
"iter": 19, "tests": 106, "status": "alive", "nodes": 107, "seconds": 13.1, "escapes": 3, "best_min_dist": 0.10107888300951362
"iter": 20, "tests": 109, "status": "alive", "nodes": 110, "seconds": 15.3, "escapes": 3, "best_min_dist": 0.09391208149981874
"iter": 21, "tests": 112, "status": "alive", "nodes": 113, "seconds": 14.6, "escapes": 8, "best_min_dist": 0.06513331468466756
"iter": 22, "tests": 118, "status": "alive", "nodes": 119, "seconds": 19.5, "escapes": 6, "best_min_dist": 0.09449882633776303
"iter": 23, "tests": 124, "status": "alive", "nodes": 125, "seconds": 19.2, "escapes": 5, "best_min_dist": 0.08028326444488558
"iter": 24, "tests": 129, "status": "alive", "nodes": 130, "seconds": 20.6, "escapes": 3, "best_min_dist": 0.26620498352177313
"iter": 25, "tests": 132, "status": "alive", "nodes": 133, "seconds": 22.2, "escapes": 9, "best_min_dist": 0.1320471138509479
"iter": 26, "tests": 138, "status": "alive", "nodes": 139, "seconds": 23.5, "escapes": 13, "best_min_dist": 0.051263981718356895
"iter": 27, "tests": 144, "status": "alive", "nodes": 145, "seconds": 29.6, "escapes": 9, "best_min_dist": 0.05038752349949475
"iter": 28, "tests": 150, "status": "alive", "nodes": 151, "seconds": 27.6, "escapes": 5, "best_min_dist": 0.057200956696538525
```

### `segments.log`

Output as run.

```text
S10C-l0.1: 11 marks; escapes 0/16; best exact min dist 0.00000 at (83/25,167/50) t=0 theta=0.000; float margin -0.00600; 6.1s
S10C-l0.2: 11 marks; escapes 0/16; best exact min dist 0.00000 at (83/25,167/50) t=0 theta=0.000; float margin -0.00600; 6.8s
S10C-l0.3: 11 marks; escapes 0/16; best exact min dist 0.00000 at (83/25,167/50) t=0 theta=0.000; float margin -0.00600; 8.0s
K4S-l0.1: 11 marks; escapes 16/16; best exact min dist 0.01401 at (1/2,7/5) t=0 theta=0.000; float margin 0.00801; 8.2s
K4S-l0.2: 11 marks; escapes 16/16; best exact min dist 0.01401 at (1/2,36/25) t=0 theta=0.000; float margin 0.00801; 8.6s
K4S-l0.3: 11 marks; escapes 16/16; best exact min dist 0.01401 at (1/2,3/2) t=0 theta=0.000; float margin 0.00801; 8.1s
```

### `spotcheck.log`

Output as run.

```text
marks: [('segment', '(Fraction(19, 20), Fraction(1, 1))', '(Fraction(21, 20), Fraction(1, 1))'), ('segment', '(Fraction(187, 100), Fraction(1, 1))', '(Fraction(197, 100), Fraction(1, 1))'), ('segment', '(Fraction(279, 100), Fraction(1, 1))', '(Fraction(289, 100), Fraction(1, 1))')] ...
laneC interior: escape=False min=0.00000 nearest=[(['187/100', '1'], 0.0), (['141/100', '48/25'], 0.0)]
P10 wall: escape=False min=0.00000 nearest=[(['19/20', '1'], 0.0), (['187/100', '1'], 0.0)]
laneC at 3.82-type: escape=False min=0.00000 nearest=[(['187/100', '1'], 0.0), (['141/100', '48/25'], 0.0)]
300 random contained poses: 0 with positive distance to all marks; largest min-distance 0.00000
fine search (0.01 / 0.75 deg): escapes 0/12; best float margin -0.00600; best exact min dist 0.00000 at (87/100,167/50) t=0; 48s
```

### `variants.log`

Output as run.

```text
S10-l0.1: 10 marks; escapes 0; best exact min dist 0.00000 at (83/25,167/50) t=0 theta=0.00; float margin -0.00600; falsifier 10.0s; reader: nodes 404613 leaves 184756 failed 0 13.5s
S10C-l0.09: 11 marks; escapes 0; best exact min dist 0.00056 at (119/50,3781770790379/1207117678850) t=132958/320989 theta=45.00; float margin -0.00544; falsifier 8.0s; reader: nodes 432993 leaves 197007 failed 0 10.2s
S10C-l0.08: 11 marks; escapes 0; best exact min dist 0.00409 at (73/50,16426578682439/5243261590850) t=123924/299179 theta=45.00; float margin -0.00191; falsifier 7.4s; reader: nodes 659921 leaves 292913 failed 3626 14.1s
S10C-l0.07: 11 marks; escapes 5; best exact min dist 0.00763 at (119/50,178056263/56834450) t=408/985 theta=45.00; float margin 0.00163; falsifier 6.9s
S10C-l0.06: 11 marks; escapes 5; best exact min dist 0.01116 at (119/50,178056263/56834450) t=408/985 theta=45.00; float margin 0.00516; falsifier 7.0s
```

### `cover-exact-S10-l0.1.log`

Output as run.

```text
load at start: 8.44,
Tue Sep  8 05:18:14 UTC 2026
{
 "nodes": 404613,
 "certified_leaves": 184756,
 "discarded": 17551,
 "failed": 0,
 "wall_s": 8.0,
 "floor": 0.0002,
 "tau": 0.004242,
 "eps": 1e-09,
 "min_leaf_halfwidth": 0.000244140625,
 "exact_recheck": {
  "leaves": 184756,
  "failed": 0,
  "wall_s": 91.5
 },
 "marks": "/tmp/claude-0/-home-user-squares/9010767e-5bb7-5e7d-99d2-858400f3969a/scratchpad/lane-302/set-S10-l0.1.json"
}
Tue Sep  8 05:19:54 UTC 2026
load at end: 7.47,
```

### `reader_sanity.log`

Output as run.

```text
184756 leaves rebuilt; 6000 random poses in 3000 random leaves: 0 not within delta of any mark; largest least-distance lower bound seen 0.002022
```

### `set-W11.json (marks, exact)`

```text
point 29586032/29422725 29586032/29422725
point 29586032/29422725 83397232/29422725
point 83397232/29422725 29586032/29422725
point 83397232/29422725 83397232/29422725
point 48/25 48/25
point 1952/3175 3184/3175
point 1952/3175 9008/3175
point 3184/3175 1952/3175
point 3184/3175 2048/635
point 9008/3175 1952/3175
point 9008/3175 2048/635
```

### `clean-W11.json (verified escapes, exact poses)`

```text
centre (48/25, 1/2)  t = 0  cos = 1  sin = 0  theta = 0.0000 deg
  corners: (71/50, 0); (121/50, 0); (121/50, 1); (71/50, 1)
  contained: True  escape: True  least distance: 0.414487
  mark (29586032/29422725, 29586032/29422725): dist^2 = 594904389530621/3462786985702500  dist = 0.414487
  mark (83397232/29422725, 29586032/29422725): dist^2 = 594904389530621/3462786985702500  dist = 0.414487
  mark (3184/3175, 1952/3175): dist^2 = 7017201/40322500  dist = 0.417165
centre (48/25, 167/50)  t = 0  cos = 1  sin = 0  theta = 0.0000 deg
  corners: (71/50, 71/25); (121/50, 71/25); (121/50, 96/25); (71/50, 96/25)
  contained: True  escape: True  least distance: 0.414487
  mark (29586032/29422725, 83397232/29422725): dist^2 = 594904389530621/3462786985702500  dist = 0.414487
  mark (83397232/29422725, 83397232/29422725): dist^2 = 594904389530621/3462786985702500  dist = 0.414487
  mark (3184/3175, 2048/635): dist^2 = 7017201/40322500  dist = 0.417165
centre (167/50, 48/25)  t = 0  cos = 1  sin = 0  theta = 0.0000 deg
  corners: (71/25, 71/50); (96/25, 71/50); (96/25, 121/50); (71/25, 121/50)
  contained: True  escape: True  least distance: 0.414487
  mark (83397232/29422725, 29586032/29422725): dist^2 = 594904389530621/3462786985702500  dist = 0.414487
  mark (83397232/29422725, 83397232/29422725): dist^2 = 594904389530621/3462786985702500  dist = 0.414487
  mark (9008/3175, 1952/3175): dist^2 = 26143093/40322500  dist = 0.805202
centre (1/2, 48/25)  t = 0  cos = 1  sin = 0  theta = 0.0000 deg
  corners: (0, 71/50); (1, 71/50); (1, 121/50); (0, 121/50)
  contained: True  escape: True  least distance: 0.414487
  mark (29586032/29422725, 29586032/29422725): dist^2 = 594904389530621/3462786985702500  dist = 0.414487
  mark (29586032/29422725, 83397232/29422725): dist^2 = 594904389530621/3462786985702500  dist = 0.414487
  mark (1952/3175, 3184/3175): dist^2 = 7017201/40322500  dist = 0.417165
```

### `set-G11.json (marks, exact)`

```text
point 896/635 1216/635
point 7712/3175 1216/635
point 159108/79375 567573008/565826275
point 159108/79375 1605199888/565826275
point 2924153744/2921600075 2704469808/2690568025
point 2924153744/2921600075 7627311408/2690568025
point 9248/3175 3184/3175
point 9248/3175 9008/3175
point 52192/85725 48/25
point 9008/3175 6368/3175
point 48/25 48/25
```

### `clean-G11.json (verified escapes, exact poses)`

```text
centre (3/2, 26473/8450)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (254/169, 10249/4225); (373/169, 13249/4225); (253/169, 96/25); (134/169, 13224/4225)
  contained: True  escape: True  least distance: 0.063100
  mark (2924153744/2921600075, 7627311408/2690568025): dist^2 = 19909056369511099182461269153872007684/5000216934034926189033598778318296425625  dist = 0.063100
  mark (159108/79375, 1605199888/565826275): dist^2 = 591887656622726507968929/133246855389824024455140625  dist = 0.066649
  mark (896/635, 1216/635): dist^2 = 77565903509/287912730625  dist = 0.519045
centre (3/2, 239/338)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (254/169, 0); (373/169, 120/169); (253/169, 239/169); (134/169, 119/169)
  contained: True  escape: True  least distance: 0.064290
  mark (2924153744/2921600075, 2704469808/2690568025): dist^2 = 20666870968326153156171926092971374809/5000216934034926189033598778318296425625  dist = 0.064290
  mark (159108/79375, 567573008/565826275): dist^2 = 698464665043314015887072761/163227397852534429957547265625  dist = 0.065415
  mark (896/635, 1216/635): dist^2 = 2973091482/11516509225  dist = 0.508094
```

### `set-P10.json (marks, exact)`

```text
point 1 1
point 48/25 1
point 71/25 1
point 27/50 48/25
point 73/50 48/25
point 119/50 48/25
point 33/10 48/25
point 1 71/25
point 48/25 71/25
point 71/25 71/25
```

### `clean-P10.json (verified escapes, exact poses)`

```text
centre (73/50, 239/338)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (6181/4225, 0); (9156/4225, 120/169); (6156/4225, 239/169); (3181/4225, 119/169)
  contained: True  escape: True  least distance: 0.031881
  mark (48/25, 1): dist^2 = 518199696/509831700625  dist = 0.031881
  mark (1, 1): dist^2 = 22033636/20393268025  dist = 0.032870
  mark (73/50, 48/25): dist^2 = 18267701/71402500  dist = 0.505807
centre (119/50, 26473/8450)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (10068/4225, 10249/4225); (13043/4225, 13249/4225); (10043/4225, 96/25); (7068/4225, 13224/4225)
  contained: True  escape: True  least distance: 0.031881
  mark (48/25, 71/25): dist^2 = 518199696/509831700625  dist = 0.031881
  mark (71/25, 71/25): dist^2 = 22033636/20393268025  dist = 0.032870
  mark (119/50, 48/25): dist^2 = 18267701/71402500  dist = 0.505807
centre (73/50, 26473/8450)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (6181/4225, 10249/4225); (9156/4225, 13249/4225); (6156/4225, 96/25); (3181/4225, 13224/4225)
  contained: True  escape: True  least distance: 0.031881
  mark (1, 71/25): dist^2 = 518199696/509831700625  dist = 0.031881
  mark (48/25, 71/25): dist^2 = 22033636/20393268025  dist = 0.032870
  mark (73/50, 48/25): dist^2 = 18267701/71402500  dist = 0.505807
centre (119/50, 239/338)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (10068/4225, 0); (13043/4225, 120/169); (10043/4225, 239/169); (7068/4225, 119/169)
  contained: True  escape: True  least distance: 0.031881
  mark (71/25, 1): dist^2 = 518199696/509831700625  dist = 0.031881
  mark (48/25, 1): dist^2 = 22033636/20393268025  dist = 0.032870
  mark (119/50, 48/25): dist^2 = 18267701/71402500  dist = 0.505807
```

### `set-P10C.json (marks, exact)`

```text
point 1 1
point 48/25 1
point 71/25 1
point 27/50 48/25
point 73/50 48/25
point 119/50 48/25
point 33/10 48/25
point 1 71/25
point 48/25 71/25
point 71/25 71/25
point 48/25 48/25
```

### `clean-P10C.json (verified escapes, exact poses)`

```text
centre (73/50, 239/338)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (6181/4225, 0); (9156/4225, 120/169); (6156/4225, 239/169); (3181/4225, 119/169)
  contained: True  escape: True  least distance: 0.031881
  mark (48/25, 1): dist^2 = 518199696/509831700625  dist = 0.031881
  mark (1, 1): dist^2 = 22033636/20393268025  dist = 0.032870
  mark (73/50, 48/25): dist^2 = 18267701/71402500  dist = 0.505807
centre (119/50, 26473/8450)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (10068/4225, 10249/4225); (13043/4225, 13249/4225); (10043/4225, 96/25); (7068/4225, 13224/4225)
  contained: True  escape: True  least distance: 0.031881
  mark (48/25, 71/25): dist^2 = 518199696/509831700625  dist = 0.031881
  mark (71/25, 71/25): dist^2 = 22033636/20393268025  dist = 0.032870
  mark (119/50, 48/25): dist^2 = 18267701/71402500  dist = 0.505807
centre (73/50, 26473/8450)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (6181/4225, 10249/4225); (9156/4225, 13249/4225); (6156/4225, 96/25); (3181/4225, 13224/4225)
  contained: True  escape: True  least distance: 0.031881
  mark (1, 71/25): dist^2 = 518199696/509831700625  dist = 0.031881
  mark (48/25, 71/25): dist^2 = 22033636/20393268025  dist = 0.032870
  mark (73/50, 48/25): dist^2 = 18267701/71402500  dist = 0.505807
centre (119/50, 239/338)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (10068/4225, 0); (13043/4225, 120/169); (10043/4225, 239/169); (7068/4225, 119/169)
  contained: True  escape: True  least distance: 0.031881
  mark (71/25, 1): dist^2 = 518199696/509831700625  dist = 0.031881
  mark (48/25, 1): dist^2 = 22033636/20393268025  dist = 0.032870
  mark (119/50, 48/25): dist^2 = 18267701/71402500  dist = 0.505807
```

### `set-OPT-p10p1-1.json (marks, exact)`

```text
point 1 1
point 48/25 1
point 71/25 1
point 27/50 48/25
point 73/50 48/25
point 119/50 48/25
point 33/10 48/25
point 1 71/25
point 48/25 71/25
point 71/25 71/25
point 17516/7575 23823/8725
```

### `clean-OPT-p10p1-1.json (verified escapes, exact poses)`

```text
centre (73/50, 239/338)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (6181/4225, 0); (9156/4225, 120/169); (6156/4225, 239/169); (3181/4225, 119/169)
  contained: True  escape: True  least distance: 0.031881
  mark (48/25, 1): dist^2 = 518199696/509831700625  dist = 0.031881
  mark (1, 1): dist^2 = 22033636/20393268025  dist = 0.032870
  mark (73/50, 48/25): dist^2 = 18267701/71402500  dist = 0.505807
centre (73/50, 26473/8450)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (6181/4225, 10249/4225); (9156/4225, 13249/4225); (6156/4225, 96/25); (3181/4225, 13224/4225)
  contained: True  escape: True  least distance: 0.031881
  mark (1, 71/25): dist^2 = 518199696/509831700625  dist = 0.031881
  mark (48/25, 71/25): dist^2 = 22033636/20393268025  dist = 0.032870
  mark (17516/7575, 23823/8725): dist^2 = 95663912217450236676/633461809882789200625  dist = 0.388610
centre (119/50, 239/338)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (10068/4225, 0); (13043/4225, 120/169); (10043/4225, 239/169); (7068/4225, 119/169)
  contained: True  escape: True  least distance: 0.031881
  mark (71/25, 1): dist^2 = 518199696/509831700625  dist = 0.031881
  mark (48/25, 1): dist^2 = 22033636/20393268025  dist = 0.032870
  mark (119/50, 48/25): dist^2 = 18267701/71402500  dist = 0.505807
centre (68/47, 103/146)  t = 5/11  cos = 48/73  sin = 55/73  theta = 48.8879 deg
  corners: (10257/6862, 0); (14769/6862, 55/73); (9599/6862, 103/73); (5087/6862, 48/73)
  contained: True  escape: True  least distance: 0.030294
  mark (1, 1): dist^2 = 230280625/250926857476  dist = 0.030294
  mark (48/25, 1): dist^2 = 42796851876/39207321480625  dist = 0.033039
  mark (73/50, 48/25): dist^2 = 386791421/1471470125  dist = 0.512699
```

### `set-OPT-k4-1.json (marks, exact)`

```text
point 48/25 48/25
point 48/25 16929/5987
point 48/25 900/889
point 7243/7156 23337/9949
point 8755/3096 23337/9949
point 7243/7156 2243/1501
point 8755/3096 2243/1501
point 2205/779 20341/6925
point 7479/7409 20341/6925
point 2205/779 5778/6401
point 7479/7409 5778/6401
```

### `clean-OPT-k4-1.json (verified escapes, exact poses)`

```text
centre (239/338, 48/25)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (120/169, 10249/8450); (239/169, 16249/8450); (119/169, 22199/8450); (0, 16199/8450)
  contained: True  escape: True  least distance: 0.016336
  mark (7243/7156, 2243/1501): dist^2 = 3924125905535907192081/14705130830524280196602500  dist = 0.016336
  mark (7243/7156, 23337/9949): dist^2 = 30046917220006575913249/103368056926780481500896400  dist = 0.017049
  mark (7479/7409, 5778/6401): dist^2 = 29850342668424209838781/160593610404312408602500  dist = 0.431132
centre (26473/8450, 48/25)  t = 5/12  cos = 119/169  sin = 120/169  theta = 45.2397 deg
  corners: (13249/4225, 10249/8450); (96/25, 16249/8450); (13224/4225, 22199/8450); (10249/4225, 16199/8450)
  contained: True  escape: True  least distance: 0.016336
  mark (8755/3096, 23337/9949): dist^2 = 896393040732016148281/3359116834646909816902500  dist = 0.016336
  mark (8755/3096, 2243/1501): dist^2 = 3200396749668923754481/11010071119579798017960000  dist = 0.017049
  mark (2205/779, 20341/6925): dist^2 = 617972224989642381/3324664846312322500  dist = 0.431132
centre (4543/1450, 25/13)  t = 2/5  cos = 21/29  sin = 20/29  theta = 43.6028 deg
  corners: (2259/725, 917/754); (96/25, 1437/754); (2284/725, 1983/754); (1759/725, 1463/754)
  contained: True  escape: True  least distance: 0.016535
  mark (8755/3096, 23337/9949): dist^2 = 12112360286760526321/44299568566589457341025  dist = 0.016535
  mark (8755/3096, 2243/1501): dist^2 = 50195652128151222001/179258390458778577960000  dist = 0.016734
  mark (2205/779, 5778/6401): dist^2 = 1587509799727265859721/8834729945841509222500  dist = 0.423898
centre (103/146, 83/43)  t = 5/11  cos = 48/73  sin = 55/73  theta = 48.8879 deg
  corners: (55/73, 7689/6278); (103/73, 12419/6278); (48/73, 16547/6278); (0, 11817/6278)
  contained: True  escape: True  least distance: 0.014647
  mark (7243/7156, 23337/9949): dist^2 = 14274356546249035854409/66537715511370201097102756  dist = 0.014647
  mark (7243/7156, 2243/1501): dist^2 = 1892576870939861150625/6058015775311160976340624  dist = 0.017675
  mark (7479/7409, 5778/6401): dist^2 = 15006337985677197563689/88645657721375579076004  dist = 0.411442
```

### `set-POLISH-k4.json (marks, exact)`

```text
point 48/25 48/25
point 48/25 952805/939663
point 48/25 791332/280017
point 631133/622415 983925/420478
point 1934415/684508 983925/420478
point 631133/622415 681323/454220
point 1934415/684508 681323/454220
point 881115/891674 149871/183304
point 2713921/951638 149871/183304
point 881115/891674 2454115/811978
point 2713921/951638 2454115/811978
```

### `set-OPT-free-1.json (marks, exact)`

```text
point 4241/2205 7621/3996
point 509/265 8744/8641
point 2443/1272 25757/9107
point 3513/3473 22379/9542
point 28154/9955 19461/8288
point 6403/6331 13309/8897
point 27429/9698 14209/9507
point 6097/6247 5769/8470
point 25713/8989 5472/8257
point 4626/4727 7411/2437
point 27842/9749 13126/4323
```

### `set-S10-l0.1.json (marks, exact)`

```text
segment 19/20 1 21/20 1
segment 187/100 1 197/100 1
segment 279/100 1 289/100 1
segment 49/100 48/25 59/100 48/25
segment 141/100 48/25 151/100 48/25
segment 233/100 48/25 243/100 48/25
segment 13/4 48/25 67/20 48/25
segment 19/20 71/25 21/20 71/25
segment 187/100 71/25 197/100 71/25
segment 279/100 71/25 289/100 71/25
```

### `set-S10C-l0.1.json (marks, exact)`

```text
segment 19/20 1 21/20 1
segment 187/100 1 197/100 1
segment 279/100 1 289/100 1
segment 49/100 48/25 59/100 48/25
segment 141/100 48/25 151/100 48/25
segment 233/100 48/25 243/100 48/25
segment 13/4 48/25 67/20 48/25
segment 19/20 71/25 21/20 71/25
segment 187/100 71/25 197/100 71/25
segment 279/100 71/25 289/100 71/25
point 48/25 48/25
```

### `set-S10C-l0.09.json (marks, exact)`

```text
segment 191/200 1 209/200 1
segment 15/8 1 393/200 1
segment 559/200 1 577/200 1
segment 99/200 48/25 117/200 48/25
segment 283/200 48/25 301/200 48/25
segment 467/200 48/25 97/40 48/25
segment 651/200 48/25 669/200 48/25
segment 191/200 71/25 209/200 71/25
segment 15/8 71/25 393/200 71/25
segment 559/200 71/25 577/200 71/25
point 48/25 48/25
```

### `set-S10C-l0.08.json (marks, exact)`

```text
segment 24/25 1 26/25 1
segment 47/25 1 49/25 1
segment 14/5 1 72/25 1
segment 1/2 48/25 29/50 48/25
segment 71/50 48/25 3/2 48/25
segment 117/50 48/25 121/50 48/25
segment 163/50 48/25 167/50 48/25
segment 24/25 71/25 26/25 71/25
segment 47/25 71/25 49/25 71/25
segment 14/5 71/25 72/25 71/25
point 48/25 48/25
```

### `set-S10C-l0.07.json (marks, exact)`

```text
segment 193/200 1 207/200 1
segment 377/200 1 391/200 1
segment 561/200 1 23/8 1
segment 101/200 48/25 23/40 48/25
segment 57/40 48/25 299/200 48/25
segment 469/200 48/25 483/200 48/25
segment 653/200 48/25 667/200 48/25
segment 193/200 71/25 207/200 71/25
segment 377/200 71/25 391/200 71/25
segment 561/200 71/25 23/8 71/25
point 48/25 48/25
```

### `tests-gobel.json (the ten forced test squares)`

```text
G1: centre (419/809, 2754/829) t = 0
G2: centre (968/623, 2754/829) t = 0
G3: centre (419/809, 1909/835) t = 0
G4: centre (2754/829, 2754/829) t = 0
G5: centre (2754/829, 419/809) t = 0
G6: centre (1909/835, 419/809) t = 0
G7: centre (2754/829, 968/623) t = 0
G8: centre (419/809, 419/809) t = 0
G9: centre (1909/835, 1909/835) t = 41/99
G10: centre (968/623, 968/623) t = 41/99
```

### `cover_reader2.py`

```text
"""Second, independent interval reader for Theorem E.4 with a different bound.

Hausdorff bound: moving the centre by (dx, dy) and rotating by dtheta about the centre
moves every point of the unit square by at most sqrt(dx^2 + dy^2) + (sqrt2/2)|dtheta|,
and |dtheta| = 2|atan t - atan t0| <= 2 ht, so for every pose P in a box with
half-widths (ht, hx, hy) about P0
    dist(Q(P), m) <= dist(Q(P0), m) + hx + hy + sqrt2 * ht     (Euclidean <= L1).
A box is certified by a mark m when  dist(Q(P0), m) + hx + hy + (14143/10000) ht <= delta,
decided exactly as  dist^2 <= (delta - hx - hy - (14143/10000) ht)^2  with a nonnegative
base, where dist^2 between the closed square and a closed segment is the minimum over
the segment's endpoints of the point-to-square squared distance and over the square's
corners of the point-to-segment squared distance (the distance between two convex
polygons is attained at a vertex of one of them).  The float cover uses the same
formulas in doubles with a 1e-9 allowance; the exact stage re-decides every certified
leaf and every discarded box in fractions.Fraction with no allowance.  Discards, the
domain and the splitting rule are as in cover_reader.py; nothing from it is imported.
"""
import sys, json, math, time, argparse
from fractions import Fraction as F
Q = 96 / 25; DELTA = 3 / 500; EPS = 1e-9; C_T = 14143 / 10000
QF = F(96, 25); DELTAF = F(3, 500); C_TF = F(14143, 10000)
def load(path):
    out = []
    for m in json.load(open(path)):
        if m["kind"] == "point":
            a = (F(m["xy"][0]), F(m["xy"][1])); out.append((a, a))
        else:
            out.append(((F(m["a"][0]), F(m["a"][1])), (F(m["b"][0]), F(m["b"][1]))))
    return out
def corners(cx, cy, c, s):
    return [(cx + (a * c - b * s) / 2, cy + (a * s + b * c) / 2) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
def seg_d2(p, a, b, zero):
    ax, ay = a; bx, by = b; px, py = p; dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    if L2 == zero:
        return (px - ax) ** 2 + (py - ay) ** 2
    lam = ((px - ax) * dx + (py - ay) * dy) / L2
    lam = min(max(lam, zero), zero + 1)
    qx, qy = ax + lam * dx, ay + lam * dy
    return (px - qx) ** 2 + (py - qy) ** 2
def inside(cs, p):
    for i in range(4):
        (x1, y1), (x2, y2) = cs[i], cs[(i + 1) % 4]
        if (x2 - x1) * (p[1] - y1) - (y2 - y1) * (p[0] - x1) < 0:
            return False
    return True
def pt_sq_d2(cs, p, zero):
    if inside(cs, p):
        return zero
    return min(seg_d2(p, cs[i], cs[(i + 1) % 4], zero) for i in range(4))
def seg_sq_d2(cs, a, b, zero):
    cands = [pt_sq_d2(cs, a, zero), pt_sq_d2(cs, b, zero)]
    if a != b:
        cands += [seg_d2(c, a, b, zero) for c in cs]
    return min(cands)
def frame(t):
    d = 1 + t * t; return (1 - t * t) / d, 2 * t / d
def w_half(t):
    c, s = frame(t); return (c + s) / 2
def decide(marks, t1, t2, x1, x2, y1, y2, exact):
    """'discard' | 'ok' | 'split' with the arithmetic chosen by `exact`."""
    if exact:
        t1, t2, x1, x2, y1, y2 = (F(v) for v in (t1, t2, x1, x2, y1, y2)); zero = F(0); q = QF; delta = DELTAF; ct = C_TF; eps = F(0)
        mk = marks
    else:
        zero = 0.0; q = Q; delta = DELTA; ct = C_T; eps = EPS
        mk = [((float(a[0]), float(a[1])), (float(b[0]), float(b[1]))) for a, b in marks]
    wmin = min(w_half(t1), w_half(t2))
    if x2 < wmin - eps or x1 > q - wmin + eps or y2 < wmin - eps or y1 > q - wmin + eps:
        return "discard"
    t0, x0, y0 = (t1 + t2) / 2, (x1 + x2) / 2, (y1 + y2) / 2
    ht, hx, hy = (t2 - t1) / 2, (x2 - x1) / 2, (y2 - y1) / 2
    base = delta - hx - hy - ct * ht - eps
    if base < zero:
        return "split"
    c, s = frame(t0); cs = corners(x0, y0, c, s)
    for a, b in mk:
        if seg_sq_d2(cs, a, b, zero) <= base * base:
            return "ok"
    return "split"
def run(marks, floor, exact, sample=0):
    stack = [(0.0, 1.0, 0.5, Q - 0.5, 0.5, Q - 0.5)]; leaves = []; discards = []; failed = 0; nodes = 0; t0 = time.time()
    while stack:
        box = stack.pop(); nodes += 1
        st = decide(marks, *box, exact=False)
        if st == "discard": discards.append(box); continue
        if st == "ok": leaves.append(box); continue
        t1, t2, x1, x2, y1, y2 = box; ht, hx, hy = (t2 - t1) / 2, (x2 - x1) / 2, (y2 - y1) / 2
        if max(3 * ht, hx, hy) < floor: failed += 1; continue
        dim = max((3 * ht, "t"), (hx, "x"), (hy, "y"))[1]
        if dim == "t": tm = (t1 + t2) / 2; stack += [(t1, tm, x1, x2, y1, y2), (tm, t2, x1, x2, y1, y2)]
        elif dim == "x": xm = (x1 + x2) / 2; stack += [(t1, t2, x1, xm, y1, y2), (t1, t2, xm, x2, y1, y2)]
        else: ym = (y1 + y2) / 2; stack += [(t1, t2, x1, x2, y1, ym), (t1, t2, x1, x2, ym, y2)]
    res = {"nodes": nodes, "certified_leaves": len(leaves), "discarded": len(discards), "failed": failed, "wall_s": round(time.time() - t0, 1)}
    if exact and failed == 0:
        import random
        t0 = time.time()
        chosen = leaves if not sample else random.Random(11).sample(leaves, min(sample, len(leaves)))
        bad = sum(decide(marks, *b, exact=True) != "ok" for b in chosen)
        badd = sum(decide(marks, *b, exact=True) != "discard" for b in discards)
        res["exact_recheck"] = {"leaves_checked": len(chosen), "of": len(leaves), "failed": bad, "discards": len(discards), "discards_failed": badd, "wall_s": round(time.time() - t0, 1)}
    return res
if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("marks"); ap.add_argument("--floor", type=float, default=2e-4); ap.add_argument("--exact", action="store_true"); ap.add_argument("--sample", type=int, default=0); ap.add_argument("--out")
    a = ap.parse_args(); res = run(load(a.marks), a.floor, a.exact, a.sample); res["marks"] = a.marks
    print(json.dumps(res, indent=1))
    if a.out: json.dump(res, open(a.out, "w"), indent=1)
    sys.exit(0 if res["failed"] == 0 and res.get("exact_recheck", {"failed": 0, "discards_failed": 0})["failed"] == 0 else 1)
```

### `cover2-S10-l0.1.log`

Output as run (the bounded retry; the earlier full exact pass was stopped).

```text
load: 13.43,
Tue Sep  8 05:51:43 UTC 2026
exit 124
Tue Sep  8 05:58:43 UTC 2026
load: 9.63,
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
