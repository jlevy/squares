# Agenda 030, lane B: Orientation-class constraints

Retained planning-lane report for
[X-021](../../../../explorations/X-021-what-can-be-proved-about-eleven-squares.md),
written by a Fable sub-agent at maximum effort on 2026-09-08 under BC-291 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md).
The report is reproduced as delivered, with its own status labels; X-021 carries the
coordinator’s reading of it.
Nothing here is a registered round or a new bound.

## B — Orientation-class ("angle count") constraints for eleven unit squares in [0, L]², L ∈ [3.81, 3.8771]

Date 2026-09-08. Repository read-only; all scripts and logs live in the scratchpad
(`/tmp/claude-0/-home-user-squares/9010767e-5bb7-5e7d-99d2-858400f3969a/scratchpad/`,
written `$S` below).
The project venv at `packing/.venv` was not built (the pinned CPython 3.14.7 is not
downloadable here); a working venv with the same lockfile on CPython 3.14.0rc2 was built
at `$S/venv314` and every repository computation below ran through it
(`sqpack.fractional.classcert` imports and the `nine-point` control of
`devtools.run_class_program` reproduce exp-064’s exact numbers, 0.5 s wall).

Conventions. Orientations are taken modulo π/2 and folded to φ ∈ [0°, 45°]. A packing is
a set of closed unit squares in [0, L]² with pairwise disjoint interiors.
`B = 9977/10000` is the retained shrink, the net is the retained 181-direction net
(`certificate.json`: half-tangent limit 207107/500000, 180 steps, cell width ≈ 0.264° at
the axis end, index 159 ≈ 40.194°, index 180 = 45.000°). A *B-core* of a square is the
concentric closed square of side B at a net direction whose half-gap cell contains the
square’s angle; by Condition 4 it lies in the square’s interior, so the eleven cores of
a packing are pairwise disjoint.
Class certificates are X-014 Lemma 3 as implemented in `sqpack.fractional.classcert`.
Everything decided “exactly” below was decided by `decide_class_program` on rationalised
atoms (fractions, no tolerance); everything else is a float search and is labelled as
such. `q = 96/25 = 3.84`, `U = 3.877083590…` (rational cover `3877084/10⁶` used wherever
a theorem “at side U” is stated).

Status labels used throughout: **PROVED** (full proof here), **EXACT-VERIFIED**
(computer decision in exact rational arithmetic with the repository’s own verifier; a
theorem, but not a hand proof), **NUMERICAL** (float search, or a search that merely
found or failed to find something), **CONJECTURED**, **OPEN**.

## 1. Results proved

### 1.1 The nine-point theorem, sharpened statement and exact constants (PROVED)

**Theorem 1.1.** Let 3 < L < 4 and let θ₀(L) ∈ (0°, 45°) be defined by cos θ₀ + sin θ₀ =
4/L. In every packing of unit squares in [0, L]², at most nine squares have folded tilt
φ < θ₀(L). Hence a packing of eleven squares has at least two squares with φ ≥ θ₀(L).

*Proof.* A unit square at folded tilt φ contains the concentric axis-parallel square of
side a(φ) = 1/(cos φ + sin φ): a corner of that square, at (±a/2, ±a/2), has coordinates
(a/2)(cos φ ± sin φ) in the tilted frame, both of absolute value ≤ (a/2)(cos φ + sin φ)
= 1/2. If φ < θ₀ then a(φ) > L/4, so the open x-projection (x₁, x₂) of the core has
length > L/4 and lies in [0, L]; it therefore contains a multiple kL/4 of L/4, and k ∉
{0, 4} since 0 and L are not interior points.
The same holds in y. So the open core, hence the open unit square, contains one of the
nine points (iL/4, jL/4), i, j ∈ {1, 2, 3}. Two squares with disjoint interiors cannot
both contain the same point in their interiors, so at most nine squares have φ < θ₀. ∎

The strictness matters: at φ = θ₀ exactly the point may sit on the boundary of the core
and two squares may share it (four axis-parallel squares meeting at a grid point is the
model), so the theorem is “< θ₀”, and “at least two squares have tilt ≥ θ₀”.

**Exact constants.** Writing r = 4/L and t = tan θ₀, the defining equation is (1 + t)² =
r²(1 + t²), i.e. (r² − 1)t² − 2t + (r² − 1) = 0, so t = (1 − √(1 − (r² − 1)²))/(r² − 1).

| L | 4/L | tan θ₀ | θ₀ |
| --- | --- | --- | --- |
| q = 96/25 | 25/24 | (576 − 25√527)/49 = 0.0426120 | 2.44001° |
| 3877084/10⁶ (≥ U) | 0.9693 | 0.0322392 | 1.84653° |
| 3.82 | 1.04712 | 0.0483433 | 2.76771° |
| 3.81 | 1.04987 | 0.0512464 | 2.93364° |

X-019’s band |tan θ| ≤ 1/24 (2.3859°) at q is correct: the inscribed side is √(577)/25 =
0.96083 > 0.96 = q/4 (exactly, 577/625 > 576/625); 1/23 already fails (inscribed side² =
530/576 < (24/25)²). Script: `$S/anglemath.py` (output in §2.1).

**Proposition 1.2 (the L/4 grid is exactly sharp).** For every φ ≥ θ₀(L) there is a unit
square of tilt φ inside [0, L]² whose open interior contains none of the nine grid
points.

*Proof.* Centre the square at (3L/8, 3L/8), the centre of the grid cell with corners
(L/4, L/4), (L/2, L/4), (L/4, L/2), (L/2, L/2). Relative to the centre those four points
are (±L/8, ±L/8); their coordinates in the tilted frame are (L/8)(cos φ ± sin φ), whose
maximum is (L/8)(cos φ + sin φ) ≥ (L/8)(4/L) = 1/2 — on or outside the open square.
The other five grid points are at relative position (±3L/8, ±L/8) or (±L/8, ±3L/8) or
(3L/8, 3L/8), whose tilted coordinate of larger absolute value is at least (L/8)(3 cos φ
− sin φ) ≥ (L/8)(3 cos 45° − sin 45°) = L√2/8 > 1/2 for L > 2√2. The square is contained
in the container since 3L/8 ± (cos φ + sin φ)/2 ∈ [3L/8 − 0.7072, 3L/8 + 0.7072] ⊂
[0, L] for L ≥ 3.8. ∎

So no sharper band can come from the pitch-L/4 grid.
Sharper bands need a different point set, and the next two results say how much room
there is.

**Lemma 1.3 (box lemma).** Let 3 < L < 4 and let P be a set of nine points such that
every closed axis-parallel unit square in [0, L]² contains a point of P in its interior.
Put I₁ = (L − 3, 1), I₂ = (L − 2, 2), I₃ = (L − 1, 3). Then P has exactly one point in
each of the nine open boxes I_i × I_j.

*Proof.* Fix y₀ ∈ [0, L − 3] and gaps g₁, g₂ ≥ 0 with y₀ + 3 + g₁ + g₂ ≤ L. The three
horizontal strips [0, L] × [y₀, y₀ + 1], [0, L] × [y₀ + 1 + g₁, y₀ + 2 + g₁], [0, L] ×
[y₀ + 2 + g₁ + g₂, y₀ + 3 + g₁ + g₂] have disjoint interiors and each contains three
unit squares with pairwise disjoint interiors, each of which contains its own point of P
in its interior; so each open strip holds at least three points, hence exactly three,
and no point of P lies outside the three open strips.
Intersecting over all admissible (y₀, g₁, g₂): a y-value in [0, L − 3] is excluded by y₀
= L − 3; y ∈ [1, L − 2] by (y₀, g₁) = (0, L − 3); y ∈ [2, L − 1] by (0, 0, L − 3); y ∈
[3, L] by y₀ = 0; and every y in I₁ ∪ I₂ ∪ I₃ lies in the k-th open strip of every
configuration (its lower end is ≤ L − 4 + k < y and its upper end is ≥ k > y). The same
holds in x. The unit square [i − 1, i] × [j − 1, j] has open interior meeting only the
box I_i × I_j, so each box contains a point; nine boxes, nine points.
∎

At q the boxes have side 4 − L = 0.16: the corner points of any nine-point axis-piercing
set lie in (0.84, 1)² and its images, the middle point in (1.84, 2)². The pitch-L/4 grid
sits at 0.96, 1.92, 2.88 — near the *outer* ends of the boxes in the sense that matters
below.

**Proposition 1.4 (product sets: the band is at most 5.24° at q).** If P is a nine-point
axis-piercing set of product form {x₁, x₂, x₃} × {y₁, y₂, y₃}, then some unit square of
tilt φ avoids the interior of every point of P whenever a(φ) ≤ (x₃ − x₁)/2 or a(φ) ≤ (y₃
− y₁)/2; since x₃ − x₁ > (L − 1) − 1 = L − 2 by Lemma 1.3, every product nine-point set
fails for all φ with a(φ) ≤ (L − 2)/2, which at q is 0.92, i.e. φ ≥ 5.24°.

*Proof.* The wider of the two cells [x₁, x₂] × [y_j, y_{j+1}] and [x₂, x₃] × … in a row
has width w ≥ (x₃ − x₁)/2; the argument of Proposition 1.2 applied to a cell of width w
and the square centred in it gives an escape as soon as (w/2)(cos φ + sin φ) ≥ 1/2, i.e.
a(φ) ≤ w. ∎

**Theorem 1.5 (a wider nine-point band; EXACT-VERIFIED).** At side q = 96/25 the nine
points {1 − 1/200, q/2, q − 1 + 1/200}² pierce (i.e. contain in the closed core) every
admissible B-core at every direction of the leading 18 half-gap cells of the retained
net, whose union is the closed folded range [0°, 4.6122°]. Consequently every packing in
[0, q]² has at most nine squares with folded tilt ≤ 4.6122°, and every packing of eleven
has at least two squares with tilt > 4.6122°. At side 3877084/10⁶ ≥ U the same set with
q replaced by that side pierces the leading 13 cells, [0°, 3.2953°]. For comparison the
L/4 grid, decided the same way (B-cores), pierces 9 cells (2.2411°) at q and 7 cells
(1.7139°) at U.

*Proof of the counting step.* Each square of a packing contains its closed B-core, at
the net direction whose cell holds its angle (Condition 4, B(1 + D) < 1 holds for this
net); if the angle is in the closed range of the class, that direction is in the class;
the core then contains one of the nine atoms; the cores lie in the open squares so they
are pairwise disjoint; nine atoms, at most nine squares.
The piercing statement itself is the exact event-cell sweep `class_minima` (the same
sweep the retention gate uses) reporting least covered mass ≥ 1 on every class
direction; script `$S/nine_points.py`, output in §2.2. ∎

Remarks. (i) The pushed set is a *product* set with x₃ − x₁ = L − 2 + 0.01, so by
Proposition 1.4 its band cannot exceed a(φ) = 0.925, φ ≈ 4.8°; the exact 4.61° is the
B-core version. Sending 1/200 → 0 approaches the 5.24° limit of Proposition 1.4 but the
sweep’s B-cores need the atom strictly inside the core, so the tested values 1/200 and
1/100 are the practical optimum (1/100 gives 17 cells, 4.35°; 0 gives nothing, because
the atom at (1, 1) is on the boundary of the flush corner square’s core).
(ii) A hand proof of Theorem 1.5 is possible in principle (nine explicit points, a
one-parameter family of tilts, finitely many event cells) but was not written; the
theorem’s status is EXACT-VERIFIED. (iii) Non-product nine-point sets (staggered rows)
are not covered by Proposition 1.4, so the true optimum of the nine-point band at q lies
in [4.61°, ?] and is OPEN; the fractional class program of §2.3 gives mass 9.006 out to
6.45° at q, which means a *weighted* nine-point-like set (24 atoms of weights 1/4 and
1/2 clustered at the nine box positions) reaches 6.45°, so no integrality argument
bounds the integral optimum below 6.45°.

### 1.2 What “at least two tilted squares” gives, precisely (PROVED)

Let Θ₀ be any class of squares closed under the count bound of Theorem 1.1 or 1.5 (tilt
below θ₀(L), or tilt ≤ 4.6122° at q). Then in a packing of eleven at side ≤ L:

1. the compositions (n₀, n₁) = (11, 0) and (10, 1) are impossible — two eleventh-square
   counts, nothing else;
2. the two (or more) squares outside Θ₀ each contain a B-core at a direction outside Θ₀;
   Lemma 3 of X-014 applied with w₀ = w₁ = 1 is then the unconditional certificate, and
   applied with w₀ ≠ w₁ prices those two cores differently — this is the entire content
   that the count delivers to a certificate;
3. it says nothing about where the tilted squares are, whether they share an angle, or
   how far they tilt; Trump’s packing has five squares at 40.18°, so the bound “two” is
   not sharp and cannot be made sharp by any near-axis piercing set: the fixed-angle
   packing numbers of §2.4 show nine squares at any common tilt ≤ 30° fit in [0, q]², so
   no near-axis band can force more than two squares out.

The exact converse is also worth recording: the only way a near-axis count can be raised
from “at most nine” to “at most eight” is a band whose fractional covering value is < 9,
and the sweep of §2.3 finds no such band even one cell wide (mass exactly 9 for the axis
cell alone, which is the nine disjoint axis-parallel B-squares: the value is exact).

### 1.3 Theorem 3 of Stromquist transferred to a band at q (PROVED, modulo the source theorem)

**Proposition 1.6.** Let L ≤ q and let every square of a packing of eleven in [0, L]²
have folded angle within δ of 0° or within δ of 45°, where cos δ + sin δ ≤ L₀/q with L₀
= 2 + (4/3)√2 = 3.885618…; at q this allows δ = 0.6848°. Then no such packing exists at
side ≤ q. Equivalently: every packing of eleven at side ≤ 3.84 has a square whose folded
angle is farther than 0.6848° from both 0° and 45°.

*Proof.* Put b = q/L₀ = 0.98826. A unit square at folded angle within δ of 0° contains
the concentric axis-parallel square of side b when b(cos δ + sin δ) ≤ 1; one within δ of
45° contains the concentric 45°-square of side b under the same condition.
The eleven cores are pairwise disjoint closed squares of side b at orientations exactly
0° or 45° in [0, q]²; scaling by 1/b gives eleven unit squares at 0°/45° with disjoint
interiors in a container of side q/b = L₀. Stromquist’s Theorem 3 says eleven open
squares of side > 1 at 0°/45° do not fit in side L₀; dilating the closed configuration
by a factor slightly above 1 about the container centre produces exactly that (the
BC-255 review’s boundary bridge).
∎

The same computation at the review’s side 3.88 gives the 2 arctan(1/1500) = 0.076°
quoted there; at U it gives 0.126°, at 3.86 0.38°. The statement inherits the status of
Theorem 3, whose strengthened lemmas 7–8 are stated without proof in the 2003 paper and
were assessed in BC-255. This is weaker than H-036 (0.25° robust bands, side ≥ 3.878) in
the side but far stronger in the band at q; H-036 remains OPEN.

**Theorem 1.11 (robust {0°, 45°} band at q; EXACT-VERIFIED, no Stromquist input).** No
packing of eleven unit squares in [0, 96/25]² has every folded angle in [0°, 1.4503°] ∪
[43.7565°, 45°]. Equivalently, every packing of eleven at side ≤ 3.84 has a square whose
folded angle lies in (1.4503°, 43.7565°).

*Proof.* The class Θ = cells 0–5 ∪ 175–180 of the retained net is exactly that folded
set (cell bounds are exact tangents, `DirectionClasses.cell_bounds`). The
composition-(11, 0) class program at q on grid 79 converged in 29 rounds; its
rationalised measure has total mass 10.7021484375 = 43836/4096 and the exact event-cell
sweep reports least covered mass 1025/1024 ≥ 1 on every direction of Θ, with Conditions
1, 3, 4 holding (`$S/prio2_q.jsonl`, first record).
If all eleven squares had angles in Θ, their eleven pairwise disjoint B-cores would each
carry mass ≥ 1, total ≥ 11 > 10.7022. ∎

This doubles the transfer band of Proposition 1.6 on both ends and needs neither Theorem
3 nor its unproved lemmas 7–8; it is the first rung of the band ladder of §3.5. On grid
79 the next symmetric widening (cells 0–12 ∪ 168–180, i.e. 3.30° and 3.30°) is *not*
refuted (11.16), so the grid-79 rung lies between the two; Session S2 refines it.

**Theorem 1.12 (a square below 30°; EXACT-VERIFIED).** At most ten squares of any
packing in [0, 96/25]² have folded angle in [30.0149°, 45°]; hence every packing of
eleven at side ≤ 3.84 contains a square with folded tilt < 30.0149°.

*Proof.* The class of cells 117–180 (lower bound the exact tangent
120639827500000/208829222337727 of 30.0149°) has a converged class program at q on grid
79 whose rationalised measure has mass 42589/4096 = 10.39771 and least covered core mass
4147/4096 ≥ 1 on every class direction, all conditions holding (`$S/prio2_q.jsonl`,
record `tiltge30`). Eleven disjoint cores in the class would carry mass ≥ 11 > 10.398. ∎

**Corollary 1.13 (angle-count facts at side ≤ 3.84, all EXACT-VERIFIED or PROVED).**
Every packing of eleven unit squares in [0, 96/25]² has: (a) at most nine squares with
folded tilt ≤ 6.4537°, so at least two with tilt > 6.4537° (nine points suffice for
4.6122°, and the bare grid for 2.44°); (b) at most ten with tilt ≤ 10.3875°; (c) at most
nine within 2.1547° of 45°; (d) at most ten within ±2.44° of 40.194°; (e) a square with
folded angle in (1.4503°, 43.7565°); (f) a square with folded tilt below 30.0149°; (g)
(Proposition 1.6) a square farther than 0.6848° from both 0° and 45°. Trump’s packing
(six at 0°, five at 40.18°) satisfies all of them with room: the counts are consistent,
not sharp, and (a)–(d) cannot be sharpened below 9 or 8 by any covering argument (§3.1).

### 1.4 Segment contacts and orientation classes (PROVED)

**Lemma 1.7 (propagation).** In a packing, if two squares share a boundary segment of
positive length, their orientations agree modulo π/2; a square with a positive-length
segment on a container wall is axis-parallel.
Let G be the graph with the eleven squares and a wall vertex, edges for positive-length
segment contacts; if k(G) is the number of components not containing the wall vertex,
then the orientations of the packing take at most k(G) + 1 values modulo π/2 (at most
k(G) distinct non-axis values), and the “angular incidence” system (one equation θ_i =
θ_j per edge, θ_i = 0 per wall edge) has rank 11 − k(G).

*Proof.* Two closed unit squares with disjoint interiors that share a segment of
positive length share the supporting line of that segment as an edge line of both (a
segment of one square’s boundary that is not contained in one edge would contain a
corner, and the other square’s boundary would have to contain a neighbourhood of that
corner on the same line — an edge of the other square — so the two edges are collinear
either way); parallel edges mean equal orientation modulo π/2. Rank: a spanning forest
of G has 11 − k(G) edges after contracting the wall into the forest, and these are
independent. ∎

