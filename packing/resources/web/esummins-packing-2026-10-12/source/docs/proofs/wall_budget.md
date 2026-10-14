# Lemma WALL — the 1-D wall-length budget for K0-BLOCKED, the jam count, and the composition with the corner charges — A97, 2026-09-04

Target (A97 BRIEF, PI mechanism): a near-zero-wastage corner is a JAM (axis-aligned slot square at
offset g ≤ 0.1 plus a near-flush nick partner, Lemma JAM-0); jams are area-free but should be
WALL-expensive — the slot square plus its pusher are two flush unit widths on a wall of length
< 3.877 that carries ≤ 3 squares — so two jams cannot share a wall, the jam count is bounded, and
the neighbouring corners are squeezed into charged cells of A47's corner table. Prove the 1-D
budget as a packing of wall-touching squares (A50-ruler style), compose it with the corner charges,
and run the exact Trump canary on every wall. Labels: [T] proved, [S] routine given cited items,
[M] measured (`attempts/A97-wall-budget/results/`), [F] finding, [C] open. Conventions:
`tilt_floor_k0.md` (LOCK, MENU, JAM-0, TF-U, ID), `nocrit_k0_blocked.md` (Lemma K, CLUSTER,
NOCRIT-SEL, COL), `k0_blocked_side.md` (CEIL, SLIDE, K0-O1), `frame_census.md` F2 (the chord lemma),
`structure_lemmas.md` L5–L7, A47 `results/primitives_report.md` (corner table), A85
`results/cases85.json` (JAM/BLOCK/WEDGE/OTHER, 21 patterns), `charge85.pairs.jsonl` (pair charges,
chore in progress at close-out). ŝ = 3.877083590022814, s0 = 969271/250000, m ∈ [3.82, ŝ),
E(m) = m² − 11 ≤ 4.03178, h₀ := 1/√2.

## 0. Verdict

