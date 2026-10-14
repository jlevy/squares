# FLAT X — STRIP₂ on the near-flat corner by hand: at φ = 0 the intruder is the FLAT square resting on C's top line with its left edge on X's right edge, its corner (1, C_top) is (1 − c) c from T_u (that is the 0.25 θ² margin, halved by the probe), and every other square is dead by chord/pin inequalities; the corner θ, φ ≤ 5° is [T] — A276, 2026-09-23

The brief (A276 BRIEF): STRIP₂ with X near flat, route R2 only (A274: R1 dead).  Tags [T] proved, [T-computed]
finite computation with its own check, [M] measured, [C] conjecture, [F] false.  Derivation on disk in pieces:
`attempts/A276-flat-x/notes/flatx276_part0..6.md` (the parts are the proof; this document is the statement, the
mechanism and the map of cases).  Code `attempts/A276-flat-x/code/` (`check276` the φ = 0 cross-check, `check276b`
the corner cross-check, `page276`); page `docs/residue_map/campaigns/A276-flat-x/flat_x.svg`; Lean
`Statements/Open/FlatX.lean`.  Notation as A267/A271/A272: corner frame, C the floater (h_u, h_v, θ; c, s; L = (h_u,
L_h), T = (T_x, C_top), T_x = h_u + c), T_u = C − h_u e_x with top vertex T′ = (c, C_top), S = T_u ∖ C; X the wall
toucher (φ; B_X = (sin φ, X_low), R_X = (w_φ, X_low*), w_φ = cos φ + sin φ, X_low* = X_low + sin φ); D = C_top − X_low;
w0 := T_x − 1 = h_u + c − 1; Q the free square (lowest vertex V, tilt ω, left vertex W_L = (x_min, y_WL), right vertex
W_R, centre q); r_Tu(y) = c + (C_top − y) tan θ is T_u's upper-right edge line (T_u ⊂ {x ≤ r_Tu(y)} ∩ {y ≤ C_top}).

## 0. Verdict

> **Theorem FLAT-X [T]** (part 3 §3.6).  *H1–H3, side in [3.82, ŝ], X flat (φ = 0), 0 < θ ≤ 30°: no unit square Q of the
> quadrant with int Q ∩ int C = ∅ = int Q ∩ int X has an interior point in S.  In the only non-dead case (Q entirely
> right of x = 1, or its left vertex above X) every point of Q below C_top is at horizontal distance ≥ 1 − c =
> 2 sin²(θ/2) right of T_u's upper-right edge line.*
> **Theorem CORNER [T]** (part 6 §6.3).  *H1–H3, side in [3.82, ŝ], 0 ≤ θ ≤ 5°, 0 ≤ φ ≤ 5°: the same conclusion.*
> **The mechanism at X flat** (part 2 §2.1): the near-miss is the FLAT square with its left edge on X's right edge
> x = 1 and its bottom edge on y = C_top (touching C only at T); its bottom-left corner (1, C_top) is at distance
> (1 − c) c from T_u — the foot of the perpendicular lies on T_u's upper-right edge just below T′ (1.4).  The probe's
> three equal penetrations (X, C, T_u) split that into (1 − c) c / 2 = c sin²(θ/2): 0.001895 / 0.000304 / 0.0000761 at
> 5 / 2 / 1° against A274's measured 0.00190 / 0.000306 / 0.000078 — the "0.25 θ²" is explained to three digits.
> The brief's "sliver of S above C's top line" does not exist (T_u ⊂ {y ≤ C_top}); the exposed sliver Σ of S right of
> x = 1 (part 1 §1.2) has WIDTH O(θ²) and the intruder never touches it: what it reaches for is T_u's edge just
> below T′, which is only 1 − c left of x = 1 because T′ = (c, C_top).  Tilting Q does not help (Lemma A): its left
> vertex must clear x = 1 up to X_top, which costs sin ω, while V can sink at most (w0 − sin ω) tan ω below C_top.
> **For φ > 0 the flat square is dead outright** (its left edge would have to be right of R_X, x ≥ w_φ > 1, and
> T_x − w_φ < 1), and no second-order near-miss family exists; the pins R_X / T / L leave first-order slack — the
> measured 0.5 θ on the diagonal.  The proof for φ > 0 is the same case split with three pins (part 4 §4.2).
> **Domain and residual**: FLAT-X holds to θ = 30° (the A1 step needs s < 1/2 and (1 + (1 − tan²θ)^½)/2 > cos θ, true to
> 38°); CORNER holds on [0, 5°]², which is exactly A273's open layer; with A273's tree outside the corner (40+/81 cells
> CERT, two capped cells at θ 25–30° still open) STRIP₂-IN-JAM under H1–H3 is now [T] on the corner + [T-computed]
> outside it, except those capped cells.  Nothing here uses the ring inequalities, A, or the DROP lemma.