Trump’s packing (review of 2026-09-07, `cases/trump11`): six wall-anchored squares, one
unanchored five-square component, k = 1, rank 10, exactly one non-axis angle.
This is a description of one packing; Lemma 1.7 bounds *nothing* for an unknown packing
without an independent bound on k(G), and §3.3 shows that no local argument supplies
one.

**Lemma 1.8 (first-order movability of a square with few point contacts).** Let Q be a
square of a packing and suppose every contact of Q with the container and with other
squares is of one of the smooth kinds: a corner of Q in the relative interior of a wall
or of an edge of another square, or a corner of another square in the relative interior
of an edge of Q (no corner-to-corner coincidence and no positive-length segment
contact). Each such contact is described near the current pose p₀ = (x, y, θ) ∈ ℝ³ of Q
by one smooth inequality g_j(p) ≥ 0 (the signed distance of the corner to the edge
line), and locally the feasible poses of Q with everything else fixed are exactly {g_j ≥
0 ∀ j}. If there is no nonzero λ ≥ 0 with Σ_j λ_j ∇g_j(p₀) = 0, then Q admits a finite
feasible motion along which its orientation changes continuously, all other squares and
the container fixed.
In particular this holds when Q has at most two such contacts with non-antiparallel
gradients, and when it has three with linearly independent gradients.

*Proof.* By Gordan’s alternative there is v ∈ ℝ³ with ∇g_j(p₀)·v > 0 for all j; the set
of such v is open, so it contains a v with v_θ ≠ 0. Then g_j(p₀ + tv) = t ∇g_j·v + O(t²)
\> 0 for small t > 0, and the strict separations from all non-touching squares and walls
persist by continuity; the local equivalence of “g_j ≥ 0” with non-overlap holds because
the touching corner is in the relative interior of the edge and all other feature pairs
are strictly apart, so crossing the edge line means entering the other square’s
interior.
The two- and three-contact cases: with ≤ 3 vectors in ℝ³, a nonzero nonnegative
null combination exists only if two are antiparallel or the three are linearly dependent
with a positive relation.
∎

Consequences. (a) A square whose orientation is *locked* (no motion at all with the rest
fixed) has a segment contact, a corner–corner coincidence, or at least three point
contacts carrying a positive stress; generically four.
(b) Two antiparallel gradients occur exactly when Q is wedged between two parallel lines
at distance equal to its width in that direction and the width is stationary in θ, i.e.
the lines are at 45° to Q’s edges; there Q is still movable (rotation reduces the width
at second order) but not by the first-order argument.
(c) The lemma is a rattler criterion, and rattlers *increase* the number of orientation
classes a packing can have; it cannot bound that number.
It is the tool that would be needed to prove that a square “with fewer than k
independent active constraints can be moved”, and the answer is k = 3 in general
position, with the two exceptional degenerate patterns above.

**Lemma 1.9 (width lemma: a confined square whose feasible angles avoid every
neighbouring class).** If a unit square at folded angle θ lies in a region R, then for
every direction u the width of R in direction u is at least the width of the square,
which is
|cos ψ| + |sin ψ| for ψ the angle between u and an edge of the square. If R has width w_v in
the vertical direction and width w_d in the diagonal direction (45°) then √2 sin(θ +
45°) ≤ w_v and √2 cos θ ≤ w_d, so the feasible folded angles lie in
[arccos(w_d/√2), arcsin(w_v/√2) − 45°]. For w_v, w_d ∈ (√2 cos 22.5°, √2) = (1.3066,
1.4142) this interval is non-empty and contained in the open interval (0°, 45°): a unit
square can sit in such a region at 22.5° but at neither 0° nor 45°. For the hexagon
H(w_v, w_d) = {|Y| ≤ w_v/2, |X ± Y| ≤ w_d/√2} the width conditions are also sufficient
to the resolution of a 0.1° LP scan (§2.5; NUMERICAL): e.g. H(1.36, 1.36) admits the
folded angles [15.9°, 29.1°] and nothing outside [15.92°, 29.08°].

*Proof of the width bound.* Containment is monotone under projection onto u. ∎

**Lemma 1.10 (the natural realisation with four corner diamonds is impossible).** A
pocket bounded by four axis-parallel unit-square edges (top, bottom, left, right, at
distance 2r < √2 apart) and by the inner edges of four unit squares at 45° in its
corners (diagonal width 2ρ < √2) cannot occur in a packing.

*Proof.* Put the pocket centre at the origin.
The lower-right diamond has an edge on the line X − Y = √2 ρ and its centre at (ρ/√2 +
1/2, −ρ/√2 − 1/2) (distance ρ + √2/2 from the origin along (1, −1)/√2); its leftmost
vertex is at X = ρ/√2 + 1/2 − √2/2 = ρ/√2 − 0.2071, at the height Y_c = −ρ/√2 − 1/2 of
its centre.
The bottom axis square is [x₀, x₀ + 1] × [−r − 1, −r]; since r ≤ ρ/√2 + 1/2 ≤
r + 1 for r, ρ ∈ (0.65, 0.71) (the range Lemma 1.9 needs), the height Y_c lies inside
its vertical extent, so at that height it must fit between the two bottom diamonds’
inner vertices: 1 ≤ 2(ρ/√2 − 0.2071), i.e. ρ ≥ 1.0 > √2/2. ∎

So the mixed pocket of Lemma 1.9 cannot be built from a square hole chamfered by four
diamonds; whether it can be built at all from unit squares at 0° and 45° (walls, two
diamonds and axis squares, or with a third class of features) is OPEN and is Session S5
below. Its role in §3.3 does not depend on realisability.

## 2. Numerical checks

All commands were run from `/home/user/squares/packing` with
`OMP_NUM_THREADS=1 $S/venv314/bin/python3 …`; the machine has one core.

### 2.1 Exact constants (`$S/anglemath.py`, system python3)

```
q = 96/25: L/4 = 0.960000; theta0 = 2.44001 deg, tan theta0 = 0.042611956
U (3.877084): L/4 = 0.969271; theta0 = 1.84653 deg, tan theta0 = 0.032239228
at q: tan theta = 1/24 gives inscribed side^2 = 577/625 > (24/25)^2: True; 1/23: False
sharpness: square tilted by theta0 + 1e-9 centred at (3L/8, 3L/8) avoids all nine points (q and U)
Theorem-3 transfer: not all eleven within delta of {0,45}: delta = 0.6848 deg at q,
   0.3815 at 3.86, 0.2317 at 3.87, 0.1263 at U
net index 159: 40.1940 deg; 149: 37.85; 169: 42.50; 180: 45.00
```

### 2.2 Nine-point sets decided by the exact sweep (`$S/nine_points.py`)

Nine unit atoms at {1 − δ, L/2, L − 1 + δ}²; “pierces leading k cells” means the exact
sweep reports least covered mass ≥ 1 on every direction of cells 0..k−1 (B-cores); the
last column is the upper bound of cell k−1 (closed folded range).

| side | δ | cells pierced | folded tilt ≤ |
| --- | --- | --- | --- |
| q = 96/25 | 0 | 0 | — (atom (1,1) on the core boundary of the flush corner square) |
| q | 1/200 | 18 | 4.6122° |
| q | 1/100 | 17 | 4.3489° |
| q | 1/50 | 14 | 3.5588° |
| q | 1/25 | 9 | 2.2411° |
| q | 3/50 | 4 | 0.9229° |
| q | ≥ 2/25 | 0 | — |
| q | L/4 grid (control) | 9 | 2.2411° |
| 3877084/10⁶ | 1/200 | 13 | 3.2953° |
| 3877084/10⁶ | 1/100 | 12 | 3.0318° |
| 3877084/10⁶ | 1/50 | 10 | 2.5047° |
| 3877084/10⁶ | 1/25 | 5 | 1.1866° |
| 3877084/10⁶ | L/4 grid (control) | 7 | 1.7139° |

The control agrees with exp-064 (leading six cells ≤ 1.45° certainly, seven cells at
1.71° is the B-core version of θ₀(U) = 1.85°). Monotone decrease in δ is Proposition 1.4
in action: the cells widen with δ.

### 2.3 Band certificates: class program, composition (11, 0), grid 79 inset 1/10, exact decision (`$S/angle_bands.py bands`, `$S/rerun_bands.py`)

For a class Θ (union of half-gap cells) the composition-(11, 0) program computes a
D4-symmetric measure of mass M every admissible B-core at a direction in Θ covers with
mass ≥ 1 (w₀ = 1); “exact M” is the mass of the rationalised atoms after the exact sweep
confirmed Condition 5′ on every class direction.
**Count bound: at most ⌊exact M⌋ squares of any packing at side ≤ L have folded angle in
the closed range of Θ** (Theorem 1.5’s counting step; EXACT-VERIFIED where an exact M is
given). “float” means the row loop did not converge and the point was not, or could not
be, exact-decided; those rows are NUMERICAL only.
Logs: `$S/bands_q_g79.jsonl`, `$S/bands_U_g79.jsonl`, `$S/prio_q.jsonl`,
`$S/prio2_q.jsonl`, `$S/split25.jsonl` (the U-side sweep and the large “tilt ≥ 10°/20°”
bands were cut for time on the single core; what ran is what is tabulated).

**Near-axis bands, q = 96/25:**

| class (cells) | folded range | float M | exact M | count bound |
| --- | --- | --- | --- | --- |
| 0–5 | [0°, 1.4503°] | 9.0000 | 9.00391 | ≤ 9 |
| 0–9 | [0°, 2.5047°] | 9.0000 | 9.00391 | ≤ 9 |
| 0–18 | [0°, 4.8754°] | 9.0000 | 9.00586 | ≤ 9 |
| 0–24 | [0°, 6.4537°] | 9.0000 | 9.00586 | ≤ 9 |
| 0–29 | [0°, 7.7671°] | 9.3333 | 9.33887 | ≤ 9 |
| 0–34 | [0°, 9.0785°] | 10.0000 | 10.00977 | ≤ 10 |
| 0–39 | [0°, 10.3875°] | 10.5000 | 10.51270 | ≤ 10 |
| 0–49 | [0°, 12.997°] | 11.0 (80 rounds, not converged) | — | none |
| 0–59 | [0°, 15.593°] | 11.0000 | 11.00977 (Condition 2′ fails) | none |

**Near-axis bands, side 3877084/10⁶ ≥ U:** 0–15 (≤ 4.0856°): exact 9.00586 → ≤ 9; 0–18
(≤ 4.8754°): 9.55151 → ≤ 9 (exp-064’s number, reproduced); 0–21 (≤ 5.6649°): 9.70215 → ≤
9; 0–24 (≤ 6.4537°): 9.82910 → ≤ 9; 0–29 (≤ 7.7671°): 10.00293 → ≤ 10; 0–34 and wider: ≥
11.005, no bound.

So at q at most nine squares are within 6.45° of the axes and at most ten within 10.39°;
at U at most nine within 6.45° and at most ten within 7.77°. The measure at q for 0–24
is the smeared nine-point pattern (24 atoms of weights 1/4 and 1/2 at (0.987, 0.893),
(0.893, 0.987), (0.987, 0.987), (1.873, 0.987), (1.967, 0.987), … and their images),
i.e. the box positions of Lemma 1.3 with the middle point split in two.

**Near-45° bands, q:** trailing 1 cell [44.887°, 45°]: float 9.452 (not converged);
trailing 3 [44.436°, 45°]: exact 9.49414 → **≤ 9 squares within 0.564° of 45°**;
trailing 6 [43.757°, 45°]: float 9.623; trailing 10 [42.845°, 45°]: float 9.690;
trailing 19 [40.774°, 45°]: float 9.831; trailing 30 [38.205°, 45°]: float 9.937 (80
rounds). **Near-45° bands, U:** trailing 6: exact 10.15820 → ≤ 10 within 1.24° of 45°;
trailing 10 [42.845°, 45°]: exact 10.1875 → ≤ 10; trailing 30: float 10.35.

**Trump band, q** (`$S/rerun_bands.py`, round cap 150/100, exact decision of the final
point regardless of convergence): cells 157–161 [39.73°, 40.66°]: float 9.857 (not
converged), exact M = 10.03296 with every class core covered (least 4147/4096) → **≤ 10
squares within ±0.47° of 40.19°** (EXACT-VERIFIED); cells 154–164 [39.03°, 41.35°]:
float 9.888, exact point fails Condition 5′ by 1/2048 at direction 154 → undecided
(NUMERICAL: the value is ≈ 9.9, so “≤ 9 in the ±1.2° Trump band” is the expected theorem
with more rounds). Mid-angle bands are much slower for the row loop than the near-axis
ones (many event cells per direction at grid 79).

**Union-of-end-cells classes, q** (the robust {0°, 45°} band, Task 5’s first rung):

| class | folded set | float M | exact M | verdict |
| --- | --- | --- | --- | --- |
| 0–5 ∪ 175–180 | [0°, 1.4503°] ∪ [43.7565°, 45°] | 10.6866 | **10.70215**, least core mass 1025/1024, all conditions hold | **refuted: no packing of eleven at side ≤ 96/25 has all folded angles in this set** (EXACT-VERIFIED; Theorem 1.11) |
| 0–12 ∪ 168–180 | [0°, 3.2953°] ∪ [41.7°, 45°] | 11.139 | 11.157 (Condition 2′ fails) | not refuted on grid 79 |

**Further exact rows at q from the re-run script** (round cap 100, exact decision of the
final point; the folded ranges below are the exact cell bounds, `cell_bounds`, not the
net directions): trailing 10 cells [42.8453°, 45°]: float 9.694 (not converged), exact M
= 9.75488, least core mass 2053/2048, all conditions hold → **≤ 9 squares within 2.155°
of 45°**; cells 149–169 [37.7333°, 42.6166°]: float 9.946 (not converged), exact M =
10.13892, least 1037/1024 → **≤ 10 squares within ±2.44° of 40.19°** (the ±2-cell band
157–161 is [39.6115°, 40.7743°], ±5 is [38.9097°, 41.4678°]); cells 0–18 ∪ 162–180:
11.165, not refuted; cells 0–29 ∪ 151–180 ([0°, 7.77°] ∪ [38.2°, 45°]): 11.269, not
refuted.

**Cells 117–180 = [30.0149°, 45°] at q:** converged in 60 rounds (700 s); float 10.2309,
exact M = 10.39771 = 42589/4096, least core mass 4147/4096 at direction 117, Conditions
1, 3, 4 hold → **at most ten squares of any packing at side ≤ 96/25 have folded angle ≥
30.0149°; every packing of eleven has a square with folded tilt < 30.0149°**
(EXACT-VERIFIED, Theorem 1.12). Trump’s packing has six such squares.

**Cells 139–179 = [35.3556°, 44.8874°] at q:** converged in 94 rounds (927 s); float
10.065, exact M = 10.23975, least core mass 259/256 → **≤ 10 squares in
[35.36°, 44.89°]** (EXACT-VERIFIED; implied by Theorem 1.12 up to the last cell, and
consistent with it).

Costs on one core at grid 79: near-axis and end-cell classes 1–15 s; the 45°-side and
Trump bands 60–930 s because their event grids are dense; the composition split 25–180 s
per composition. Nothing here was run at grid 119 or with adaptive sites; every “none”
above may change with a stronger site set, every “≤ N” cannot.

### 2.4 Fixed-angle packing numbers, lower bounds by MILP on a 0.1-grid (`$S/fixed_angle_packing.py`)

P(θ, L) = the largest number of pairwise interior-disjoint unit squares all at
orientation θ in [0, L]²; computed as a MILP (HiGHS) over lower-left corners on a
0.1-grid in the frame rotated by −θ with exact half-open clique rows (every solution is
a genuine packing, so these are rigorous lower bounds; the true P may be larger
off-grid). Every band Θ ∋ θ has fractional and integral piercing number ≥ P(θ, L), so no
count bound below P(θ, L) is possible for it.

| θ | P(θ, 3.84) ≥ | P(θ, U) ≥ |
| --- | --- | --- |
| 0° | 9 | 9 |
| 5°, 10°, 15°, 20°, 25°, 30° | 9 | 9 |
| 35° | 8 | 9 |
| 40.181937° | 8 | 8 |
| 42° | 8 | 8 |
| 45° | 8 | 8 |

At 45° the exact value is P(45°, q) ∈ {8, 9}: the MILP packing gives ≥ 8, and the exact
class certificate for the trailing three cells (§2.3: mass 9.494 < 10 with every
44.44°–45° core covered) gives ≤ 9. I could not settle 8 versus 9 by hand: in
coordinates u = (x+y)/√2, v = (x−y)/√2 the problem is “centres in the diamond |p| + |q|
≤ L/√2 − 1 = 1.7153 with pairwise L∞-distance ≥ 1”, a row (centres with pairwise |Δq| <
1\) holds at most 1 + 3.4306 − |q_a| − |q_b| ≤ 4 centres, but summing such row bounds
over a partition of the q-range never gets below 11, and no covering (weighting)
argument can reach 8 because the fractional value of the same band is ≈ 9.45 > 9 on grid
79\. NUMERICAL: the MILP optimum on the 0.1-grid is 8 at both sides (4 + 2 + 2 in three
rows). If the true fractional value exceeds 9, no nine-point set pierces all 45° squares
at q; OPEN (Session S3).

### 2.5 The confined-square LP (`$S/pocket.py`)

Feasible folded angles of a unit square inside the hexagon H(w_v, w_d) of Lemma 1.9 (LP
over θ in 0.1° steps; “width prediction” is the interval of Lemma 1.9):

```
wh=1.36 wd=1.36: LP feasible folded angles = [16.0, 29.1] deg; width prediction [15.92, 29.08]; theta=0 fits False, theta=45 fits False
wh=1.32 wd=1.40: [8.2, 24.0] ; prediction [8.13, 23.97]; 0 False, 45 False
wh=1.40 wd=1.32: [21.1, 36.9]; prediction [21.03, 36.87]; 0 False, 45 False
wh=1.31 wd=1.31: [22.2, 22.8]; prediction [22.13, 22.87]; 0 False, 45 False
wh=1.42 wd=1.36: [16.0, 45.0]; prediction [15.92, 45.00]; 0 False, 45 True
wh=1.36 wd=1.42: [0.0, 29.1] ; prediction [0.00, 29.08]; 0 True,  45 False
```

The LP agrees with the width prediction to the scan resolution, so for this region the
width conditions are necessary and sufficient.
(The first version of this script used four corner diamonds in a 3.05–3.10 container and
found 45° feasible — which led to Lemma 1.10.)

### 2.6 Composition split at q (`$S/split_sel.py`, grid 79, near class Θ₀ = leading 25 cells, folded tilt ≤ 6.4537°)