> **Max jam count and the two-jams-per-wall verdict.** [T] The sound 1-D budget is Lemma WALL-F:
> Σ_Q φ_w(Q) ≤ m over ALL squares, where φ_w(Q) is the chord of int Q on the line at distance
> h₀ = 1/√2 from wall w; a square touching w has φ_w = 1/cos(tilt) ∈ [1, √2] EXACTLY, so ≤ 3
> squares touch a wall and three touchers satisfy Σ(1/cos θ_i − 1) ≤ m − 3 < 0.877084 (an upright
> with two 45° diamonds needs m ≥ 1 + 2√2 = 3.828427 — A47's s* and Lemma COL's ghost threshold
> again). **The brief's width cos t + sin t is NOT a budget: projections of interior-disjoint
> wall-touchers can overlap (by up to 0.092; explicit counterexample, §1.3).** A jam pair puts
> exactly 1 (the slot square S) on both of its walls and 1/cos α ≥ 1 (the nick partner N) on its
> NICK wall, nothing on the other. Hence [T]: **two jams cannot share a wall if both are nicked on
> it (Σφ ≥ 4 > m); two jams nicked on the perpendicular walls CAN share a wall as far as the budget
> is concerned (Σφ ≥ 2), and one-nick sharing leaves < 0.877 for everything else.** The slot
> square's pusher is a FREE square, distinct across jams ⇒ **j ≤ 3 jams unconditionally** (JAM⁴
> dead, agreeing with cases85's free-square kill), and **j ≤ 2, at OPPOSITE corners, under the
> named hypothesis P-ON (the pusher has unit footprint on the pusher wall — e.g. it touches it).**
> P-ON is not a theorem: the pusher of an x-side slot square is only forced to press S's far edge
> (NOCRIT-SEL Cor. 2), and [M] in the exact K0-BLOCKED corpus it FAILS 3/3 — every corpus jam
> (k0dir87 s0380 BR ×2, s0076 BR, all at σ = 4.000) has its slot square pressed by a square
> FLOATING 0.76–0.94 above the pusher wall with footprint 0. The corpus premise of the brief ("the
> on-wall pusher in every deep jam") is refuted; the residue is the floating-pusher POCKET
> (§2.4), the same object as the brief's "above-wall lock" (d). **Lemma FLOAT [T] (PI follow-up)
> prices the pocket exactly: the strip P = (a+1, a+2) × (0, h₀) beside the slot square on the
> pusher wall strands area ≥ h₀ (1 − L), where L is the WALL-F chord length spent in (a+1, a+2)
> by the other squares (Lemma SHADOW: a square's points below h₀ lie within its chord's
> x-range). So every jam pays 0.7071 (1 − L) in area plus L in wall length — a floating pusher
> with an empty pocket strands exactly 0.7071, which is what the three corpus jams do (stranded
> 0.7071 / 0.7071 / 0.7064, L = 0 / 0 / 0.021).**
>
> **Composition verdict.** [T+M] NOT dead by area for j = 0, 1, 2 (nor 3) — with Lemma FLOAT
> the jams contribute ≥ 0.707 (1 − L) each, i.e. ≤ 2.12 for j = 3 with floating pushers, against
> E(m) ≥ 3.83 and non-jam corners with charge-0 pairs; max jam count stays 3 (2 opposite when
> every pusher is on-wall) — and NO offset cap:
> the wall budget forces at most ONE unit-footprint member of the adjacent crowd onto a jam's nick
> wall (exact inequality in the member's tilt and wall distance, Lemma WALL-S), but a corner pair
> with one floating member sits in the charge-zero strata (BLOCK/WEDGE pairs with certified pair
> charge 0 / 0.023 in charge85's 200-pair sample; 89 % of the 7 044 realisable pairs pass the
> squeeze; charge85's own four-corner composition kills 5·10⁻⁵ of the sampled orbits), so
> the forced sum is ≈ 0 ≪ E(m) for every j — A47's sixth face, one level up. What the budget does
> give is an OFFSET FLOOR, not a cap: an OFFSET-UPRIGHT corner adjacent to a jam along the nick
> wall w needs its upright at distance > h₀ = 0.707 from w or its tilted partner at distance ≥
> h₀ − 0.4385·sin 2θ_P ≥ 0.2686 from w — so a nick pocket on w's side must be ≥ 0.2686 wide
> (Trump's TL: the upright hugs the left wall, the nick is in the TOP gap, the partner's left-wall
> distance is 0.8317 — allowed). The zero cell
> (A47 C_x0_x0_b0_1) is denied only in the sense that a wall line carries ≤ 3 unit footprints and
> a jam already spends two of them on its nick wall; every cell whose pair keeps Σφ ≤ 1.877 on the
> shared line stays available to the adversary (§3.3 lists them).
>
> **Escapes** (§4.2): (E1) floating pusher / above-wall lock — corpus 3/3 jams; (E2) crowd
> members with zero wall footprint — 27 % of realisable pairs per line have no unit-footprint
> member, and [T] a zero-footprint intruder has depth ≤ 1 − h₀ = 0.2929 (= CEIL's constant), so
> the escape is exactly the shallow member; (E3) tilted on-wall pushers — allowed (MENU
> constrains N's lock, not S's pusher) and they only tighten the budget (1/cos θ ≥ 1);
> (E4) Lemma SLIDE confines jams to the shell m ≥ ŝ − g²/√(1−g²) ≥ ŝ − 0.01005 [modulo K0-O1] —
> below it the jam question is void. **Canary: exact Trump PASSES on all four walls with the left
> wall TIGHT at exactly three flush units (Σφ = 3.000000, slack ŝ − 3 = 0.877083590) and the
> bottom wall at 3.2829; no wall carries two diamonds; Trump has no jam corner.**

## 1. The footprint budget

### 1.1 [T] Lemma WALL-F

Fix wall w and the frame in which w is {y = 0}, the container [0, m] × [0, m]. For a square Q let
φ_w(Q) := the length of int Q ∩ {y = h₀} (0 if empty), h₀ = 1/√2.

**Lemma WALL-F.** Σ_{Q} φ_w(Q) ≤ m, the sum over all eleven squares.

*Proof.* int Q ∩ {y = h₀} is an open segment of the line, contained in (0, m) × {h₀}; for distinct
squares these open segments are disjoint (the interiors are). Disjoint open subsegments of a segment
of length m have total length ≤ m. ∎

**Chord formula [T].** Let Q have tilt θ := dist(θ_Q, 90°ℤ) ∈ [0, 45°], lowest point at height
y_min ≥ 0, and t := h₀ − y_min. Then φ_w(Q) = 0 if t ≤ 0, and for t > 0
  φ_w(Q) = 1 (θ = 0, t < 1),   φ_w(Q) = min(2t/sin 2θ, 1/cos θ) (θ > 0).
*Proof.* Put the lowest vertex at the origin, edges (cos θ, sin θ) and (−sin θ, cos θ). At height
t ≤ sin θ the chord runs from the left edge x = −t tan θ to the right edge x = t cot θ, length
t(tan θ + cot θ) = 2t/sin 2θ; for t ∈ [sin θ, cos θ] the right end is on the edge R→TR,
x = cos θ − (t − sin θ) tan θ, and the length is cos θ + sin θ tan θ = 1/cos θ; the two expressions
agree at t = sin θ and the first is increasing, so on [0, cos θ] the chord is their minimum. Since
t ≤ h₀ ≤ cos θ for θ ≤ 45°, the third regime (t > cos θ, chord shrinking) never occurs. For θ = 0
the chord is 1 on 0 < t < 1 and h₀ < 1. ∎

**Corollary (touchers).** A square touching w (y_min = 0) has t = h₀ ∈ [sin θ, cos θ] for every
θ ∈ [0, 45°], hence φ_w = 1/cos θ EXACTLY — the projection of the square onto w is cos θ + sin θ
≥ 1/cos θ, with equality only at θ = 0 and θ = 45°.

**Why h₀ = 1/√2.** For a toucher at tilt θ the chord at height h equals the maximal value
1/cos θ iff h ∈ [sin θ, cos θ]; h₀ is the unique height in that interval for ALL θ ∈ [0, 45°]
(the interval degenerates to {1/√2} at θ = 45°). A91's chord lemma (`frame_census.md` F2(iii))
used h = 1/2, giving 1/cos θ for θ ≤ 30° and 1/sin 2θ ∈ [1, 1.155) above — WALL-F at h₀ dominates
it for every θ (1/cos θ ≥ 1/sin 2θ ⟺ θ ≥ 30°). On Trump the two heights give 3.283/3.000/3.309/
2.630 vs 3.000/3.000/3.014/2.014 (§5).

### 1.2 [T] Corollary WALL-3 (per-wall count and the tilt slack)

(a) At most 3 squares touch any wall (each toucher has φ ≥ 1, 4 > ŝ). This is A31/A43's N1 and
A91's F2(iii) with a sharper constant. (b) If three squares touch w, Σ_i (1/cos θ_i − 1) ≤ m − 3
< 0.877084. (c) In particular an upright plus two 45° diamonds needs 1 + 2√2 ≤ m, i.e. m ≥
3.828427: for m ∈ [3.82, 1 + 2√2) a wall carries at most ONE diamond alongside two others, and a
wall cannot carry two tilted touchers with 1/cos θ₁ + 1/cos θ₂ > m − 1. (The threshold 1 + 2√2 is
A47's s* and Lemma COL's ghost boundary: the same number, the same mechanism — three unit widths
of which two are diagonal.) (d) [S] Squares not touching w but with y_min < h₀ − sin θ also have
φ_w = 1/cos θ ≥ 1; the count of "unit-footprint" squares (φ_w ≥ 1) per wall is ≤ 3 as well.

### 1.3 [T] Lemma WALL-NP — the projection width is not a budget (correction to the brief)

The brief prices a tilted wall member at width cos t + sin t. That is unsound: the projections of
two interior-disjoint wall-touching unit squares onto the wall can overlap.

*Counterexample.* Q with tilt 20° and lowest vertex at the origin (edges e₁ = (cos 20°, sin 20°),
e₂ = (−sin 20°, cos 20°)); P the 45° diamond whose rightmost vertex lies on the line through Q's
left edge, P ⊂ {⟨·, e₁⟩ ≤ 0}: P has vertices (−0.2574, 0.7071), (−0.9645, 1.4142), (−1.6716,
0.7071), (−0.9645, 0) — it touches the wall at its bottom vertex, and max_P ⟨·, e₁⟩ = 0, so P and
Q are separated by Q's left-edge line and are interior-disjoint. Projections: P → [−1.6716,
−0.2574], Q → [−0.3420, 0.9397], overlap 0.0847 > 0. (Verified numerically,
`code/wallcanary97.py` companion check; `results/`.) The chords at h₀ touch exactly at
x = −0.2574 = −h₀ tan 20° (P's rightmost vertex is Q's left chord end) — WALL-F is tight there. ∎

The overhang a neighbour can steal from a toucher at tilt θ is sin θ − h₀ tan θ = sin θ (1 −
h₀/cos θ), maximal ≈ 0.092 near θ = 30°, zero at 0° and 45°. So a budget in projection widths
over-counts a tilted toucher by up to 0.092 and would wrongly exclude packings; the sound width of
a wall member is 1/cos θ, not cos θ + sin θ.

### 1.4 [T] Footprints of corner intruders

In corner c's frame, let Q intrude c with depth d = d_c(Q) > 0: some p ∈ int Q has max(p_x, p_y)
< 1 − d. Then y_min(Q) ≤ p_y < 1 − d and x_min(Q) < 1 − d, so on BOTH wall lines of c
  t ≥ d − (1 − h₀) = d − 0.292893,   φ ≥ F(d, θ) := min(2(d − 0.292893)⁺ / sin 2θ, 1/cos θ)
(θ > 0; for θ = 0, φ = 1 as soon as d > 0.292893). Conversely: **[T] an intruder with φ_w = 0 on
one of its corner's walls has depth ≤ 1 − h₀ = 0.292893** (y_min ≥ h₀ forces every point of Q to
height ≥ h₀, so 1 − d = min max(p_x, p_y) ≥ h₀). The constant is Theorem CEIL's (the two are the
same geometry: a square with no point below h₀ cannot reach past the diagonal point (1−h₀, 1−h₀)).
A slot-adjacent axis-aligned square [a, a+1] × [b, b+1] with max(a, b) ≤ h₀ has φ = 1 on both
lines; with a ∈ (h₀, 1) it has φ = 1 on the bottom line and 0 on the left line.

## 2. Jams

### 2.1 Definition and the pair's footprint

A **JAM corner** (cases85's stratum, `tilt_floor_k0.md` Lemma JAM-0) at c, in c's frame: an
axis-aligned S = [a, a+1] × [b, b+1] with g := max(a, b) ∈ (0, 0.1] (g = 0 is a slot square, k ≥ 1,
outside k0_00; g < δ_pin = 0.02 is the K0-REUSE pocket, k1_00's tree), and a partner N with a
vertex in the L-strip U = ((0, a) × (0, 1)) ∪ ((0, 1) × (0, b)), tilt α with sin α ≤ g (≤ 5.74°)
and depth ≤ ν(g) := g²/√(1 − g²) ≤ 0.010050. By the diagonal reflection WLOG N's vertex v lies in
the LEFT strip (v_x < a, so a > 0); by JAM-0's proof v is N's LOWEST vertex with sin α ≤ v_x < a
(the leftmost-vertex sub-case of the proof is vacuous: it forces N to pass under S), hence
N ⊂ {y ≥ v_y} with v_y ≥ 1 − ν(g) (v_x < 1 − ν and d_c(N) ≤ ν). The **nick wall** of the jam is
the wall of the strip (here x = 0); the other wall is its **pusher wall**.

**Lemma WALL-J1 [T].** A jam pair has φ = 1 (S) + 1/cos α (N) ∈ [2, 2.00504] on the nick wall's
line and φ = 1 (S) + 0 (N) on the pusher wall's line.
*Proof.* S: x-range [a, a+1] ∋ h₀ and y-range [b, b+1] ∋ h₀ (a, b ≤ 0.1 < h₀ < 1), interior chords
of length 1 on both lines. N on the nick line x = h₀: N's leftmost point is v + (−sin α, cos α) at
x_min = v_x − sin α ∈ [0, a), so t = h₀ − x_min ∈ (h₀ − 0.1, h₀] ⊂ [sin α, cos α] and the chord is
1/cos α. N on the pusher line y = h₀: y_min(N) = v_y ≥ 1 − ν > h₀, chord empty. ∎

### 2.2 [T] The pusher is a free square; the jam count

At the Ψ-minimal σ-minimiser (NOCRIT-SEL, `nocrit_k0_blocked.md` §3), S is x-side if a > b,
y-side if b > a, corner-type if a = b (Lemma K, axis-aligned case), and by Corollary 2 it is
PRESSED in each cardinal retreat direction by a neighbour on its far side: an x-side S by a square
R with an active row on S's right edge {a+1} × [b, b+1] or at its right corners, pushing S toward
−e_x; a y-side S by a square T on its top edge {y = b+1} × [a, a+1] or top corners. Call the
pressing square(s) the **S-pusher(s)**. (N itself presses S at the corner (a, b+1) with force
(sin α, −cos α)λ — toward +e_x and −e_y — so N is S's pusher only in the y-side case; in the
x-side case R ≠ N.)

**Lemma WALL-J2 [T].** Every S-pusher is a FREE square (intrudes no corner) or a third intruder of
the jam's own corner; S-pushers of distinct jams are distinct squares.
*Proof.* An S-pusher has a point on S's far edge, at height ≤ b + 1 ≤ 1.1 (x-side) resp. at
abscissa ≤ a + 1 ≤ 1.1 (y-side), and diameter √2, so all its points have y ≤ 2.52 resp. x ≤ 2.52
< m − 1 ≥ 2.82: it cannot meet the two far corners' slots (which need y > m − 1 resp. x > m − 1).
For the x-side pusher R and the adjacent corner BR: R has a point with x = a + 1 ≤ 1.1, so
x ≤ 2.52 < m − 1 — not a BR intruder; for TL (needs x < 1, y > m − 1): y ≤ 2.52. Symmetrically for
T. R meets the BL slot (0, 1)² only through the sliver under S's bottom-right corner when b > 0
(the edge-interior contact forces R ⊂ {x ≥ a + 1}; the top-corner contact with normal n_x > 0
puts R's points with x < a + 1 above y = b + 1 > 1), i.e. only as a third BL intruder.
Distinctness: pushers of adjacent jams along a wall have points at x ≤ 1 + a and x ≥ m − 1 − a′
(distance ≥ m − 2.2 > 1.62 > √2), pushers of opposite jams likewise in the other coordinate. ∎

**Lemma WALL-J3 [T] (jam count).** A K0-BLOCKED packing has j ≤ 3 jam corners.
*Proof.* Eleven squares ≥ Σ_c (intruders of c) + (free pushers) ≥ 8 + j: each jam contributes a
distinct pusher that is either free or an extra (third) intruder of its corner. ∎
(cases85 kills JAM⁴ by its free-square demand; WALL-J3 is that count made exact.)

### 2.3 The pusher's footprint and hypothesis P-ON

For an x-side S the pusher R has a point at height y_c ∈ [b, b + 1] on the pusher wall's line's
side, so y_min(R) ≤ y_c ≤ 1.1 and φ_pusher-wall(R) = φ(h₀ − y_min(R), θ_R): equal to 1/cos θ_R
≥ 1 iff y_min(R) ≤ h₀ − sin θ_R (in particular if R touches the wall), positive iff y_min(R) < h₀,
and ZERO iff y_min(R) ≥ h₀. Nothing in NOCRIT-SEL / LOCK / MENU forces y_min(R): MENU is the lock
menu of the tilted wall-touching blocker N (far-side contacts of N), not of S, and S — axis-
aligned — has nothing to lock; its only obligation is to be pressed and anchored (Lemma COL: a
horizontal contact column S → R → … → the right wall of ≥ 3 members, or a BR intruder deepening),
and column members carry no height constraint.

**Hypothesis P-ON (jam c).** Some S-pusher of c has φ ≥ 1 on the pusher wall's line, i.e. y_min ≤
h₀ − sin θ (touching the wall suffices). **Tilted pushers** are allowed and cost 1/cos θ_R ≥ 1: they
only tighten the budget. **Corpus [M, `results/corpusjam97.json`]:** the exact K0-BLOCKED corpus
(the four polished k0dir87 endpoints with exact z, all at σ = 4.000; Trump as control) contains
three JAM corners in cases85's sense — s0380@4.000000 BR (S = sq3 at g = 0.0564, x-side, partner
tilt 0.020°), s0076@4.000004 BR (g = 0.0504, y-side, partner 0.116°), s0380@4.000007 BR (g =
0.0572, x-side, partner 0.128°, pusher not within 10⁻⁴). The two with a detected pusher have it
FLOATING: sq9 at y_min = 0.764 (tilt 3.13°) and sq10 at 0.942 (tilt 2.54°) above the pusher wall,
footprint 0, touching no wall, intruding no corner. **P-ON fails 3/3 (2 measured, 1 pusherless).**
The brief's "on-wall pusher in every deep jam" is not what d1max87 recorded either: its "side
pusher" is N's far-edge contact (§5.2's K > 0), always a wall-free `free_square`.

**(d) The above-wall lock.** A downward contact at S's outer top vertex (a+1, b+1) pressing S
toward −e_x (a square T′ with an edge over the corner, inward normal n_x > 0) is an S-pusher in the
sense of §2.2; its footprint is φ(h₀ − y_min(T′), θ′), zero iff y_min(T′) ≥ h₀. So the vertex
presser EVADES the budget exactly when it floats above h₀ — the same residue as E1.

### 2.4 [T] Lemma FLOAT — the pocket pays in area what it saves in wall length (PI follow-up)

**Lemma SHADOW.** Let Q be a square in {y ≥ 0} with y_min(Q) < h₀ and chord [c_L, c_R] on the
line y = h₀ (nonempty: y_max ≥ y_min + 1 > h₀). Then every point of Q with x < c_L or x > c_R has
y > h₀; i.e. Q ∩ {y ≤ h₀} ⊂ [c_L, c_R] × [0, h₀].
*Proof.* Upright: the chord spans Q's full width. Tilt θ ∈ (0, 45°], lowest vertex (x_v, y_v),
t = h₀ − y_v ∈ (0, h₀] ⊂ (0, cos θ] (y_v ≥ 0): the line meets Q's left edge (direction
(−sin θ, cos θ) from the lowest vertex, length 1, rising to height y_v + cos θ ≥ h₀) at
c_L = x_v − t tan θ. Q lies on the right/upper side of its left-edge line, so a point of Q with
x < c_L has y ≥ y_v + (x_v − x) cot θ > y_v + t = h₀, and Q has no points left of the edge's
x-range at all. The right side is the mirror (the line meets the right edge or the edge R→TR,
in both cases at a point below which Q has nothing to the right: for t ≤ sin θ the right edge
rises from the lowest vertex at slope tan θ and Q lies above it; for t ∈ [sin θ, cos θ] the
points of Q right of c_R lie above the edge R→TR, which has height ≥ h₀ there). ∎

**Lemma FLOAT.** Let c carry a jam nicked on the left wall (S = [a, a+1] × [b, b+1], nick
partner N in the left strip), and let P := (a+1, a+2) × (0, h₀) — the strip beside S on the
pusher wall, area h₀ = 0.7071. Let L := Σ_{Q ≠ S} |chord_{h₀}(Q) ∩ (a+1, a+2)| ∈ [0, 1] be the
wall-line length spent in (a+1, a+2) by the other squares (WALL-F: the chords are disjoint).
Then the area of P covered by no square's interior is ≥ h₀ (1 − L). In particular EITHER the
bottom line carries S plus a chord budget L in (a+1, a+2) (an on-wall or near-wall pusher, or
any wall toucher under the floating pusher: L = 1 exactly when that square has a unit chord
there — case (b), P-ON) OR the pocket strands area ≥ h₀ (1 − L) (case (a)); a floating pusher
with an empty pocket strands exactly h₀ = 0.7071.
*Proof.* A square Q meeting P has a point p ∈ P with p_y < h₀, so y_min(Q) < h₀ and Q's chord
at h₀ exists; by Lemma SHADOW p_x ∈ [c_L(Q), c_R(Q)], so Q ∩ P ⊂ ([c_L, c_R] ∩ (a+1, a+2)) ×
(0, h₀) and area(Q ∩ P) ≤ |chord_Q ∩ (a+1, a+2)| · h₀. Q ≠ S (S ⊂ {x ≤ a+1}), and any pusher R
with y_min ≥ h₀ does not meet P. Summing over the squares meeting P: covered area ≤ h₀ L. ∎
Remarks. (i) No hypothesis on the pusher is needed: for an on-wall pusher L = 1 and the bound is
vacuous, which is right — the wall is spent instead. (ii) The same holds for y-side and corner-
type jams: the presser T of S sits at y ≥ b + 1 > h₀ and never meets P, N is in the left strip
at y ≥ 1 − ν > h₀; so EVERY jam carries the pocket on its pusher wall. (iii) The trade-off is
exactly linear: area ≥ h₀ (1 − L), wall length L; the pocket cannot be bought for less than
h₀ (1 − L) + L·(a wall unit) — the PI's "the floating pusher escapes WALL-F but pays in area".
(iv) The pocket is disjoint from every corner box (P ⊂ {x > 1} ∩ {y < h₀}, and a + 2 ≤ 2.1 <
m − 1) and from the jam's own corner; for the four-corner composition it is clipped to the BL
quadrant, w := min(1, m/2 − a − 1) ≥ 0.81 (≥ 0.8385 at ŝ with a = 0.1), giving ≥ h₀ (w − L_w) with
L_w the chord length spent in (a+1, a+1+w) — clipping only matters when both corners of the
pusher wall are jams pocketed on it (WALL-J4 (c)).
(v) [M, `results/corpusjam97.json`, grid 400 × 280] On the three corpus jams: s0380 BR
(x-side, pusher sq9 floating at 0.764): L = 0, NOTHING meets P, stranded 0.7071 = h₀ exactly;
s0380@4.000007 BR (x-side): L = 0, stranded 0.7071; s0076 BR (y-side, presser sq10 at 0.942,
diagonally reflected so the nick is on the left): L = 0.0214 (sq6's chord just enters), stranded
0.7064 ≥ h₀(1 − L) = 0.6920. Lemma FLOAT is sharp on the corpus: the floating-pusher jams strand
the whole pocket.

**Consequence for WALL-S (case (b)).** If a wall toucher (or any square with a unit chord in
(a+1, a+2)) sits under the pusher, the pusher wall carries S + 1 = 2 in (a, a+2) and Lemma
WALL-S applies to the far corner of that wall with 1 + L in place of 1 + 1/cos α: its crowd
keeps ≤ 1 unit-footprint member there, and for a unit-footprint D the partner satisfies
dist_w(P) ≥ h₀ − (m − 2 − L)·sin 2θ_P / 2 ≥ L/2 − 0.2314 — a floor as soon as L > 0.4629,
reaching 0.2686 at L = 1.

### 2.5 [T] Two jams on one wall; the maximum count

Let jams sit at the two corners of wall w.
 (a) Both nicked on w: Σφ_w ≥ 2 + 2 = 4 > m. **Impossible.**
 (b) Exactly one nicked on w (nick pair 1 + 1/cos α, the other jam's S): Σφ_w ≥ 3 + (1/cos α − 1),
     so everything else on w — the second jam's pusher, the free squares, both nick partners'
     supporters — has total footprint ≤ m − 3 − (1/cos α − 1) < 0.877084; in particular no third
     square touches w, and the second jam's pusher satisfies y_min > h₀ − 0.4385·sin 2θ ≥ 0.2686.
 (c) Neither nicked on w: Σφ_w ≥ 2 from the two S's; both nicks are on the perpendicular walls.
 (d) Under P-ON at both jams: every jam loads BOTH its walls by ≥ 2 (nick wall S + N; pusher wall
     S + R), so two jams on one wall give ≥ 4 > m: **impossible**; jams are at opposite corners
     and j ≤ 2; with j = 2 every wall carries ≥ 2 from the jams and ≤ 1 further unit footprint.
 (e) Without P-ON: j = 3 is compatible with the budget (three nick walls distinct, each nick wall
     ≥ 3 + …, all three pushers floating — the pocket configuration at all three), j = 4 is dead
     by WALL-J3; the nick walls of any jam set are pairwise distinct (by (a)), so j jams use j
     distinct nick walls in a pinwheel.
Corpus: no configuration with two jams on one wall exists in the exact corpus (3 jams, all at BR
of their configurations); d1max87's `s0380` carries JAM at BR plus two nicked-BLOCK corners at TL.

### 2.6 [T] The shell (Lemma SLIDE) and the live offsets

A jam has d₂(c) ≤ ν(g) ≤ 0.010050; Lemma SLIDE (`k0_blocked_side.md` §3.1, ∀-packings modulo
K0-O1) gives d₂(c) ≥ ŝ − m at every corner of a K0-BLOCKED packing at side m < ŝ. Hence a jam of
offset g exists only at m ≥ ŝ − ν(g), and at side m the live offsets are g ∈ [g_min(m), 0.1] with
ν(g_min) = ŝ − m: g_min = 0.02 (the pocket edge) at m = ŝ − 4.0·10⁻⁴, g_min = 0.05 at ŝ − 0.0025,
g_min = 0.1 at ŝ − 0.01005; below ŝ − 0.01005 there are no jams at all. Everything in this file
about jams concerns the top 0.0101 of the window.

### 2.7 [T] Lemma WALL-S — the squeeze on the neighbours

Let c carry a jam nicked on wall w (S + N: 1 + 1/cos α), and let c′ be the other corner of w with
intruders D, P (depths d₁ ≥ d₂). Then on w's line
  φ_w(D) + φ_w(P) + Σ_{others} φ_w ≤ m − 1 − 1/cos α < 1.877084,
with φ_w(Q) = min(2(h₀ − y_min(Q))⁺ / sin 2θ_Q, 1/cos θ_Q) (θ_Q > 0) resp. 1[y_min < h₀] (θ_Q = 0).
Consequences.
 (i) At most one of D, P has a unit footprint on w; if D touches w (or has y_min ≤ h₀ − sin θ_D)
     then y_min(P) > h₀ − (0.877084 − (1/cos θ_D − 1))·sin 2θ_P / 2 ≥ h₀ − 0.4385·sin 2θ_P, and
     for an axis-aligned P, y_min(P) ≥ h₀: P is entirely above the line, hence (§1.4) d₂ ≤ 0.2929
     and P's intrusion of c′'s slot comes from the perpendicular wall's side: P ∩ (0,1)² (c′-frame)
     ⊂ {y ≥ h₀}, so P's intruding points have their w-coordinate ≥ h₀ and P's "reach" along w
     toward c is bounded by its chord on the line y = h₀… which is empty: P's whole body lies in
     the strip y ≥ h₀, and its extent along w is ≤ √2 from its intruding point.
 (ii) Under P-ON the same holds on the PUSHER wall with 1 + 1/cos θ_R in place of 1 + 1/cos α, and
     then the c′ crowd's unit-footprint member on that wall has its chord to the right of R's: its
     leftmost point at height h₀ is ≥ a + 1 + 1/cos θ_R ≥ a + 2, i.e. the crowd's reach along w
     toward the jam stops at the pusher's far chord end (the brief's "collision of the pusher
     with the crowd's reach region" made exact: reach region ∩ {y = h₀} ⊂ [a + 2, m]).
 (iii) OFFSET-UPRIGHT (cases85 OTHER) corner c′: axis-aligned member D at distance a′ from w
     (and some offset from the perpendicular wall), tilted partner P nicking one of the two gaps.
     D has φ_w = 1 iff a′ ≤ h₀. So with a jam nicked on w, EITHER a′ > h₀ = 0.707 (D off w's
     line) OR the partner floats off the line: dist_w(P) := its lowest point above w satisfies
     dist_w(P) ≥ h₀ − 0.4385 sin 2θ_P ≥ 0.2686. If P nicks the gap between D and w (width a′),
     P has a point at distance < a′ from w, hence a′ > 0.2686 in both cases: **a FLOOR on the
     offset of an OTHER corner adjacent to a jam along its nick wall, not a cap.** If P nicks
     the gap between D and the perpendicular wall (Trump's TL: D = sq4 hugs the left wall,
     a′ = 0, the nick is in the top gap, and P = sq6 has left-wall distance 0.8317 ≥ 0.2686),
     the constraint is on P's wall distance only and D may hug w — Trump-safe.
 (iv) Two-jam case (P-ON, opposite jams at BL, TR): each of TL, BR has both its walls loaded by 2
     and keeps at most one unit-footprint member on each — its pair is "one wall member per wall".

## 3. Composition with the corner charges (T2)

### 3.1 The charges

A47's 54-entry corner table charges ONE square by (centre cell, tilt bin): the wall-hugging
near-upright cell C_x0_x0_b0_1 ([0.49, 0.7]², tilt ≤ 1°) is EXACTLY 0, the far cell [0.9, 1.1]²
at tilt ≤ 1° is 0.854. charge85 (A85 chore, `charge85.{pairs.jsonl,summary.json}`, 200-pair
sample by stratum, complete at close-out, exact certified lower bounds clipped to the quadrant):
JAM min 0 / median 0.203 / max 0.344 (n = 40); BLOCK 0 / 0.598 / 1.234 (40); WEDGE 0.023 / 0.453 /
1.051 (40); OTHER[0.1, 0.3) 0.121 / 0.293 / 0.492 (20); OTHER[0.3, 0.5) 0.348 / 0.609 / 0.746 (20);
OTHER[0.5, 0.7) 0.449 / 0.707 / 1.012 (20); OTHER[0.7, 1.0) 0.020 / 0.641 / 1.063 (20). The
budget lemma (A23 Lemma 2): Σ_c charge(c) ≤ E(m) = m² − 11 ≤ 4.03178. The chore's own
four-corner composition: at E(s0) only 10 465 of 2.02·10⁸ sampled four-corner orbits (5.2·10⁻⁵)
are dead by area, no OTHER bin is fully dead beside three minimal non-jam corners, and even
"4 × same-bin OTHER" dies only for some pairs in the [0.5, 0.7) and [0.7, 1.0) bins (four_max
4.05 / 4.25 vs 4.03). (Sample minima are measured, not certified minima over the strata; the
qualitative reading — near-zero minima in JAM/BLOCK/WEDGE, growth with g in OTHER — is A47's
zero-cell law and Trump's TL at 0.69.)

### 3.2 [T+M] Dead by area? No, for every j — also with Lemma FLOAT

**Composition rerun with the pocket (PI follow-up).** By Lemma FLOAT every jam corner carries
min over L ∈ [0, 1] of {area h₀ (w − L) in its pocket, plus wall length L on its pusher wall}
with w ≥ 0.8385 (quadrant clip; w = 1 when the pusher wall's other corner is not pocketed on
it). Since the area term is ≤ h₀ w ≤ 0.7071 per jam and j ≤ 3, the jams contribute ≤ 3 × 0.7071 =
2.12 of area in the best case for the prover (all pushers floating, L = 0: exactly the corpus
picture), and the 4 − j non-jam corners contribute ≥ their charge85 sample minima (0 / 0 / 0.023
/ 0.121 for BLOCK / JAM / WEDGE / OTHER[0.1, 0.3)), so
  j = 0: ≥ 0;  j = 1: ≥ 0.707 (+ 0);  j = 2: ≥ 1.414;  j = 3: ≥ 2.121  — all < E(m) ≥ 3.83.
At the other end (L = 1 at every jam) the area term is 0 but P-ON holds at every jam, so j ≤ 2
at opposite corners and each pusher wall is loaded by 2 (WALL-J4 (d)); the far corners keep ≤ 1
unit-footprint member per wall and get the WALL-S floor — still no area kill, since a corner
with one wall member and one floating member is a charge-0 BLOCK pair. Mixed L interpolate
linearly. **Verdict: the four-corner sum never exceeds 4.0318 for any j ∈ {0, 1, 2, 3}; the
maximum jam count stays 3 unconditionally (2 opposite under L = 1 everywhere, i.e. P-ON), with
j = 3 now costing ≥ 2.12 of the ≤ 4.03 budget in area when all three pushers float and ≥ 3 wall
units (one per pusher wall) when they do not; the offset floor on an OTHER neighbour is 0.2686
on a nick wall and L/2 − 0.2314 (for L > 0.4629) on a pusher wall.** What Lemma FLOAT changes
is the accounting, not the verdict: a jam is no longer "area-free" — it is worth h₀(1 − L) of
area — so a certificate that prices the three corners around a jam by their pair charges may add
0.707(1 − L) for the jam; whether that closes anything is a question for the crowd certificate
(A92 Lemma CW with the pocket as an exempt box, priced by an LP, not here [C]).

The pre-FLOAT accounting, kept for the record: j jams charge ≈ 0 each (JAM stratum). The 4 − j remaining corners are squeezed by Lemma WALL-S
only on the wall lines they share with a jam (nick wall; pusher wall under P-ON): the constraint is
"Σφ_w(pair) ≤ m − 2 − …", which [M, `results/wallcensus97.json`, sound box-level lower bounds
φ_lb over the 644 boxes and 7 044 realisable pairs] is violated by only 378 / 7 044 = 5.4 % of the
pairs on a given line (758 = 10.8 % on at least one of the two lines; 511 = 7.3 % have both members
unit-footprint on a line; 0 pairs violate on both lines at once). The surviving 89 % contain the
charge-0 BLOCK pairs and the 0.023 WEDGE pairs (their minimum-charge members are wall-adjacent
near-flush pairs with one member above the line — exactly the flush-parking evasion of A47 §4).
Hence the forced sum is  j·0 + (4 − j)·≈0 ≪ E(m)  for j = 0, 1, 2, 3: **not dead by area**, and
no offset cap follows: an OFFSET-UPRIGHT corner of any offset g ≤ 1 charges ≤ 1.06 in the sample
(≤ 1 in the corner box by CEIL's corollary) against a budget of 4.03 shared with three corners
that can charge 0. The composition inequality is slack by ≥ 2.9 in every pattern.

### 3.3 What the wall budget denies and what it leaves

Denied: on a jam's nick wall, both neighbouring intruders in the unit-footprint class — in A47's
cells, the class is {centre's wall distance c ≤ h₀ + (cos θ − sin θ)/2} (c − (cos θ + sin θ)/2 ≤
h₀ − sin θ): the whole [0.49, 0.7] wall column at every feasible tilt, the [0.7, 0.9] column at
tilt ≤ 29.2° (0.9 ≤ h₀ + (cos θ − sin θ)/2 ⟺ θ ≤ 29.2°), and the [0.9, 1.1] column at tilt ≤
11.2°. Available to the adversary: one member anywhere, the other in the [0.7, 0.9] column above
29.2°, the [0.9, 1.1] column above 11.2°, the (40, 45] bins, or off the table (wall distance >
1.1) — and, with no P-ON, everything on the pusher wall. The A47 zero cell itself (C_x0_x0_b0_1) is a unit-footprint cell on both lines; it is
the jam's S cell, and a second zero-cell square on the same wall line is allowed (3 units fit)
unless the wall already carries a nick pair AND a pusher. So the zero cell is not denied; the
budget denies the THIRD unit footprint on a wall that carries a nick pair plus one more.

## 4. Verdict and consumers (T3)

### 4.1 [T+M] Box-level consumption — the (C-wall) leaf

For a node with corner-crowd boxes B (centre box [x0, x1] × [y0, y1], tilt cell [θ0, θ1]) the
sound footprint lower bound on the line of wall w is
  φ_lb(B) = min(2 t_lb / sin 2τ_max, 1/cos τ_min) if t_lb := h₀ − c_⊥,max + h_min > 0, else 0,
with c_⊥,max the largest centre coordinate perpendicular to w in the box, h_min = min over the
cell of (cos θ + sin θ)/2 and [τ_min, τ_max] the tilt image of the cell (`code/wallcensus97.py`).
Leaf rule: kill the node if Σ_{B assigned to w} φ_lb(B) > m_hi for some wall (the free squares'
boxes included when localised; unlocalised squares contribute 0 — sound). It is exact, LP-free,
and monotone in the box (a sub-box has larger φ_lb). Census effect at the pair level [M]:
178 / 644 boxes have unit footprint on a given line (264 have zero); 7.3 % of the pairs have both
members unit on a line, 10.8 % exceed 1.877 on at least one line — those die as the neighbour of a
jam nicked on that line (or of any corner whose pair sums to ≥ 2 on it). Pattern level: JAM⁴ dead
(WALL-J3 = cases85); adjacent JAM-JAM patterns (JJBB, JJBW, JJWW and JJJ·) die iff both nicks are
on the shared wall — an orientation sub-case, not a pattern kill — and die outright under P-ON
(6 of the 21 D4 patterns, 25 of 81 labelled; ≈ 0.06 % of the labelled 4-tuple census, JAM being
68 / 7 044 of the pairs). The budget's kills are concentrated where the census is thin; A89's
reading "the ghost zone is not where the cost is" stands.

### 4.2 The escape list, with corpus frequency

 E1 Floating pusher / above-wall lock (P-ON false): corpus 3 / 3 jams (§2.3); Trump: no jam.
    PRICED by Lemma FLOAT (§2.4): the pocket strands ≥ h₀ (1 − L) — 0.7071 on every corpus
    jam — so E1 is no longer an escape from the accounting, only from the wall count; the
    sum of pockets (≤ 2.12) still does not reach E(m).
 E2 Crowd members with zero wall footprint: 27.4 % of realisable pairs have no unit-footprint
    member on a given line; [T] such a member has depth ≤ 0.2929 (§1.4), so E2 is exactly the
    shallow (CEIL-side) intruder — the object Lemma SLIDE bounds from below by ŝ − m and A92's
    crowd certificate prices; the wall budget cannot see it and does not need to.
 E3 Tilted on-wall pushers: allowed (MENU is silent about S's pusher), cost 1/cos θ ≥ 1; they
    make P-ON's conclusions stronger, never weaker. Corpus pushers are tilted (2.5°, 3.1°) AND
    floating.
 E4 Sub-case (ii)/(iii) jams (S y-side or corner-type: b ≥ a > 0, S floating off both walls): the
    presser T sits over S's top-right corner (squeezed by N: an upright T must have x_T ≥ a +
    cos α), so it has zero footprint on both lines; the region right of S and below T is again a
    pocket. Corpus: s0076 BR is such a y-side jam (g = 0.0504, pusher floating at 0.942).
 E5 The shell: jams live only at m ≥ ŝ − ν(g) (§2.6) [modulo K0-O1].

### 4.3 What a proof of P-ON would need

P-ON is a statement about where S's horizontal anchoring column runs: if the column S → R → … →
right wall stays above h₀ in its first link, the pocket B is open below it and must be paid for by
area. A lemma "the pocket strands ≥ β" would turn E1 into a charge; the candidate is the A47
corner-table machinery applied to the strip [a+1, a+2] × [0, h₀] with the hypothesis "no square
has a point in it with x ≤ a + 1 + ε" — a PlacedBox certificate of the kind A47 shipped, not a
theorem of this file [C, priced at A47's per-entry cost].

## 5. [M, exact] The Trump canary (`results/trump_wall_canary.{json,md}`, 70 dps from A03's 60-digit data)

| wall | touchers | Σφ(h₀) | slack ŝ − Σφ | contributors (φ) |
|---|---|---|---|---|
| bottom y = 0 | 3 (sq0, sq1, sq2, flush) | 3.282914 | 0.594170 | 1, 1, 1; sq8 (40.18°, y_min 0.5676) 0.282914 |
| left x = 0 | 3 (sq0, sq3, sq4, flush) | **3.000000** | **0.877084 = ŝ − 3** | 1, 1, 1; sq6/sq7 above the line (0) |
| right x = ŝ | 3 (sq2, sq5 flush; sq10 vertex, 40.18°) | 3.308901 | 0.568182 | 1, 1, 1/cos 40.18° = 1.308901 |
| top y = ŝ | 2 (sq5 flush; sq6 vertex) | 2.630367 | 1.246716 | 1, 1.308901; sq9 (y_min 0.5486 below the top) 0.321466 |

Lemma WALL-F: PASS on all four walls; WALL-3: PASS (3/3/3/2 touchers; the three-toucher walls have
tilt slack 0 (left, bottom: three uprights) and 0.309 (right) ≤ 0.877). The left wall is TIGHT in
the sense of the brief — three flush unit widths, exactly ŝ − 3 of free length, all of it the gap
above sq4 (0.8445) plus the 0.0326 gap between sq3 and sq4 — and is the wall the lemma must not
exclude: it does not (3 ≤ ŝ). No wall carries two diamonds (threshold 1 + 2√2 not hit; Trump's
tilted squares are at 40.18° with 1/cos = 1.3089, and the right/top walls carry one each). Jam
clauses: Trump has no JAM corner (TL is OTHER: sq4 axis-aligned at wall distance 0 from the left
wall and offset 0.8445 from the top wall, partner sq6 at 40.18°); WALL-S (iii) is satisfied on the
top wall (sq4's top-wall distance 0.8445 ≥ h₀ ⇒ φ_top(sq4) = 0, consistent with the table), and the
adjacent corners of every wall keep ≤ 1 unit footprint beyond the slot squares. Projection widths
would have summed to 3.409 (right) and 2.730 (top) — also ≤ ŝ here, but that is luck, not a lemma
(§1.3). A85's own Trump TL row (`cases85.json` trump_TL: label OTHER, depth 0.1683/0.1555) is
reproduced by `code/corpusjam97.py` (intruders {4, 6}, no jam).

## 6. Obligations ledger

| # | item | status |
|---|---|---|
| A97-O1 | Lemma WALL-F (footprint budget at h₀ = 1/√2), chord formula, WALL-3 (≤ 3 per wall, tilt slack, 1 + 2√2 threshold) | [T] §1.1–1.2 |
| A97-O2 | Lemma WALL-NP: projection widths are not a budget (counterexample; correction to the brief and to any consumer using cos t + sin t) | [T] §1.3 |
| A97-O3 | Jam footprints WALL-J1; pusher free WALL-J2; j ≤ 3 WALL-J3; two-jams-per-wall WALL-J4 (a)–(e); j ≤ 2 opposite under P-ON | [T] §2 |
| A97-G1 | P-ON (unit-footprint pusher) — corpus 3/3 against; RESOLVED into the dichotomy of Lemma FLOAT (area h₀(1 − L) or wall length L) | [T] §2.4 (Lemma SHADOW + FLOAT); [M] sharp on the corpus (0.7071 stranded) |
| A97-O4 | Lemma WALL-S (the squeeze; zero-footprint ⇒ depth ≤ 0.2929; offset FLOOR ≥ 0.2686 for adjacent OTHER corners) | [T] §2.7, §1.4 |
| A97-O5 | Composition: not dead by area for any j; no offset cap; cells left to the adversary | [T+M] §3 |
| A97-O6 | (C-wall) leaf rule + census (7.3 % / 10.8 % of pairs; JAM patterns ≈ 0.06 % of 4-tuples) | [T+M] §4.1 |
| A97-O7 | Trump canary on every wall, exact | [M] §5 PASS |
| A97-C1 | pocket charge (turn E1 into an A47-type certificate) | DISCHARGED by Lemma FLOAT (exact, no certificate needed); the remaining [C] is whether a crowd certificate (A92 CW) with the pocket as an exempt box closes anything |

Runs (`attempts/A97-wall-budget/code/`, one process each, seconds, no BLAS): `wallcanary97.py`
(exact Trump, 70 dps) → `results/trump_wall_canary.{json,md}`; `wallcensus97.py` (box-level φ_lb
on the 644 sound boxes / 7 044 realisable pairs) → `results/wallcensus97.json`; `corpusjam97.py`
(exact K0-BLOCKED corpus + Trump: jams, pushers, P-ON, per-wall sums) → `results/corpusjam97.json`.
No A57/A60/A61/A96 file or process touched; frozen verifiers untouched.