## 1. What is used from before  [T]
(P0) q_y > L_h (A267 WEDGE-FLOAT); (P1) LEFT: Q ∩ {h_v < y < C_top} ⊂ {x < ℓ_C(y)}, chord at C_top ⊂ [.., T_x], no
point of Q at height ≤ h_v; (P2) ONE-SIDE + NO-LEFT: Q's chords at X's heights are right of X (the left cases: C-left
dead by Lemma CL, A1-left needs θ ≥ 11.7°) — at φ = 0 the room left of X is ZERO, so Q ∩ {X_low ≤ y ≤ X_top} ⊂ {x ≥ 1}
(1.5), and at φ > 0 Q ∩ {X_low ≤ y ≤ X_top} ⊂ {x ≥ r_X(y)} (4.1); (D-low) D > (c − sin φ) tan min(θ, φ); (D-high).

## 2. The geometry at X flat  [T]  (part 1)
(1.1) Dip window: h_u + c > 1 and 0 < D ≤ D_max := w0 tan θ (X's bottom edge above C's upper-left edge at x = 1;
D > 0 by H2).  T′ is under X.  (1.2) S right of x = 1 is the triangle Σ = {y1 < y < y2, 1 ≤ x < r_Tu(y)}, y1 = L_h +
(1 − h_u) tan θ, y2 = L_h + tan(θ/2), width ≤ tan²θ (h_u − c/(1 + c)) — O(θ²).  (1.3) S under X at heights (y1, X_low)
is the channel Κ = {ℓ_Tu(y) ≤ x < 1}, mouth height η = D_max − D < tan θ, widening to the left.  (1.4)
dist((1, C_top), T_u) = (1 − c) c (foot on the upper-right edge, parameter (1 − c) s > 0).

## 3. The case map at φ = 0  (parts 2–3; θ ≤ 30°)
By W_L's height against X: y_WL ∈ [X_low, X_top] ⟹ x_min ≥ 1 ⟹ **Lemma A** (§2.2): with the chord at C_top,
V_x + d_V cot ω ≤ T_x and V_x ≥ 1 + sin ω give d_V ≤ (w0 − sin ω) tan ω ≤ cos ω (so W_L is above C_top, and ω = 0
forces d_V = 0), and on the cap x_L(d) − r_Tu(d) ≥ 1 − c + sin ω − d_V tan ω + d (tan ω − tan θ) ≥ 1 − c.  (B) y_WL <
X_low, x_min < 1: the upper-left edge must reach x = 1 by height X_low, (1 − x_min) tan ω ≤ X_low − y_WL (3.1); with V
above C's upper-left line this gives η ≥ cos ω + sin ω tan θ + (1 − x_min)(tan ω − tan θ) (3.2), impossible since
η < w0 tan θ < tan θ ≤ cos(ω − θ)/c (ω ≥ θ) or η < (h_u + c − 1) tan θ < c − (1 − h_u) tan θ (ω < θ); the sub-case
x_min < h_u uses q_y > C_top (ω > 45°, 1 − x_min ≤ 1/8, V_x > 1.58) and ends in sin ω < s/2.  (C) y_WL > X_top:
V_x ≥ 1 + (1 − D + d_V) tan ω, d_V ≤ w0 tan ω, clearance ≥ 1 − c + tan ω (1 − 2 w0 tan θ) ≥ 1 − c.  Centre-low: A2
dead (chord in [1, T_x), T_x < 2); A1 dead (the inscribed disc's chord at X_low is right of x = 1 while the centre
chord is left of ℓ_C(q_y) < 1 + w0: (1 + (1 − tan²θ)^½)/2 < cos θ is false).  [T-computed] `check276`: 3 200 feasible
Q on 80 random configurations, area(Q ∩ T_u) = 0 always; Lemma A's clearance − (1 − c) ≥ +0.0149; (1.4) exact to 1e−16.

