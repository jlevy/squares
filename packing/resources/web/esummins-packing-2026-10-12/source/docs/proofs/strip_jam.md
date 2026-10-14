# STRIP₂ IN JAM under H1–H3 alone — what stops the square on every violator of the ring inequalities is X's right boundary casting a shadow over T_u's top (not the C–X wedge); the free-strip-square problem reduces [T] to a statement about a POINT and three CONVEX SETS (the DISC LEMMA), which is [M] true on the whole H1–H3 set with sup slack −0.005 (−0.017 for the square itself) and NOT proved; the case split is on the CENTRE's height, not on X's tilt — A272, 2026-09-23

The brief (A272 BRIEF): STRIP₂ under H1–H3 only — A267's proof needs the ring inequalities (U3)–(U6), (U8), which
A271 showed are FALSE as consequences of H1–H3 while STRIP₂ itself survives every violator; draw where the
square's best attempt sits on each violator and what stops it, then find the proof by cases (the brief's
candidate: on |φ − θ|).  Tags [T] proved, [T-prose] proved in prose with the arithmetic cores in Lean,
[T-computed] finite computation with its own check, [M] measured, [C] conjecture, [F] false.  Code
`attempts/A272-strip-jam/code/` (`upper272` the UPPER-case probe, `left272` the same with the LEFT constraint —
the probe that isolates the mechanism —, `disc272` / `disc272b` the disc-lemma tests, `pages272`); results beside
it; page `docs/residue_map/campaigns/A272-strip-jam/strip_jam.svg` (six panels, exact checks each); Lean
`Statements/Open/StripJam.lean`.  Notation as A267 / A271: corner frame, C the floater (h_u, h_v, θ; c, s;
L = (h_u, L_h), T = (h_u + c, C_top)), T_u = C − h_u e_x, S = T_u ∖ C, X the wall toucher (φ; B_X = (sin φ, X_low),
R_X = (w_φ, Y_R := X_low + sin φ), wall vertex W = (0, Y_W := X_low + cos φ), top X_top), r_X(y) / ℓ_C(y) X's right
and C's left boundary at height y, D := C_top − X_low (X's dip below C's top), Q the free square (centre q,
tilt ψ) with p ∈ int Q ∩ S.  The point T' := (c, C_top) is T_u's top vertex.

## 0. Verdict

**A273 (2026-09-23): the DISC LEMMA below is [F] (exact witness); the corrected DROP LEMMA is in §5's correction note and `attempts/A273-disc-lemma/notes/disc273.md`.**