The two-threshold program (X-014 Lemma 3, `solve_class_program`) for compositions (n₀,
n₁ = 11 − n₀), normalised by n₀w₀ + n₁w₁ = 1; margin = M − 1 (negative refutes).
Since Θ₀ alone has exact covering value 9.006 (§2.3), (11, 0) and (10, 1) are refuted by
the count; the question is whether pricing the tilted squares at their own threshold
buys anything for n₀ ≤ 9. This near class is wider than the nine-point tilt for B-cores
(`within_nine_point_tilt` is False for 25 cells), which is allowed: the count for it
comes from §2.3’s certificate, not from the nine points.

| (n₀, n₁) | w₀ | w₁ | M (normalised) | margin | rounds, time | reading |
| --- | --- | --- | --- | --- | --- | --- |
| (9, 2) | 1/9 | 0 | 1.000000 | +0.000000 | 11, 23 s | LP collapses to the near-axis count: w₁ = 0 optimal, the two tilted squares are priced at nothing; not refuted (margin exactly 0 = the count bound 9 ≤ 9) |
| (8, 3) | 0.092233 | 0.087379 | 1.032362 | +0.032362 | 32, 88 s | not refuted; M/w₀ = 11.19 against 8 + 3·0.947 = 10.84 |
| (6, 5) | 0.090780 | 0.091064 | 1.033036 | +0.033036 | 24, 69 s | not refuted; w₀ ≈ w₁: the split buys nothing over the unconditional program |
| (5, 6) | 0.090454 | 0.091288 | 1.032397 | +0.032397 | 28, 91 s | not refuted; same |
| (3, 8) | 0.089585 | 0.091406 | 1.030104 | +0.030104 | 34, 128 s | not refuted; same |
| (0, 11) | 0 | 1/11 | 1.018871 | +0.018871 | 37, 182 s | not refuted: the covering value restricted to tilts > 6.45° is 11.21 on this site set |

Reading (NUMERICAL, site-set dependent): on grid 79 at q no composition with n₀ ≤ 9 is
refuted, and for 3 ≤ n₀ ≤ 8 the optimal thresholds are equal to within 2%, i.e. the
two-threshold program degenerates to the unconditional one (whose grid-79 value at q is
> 11 as well). The only composition where the class split does anything is n₀ = 9, where
> it reduces to the count.
> exp-064 saw the same at U: one threshold +0.082, two thresholds +0.072. So
> conditioning on *this* angle count has no headroom at q on this site set; the headroom
> question is transferred to a strong site set and to the fractional-packing certificate
> of the obstruction (Session S1), with the 3.82 evidence of §3.1 predicting that the
> obstruction is real (fractional packings with about seven near-axis units and the rest
> at 8°–30° exist at 3.82 with value 10.38 and will only grow at 3.84).

The class-weighted fractional packing polytope Π(q) (§3.4) therefore very probably
contains points with n₀ + n₁ ≥ 11 for every n₀ ≤ 9 — but this is *not* proved here: a
converged covering LP on a finite site set is an upper bound on the covering value, not
a fractional packing; the depth-≤1 certificate is S1’s job.

## 3. Obstructions: what does not work and why

### 3.1 Which bands admit no useful count, and why

Three facts bound what any covering argument — points, weighted points, or the class
program — can say about a band Θ at side L:

1. **Packing floor.** Any count bound N(Θ) obtained from a measure that every Θ-core
   covers with mass ≥ 1 satisfies N(Θ) ≥ ν*(Θ) ≥ P(θ, L) for every θ ∈ Θ (a fixed-angle
   packing is a fractional packing of the dual).
   By §2.4, P(θ, q) ≥ 9 for every θ ≤ 30° and ≥ 8 for θ ∈ [35°, 45°]: no band gets a
   count below 9 unless it lies inside (30°, 45°], and none below 8 at all.
   So “at most nine near-axis squares” is the best possible near-axis count at q by any
   covering method whatsoever, and the only room is in the *width* of the band (6.45°
   fractional, 4.61° with nine points, §1) and in bands inside (30°, 45°], where 8 is
   conceivable but the fractional value already sits at 9.45 for the single 45° cell.

2. **Fractional saturation.** The unconditional covering value at 3.82 is bracketed
   10.384 ≤ ν* ≤ τ* ≤ 11.056 (exp-070), so at q ≥ 3.82 every band Θ whose fractional
   packing value already exceeds 11 gives nothing.
   On grid 79 at q this happens for the near-axis band of width 13° (0–49 cells, 11.0)
   and beyond, i.e. as soon as the band is wide enough for the fractional packing to
   shift its near-axis mass around: the 3.82 depth-1 family
   (`bc-232-leg-01-family.json`, exact depth ≤ 1, value 10.384) has folded angular
   support 6.54 in
   [0°, 2.5°), 0.69 in [7.5°, 10°), 1.33 in [27.5°, 30°) and only 0.41 in [38.2°, 45°]
   (computed here; `$S` shell transcript).
   The obstruction the instrument sees near q is therefore *not* Trump-shaped: it is
   seven near-axis cores plus fractional mass around 29° and 8°, which is exactly a
   configuration no integral packing realises (nine near-axis squares fit, but the
   remaining two must then be far from the axes with room for nothing at 29°). That is
   an integrality gap of the covering relaxation, and it is where geometric conditioning
   (H-111) rather than angle counting has to work.

3. **Lattice counting for generic angles.** For a fixed generic θ the θ-rotated integer
   lattice clipped to [0, L]² has about L² = 14.7 points, so a lattice piercing set for
   the single angle θ is useless (≥ 11 points); only the integer effects of L < 4 near θ
   = 0 (⌊L⌋² = 9 disjoint squares, nine grid points) and near 45° (rows 4 + 2 + 2 = 8
   diamonds) push the count below eleven, and the fractional relaxation smooths even
   those: P(θ, q) = 9 for all θ ≤ 30° (MILP) while the fractional band values rise from
   9.0 (≤ 6.45°) through 10.5 (≤ 10.4°) to ≥ 11 (≤ 13°). Bands that contain the
   near-axis range together with the 8°–30° stretch admit no bound at all (that is where
   the 3.82 dual puts its mass); the band [30°, 45°] on its own still does (≤ 10,
   Theorem 1.12), because the dual puts only about 0.8 of its 10.38 units there.

**Summary of what the bands give at q on grid 79** (§2.3, §2.6; each “≤ N” is
EXACT-VERIFIED, each “none” is a non-refutation on this site set and therefore
NUMERICAL):

| band (folded) | best count | status |
| --- | --- | --- |
| [0°, 6.45°] | ≤ 9 | exact; the nine-point set gives ≤ 9 on [0°, 4.61°] by hand-checkable atoms |
| [0°, 10.39°] | ≤ 10 | exact |
| [0°, 13°] and wider near-axis | none (≥ 11.0) | fractional saturation; §3.1 item 2 |
| [44.44°, 45°] | ≤ 9 | exact |
| [42.85°, 45°] | ≤ 9 | exact (mass 9.755) |
| [40.77°, 45°], [38.2°, 45°] | ≈ 9.8, 9.9 float | undecided (not converged); ≤ 10 likely exact with more rounds |
| [39.61°, 40.77°] (±0.6° about 40.19°) | ≤ 10 | exact |
| [38.91°, 41.47°] (±1.3°) | ≈ 9.9 float | undecided |
| [37.73°, 42.62°] (±2.4°) | ≤ 10 | exact (mass 10.139; float 9.95) |
| [30.01°, 45°] | ≤ 10 | exact (mass 10.398): **Theorem 1.12** |
| [0°, 1.45°] ∪ [43.76°, 45°] | ≤ 10 (value 10.70) | exact: **Theorem 1.11** |
| [0°, 3.30°] ∪ [41.7°, 45°], [0°, 7.77°] ∪ [38.2°, 45°] and wider unions | none (≥ 11.14) |  |
| (6.45°, 45°] (all tilted, composition (0, 11)) | none (11.21) |  |
| any composition (n₀, 11 − n₀), n₀ ≤ 9, near class [0°, 6.45°] | none | w₀ ≈ w₁: no leverage |
| [35.36°, 44.89°] | ≤ 10 | exact (mass 10.240) |
| everything, all 181 cells | none | (≥ 11.06 already at 3.82) |

The pattern is the one items 1–3 predict: every band that excludes the near-axis range,
and every near-axis band narrower than 8°, has a count; every band that contains both
the axis and a stretch of 8°–30° has none.
The composition split adds nothing because its optimal thresholds are equal (w₀ ≈ w₁)
whenever both classes are populated — the instrument prices a near-axis core and a
tilted core identically at q, which is the numerical face of the same integrality gap.

### 3.2 Site-set dependence, and what a non-refutation means (the exp-064 lesson)

The class program’s optimum on a finite site set is an *upper* bound on the class
covering value; a non-refutation on a product grid is therefore never evidence.
exp-064’s side scan for the two end cells (grid 39, inset 1/10) reported refutation only
below 3.755, while the retained T-018 certificate (1121 adaptive atoms at 3.81) is a
feasible point of that very class program with mass 10.86 < 11 — so the class covering
value at 3.81 is < 11 and the scan’s “not refuted at 3.76” was a site-set artefact.
Two corollaries for this report: every non-refutation in §2.3 and §2.6 is inconclusive
by itself; and the *only* way to prove that a band or a composition cannot be closed by
the instrument at a side is a fractional packing of the dual (depth ≤ 1 at every
arrangement vertex, `ceiling.py`), or an integral one (eleven disjoint B-cores of the
class in the container).
The integral obstruction for the exact {0°, 45°} class is Stromquist’s own value: eleven
such cores fit iff L/B ≥ L₀, i.e. L ≥ B·L₀ = 3.87668 — below U (this is why exp-064’s
control was unreachable) but above q, so at q the {0,45}-band program is not obstructed
integrally (Session S2). For the full net the integral obstruction is Trump’s own cores
at L ≥ 3.868983 (CERTIFICATE-REACH), also above q. At q nothing integral is known to
obstruct any class; the obstructions, if any, are fractional.

### 3.3 The exact obstruction to a “fewest non-axis angles” minimizer argument (H-121)

The argument H-121 proposes: choose a global minimizer P with the fewest distinct
non-axis orientations; if there are at least two, exhibit a finite feasible motion at
non-increasing side that ends with fewer; contradiction.
Write (E) for the needed lemma: *every packing at side s with ≥ 2 distinct non-axis
classes is joined, within the space of packings at side ≤ s, by a path to a packing with
fewer non-axis classes.* Three precise obstructions:

1. **Local motions of one square do not suffice, and no local lemma can make them
   suffice.** Lemma 1.8 gives the exact condition under which a square can move at all
   with the rest fixed (no nonnegative stress on its own contact gradients), and Lemma
   1.9 gives a region shape — width strictly between √2 cos 22.5° and √2 in the axis and
   in the diagonal direction — in which a movable square’s whole angle range is a closed
   interval avoiding 0°, 45° and every orientation of the confining features.
   A square so confined by 0°/45° features can be rotated but never *merged* into a
   class by its own motion.
   Whether such a pocket is realisable inside a genuine packing is OPEN (Lemma 1.10
   removes the most natural realisation; Session S5), but the point stands
   independently: any proof of (E) must move several squares at once, through contact
   changes, and there is no first-order or single-square principle that produces such a
   motion.

2. **Locally isolated multi-class packings make (E) a global statement.** If P is
   locally isolated at its side (exp-013 proves this for Trump’s packing: every branch
   cone is {0}), then no path at side ≤ side(P) leaves P, so (E) can hold at P only if P
   is not a minimizer — i.e. (E) at P is equivalent to “some *other* packing with fewer
   classes has side ≤ side(P)”, which is a comparison of global optima over two
   families, not a perturbation statement.
   Isolation is the typical situation for a jammed packing (Trump’s has 44 active rows
   on 33 coordinates); so the elimination lemma, wherever it is needed most, is exactly
   the restricted-family lower bound H-112/H-113 ask for.
   This is the precise sense in which H-121 is not a shortcut.

3. **No n-independent principle exists.** The best known packing at n = 17 has two
   distinct non-axis orientations (+39.80°, −36.62°; `frontier/n-017.md`), and the n =
   29 record has five, pairwise separated by ≥ 0.296° (exp-012, exp-037). If either is
   optimal, “some minimizer has ≤ 1 non-axis class” is false there, so any proof of
   H-121 must use n = 11-specific geometry (e.g. that six axis squares and five others
   must fill 3.84²); general contact or stress arguments cannot do it.

What *is* provable, for comparison: Lemma 1.7 (segment propagation, rank 11 − k), Lemma
1.8 (movability with < 3 independent point contacts), the counts of §1 (at least two
squares tilted > 4.61° at q; at least one farther than 0.68° from both 0° and 45°), and
the review’s LP-vertex statement (some minimizer with the same angles has a full
translation basis).
None of these bounds the number of components k of the segment graph:
a packing at side ≤ U with k = 11 (no segment contacts at all) is obtained from Trump’s
by shrinking each square about its centre by any factor in (B, 1) and rescaling — every
contact becomes a strict separation — so a bound on k can only hold for *minimizers*,
and the standards of this investigation allow no test of such a claim below U.
Conclusion: a bound on the number of distinct orientation classes in a side-minimal
packing is OPEN, and no elementary argument of the local kind can give one.

### 3.4 What the composition split can and cannot see

The dual of the two-threshold program is explicit.
For classes Θ₀, Θ₁ and counts (n₀, n₁), the program refutes the composition at side L
iff there is *no* fractional packing y ≥ 0 of admissible B-cores at net directions with
depth ≤ 1 everywhere and Σ_{Θ₀} y ≥ n₀, Σ_{Θ₁} y ≥ n₁ (one line of LP duality on
`_class_lp`: the normalisation row’s multiplier is the packing value).
So the complete split by n₀ = 0, …, 9 is the same object as the class-weighted
fractional packing polytope Π(L) = {(a, b): some depth-≤1 fractional packing has class
weights ≥ (a, b)}, and composition (n₀, n₁) survives iff (n₀, n₁) ∈ Π(L). Two
consequences. (i) Compositions dominated by a surviving one survive: if (6, 5) survives,
so do all (n₀, n₁) with n₀ ≤ 6, n₁ ≤ 5, and the ladder can only ever close a *down-set
complement*. (ii) The headroom question at q is exactly whether Π(q) contains the
segment {(a, 11 − a): 0 ≤ a ≤ 9}; since the unconditional value at 3.82 already sits at
11.000 on two site sets, Π(q) very probably contains points with a + b = 11, and the
only question is which.
§2.6 measures this on grid 79; Session S1 measures it with a strong site set and
certifies the obstruction with `ceiling.py`.

### 3.5 The band ladder (Task 5): what it is, and its first rung

A *band-restricted theorem* at side L is a statement “every packing of eleven all of
whose folded angles lie in S has side > L”, for a set S ⊂ [0°, 45°]. Stromquist’s
Theorem 3 is S = {0°, 45°} at L = L₀ = 3.8856; H-036 asks S = [0, 0.25°] ∪ [44.75°, 45°]
at 3.878; the class program proves such a theorem at L whenever the covering value
restricted to S (as a union of cells) is < 11 at L, exactly.
Three structural facts about the ladder:

- **Monotonicity in S and L.** The restricted covering value is monotone in both, so the
  ladder is a single non-decreasing function S ↦ L*(S) (the largest side at which S can
  be refuted) and the theorems nest.
  The ceiling of the instrument for S is L*(S) ≤ B·s_S(11), where s_S(11) is the least
  side for eleven unit squares with angles in S: for S = {0, 45} that is B·L₀ = 3.8767 <
  U (exp-064’s wall); for any S containing 40.18° and 0° it is ≤ B·U = 3.869 (Trump’s
  cores), so the ladder can never reach U on any rung that contains the Trump band
  together with the axis: those rungs are refuted at most up to 3.869 by this shrink,
  and the last rung (S = everything but a Trump band) is the unrestricted problem with
  the Trump band removed — its ceiling is B·s_S(11), which is unknown and is essentially
  the conjecture that Trump’s angle is necessary.
- **Where the ladder is new.** Below q the unconditional ladder is already proved (T-018
  at 3.81), so the band ladder only matters between 3.81 and the shrink cap 3.869, and
  at q it asks: which S have L*(S) ≥ q? By §2.3, all S ⊂ [0°, 7.77°] and all S ⊂
  [44.44°, 45°] do (values < 10, so even eleven cores are impossible with room to
  spare); by the 3.82 diagnostic (§3.1) the sets S that fail first are those containing
  a near-axis band of width ≳ 10° together with a cluster near 29°.
- **The first rung that is new and plausibly provable** is therefore S = [0, α] ∪
  [45° − β, 45°] at q with α + β as large as the site set allows (Session S2): it is new
  for any α, β beyond the 0.68° of Proposition 1.6 (which is the only current theorem of
  this shape below U), it is not integrally obstructed at q (q < B·L₀), and the
  instrument needs no new code.
  The second rung is S = [0, α] ∪ [45° − β, 45°] ∪ [γ₁, γ₂] with a mid band, which is
  where the 29° cluster will bite; the third is the complement of a Trump band (Session
  S4), which the diagnostic predicts will *not* close at q on the fractional instrument,
  and for which the honest formulation is the obstruction with its support histogram.

A ladder “with bands progressively enlarged until only a band around 40.18° remains” is
thus a sequence of class certificates whose last member is the unrestricted problem
minus the Trump band, and the fractional instrument is predicted to stall before that
member for the integrality reason of §3.1; the rungs it can prove are the near-{0,45}
ones, which are exactly Stromquist’s and H-036’s territory transported down to q with
wider bands.

## 4. Proposed research sessions

All sessions use the scratchpad venv (or `packing/.venv` once it builds), the retained
net and B, and `decide_class_program` / `class_minima` as the exact verifier; a run’s
float optimum is never a result.
Every session records its site set (grid count, inset, or the list of atom positions)
with the result, because §3.2 says a non-refutation is meaningless without it.
Sessions S1–S4 and S6 are mutually independent and can run in parallel; S5 is
independent of all of them.
Estimated hours are for one agent with one core; the class programs below took 1–8
minutes per band at grid 79 in this session.

### S1 — Composition-split headroom at q with a strong site set (3 h)

