# Agenda 030, lane G: What the segment cover and the corner pair localise at 96/25

Lane BC-299 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md) under
[H-126](../../../../hypotheses/H-126-insertion-saturation-corner-structure.md) and
[H-111](../../../../hypotheses/H-111-resource-anchor-case-exclusion.md), bead
`think-4ifm`, session record
[session-108](../../../../agent-sessions/session-108-anchors-at-q.md).
One block of 2.5 hours on one worker (`PACK_JOBS=1`) of a four-core host shared with two
other lanes; the load average is recorded beside every wall time.

Two premises entered this lane proved by earlier lanes and are used here without
re-proof: **Theorem E.4** of
[lane E](lane-e-ownership-set-at-q.md#62-the-certified-sets-and-the-threshold-in-the-segment-length)
(every contained closed unit square at `96/25` is within `√2 · 2121/500000 < 3/500` of
one of the ten horizontal segments of length `1/10` centred on Stromquist’s Figure-13
points) and the **four-corner pair theorem** of
[lane C, Session-101](lane-c-n10-transfer.md#a-four-corner-theorem-the-free-measure-does-prove)
(every packing of eleven unit squares in `[0, 96/25]²` has four distinct squares, one
per corner, whose cores contain one of the corner’s two marks `(3152/3175, 2336/3175)`,
`(2336/3175, 3152/3175)` or their images).
The anchored certificate is
[Lemma B of lane C](lane-c-n10-transfer.md#12-reconstruction-of-theorem-2-n--11-at-s--2--45-as-an-anchored-certificate).

## 0. Findings in one page

- **What the two premises localise, exactly** (Section 2). Eleven cores and ten points
  leave a core that contains no Figure-13 point, and by Theorem E.4 that escaping core
  grazes a segment: it lies within `1/100` of a segment centred on a point it does not
  contain (Theorem G.1). Since the ten segments fall into four orbits of the container’s
  midline reflections, the escape class is `K4 · (E0_C ∪ E0_W ∪ E0_O ∪ E0_I)` with four
  thin *grazing classes* as its fundamental piece.
  This is the segment analogue of Stromquist’s “every avoider is centred in a `K4`-image
  of `R`”, it holds at every angle, and it is exactly the localisation Lemma B’s branch
  2 needs; branch 1 is free at `96/25` because ten unit atoms have mass ten.
- **What they do not localise.** The corner square is not pinned to the corner segment:
  an exact `45°` square at centre `(38/25, 3/4)` contains the mark in its interior and
  is `0.009 > 3/500` from the corner segment (Proposition G.2); a corner square can be
  near any of four segments.
  Eleven squares and ten segments give a *shared* segment, a two-body event, and a
  segment can be met by four interior-disjoint unit squares, so nothing like
  Stromquist’s exactly-one ownership follows (Proposition G.3).
- **The band question is answered by the escaping square** (Section 3). The closed unit
  square with centre `(53/35, 1398/985)` and `tan(ψ/2) = 137/1198`, tilt `13.0477°`, is
  contained, avoids all ten points strictly, and is centred outside both wall rectangles
  (Theorem G.6, exact).
  So Stromquist’s ten points localise avoiders to the wall rectangles for no band
  reaching `13.05°`; the float search reads the first avoider anywhere at `11.65°` (an
  exact one at `11.67°` in the bottom wall rectangle) and the first interior one at
  `13.03°`, so the wall-localised band, if it exists, is about `1.4°` wide — below the
  `2°` the cell asked for — and is not proved.
- **Pricing an anchor is decided by one fractional packing** (Lemma G.4). If `x` is a
  fractional packing on the site set with value `V ≥ 11` and `x(E0) ≥ 1` on an anchor
  class `E0`, no measure on that site set with threshold `w` on `E0` has mass below
  `10 + w`, for any `w`. The corner-pair class is such a class on the very site set that
  proves the corner-pair theorem, because the ownership lemma’s premise — a heavy atom —
  is the complementary-slackness condition that saturates it (Corollary G.4.2): *an
  anchor proved by the ownership lemma is unpriceable on its own site set.*
- **The trade-off curve, read from the free dual** (Section 5). Run 1 solved the free
  covering LP at `96/25` on session-101’s site set (`619` orbits, `4645` sites) in
  `65 s`; its dual, rationalised down and symmetrised, is an exactly verified fractional
  packing of value `V = 45544013/4000000 = 11.386`. It charges the corner-pair class
  `1.0024` (dead for every threshold), the P10-avoiders `3.61` of its `11.39`, and the
  four grazing classes `0.841` (corner), `0.822` (wall-middle), `0.000` (row-outer) and
  `0.142` (row-inner).
  Symmetric per-type measures are therefore dead on this site set for the corner and
  wall-middle types and alive only for the row types; an asymmetric branch-2 measure
  needs at least `w > 3.42`, `3.16`, `1.39`, `1.45` respectively (a `K4`-symmetric one
  `1.51` for the row-inner type).
  Lane C’s S4 rectangle carries `0.35` (necessary `w > 1.60`), independent of its
  height.
- **No certificate and no new bound.** No claim needs an experiment id from this lane:
  Theorem G.1 is a hand proof over E.4 (whose registered replay is lane E’s follow-up),
  Lemma G.4 is a hand proof, Theorem G.6 is an exact rational pose recorded here, and
  every charge is an exact reading on one site set.
  **Recommended statuses:** H-126 open with the corner-anchor route recorded as an
  obstruction at `96/25`; H-111 open with its anchor domain now concrete (the grazing
  classes of the row types) and its next measurement named (Section 7).

## 1. The question and the falsifiers

**Question.** For which angle band do Stromquist’s ten points localise every avoiding
square at `96/25`, and can an escape-tolerant two-branch certificate close the escapes?
Rewritten for the premises that now exist: what do Theorem E.4 and the corner-pair
theorem localise, does that give Lemma B a concrete anchor, and what does the retained
instrument say about the anchor’s price.

**Falsifiers, stated before each run.**

- *Run 1 (the free LP with its dual).* Non-convergence within `1500 s`; a rationalised
  measure the exact sweep rejects; or a mass below `11`, which would make the free
  measure a certificate and the anchor question moot.
- *The post-processing.* A site at which the rationalised, symmetrised dual has depth
  above `1` (then it is not a fractional packing and no bound follows); or a corner-pair
  charge below `1` (then the complementary-slackness prediction of Corollary G.4.2 fails
  on this site set).
- *The band search.* A found pose is a theorem once its rational rounding is decided
  exactly (containment and strict avoidance of every closed-square point); a grid with
  no find is a reading at its resolution and nothing more.
- *The hand theorems.* An interior-disjoint packing whose cores all contain a Figure-13
  point (against G.1(i)); a core that avoids the points and is farther than `1/100` from
  every segment (against G.1(ii), which would contradict E.4 or the Hausdorff bound); a
  measure on the run-1 site set below `10 + w` with threshold `w` on a class of charge
  at least one (against G.4).

## 2. What Theorem E.4 and the corner pair localise

**Notation.** `q = 96/25`, `S = [0, q]²`, `B = 9977/10000`, the retained net of `181`
directions with half-tangents `k · 207107/500000/180`; its largest half-gap tangent is
`D = 207107/90000000`. `P10` is Stromquist’s ten points at `q`: the corners `(1, 1)`,
`(q − 1, 1)`, `(1, q − 1)`, `(q − 1, q − 1)`; the wall-middles `(q/2, 1)`,
`(q/2, q − 1)`; and the middle row `(27/50, q/2)`, `(73/50, q/2)`, `(q − 73/50, q/2)`,
`(q − 27/50, q/2)`. `M10` is the set of ten closed horizontal segments
`[x − 1/20, x + 1/20] × {y}` for `(x, y) ∈ P10`. `K4` is the group generated by the two
midline reflections; `P10` and `M10` are `K4`-invariant and are *not* `D4`-invariant
(the transpose of `(q/2, 1)` is not in `P10`). The four `K4`-orbits of `M10` have
representatives `σ_C` at `(1, 1)`, `σ_W` at `(q/2, 1)`, `σ_O` at `(27/50, q/2)` and
`σ_I` at `(73/50, q/2)`, of sizes `4, 2, 2, 2`. `δ₀ = √2 · 2121/500000` is E.4’s
constant.

### 2.1 The grazing localisation of the escape class

**Theorem G.1.** Let `Q₁, …, Q₁₁` be a packing of closed unit squares in `S` and let
`P_i ⊂ int Q_i` be the concentric closed `B`-square at the net direction nearest to
`Q_i`’s angle (a core, by Condition 4). Then:

1. some core contains no point of `P10`;
2. every core `P` that contains no point of `P10` satisfies `dist(P, σ) < 1/100` for
   some `σ ∈ M10`;
3. for every such core there are `g ∈ K4` and a type `T ∈ {C, W, O, I}` with
   `gP ∩ P10 = ∅` and `dist(gP, σ_T) < 1/100`.

Write `E0_T = {admissible cores P : P ∩ P10 = ∅, dist(P, σ_T) < 1/100}` and
`E0 = E0_C ∪ E0_W ∪ E0_O ∪ E0_I`. Then (3) says the escape class of the ten unit atoms
is contained in `K4 · E0`.

*Proof.* (1) The cores lie in the interiors of squares with pairwise disjoint interiors,
so they are pairwise disjoint and each point of `P10` lies in at most one; ten points
cannot meet eleven cores.
(2) By Theorem E.4 the unit square `Q ⊃ P` is within `δ₀` of some `σ ∈ M10`. `P` and `Q`
are concentric squares of sides `B` and `1` whose angles differ by at most
`arctan D ≤ D`, so every vertex of `Q` is within
`ρ = (1 − B)/√2 + (B/√2)·D < 0.0016264 + 0.0016236 < 0.00325` of the corresponding
vertex of `P`; since `P ⊂ Q` and both are convex, `d_H(P, Q) ≤ ρ`, hence
`dist(P, σ) ≤ δ₀ + ρ < 0.006 + 0.00325 < 1/100`. (3) `K4` permutes `M10` with the four
orbits named above and fixes `P10` as a set, so for `g` with `gσ = σ_T`, `gP` avoids
`P10` and `dist(gP, σ_T) = dist(P, σ)`. ∎

**Corollary G.1.1 (Lemma B at `96/25`, typed).** Let `μ₀` be the unit atoms on `P10`
(`K4`-invariant, mass `10 < 11`). Suppose that for each type `T` there is a measure
`μ₁^T` on the quarter-turn net and a threshold `w_T ≥ 1` with `μ₁^T(P) ≥ 1` for every
admissible core `P`, `μ₁^T(P) ≥ w_T` for every `P ∈ E0_T`, and mass `M_T < 10 + w_T`.
Then no packing of eleven unit squares exists in `S`.

*Proof.* By G.1 some core `P_k` avoids `P10`; by G.1(3) choose `g ∈ K4` and `T` with
`gP_k ∈ E0_T`. The images `gP_i` are pairwise disjoint admissible cores (a midline
reflection sends a net direction `θ` to `π/2 − θ` modulo quarter turns, which the
quarter-turn net contains), so
`Σ_i μ₁^T(gP_i) ≥ w_T + 10 > M_T ≥ μ₁^T(⋃ gP_i) = Σ_i μ₁^T(gP_i)`. ∎

The content of G.1 relative to lane C’s Proposition D is this: at `96/25` the ten
*points* no longer confine the avoider to a wall rectangle (the `27.5°` interior escape
of lane C, and the `13.05°` one of Section 3), but the ten *segments* confine it to
graze one of them, at every angle.
The anchor is therefore not a box but a thin class near a known short segment, in one of
four types, and Lemma B’s branch 1 costs nothing.
Whether branch 2 can be paid is Section 5.

### 2.2 The corner square is not pinned

**Proposition G.2.** Let `m₁ = (3152/3175, 2336/3175)` and let `Q*` be the closed unit
square with centre `(38/25, 3/4)` at `45°`, that is
`Q* = {(x, y) : |x − 38/25| + |y − 3/4| ≤ 1/√2}`. Then `Q* ⊂ S`, `m₁ ∈ int Q*`,
`dist(Q*, σ_C) > 3/500`, and `Q*` meets `σ_W`.

*Proof.* The vertices of `Q*` are `(38/25 ± 1/√2, 3/4)` and `(38/25, 3/4 ± 1/√2)`, all
in `S`. The `L¹` distance from `m₁` to the centre is
`(38/25 − 3152/3175) + (3/4 − 2336/3175) = 6877/12700`, whose square `0.2932` is below
`1/2`, so `m₁` is interior.
For a point `(x, 1)` of `σ_C = [19/20, 21/20] × {1}` the `L¹` distance to the centre is
at least `(38/25 − 21/20) + 1/4 = 18/25`, whose square `0.5184` exceeds `1/2`; for a
`45°` square the Euclidean distance of an outside point is the `L¹` excess over `1/√2`
divided by `√2`, here `18/(25√2) − 1/2 = 0.00912 > 3/500`. The point `(187/100, 1)` of
`σ_W` has `L¹` distance `7/20 + 1/4 = 3/5` to the centre, and `9/25 < 1/2`. ∎

So the corner-pair theorem does not place the corner square within `3/500` of the corner
segment; the axis-parallel case, where it does (an axis square containing `m₁` has its
top edge at height in `[1, 1.736]` and `x`-range containing `3152/3175`, hence contains
`(3152/3175, 1) ∈ σ_C`), is not the general case.
What is true is the diameter bound: every point of a unit square containing a mark is
within `√2` of it, and the only segments within `√2 + 3/500` of `m₁` or `m₂` are `σ_C`,
`σ_W`, `σ_O`, `σ_I` (the nearest points of the others are at distance at least `1.786`),
so *the corner square is within `3/500` of one of the four segments of its own
quadrant*. That is the whole of what the corner pair adds to E.4’s localisation.

### 2.3 The shared segment, and where exactly-one ownership fails

**Proposition G.3.** In every packing of eleven unit squares in `S` some segment of
`M10` is within `3/500` of two distinct squares.
With the corner-pair theorem, either some square other than the four corner squares is
within `3/500` of a corner segment, or the seven other squares are each within `3/500`
of one of the six non-corner segments and two of them share one.
*Proof.* Pigeonhole on `11 > 10` and on `7 > 6`. ∎

This is where the transfer from `s(10)` stops.
Stromquist’s bijection needs `|P| = n` with points, which no square can share; here the
count is `11 > 10`, the marks are segments, and a segment of length `1/10` can be met by
four interior-disjoint unit squares (the four axis squares around `(1, 1)`), so the
shared segment is a two-body event with no forced position for either body, and the free
eleventh mark of H-134 has not been placed.
The set-ownership form of Lemma C′ (any atom set of weight above `ε` meets a core) gives
occupancy statements of the kind lane A already has, not a pinned square.

### 2.4 Pricing an anchor: weak duality on the site set

**Lemma G.4.** Let `Σ` be a site set, `x = (x_r)` a fractional packing on `Σ`: a finite
family of admissible cores `P_r` with weights `x_r ≥ 0` such that
`Σ_{r : s ∈ P_r} x_r ≤ 1` for every `s ∈ Σ`, of value `V = Σ_r x_r`. Let `E0` be any
class of admissible cores, `w ≥ 1`, and let `μ` be any measure supported on `Σ` — no
symmetry required — with `μ(P) ≥ 1` for every admissible core and `μ(P) ≥ w` for every
`P ∈ E0`. Then

`μ(S) ≥ V + (w − 1) · x(E0)`, where `x(E0) = Σ_{r : P_r ∈ E0} x_r`.

*Proof.* `μ(S) = Σ_s μ_s ≥ Σ_s μ_s Σ_{r : s ∈ P_r} x_r = Σ_r x_r μ(P_r) ≥ Σ_r x_r c_r`
with `c_r = w` on `E0` and `1` elsewhere.
∎

**Corollary G.4.1.** If `V ≥ 11` and `x(E0) ≥ 1` then `μ(S) ≥ 10 + w` for every `w ≥ 1`:
on `Σ` there is no branch-2 measure of Corollary G.1.1 (nor any conditional certificate
of X-014 Lemma-2 type) with anchor `E0`, at any threshold.
If `x(E0) < 1`, a branch-2 measure needs `w > 1 + (V − 11)/(1 − x(E0))`. For a `D4`- or
`K4`-symmetric `μ` the same holds with `E0` replaced by its orbit union.

**Corollary G.4.2 (anchors proved by ownership are unpriceable on their site set).** Let
`μ*` be the optimum of the free covering LP on `Σ` with mass `11 + ε`, `ε ≥ 0`, and `x`
its optimal dual, symmetrised.
If an atom `a` has `μ*({a}) > 0` then `x` saturates `a` (complementary slackness: the
orbit constraint `Σ_r x_r · #(O ∩ P_r) ≤ |O|` is tight when the orbit’s weight is
positive, and symmetrising spreads that to depth `1` at every member), so every class
`E0 ⊇ {P : a ∈ P}` has `x(E0) ≥ 1` and is dead by G.4.1. The ownership lemma’s premise
for anchoring a core at `a` — weight above `ε` at `a` — is precisely this condition.
So the corner-pair anchor, proved on session-101’s site set from the free measure,
cannot be priced on that site set at any threshold; Section 5 exhibits the number.

The lesson is structural rather than numerical: a fractional packing already pays a unit
at every heavy atom, so re-charging an integral packing for containing that atom gives
the LP nothing.
An anchor with headroom must be a class the fractional packing under-uses
relative to its integral obligation, which is what G.1’s grazing classes are candidates
for.

## 3. The band question: the escaping square

**Theorem G.6 (exact).** Let `t = 137/1198`, `ψ = 2 arctan t = 13.0477°`, and let `Q` be
the closed unit square with centre `(53/35, 1398/985)` and tilt `ψ`. Then `Q ⊂ S`, the
centre of `Q` lies outside both wall rectangles `[1, q − 1] × [0, 1]` and
`[1, q − 1] × [q − 1, q]`, and `Q` contains none of the ten points: in `Q`’s frame,
`max(|u| − 1/2, |v| − 1/2) ≥ 3930001/100251438350 > 0` for every point of `P10`.
Likewise the closed unit square with centre `(115/77, 565/956)` and
`tan(ψ/2) = 191/1869` (`ψ = 11.6700°`) is a contained avoider whose centre lies in the
bottom wall rectangle.

*Proof.* Exact rational evaluation of the half-extent `(cos ψ + sin ψ)/2` with
`cos ψ = (1 − t²)/(1 + t²)`, `sin ψ = 2t/(1 + t²)`, of the containment inequalities, of
the rectangle membership, and of the ten frame margins, all in `fractions.Fraction`
(`band.py`, Appendix; the script refuses to print a witness that fails any of them).
∎

*Readings, not theorems.* On the grid of step `0.01` in the centre and `0.25°`
(interior) or `0.05°` (wall rectangles) in the tilt, refined by bisection with a centre
step `0.0025`, the least tilt of any avoider is `11.65°` (in a wall rectangle, margin
`0.0002`) and the least tilt of an avoider centred outside the wall rectangles is
`13.03°` (margin at the grid `0.0003`). Below `11.65°` neither search found an avoider.

*What this settles.* The cell asked for a localisation theorem “for a band of at least
`2°`, or the escaping square”; the answer is the escaping square.
Every band `[0, α]` with `α ≥ 13.05°` contains an interior avoider, so Stromquist’s
wall-rectangle localisation holds at `96/25` for no such band; if it holds at all it
holds on a band inside `[11.65°, 13.05°)`, about `1.4°` wide, and proving it would need
an interval certificate over that band, which was not run.
The mechanism is the row slack: the rows `y = 1` and `y = q/2` are `0.92` apart and the
points in a row are `0.92` apart, so an axis square always contains a point, and the
first avoider appears when the tilt lets the row `y = 1` cut the square’s top wedge in a
chord shorter than `0.92` between two points — at `11.67°` the chord is `0.918`. H-106’s
near-axis clause (no avoider at all) therefore extends at `96/25` to a band of about
`11.6°` by this reading, far beyond the `±0.25°` it certified at `1939/500`; the band
the anchor route needs is not this one but G.1’s, which holds at every angle.

## 4. Runs, inputs and exact verdicts

**Inputs common to every run.** Side `96/25`, shrink `9977/10000`, the retained
`181`-direction net (`certificate.json`: half-tangent limit `207107/500000`, `180` equal
steps), `D = 207107/90000000`; site set as in session-101’s start: T-018’s `1121` atoms
scaled by `128/127` unioned with the library’s density grids
`site_counts_for_side(96/25, 9977/10000) = (25, 34, 42)` at inset `1/2`, closed under
`D4` — `619` orbits, `4645` sites; `solve_rows` with `rows_per_direction 3`, at most
`100` rounds, deadline `1500 s`, no column rounds (the run wants the dual on the stated
site set, not a lighter measure); `rationalise_sites` at scale `4 000 000` with the
`1000001/1000000` bump for the measure; the dual rationalised *down* (scaled by
`999999/1000000`, floored at `1/4000000`), placements with centres rationalised at
denominator `10⁶` and clamped into the exact centre domain as `colgen.dual_squares`
does, then spread over the eight `D4` images at weight `1/8`; interpreter the project’s
Python 3.14 from the frozen environment; `sqpack` unmodified.

**Run 1 (the free LP with its dual).** Converged: “every placement covers mass 1” after
`21` rounds, `4775` rows, objective `11.386020301400558`, least covered placement
`0.99999999999996`; wall `65.2 s`, load `0.35` before and `1.53` after.
Rationalised measure: mass `45544287/4000000 = 11.38607175` over `329` atoms; the exact
sweep in one worker (`11.7 s`, load `1.45`): Conditions 1, 3, 4 and 5 hold, least cell
`400001/400000` at direction `0`, Condition 2 fails as it must at that mass.
The falsifier is not met.
The value sits above session-101’s phase-D `11.262` because that reading followed ten
column rounds on `637` orbits; the site set here is the one the pair theorem’s measure
started from, and the dual is what the lane needs.

**Post-processing (`charges.py`, `14.8 s`, load `1.2` to `1.6`).** `45` rows carry a
positive dual (their float total equals the objective to `10⁻¹²`, as strong duality
requires); `360` symmetrised placements; value `V = 45544013/4000000 = 11.38600325`
exactly.
Depth at every one of the `4645` sites, decided as an exact sum over memberships
flagged in floats with a conservative `10⁻⁹` band (so the flagged sum is an upper bound
on the exact depth): at most `15999983/16000000 < 1`; `893` sites at depth `≥ 0.999`.
The marks `(3152/3175, 2336/3175)` and `(2336/3175, 3152/3175)` are sites and carry
depth `15999983/16000000` each — saturated, as Corollary G.4.2 predicts; the scaled
T-018 corner atom `(29586032/29422725, ·)` carries `7124827/8000000 = 0.891` and, as in
session-101, weight `0` in the measure.
Neither post-processing falsifier is met.

**The band searches (`band.py`).** Interior: `11.6 s`; wall rectangles: `12.5 s`; load
`1.2` to `1.7`; the exact witnesses of Theorem G.6.

## 5. The trade-off curve

Every number below is `x(E0)` for the exactly verified fractional packing `x` of run 1,
an exact rational printed to six places (lower and upper bounds coincide except where a
segment-distance test is sampled, where they still agreed at this resolution), and the
verdict is Corollary G.4.1 with `V = 11.386`. Classes are in the bottom-left frame; “any
core” has no avoidance filter; “grazing” means the core contains no point of `P10`. The
radius `h` is the Euclidean distance from the core to the segment.

| Anchor class `E0` | charge | verdict for a branch-2 measure on this site set |
| --- | --- | --- |
| core contains `m₁` or `m₂` (the corner pair) | `1.002367` | dead for every `w` |
| core contains the scaled T-018 corner atom | `0.890603` | needs `w > 4.53` |
| all `P10`-avoiding cores (Lemma B’s `E`) | `3.608129` | dead for every `w` |
| within `1/100` of `σ_C`, any core / grazing | `2.335340` / `0.840596` | dead / needs `w > 3.42` |
| within `1/5` of `σ_C`, any core / grazing | `2.542421` / `0.858685` | dead / needs `w > 3.73` |
| within `1/100` of `σ_W`, any core / grazing | `1.844134` / `0.821522` | dead / needs `w > 3.16` |
| within `1/5` of `σ_W`, any core / grazing | `2.134337` / `0.826258` | dead / needs `w > 3.22` |
| within `1/100` to `1/5` of `σ_O`, any core / grazing | `0.999999` / `0` | needs `w > 2.9 · 10⁵` / needs `w > 1.386` |
| within `1/100` of `σ_I`, any core / grazing | `1.483797` / `0.142054` | dead / needs `w > 1.45` |
| within `1/20` of `σ_I`, any core / grazing | `1.815750` / `0.209566` | dead / needs `w > 1.49` |
| `K4`-union, grazing: `σ_C` (4 images) / `σ_W` (2) / `σ_O` (2) / `σ_I` (2) | `3.362383` / `1.643044` / `0` / `0.245745` | dead / dead / needs `w > 1.39` / needs `w > 1.51` |
| `D4`-union, grazing: `σ_C` (8) / `σ_W` (4) / `σ_O` (4) / `σ_I` (4) | `3.362383` / `1.643044` / `1.406770` / `0.245745` | dead / dead / dead / needs `w > 1.51` |
| centre within `1/2` of `σ_C`’s centre, any / grazing | `1.435235` / `0.150851` | dead / needs `w > 1.45` |
| centre within `1/2` of `σ_W`’s centre, any / grazing | `0.864217` / `0.330852` | needs `w > 3.84` / needs `w > 1.58` |
| centre within `1/2` of `σ_I`’s centre, any / grazing | `0.870966` / `0.178123` | needs `w > 3.99` / needs `w > 1.47` |
| centre within `3/10` or less of any segment centre, grazing | `0` | needs `w > 1.386` |
| lane C’s S4: centre in `[1, q/2] × [0, h]`, `h ∈ {1, 11/10, 6/5}`, any / avoiding the three bottom-row points | `0.499999` / `0.351692` | needs `w > 1.77` / needs `w > 1.60` |

Three checks are in the table.
Every grazing core of the dual is within `1/100` of some segment (`0` exceptions), as
Theorem G.1(2) requires of cores arising from contained unit squares.
For the dual’s admissible `B`-cores this is a separate check: the theorem’s proof needs
a contained unit-square parent, which an arbitrary admissible `B`-core need not have.
The corner-pair class is dead with charge above one, Corollary G.4.2 realised.
And the `σ_O` class with no avoidance filter carries `0.999999` on twenty squares: the
free packing puts exactly a unit of weight on cores containing `(27/50, q/2)`, which is
a Figure-13 point *and* a saturated site of this dual, yet not one of those cores avoids
the point — the row-outer segment is where the fractional packing’s integral and
fractional obligations coincide, and the grazing class beside it is empty.

**What the curve says.** Read as `h ↦ (M₀(E), w(E0))` in the cell’s terms: branch 1 is
free (`M₀ = 10`) at every `h` because the localisation is G.1’s, not a box; the binding
question is the branch-2 threshold, and its floor is set by the charge.
The corner and wall-middle grazing classes carry `0.82` to `0.86` at every radius from
`1/100` to `1/5` — the fractional packing lives there — so a symmetric per-type measure
is dead for those types on this site set, and an asymmetric one would need to place more
than `2.4` extra units of threshold on a class the free measure already covers at `1`.
The row types are different: the row-outer grazing class is empty of dual weight at
every radius and the row-inner one carries `0.14` to `0.25`, so for those two types the
necessary threshold is `1.39` to `1.51`, within the range Stromquist’s `w = 3` scheme
paid. No run of the threshold program itself was made; the reading is one fractional
packing, and a threshold program’s own dual can only be heavier.

**Which pose classes carry the binding rows.** The `45` binding placements sit at `37`
net directions from `0°` to `45°`. Of their `360` symmetrised images, `48` are grazing
cores; in the bottom-left frame `5` graze the corner segment (at `0°`, `0.53°` and
`45°`), `18` the wall-middle segment (at `0°`, `0.53°` and six directions from `13.39°`
to `22.9°`), none the row-outer segment, and `16` the row-inner segment (the same six
tilted directions only).
So the near-axis grazers are the cores that slide along the row `y = 1` past its points,
and the tilted grazers at `13°` to `23°` are the interior-escape poses of Section 3 seen
from the dual’s side: the fractional packing puts its weight exactly where the point set
first admits avoiders.

## 6. Obstructions and status

- **The corner pair prices nothing on its own site set.** Corollary G.4.2 is the general
  form of session-101’s observation that pricing the corner orbit leaves it at weight
  zero: any anchor the LP already pays for is charged one by its dual.
  The four-corner containment theorem is a true structural statement and, on the
  retained instrument, an unpriceable one.
  For H-126 this is the obstruction to the corner-anchor route, recorded with its site
  set.
- **Symmetric measures cannot anchor a `K4`-symmetric point set at the corners or the
  walls.** On the run-1 site set the `K4`-union charges of the corner and wall-middle
  grazing classes are `3.36` and `1.64`; Corollary A.2 of lane C (the `K4`-average of
  Stromquist’s data is not a certificate) is the same fact at `2 + 4/√5`.
- **The band is narrower than the cell hoped.** The wall-rectangle localisation of point
  avoiders fails from `13.05°` (exact) and avoiders exist from `11.65°` (reading); the
  localisation that survives is the segment one, which is a thin class rather than a box
  and needs a threshold measure shaped to it.
- **The segment premise is a two-body premise for ownership.** Nothing in E.4 plus the
  corner pair pins a single square to a single segment; the shared-segment split of G.3
  needs pair rows, which the retained row generator does not have, and the atoms a pair
  measure would want sit on the shared segment itself, where the cores of two touching
  squares leave them uncounted.
- **What was not run.** The threshold program for the row types (an instrument
  extension: a row generator with the grazing predicate on the `D4` images of a
  placement); the interval certificate of the no-avoider band below `11.6°` (H-106’s
  reader with `q` and the band as parameters, the cell’s own instrument); the event-cell
  filter of lane C’s S4 and its mutation test.

**Recommended status for H-126:** open, unchanged in kind; the corner-anchor route is
recorded as an obstruction at `96/25` on the retained shrink, net and session-101’s site
set (Corollary G.4.2 with the charge `1.002367`), and the corner square’s pose is
localised only to the four segments of its quadrant (Proposition G.2).

**Recommended status for H-111:** open, with the anchor domain now concrete: Theorem G.1
gives the complete pose cover its branch 1 for free, the anchor classes are the four
grazing classes, and the retained instrument’s reading is that only the row types can be
priced; the next measurement is named below.
No claim is frozen and no experiment id is needed.

## 7. What the next session does first

1. Run the threshold program for the row-inner type on the run-1 site set: a
   `D4`-symmetric measure with `μ ≥ 1` everywhere and `μ ≥ w` on every placement one of
   whose `D4` images is a grazing core within `1/100` of `σ_I`, for `w ∈ {3/2, 2, 5/2}`,
   decided by the exact sweep; certificate iff the mass is below `10 + w`. The row
   generator needs the grazing predicate on the eight images of a placement;
   `placement_cells` supplies the least-mass cells, so the class’s own least-mass cells
   need a second pass restricted to the class.
   The row-outer type needs a `K4`-symmetric measure (its `D4`-union is dead, its
   `K4`-union is empty on this dual).
   It can use the same folded angle range once the row generator and exact symmetry
   check support `K4`.
2. If the threshold program leaves a class alive, do the same on session-101’s
   `637`-orbit site set with column rounds, where the free value is `11.262`.
3. Only if a band theorem is wanted: the interval certificate that no contained unit
   square of folded tilt at most `11°` avoids `P10` at `96/25` (the H-106 reader with
   `q` and the band as parameters).

**Readiness correction, 2026-09-08.** The earlier claim that the row-outer `K4` program
requires a quarter-turn sweep was too strong.
A vertical reflection in `K4` sends a square’s angle `θ`, modulo `π/2`, to `π/2 − θ`.
Both the measure and the `K4`-orbit union of the row-outer grazing class are invariant
under that reflection, so checking `[0, π/4]` covers the remaining angles as well.
The missing instrument is the region-class separator and a verifier that checks the
declared `K4` symmetry; `classcert._symmetry_report` currently accepts only `D4`. A
small-grid comparison against an expanded angular sweep and a broken-symmetry mutation
should guard that extension.
The threshold program was not run in session-108. A row-type exclusion would still leave
the corner and wall-middle types of Corollary G.1.1 to discharge.

## 8. Inputs and resources

- Side `96/25`, shrink `9977/10000`, net `k · 207107/500000/180`, `k = 0..180`; site set
  `619` orbits, `4645` sites (T-018 scaled by `128/127` plus grids `25, 34, 42` at inset
  `1/2`); rows `4775`; dual rows with positive weight `45`.
- Rationalisation: measure up at scale `4 000 000` with bump `1000001/1000000`; dual
  down by `999999/1000000` then floored at `1/4000000`; centres at denominator `10⁶`,
  clamped.
- Marks: `m₁ = (3152/3175, 2336/3175)`, `m₂ = (2336/3175, 3152/3175)`; scaled corner
  atom `(29586032/29422725, 29586032/29422725)`; `P10` and `M10` as in Section 2;
  segment-distance tests sampled at `401` points per segment with the `1`-Lipschitz
  sampling error added to the lower bound and a `10⁻⁹` float allowance.
- Band search: centre step `0.01` on the fundamental domain `[w, q/2]²`, tilt steps
  `0.25°` (interior) and `0.05°` (wall rectangles), forty bisection steps with centre
  step `0.0025`, then the tilt slack menu `0.02°` to `0.5°` with centre step `0.002`,
  rationalised at denominators `2000` (half-tangent) and `1000` (centre), decided
  exactly.
- Wall times with the load average: run 1 `65.2 s` at `0.35` to `1.53`; its exact sweep
  `11.7 s` at `1.45`; `charges.py` `14.8 s` at `1.2` to `1.6`; the band searches
  `11.6 s` and `12.5 s` at `1.2` to `1.7`. One worker throughout; four cores shared with
  two other lanes.
- No repository code was modified; every script is lane-owned and reproduced below.

## Appendix: scripts and outputs as run

Every script ran from `<worktree>/packing` as
`PACK_JOBS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 uv run --frozen --all-extras --group dev python <script> <args>`
with the project interpreter; the scripts are lane-owned and none was promoted to
`devtools/`.

### `free_dual.py` (run 1: the free LP with its dual saved)

```text
"""Lane BC-299, run 1: the free covering LP at 96/25 on session-101's site set, dual saved.

Same inputs as session-101's phase A/D start (seed = T-018's atoms scaled by 128/127,
density grids 25/34/42 at inset 1/2, rows_per_direction 3), no column rounds: the point
of the run is the dual, a D4-symmetrisable fractional packing on the site set, not the
measure.  Everything the post-processor needs is dumped as JSON.
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction
from pathlib import Path

from sqpack.fractional.certificate import Certificate, verify
from sqpack.fractional.colgen import (
    Rows,
    rationalise_sites,
    site_counts_for_side,
    site_set_from_points,
    solve_rows,
)
from sqpack.fractional.generate import build_site_grid

out = Path(sys.argv[1])
L = Fraction(96, 25)
B = Fraction(9977, 10000)
LIMIT = Fraction(207107, 500000)
STEPS = 180
half_tangents = tuple(LIMIT * k / STEPS for k in range(STEPS + 1))

cert = json.load(open(Path("cases/n11_fractional_certificate/certificate.json")))
assert Fraction(cert["outer_side"]) == Fraction(381, 100)
assert Fraction(cert["angle_limit"]) == LIMIT and cert["direction_steps"] == STEPS
scale = L / Fraction(381, 100)
seed = {(Fraction(x) * scale, Fraction(y) * scale) for x, y, _ in cert["atoms"]}
counts = site_counts_for_side(L, B)
points = set(seed)
for count in counts:
    points.update(build_site_grid(L, count, Fraction(1, 2)).positions())
sites = site_set_from_points(L, points)
print("grids", counts, "orbits", len(sites.orbits), "sites", sites.size, flush=True)

rows = Rows()
started = time.perf_counter()
load0 = os.getloadavg()
solution = solve_rows(
    sites, B, half_tangents, rows, max_rounds=100, rows_per_direction=3, deadline=started + 1500
)
wall = time.perf_counter() - started
load1 = os.getloadavg()
print(
    "stopped:", solution.stopped, "objective", repr(solution.objective), "rounds", solution.rounds,
    "rows", len(rows), "least_covered", solution.least_covered, "wall", round(wall, 1),
    "load", load0, load1, flush=True,
)
atoms = rationalise_sites(sites, solution.weights, scale=4_000_000)
mass = sum((a.weight for a in atoms), start=Fraction(0))
print("rationalised mass", mass, float(mass), "atoms", len(atoms), flush=True)

record = {
    "id": "bc-299-run1-free-dual-96-25",
    "outer_side": str(L),
    "square_side": str(B),
    "angle_limit": str(LIMIT),
    "direction_steps": STEPS,
    "grid_counts": list(counts),
    "inset": "1/2",
    "seed": "T-018 atoms scaled by 128/127",
    "orbits": [[[str(x), str(y)] for x, y in orbit] for orbit in sites.orbits],
    "lp_objective": solution.objective,
    "stopped": solution.stopped,
    "rounds": solution.rounds,
    "least_covered": solution.least_covered,
    "wall_seconds": wall,
    "load_before": load0,
    "load_after": load1,
    "rows": [
        [int(d), float(cu), float(cv), float(y)]
        for d, (cu, cv), y in zip(rows.directions, rows.centres, solution.duals, strict=True)
    ],
    "weights": [float(w) for w in solution.weights],
    "atoms": [[str(a.x), str(a.y), str(a.weight)] for a in atoms],
    "rationalised_mass": str(mass),
}
out.write_text(json.dumps(record))
print("wrote", out, flush=True)

started = time.perf_counter()
verdict = verify(
    Certificate(11, L, B, atoms, half_tangents), workers=1
)
print("verify wall", round(time.perf_counter() - started, 1), "load", os.getloadavg(), flush=True)
print(verdict, flush=True)
```

### `charges.py` (the exact fractional packing and the charge of every class)

```text
"""Lane BC-299, post-processing of run 1: the free dual as an exact fractional packing,
and its charge on every anchor class the lane prices.

Reads run1-free-dual.json.  Rationalises the row duals *down* (scaled by 1 - 1e-6, floored
at 1/4000000), builds the exact placements (centres rationalised at 10^6 and clamped into
the centre domain, as colgen.dual_squares does), spreads each over its eight D4 images at
weight/8, and verifies exactly that the depth at every site is at most 1 (memberships
flagged in floats with a conservative 1e-9 band, weights summed as Fractions).  Then for
each class it reports a lower and an upper bound on the charge x(E0) = sum of weights of
placements in E0, and the verdict weak duality gives: a threshold-w measure on this site
set has mass at least V + (w - 1) x(E0).
"""

from __future__ import annotations

import json
import math
import sys
import time
from fractions import Fraction

import numpy as np

from sqpack.fractional.colgen import square_at
from sqpack.fractional.generate import direction_net

path = sys.argv[1]
run = json.load(open(path))
L = Fraction(run["outer_side"])
B = Fraction(run["square_side"])
LIMIT = Fraction(run["angle_limit"])
STEPS = run["direction_steps"]
half_tangents = tuple(LIMIT * k / STEPS for k in range(STEPS + 1))
directions = direction_net(half_tangents)
SCALE = 4_000_000
DOWN = Fraction(999999, 1000000)

sites = [(Fraction(x), Fraction(y)) for orbit in run["orbits"] for x, y in orbit]
site_arr = np.array([[float(x - L / 2), float(y - L / 2)] for x, y in sites])
print("sites", len(sites))

# exact placements with rationalised-down weights
placements = []
raw_total = 0.0
for d, cu, cv, y in run["rows"]:
    if y <= 1e-12:
        continue
    raw_total += y
    direction = directions[d]
    cosine, sine = float(direction.ux), float(direction.uy)
    x = Fraction(cosine * cu - sine * cv).limit_denominator(10**6)
    yy = Fraction(sine * cu + cosine * cv).limit_denominator(10**6)
    extent = B * (direction.ux + direction.uy) / 2
    x = min(max(x, extent), L - extent)
    yy = min(max(yy, extent), L - extent)
    weight = Fraction(math.floor(Fraction(y) * DOWN * SCALE), SCALE)
    if weight <= 0:
        continue
    placements.append((square_at(direction, (x, yy), L, B), weight, d))
print("rows with positive dual", len(placements), "raw dual total", raw_total)

# symmetrise
family = []
for square, weight, d in placements:
    for image in square.images():
        family.append((image, weight / 8, d))
V = sum((w for _, w, _ in family), start=Fraction(0))
print("symmetrised squares", len(family), "V =", V, float(V))

# exact-ish depth: float flags with a conservative band, exact weight sums
started = time.perf_counter()
axes = np.array([[[float(s.ax), float(s.ay)], [float(s.bx), float(s.by)]] for s, _, _ in family])
offs = np.array([[float(s.u), float(s.v)] for s, _, _ in family])
half = float(B / 2)
weights_f = np.array([float(w) for _, w, _ in family])
# inside flags: |a.q - u| <= half + 1e-9 and |b.q - v| <= half + 1e-9
au = axes[:, 0, :] @ site_arr.T - offs[:, [0]]
bv = axes[:, 1, :] @ site_arr.T - offs[:, [1]]
inside = (np.abs(au) <= half + 1e-9) & (np.abs(bv) <= half + 1e-9)
depth_f = weights_f @ inside
worst = int(np.argmax(depth_f))
print("float depth max", depth_f.max(), "at site", sites[worst])
# exact sums at every site over the flagged pairs
max_depth = Fraction(0)
tight = 0
depth_exact = []
for j in range(len(sites)):
    total = Fraction(0)
    for i in np.nonzero(inside[:, j])[0]:
        total += family[i][1]
    depth_exact.append(total)
    if total > max_depth:
        max_depth = total
    if total >= Fraction(999, 1000):
        tight += 1
print("exact depth max", max_depth, float(max_depth), "sites with depth >= 0.999:", tight,
      "wall", round(time.perf_counter() - started, 1))
assert max_depth <= 1, "the rationalised dual is not a fractional packing"

# marks and points
m1 = (Fraction(3152, 3175), Fraction(2336, 3175))
m2 = (Fraction(2336, 3175), Fraction(3152, 3175))
corner_atom = (Fraction(29586032, 29422725), Fraction(29586032, 29422725))
q = L
P10 = []
for x, y in [(Fraction(1), Fraction(1)), (q / 2, Fraction(1)), (Fraction(3, 2) - q / 4, q / 2), (Fraction(1, 2) + q / 4, q / 2)]:
    for xx in {x, q - x}:
        for yyy in {y, q - y}:
            P10.append((xx, yyy))
P10 = sorted(set(P10))
assert len(P10) == 10
seg_centres = {"C": (Fraction(1), Fraction(1)), "W": (q / 2, Fraction(1)),
               "O": (Fraction(3, 2) - q / 4, q / 2), "I": (Fraction(1, 2) + q / 4, q / 2)}
for name, (x, y) in seg_centres.items():
    assert (x, y) in P10
for p in (m1, m2, corner_atom):
    idx = [j for j, s in enumerate(sites) if s == p]
    print("site", p, "index", idx, "depth", [str(depth_exact[j]) for j in idx])


def covers(square, point):
    return square.covers(point[0] - L / 2, point[1] - L / 2)


def dist_point_square_f(square, px, py):
    """Float distance from a point to a closed square, in the square's frame."""
    qx, qy = px - float(L / 2), py - float(L / 2)
    du = abs(float(square.ax) * qx + float(square.ay) * qy - float(square.u)) - half
    dv = abs(float(square.bx) * qx + float(square.by) * qy - float(square.v)) - half
    return math.hypot(max(du, 0.0), max(dv, 0.0))


SAMPLES = np.linspace(-0.05, 0.05, 401)
HALF_STEP = 0.05 / 400  # 1-Lipschitz in the point, so this bounds the sampling error


def dist_segment_bounds(square, cx, cy):
    """(lower, upper) bounds on the distance from the square to the horizontal segment."""
    ds = [dist_point_square_f(square, float(cx) + t, float(cy)) for t in SAMPLES]
    m = min(ds)
    return m - HALF_STEP - 1e-9, m + 1e-9


def centre_of(square):
    """Exact absolute centre of the placement."""
    x = square.ax * square.u + square.bx * square.v + L / 2
    y = square.ay * square.u + square.by * square.v + L / 2
    return x, y


avoid = [all(not covers(s, p) for p in P10) for s, _, _ in family]
print("charge of P10-avoiders (all directions, exact):",
      float(sum((w for (s, w, _), a in zip(family, avoid, strict=True) if a), start=Fraction(0))))
seg_d = {name: [dist_segment_bounds(s, cx, cy) for s, _, _ in family] for name, (cx, cy) in seg_centres.items()}
centres = [centre_of(s) for s, _, _ in family]


def charge(flags_lower, flags_upper):
    lo = sum((family[i][1] for i in range(len(family)) if flags_lower[i]), start=Fraction(0))
    hi = sum((family[i][1] for i in range(len(family)) if flags_upper[i]), start=Fraction(0))
    return lo, hi


def verdict(lo, hi):
    if lo >= 1:
        return "dead for every w"
    need = 1 + (V - 11) / (1 - hi) if hi < 1 else float("inf")
    return f"alive only with w > {float(need):.4f}"


rows_out = []


def report(label, flags_lower, flags_upper):
    lo, hi = charge(flags_lower, flags_upper)
    n_lo = sum(flags_lower)
    n_hi = sum(flags_upper)
    print(f"{label:58s} charge in [{float(lo):.6f}, {float(hi):.6f}]  squares {n_lo}/{n_hi}  {verdict(lo, hi)}")
    rows_out.append((label, str(lo), str(hi), n_lo, n_hi, verdict(lo, hi)))


print("\n== anchor classes in the bottom-left frame (charges under the D4-symmetrised dual) ==")
cp = [covers(s, m1) or covers(s, m2) for s, _, _ in family]
report("corner pair: core contains m1 or m2", cp, cp)
ca = [covers(s, corner_atom) for s, _, _ in family]
report("scaled T-018 corner atom in the core", ca, ca)
for name in "CWOI":
    for h in (Fraction(1, 100), Fraction(1, 50), Fraction(1, 20), Fraction(1, 10), Fraction(1, 5)):
        lo_f = [d[1] <= float(h) for d in seg_d[name]]
        hi_f = [d[0] <= float(h) for d in seg_d[name]]
        report(f"within {h} of segment {name}, any core", lo_f, hi_f)
        report(f"within {h} of segment {name}, P10-avoiding core", [a and f for a, f in zip(avoid, lo_f, strict=True)],
               [a and f for a, f in zip(avoid, hi_f, strict=True)])
print("\n== union over the four types (E of Lemma B, the whole grazing class) ==")
for h in (Fraction(1, 100), Fraction(1, 50), Fraction(1, 20)):
    any_lo = []
    any_hi = []
    for i in range(len(family)):
        lo_any = False
        hi_any = False
        for name, (cx, cy) in seg_centres.items():
            for gx in {cx, q - cx}:
                for gy in {cy, q - cy}:
                    dl, dh = dist_segment_bounds(family[i][0], gx, gy) if (gx, gy) != (cx, cy) else seg_d[name][i]
                    lo_any |= dh <= float(h)
                    hi_any |= dl <= float(h)
        any_lo.append(lo_any)
        any_hi.append(hi_any)
    report(f"within {h} of some segment, any core", any_lo, any_hi)
    report(f"within {h} of some segment, P10-avoiding core", [a and f for a, f in zip(avoid, any_lo, strict=True)],
           [a and f for a, f in zip(avoid, any_hi, strict=True)])
    print("   P10-avoiders NOT within", h, "of any segment (upper flag false):",
          sum(1 for a, f in zip(avoid, any_hi, strict=True) if a and not f))

print("\n== box classes: centre within h (sup norm) of the segment's centre ==")
for name, (cx, cy) in seg_centres.items():
    for h in (Fraction(1, 20), Fraction(1, 10), Fraction(1, 5), Fraction(3, 10), Fraction(1, 2)):
        f = [abs(x - cx) <= h and abs(y - cy) <= h for x, y in centres]
        report(f"centre within {h} of {name}'s centre, any core", f, f)
        report(f"centre within {h} of {name}'s centre, P10-avoiding core", [a and g for a, g in zip(avoid, f, strict=True)],
               [a and g for a, g in zip(avoid, f, strict=True)])
print("\n== lane C's S4 wall rectangle [1, q/2] x [0, h] ==")
mask_pts = [(Fraction(1), Fraction(1)), (q - 1, Fraction(1)), (q / 2, Fraction(1))]
for h in (Fraction(1), Fraction(11, 10), Fraction(6, 5)):
    f = [1 <= x <= q / 2 and 0 <= y <= h for x, y in centres]
    report(f"centre in [1, q/2] x [0, {h}], any core", f, f)
    g = [ff and all(not covers(s, p) for p in mask_pts) for ff, (s, _, _) in zip(f, family, strict=True)]
    report(f"centre in [1, q/2] x [0, {h}], avoiding the three bottom-row P10 points", g, g)


print("\n== D4 union per type: within h of ANY of the eight D4 images of the segment (symmetric per-type measure) ==")


def images_of_segment(cx, cy):
    """The D4 images of the horizontal segment centred at (cx, cy), as endpoint pairs."""
    a = (cx - Fraction(1, 20), cy)
    b = (cx + Fraction(1, 20), cy)
    out = set()
    for (x1, y1), (x2, y2) in [(a, b)]:
        for sx in (1, -1):
            for sy in (1, -1):
                for swap in (False, True):
                    p1 = (x1 if sx == 1 else q - x1, y1 if sy == 1 else q - y1)
                    p2 = (x2 if sx == 1 else q - x2, y2 if sy == 1 else q - y2)
                    if swap:
                        p1, p2 = (p1[1], p1[0]), (p2[1], p2[0])
                    out.add(tuple(sorted((p1, p2))))
    return sorted(out)


def dist_general_segment_bounds(square, p1, p2):
    ds = [dist_point_square_f(square, float(p1[0]) + t * float(p2[0] - p1[0]), float(p1[1]) + t * float(p2[1] - p1[1]))
          for t in np.linspace(0.0, 1.0, 401)]
    m = min(ds)
    return m - HALF_STEP - 1e-9, m + 1e-9


for name, (cx, cy) in seg_centres.items():
    segs = images_of_segment(cx, cy)
    print("  type", name, "has", len(segs), "D4 images")
    for h in (Fraction(1, 100), Fraction(1, 20)):
        lo_f = []
        hi_f = []
        for s, _, _ in family:
            bounds = [dist_general_segment_bounds(s, p1, p2) for p1, p2 in segs]
            lo_f.append(min(b[1] for b in bounds) <= float(h))
            hi_f.append(min(b[0] for b in bounds) <= float(h))
        report(f"within {h} of a D4 image of segment {name}, any core", lo_f, hi_f)
        report(f"within {h} of a D4 image of segment {name}, P10-avoiding core",
               [a and f for a, f in zip(avoid, lo_f, strict=True)], [a and f for a, f in zip(avoid, hi_f, strict=True)])

print("\n== K4 union per type: within h of any of the K4 images (the symmetry group of P10) of the segment ==")


def k4_images_of_segment(cx, cy):
    out = set()
    for gx in {cx, q - cx}:
        for gy in {cy, q - cy}:
            out.add(((gx - Fraction(1, 20), gy), (gx + Fraction(1, 20), gy)))
    return sorted(out)


for name, (cx, cy) in seg_centres.items():
    segs = k4_images_of_segment(cx, cy)
    print("  type", name, "has", len(segs), "K4 images")
    for h in (Fraction(1, 100), Fraction(1, 20)):
        lo_f = []
        hi_f = []
        for s, _, _ in family:
            bounds = [dist_general_segment_bounds(s, p1, p2) for p1, p2 in segs]
            lo_f.append(min(b[1] for b in bounds) <= float(h))
            hi_f.append(min(b[0] for b in bounds) <= float(h))
        report(f"within {h} of a K4 image of segment {name}, any core", lo_f, hi_f)
        report(f"within {h} of a K4 image of segment {name}, P10-avoiding core",
               [a and f for a, f in zip(avoid, lo_f, strict=True)], [a and f for a, f in zip(avoid, hi_f, strict=True)])

print("\n== directions of the grazing squares per class at h = 1/100 (net index; angle in degrees) ==")
for name in "CWOI":
    idx = [i for i in range(len(family)) if avoid[i] and seg_d[name][i][1] <= 0.01]
    angles = sorted({(family[i][2], round(math.degrees(2 * math.atan(float(half_tangents[family[i][2]]))), 2)) for i in idx})
    print(f"  {name}: {len(idx)} squares, directions {angles}")
idx = [i for i in range(len(family)) if avoid[i]]
angles = sorted({(family[i][2], round(math.degrees(2 * math.atan(float(half_tangents[family[i][2]]))), 2)) for i in idx})
print(f"  all grazing: {len(idx)} squares, directions {angles}")
print("  all binding placements (45 rows), directions:", sorted({(d, round(math.degrees(2 * math.atan(float(half_tangents[d]))), 2)) for _, _, d in placements}))

json.dump({"V": str(V), "max_depth": str(max_depth), "rows": rows_out}, open(path.replace(".json", "-charges.json"), "w"), indent=1)
print("done")
```

### `band.py` (the band search with an exact witness; `0.25` interior, `0.05 walls` for the wall rectangles)

```text
"""Lane BC-299: the least folded tilt of a contained closed unit square that avoids all ten
Figure-13 points at 96/25 with its centre outside both wall rectangles [1, q-1] x [0, 1]
and [1, q-1] x [q-1, q].  Float grid search, then refinement, then an exact rational
decision of the pose found (containment and strict avoidance of every closed-square point).
A found pose is a theorem about the band; a grid without a find is only a reading.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction

import numpy as np

q = Fraction(96, 25)
qf = float(q)
P10 = []
for x, y in [(Fraction(1), Fraction(1)), (q / 2, Fraction(1)), (Fraction(3, 2) - q / 4, q / 2), (Fraction(1, 2) + q / 4, q / 2)]:
    for xx in {x, q - x}:
        for yy in {y, q - y}:
            P10.append((xx, yy))
P10 = sorted(set(P10))
P = np.array([[float(x), float(y)] for x, y in P10])


def margins(psi, cx, cy):
    """For each point, max(|u| - 1/2, |v| - 1/2) in the square's frame: > 0 means outside."""
    c, s = math.cos(psi), math.sin(psi)
    dx, dy = P[:, 0] - cx, P[:, 1] - cy
    u = c * dx + s * dy
    v = -s * dx + c * dy
    return np.maximum(np.abs(u) - 0.5, np.abs(v) - 0.5)


def contained(psi, cx, cy):
    w = (abs(math.cos(psi)) + abs(math.sin(psi))) / 2
    return w <= cx <= qf - w and w <= cy <= qf - w


INSIDE = len(sys.argv) > 2 and sys.argv[2] == "walls"


def outside_walls(cx, cy):
    inside = 1 <= cx <= qf - 1 and (cy <= 1 or cy >= qf - 1)
    return inside if INSIDE else not inside


best = None
step_deg = float(sys.argv[1]) if len(sys.argv) > 1 else 0.25
grid = 0.01
for deg in np.arange(0.0, 45.0 + 1e-9, step_deg):
    psi = math.radians(deg)
    w = (math.cos(psi) + math.sin(psi)) / 2
    found = None
    for cx in np.arange(w, qf / 2 + 1e-9, grid):
        for cy in np.arange(w, qf / 2 + 1e-9, grid):
            if not outside_walls(cx, cy):
                continue
            m = margins(psi, cx, cy).min()
            if m > 0 and (found is None or m > found[0]):
                found = (m, cx, cy)
    if found is not None:
        print(f"tilt {deg:.2f} deg: avoider centre ({found[1]:.3f}, {found[2]:.3f}) margin {found[0]:.5f}", flush=True)
        best = (deg, found)
        break
if best is None:
    print("no avoider outside the wall rectangles up to 45 degrees at this resolution")
    sys.exit(0)

# refine: local search over (psi, cx, cy) minimising the tilt subject to margin > 0
deg0, (m0, cx0, cy0) = best
lo, hi = max(0.0, deg0 - step_deg), deg0
for _ in range(40):
    mid = (lo + hi) / 2
    psi = math.radians(mid)
    w = (math.cos(psi) + math.sin(psi)) / 2
    ok = None
    for cx in np.arange(cx0 - 0.15, cx0 + 0.15, 0.0025):
        for cy in np.arange(cy0 - 0.15, cy0 + 0.15, 0.0025):
            if not outside_walls(cx, cy) or not contained(psi, cx, cy):
                continue
            m = margins(psi, cx, cy).min()
            if m > 0 and (ok is None or m > ok[0]):
                ok = (m, cx, cy)
    if ok is not None:
        hi = mid
        cx0, cy0 = ok[1], ok[2]
        best = (mid, ok)
    else:
        lo = mid
deg, (m, cx, cy) = best
print(f"refined: tilt {deg:.4f} deg, centre ({cx:.4f}, {cy:.4f}), margin {m:.5f}")

# exact decision: add a little tilt slack, re-optimise the centre for margin, rationalise, decide
def exact_try(deg_try, cx0, cy0):
    psi = math.radians(deg_try)
    okk = None
    for cx in np.arange(cx0 - 0.1, cx0 + 0.1, 0.002):
        for cy in np.arange(cy0 - 0.1, cy0 + 0.1, 0.002):
            if not outside_walls(cx, cy) or not contained(psi, cx, cy):
                continue
            m = margins(psi, cx, cy).min()
            if m > 0 and (okk is None or m > okk[0]):
                okk = (m, cx, cy)
    if okk is None:
        return None
    t = Fraction(math.tan(psi / 2)).limit_denominator(2000)
    cxr = Fraction(okk[1]).limit_denominator(1000)
    cyr = Fraction(okk[2]).limit_denominator(1000)
    den = 1 + t * t
    cos_, sin_ = (1 - t * t) / den, 2 * t / den
    half = Fraction(1, 2)
    w = (cos_ + sin_) / 2
    if not (w <= cxr <= q - w and w <= cyr <= q - w):
        return None
    inside = 1 <= cxr <= q - 1 and (cyr <= 1 or cyr >= q - 1)
    if inside != INSIDE:
        return None
    worst = None
    for x, y in P10:
        dx, dy = x - cxr, y - cyr
        u = cos_ * dx + sin_ * dy
        v = -sin_ * dx + cos_ * dy
        mm = max(abs(u) - half, abs(v) - half)
        worst = mm if worst is None else min(worst, mm)
    if worst <= 0:
        return None
    return t, cxr, cyr, worst, okk[0]


for slack in (0.02, 0.05, 0.1, 0.2, 0.3, 0.5):
    got = exact_try(deg + slack, cx, cy)
    if got is not None:
        t, cxr, cyr, worst, fm = got
        angle = math.degrees(2 * math.atan(float(t)))
        print(f"EXACT avoider ({'inside' if INSIDE else 'outside'} the wall rectangles): tan(psi/2) = {t}, tilt {angle:.4f} deg, "
              f"centre ({cxr}, {cyr}), least frame margin {worst} = {float(worst):.6f} (float search margin {fm:.5f})")
        break
else:
    print("no exact witness found with the slack menu")
```

### `run1.log`

```text
grids (25, 34, 42) orbits 619 sites 4645
stopped: converged: every placement covers mass 1 objective 11.386020301400558 rounds 21 rows 4775 least_covered 0.9999999999999554 wall 65.2 load (0.3544921875, 0.4013671875, 0.580078125) (1.52685546875, 0.74609375, 0.68994140625)
rationalised mass 45544287/4000000 11.38607175 atoms 329
wrote /tmp/claude-0/-home-user-squares/9010767e-5bb7-5e7d-99d2-858400f3969a/scratchpad/lane-299/run1-free-dual.json
verify wall 11.7 load (1.4453125, 0.7548828125, 0.69384765625)
Verdict(conditions=(ConditionReport(name='Condition 1 atoms carry the declared symmetry', detail='329 atoms closed under D4 about the centre', holds=True), ConditionReport(name='Condition 2 total mass below n', detail='total 45544287/4000000 against n = 11', holds=False), ConditionReport(name='Condition 3 net reaches pi/4', detail='final half-tangent 207107/500000, t^2 + 2t - 1 = 309449/250000000000', holds=True), ConditionReport(name='Condition 4 containment B(1 + D) < 1', detail='B = 9977/10000, D = 207107/90000000, B(1 + D) = 899996306539/900000000000', holds=True), ConditionReport(name='Condition 5 every reachable cell carries mass 1', detail='least cell mass 400001/400000 at direction 0', holds=True)), total_mass=Fraction(45544287, 4000000), minimum_cell_mass=Fraction(400001, 400000), worst_direction='0')
```

### `charges1.log`

```text
sites 4645
rows with positive dual 45 raw dual total 11.38602030140046
symmetrised squares 360 V = 45544013/4000000 11.38600325
float depth max 0.9999989375 at site (Fraction(1536, 3175), Fraction(3136, 3175))
exact depth max 15999983/16000000 0.9999989375 sites with depth >= 0.999: 893 wall 0.8
site (Fraction(3152, 3175), Fraction(2336, 3175)) index [1322] depth ['15999983/16000000']
site (Fraction(2336, 3175), Fraction(3152, 3175)) index [1320] depth ['15999983/16000000']
site (Fraction(29586032, 29422725), Fraction(29586032, 29422725)) index [3076] depth ['7124827/8000000']
charge of P10-avoiders (all directions, exact): 3.608128875

== anchor classes in the bottom-left frame (charges under the D4-symmetrised dual) ==
corner pair: core contains m1 or m2                        charge in [1.002367, 1.002367]  squares 6/6  dead for every w
scaled T-018 corner atom in the core                       charge in [0.890603, 0.890603]  squares 34/34  alive only with w > 4.5285
within 1/100 of segment C, any core                        charge in [2.335340, 2.335340]  squares 43/43  dead for every w
within 1/100 of segment C, P10-avoiding core               charge in [0.840596, 0.840596]  squares 5/5  alive only with w > 3.4215
within 1/50 of segment C, any core                         charge in [2.335340, 2.335340]  squares 43/43  dead for every w
within 1/50 of segment C, P10-avoiding core                charge in [0.840596, 0.840596]  squares 5/5  alive only with w > 3.4215
within 1/20 of segment C, any core                         charge in [2.441135, 2.441135]  squares 48/48  dead for every w
within 1/20 of segment C, P10-avoiding core                charge in [0.844111, 0.844111]  squares 6/6  alive only with w > 3.4761
within 1/10 of segment C, any core                         charge in [2.518008, 2.518008]  squares 54/54  dead for every w
within 1/10 of segment C, P10-avoiding core                charge in [0.846479, 0.846479]  squares 7/7  alive only with w > 3.5143
within 1/5 of segment C, any core                          charge in [2.542421, 2.542421]  squares 56/56  dead for every w
within 1/5 of segment C, P10-avoiding core                 charge in [0.858685, 0.858685]  squares 8/8  alive only with w > 3.7315
within 1/100 of segment W, any core                        charge in [1.844134, 1.844134]  squares 84/84  dead for every w
within 1/100 of segment W, P10-avoiding core               charge in [0.821522, 0.821522]  squares 18/18  alive only with w > 3.1627
within 1/50 of segment W, any core                         charge in [1.916185, 1.916185]  squares 88/88  dead for every w
within 1/50 of segment W, P10-avoiding core                charge in [0.826258, 0.826258]  squares 20/20  alive only with w > 3.2217
within 1/20 of segment W, any core                         charge in [1.968975, 1.968975]  squares 90/90  dead for every w
within 1/20 of segment W, P10-avoiding core                charge in [0.826258, 0.826258]  squares 20/20  alive only with w > 3.2217
within 1/10 of segment W, any core                         charge in [1.997849, 1.997849]  squares 94/94  dead for every w
within 1/10 of segment W, P10-avoiding core                charge in [0.826258, 0.826258]  squares 20/20  alive only with w > 3.2217
within 1/5 of segment W, any core                          charge in [2.134337, 2.134337]  squares 110/110  dead for every w
within 1/5 of segment W, P10-avoiding core                 charge in [0.826258, 0.826258]  squares 20/20  alive only with w > 3.2217
within 1/100 of segment O, any core                        charge in [0.999999, 0.999999]  squares 20/20  alive only with w > 294098.7143
within 1/100 of segment O, P10-avoiding core               charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
within 1/50 of segment O, any core                         charge in [0.999999, 0.999999]  squares 20/20  alive only with w > 294098.7143
within 1/50 of segment O, P10-avoiding core                charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
within 1/20 of segment O, any core                         charge in [0.999999, 0.999999]  squares 20/20  alive only with w > 294098.7143
within 1/20 of segment O, P10-avoiding core                charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
within 1/10 of segment O, any core                         charge in [0.999999, 0.999999]  squares 20/20  alive only with w > 294098.7143
within 1/10 of segment O, P10-avoiding core                charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
within 1/5 of segment O, any core                          charge in [0.999999, 0.999999]  squares 20/20  alive only with w > 294098.7143
within 1/5 of segment O, P10-avoiding core                 charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
within 1/100 of segment I, any core                        charge in [1.483797, 1.483797]  squares 126/126  dead for every w
within 1/100 of segment I, P10-avoiding core               charge in [0.142054, 0.142054]  squares 16/16  alive only with w > 1.4499
within 1/50 of segment I, any core                         charge in [1.643193, 1.643193]  squares 130/130  dead for every w
within 1/50 of segment I, P10-avoiding core                charge in [0.142054, 0.142054]  squares 16/16  alive only with w > 1.4499
within 1/20 of segment I, any core                         charge in [1.815750, 1.815750]  squares 148/148  dead for every w
within 1/20 of segment I, P10-avoiding core                charge in [0.209566, 0.209566]  squares 22/22  alive only with w > 1.4883
within 1/10 of segment I, any core                         charge in [1.818118, 1.818118]  squares 150/150  dead for every w
within 1/10 of segment I, P10-avoiding core                charge in [0.209566, 0.209566]  squares 22/22  alive only with w > 1.4883
within 1/5 of segment I, any core                          charge in [1.978583, 1.978583]  squares 166/166  dead for every w
within 1/5 of segment I, P10-avoiding core                 charge in [0.209566, 0.209566]  squares 22/22  alive only with w > 1.4883

== union over the four types (E of Lemma B, the whole grazing class) ==
within 1/100 of some segment, any core                     charge in [11.386003, 11.386003]  squares 360/360  dead for every w
within 1/100 of some segment, P10-avoiding core            charge in [3.608129, 3.608129]  squares 48/48  dead for every w
   P10-avoiders NOT within 1/100 of any segment (upper flag false): 0
within 1/50 of some segment, any core                      charge in [11.386003, 11.386003]  squares 360/360  dead for every w
within 1/50 of some segment, P10-avoiding core             charge in [3.608129, 3.608129]  squares 48/48  dead for every w
   P10-avoiders NOT within 1/50 of any segment (upper flag false): 0
within 1/20 of some segment, any core                      charge in [11.386003, 11.386003]  squares 360/360  dead for every w
within 1/20 of some segment, P10-avoiding core             charge in [3.608129, 3.608129]  squares 48/48  dead for every w
   P10-avoiders NOT within 1/20 of any segment (upper flag false): 0

== box classes: centre within h (sup norm) of the segment's centre ==
centre within 1/20 of C's centre, any core                 charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/20 of C's centre, P10-avoiding core        charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/10 of C's centre, any core                 charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/10 of C's centre, P10-avoiding core        charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/5 of C's centre, any core                  charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/5 of C's centre, P10-avoiding core         charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 3/10 of C's centre, any core                 charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 3/10 of C's centre, P10-avoiding core        charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/2 of C's centre, any core                  charge in [1.435235, 1.435235]  squares 42/42  dead for every w
centre within 1/2 of C's centre, P10-avoiding core         charge in [0.150851, 0.150851]  squares 3/3  alive only with w > 1.4546
centre within 1/20 of W's centre, any core                 charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/20 of W's centre, P10-avoiding core        charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/10 of W's centre, any core                 charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/10 of W's centre, P10-avoiding core        charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/5 of W's centre, any core                  charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/5 of W's centre, P10-avoiding core         charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 3/10 of W's centre, any core                 charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 3/10 of W's centre, P10-avoiding core        charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/2 of W's centre, any core                  charge in [0.864217, 0.864217]  squares 52/52  alive only with w > 3.8428
centre within 1/2 of W's centre, P10-avoiding core         charge in [0.330852, 0.330852]  squares 10/10  alive only with w > 1.5769
centre within 1/20 of O's centre, any core                 charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/20 of O's centre, P10-avoiding core        charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/10 of O's centre, any core                 charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/10 of O's centre, P10-avoiding core        charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/5 of O's centre, any core                  charge in [0.126902, 0.126902]  squares 10/10  alive only with w > 1.4421
centre within 1/5 of O's centre, P10-avoiding core         charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 3/10 of O's centre, any core                 charge in [0.126902, 0.126902]  squares 10/10  alive only with w > 1.4421
centre within 3/10 of O's centre, P10-avoiding core        charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/2 of O's centre, any core                  charge in [0.999999, 0.999999]  squares 20/20  alive only with w > 294098.7143
centre within 1/2 of O's centre, P10-avoiding core         charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/20 of I's centre, any core                 charge in [0.004809, 0.004809]  squares 4/4  alive only with w > 1.3879
centre within 1/20 of I's centre, P10-avoiding core        charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/10 of I's centre, any core                 charge in [0.096147, 0.096147]  squares 14/14  alive only with w > 1.4271
centre within 1/10 of I's centre, P10-avoiding core        charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/5 of I's centre, any core                  charge in [0.117779, 0.117779]  squares 18/18  alive only with w > 1.4375
centre within 1/5 of I's centre, P10-avoiding core         charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 3/10 of I's centre, any core                 charge in [0.177178, 0.177178]  squares 24/24  alive only with w > 1.4691
centre within 3/10 of I's centre, P10-avoiding core        charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
centre within 1/2 of I's centre, any core                  charge in [0.870966, 0.870966]  squares 96/96  alive only with w > 3.9915
centre within 1/2 of I's centre, P10-avoiding core         charge in [0.178123, 0.178123]  squares 18/18  alive only with w > 1.4697

== lane C's S4 wall rectangle [1, q/2] x [0, h] ==
centre in [1, q/2] x [0, 1], any core                      charge in [0.499999, 0.499999]  squares 10/10  alive only with w > 1.7720
centre in [1, q/2] x [0, 1], avoiding the three bottom-row P10 points charge in [0.351692, 0.351692]  squares 3/3  alive only with w > 1.5954
centre in [1, q/2] x [0, 11/10], any core                  charge in [0.499999, 0.499999]  squares 10/10  alive only with w > 1.7720
centre in [1, q/2] x [0, 11/10], avoiding the three bottom-row P10 points charge in [0.351692, 0.351692]  squares 3/3  alive only with w > 1.5954
centre in [1, q/2] x [0, 6/5], any core                    charge in [0.499999, 0.499999]  squares 10/10  alive only with w > 1.7720
centre in [1, q/2] x [0, 6/5], avoiding the three bottom-row P10 points charge in [0.351692, 0.351692]  squares 3/3  alive only with w > 1.5954

== D4 union per type: within h of ANY of the eight D4 images of the segment (symmetric per-type measure) ==
  type C has 8 D4 images
within 1/100 of a D4 image of segment C, any core          charge in [9.475988, 9.475988]  squares 176/176  dead for every w
within 1/100 of a D4 image of segment C, P10-avoiding core charge in [3.362383, 3.362383]  squares 20/20  dead for every w
within 1/20 of a D4 image of segment C, any core           charge in [10.053090, 10.053090]  squares 208/208  dead for every w
within 1/20 of a D4 image of segment C, P10-avoiding core  charge in [3.376444, 3.376444]  squares 24/24  dead for every w
  type W has 4 D4 images
within 1/100 of a D4 image of segment W, any core          charge in [7.376536, 7.376536]  squares 336/336  dead for every w
within 1/100 of a D4 image of segment W, P10-avoiding core charge in [1.643044, 1.643044]  squares 36/36  dead for every w
within 1/20 of a D4 image of segment W, any core           charge in [7.395479, 7.395479]  squares 344/344  dead for every w
within 1/20 of a D4 image of segment W, P10-avoiding core  charge in [1.652515, 1.652515]  squares 40/40  dead for every w
  type O has 4 D4 images
within 1/100 of a D4 image of segment O, any core          charge in [3.999995, 3.999995]  squares 80/80  dead for every w
within 1/100 of a D4 image of segment O, P10-avoiding core charge in [1.406770, 1.406770]  squares 12/12  dead for every w
within 1/20 of a D4 image of segment O, any core           charge in [3.999995, 3.999995]  squares 80/80  dead for every w
within 1/20 of a D4 image of segment O, P10-avoiding core  charge in [1.406770, 1.406770]  squares 12/12  dead for every w
  type I has 4 D4 images
within 1/100 of a D4 image of segment I, any core          charge in [3.395484, 3.395484]  squares 264/264  dead for every w
within 1/100 of a D4 image of segment I, P10-avoiding core charge in [0.245745, 0.245745]  squares 28/28  alive only with w > 1.5118
within 1/20 of a D4 image of segment I, any core           charge in [3.395484, 3.395484]  squares 264/264  dead for every w
within 1/20 of a D4 image of segment I, P10-avoiding core  charge in [0.245745, 0.245745]  squares 28/28  alive only with w > 1.5118

== K4 union per type: within h of any of the K4 images (the symmetry group of P10) of the segment ==
  type C has 4 K4 images
within 1/100 of a K4 image of segment C, any core          charge in [9.341359, 9.341359]  squares 172/172  dead for every w
within 1/100 of a K4 image of segment C, P10-avoiding core charge in [3.362383, 3.362383]  squares 20/20  dead for every w
within 1/20 of a K4 image of segment C, any core           charge in [9.764539, 9.764539]  squares 192/192  dead for every w
within 1/20 of a K4 image of segment C, P10-avoiding core  charge in [3.376444, 3.376444]  squares 24/24  dead for every w
  type W has 2 K4 images
within 1/100 of a K4 image of segment W, any core          charge in [3.688268, 3.688268]  squares 168/168  dead for every w
within 1/100 of a K4 image of segment W, P10-avoiding core charge in [1.643044, 1.643044]  squares 36/36  dead for every w
within 1/20 of a K4 image of segment W, any core           charge in [3.937951, 3.937951]  squares 180/180  dead for every w
within 1/20 of a K4 image of segment W, P10-avoiding core  charge in [1.652515, 1.652515]  squares 40/40  dead for every w
  type O has 2 K4 images
within 1/100 of a K4 image of segment O, any core          charge in [1.999997, 1.999997]  squares 40/40  dead for every w
within 1/100 of a K4 image of segment O, P10-avoiding core charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
within 1/20 of a K4 image of segment O, any core           charge in [1.999997, 1.999997]  squares 40/40  dead for every w
within 1/20 of a K4 image of segment O, P10-avoiding core  charge in [0.000000, 0.000000]  squares 0/0  alive only with w > 1.3860
  type I has 2 K4 images
within 1/100 of a K4 image of segment I, any core          charge in [2.861867, 2.861867]  squares 228/228  dead for every w
within 1/100 of a K4 image of segment I, P10-avoiding core charge in [0.245745, 0.245745]  squares 28/28  alive only with w > 1.5118
within 1/20 of a K4 image of segment I, any core           charge in [3.390748, 3.390748]  squares 260/260  dead for every w
within 1/20 of a K4 image of segment I, P10-avoiding core  charge in [0.245745, 0.245745]  squares 28/28  alive only with w > 1.5118

== directions of the grazing squares per class at h = 1/100 (net index; angle in degrees) ==
  C: 5 squares, directions [(0, 0.0), (2, 0.53), (180, 45.0)]
  W: 18 squares, directions [(0, 0.0), (2, 0.53), (51, 13.39), (61, 15.98), (70, 18.3), (76, 19.84), (86, 22.39), (88, 22.9)]
  O: 0 squares, directions []
  I: 16 squares, directions [(51, 13.39), (61, 15.98), (70, 18.3), (76, 19.84), (86, 22.39), (88, 22.9)]
  all grazing: 48 squares, directions [(0, 0.0), (2, 0.53), (51, 13.39), (61, 15.98), (70, 18.3), (76, 19.84), (86, 22.39), (88, 22.9), (180, 45.0)]
  all binding placements (45 rows), directions: [(0, 0.0), (2, 0.53), (5, 1.32), (7, 1.85), (10, 2.64), (21, 5.53), (39, 10.26), (51, 13.39), (58, 15.2), (61, 15.98), (70, 18.3), (76, 19.84), (86, 22.39), (88, 22.9), (91, 23.65), (99, 25.67), (100, 25.92), (102, 26.42), (105, 27.17), (108, 27.91), (112, 28.9), (114, 29.4), (115, 29.65), (119, 30.63), (125, 32.1), (130, 33.31), (133, 34.03), (138, 35.24), (143, 36.43), (146, 37.14), (161, 40.66), (164, 41.35), (167, 42.04), (170, 42.73), (176, 44.1), (177, 44.32), (180, 45.0)]
done
```

### `band-outside.log` (`band.py 0.25`)

```text
tilt 13.25 deg: avoider centre (1.441, 1.401) margin 0.00033
refined: tilt 13.0277 deg, centre (1.4363, 1.4013), margin 0.00000
EXACT avoider (outside the wall rectangles): tan(psi/2) = 137/1198, tilt 13.0477 deg, centre (53/35, 1398/985), least frame margin 3930001/100251438350 = 0.000039 (float search margin 0.00004)
```

### `band-walls.log` (`band.py 0.05 walls`)

```text
tilt 11.70 deg: avoider centre (1.491, 0.591) margin 0.00007
refined: tilt 11.6500 deg, centre (1.4935, 0.5910), margin 0.00022
EXACT avoider (inside the wall rectangles): tan(psi/2) = 191/1869, tilt 11.6700 deg, centre (115/77, 565/956), least frame margin 3390269/9279428818 = 0.000365 (float search margin 0.00036)
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