> **[M] The mechanism on every violator (§1, page (a)–(f)).**  Restricting the probe to squares that could contain a
> strip point (centre above L_h by WEDGE-FLOAT, and LEFT: the part below C_top left of C), the best square on
> every violator is stopped by **X and T_u only** — active terms `gap_X` + `depth_Tu` (+ the LEFT constraint), C's
> gap NEVER active: sup t = −0.080 (U3), −0.179 (U4), −0.170 (U5), −0.175 (U6), −0.031 (U8-minimiser).  Q comes
> from the right, above C_top; to be right of X at every height of X it must clear X's lower-right edge up to its
> own left vertex, and that pushes its bottom right of T_u's top: **X's right boundary casts a shadow over T_u's
> top corner**, the C–X wedge that A267 trapped the chords in plays no part, and neither does A.  Without LEFT
> (`upper272`) the probe's sup is 0 — at h_u → 0, where Q sits RIGHT of C touching T_u's right edge from outside:
> a vacuous boundary (S has width h_u), not a mechanism.  Over the whole H1–H3 set (joint search, `left272`):
> **sup t = −0.0168**, at X FLAT (φ = 0), θ = 15°, h_u = 0.42, with Q flat, its bottom edge ON y = C_top right of
> X's right edge x = 1 (page (f)).  So the worst points are not "X tilted far from C" but X flat over a 15–35°
> C with X's flat bottom just under C's top — every one a (U3)+(U4) violator with (U5) tight.
> **[T] The reduction (§2–§4).**  Every free strip square has centre q above L_h (A267 §1–2); its horizontal
> chords at heights in [X_low, X_top] lie on ONE side of X (NO-LEFT + IVT); its part below C_top is left of C
> (LEFT).  Hence its inscribed disc D(q, ½) misses the two CONVEX sets Ξ := {X_low ≤ y ≤ X_top, x ≤ r_X(y)} (Q
> right of X; Ξ′ := {…, x ≥ X's left boundary} when Q is left of X) and Γ := {h_v ≤ y ≤ C_top, x ≥ ℓ_C(y)}, and
> its strip point p lies within 1/√2 of q outside Ξ ∪ Γ (a DROP conv(D(q, ½) ∪ {p}) ⊂ Q).  The case "q above X_top
> with Q LEFT of X" is dead outright by **Lemma CL** [T]: (D − cos φ) cot φ ≤ c, so the pocket left of X's
> upper-left edge above W misses T_u (Lean `cl_core_i`, `cl_core_ii`).  The other cases (q ∈ (L_h, X_low) with
> Q left of X, q ∈ (L_h, X_low) or [X_low, C_top] or above C_top with Q right of X) all reduce to
> **the DISC LEMMA: no point q with q_y > L_h, dist(q, Ξ) ≥ ½ (resp. Ξ′), dist(q, Γ) ≥ ½ lies within 1/√2 of
> P := S ∖ (Ξ ∪ Γ)** — a statement about a point and three convex sets in the five parameters (h_u, h_v, θ, X_low, φ),
> tilt-free.  Lean `centre_right_core`: Q's a-range crosses T_u's top edge, so only a poke reaches the strip.
> **[M] The DISC LEMMA holds on the H1–H3 set** (§5, `disc272`: centres above C_top, sup slack −0.005, attained
> only with h_v → 1.0000 — the open boundary where C leaves the box — and X flat; −0.047 on the 43 rings and the
> four violators; `disc272b`: centres in (L_h, C_top], right and left of X — see §5 for the numbers).  It is
> **NOT PROVED**: the hand proof by cases did not close, the disc lemma IS the residual, and its price (§6) is a
> box tree over the five parameters with a 2-D convex-geometry test per box, ~10² CPU-h on the H1–H3 set, ~20 on
> the (U3)–(U6)+(U8)-violating part — not launched (no verified kernel exists; A266's tilt-binned `strip266` at
> ~10³ CPU-h is the wrong tool).
> **Statement (§7): STRIP₂-IN-JAM ⟸ H1–H3 + DISC LEMMA** [T-prose]; Lean `strip_two_in_jam_of_disc` (axiom),
> `strip_two_in_ring_of_disc` (the pair3 bridge), cores `d_low_core`, `cl_core_i`, `cl_core_ii`,
> `centre_right_core`; A271's `strip_two_in_jam` under `RingIneq` untouched.  (U8) is FOLDED: the case
> q_y > X_top is Case C of §2, handled by the same reduction — (U8) is not a hypothesis anywhere.
> **What the brief had wrong (§8):** the case split is not on |φ − θ| — the violators' mechanism is uniform and
> the worst points have X FLAT; the C–X wedge ("tall but narrow") is not what stops Q; C is never the active
> obstacle; A267's argument does not survive for small |β| either (its (U3), (U5) can fail at β = 0).

## 1. The violators: where Q's best attempt sits and what stops it  [M, exact geometry check per panel]

`upper272` maximises t = min(gap(Q, C), gap(Q, X), Q_xmin, Q_ymin, depth(Q, T_u), q_y − L_h) over Q (centre, tilt;
grid 11 × 9 × 8 then Nelder–Mead) on adv271's violators and the 43 rings; `left272` adds the LEFT term
−max{x − ℓ_C(y) : (x, y) a vertex of Q clipped to the bands [h_v, L_h], [L_h, C_top]} (ℓ_C is affine on each band,
so the max is at a vertex).  Every Q reported passes the exact SAT check; every panel's configuration passes the
exact H1–H3 check (20 terms ≥ −10⁻⁹).

| violator | β = φ − θ | best Q without LEFT (`upper272`) | best Q with LEFT (`left272`) | active terms | what stops it |
|---|---|---|---|---|---|
| (U3) h_u .39, θ 34.5°, φ 0 | −34.5° | −0.061, ψ 0°, touching X, C, T_u | **−0.080**, ψ 0° | gap_X, depth_Tu, LEFT | X's right edge x = 1; T_u's top is 0.18 left of it |
| (U4) h_u .82, θ 10.4°, φ 28.7° | +18.3° | −0.139, ψ 72° | **−0.179**, ψ 83° | gap_X, depth_Tu | X's lower-right edge up to Q's left vertex |
| (U5) h_u .63, θ 2°, φ 45° | +43° | −0.102, ψ 71° | **−0.170**, ψ 82° | gap_X, depth_Tu | the 45° edge of X |
| (U6) h_u .90, θ 5.7°, φ 45° | +39° | −0.126, ψ 74° | **−0.175**, ψ 81° | gap_X, depth_Tu | the same |
| (U8)-min h_u .59, θ 20.8°, φ 0 | −20.8° | −0.027, ψ 0° | **−0.031**, ψ 0° | gap_X, depth_Tu, LEFT | x = 1; T_u's top vertex is INSIDE X; the exposed sliver is right of x = 1 |
| sup point (`left272` joint) h_u .42, θ 15°, φ 0, h_v .995 | −15° | — | **−0.0168**, ψ 0° | gap_X, depth_Tu | Q flat, bottom edge on y = C_top, left edge on x = 1 |

Without LEFT the near-misses are on the WRONG side of C (b < 0 at a > 1, below C_top: they contain no strip point
and say nothing); with LEFT the picture is uniform: **C's gap is never active**.  The obstacle is X's right
boundary — for φ > 0 its lower-right edge (Q's left vertex must be right of it, and the edge rises at cot φ per
unit height: the higher Q's left vertex, the further right Q's bottom), for φ = 0 its right edge x = 1 — together
with the requirement to reach T_u ∩ {y < C_top}, whose top vertex T' = (c, C_top) is at most w(θ) < 1.415 from the
wall.  On the rings (A267's domain, U3–U6 ≥ 0.04) the LEFT-constrained sup is −0.12 to −0.15: the ring domain
buys margin, not the mechanism.  The joint sup over H1–H3 (58 starts, 55 feasible ends) is −0.0168 at X flat:
STRIP₂ under H1–H3 alone is [M] true with that margin, away from the open boundaries (h_v → 1, h_u → 0, X's
depth in T_u → 0 — all three are where the JAM domain is open and the statement vacuous).

## 2. What is [T] before any case: the three chord facts and (D-low)

All under H1–H3 at a side in [3.82, ŝ] (A271 §1: h_v < 1 < 1.121 ≤ L_h, 1.406 < X_low < C_top, X above C's
upper-left line on a ∈ [0, 1], σ < 1 on T_u), for a unit square Q of the quadrant with int Q ∩ int C = ∅ =
int Q ∩ int X and p ∈ int Q ∩ S.
**(P0) q_y > L_h** — A267 §1–2 (WEDGE-FLOAT, then the centre chord in [0, g) is too long).  [T]
**(P1) LEFT** — Q ∩ {h_v < y < C_top} ⊂ {x < ℓ_C(y)}, and by closure Q ∩ {y = C_top} ⊂ {x ≤ T_x}; Q has no point
at height ≤ h_v (its lowest point is above L_h − 1/√2 ≥ h_v).  So **int Q ∩ int Γ = ∅**, Γ := {h_v ≤ y ≤ C_top,
x ≥ ℓ_C(y)} — CONVEX (ℓ_C is convex in y: a V with vertex at L).  [T]
**(P2) ONE SIDE** — Q's horizontal chords at heights in [X_low, X_top] are all left of X or all right of X (two
chords on different sides: the segment between a point of each crosses X's non-degenerate chords, IVT), and at
least one of them has length ≥ 1 when q_y ∈ [X_low, X_top] (the centre chord, NO-LEFT: the room left of X at any
of its heights is < 1) — then they are all RIGHT of X: **int Q ∩ int Ξ = ∅**, Ξ := {X_low ≤ y ≤ X_top, x ≤ r_X(y)}
— CONVEX (r_X concave: X's lower-right edge then its right edge).  If Q is left of X: int Q ∩ int Ξ′ = ∅ with
Ξ′ := {X_low ≤ y ≤ X_top, x ≥ x_left(y)} (convex: X's left boundary is a V at W).  [T]
**(P3) the DROP** — D(q, ½) ⊂ Q (inscribed disc) and for p ∈ int Q the whole conv(D(q, ½) ∪ {p}) ⊂ Q (convexity:
(1 − λ) D(q, ½) + λ p ⊂ Q); |q − p| < 1/√2 (circumradius).  Hence **dist(q, Ξ or Ξ′) ≥ ½, dist(q, Γ) ≥ ½,
dist(q, P) < 1/√2 with P := S ∖ int(Ξ ∪ Γ)** (p ∉ int Ξ since p ∈ int Q).  [T]
**(D-low)** [T] — X meets int T_u: a point z of X at height X_low + t (0 ≤ t < D) has z_x ≥ (z_y − L_h) cot θ
(T_u's upper-left edge) and z_x ≤ sin φ + t cot φ (X's lower-right edge); so (s − D + t) cot θ ≤ sin φ + t cot φ,
and if φ ≥ θ: **D ≥ (c − sin φ) tan θ** (Lean `d_low_core`); if φ < θ the same computation gives D > (c − sin φ) tan φ.
X's dip below C's top is not a sliver in the direction that matters: r_X(C_top) ≥ sin φ + (c − sin φ) tan θ cot φ.
**(D-high)** [T] — X ∩ int C = ∅ with the positive-slope separator (BLOCKER-SIDE): if T_x ≤ w_φ, X's lower-right
edge passes above T: D ≤ (h_u + c − sin φ) tan φ; if T_x > w_φ (w_φ ≥ 1 > h_u, so R_X is over C's upper-left edge),
R_X is above C's upper-left line: D ≤ s + sin φ − (w_φ − h_u) tan θ.

## 3. The cases, by the centre's height (not by X's tilt)

 A1. L_h < q_y < X_low: the centre chord is in [0, ℓ_C(q_y)), so ℓ_C(q_y) > 1 — needs (U4)'s ℓ_C(X_low) < 1 to fail.
     A1-right: Q's chords at X's heights (if any) right of X.  A1-left: left of X — Q pokes its top into the
     pocket between the wall and X's lower-left edge (chords ≤ sin φ − (y − X_low) tan φ there): its top is at
     most sin φ/2 above X_low, so **X_low − q_y ≥ (1 − sin φ)/2 ≥ 0.146** and (D-low) with X_low > q_y ≥ L_h + (1 −
     h_u) tan θ forces sin φ + h_u > 1, tan θ ≥ (1 − sin φ)/(2(sin φ + h_u − 1)): θ ≥ 11.7°, φ ≥ 30°.  Live [M].
 A2. X_low ≤ q_y ≤ C_top: the centre chord is right of X and left of C: ρ(q_y) ≥ 1 — (U4) fails.  Live [M].
 M.  C_top < q_y ≤ X_top: the centre chord is right of X (NO-LEFT); Q ∩ int Ξ = ∅.  THE case (every probe optimum).
 C.  q_y > X_top: the centre is above X.  (U8)'s case.  C-right: Q's chords at X's heights right of X — then as M
     (only "q_y > C_top and Q right of X" is used there).  C-left: Q's chords at X's heights LEFT of X: the room
     left of X vanishes at W = (0, Y_W), so Q's part below X_top cannot span Y_W: Q's bottom is above Y_W and p ∈ T_u
     lies left of X's upper-left edge at a height in (Y_W, C_top): (p_y − L_h) cot θ ≤ p_x < (p_y − Y_W) cot φ.  The
     difference is affine in p_y, negative at Y_W (> L_h), so it needs (C_top − Y_W) cot φ > c, i.e. **(D − cos φ)
     cot φ > c** — against **Lemma CL** [T]: (D − cos φ) cot φ ≤ c in both branches of (D-high) (Lean `cl_core_i`:
     (h_u + c − sin φ) sin φ ≤ cos²φ + c sin φ ⟸ h_u sin φ ≤ 1; `cl_core_ii`: s + sin φ − (w_φ − h_u) tan θ ≤ cos φ
     + c tan φ, with h_u ≤ 1, tan θ ≤ 1, sin φ ≤ cos φ).  **C-left is dead.**  So (U8) is never needed: C-right is M.
**In every live case (A1, A2, M, C-right) the centre q satisfies the DROP conditions of (P3)** with Ξ (right of X) or
Ξ′ (A1-left), and q_y > L_h.  Nothing else about Q is used from here on — the tilt ψ is gone.

## 4. Where Q's body is  [T]

In cases M and A2 the centre chord is right of X: q_x ≥ r_X(q_y) + ½ with r_X(q_y) > 0 (= 1 for a flat X), and
q_y − L_h > s; in C's frame a_q = c (q_x − h_u) + s (q_y − L_h) > (1 − h_u c) − ½ = a* − ½ (Lean `centre_right_core`:
c r + (1 − c)(½ + c) > 0), so a_max = a_q + (c′ + s′)/2 > a*: **Q's a-range crosses T_u's top edge a = a*; Q's body is
right of it and only a poke of Q reaches the strip** — exactly what the panels show (Q's a_min is 0.03–0.14 short of
a* on the violators).  A267's route bounded that poke by the C–X wedge's width (needs (U3)) after establishing that
E is past the mouth (needs (U4), (U6)) and that the chords are under X (FAR-SIDE, needs (U5)); the panels say the
poke is stopped by X's right boundary alone, i.e. by the DROP's side condition dist(q, Ξ) ≥ ½ — which is why the
reduction of §3 keeps Ξ whole (X's lower-right edge AND its right edge, up to R_X and T_X) instead of the wedge roof.

## 5. The DISC LEMMA  [M on H1–H3; [T] nowhere yet]

> **[F] A273 correction (2026-09-23, `attempts/A273-disc-lemma/notes/disc273.md`).**  The statement below is FALSE on
> H1–H3: exact Fraction witness `witness273` (h_u 17/20, h_v 199/200, tan(θ/2) 7/100, X_low 211/100, X flat) — a centre
> q with dist(q, Ξ), dist(q, Γ) ≥ ½ and a strip point within 1/√2; the disc slack reaches +0.008, the "sup −0.005 at
> h_v → 1" below is an optimiser artefact.  The distance form drops the cone: the reduction (P3) gives the whole DROP
> conv(D(q, ½) ∪ {p}) ⊂ Q, and the corrected **DROP LEMMA** (no (q, p) with the drop missing int Ξ and int Γ, q_x ≥ ½)
> is what A273 certifies — 4 parameters (h_v-invariant), box-valid penumbra test, verified tree over (θ, φ) cells
> outside the corner θ, φ ≤ 5°, where STRIP₂'s own margin → 0 (open layer, hand proof needed).

**Statement.**  *Under H1–H3, no point q with q_y > L_h, dist(q, Ξ) ≥ ½, dist(q, Γ) ≥ ½ has dist(q, P) < 1/√2,
P := S ∖ int(Ξ ∪ Γ); and none with q_y ∈ (L_h, X_low), dist(q, Ξ′) ≥ ½, dist(q, Γ) ≥ ½ has dist(q, S ∖ int Ξ′) < 1/√2.*
By §2–§3 it implies STRIP₂-IN-JAM.  It is a statement about a point and three convex polygons, tilt-free, in the
five parameters (h_u, h_v, θ, X_low, φ) (A, the side, and h_v beyond L_h > 1 enter only through the H1–H3 set).
**Measured** (`disc272`, `disc272b`: the slack t_disc = min(dist(q, Ξ) − ½, dist(q, Γ) − ½, q_y − L_h (or − C_top),
1/√2 − dist(q, P)) maximised over q by a 29 × 21 grid + Nelder–Mead, then jointly over (q, configuration) with
H1–H3 HARD from the violators, the 43 rings and random feasible starts; every reported configuration passes the
exact H1–H3 check):
 * centres above C_top (case M): sup over the 55 fixed configurations −0.047 (a ring), over the H1–H3 set
   **−0.0050**, at h_u = 0.88, θ = 5.9°, X FLAT, X_low = 2.010, C_top = 2.098 and **h_v = 1.0000** — the open boundary
   where C leaves the box (the next rows: −0.0156, −0.0162 at h_v = 0.9997, 0.9991, X flat, θ = 15–18°).
 * centres anywhere above L_h, Q right of X (M ∪ A2 ∪ A1-right): fixed −0.047, joint **−0.0050** — the same point:
   the lower cases add nothing.
 * centres in (L_h, X_low), Q left of X (A1-left): fixed −0.126, joint **−0.122**: far from tight.
 * the square statement itself (`left272`): sup −0.0168 at X flat, θ = 15°, h_v = 0.995 — the disc relaxation
   loses 0.012 of margin and stays negative.
**Why it is tight where it is tight.**  For a flat X with its bottom edge y = X_low a little under C_top, T_u's top
vertex T′ is inside X (whenever c < 1: T′ = (c, C_top) has x < 1 and y > X_low), and the exposed part of S near the
top is the triangle right of x = 1 between X's bottom and T_u's upper-right edge, of height (1 − c) cot θ.  A flat Q
right of x = 1 with its bottom edge on y = C_top has its centre at (1.5, C_top + ½): dist to Ξ = ½, dist to Γ = ½
(if T_x ≥ 1.5), dist to the triangle's top ≈ sqrt(¼ + ((1 − c) cot θ)²) → the slack is ≈ 1/√2 − that, small when
(1 − c) cot θ ≈ ½, i.e. θ ≈ 15–20° — the whole family of §1's worst points.  A hand proof of the disc lemma must
resolve this family with margin ~0.005–0.017: it is a two-obstacle computation in which BOTH X's right edge and
T_u's upper-right edge enter, and none of the one-obstacle lemmas (POKE, WEDGE, the tent) does it.
**What is proved of it.**  Nothing beyond the cases dead before it: C-left (Lemma CL) and the vacuous boundaries.
Two partial facts [T] that any proof will use: (i) the DROP's apex angle at p exceeds 90° (sin of the half-angle =
½ / |q − p| > 1/√2), so p sees a right angle of free directions towards q; (ii) §4: q is right of a* − ½ in C's
frame.  I did not find the proof; the brief's candidate ("the wedge is tall but narrow at the strip's height") is
not it (§8).

## 6. The residual and its price

**The residual IS the disc lemma** (§5) on the H1–H3 set — or, if A271's ring inequalities are kept as hypotheses
where they hold, on R := {H1–H3} ∖ {(U3) ∧ (U4) ∧ (U5) ∧ (U6) ∧ (U8)} (~18 % of the set, A271 §4; every worst point
of §1 and §5 lies in R: (U3), (U4) fail on all of them).  Its certificate is a box tree over (h_u, h_v, θ, X_low,
φ) whose per-box test is 2-dimensional and convex: the bad-centre set B := ((P ⊕ D(1/√2)) ∩ {y > L_h}) ∖ ((Ξ ⊕ D(½))
∪ (Γ ⊕ D(½))) must be empty (`pages272` computes it exactly per configuration: area 0 on every panel), with
inner/outer polygon bounds over a box.  No tilt loop, no SAT over squares: per box ~10⁻³ of A266's `strip266`
sub-cell (535 s), so with a comparable cell count (~10⁴–10⁵ sub-cells at the margin ~0.005 of the flat-X family, the
tree must go fine there) the price is **~10² CPU-h on the H1–H3 set, ~20 CPU-h on R** [M estimate, no kernel
exists yet].  Not launched: the kernel and its verifier are a day's work, and the brief's ≤ 30 CPU-h line is met only
on R with A271's ring inequalities kept as the alternative hypothesis.  Cheaper still would be a proof.

## 7. The statement

**Theorem (STRIP₂-IN-JAM, disc form) [T-prose].**  *Let s̄ ∈ [3.82, ŝ] and A, C, X unit squares of the corner
quadrant with H1–H3 (a JAM corner).  Assume the DISC LEMMA of §5 for this configuration.  Then no unit square of
the quadrant interior-disjoint from C and X has an interior point in S = T_u ∖ C.*  Proof: §2 (P0)–(P3), §3 (C-left
by Lemma CL, every other case reduces to the drop conditions), §5.  ∎  Lean: `Statements/Open/StripJam.lean` —
`DiscLemma` opaque, axiom `strip_two_in_jam_of_disc` [T-prose], theorem `strip_two_in_ring_of_disc` (the BL sectors
of a JAM corner reduce to `pair3` under JamCorner ∧ DiscLemma), cores `d_low_core`, `cl_core_i`, `cl_core_ii`,
`centre_right_core`; A271's `strip_two_in_jam` under `RingIneq` is left in place: the two hypotheses are
alternatives ((U3)–(U6)+(U8) hold on the 43 rings with margin ≥ 0.041; the disc lemma is [M] on all of H1–H3).
**(U8)** is not a hypothesis of either route here: q_y > X_top is Case C, dead (C-left) or reduced (C-right).
**5b of k0_route.md §13** = STRIP₂-IN-JAM [T-prose under (U3)–(U6)+(U8), A271; under the DISC LEMMA, this note] + `pair3`.

## 8. What the brief had wrong

1. "Proof by cases on X's tilt relative to C: |φ − θ| small = A267's argument, large = the new argument."  The
   violators' mechanism is one and the same at β = −34.5°, +18°, +43° (X's right boundary shadows T_u's top, §1),
   and the worst points of the H1–H3 set have X FLAT (β = −15° to −35°); A267's argument does not survive at small
   |β| either — (U3) and (U5) fail at β = 0 when X's right vertex sits at T_u's top edge.  The split that the
   geometry accepts is on the CENTRE's height (§3), and it does not close: it reduces to the disc lemma.
2. "With X tilted far from C, X's lower-right edge is steep, the wedge under it is tall but narrow at the strip's
   height — a unit square in it has width ≥ 1 > the wedge's width there; or POKE through the wedge mouth."  The
   wedge is not what stops Q: C is never an active obstacle (§1), and for β < 0 the wedge NARROWS towards T_u's
   top edge, so its mouth is at the far end.  What stops Q is being right of X at ALL of X's heights (its left
   vertex, not its chords, is the binding point) while reaching a target left of X's right boundary's projection.
3. "Which obstacle stops it — C's upper-left edge? X's lower edge? the wall? T_u's own top edge?"  X's lower-right
   edge or right edge, together with T_u's UPPER-RIGHT edge (the target's boundary); never C, never the wall.
4. "(U8) for θ > 6.5°: derive or fold into the case split" — folded (Case C); no derivation was needed.
5. Right in the brief: STRIP₂ is true on every violator (sup −0.017 over H1–H3 with the LEFT constraint, −0.03 to
   −0.18 on the named violators), and A267's proof, not the statement, is what fails there.

## 9. What NO-JAM(11) still lacks

5b = STRIP₂-IN-JAM + `pair3`: the DISC LEMMA (this note: [M], residual, ~20–10² CPU-h or a proof) OR the ring
inequalities on the JAM-ring family (A271); `pair3` (A262 chain3, `certs/pair3262_index.jsonl` still absent);
5d (indirect jams, FLOAT2); 6's Lean axiom `jam_count`.  General m: §2–§4 are corner-local and s-free; the disc
lemma's five parameters and the numbers 1.406 / 2.82 enter through H1 as in A271.

## 10. Lean, reproduce

`Statements/Open/StripJam.lean`: theorems `d_low_core`, `cl_core_i`, `cl_core_ii`, `centre_right_core`; opaque
`DiscLemma`; axiom [T-prose] `strip_two_in_jam_of_disc`; theorem `strip_two_in_ring_of_disc`; build + audit 0 sorry.
Reproduce (`JAM_COARSE=1` not needed; each ≤ 15 min single-threaded): `python upper272.py fixed`, `python upper272.py
joint 900`, `python left272.py fixed`, `python left272.py joint 900`, `python disc272.py fixed`, `python disc272.py
joint 900`, `python disc272b.py all fixed`, `python disc272b.py all joint 500`, `python disc272b.py leftX fixed`,
`python disc272b.py leftX joint 500`, `python pages272.py` (exact checks: every panel H1–H3 ≥ −10⁻⁹, bad-centre area 0).