*Question.* With Θ₀ = the leading 25 cells (folded tilt ≤ 6.4537°, count ≤ 9 by §2.3)
and Θ₁ its complement, which compositions (n₀, 11 − n₀), n₀ = 0, …, 9, does the
two-threshold program refute at q = 96/25, and for those it does not, does a
class-weighted fractional packing certify that no site set can?
*Entry.* This report’s grid-79 margins (§2.6) as the control; `ceiling.py` as the depth
oracle; the T-018 atom positions (`certificate.json`) dilated by q/3.81 as an extra site
set (`site_set_from_points` in `colgen.py` accepts arbitrary points;
`solve_class_program` wants a `SiteGrid`, so either add the 1121 dilated points to a
grid-79 product set through a small adapter or run the class rows through `colgen`’s row
loop). *Procedure.* (1) Re-run n₀ = 0..9 at grid 119 and on the dilated-T-018 set,
`max_rounds ≥
200`; exact-decide every negative float margin; (2) for each surviving composition,
build the dual fractional packing from the final LP (the `y` of the rows) and run the
depth check at all arrangement vertices; add violating vertices as sites and iterate
(the cutting-plane loop X-014 measurement 1 describes); (3) report Π(q)'s boundary
points found. *Exit.* Theorem: “no packing at side ≤ 96/25 has exactly n₀ squares with
folded tilt ≤ 6.45° for n₀ ∈ R” with the exact atoms and thresholds frozen; or a scoped
obstruction: a depth-≤1 fractional packing with class weights ≥ (n₀, 11 − n₀) for the
compositions that survive (then no class certificate with this shrink and net closes
them at q). *Falsifier.* The fractional packing of step (2); for the theorem, any
packing at 3.84 with a refuted composition (none can exist if the decision is exact).
*Buys for 3.84.* The map of which compositions the composition route can ever close at
q. If (6, 5) and (5, 6) have fractional packings at q, the route to 3.84 must go through
geometric conditioning (Lemma 2 of X-014, H-111), not through angle counts; if some
mid-composition closes, the survivors become the branch list for that conditioning.

### S2 — The robust {0°, 45°} band theorem at q (2–3 h)

*Question.* The largest (α, β) such that the class Θ = [0, α] ∪ [45° − β, 45°] (a union
of end cells) has class covering value < 11 at q, exactly.
The result reads: every packing of eleven all of whose folded angles lie in [0, α] ∪
[45° − β, 45°] has side > 3.84 — the first rung of the band ladder of Task 5 and a
robust form of Stromquist’s Theorem 3 at a lower side (Proposition 1.6 gives α = β =
0.68° by transfer; H-036 asks 0.25° at 3.878). *Entry.* §2.3’s end-cell rows (k = 1, 6,
13, 19, 30, 40) at grid 79 as controls; the integral ceiling for the exact class is B·L₀
= 3.8767 > q, so the class is not integrally obstructed at q. *Procedure.* Symmetric
widening k → k + 1 until the exact decision fails at grid 119; then asymmetric (α wide,
β narrow and vice versa); freeze the atoms of the widest exact success.
*Exit.* An exact-decided (α, β) with α + β ≥ 3° (clearly beyond the transfer), or the
obstruction: a fractional packing on the end cells of value ≥ 11 at q (then this class
needs Stromquist’s box step — a conditional certificate — not a covering).
*Falsifier.* Eleven disjoint B-cores at directions in Θ inside [0, q]² (integral), or
the fractional packing.
*Buys for 3.84.* The ladder’s base case, and the width of the excluded
{0,45}-neighbourhood that any later case analysis may assume; also a direct comparison
with H-036’s method.

### S3 — The optimal integral nine-point set at q (2 h)

*Question.* Maximise the band [0, φ] such that some nine-point set pierces every unit
square of tilt ≤ φ in [0, q]²; product sets are capped at a(φ) = 0.92 (Proposition 1.4,
5.24°) and the pushed-corner set reaches 4.61° with B-cores (Theorem 1.5); staggered
rows are untested.
Secondary: is there an eight-point set for a band around 45° (P(45°) =
8 makes it possible in principle; the fractional value 9.45 says no if the true
fractional value exceeds 9), and a ten-point set for [0, 10°]? *Entry.* `class_minima`
with unit atoms as the exact verifier (`$S/nine_points.py`); Lemma 1.3’s boxes as the
search domain.
*Procedure.* Random restarts + coordinate search over nine points in their
boxes, objective the number of leading cells pierced, product family first (expected
optimum: corners at 1 − ε, middle at q/2) then staggered rows (row offsets up to 0.16);
every candidate decided exactly; for the 45° band use the trailing cells.
*Exit.* An exact-verified nine-point set with band ≥ 5.5° (beats every product set) or
the verified statement that no tested staggered set beats 4.61° together with the
product cap.
*Falsifier.* The minimum-mass cell the sweep reports is an explicit escaping
placement. *Buys for 3.84.* A hand-checkable count “at least two squares tilt > φ*” for
use in restricted-family theorems (H-036, H-102, H-112’s pruning m ≥ 2) without the
class program.

### S4 — Band ladder toward the Trump band at q (3–4 h)

*Question.* For Θ(k) = all cells except [159 − k, 159 + k] and Θ′(k) = all cells except
[159 − k, 180], find the smallest k with class covering value < 11 at q on a strong site
set; identify the angular support of the fractional packing when the value stays ≥ 11.
*Entry.* §2.3’s “all but Trump band” rows (grid 79); `ceiling.py`. *Procedure.* As S1
step (2) but with the class fixed to Θ(k); when the value is ≥ 11, extract the dual’s
directions and weights: the histogram of fractional weight by angle is the diagnostic.
*Exit.* A theorem “every packing at side ≤ 3.84 has a square with folded angle within Δ
of 40.19°” (a new structural fact if Δ < 5°), or the obstruction with the support
histogram attached. *Falsifier.* Fractional packing supported away from the band.
*Buys for 3.84.* Where the fractional obstruction at q lives in angle.
The 3.82 evidence (§3.1, item 2) already says: 6.5 units of the 10.38 sit within 2.5° of
the axes, 1.3 units near 29°, 0.7 near 8°, and only 0.4 in [38.2°, 45°]. If the q-side
dual keeps that shape, the obstruction is an integrality artefact of the covering
relaxation (at most nine near-axis squares are integral, and nothing integral sits at
29° beside seven near-axis squares) that geometric conditioning (H-111) can target, and
the Trump band itself is *not* what blocks the instrument; if the q-side support
migrates toward 40°, the instrument is seeing Trump-like fractional packings and the
split must go through H-111/H-112. Either answer redirects the programme; this is the
cheapest decisive measurement on the list.
First step (30 min): re-run the `ceiling.py` depth check on `bc-232-leg-01-family.json`
dilated to 96/25 (dilation preserves depth ≤ 1 and containment), then extend it by
cutting planes at q.

### S5 — Realisability of the mixed pocket, or a merging lemma (3 h)

*Question.* Does any packing of unit squares (any n, any container) contain a square
whose feasible angle set with the rest fixed is a closed interval avoiding 0°, 45° and
all other squares’ orientations, the confining features being walls and edges of squares
at 0° and 45° only? Lemma 1.10 excludes the four-corner-diamond octagon; the two-diamond
hexagon H(w_v, w_d) with two axis squares and two walls is the next candidate, and the
alternative is a positive lemma: with 0°/45° confinement the feasible set always meets
{0°, 45°}. *Entry.* `$S/pocket.py` (idealized region LP); a disjunctive
(separating-axis) LP over θ for candidate configurations of actual squares; exact
verification of any packing found.
*Exit.* An explicit verified packing (a counterexample to the single-square elimination
step for real squares), or a proof of the merging lemma for 0°/45° confinement (a
genuine structural lemma: “a rattler confined by two classes can always join one of
them”). *Falsifier.* For the lemma, the packing; for the packing, the SAT-LP
infeasibility over all θ in the claimed interval.
*Buys for 3.84.* Nothing numerical; it settles whether H-121’s local step has any hope
and therefore whether the structural lane (BC-288) should spend time on elimination
motions at all.

### S6 — Ten-point localisation band at q (3 h)

*Question.* With Stromquist’s ten Figure-13 points evaluated at q (the unchanged
formulas (1, 1), (q/2, 1), (3/2 − q/4, q/2), (1/2 + q/4, q/2) and their reflections),
for which band [0, α] does every unit square of tilt ≤ α that avoids all ten points have
its centre in the top or bottom wall rectangle [1, q − 1] × ([0, 1] ∪ [q − 1, q])? H-106
proved the ±0.25° near-axis clause at 1939/500 and H-123 the near-45° localisation
there; the instrument (polynomial guards over closed half-angle slabs, source-distinct
reader) exists and needs only q and the band as parameters.
*Exit.* A localisation theorem at q for a band α ≥ 2°, or the escaping square.
*Falsifier.* An exact escaping square (H-110-style fixed candidate).
*Buys for 3.84.* The premise every conditional certificate (X-014 Lemma 2, H-111’s
anchor box) needs: a square forced into a known box; combined with Theorem 1.5 it gives
“either two squares tilt > 4.6° or one square sits in a wall rectangle”, a two-branch
split with both branches concrete.

## 5. Open questions ranked by expected value

1. **Is the class covering value at q below 11 for any class containing both the axis
   cells and the Trump cells?** (S4, then S1.) Everything about the composition route at
   3.84 hinges on it, and the angular support of the dual is the diagnostic the
   programme lacks.
2. **The robust {0°,45°} band at q** (S2): the first rung that is new (Proposition 1.6
   gives 0.68°; anything ≥ 3° is a real theorem) and plausibly provable by the existing
   instrument.
3. **Do compositions (n₀, 11 − n₀) with 3 ≤ n₀ ≤ 8 close at q?** (S1.) A “no” with a
   fractional-packing certificate is as valuable as a “yes”: it ends the composition
   route.
4. **Exact count in the near-45 band:** is “at most nine squares in [38.2°, 45°] at q”
   true exactly (the float value is 9.94, not converged; §2.3)? A one-hour re-run with
   more rounds and the exact decision (`$S/rerun_bands.py`).
5. **The integral nine-point optimum and the eight-point 45° question** (S3).
6. **The mixed-pocket realisability or merging lemma** (S5): decides whether H-121’s
   local step is worth any further attention.
7. **H-036 at 3.878 with 0.25° bands** (existing, unresolved): after S2 and S6, it is
   the same question at a higher side and narrower band; S2’s method transfers.

## Appendix: scripts and outputs as run

Retained verbatim from the lane’s working directory on 2026-09-08. Scripts that import
`sqpack` were run through the project environment; the rest are standard-library Python.
None has been promoted to `devtools/`; the first lane that reuses one owns that
promotion.

### `anglemath.py`

```text
"""Exact arithmetic for the nine-point band, its sharpness, and the Theorem-3 transfer.

Runs on any CPython >= 3.10 (fractions + math only).
"""

from __future__ import annotations

import math
from fractions import Fraction as F


def isqrt_floor(n: int) -> int:
    return math.isqrt(n)


def theta0_tangent(L: F) -> tuple[F, F, float]:
    """tan(theta0) where cos theta0 + sin theta0 = 4/L, exactly as a quadratic root.

    (1+t)^2 = r^2 (1+t^2) with r = 4/L, i.e. (r^2-1) t^2 - 2 t + (r^2-1) = 0, so
    t = (1 - sqrt(1 - (r^2-1)^2)) / (r^2-1). Returns rational lower and upper bounds
    and a float.
    """
    r2 = (4 / L) ** 2
    a = r2 - 1
    disc = 1 - a * a
    # rational sandwich of sqrt(disc)
    num, den = disc.numerator, disc.denominator
    scale = 10**30
    s_lo = F(isqrt_floor(num * scale * scale // den), scale)  # <= sqrt(disc)
    s_hi = s_lo + F(1, scale)
    t_lo = (1 - s_hi) / a
    t_hi = (1 - s_lo) / a
    return t_lo, t_hi, float((1 - math.sqrt(float(disc))) / float(a))


def cos_plus_sin_from_tangent(t: F) -> float:
    return float((1 + t) / (1 + t * t) ** 0.5)


def inscribed_axis_side_exceeds(t: F, target: F) -> bool:
    """1/(cos+sin) > target  <=>  (1+t^2) > target^2 (1+t)^2  (t = tan theta >= 0)."""
    return (1 + t * t) > target * target * (1 + t) ** 2


def main() -> None:
    U = F(3877084, 1000000)  # rational upper bound of Trump's side
    q = F(96, 25)
    for name, L in (("q = 96/25", q), ("U (rational cover 3.877084)", U), ("3.82", F(382, 100)), ("3.81", F(381, 100))):
        t_lo, t_hi, t_f = theta0_tangent(L)
        print(f"{name}: L/4 = {float(L/4):.6f}; theta0 = {math.degrees(math.atan(t_f)):.5f} deg, tan theta0 in [{float(t_lo):.9f}, {float(t_hi):.9f}]")
    # The 1/24 band at q: inscribed axis-parallel side = sqrt(577)/25 vs q/4 = 24/25.
    t = F(1, 24)
    print("at q: tan theta = 1/24 gives inscribed side^2 =", (1 + t * t) / (1 + t) ** 2, "=", float(((1 + t * t) / (1 + t) ** 2) ** 0.5), "> 0.96:", inscribed_axis_side_exceeds(t, q / 4))
    print("   cos+sin at 1/24 =", cos_plus_sin_from_tangent(t), "vs 4/q =", float(4 / q))
    # Largest rational-friendly tangent bands below theta0(q): 1/23? 1/23.5?
    for d in (24, 23, 22):
        t = F(1, d)
        print(f"   tan theta = 1/{d}: inscribed side > q/4: {inscribed_axis_side_exceeds(t, q/4)}, theta = {math.degrees(math.atan(1/d)):.4f} deg")
    # Sharpness of the pitch-L/4 grid: the open unit square tilted by theta with
    # tan theta = t, centred at the centre of a grid cell (3L/8, 3L/8) relative offsets
    # (+-L/8, +-L/8), avoids the four cell corners iff (L/8)(cos+sin) >= 1/2, i.e.
    # cos+sin >= 4/L, i.e. theta >= theta0.  Check the other five grid points too.
    for name, L in (("q", q), ("U", U)):
        t_lo, t_hi, t_f = theta0_tangent(L)
        th = math.atan(t_f) + 1e-9
        c, s = math.cos(th), math.sin(th)
        p = float(L) / 4
        cx = cy = 1.5 * p
        worst = 0.0
        for i in (1, 2, 3):
            for j in (1, 2, 3):
                dx, dy = i * p - cx, j * p - cy
                u = dx * c + dy * s
                v = -dx * s + dy * c
                worst = max(worst, 0.5 - max(abs(u), abs(v)))  # >0 means strictly inside
        print(f"sharpness at {name}: square tilted by theta0+1e-9 rad centred at (3L/8,3L/8): max interior depth over the 9 grid points = {worst:.3e} (<=0 means avoids all nine)")
    # Theorem-3 transfer at q (review's endpoint-neighbourhood argument, redone at 3.84):
    # if every folded angle is within delta of 0 or 45, concentric b-cores at the exact
    # axis/diagonal exist for b R(delta) <= 1 with R = cos delta + sin delta; scaled by 1/b
    # they are unit 0/45 squares in side q/b, which needs q/b >= L0 = 2 + 4 sqrt2 / 3.
    L0 = 2 + 4 * math.sqrt(2) / 3
    for name, L in (("q", q), ("U", U), ("3.86", F(386, 100)), ("3.87", F(387, 100))):
        b = float(L) / L0  # the largest shrink allowed: q/b < L0 forbids; need b > q/L0
        R = 1 / b
        # cos d + sin d = R -> sin(d + 45) = R / sqrt2
        d = math.degrees(math.asin(R / math.sqrt(2)) - math.pi / 4)
        print(f"Theorem-3 transfer at {name}: not all eleven within delta = {d:.4f} deg of {{0,45}} (L0 = {L0:.6f}, b = {b:.6f})")
    # H-036-style statement is different: it asks for side >= 3.878 for all-within-0.25-deg;
    # the transfer above gives side >= q for all-within-delta(q).
    # Band widths available for a band around 40.18 deg via Trump: the tilted squares
    # of Trump's packing are at 40.181937 deg; the folded net index 159 is at:
    limit = F(207107, 500000)
    for i in (149, 155, 158, 159, 160, 163, 169, 170, 179, 180):
        print(f"net index {i}: angle {math.degrees(2*math.atan(float(limit)*i/180)):.4f} deg")


if __name__ == "__main__":
    main()
```

### `nine_points.py`

```text
"""Exact test of candidate nine-point sets: the widest leading-k cell class they pierce.

For a nine-atom unit-weight measure, decide_class_program's Condition 5' for the class
of the leading k cells says every admissible B-core at a class direction covers at least
one atom (mass >= 1).  Since the cores of a packing are pairwise disjoint, at most nine
squares can then have folded angle in the closed range of those k cells.
"""
import sys, math
sys.path.insert(0, '/tmp/claude-0/-home-user-squares/9010767e-5bb7-5e7d-99d2-858400f3969a/scratchpad')
from fractions import Fraction
from angle_bands import load_net, deg
from sqpack.project import require_project_root
from sqpack.fractional.model import Atom
from sqpack.fractional.classcert import DirectionClasses, class_minima, Composition
root = require_project_root(); ht, B = load_net(root)

def nine(side: Fraction, delta: Fraction):
    xs = (1 - delta, side / 2, side - 1 + delta)
    return tuple(Atom(f"{i}{j}", xs[i], xs[j], Fraction(1)) for i in range(3) for j in range(3))

def widest(side, atoms):
    # largest k with min mass >= 1 over cells 0..k-1 (monotone in k)
    best = 0
    for k in range(1, 61):
        classes = DirectionClasses(ht, frozenset(range(k)))
        minima = class_minima(atoms, classes, Composition(11, 0), side, B)
        m = minima[0].mass
        if m is not None and m >= 1:
            best = k
        else:
            break
    return best

for side_name, side in (("q=96/25", Fraction(96, 25)), ("U~3.877084", Fraction(3877084, 1000000))):
    for delta in (Fraction(0), Fraction(1, 200), Fraction(1, 100), Fraction(1, 50), Fraction(1, 25), Fraction(3, 50), Fraction(2, 25), Fraction(1, 10), Fraction(3, 25)):
        atoms = nine(side, delta)
        k = widest(side, atoms)
        classes = DirectionClasses(ht, frozenset(range(max(k, 1))))
        upper = deg(classes.cell_bounds(k - 1)[1]) if k else 0.0
        print(f"{side_name}: corners at 1-{float(delta):.3f} and L-1+{float(delta):.3f}, middle L/2: pierces leading {k} cells, i.e. folded tilt <= {upper:.4f} deg", flush=True)
    # the L/4 grid control
    q = side / 4
    grid_atoms = tuple(Atom(f"{i}{j}", q * i, q * j, Fraction(1)) for i in (1, 2, 3) for j in (1, 2, 3))
    k = widest(side, grid_atoms)
    print(f"{side_name}: L/4 grid control pierces leading {k} cells (<= {deg(DirectionClasses(ht, frozenset(range(k))).cell_bounds(k-1)[1]):.4f} deg)", flush=True)
```

### `angle_bands.py`