## 4. The case map at 0 < φ ≤ 5°, θ ≤ 5°  (parts 4–6)
**Lemma A\*** (§4.3, φ-free): if Q's left boundary at C_top is on the edge V W_L with x_L(C_top) ≥ x0 ≥ 1, then
d_V ≤ (T_x − x0) sin ω cos ω and every cap point has x − r_Tu(y) ≥ x0 − c − (T_x − x0) tan²θ/4 ≥ 1 − c − w0 tan²θ/4 > 0
(Lean `clearance_core`).  **Pins** (§4.2): (R) Q's chord at X_low* is right of R_X: x ≥ w_φ; (T) chord at C_top ⊂
[r_X(C_top), T_x]; (L) chord at y ∈ (h_v, C_top) ⊂ [0, ℓ_C(y)), ℓ_C ≤ h_u + s below L_h.  Two chord tools: (T-chord)
x_min + 1/sin ω + (C_top − y_WL) cot ω ≤ T_x when W_R is above C_top; (L-chord) the same with L_h and h_u.
Regimes: (I) D ≤ sin φ (R_X above C_top), (II) D > sin φ.  **Cases** (q_y > C_top):
 (α) y_WL ≥ X_low* (I) or y_WL ≥ C_top (II): (R) resp. X's right edge puts x_L(C_top) ≥ 1 — Lemma A\*.  Dead.
 (β) I, y_WL ∈ [C_top, X_low*): d_V = cos ω − u; T-chord forces ω > 27°; then either V ≥ h_u and cos ω ≤ 0.19 so (R)
     gives x_min > 1 (Lemma A), or V_x < h_u, x_min < 0.546 and (R) needs cot ω ≥ 5.2; W_R below C_top similarly.  Dead.
 (γ) y_WL ∈ [X_low, C_top): ω ≥ 30° (T-chord or W_R above C's line), (R) gives x_min ≥ 0.932, V_x > h_u + s so V is
     above C's line: cos ω < 0.05, then x_min > 1 and (2.1)-(ii) put W_L above C_top.  Dead.
 (δ) y_WL < X_low: ω > 45°, (R) gives x_min ≥ 0.87, V above C's line, and the master inequality (5.1)
     cos ω + (w_φ − x_min) tan ω + sin ω tan θ ≤ (T_x − x_min) tan θ + sin φ − D reduces to
     cos ω + (w_φ − 1) tan ω + (sin ω − c) tan θ < sin φ − D; with (D-low) this is < sin φ (φ > θ; AM–GM: LHS ≥
     1.68 (0.95 sin φ)^½, Lean `delta_core`) or < 1.01 φ² with every LHS term positive (φ ≤ θ; then tan ω < 0.1).  Dead.
 Centre-low: **A2** the disc chord at X_low* is right of w_φ (q_x ≥ 1.468) while the disc chord at q_y − 0.45 is left of
 h_u + s ≤ 1.09 (q_x < 0.872) — Lean `a2_core`.  **A1** (Q right of X): δ := X_low* − q_y < 0.032 tan θ + sin φ and
 (cos φ + sin φ − 1) + 1/2 + (1/4 − δ²)^½ < cos θ is required, false on [0, 5°]² (min 0 at the origin, 0.0038 at (5, 0),
 0.079 at (5, 5); grid 501² [T-computed] `check276b`; by Taylor ≈ θ²/2 + φ(1 − θ − 1.6 φ) > 0).  Dead.
[T-computed] `check276b`: 2 400 feasible Q on 80 random corner configurations (exact shapely feasibility: X ∩ int C =
∅, X meets int T_u), area(Q ∩ T_u) = 0 always; the flat Q needs h_u ≥ 1 + (w_φ − c) > 1 for every φ > 0.

## 5. The statements

**Theorem FLAT-X [T]** and **Theorem CORNER [T]** as in §0; proofs parts 2–3 and 4–6 (each case ends in a displayed
inequality with its numeric slack).  Lean `Statements/Open/FlatX.lean`: cores `dip_window`, `near_miss_pos`,
`lemma_a_dv`, `clearance_core`, `a2_core`, `delta_core` [T]; opaque `FlatX`, `CornerTilts` (the tilts are not fields of
A271's opaque `JamCorner`); axioms `strip_two_in_jam_flat_x`, `strip_two_in_jam_corner` [T-prose]; theorem
`strip_two_in_ring_of_corner` (the `pair3` bridge on the corner).  Build + audit 0 sorry; `lean/AUDIT.md` regenerated.
**5b of k0_route.md §13** = STRIP₂-IN-JAM [T on the corner θ, φ ≤ 5° (this note) + T-computed outside it (A273's drop
tree, two capped cells θ 25–30° open)] + `pair3` (not landed).  General n: nothing here depends on n or the side beyond
H1's 1.406 < X_low < C_top (through (P0)–(P2)); the corner statement is about three squares in a quadrant.

## 6. What the brief had wrong
1. "T_u's top edge is higher than C's top by h_u tan θ, so S has a thin sliver ABOVE C's top line" — no: T_u's top
   vertex T′ = (c, C_top) is at the SAME height as T; T_u ⊂ {y ≤ C_top}.  The sliver that exists is Σ, right of x = 1,
   of width O(θ²) (§2); the intruder does not touch it.  The second-order quantity is 1 − c = the horizontal offset of
   T′ from X's right edge, and the clearance is (1 − c) c.
2. "The best intruder is NOT squeezing through the channel; find what it is doing" — right: it rests on C's top line
   with its left edge on X's right edge, flat; the channel Κ (mouth η < tan θ) is never entered (case B, part 3).
3. "The margin is monotone in φ / bound the φ-derivative" — not needed and not true as a perturbation of the flat
   family: at φ > 0 the flat square is dead outright and the near-miss changes family (first order, the pins);
   the corner proof is a fresh case split with the three pins, not a perturbation.
4. "Covering [0, 5°]² minus what A273's cells certify" — A273's cells exclude exactly the corner cell (its index
   lists no cell with θ, φ ≤ 5°); the theorem here covers all of it.
5. Right in the brief: the mechanism is second order only along φ → 0; (U8) is a theorem there but not needed here.

## 7. Reproduce
`python check276.py 80 40` (< 2 min), `python check276b.py 80 30` (< 3 min), `python page276.py` (assertions = the
geometry check of every panel); Lean: `python attempts/A78-lean-wave6/code/lakeb.py PackingCertMathlib.Statements.Open.FlatX`,
then `python lean/audit.py`.