```text
"""Band counts and composition split with the repository's class-certificate instrument.

For a class Theta (a union of half-gap cells of the retained 181-direction net) and the
composition (11, 0), the class program's optimum M (rescaled to w0 = 1) is the covering
value restricted to Theta: a D4-symmetric measure of mass M every admissible B-core at a
direction in Theta covers with mass >= 1. Since the cores of a packing are pairwise
disjoint, the number of squares whose folded angle lies in Theta is at most floor(M)
whenever the exact decision holds. Nothing here is retained; the exact decision
(decide_class_program on the rationalised atoms) is what makes a bound a theorem.

Usage (from packing/, with the scratchpad venv):
    python angle_bands.py bands  <side> <grid> <out.jsonl>
    python angle_bands.py split  <side> <grid> <near_cells> <out.jsonl>
"""

from __future__ import annotations

import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

from sqpack.fractional.classcert import (
    NEAR,
    ClassRoundTiming,
    ClassThresholds,
    Composition,
    DirectionClasses,
    decide_class_program,
    solve_class_program,
    within_nine_point_tilt,
)
from sqpack.fractional.generate import build_site_grid, net_half_tangents, rationalise
from sqpack.project import require_project_root

NET_SOURCE = Path("cases/n11_fractional_certificate/certificate.json")


def load_net(root: Path):
    spec = json.loads((root / NET_SOURCE).read_text())
    limit = Fraction(spec["angle_limit"])
    steps = int(spec["direction_steps"])
    return net_half_tangents(limit, steps), Fraction(spec["square_side"])


def deg(t: Fraction) -> float:
    return math.degrees(math.atan(float(t)))


def run_class(
    half_tangents, shrink, side: Fraction, cells: frozenset[int], composition: Composition,
    *, grid_count: int, inset: Fraction, scale: int = 4096, max_rounds: int = 80,
) -> dict:
    classes = DirectionClasses(half_tangents, cells)
    grid = build_site_grid(side, grid_count, inset)
    timings: list[ClassRoundTiming] = []
    started = time.perf_counter()
    weights, log = solve_class_program(
        grid, shrink, classes, composition, timings=timings, max_rounds=max_rounds
    )
    elapsed = time.perf_counter() - started
    w0, w1 = log.thresholds
    lo = min(cells)
    hi = max(cells)
    b_lo, b_hi = classes.cell_bounds(lo)[0], classes.cell_bounds(hi)[1]
    record = {
        "side": str(side),
        "grid": grid_count,
        "inset": str(inset),
        "cells": f"{lo}..{hi}" if len(cells) == hi - lo + 1 else sorted(cells),
        "ncells": len(cells),
        "class_deg": [round(deg(b_lo), 4), round(deg(b_hi), 4)],
        "composition": [composition.near, composition.tilted],
        "stopped": log.stopped,
        "rounds": log.rounds,
        "rows": log.rows,
        "w0": w0,
        "w1": w1,
        "M": log.objective,
        "required": log.required,
        "margin": log.margin,
        "seconds": round(elapsed, 2),
    }
    if composition.tilted == 0 and w0 > 0:
        record["M_at_w0_1"] = log.objective / w0
    if composition.near == 0 and w1 > 0:
        record["M_at_w1_1"] = log.objective / w1
    # Exact decision when the float search refutes.
    if log.converged and log.margin < -1e-6 and w0 > 0:
        atoms = rationalise(grid, weights / w0, scale=scale)
        ratio = Fraction(w1 / w0).limit_denominator(10**6) if composition.tilted else Fraction(0)
        # Round the tilted threshold DOWN so Condition 5' for class 1 stays valid.
        ratio = Fraction(math.floor(ratio * scale), scale)
        thresholds = ClassThresholds(Fraction(1), ratio)
        verdict = decide_class_program(
            atoms, side, shrink, classes, composition, thresholds=thresholds
        )
        record["exact"] = {
            "atoms": len(atoms),
            "M": str(verdict.total_mass),
            "M_float": float(verdict.total_mass),
            "required": str(verdict.required),
            "margin": str(verdict.margin),
            "refutes": verdict.refutes,
            "failures": list(verdict.failures),
            "minima": [
                (m.label, str(m.mass), m.direction) for m in verdict.minima if m.mass is not None
            ],
        }
    elif composition.tilted == 0 and log.converged and w0 > 0:
        # Not a refutation of (11,0), but floor(M) may still be a useful count bound
        # below eleven: decide the exact value at w0 = 1 and report floor.
        atoms = rationalise(grid, weights / w0, scale=scale)
        verdict = decide_class_program(
            atoms, side, shrink, classes, composition, thresholds=ClassThresholds(Fraction(1), Fraction(0))
        )
        record["exact"] = {
            "atoms": len(atoms),
            "M": str(verdict.total_mass),
            "M_float": float(verdict.total_mass),
            "conditions_hold": all(c.holds for c in verdict.conditions if not c.name.startswith("Condition 2'")),
            "failures": list(verdict.failures),
            "minima": [
                (m.label, str(m.mass), m.direction) for m in verdict.minima if m.mass is not None
            ],
        }
    return record


def band_list(half_tangents) -> list[tuple[str, frozenset[int]]]:
    n = len(half_tangents)  # 181 cells, index 159 ~ 40.19 deg
    bands: list[tuple[str, frozenset[int]]] = []
    for k in (6, 10, 13, 16, 19, 22, 25, 30, 35, 40, 50, 60):
        bands.append((f"near-axis leading {k}", frozenset(range(k))))
    for k in (1, 3, 6, 10, 19, 30, 40):
        bands.append((f"near-45 trailing {k}", frozenset(range(n - k, n))))
    for k in (0, 2, 5, 10, 15, 20, 30):
        bands.append((f"Trump band 159+-{k}", frozenset(range(159 - k, min(n, 159 + k + 1)))))
    for i0, name in ((38, "tilt >= 10 deg"), (77, "tilt >= 20 deg"), (117, "tilt >= 30 deg"), (140, "tilt >= 35.5 deg")):
        bands.append((name, frozenset(range(i0, n))))
    for k in (1, 6, 13, 19, 30, 40):
        bands.append((f"end cells leading {k} + trailing {k}", frozenset(range(k)) | frozenset(range(n - k, n))))
    bands.append(("mid band 10..30 deg", frozenset(range(38, 117))))
    bands.append(("all but Trump band 159+-10", frozenset(range(n)) - frozenset(range(149, 170))))
    bands.append(("all but Trump band 159+-20", frozenset(range(n)) - frozenset(range(139, 180))))
    bands.append(("all 181 cells (unconditional)", frozenset(range(n))))
    return bands


def main() -> None:
    mode = sys.argv[1]
    side = Fraction(sys.argv[2])
    grid_count = int(sys.argv[3])
    root = require_project_root()
    half_tangents, shrink = load_net(root)
    inset = Fraction(1, 10)
    if mode == "bands":
        out = Path(sys.argv[4])
        with out.open("a") as handle:
            for name, cells in band_list(half_tangents):
                try:
                    record = run_class(
                        half_tangents, shrink, side, cells, Composition(11, 0),
                        grid_count=grid_count, inset=inset,
                    )
                except Exception as error:  # noqa: BLE001
                    record = {"name": name, "error": repr(error)}
                record["name"] = name
                handle.write(json.dumps(record) + "\n")
                handle.flush()
                m = record.get("M_at_w0_1", float("nan"))
                ex = record.get("exact", {})
                print(
                    f"{name:42s} side {float(side):.6f} grid {grid_count} cells {record.get('ncells')} "
                    f"{record.get('class_deg')} M/w0={m:.4f} exact={ex.get('M_float')} "
                    f"failures={ex.get('failures')} {record.get('seconds')}s {record.get('stopped')}",
                    flush=True,
                )
    elif mode == "split":
        near_cells = int(sys.argv[4])
        out = Path(sys.argv[5])
        cells = frozenset(range(near_cells))
        classes = DirectionClasses(half_tangents, cells)
        inside = within_nine_point_tilt(classes, side, shrink)
        print(f"near class leading {near_cells} cells inside nine-point tilt at B: {inside}", flush=True)
        with out.open("a") as handle:
            for n0 in range(0, 12):
                composition = Composition(n0, 11 - n0)
                try:
                    record = run_class(
                        half_tangents, shrink, side, cells, composition,
                        grid_count=grid_count, inset=inset,
                    )
                except Exception as error:  # noqa: BLE001
                    record = {"error": repr(error), "composition": [n0, 11 - n0]}
                record["name"] = f"split near={near_cells} cells composition ({n0},{11-n0})"
                handle.write(json.dumps(record) + "\n")
                handle.flush()
                ex = record.get("exact", {})
                print(
                    f"({n0:2d},{11-n0:2d}) side {float(side):.6f} grid {grid_count} "
                    f"w0={record.get('w0')} w1={record.get('w1')} M={record.get('M')} "
                    f"margin={record.get('margin')} exact_refutes={ex.get('refutes')} "
                    f"{record.get('seconds')}s {record.get('stopped')}",
                    flush=True,
                )


if __name__ == "__main__":
    main()
```

### `rerun_bands.py`

```text
"""Re-run selected bands with a larger round cap and ALWAYS exact-decide the point reached.

The exact sweep decides Condition 5' over every placement of every class direction, so a
point that the float loop did not certify as converged can still be a valid certificate
(the loop's rows are only a subset of placements; the sweep is complete).
"""
import json, sys, math, time
sys.path.insert(0, '/tmp/claude-0/-home-user-squares/9010767e-5bb7-5e7d-99d2-858400f3969a/scratchpad')
from fractions import Fraction
from pathlib import Path
from angle_bands import load_net, deg
from sqpack.project import require_project_root
from sqpack.fractional.generate import build_site_grid, rationalise
from sqpack.fractional.classcert import (DirectionClasses, Composition, ClassThresholds,
    solve_class_program, decide_class_program)

root = require_project_root(); ht, B = load_net(root)
side = Fraction(sys.argv[1]); grid_count = int(sys.argv[2]); rounds = int(sys.argv[3]); out = Path(sys.argv[4])
specs = sys.argv[5:]   # each "name:lo-hi" or "name:lo-hi,lo-hi"
n = len(ht)
with out.open('a') as handle:
    for spec in specs:
        name, ranges = spec.split(':')
        cells = set()
        for r in ranges.split(','):
            lo, hi = r.split('-'); cells |= set(range(int(lo), int(hi) + 1))
        cells = frozenset(cells)
        classes = DirectionClasses(ht, cells)
        grid = build_site_grid(side, grid_count, Fraction(1, 10))
        t0 = time.perf_counter()
        w, log = solve_class_program(grid, B, classes, Composition(11, 0), max_rounds=rounds)
        el = time.perf_counter() - t0
        rec = {"name": name, "side": str(side), "grid": grid_count, "cells": sorted(cells)[0:1] + sorted(cells)[-1:], "ncells": len(cells),
               "M_at_w0_1": log.objective / log.thresholds[0] if log.thresholds[0] > 0 else None,
               "rounds": log.rounds, "stopped": log.stopped, "seconds": round(el, 1)}
        if log.thresholds[0] > 0:
            atoms = rationalise(grid, w / log.thresholds[0], scale=4096)
            v = decide_class_program(atoms, side, B, classes, Composition(11, 0), thresholds=ClassThresholds(Fraction(1), Fraction(0)))
            rec["exact"] = {"atoms": len(atoms), "M": str(v.total_mass), "M_float": float(v.total_mass),
                            "failures": list(v.failures), "minima": [(m.label, str(m.mass), float(m.mass), m.direction) for m in v.minima if m.mass is not None]}
        handle.write(json.dumps(rec) + "\n"); handle.flush()
        ex = rec.get("exact", {})
        print(f"{name:40s} side {float(side):.6f} grid {grid_count} ncells {len(cells)} M/w0={rec['M_at_w0_1']} exact={ex.get('M_float')} failures={ex.get('failures')} minima={ex.get('minima')} rounds={log.rounds} {rec['seconds']}s {log.stopped}", flush=True)
```

### `split_sel.py`

```text
"""Composition split at one side for selected compositions, near class = leading K cells."""
import json, sys, time
sys.path.insert(0, '/tmp/claude-0/-home-user-squares/9010767e-5bb7-5e7d-99d2-858400f3969a/scratchpad')
from fractions import Fraction
from pathlib import Path
from angle_bands import load_net, run_class
from sqpack.project import require_project_root
from sqpack.fractional.classcert import Composition, DirectionClasses, within_nine_point_tilt
root = require_project_root(); ht, B = load_net(root)
side = Fraction(sys.argv[1]); grid = int(sys.argv[2]); K = int(sys.argv[3]); rounds = int(sys.argv[4]); out = Path(sys.argv[5])
comps = [int(c) for c in sys.argv[6].split(',')]
cells = frozenset(range(K))
print(f"near class = leading {K} cells; inside nine-point tilt at B: {within_nine_point_tilt(DirectionClasses(ht, cells), side, B)}", flush=True)
with out.open('a') as h:
    for n0 in comps:
        comp = Composition(n0, 11 - n0)
        rec = run_class(ht, B, side, cells, comp, grid_count=grid, inset=Fraction(1, 10), max_rounds=rounds)
        rec['name'] = f'split K={K} ({n0},{11-n0})'
        h.write(json.dumps(rec) + '\n'); h.flush()
        ex = rec.get('exact', {})
        print(f"({n0:2d},{11-n0:2d}) side {float(side):.6f} grid {grid} K {K}: w0={rec['w0']:.6f} w1={rec['w1']:.6f} M={rec['M']:.6f} required={rec['required']:.6f} margin={rec['margin']:+.6f} M/w0={rec['M']/rec['w0'] if rec['w0']>0 else float('nan'):.4f} exact_refutes={ex.get('refutes')} exact_M={ex.get('M_float')} rounds={rec['rounds']} {rec['seconds']}s {rec['stopped']}", flush=True)
```

### `fixed_angle_packing.py`

```text
"""Lower bounds on the fixed-angle packing number P(theta, L): the largest number of
pairwise interior-disjoint unit squares, all at the same orientation theta, inside
[0, L]^2.  P(theta, L) is a lower bound on the (integral and fractional) piercing number
of every angle band containing theta, hence on any class-program optimum for such a
band: no piercing set with fewer than P(theta, L) points, and no class certificate with
M < P(theta, L), can exist for a band containing theta.

Method: work in the frame rotated by -theta, where the squares are axis-parallel and the
container is a rotated square. Candidate lower-left corners on a grid of pitch h; two
candidates conflict iff their half-open squares [x,x+1) x [y,y+1) meet, which for
grid-aligned candidates is exact. Maximise the count by a MILP (HiGHS via scipy) with
clique rows at grid points. Any feasible solution is an actual packing (rigorous lower
bound); optimality is only over the grid.
"""

from __future__ import annotations

import math
import sys

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


def container_halfplanes(L: float, theta: float):
    """Half-planes (a, b, c): a x + b y <= c describing the container in the rotated frame.

    A point (x, y) in the rotated frame maps to the original frame by rotation by theta;
    the container is 0 <= X <= L, 0 <= Y <= L with X = c x - s y, Y = s x + c y.
    """
    c, s = math.cos(theta), math.sin(theta)
    return [(-c, s, 0.0), (c, -s, L), (-s, -c, 0.0), (s, c, L)]


def square_fits(x: float, y: float, planes, eps=1e-12) -> bool:
    for (a, b, cc) in planes:
        for dx in (0.0, 1.0):
            for dy in (0.0, 1.0):
                if a * (x + dx) + b * (y + dy) > cc + eps:
                    return False
    return True


def packing_number_lower_bound(L: float, theta_deg: float, pitch: float, time_limit: float = 60.0):
    theta = math.radians(theta_deg)
    planes = container_halfplanes(L, theta)
    # Bounding box of the rotated container in the rotated frame.
    c, s = math.cos(theta), math.sin(theta)
    corners = [(0, 0), (L, 0), (L, L), (0, L)]
    xs = [c * X + s * Y for X, Y in corners]
    ys = [-s * X + c * Y for X, Y in corners]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    nx = int(math.floor((x1 - x0 - 1) / pitch)) + 1
    ny = int(math.floor((y1 - y0 - 1) / pitch)) + 1
    cands = []
    for i in range(nx + 1):
        for j in range(ny + 1):
            x, y = x0 + i * pitch, y0 + j * pitch
            if square_fits(x, y, planes):
                cands.append((i, j))
    if not cands:
        return 0, []
    index = {cij: k for k, cij in enumerate(cands)}
    m = int(round(1 / pitch))  # squares span m grid steps
    # Clique constraints: for each grid point (i, j), the squares covering it half-open
    # are those with corner (i - a, j - b), 0 <= a, b < m.
    rows = {}
    for (i, j) in cands:
        for a in range(m):
            for b in range(m):
                rows.setdefault((i + a, j + b), []).append(index[(i, j)])
    A = lil_matrix((len(rows), len(cands)))
    for r, (pt, members) in enumerate(rows.items()):
        for k in members:
            A[r, k] = 1.0
    cons = LinearConstraint(A.tocsr(), -np.inf, 1.0)
    res = milp(
        c=-np.ones(len(cands)),
        constraints=[cons],
        integrality=np.ones(len(cands)),
        bounds=Bounds(0, 1),
        options={"time_limit": time_limit, "disp": False},
    )
    if res.x is None:
        return 0, []
    chosen = [cands[k] for k in range(len(cands)) if res.x[k] > 0.5]
    placed = [(x0 + i * pitch, y0 + j * pitch) for i, j in chosen]
    # Rigorous re-check of disjointness and containment in floats with margin.
    for (xa, ya) in placed:
        assert square_fits(xa, ya, planes, eps=1e-9)
    for p in range(len(placed)):
        for q in range(p + 1, len(placed)):
            xa, ya = placed[p]
            xb, yb = placed[q]
            assert abs(xa - xb) >= 1 - 1e-9 or abs(ya - yb) >= 1 - 1e-9, (placed[p], placed[q])
    return len(placed), placed


def main() -> None:
    L_list = [3.84, 3.877084]
    angles = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.181937, 42.0, 45.0]
    pitch = float(sys.argv[1]) if len(sys.argv) > 1 else 0.05
    for L in L_list:
        for th in angles:
            n, placed = packing_number_lower_bound(L, th, pitch, time_limit=90.0)
            print(f"L = {L:.6f} theta = {th:9.6f} deg pitch {pitch}: P >= {n}", flush=True)


if __name__ == "__main__":
    main()
```

### `pocket.py`

```text
"""Feasible orientation set of a unit square confined to an idealized pocket.

Pocket H(wh, wd): the hexagon  |Y| <= wh/2,  |X+Y| <= wd/sqrt2,  |X-Y| <= wd/sqrt2.
Its supporting lines have normals at 90, 45 and 135 degrees: the kind of boundary that
walls / axis-aligned squares (horizontal edges) and 45-degree squares (diagonal edges)
present.  A unit square at orientation theta fits into H iff some translation puts its
four corners in H; for fixed theta this is a linear feasibility problem in the centre.

Claim checked: for wh, wd in (sqrt2 cos(22.5 deg), sqrt2) = (1.3066, 1.4142) the feasible
set is a closed interval of folded angles contained in the OPEN interval (0, 45): the
square can sit at 22.5 degrees but at neither 0 nor 45 degrees, i.e. at neither of the
orientation classes its confining features belong to.  Widths are necessary conditions;
the LP shows they are also sufficient here.

This is an idealized region.  Whether such a pocket can be the free region of a genuine
packing of unit squares at 0 and 45 degrees only is NOT established here (the natural
four-corner-diamond octagon cannot: see the report).
"""

from __future__ import annotations

import math

import numpy as np
from scipy.optimize import linprog

R2 = math.sqrt(2)


def hexagon(wh: float, wd: float):
    d = wd / R2
    return [
        (0.0, -1.0, wh / 2), (0.0, 1.0, wh / 2),
        (-1.0, -1.0, d), (1.0, 1.0, d),
        (1.0, -1.0, d), (-1.0, 1.0, d),
    ]


def fits(rows, theta_deg: float, margin: float = 0.0) -> bool:
    th = math.radians(theta_deg)
    c, s = math.cos(th), math.sin(th)
    corners = [(0.5 * (dx * c - dy * s), 0.5 * (dx * s + dy * c)) for dx in (-1, 1) for dy in (-1, 1)]
    A, b = [], []
    for (a, bb, cc) in rows:
        for (px, py) in corners:
            A.append([a, bb])
            b.append(cc - (a * px + bb * py) - margin)
    res = linprog(c=[0, 0], A_ub=np.array(A), b_ub=np.array(b), bounds=[(None, None)] * 2, method="highs")
    return res.status == 0


def main() -> None:
    for wh, wd in ((1.36, 1.36), (1.32, 1.40), (1.40, 1.32), (1.31, 1.31), (1.42, 1.36), (1.36, 1.42)):
        rows = hexagon(wh, wd)
        feas = [th for th in np.arange(0.0, 90.0001, 0.1) if fits(rows, th)]
        lo, hi = (round(min(feas), 2), round(max(feas), 2)) if feas else (None, None)
        # predicted interval from the two width conditions:
        ta = math.degrees(math.acos(min(1.0, wd / R2)))          # sqrt2 cos theta <= wd  -> theta >= ta
        tb = math.degrees(math.asin(min(1.0, wh / R2))) - 45.0   # sqrt2 sin(theta+45) <= wh -> theta <= tb
        print(f"wh={wh} wd={wd}: LP feasible folded angles = [{lo}, {hi}] deg;"
              f" width prediction [{ta:.2f}, {tb:.2f}] (folded);  theta=0 fits {fits(rows,0)}, theta=45 fits {fits(rows,45)}")


if __name__ == "__main__":
    main()
```

## Session-102 — angle-band theorems at 96/25 (2026-09-08)

Lane BC-295 of
[Agenda 030](../../../../agendas/agenda-030-parallel-structural-lanes-at-n11.md) under
[H-130](../../../../hypotheses/H-130-robust-end-band-theorem-at-q.md) and
[H-131](../../../../hypotheses/H-131-near-axis-counts-at-q.md), bead `think-ndqj`,
session record
[session-102](../../../../agent-sessions/session-102-angle-band-theorems-at-q.md).
The planning report above is left as delivered; this section is the registered replay of
its Section 2.3 decisions and the widening of its Theorem 1.11. Everything called a
verdict below is `decide_class_program` on rationalised atoms with exact thresholds
`(1, 0)` for the composition `(11, 0)`; the float optimum of `solve_class_program` is
context only.
Wall times were measured on one worker (`PACK_JOBS=1`, `OMP_NUM_THREADS=1`)
of a four-core machine shared with five other agents, so they are not comparable with
the planning lane’s.

**Question.** How wide a band around `0°` and `45°` can be excluded at `96/25`, decided
exactly; do the planning lane’s counts (H-131) replay under a registered round; and
where does the fractional obstruction live in angle once the band toward `40.19°` stays
at or above eleven.

**Inputs, fixed for every run.** Side `q = 96/25` (and `3877084/10⁶ ≥ U` for the three
`U` rows of H-131); shrink `B = 9977/10000`; the retained 181-direction net
(`cases/n11_fractional_certificate/certificate.json`: half-tangent limit
`207107/500000`, 180 equal steps, cell width about `0.264°` at the axis end and `0.225°`
at the diagonal end); site set `build_site_grid(side, 79, 1/10)` — the `79 × 79` product
grid inset `1/10` from the walls, folded into `D4` orbits (`6241` sites, `820` orbits);
composition `(11, 0)`; `rows_per_direction = 3`; the row loop capped at a hundred rounds
and the point reached decided regardless of convergence (the exact sweep is complete;
the loop’s rows are a subset of placements); rationalisation at scale `4096` with the
standard bump `1 + 10⁻⁶`; exact thresholds `(1, 0)`. A class is a union of half-gap
cells and its folded range is the closed union of the cells’ exact-tangent bounds
(`DirectionClasses.cell_bounds`), so every band below is stated with closed ends.
Legal touching is retained throughout: a square’s `B`-core lies in its open interior
(Condition 4), so the cores of a packing are pairwise disjoint even where squares touch.

**Falsifiers, stated before the runs.** For a count class `Θ` with claimed bound “at
most `N`”: the exact sweep reports a core of mass below one at some direction of `Θ`, or
the exact mass reaches `N + 1`, or `N + 1` pairwise disjoint `B`-cores at directions in
`Θ` fit in `[0, 96/25]²`. For the end band `[0°, α] ∪ [45° − β, 45°]`: a fractional
packing on the end cells of value at least eleven at `96/25`, or eleven pairwise
disjoint `B`-cores at end-cell directions in the container.
A non-refutation on grid 79 is neither; it is a site-set reading and is labelled as
such. For the nine-point control: an admissible `B`-core at a direction of the leading
eighteen cells that misses all nine atoms.

### The registered replay (H-131 and the Section 2.3 end bands)

Every row is one `solve_class_program` search on the site set above followed by
`decide_class_program` on the rationalised point reached; “least core” is the exact
least covered mass over every direction of the class (Condition 5′), “conditions” lists
the failures among Conditions 1, 3, 4 and 5′ (Condition 2′ is the `(11, 0)` refutation
itself and is reported in the last column).
The count bound is `⌊M⌋` whenever Condition 5′ holds, by Theorem 1.5’s counting step.

| class (cells) | folded range, closed | side | rounds | float `M` | exact `M` | least core | count | planning lane | wall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0–24 | `[0°, 6.4537°]` | `96/25` | 9, converged | 9.0000 | `4611/512 = 9.00586` | `2049/2048` | **≤ 9** | `9.00586` | 3 s |
| 0–39 | `[0°, 10.3875°]` | `96/25` | 14, converged | 10.5000 | `10765/1024 = 10.51270` | `1025/1024` | **≤ 10** | `10.51270` | 6 s |
| 171–180 | `[42.8453°, 45°]` | `96/25` | 100, cap | 9.6938 | `9989/1024 = 9.75488` | `2053/2048` | **≤ 9** | `9.75488` | 67 s |
| 149–169 | `[37.7333°, 42.6166°]` | `96/25` | 100, cap | 9.9457 | `41529/4096 = 10.13892` | `1037/1024` | **≤ 10** | `10.13892` | 596 s |
| 117–180 | `[30.0149°, 45°]` | `96/25` | 60, converged | 10.2309 | `42589/4096 = 10.39771` | `4147/4096` | **≤ 10** | `10.39771` | 1149 s |
| 0–5 | `[0°, 1.4503°]` | `96/25` | 12, converged | 9.0000 | `2305/256 = 9.00391` | `4097/4096` | **≤ 9** | `9.00391` | 1 s |
| 175–180 | `[43.7565°, 45°]` | `96/25` | 100, cap | 9.6277 | `9925/1024 = 9.69238` | `1021/1024` at 175 | undecided (5′ fails) | float only | 24 s |
| 0–5 ∪ 175–180 | `[0°, 1.4503°] ∪ [43.7565°, 45°]` | `96/25` | 29, converged | 10.6866 | `10959/1024 = 10.70215` | `1025/1024` | **refutes `(11, 0)`** | `10.70215` | 5 s |
| 0–24 | `[0°, 6.4537°]` | `3877084/10⁶` | 17, converged | 9.8125 | `10065/1024 = 9.82910` | `4101/4096` | **≤ 9** | `9.82910` | 6 s |
| 0–29 | `[0°, 7.7671°]` | `3877084/10⁶` | 7, converged | 10.0000 | `10243/1024 = 10.00293` | `4097/4096` | **≤ 10** | `10.00293` | 4 s |
| 175–180 | `[43.7565°, 45°]` | `3877084/10⁶` | 63, converged | 10.1379 | `5201/512 = 10.15820` | `2051/2048` | **≤ 10** | `10.15820` | 9 s |

Every exact mass reproduces the planning lane’s to the fraction, on the same inputs; no
falsifier occurred. The one row that stays undecided, the six trailing cells alone at
`96/25`, was float-only in the planning lane too, and the count it would give is implied
by the trailing-ten row (`[43.7565°, 45°] ⊂ [42.8453°, 45°]`, so at most nine there as
well). So H-131’s list is now decided under this record: at `96/25` at most nine squares
within `6.4537°` of the axes, at most ten within `10.3875°`, at most nine within
`2.1547°` of `45°`, at most ten within `±2.44°` of `40.194°` (the class
`[37.7333°, 42.6166°]`), and at most ten with folded tilt in `[30.0149°, 45°]`; at `U`
at most nine within `6.4537°`, ten within `7.7671°`, and ten within `1.2435°` of `45°`.
The site set in every case is the `79 × 79` inset-`1/10` grid, and the rationalised
atoms are reproducible from the scripts in the appendix (`replay.jsonl` in the session
scratchpad holds each verdict with its conditions and minima).

### The band theorems this decides

Both statements are theorems of the exact verifier on the stated site set
(EXACT-VERIFIED in the planning report’s vocabulary); the atoms are reproducible from
the appendix and each verdict is in the scratchpad log with its conditions.
Both are frozen claims that need an experiment id (none is allocated here).

**Theorem A (the exit band; cells `0–6 ∪ 174–180`).** No packing of eleven unit squares
in `[0, 96/25]²` has every folded angle in `[0°, 1.7139°] ∪ [43.5293°, 45°]` — exactly,
the closed set of angles whose tangent lies in `[0, 40385865000000/1349699746833857] ∪
[1077991935000000/1134804266494367, 1]`. Equivalently every packing of eleven at side at
most `3.84` has a square whose folded angle lies in `(1.7139°, 43.5293°)`, farther than
`1.7139°` from `0°` and than `1.4707°` from `45°`; `α + β = 3.1846° ≥ 3°`, which is
H-130’s criterion.

*Proof.* The composition-`(11, 0)` class program on the `79 × 79` inset-`1/10` grid
converged in 49 rounds; its rationalised measure (152 atoms, `D4`-closed) has total mass
`5529/512 = 10.798828125`, the exact event-cell sweep reports least covered mass
`4099/4096 ≥ 1` on every one of the fourteen class directions, and Conditions 3 and 4
hold for the net (`B(1 + D) = 899996306539/900000000000 < 1`). Each square of a packing
contains its closed `B`-core at the net direction whose cell holds its angle; if all
eleven angles lay in the class, eleven pairwise disjoint cores would each carry mass at
least one, total at least eleven, against `10.7988`. ∎

**Theorem B (the widest band decided here; cells `0–39 ∪ 174–180`).** No packing of
eleven unit squares in `[0, 96/25]²` has every folded angle in
`[0°, 10.3875°] ∪ [43.5293°, 45°]` — tangent in `[0, 12271089750000/66942386977163] ∪
[1077991935000000/1134804266494367, 1]`. Equivalently every packing of eleven at side at
most `3.84` has a square whose folded angle lies in `(10.3875°, 43.5293°)`, and so, with
Theorem 1.12, a square with folded tilt in `(10.3875°, 43.5293°)` and a square with
folded tilt below `30.0149°` (possibly the same square).
Here `α + β = 11.8582°`.

*Proof.* The same program converged in 41 rounds; the rationalised measure (216 atoms)
has mass `351/32 = 10.96875`, least covered core `4101/4096` over the forty-seven class
directions, Conditions 1, 3, 4 hold; eleven disjoint cores in the class are impossible.
∎

Theorem B contains Theorem A and every `(a, 7)` row of the table; Theorem A is kept as
the statement H-130 asked for, with its own smaller certificate.
Neither theorem uses Stromquist’s Theorem 3 or its lemmas 7–8. Trump’s packing (six
squares at `0°`, five at `40.18°`) satisfies both with room, as it must: its five tilted
squares lie in `(10.39°, 43.53°)`.

**Theorem C (the widest band decided here, grid 119; cells `0–39 ∪ 172–180`).** No
packing of eleven unit squares in `[0, 96/25]²` has every folded angle in
`[0°, 10.3875°] ∪ [43.0737°, 45°]` — tangent in `[0, 12271089750000/66942386977163] ∪
[177594252500000/189956166180167, 1]`. Equivalently every packing of eleven at side at
most `3.84` has a square whose folded angle lies in `(10.3875°, 43.0737°)`;
`α + β = 12.3138°`.

*Proof.* The same program on `build_site_grid(96/25, 119, 1/10)` converged in 81 rounds;
the rationalised measure (296 atoms) has mass `11083/1024 = 10.8232421875`, least
covered core `4101/4096` over the forty-nine class directions, Conditions 1, 3, 4 hold
(`widen_ext_g119.jsonl`); eleven disjoint cores in the class are impossible.
∎

Theorem C contains Theorem B; the grid-119 table in the refinement section carries the
symmetric companion `(12, 12)` and the intermediate `(40, 8)`.

**Corollary (a two-sided count).** At `96/25` the near-axis count and the end band
combine: in any packing of eleven at most ten squares are within `10.3875°` of the axes
(replay row `0–39`), and the remaining square or squares cannot all be within `1.4707°`
of `45°` either — the band `[0°, 10.3875°] ∪ [43.5293°, 45°]` holds at most ten squares,
`⌊10.96875⌋`.

### Widening the robust end band at 96/25

The class is `[0°, α(a)] ∪ [45° − β(b), 45°]` for `a` leading and `b` trailing cells,
with `α(a)` the exact upper tangent of cell `a − 1` and `45° − β(b)` the exact lower
tangent of cell `181 − b` (both closed).
Symmetric widening first, `a = b`, from the planning lane’s `a = b = 6`; then, from the
widest symmetric success, one end held and the other pushed.
Every point is the same search and the same exact decision as the replay rows.

| `(a, b)` | band, closed | `α + β` | rounds | float `M` | exact `M` | least core | verdict (grid 79) | wall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `(6, 6)` | `[0°, 1.4503°] ∪ [43.7565°, 45°]` | `2.6937°` | 29 | 10.6866 | `10959/1024 = 10.70215` | `1025/1024` | **refuted** (Theorem 1.11, replayed) | 5 s |
| `(7, 7)` | `[0°, 1.7139°] ∪ [43.5293°, 45°]` | `3.1846°` | 49 | 10.7761 | `5529/512 = 10.79883` | `4099/4096` | **refuted** | 18 s |
| `(8, 8)` | `[0°, 1.9775°] ∪ [43.3017°, 45°]` | `3.6759°` | 37 | 11.0000 | `5637/512 = 11.00977` | `4099/4096` | not refuted: Condition 2′ fails | 13 s |
| `(7, 8)` | `[0°, 1.7139°] ∪ [43.3017°, 45°]` | `3.4122°` | 24 | 11.0000 | `45109/4096 = 11.01294` | `2049/2048` | not refuted: Condition 2′ fails | 5 s |
| `(8, 7)` | `[0°, 1.9775°] ∪ [43.5293°, 45°]` | `3.4482°` | 36 | 10.7761 | `5529/512 = 10.79883` | `4099/4096` | **refuted** | 10 s |
| `(9, 7)` | `[0°, 2.2411°] ∪ [43.5293°, 45°]` | `3.7118°` | 50 | 10.7761 | `11061/1024 = 10.80176` | `4101/4096` | **refuted** | 21 s |
| `(10, 7)` | `[0°, 2.5047°] ∪ [43.5293°, 45°]` | `3.9754°` | 44 | 10.7761 | `5533/512 = 10.80664` | `4099/4096` | **refuted** | 18 s |
| `(11, 7)` | `[0°, 2.7683°] ∪ [43.5293°, 45°]` | `4.2390°` | 42 | 10.7761 | `5531/512 = 10.80273` | `4099/4096` | **refuted** | 13 s |
| `(12, 7)` | `[0°, 3.0318°] ∪ [43.5293°, 45°]` | `4.5025°` | 37 | 10.7761 | `11059/1024 = 10.79980` | `4099/4096` | **refuted** | 12 s |
| `(13, 7)` | `[0°, 3.2953°] ∪ [43.5293°, 45°]` | `4.7660°` | 38 | 10.7761 | `11059/1024 = 10.79980` | `4099/4096` | **refuted** | 15 s |
| `(14, 7)` | `[0°, 3.5588°] ∪ [43.5293°, 45°]` | `5.0295°` | 37 | 10.7761 | `11059/1024 = 10.79980` | `4099/4096` | **refuted** | 19 s |
| `(15, 7)` | `[0°, 3.8222°] ∪ [43.5293°, 45°]` | `5.2929°` | 44 | 10.7761 | `11061/1024 = 10.80176` | `4099/4096` | **refuted** | 24 s |
| `(16, 7)` | `[0°, 4.0856°] ∪ [43.5293°, 45°]` | `5.5563°` | 38 | 10.7761 | `11059/1024 = 10.79980` | `4099/4096` | **refuted** | 18 s |
| `(17, 7)` | `[0°, 4.3489°] ∪ [43.5293°, 45°]` | `5.8196°` | 43 | 10.7761 | `11067/1024 = 10.80762` | `4099/4096` | **refuted** | 18 s |
| `(18, 7)` | `[0°, 4.6122°] ∪ [43.5293°, 45°]` | `6.0829°` | 43 | 10.7761 | `11059/1024 = 10.79980` | `4099/4096` | **refuted** | 19 s |
| `(19, 7)` | `[0°, 4.8754°] ∪ [43.5293°, 45°]` | `6.3462°` | 46 | 10.7761 | `1383/128 = 10.80469` | `4101/4096` | **refuted** | 31 s |
| `(22, 7)` | `[0°, 5.6649°] ∪ [43.5293°, 45°]` | `7.1356°` | 45 | 10.7761 | `11057/1024 = 10.79785` | `4099/4096` | **refuted** | 35 s |
| `(25, 7)` | `[0°, 6.4537°] ∪ [43.5293°, 45°]` | `7.9244°` | 39 | 10.7761 | `691/64 = 10.79688` | `4099/4096` | **refuted** | 28 s |
| `(30, 7)` | `[0°, 7.7671°] ∪ [43.5293°, 45°]` | `9.2378°` | 34 | 10.7761 | `11065/1024 = 10.80566` | `4101/4096` | **refuted** | 24 s |
| `(35, 7)` | `[0°, 9.0785°] ∪ [43.5293°, 45°]` | `10.5492°` | 39 | 10.7761 | `11057/1024 = 10.79785` | `4099/4096` | **refuted** | 41 s |
| `(40, 7)` | `[0°, 10.3875°] ∪ [43.5293°, 45°]` | `11.8582°` | 41 | 10.9311 | `351/32 = 10.96875` | `4101/4096` | **refuted** | 52 s |
| `(6, 8)` | `[0°, 1.4503°] ∪ [43.3017°, 45°]` | `3.1486°` | 37 | 11.0000 | `11277/1024 = 11.01270` | `2049/2048` | not refuted: Condition 2′ fails | 8 s |
| `(1, 8)` | `[0°, 0.1318°] ∪ [43.3017°, 45°]` | `1.8302°` | 22 | 11.0000 | `11277/1024 = 11.01270` | `4099/4096` | not refuted: Condition 2′ fails | 3 s |
| `(1, 10)` | `[0°, 0.1318°] ∪ [42.8453°, 45°]` | `2.2865°` | 39 | 11.1394 | `11423/1024 = 11.15527` | `1025/1024` | not refuted: Condition 2′ fails | 6 s |
| `(3, 8)` | `[0°, 0.6592°] ∪ [43.3017°, 45°]` | `2.3576°` | 24 | 11.0000 | `1411/128 = 11.02344` | `4101/4096` | not refuted: Condition 2′ fails | 3 s |

The rationalised atoms of every refuted row carry `D4` symmetry, Conditions 3 and 4 hold
for the net (`B(1 + D) = 0.99770… < 1`), and the least core mass over every class
direction is at least one; the verdicts are in `widen_g79.jsonl` and `widen_ext.jsonl`
in the session scratchpad with the atom counts (93 to 216 atoms per point).

### Where the obstruction lives in angle: the dual’s support

For a class whose grid-79 value stays at or above eleven, the LP dual on the rows the
loop generated is a fractional packing on the site set: weights `y_r ≥ 0` on placements
(`B`-cores at class directions) with `Σ_r y_r A[r, a] ≤ |a|` for every `D4` orbit `a` of
sites, and `Σ_r y_r = M` at optimality.
Equivalently the `D4`-symmetrised family (each row’s eight images at weight `y_r / 8`)
has depth at most one at every site.
That is a site-set object: depth at most one *between* sites is not implied, and the
honest continuum value is `M / d` for the exact maximum depth `d` that `ceiling.py`
decides. The angular support below is the dual read by the direction of its rows
(`histogram.py`; `hist.json` in the scratchpad holds each family with its centres).

| class | folded set | `M` (grid 79) | support rows | `[0°, 2.5°)` | `[38.2°, 40.77°)` | `[40.77°, 42.5°)` | `[42.5°, 45°]` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `0–5 ∪ 151–180` | `[0°, 1.4503°] ∪ [38.2049°, 45°]` (contains `40.194°`) | 11.2535, converged in 25 rounds | 29 | 7.472 | 1.775 | 0.465 | 1.542 |
| `0–7 ∪ 173–180` | `[0°, 1.9775°] ∪ [43.3017°, 45°]` (first symmetric failure) | 11.0000, converged in 33 rounds | 8 | 6.000 | — | — | 5.000 |
| `0–6 ∪ 173–180` | `[0°, 1.7139°] ∪ [43.3017°, 45°]` | 11.0000, converged in 20 rounds | 5 | 8.000 | — | — | 3.000 |
| `0–5 ∪ 149–180` | `[0°, 1.4503°] ∪ [37.7333°, 45°]` (Trump band `±2.44°` and the diagonal end) | 11.2535, converged in 30 rounds | 30 | 7.465 | 1.141 (and 0.535 in `[35°, 38.2°)`) | 0.451 | 1.662 |

By direction, the band toward `40.19°` carries `6.739` at direction `0` (exactly
axis-parallel), `0.155` at `0.79°`, `0.578` at `1.32°`, then `0.761` at `38.32°`,
`0.437` at `39.03°`, `0.338` at `40.19°` itself, `0.183` at `40.89°`, `0.211` at
`41.35°`, `0.366` at `42.73°`, `0.296` at `43.19°`, `0.254` at `43.42°`, `0.549` at
`44.32°`, and small remainders.
Seven and a half units of the eleven-and-a-quarter sit within `1.32°` of the axis and
the other three and three-quarters are spread over the whole of `[38.2°, 45°]` rather
than concentrated at Trump’s angle: the mass at `40.19° ± 0.5°` is `0.45`.

The two end-band failures are sharper.
At `(8, 8)` the dual is eight rows of integer weight summing to exactly eleven: five
units at direction `0`, one at `0.26°`, two at `43.42°`, one each at `43.64°`, `43.87°`
and `44.32°` — six near the axis and five near `45°`, Trump’s composition.
At `(7, 8)` it is five rows, again integral, eight near the axis (six at `0°`, two at
`0.79°`) and three near `45°`. Both are `D4`-symmetrised fractional families (a corner
core of weight three, for instance, is three quarters of a core at each of the four
corners), not packings of eleven squares; and since `96/25 ÷ (9977/10000) = 3.8489` is
below every known side for eleven unit squares, no family of eleven disjoint `B`-cores
exists in the container at all.
The site-set dual can still reach eleven because two cores may overlap by up to a site
spacing (`(96/25 − 1/5)/78 = 0.0467`) without sharing a site.

`ceiling.py` decides that reading exactly (`ceiling_check.py`: the symmetrised family as
a `CeilingCertificate` in the `net` regime, `scaled_to_unit_depth`, then
`verify_ceiling`). All three duals fail as continuum obstructions, and by a wide margin:

| dual | rows, placements | raw total | exact maximum depth | scaled total | K2 depth ≤ 1 after scaling | K3 total ≥ 11 |
| --- | --- | --- | --- | --- | --- | --- |
| `0–7 ∪ 173–180`, `(8, 8)` | 8, 64 | 11 | `2` | `11/2` | holds (13 488 vertices, 327 decided exactly) | fails |
| `0–6 ∪ 173–180`, `(7, 8)` | 5, 40 | 11 | `2` | `11/2` | holds (4 488 vertices) | fails |
| `0–5 ∪ 151–180`, toward `40.19°` | 29, 232 | 11.2535 | `1291/568 = 2.2729` | `6392/1291 = 4.9512` | holds (220 532 vertices, 1 514 decided exactly) | fails |

A depth of exactly two is two cores of the integral family overlapping in a region that
contains no site; at grid 79 the site spacing is `0.0467` and a `B`-core is `0.9977`
wide, so that is the expected failure mode.
The reading for the cell’s question is therefore: on grid 79, every band whose value
stays at or above eleven is stopped by a near-integral, Trump-composition family that is
*not* a fractional packing of the continuum; the obstruction the site set shows is an
artefact of the site set, not of the relaxation, and the true class covering values of
these bands are open from below.
The grid-119 refinement below confirms it for the two end bands.
For the band toward `40.19°` the honest obstruction, if one exists, has to come from a
continuum family (`BC-294`’s cutting-plane loop with the disjointness filter, or a
hand-built family) and not from a site-set dual; nothing here shows that band to be
unclosable.

### One refinement: grid 119

The site set, not the relaxation, stopped the diagonal end on grid 79, so the failing
points were rerun on `build_site_grid(96/25, 119, 1/10)` (`14 161` sites), everything
else unchanged.

| `(a, b)` | band, closed | `α + β` | grid | rounds | float `M` | exact `M` | least core | verdict | wall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `(8, 8)` | `[0°, 1.9775°] ∪ [43.3017°, 45°]` | `3.6759°` | 119 | 52 | 10.7012 | `43857/4096 = 10.70728` | `4097/4096` | **refuted** | 52 s |
| `(7, 8)` | `[0°, 1.7139°] ∪ [43.3017°, 45°]` | `3.4122°` | 119 | 54 | 10.7012 | `43865/4096 = 10.70923` | `4097/4096` | **refuted** | 50 s |
| `(7, 7)` | `[0°, 1.7139°] ∪ [43.5293°, 45°]` | `3.1846°` | 119 | 53 | 10.7012 | `43857/4096 = 10.70728` | `4097/4096` | **refuted** | 42 s |
| `(9, 9)` | `[0°, 2.2411°] ∪ [43.0737°, 45°]` | `4.1675°` | 119 | 40 | 10.7017 | `43951/4096 = 10.73022` | `2051/2048` | **refuted** | 27 s |
| `(10, 10)` | `[0°, 2.5047°] ∪ [42.8453°, 45°]` | `4.6594°` | 119 | 46 | 10.7017 | `43951/4096 = 10.73022` | `2051/2048` | **refuted** | 45 s |
| `(40, 8)` | `[0°, 10.3875°] ∪ [43.3017°, 45°]` | `12.0858°` | 119 | 86 | 10.7981 | `11085/1024 = 10.82520` | `2051/2048` | **refuted** | 474 s |
| `(11, 11)` | `[0°, 2.7683°] ∪ [42.6166°, 45°]` | `5.1516°` | 119 | 50 | 10.7017 | `43951/4096 = 10.73022` | `1025/1024` | **refuted** | 56 s |
| `(40, 9)` | `[0°, 10.3875°] ∪ [43.0737°, 45°]` | `12.3138°` | 119 | 81 | 10.7981 | `11083/1024 = 10.82324` | `4101/4096` | **refuted** | 584 s |
| `(12, 12)` | `[0°, 3.0318°] ∪ [42.3876°, 45°]` | `5.6442°` | 119 | 47 | 10.7351 | `11033/1024 = 10.77441` | `4101/4096` | **refuted** | 109 s |

Grid 119 refutes `(8, 8)`, which grid 79 could not, lowers the value of `(7, 7)` from
`10.799` to `10.707`, and then keeps going: every symmetric point through `(12, 12)` —
`[0°, 3.0318°] ∪ [42.3876°, 45°]`, `α + β = 5.6442°`, mass `11033/1024 = 10.7744` — is
refuted, and so are `(40, 8)` and `(40, 9)`, the latter being Theorem C above with
`α + β = 12.3138°`. The `(13, 13)` and `(40, 10)` points were cut off by the clock, not
decided, so the grid-119 rung lies at or beyond `(12, 12)` and `(40, 9)`. The widest
exact-decided band is therefore a property of the site set as much as of the side, every
non-refutation in the grid-79 table is a grid-79 reading only, and the ladder’s true
rung at `96/25` lies beyond every point either grid decided.
A finer site set needs nothing new in code; its cost is the row loop, not the exact
sweep — the symmetric points took 27 to 109 s at grid 119 on this loaded machine and the
`(40, b)` points 474 and 584 s, with the exact decision under four seconds in every
case. The axis end is different — its limit is the near-axis saturation (`[0°, 13°]`
alone is already at eleven on grid 79, planning report §2.3) — and the last points
decided at grid 79 are:

| `(a, b)` | band, closed | `α + β` | rounds | float `M` | exact `M` | least core | verdict (grid 79) | wall |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `(43, 7)` | `[0°, 11.1716°] ∪ [43.5293°, 45°]` | `12.6423°` | 59 | 11.0000 | `11275/1024 = 11.01074` | `1025/1024` | not refuted: Condition 2′ fails | 72 s |
| `(45, 7)` | `[0°, 11.6937°] ∪ [43.5293°, 45°]` | `13.1644°` | 28 | 11.0891 | `11371/1024 = 11.10449` | `4099/4096` | not refuted: Condition 2′ fails | 24 s |
| `(47, 7)` | `[0°, 12.2154°] ∪ [43.5293°, 45°]` | `13.6861°` | 39 | 11.0898 | `22747/2048 = 11.10693` | `1025/1024` | not refuted: Condition 2′ fails | 34 s |
| `(49, 7)` | `[0°, 12.7366°] ∪ [43.5293°, 45°]` | `14.2073°` | 36 | 11.0898 | `5689/512 = 11.11133` | `2051/2048` | not refuted: Condition 2′ fails | 28 s |
| `(41, 7)` | `[0°, 10.6489°] ∪ [43.5293°, 45°]` | `12.1197°` | 82 | 11.0000 | `11293/1024 = 11.02832` | `4099/4096` | not refuted: Condition 2′ fails | 126 s |
| `(42, 7)` | `[0°, 10.9103°] ∪ [43.5293°, 45°]` | `12.3810°` | 49 | 11.0000 | `11275/1024 = 11.01074` | `1025/1024` | not refuted: Condition 2′ fails | 49 s |

### Obstructions

- **The `45°` end is the binding end.** With seven trailing cells (`β = 1.4707°`) the
  float value is pinned at `10.7761` for every axis width from `1.71°` to `9.08°`, and
  the same measure works: the near-axis cores are pierced by the smeared nine-point
  pattern at mass nine whatever the width, and the diagonal cores cost the rest.
  The eighth trailing cell (`43.3017°`) tips grid 79 to eleven even with a single axis
  cell; grid 119 takes it back.
  A theorem with `β` beyond `1.47°` is a site-set question, not a relaxation question,
  on the evidence here.
- **The site-set dual is not an obstruction.** Every dual that reached eleven on grid 79
  has continuum depth two or more; `ceiling.py` scales them to `5.5` and `4.95`. A
  non-refutation on a grid remains what the planning report’s §3.2 said it is.
- **Cost.** Wall times here ran at load average eight on four cores with one worker; the
  `[30°, 45°]` replay took 1 149 s against 700 s in the planning lane.
  The band toward `40.19°` converged in 25 rounds and 16 s on grid 79 (the planning
  lane’s 80-round cap on the trailing-30 class alone was the slow case, not this union),
  so a grid-119 run of it is affordable next.
- **Not done.** `(13, 13)` and `(40, 10)` at grid 119 were cut off by the clock, so
  neither end is known to be exhausted there; the single trailing-six class at `96/25`
  stays undecided on its own (implied by the trailing-ten count); no continuum family
  was built for any band.
  A note on method: the queue that ran grid 119 piped its output through `grep`, whose
  block-buffered file output hid the finished rows until the end, so the session
  believed for half an hour that `(9, 9)` had stalled; the `jsonl` logs, written per
  point, are the record.

### Status recommended for H-130 and H-131

- **H-130**: confirmed as stated, exact-decided — Theorem A gives `α + β = 3.1846°` on
  grid 79, Theorem B `11.8582°` on grid 79, and Theorem C `12.3138°` on grid 119 (with
  the symmetric `5.6442°` of `(12, 12)` there).
  Frozen claims, need exp ids.
  The hypothesis text should be read with its domain: closed folded ranges, the tangent
  bounds above, `B = 9977/10000`, the retained net.
- **H-131**: the registered replay is complete and every count reproduces to the
  fraction on the stated site set; the counts can now be cited as results of this
  record. Frozen claim, needs exp id (one record for the five `96/25` counts and the
  three `U` counts, or the replay table here cited directly).

### What the next session should do first

1. Continue the end band at grid 119 (and 159) from `(13, 13)` and `(40, 10)` until
   Condition 2′ fails; symmetric points are one to two minutes at grid 119, the
   `(40, b)` points about ten.
   Freeze the widest success with its atoms.
2. Run the band toward `40.19°` (`0–5 ∪ 151–180`, and `0–39 ∪ 151–180`) at grid 119; if
   it stays above eleven, build the family in the continuum (`BC-294`’s loop with the
   disjointness filter) and verify it with `ceiling.py` before calling it an
   obstruction.
3. Allocate the experiment ids for Theorems A and B and the replay, and move H-130 and
   H-131 to the status the registry uses for exact-decided claims.

### Appendix: scripts as run (session-102)

All scripts live in the session scratchpad and import the repository’s `sqpack` from the
lane worktree; they were run from `packing/` as
`PACK_JOBS=1 OMP_NUM_THREADS=1 uv run --frozen --all-extras --group dev python <script>`.

#### `bandlib.py`

```text
"""Lane BC-295 (session-102): band classes at 96/25 with the repository's class program.

Every decision is `decide_class_program` on rationalised atoms at thresholds (1, 0) for the
composition (11, 0); the float search only proposes. `solve_rows` mirrors the row loop of
`solve_class_program` at w0 = 1 and keeps each row's direction so the LP dual can be read
as a fractional packing by angle (the histogram the cell asks for). Nothing here is retained.
"""

from __future__ import annotations

import json
import math
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from sqpack.fractional.classcert import (
    ClassThresholds,
    Composition,
    DirectionClasses,
    decide_class_program,
    solve_class_program,
)
from sqpack.fractional.generate import (
    LP_FEASIBILITY,
    build_site_grid,
    direction_net,
    net_half_tangents,
    placement_cells,
    rationalise,
)
from sqpack.project import require_project_root

NET_SOURCE = Path("cases/n11_fractional_certificate/certificate.json")
Q = Fraction(96, 25)
U = Fraction(3877084, 10**6)


def load_net():
    root = require_project_root()
    spec = json.loads((root / NET_SOURCE).read_text())
    limit = Fraction(spec["angle_limit"])
    steps = int(spec["direction_steps"])
    return net_half_tangents(limit, steps), Fraction(spec["square_side"])


def deg(t: Fraction) -> float:
    return math.degrees(math.atan(float(t)))


def parse_cells(spec: str) -> frozenset[int]:
    cells: set[int] = set()
    for r in spec.split(","):
        lo, hi = r.split("-")
        cells |= set(range(int(lo), int(hi) + 1))
    return frozenset(cells)


def folded_ranges(classes: DirectionClasses, cells: frozenset[int]) -> list[tuple[int, int, float, float]]:
    """Maximal runs of cells with their exact-tangent bounds in degrees."""
    runs = []
    for c in sorted(cells):
        if runs and runs[-1][1] == c - 1:
            runs[-1][1] = c
        else:
            runs.append([c, c])
    return [
        (lo, hi, deg(classes.cell_bounds(lo)[0]), deg(classes.cell_bounds(hi)[1]))
        for lo, hi in runs
    ]


def run_class(
    ht, shrink, side: Fraction, cells: frozenset[int], *, grid_count: int = 79,
    inset: Fraction = Fraction(1, 10), max_rounds: int = 100, scale: int = 4096, name: str = "",
) -> dict:
    """Float search then the exact decision of the reached point at thresholds (1, 0)."""
    classes = DirectionClasses(ht, cells)
    grid = build_site_grid(side, grid_count, inset)
    comp = Composition(11, 0)
    t0 = time.perf_counter()
    weights, log = solve_class_program(grid, shrink, classes, comp, max_rounds=max_rounds)
    t_float = time.perf_counter() - t0
    rec = {
        "name": name, "side": str(side), "grid": grid_count, "inset": str(inset),
        "sites": len(grid.positions()), "orbits": len(grid.orbits), "shrink": str(shrink),
        "net": {"cells": len(ht), "limit": str(ht[-1]), "steps": len(ht) - 1},
        "cells": sorted(cells), "ncells": len(cells),
        "ranges_deg": folded_ranges(classes, cells),
        "ranges_tan": [
            [str(classes.cell_bounds(lo)[0]), str(classes.cell_bounds(hi)[1])]
            for lo, hi, _, _ in folded_ranges(classes, cells)
        ],
        "composition": [11, 0], "max_rounds": max_rounds, "rounds": log.rounds,
        "rows": log.rows, "stopped": log.stopped, "scale": scale,
        "float_M_at_w0_1": (log.objective / log.thresholds[0]) if log.thresholds[0] > 0 else None,
        "float_seconds": round(t_float, 1),
    }
    if log.thresholds[0] > 0:
        atoms = rationalise(grid, weights / log.thresholds[0], scale=scale)
        t1 = time.perf_counter()
        v = decide_class_program(
            atoms, side, shrink, classes, comp, thresholds=ClassThresholds(Fraction(1), Fraction(0))
        )
        t_exact = time.perf_counter() - t1
        M = v.total_mass
        holds_5 = all(c.holds for c in v.conditions if not c.name.startswith("Condition 2'"))
        rec["exact"] = {
            "atoms": len(atoms), "M": str(M), "M_float": float(M),
            "floor_M": math.floor(M),
            "conditions": [(c.name, c.holds, c.detail) for c in v.conditions],
            "failures": list(v.failures),
            "refutes_11_0": v.refutes,
            "count_bound": math.floor(M) if holds_5 else None,
            "minima": [(m.label, str(m.mass), float(m.mass), m.direction) for m in v.minima if m.mass is not None],
            "exact_seconds": round(t_exact, 1),
        }
    return rec


def solve_rows(ht, shrink, side: Fraction, cells: frozenset[int], *, grid_count: int = 79,
               inset: Fraction = Fraction(1, 10), max_rounds: int = 100, rows_per_direction: int = 3,
               tolerance: float = 1e-9):
    """The composition-(11, 0) row loop at w0 = 1, keeping each row's direction and centre.

    Returns (weights, rows, row_dirs, row_centres, duals, objective, stopped, rounds).
    The dual y >= 0 on rows satisfies sum_r y_r A[r, a] <= |orbit a| for every orbit a and
    sum_r y_r = objective at optimality: a fractional packing of B-cores at class directions
    with depth at most one on the site set, whose value is the class covering value on this
    site set.
    """
    classes = DirectionClasses(ht, cells)
    grid = build_site_grid(side, grid_count, inset)
    positions = grid.positions()
    points = np.array([[float(x), float(y)] for x, y in positions])
    sizes = np.array([len(o) for o in grid.orbits], dtype=float)
    membership = np.zeros(len(positions), dtype=int)
    cursor = 0
    for index, orbit in enumerate(grid.orbits):
        membership[cursor: cursor + len(orbit)] = index
        cursor += len(orbit)
    directions = direction_net(ht)
    outer, sq = float(side), float(shrink)
    rows: list[np.ndarray] = []
    row_dirs: list[int] = []
    row_centres: list[tuple[float, float]] = []
    held: set[bytes] = set()
    weights = np.zeros(len(grid.orbits))
    duals = np.zeros(0)
    objective = float("inf")
    stopped = ""
    rounds = 0
    for round_index in range(max_rounds):
        rounds = round_index + 1
        site_weights = weights[membership]
        violated = added = 0
        least_slack = float("inf")
        for index in sorted(cells):
            direction = directions[index]
            for mass, u, v, covers in placement_cells(points, site_weights, direction, outer, sq, keep=rows_per_direction):
                if mass >= 1.0 - tolerance:
                    break
                row = np.zeros(len(grid.orbits))
                np.add.at(row, membership[covers], 1.0)
                if row.sum() == 0:
                    stopped = "a placement covers no site"
                    return weights, rows, row_dirs, row_centres, duals, objective, stopped, rounds
                violated += 1
                least_slack = min(least_slack, 1.0 - mass)
                key = row.tobytes()
                if key not in held:
                    held.add(key)
                    rows.append(row)
                    row_dirs.append(index)
                    row_centres.append((float(u), float(v)))
                    added += 1
        if violated == 0 or (added == 0 and least_slack <= LP_FEASIBILITY):
            objective = float(sizes @ weights)
            stopped = "converged"
            break
        if added == 0:
            stopped = f"held row short by {least_slack:.3e}"
            break
        A = np.vstack(rows)
        res = linprog(c=sizes, A_ub=-A, b_ub=-np.ones(len(rows)), bounds=[(0.0, None)] * len(sizes), method="highs")
        if not res.success:
            stopped = "LP refused"
            break
        weights = np.asarray(res.x, dtype=float)
        objective = float(res.fun)
        duals = -np.asarray(res.ineqlin.marginals, dtype=float)
    else:
        stopped = f"round limit {max_rounds}"
    return weights, rows, row_dirs, row_centres, duals, objective, stopped, rounds


def histogram(ht, row_dirs, duals, bins_deg=(0, 2.5, 5, 7.5, 10, 15, 20, 25, 30, 35, 38.2, 40.77, 42.5, 45.0001)):
    """Dual weight by direction cell and by coarse folded-angle bin."""
    by_dir: dict[int, float] = {}
    for d, y in zip(row_dirs, duals):
        if y > 1e-12:
            by_dir[d] = by_dir.get(d, 0.0) + float(y)
    angles = {d: 2 * math.degrees(math.atan(float(ht[d]))) for d in by_dir}
    by_bin = {}
    for d, y in by_dir.items():
        a = angles[d]
        for lo, hi in zip(bins_deg[:-1], bins_deg[1:]):
            if lo <= a < hi:
                key = f"[{lo}, {hi if hi < 45.0001 else 45}{')' if hi < 45.0001 else ']'}"
                by_bin[key] = by_bin.get(key, 0.0) + y
                break
    return {"total": float(sum(by_dir.values())), "by_direction": {str(d): (round(angles[d], 3), round(y, 4)) for d, y in sorted(by_dir.items())}, "by_bin": {k: round(v, 4) for k, v in by_bin.items()}}
```

#### `replay.py`

```text
"""Registered replay of the planning lane's decisions (H-131 counts and the end bands)."""
import json, sys, time
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from bandlib import Q, U, load_net, parse_cells, run_class

ht, B = load_net()
out = Path(sys.argv[1])
jobs = [
    # name, side, cells, rounds, planning-lane claim
    ("q_lead25_axis_6.45", Q, "0-24", 100, "<= 9 within 6.4537 deg; planning exact 9.00586"),
    ("q_lead40_axis_10.39", Q, "0-39", 100, "<= 10 within 10.3875 deg; planning exact 10.5127"),
    ("q_end6_axis_1.45", Q, "0-5", 100, "end band [0, 1.4503]; planning exact 9.00391"),
    ("q_trail6_45_1.24", Q, "175-180", 100, "end band [43.7565, 45]; planning float 9.623, not exact-decided"),
    ("q_union_0-5_175-180_T1.11", Q, "0-5,175-180", 100, "Theorem 1.11; planning exact 10.70215"),
    ("U_lead25_axis_6.45", U, "0-24", 100, "<= 9 at U; planning exact 9.82910"),
    ("U_lead30_axis_7.77", U, "0-29", 100, "<= 10 at U; planning exact 10.00293"),
    ("U_trail6_45_1.24", U, "175-180", 100, "<= 10 at U; planning exact 10.15820"),
    ("q_trail10_45_2.155", Q, "171-180", 100, "<= 9 within 2.155 of 45; planning exact 9.75488"),
    ("q_trump_149-169_pm2.44", Q, "149-169", 100, "<= 10 within 2.44 of 40.19; planning exact 10.13892"),
    ("q_tilt_ge_30.01", Q, "117-180", 100, "<= 10 in [30.0149, 45]; planning exact 10.39771"),
]
only = set(sys.argv[2:])
with out.open("a") as h:
    for name, side, spec, rounds, claim in jobs:
        if only and name not in only:
            continue
        t0 = time.perf_counter()
        rec = run_class(ht, B, side, parse_cells(spec), max_rounds=rounds, name=name)
        rec["planning_claim"] = claim
        rec["wall_seconds"] = round(time.perf_counter() - t0, 1)
        h.write(json.dumps(rec) + "\n"); h.flush()
        ex = rec.get("exact", {})
        print(f"{name:32s} side {float(side):.6f} cells {rec['ncells']} {rec['ranges_deg']} float {rec['float_M_at_w0_1']} rounds {rec['rounds']} {rec['stopped']} | exact M {ex.get('M')} = {ex.get('M_float')} count<= {ex.get('count_bound')} refutes(11,0) {ex.get('refutes_11_0')} fail {ex.get('failures')} min {ex.get('minima')} | {rec['wall_seconds']}s", flush=True)
```

#### `widen.py`

```text
"""Widen the robust end band [0, alpha] U [45 - beta, 45] at 96/25 on grid 79, cell by cell.

Symmetric first (k leading cells and k trailing cells), until Condition 2' fails; then
asymmetric from the widest symmetric success: hold one end and push the other. Each point
is exact-decided regardless of convergence (the exact sweep is complete; the loop's rows
are a subset). Usage: widen.py OUT.jsonl [grid] [k_lo] [k_hi]
"""
import json, sys, time
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from bandlib import Q, load_net, run_class

ht, B = load_net()
n = len(ht)
out = Path(sys.argv[1])
grid = int(sys.argv[2]) if len(sys.argv) > 2 else 79
k_lo = int(sys.argv[3]) if len(sys.argv) > 3 else 7
k_hi = int(sys.argv[4]) if len(sys.argv) > 4 else 13
rounds = 100


def band(a: int, b: int) -> frozenset[int]:
    return frozenset(range(a)) | frozenset(range(n - b, n))


def run(name, a, b):
    t0 = time.perf_counter()
    rec = run_class(ht, B, Q, band(a, b), grid_count=grid, max_rounds=rounds, name=name)
    rec["lead"] = a; rec["trail"] = b
    rec["wall_seconds"] = round(time.perf_counter() - t0, 1)
    with out.open("a") as h:
        h.write(json.dumps(rec) + "\n")
    ex = rec.get("exact", {})
    r = rec["ranges_deg"]
    alpha = r[0][3]; beta = 45.0 - r[-1][2]
    ok = ex.get("refutes_11_0")
    print(f"{name:22s} grid {grid} lead {a} trail {b} alpha {alpha:.4f} beta {beta:.4f} sum {alpha+beta:.4f} | float {rec['float_M_at_w0_1']:.5f} rounds {rec['rounds']} {rec['stopped'][:9]} | exact M {ex.get('M')} = {ex.get('M_float')} refutes {ok} fail {ex.get('failures')} min {ex.get('minima')} | {rec['wall_seconds']}s", flush=True)
    return bool(ok), alpha, beta


# Symmetric.
best = None
for k in range(k_lo, k_hi + 1):
    ok, alpha, beta = run(f"sym_{k}", k, k)
    if ok:
        best = k
    else:
        break
print(f"widest symmetric success on grid {grid}: k = {best}", flush=True)
if best is None:
    sys.exit(0)
# Asymmetric: hold the trailing end at best, push the leading end; then the reverse.
for a in range(best + 1, best + 12):
    ok, alpha, beta = run(f"asym_lead_{a}_{best}", a, best)
    if not ok:
        break
for b in range(best + 1, best + 12):
    ok, alpha, beta = run(f"asym_trail_{best}_{b}", best, b)
    if not ok:
        break
```

#### `nine_replay.py`

```text
"""Replay of Theorem 1.5's nine-point control: the pushed set pierces the leading 18 cells at q."""
import sys
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from bandlib import Q, U, deg, load_net
from sqpack.fractional.model import Atom
from sqpack.fractional.classcert import Composition, DirectionClasses, class_minima

ht, B = load_net()

def nine(side, delta):
    xs = (1 - delta, side / 2, side - 1 + delta)
    return tuple(Atom(f"{i}{j}", xs[i], xs[j], Fraction(1)) for i in range(3) for j in range(3))

def widest(side, atoms, kmax=30):
    best, last = 0, None
    for k in range(1, kmax + 1):
        classes = DirectionClasses(ht, frozenset(range(k)))
        m = class_minima(atoms, classes, Composition(11, 0), side, B)[0]
        if m.mass is not None and m.mass >= 1:
            best = k
        else:
            last = (k, str(m.mass), m.direction)
            break
    return best, last

for name, side in (("q", Q), ("U", U)):
    for delta in (Fraction(0), Fraction(1, 200), Fraction(1, 100)):
        k, fail = widest(side, nine(side, delta))
        upper = deg(DirectionClasses(ht, frozenset(range(max(k, 1)))).cell_bounds(k - 1)[1]) if k else 0.0
        print(f"{name} delta {delta}: pierces leading {k} cells, folded tilt <= {upper:.4f} deg; first miss {fail}", flush=True)
    grid_atoms = tuple(Atom(f"{i}{j}", side / 4 * i, side / 4 * j, Fraction(1)) for i in (1, 2, 3) for j in (1, 2, 3))
    k, fail = widest(side, grid_atoms)
    print(f"{name} L/4 grid control: leading {k} cells (<= {deg(DirectionClasses(ht, frozenset(range(k))).cell_bounds(k-1)[1]):.4f} deg); first miss {fail}", flush=True)
```

#### `histogram.py`

```text
"""Angular support of the LP dual (a fractional packing on the site set) for a class at q.

Usage: histogram.py OUT.json name lo-hi[,lo-hi] [grid] [rounds]
"""
import json, sys, time
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from bandlib import Q, histogram, load_net, parse_cells, solve_rows, folded_ranges
from sqpack.fractional.classcert import DirectionClasses

ht, B = load_net()
out = Path(sys.argv[1]); name = sys.argv[2]; cells = parse_cells(sys.argv[3])
grid = int(sys.argv[4]) if len(sys.argv) > 4 else 79
rounds = int(sys.argv[5]) if len(sys.argv) > 5 else 100
t0 = time.perf_counter()
weights, rows, row_dirs, row_centres, duals, objective, stopped, nrounds = solve_rows(ht, B, Q, cells, grid_count=grid, max_rounds=rounds)
el = time.perf_counter() - t0
h = histogram(ht, row_dirs, duals)
support = [(d, str(ht[d]), cu, cv, float(y)) for d, (cu, cv), y in zip(row_dirs, row_centres, duals) if y > 1e-12]
rec = {"name": name, "cells": sorted(cells), "ranges_deg": folded_ranges(DirectionClasses(ht, cells), cells), "grid": grid, "side": str(Q), "shrink": str(B),
       "rounds": nrounds, "stopped": stopped, "rows": len(rows), "objective_M": objective, "dual_total": h["total"],
       "support_rows": len(support), "by_bin": h["by_bin"], "by_direction": h["by_direction"], "seconds": round(el, 1),
       "family": support}
existing = json.loads(out.read_text()) if out.exists() else {}
existing[name] = rec
out.write_text(json.dumps(existing, indent=1))
print(f"{name}: cells {rec['ranges_deg']} grid {grid} rounds {nrounds} {stopped} M {objective:.5f} dual total {h['total']:.5f} support rows {len(support)} {el:.0f}s", flush=True)
print("by bin:", json.dumps(h["by_bin"]), flush=True)
print("by direction:", json.dumps(h["by_direction"]), flush=True)
```

#### `ceiling_check.py`

```text
"""Exact ceiling check of a dual family read by histogram.py.

The LP dual y on rows satisfies sum_r y_r A[r, a] <= |orbit a|, so the D4-symmetrised
family (each row's eight images at weight y_r / 8) has depth at most one at every site of
the grid. verify_ceiling decides depth on the continuum; scaled_to_unit_depth divides by the
exact maximum depth d, and the honest value is (sum_r y_r) / d. At or above eleven that is
an exact obstruction: the class covering value at q is at least eleven on every site set.
Usage: ceiling_check.py HIST.json name [top_k]
"""
import json, sys, time
from fractions import Fraction
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from bandlib import Q, load_net
from sqpack.fractional.ceiling import CeilingCertificate, Placement, scaled_to_unit_depth, verify_ceiling
from sqpack.fractional.generate import direction_net

ht, B = load_net()
rec = json.loads(Path(sys.argv[1]).read_text())[sys.argv[2]]
top_k = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
family = sorted(rec["family"], key=lambda f: -f[4])[:top_k]
net = direction_net(ht)
L = Q
placements = []
for d, t_str, cu, cv, y in family:
    dirn = net[d]
    t = Fraction(t_str)
    # centre in container coordinates from the rotated-frame (u, v), rationalised
    u, v = Fraction(cu).limit_denominator(10**9), Fraction(cv).limit_denominator(10**9)
    x = dirn.ux * u + dirn.vx * v
    yy = dirn.uy * u + dirn.vy * v
    w = Fraction(y).limit_denominator(10**9) / 8
    t_ref = (1 - t) / (1 + t) if t != 0 else Fraction(0)
    images = ((x, yy, t), (L - x, yy, t_ref), (x, L - yy, t_ref), (L - x, L - yy, t),
              (yy, x, t_ref), (L - yy, x, t), (yy, L - x, t), (L - yy, L - x, t_ref))
    for px, py, pt in images:
        placements.append(Placement(pt, px, py, w, B))
cert = CeilingCertificate(11, L, B, ht, tuple(placements))
print(f"{sys.argv[2]}: {len(family)} rows kept of {len(rec['family'])}, {len(placements)} placements, raw total {float(cert.total_weight):.5f}", flush=True)
t0 = time.perf_counter()
scaled, factor = scaled_to_unit_depth(cert)
print(f"exact maximum depth {factor} = {float(factor):.6f}; scaled total {scaled.total_weight} = {float(scaled.total_weight):.5f} ({time.perf_counter()-t0:.0f}s)", flush=True)
verdict = verify_ceiling(scaled)
for c in verdict.conditions:
    print(f"  {c.name}: {c.holds} -- {c.detail[:200]}")
print(f"ceiling verdict: total {float(verdict.total_weight) if hasattr(verdict,'total_weight') else scaled.total_weight} regime {getattr(verdict,'regime',None)} holds {all(c.holds for c in verdict.conditions)} ({time.perf_counter()-t0:.0f}s)", flush=True)
out = Path(sys.argv[1]).with_suffix(f".{sys.argv[2]}.ceiling.json")
out.write_text(json.dumps({"family_rows": len(family), "placements": len(placements), "max_depth": str(factor), "scaled_total": str(scaled.total_weight), "scaled_total_float": float(scaled.total_weight), "conditions": [(c.name, c.holds, c.detail) for c in verdict.conditions], "certificate": scaled.to_record()}))
```

#### `queue2.sh`

```text
#!/bin/bash
S=/tmp/claude-0/-home-user-squares/9010767e-5bb7-5e7d-99d2-858400f3969a/scratchpad
export PACK_JOBS=1 OMP_NUM_THREADS=1 PATH=$S/uv012:$PATH
cd $S/wt-lane-295/packing
run() { uv run --frozen --all-extras --group dev python "$@" 2>&1 | grep -v UV_NATIVE; }
echo "== widen start $(date -u +%H:%M:%S)"
run $S/lane-295/widen.py $S/lane-295/widen_g79.jsonl 79 7 13
echo "== nine start $(date -u +%H:%M:%S)"
run $S/lane-295/nine_replay.py
echo "== hist end6+151 start $(date -u +%H:%M:%S)"
run $S/lane-295/histogram.py $S/lane-295/hist.json end6_trail30 0-5,151-180 79 100
echo "== queue2 done $(date -u +%H:%M:%S)"
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
