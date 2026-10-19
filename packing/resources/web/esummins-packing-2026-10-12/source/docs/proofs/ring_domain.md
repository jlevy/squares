# RING DOMAIN — which of STRIP₂-IN-RING's domain conditions the JAM hypotheses force: (D1), (D2), (U1), (U2), (U9) are THEOREMS from H1–H3 (Lemma SLOPE, Lemma LOW: a floater that shares its box with a floor toucher has its left vertex above height 1.12), (U8) is not derived, and (U3)–(U6) are FALSE as consequences (drawn: X tilted ≥ 13° more or less than C, meeting T_u by a sliver) — yet no free strip square exists on any violator found; the residual is ~18 % of the H1–H3 set, priced ~10³ CPU-h, not launched — A271, 2026-09-23

The brief (A271 BRIEF, PI: "the ring domain is essentially required by the double-meeter requirement round the border
plus the pinning requirement — so what do we actually need to show?"): derive each of A267's domain conditions
(D1)–(D2), (U1)–(U9) (`strip_enclosure.md` §3.1) from the hypotheses H1–H5, or draw a configuration satisfying them
that violates it.  Tags [T] proved, [T-computed] finite computation with its own check, [M] measured, [C] conjecture,
[F] false (witness).  Code `attempts/A271-ring-domain/code/` (`ringdom271` H1–H3 as HARD constraints + the domain
margins exactly as `hyp267`, `check271` 43 rings = hyp267 to 10⁻¹⁵, `adv271` the per-condition adversary, `probe271`
the strip search under H1–H3, `mc271` the residual's size, `pages271`); results beside it; page
`docs/residue_map/campaigns/A271-ring-domain/ring_domain.svg`; Lean `Statements/Open/RingDomain.lean`.
Notation as A267: corner frame BL, wall x = 0, floor y = 0; C the floater, lowest vertex B = (u, h_v), u = h_u + s,
tilt θ ∈ [0°, 45°], c = cos θ, s = sin θ, w = c + s, left vertex L = (h_u, L_h), L_h = h_v + c, top T = (h_u + c,
C_top), C_top = h_v + w, right vertex R = (u + c, h_v + s); g = ℓ_C(1); T_u = C − h_u e_x, S = T_u ∖ C; X the wall
toucher, leftmost vertex (0, y_X), lowest point X_low = y_X − cos φ, tilt φ ∈ [0°, 45°], bottom vertex B_X =
(sin φ, X_low), top X_top = X_low + w(φ); A the floor toucher, lowest vertex (a_x, 0), tilt α ∈ [0°, 90°), leftmost
point x_min(A) = a_x − sin α; C's frame (a, b) as A267 §3.1; s̄ the container side (the side is called s̄ here, s
being sin θ).  **The hypotheses** (the brief's H1–H5, in the form used):
 H1 X meets the open TL box (0,1) × (s̄−1, s̄): X_top > s̄ − 1; X ⊆ the container: X_top ≤ s̄; X misses the open BL
    box (the corner is of JAM type, no wall toucher meets it): X_low ≥ 1.
 H2 int X ∩ int T_u ≠ ∅ (X holds C), int X ∩ int C = ∅.
 H3 C meets the open box and floats (h_u, h_v > 0); A ⊆ the quadrant meets the open box; int A ∩ int C = ∅.
 H4 s̄ ∈ [3.82, ŝ]; the packing is family-stuck and normal (P1–P4).  H5 HELD-JAM (not used).
Only the side bounds of H4 are used below (through H1).  Family-stuckness and P1–P4 are used NOWHERE: every
derivation is a statement about the three squares A, C, X in the corner quadrant at a side in [3.82, ŝ].

## 0. Verdict

> **[T] Five of the ten conditions are theorems from H1–H3** (§2): **(D1)** h_v < 1, g < 1 (C meets the box) and
> L_h > 1 — by **Lemma LOW** (all tilts α ∈ [0°, 90°) of A; α is not a frame convention): L_h ≥ cos α + tan(45° −
> θ/2) ≥ 1.121 for α ≤ 45°, ≥ 1.121 for α > 45° with A's top vertex left of C's right vertex, and > 1 (no uniform
> margin; [M] ≥ 1.14) in the remaining steep case, whenever a floor toucher A shares the open box with the floater C
> (proof: **Lemma SLOPE** — the line separating A from C has POSITIVE slope, A below-right, C
> above-left; then A's left vertex under the line and C's vertices B, R above it give h_v ≥ cos α − tan θ ·
> (x_min(A) − u)⁺, or the same with A's top vertex; Lean `low_core`, `lh_gt_one`, `lh_gt_one_steep`, `tangent_core`); **(D2)** X_low ≥ h_v — by H1 + the window: X_low > s̄ − 1 − w(φ)
> ≥ 1.406 > 1 > h_v; **(U1)** a₁ < a* ⟺ c sin φ + s (X_low − L_h) < 1, and X_low − L_h < s (X meets int T_u ⊂
> {y < C_top}) gives c sin φ + s² ≤ 1 − c (c − sin φ) ≤ 1 (Lean `u1_core`); **(U2)** b_X ≥ 0 on [a₁, a₂] — by
> BLOCKER-SIDE (mirror, `box_meeters.md` §1.2): X is separated from C by a line of positive slope, so no point of X
> with a ∈ [0, 1] lies below C's upper-left line (b ∈ (−1, 0) is int C; b ≤ −1 is below that line, and touching at
> b = −1 would make C's lower-right edge line a supporting line of C with C on its wrong side); **(U9)** σ < 1 on
> T_u — X_low > 2.82 − w(φ) and C_top < 1 + w(θ) give σ(T_u's top vertex) < 1 + cos φ (sin φ + w(θ) − 1.82) −
> sin φ cos θ < 1 (Lean `u9_core`), the other vertices are lower.
> **(U8) is not derived** (adversary minimum +0.094 under H1–H3, [M] positive); derived only the weaker X_top − C_top
> > 1.82 − w(θ), i.e. (U8) for θ ≤ 6.5°.
> **[F] (U3), (U4), (U5), (U6) are NOT consequences of H1–H5** (`adv271`, every witness re-checked exactly, all
> H1–H3 margins ≥ 10⁻⁶): minima −0.199 (U3: θ = 34.5°, φ = 0°, X's flat bottom edge descends onto C's top vertex),
> −0.300 (U4: h_u = 0.82, φ − θ = 18°), −0.243 (U5: φ = 45°, θ = 2°), −0.184 (U6: h_u = 0.90, φ = 45°) — page (b)–(d).
> All have |φ − θ| ≥ 13° and X meeting T_u by a sliver at T_u's top-right corner or in the left strip.  The 43 JAM
> rings have φ − θ ∈ [−1.7°, 14°] and U3–U6 margins ≥ 0.19 / 0.25 / 0.041 / 0.25: what keeps them there is the RING
> (A and X are START squares of adjacent walls whose rows must close at s̄ ≤ ŝ), not the corner.
> **[M] STRIP₂ itself survives every violator**: `probe271` (joint search over (C, X, A, s̄) with H1–H3 hard and a
> free square Q of the quadrant with an interior point in S; obstacles {C, X} and {C, X, A}): sup t = 0.00000, and
> every point with t > −10⁻³ has C's box depth → 0 — the flat unit box [0,1]² touching T_u from below as h_v → 1,
> exactly the brief's "h_v → 1: C leaves the box, STRIP is vacuous at the boundary".  No free strip square with
> t > 0 on 50 + 43 starts.  So STRIP₂ is [C] on the residual, true on every point tested, and A267's proof is what
> fails there, not the statement.
> **The residual and its price.**  R := {H1–H3} ∖ {(U3) ∧ (U4) ∧ (U5) ∧ (U6) ∧ (U8)} is ~18 % of the H1–H3 set
> (`mc271`, 20 000 random-walk samples; 5 of 24 uniform hits), |φ − θ| ≥ 4.4° on it; A266's `strip266` kernel on
> the 5-parameter (h_u, h_v, θ, X_low, φ) domain was priced ~5·10³ CPU-h, so R costs ~10³ CPU-h: **not launched**
> (over the 20 CPU-h line by two orders).  The brief's "it should be tiny" is wrong: the violating sub-domain is a
> fifth of the corner-local hypothesis set, and only the ring shrinks it.
> **Statement (§5): STRIP₂-IN-JAM [T-prose].**  Under H1–H3 (a JAM corner at a side in [3.82, ŝ]) and the four
> ring inequalities (U3)–(U6) + (U8), no unit square of the quadrant interior-disjoint from C and X has an interior
> point in S.  Lean: `RingDomain` is no longer opaque — `JamCorner ∧ RingIneq`, with `strip_two_in_jam` the axiom
> and `strip_two_in_ring_of_jam` the bridge; the derived conditions' arithmetic cores are theorems (`low_core`, `lh_gt_one`, `u1_core`, `u9_core`, `x_high`).
> **NO-JAM(11) still lacks** (§6): `pair3` (A262 chain3, not landed), (U3)–(U6) + (U8) on the JAM rings as a ring-level
> statement or the ~10³ CPU-h residual certificate, 5d, `jam_count`.

## 1. What H1–H3 give at once  [T]

**(F1) X is high.**  X_top > s̄ − 1 ≥ 2.82 and X_low = X_top − w(φ) > 2.82 − w(φ) ≥ 2.82 − √2 = 1.406; also
X_low ≤ s̄ − 1 ≤ 2.877.  (H1's "X misses the BL box", X_low ≥ 1, is implied.)  So (D2)'s X_low ≥ h_v holds with
margin > 0.4 (h_v < 1), and X meets int T_u ⊂ {y < C_top} forces **C_top > X_low > 1.406** and **X_low < C_top**.
**(F2) The box.**  C meets (0,1)² ⟹ h_u < 1, h_v < 1, and (A266, Lean `open_box_tilted`) h_u c + h_v s < w − sc;
with L_h > 1 (below) the lower-left edge covers the heights [h_v, 1] and the box condition is g = ℓ_C(1) < 1.
**(F3) Lemma SLOPE.**  *A, C unit squares of the quadrant, both meeting the open box, A touching the floor,
int A ∩ int C = ∅.  Every line {n·x = β} with A ⊆ {n·x ≥ β}, C ⊆ {n·x ≤ β} has n_u > 0 > n_v.*  Proof: n_u > 0 is
PUSH (ii) (`k0_count.md` §2).  If n_v ≥ 0: C lies in {n·x ≤ β} ∩ quadrant, the right triangle with legs β/n_u,
β/n_v (a half-strip if n_v = 0); SQUARE-IN-TRIANGLE (`construct_towards.md`, as in BLOCKER-SIDE) needs
β ≥ n_u + n_v (n_v = 0: C's width ≥ 1 needs β ≥ n_u); but A's point p of the open box has β ≤ n·p < n_u + n_v.  ∎
This is the "PUSH (i)" remark of `box_meeters.md` §1.2, now with its proof.  In slope form: A lies BELOW a line
y = k + m x with m = −n_u/n_v > 0, C ABOVE it.
**(F4) Lemma LOW (full range of A's tilt).**  *Under H3, L_h = h_v + cos θ > 1; moreover L_h ≥ cos α +
tan(45° − θ/2) ≥ 1.121 when α ≤ 45°, and L_h ≥ cos α (1 − tan θ) + sin α + tan(45° − θ/2) ≥ 1.121 when α > 45° and
A's top vertex is left of C's right vertex R.*  A's tilt α ∈ [0°, 90°) is read with its lowest vertex as anchor and is
NOT a frame convention: the corner frame is fixed by C and X (reflecting across the diagonal swaps the wall and the
floor), so α ∈ (45°, 90°) — A nearly flat with its lowest vertex at the right, or steep — is a genuine case (A273's
flag; it is feasible under H1–H3: an `adv271`-style search restricted to α > 45° reaches L_h = 1.1405 at α = 50.6°,
θ = 45°, h_u → 0, h_v = 0.433, in the third case below).  Proof.  The separator y = k + m x (m > 0, Lemma SLOPE) lies
above every point P of A, so k ≥ y_P − m x_P; C's B = (u, h_v) and R = (u + c, h_v + s) lie above it.  For any P ∈ A
with x_P < R_x = u + c: h_v ≥ y_P − m (x_P − u) and h_v ≥ y_P − s + m (R_x − x_P); the second rises with m, the first
falls, and the maximum of the two is ≥ their value at m = s/c: **h_v ≥ y_P − tan θ · (x_P − u)⁺**.
 (a) α ≤ 45°: P = A's left vertex (x_min, cos α), x_min < 1 < R_x, x_min − u < 1 − h_u − s < 1 − s: h_v ≥ cos α −
 tan θ (1 − s), L_h ≥ cos α + c − tan θ (1 − s) = cos α + (1 − s)/c = cos α + tan(45° − θ/2) ≥ 1/√2 + tan 22.5° = 1.1213
 (Lean `low_core`, `lh_gt_one`).
 (b) α > 45°, A's top vertex P = (x_min + cos α, cos α + sin α) has x_P < R_x: x_P − u < 1 + cos α − s, so L_h ≥
 cos α + sin α + c − tan θ (1 + cos α − s) = cos α (1 − tan θ) + sin α + tan(45° − θ/2) ≥ sin α + 0.4142 ≥ 1.1213
 (`low_core` with the top vertex; tan θ ≤ 1, sin α ≥ 1/√2).
 (c) α > 45°, A's top vertex right of R (x_min + cos α ≥ R_x): R lies above the separator, which lies above A's
 upper-left edge on [x_min, x_min + cos α] ∋ R_x, so h_v + s ≥ cos α + (R_x − x_min) tan α with R_x − x_min = h_u +
 w − x_min > w − 1 (h_u > 0, x_min < 1, tan α ≥ 1): **h_v > cos α − s + (w − 1) tan α** and L_h > cos α + c − s +
 (w − 1) tan α =: G(α, θ).  G > 1: G − 1 = cos α + (w − 1)(tan α − 1) − 2(1 − c); with (1 − c)(1 + c) = s² and s ≤ c,
 (w − 1) · 2s ≥ 2(1 − c) (⟺ (1 − c)(c − s) ≥ 0), so for tan α ≥ 1 + 2s the last two terms sum to ≥ 0 and cos α > 0
 decides; for tan α < 1 + 2s ≤ 2.42 the tangent bound cos α ≥ 0.707 − 0.354 (tan α − 1) (convexity of (1 + t²)^{−1/2}
 on t ≥ 1) gives G − 1 ≥ 0.707 − 2(1 − c) + (tan α − 1)((w − 1) − 0.354) > 0 (at tan α = 1 it is ≥ 0.121; the bracket
 is ≥ 0 for s ≥ 0.604, and for s < 0.604 the value at tan α = 1 + 2s is ≥ 0.707 − 0.708 s > 0) — Lean
 `lh_gt_one_steep`, `tangent_core`.  No uniform margin: G → 1⁺ as θ → 0, α → 90° (a flat C over an almost flat A whose
 lowest vertex is its right corner); with (F1) that limit has C_top < 1.41 < X_low and is not a JAM.  ∎
So **(D1) L_h > 1 is [T] for every tilt of A**; the margin 1.121 is [T] in cases (a), (b) and [M] (≥ 1.14) in (c).
Corollary: h_v ≥ 1/√2 − tan θ (1 − s) ≥ 0.414 in case (a); rings: h_v ≥ 0.929.
**(F5) X above C's upper-left line.**  H2 is exactly the hypothesis of BLOCKER-SIDE's mirror (`box_meeters.md`
§1.2, Lean `blocker_side_core`): X meets T_u and misses int C, so a separating normal m from X to C has
m_u > 0 > m_v — X is ABOVE a line of positive slope, C below it.  In C's frame: **every point of X with
a ∈ [0, 1] has b ≥ 0.**  For b ∈ (−1, 0) the point is in int C (a ∈ (0,1)) or on C's lower-left / upper-right edge
(a ∈ {0, 1}), and touching there puts that edge line — of NEGATIVE slope −c/s — as a supporting line of C with X on
its far side, against the positive-slope separator.  For b ≤ −1 the point P = E + t (s, −c), t = −b − 1 ≥ 0, E on
C's lower-right edge (a_P ∈ [0,1]): E is on or below the separator, (s, −c) points down-right, so P is strictly below
it unless t = 0 — and then the separator supports C at a point of its lower-right edge, i.e. IS that edge line (or
a line through B or R with C on its wrong side: from B the lower-left edge direction (−s, c) has c ≤ −m s, false).  ∎

## 2. The conditions one by one

| condition | verdict | from | margin under H1–H3 (`adv271`) | rings (`hyp267`) |
|---|---|---|---|---|
| (D1) h_v < 1, g < 1 | [T] | H3 (C meets the box), (F2) | → 0 (h_v → 1: C leaves the box) | 0.0009 |
| (D1) L_h > 1 | [T] all tilts of A; L_h ≥ 1.121 unless A steep with its top right of R | Lemma LOW (H3) | ≥ 0.12 (α ≤ 45°); 0.14 (α > 45°, [M]) | ≥ 0.89 |
| (D2) X_low ≥ h_v, X meets int T_u, misses int C | [T] | (F1) (H1 + s̄ ≥ 3.82), H2 | → 0 (X's depth in T_u → 0) | 0.0016 |
| (U1) a₁ < a* | [T] | H2 (X_low < C_top) | 0.109 | ≥ 0.29 |
| (U2) b_X ≥ 0 on [a₁, a₂] | [T] | (F5) = BLOCKER-SIDE mirror (H2) | → 0 (X's edge on C's line) | 0.0016 |
| (U3) a₂ − a* > w_max/2 | **[F]** as a consequence | — | **−0.199** | ≥ 0.19 |
| (U4) ρ(C_top), ρ(y₀) < 1, ℓ_C(X_low) < 1 | **[F]** | — | **−0.300** | ≥ 0.25 |
| (U5) a_R − sin β⁺ ≥ a* | **[F]** | — | **−0.243** | ≥ 0.041 |
| (U6) h_u + c − cos φ < 1 | **[F]** | — | **−0.184** | ≥ 0.25 |
| (U8) X_top > C_top + 1/√2 | not derived; [T] for θ ≤ 6.5° | (F1): X_top − C_top > 1.82 − w(θ) | +0.094 | ≥ 0.19 |
| (U9) σ < 1 on T_u | [T] | (F1), h_v < 1, θ, φ ≤ 45° | 0.354 | ≥ 0.76 |

**(D1) [T].**  h_v < 1 and g < 1 are the box condition itself given L_h > 1 ((F2), A266 `open_box_tilted`); L_h >
1.121 is Lemma LOW.  At the limit h_v → 1 C leaves the box, the corner stops being a JAM: the JAM domain is OPEN
there and STRIP₂ is vacuous at its boundary (the adversary's D1 → 0 is that limit, page (a) inset).
**(D2) [T].**  X_low > 1.406 > 1 > h_v by (F1); the rest is H2 and the packing.  X's tilt convention φ ∈ [0°, 45°]
with the leftmost vertex on the wall is a choice of frame (A267's `mir` lane is the reflection), not a hypothesis.
**(U1) [T].**  a_B < a* ⟺ c (sin φ − h_u) + s (X_low − L_h) < 1 − h_u c ⟺ c sin φ + s (X_low − L_h) < 1 (h_u
cancels), and 0 < a* since h_u < 1.  X meets int T_u ⊂ {y < C_top} gives X_low − L_h < s, so the left side is
< c sin φ + s² = 1 − c (c − sin φ) ≤ 1 because sin φ ≤ 1/√2 ≤ c (Lean `u1_core`; for s = 0 it reads sin φ < 1).
**(U2) [T].**  (F5): b ≥ 0 at every point of X with a ∈ [0, 1], in particular at X's lower-right edge over [a₁, a₂] ⊆
[0, 1].  The adversary's U2 → 0 is X's edge sliding onto C's upper-left line (the rings' 0.0016 is the C–X gap).
**(U9) [T].**  σ(x, y) = sin²φ − x sin φ + cos φ (y − X_low) is affine, so its maximum over T_u is at a vertex.  Top
vertex (c, C_top): C_top − X_low < 1 + w(θ) − 2.82 + w(φ) by (F1) and h_v < 1, so σ < 1 + cos φ (sin φ + w(θ) −
1.82) − sin φ cos θ, and cos φ (sin φ + w(θ) − 1.82) ≤ cos φ (sin φ − 0.4058) < sin φ cos θ (if sin φ ≤ 0.4058 the
left side is ≤ 0; else sin φ (cos φ − 0.7071) ≤ 0.2071 < 0.287 ≤ 0.4058 cos φ) — Lean `u9_core`.  Left vertex
(0, L_h): σ < 1 + cos φ (cos θ + sin φ − 1.82) < 1; right vertex (w(θ), h_v + s): σ < 1 − sin φ cos θ + cos φ (s −
1.82) < 1; bottom vertex (s, h_v): σ < sin²φ − 0.406 cos φ < 1.  ∎
**(U8) — not derived.**  X_top − C_top > (s̄ − 1) − (1 + w(θ)) ≥ 1.82 − w(θ), which exceeds 1/√2 only for θ ≤ 6.5°.
The adversary's minimum is +0.094 (θ = 20.8°, φ = 0, h_v = 0.994: X_top − C_top = 0.80); the constraint that keeps it
positive is A (a 45°-tilted C at h_v ≈ 1 leaves A no place), but I have no proof.  (U8) is used once: to put Q's
centre at or below X's top (§3.2 of A267); without it the case q_y ∈ (X_top, C_top + 1/√2] — Q hanging over X's top
into S past X's right vertex — is open.
**(U3)–(U6) [F] as consequences (page (b)–(d), every witness exact: all 20 H1–H3 terms ≥ 10⁻⁶).**
 (U3) h_u = 0.390, h_v = 0.985, θ = 34.5°, X_low = 2.374, φ = 0°, A at a_x = 1.263, α = 21.5°, s̄ = ŝ: β = −34.5°,
 X's flat bottom edge is 0.687 above L (in b) and descends onto C's top vertex (b_R = 0.12), meeting T_u's top strip
 by a sliver at its top-right corner; a₂ − a* = 0.145 < w_max/2 = 0.344: margin −0.199.
 (U4) h_u = 0.820, h_v = 0.998, θ = 10.4°, X_low = 2.070, φ = 28.7°, s̄ = 3.82: β = 18.3°, C far from the wall;
 the room right of X at C's top is ρ(C_top) = 1.30: margin −0.300.
 (U5) h_u = 0.628, h_v = 0.994, θ = 2.0°, φ = 45°, X_low = 1.997, s̄ = ŝ: β = 43°, X's right vertex short of T_u's
 top edge by 0.243 after the sin β correction (S's top corner T′ exposed beyond X).
 (U6) h_u = 0.897, h_v = 1.000⁻, θ = 5.7°, φ = 45°: h_u + c − cos φ = 1.18: margin −0.184 (U4 −0.60, U5 −0.15 too).
All four have X tilted ≥ 13° away from C (|β| ∈ [13°, 43°]) and meet T_u by a sliver; on the 43 JAM rings β ∈ [−1.7°,
14°] and the margins are 0.19 / 0.25 / 0.041 / 0.25.  What the corner does not see: A and X are the START squares of
walls 0 and 3 of a ring that must close at s̄ ≤ ŝ (A262 §3.1's HARD terms), and C's tilt is free — φ − θ up to 14°
occurs on the rings.  So (U3)–(U6) are RING-LEVEL facts; no H1–H5 derivation exists because they are false under
H1–H5 (H4's family-stuckness and P1–P4 were not used: they are properties of the whole packing that the three-square
adversary cannot violate or exploit — a proof through them would have to go through the ring's closure).

## 3. Is STRIP₂ true on the violators?  [M]

`probe271`: maximise t(q, Q) = min(gap(Q, C), gap(Q, X), Q_xmin, Q_ymin, depth(Q, T_u)) over the configuration q
(H1–H3 HARD, exact SAT) and a unit square Q (centre, tilt), from the adversary's violators, the 43 rings and 40 random
feasible starts, first over Q alone (81 centres × 6 tilts, polished) then jointly.  Obstacles {C, X}: sup t =
−0.00000; obstacles {C, X, A}: the same.  Every point with t > −10⁻³ has C's box depth → 0 and Q → the flat unit
box [0, 1]² (centre (0.5, 0.5), tilt 0): as h_v → 1 the strip's bottom edge descends to height 1 and the box square
touches it from below — STRIP₂'s vacuous boundary, not a counterexample.  Fixed-configuration values on the four
violators: −0.0077 (U3), −0.0000 (U4: h_v = 0.998), −0.0030 (U5), −0.0000 (U6: h_v = 1.000⁻).  **No free strip
square exists on any violator** — STRIP₂ is [C] on the residual, [M] true there, and what fails off the ring
domain is A267's PROOF (its §3.2 room bounds and §3.3 FAR-SIDE), not the statement.

## 4. The residual and its price

R := {q : H1–H3} ∖ {(U3) ∧ (U4) ∧ (U5) ∧ (U6) ∧ (U8)}.  `mc271`: on 20 000 random-walk samples of the H1–H3 set
(seeded at the rings and the violators, step 3 % of the box; a rough sample) 18.4 % lie in R (U3 8.9 %, U4 10.1 %,
U5 5.4 %, U6 4.0 %, U8 0 %), with |β| ≥ 4.4° on R; the uniform hit rate of the H1–H3 set in the box is 1.6·10⁻⁴
(24 hits, 5 in R).  A certificate on R is A266's `strip266` kernel (5 parameters, LEFT-SHADOW test, 535 s per
1/1200 sub-cell) with R's inequalities as PRUNE: ~0.2 × 5·10³ ≈ **10³ CPU-h — not launched** (the brief's 20 CPU-h
line).  The cheap alternative is ring-level: certify (U3)–(U6) + (U8) on the JAM-ring family (A262's 11 coordinates +
s̄, HARD terms) — the same kind of job as A261's O3, not priced here.

## 5. STRIP₂-IN-JAM — the statement with the derived domain  [T-prose]

**Theorem (STRIP₂-IN-JAM).**  *Let s̄ ∈ [3.82, ŝ] and let A, C, X be unit squares of the corner quadrant with H1–H3
(a JAM corner: C the floating box meeter, A the floor's meeter, X the wall toucher serving the TL box and holding C).
Assume the four RING INEQUALITIES (U3) a₂ − a* > w_max/2, (U4) ρ(C_top) < 1, ρ(y₀) < 1, ℓ_C(X_low) < 1 if X_low >
L_h, (U5) a_R − sin β⁺ ≥ a*, (U6) h_u + cos θ − cos φ < 1, and (U8) X_top > C_top + 1/√2.  Then no unit square of the
quadrant interior-disjoint from C and X has an interior point in S = T_u ∖ C.*  Proof: A267 §1–§3 verbatim, with (D1),
(D2), (U1), (U2), (U9) supplied by §1–§2 here instead of assumed.  ∎  The domain has shrunk from ten explicit
inequalities to five, of which four are ring-level ((U3)–(U6): false as corner statements, §2) and one is
unresolved ((U8): [M] positive under H1–H3, margin 0.094).  On the 43 JAM rings all five hold with margins ≥ 0.041.
**What replaces a derivation for (U3)–(U6) + (U8):** either (i) a RING-LEVEL certificate — the five inequalities on
A262's JAM-ring family (walls 0–2 rows of two / open pairs, X + C on wall 3, HARD terms, s̄ ∈ [3.82, ŝ]) — a job of
A261-O3 type, not priced; or (ii) the residual strip certificate on R, ~10³ CPU-h (§4); or (iii) an adapted proof of
the UPPER case for wide wedges (|β| up to 45°, X meeting T_u by a sliver), where `probe271` says the statement holds.
At the limits: h_v → 1 (D1 → 0) C leaves the box; X's depth in T_u → 0 (D2 → 0) X stops holding C; b_X → 0 (U2 → 0) X
touches C's upper-left line — all three are the JAM domain's OPEN boundary, where STRIP₂ is vacuous, never a
counterexample.

## 6. What NO-JAM(11) still lacks

5b of `k0_route.md` §13 = STRIP₂-IN-JAM [T-prose, this note: H1–H3 + (U3)–(U6) + (U8)] + `pair3` (A262 chain3:
`certs/pair3262_index.jsonl` still absent at this writing).  Still open: (i) (U3)–(U6) + (U8) as ring-level facts
(they cannot come from the corner, §2) or the ~10³ CPU-h residual; (ii) 5a/5b `pair3`; (iii) 5d (indirect jams,
FLOAT2, a middle toucher above X — `float262` / `span262`, chain3); (iv) 6's Lean axiom `jam_count`; (v) STRIP₂ off
H1–H3 altogether (the general A266 domain, `strip266` budgeted).  General m: (F1)–(F5), Lemma SLOPE, Lemma LOW, (U1),
(U2), (U9) are corner-local; the numbers 1.406 / 1.82 use s̄ ≥ 3.82 through X_top > s̄ − 1 only (for m ≥ 5 replace
by s̄ − 1 ≥ m − 2 ≥ 3: every bound improves).

## 7. What the brief had wrong

1. "The ring domain is essentially required by the double-meeter requirement plus the pinning requirement": half.
   Five conditions are (D1, D2, U1, U2, U9); four are FALSE as consequences of H1–H5 (U3–U6, drawn), one is
   unproved (U8).  The pinning requirement (H2) gives U1, U2 and part of D2; the double-meeter requirement (A + C
   share the box) gives L_h > 1.12 — a new lemma (LOW) — and nothing else; H4's family-stuckness / P1–P4 and H5 give
   nothing at the corner.  2. "The violating sub-domain is the ONLY place a certificate is needed: price it, it should
   be tiny": it is ~18 % of the H1–H3 set and costs ~10³ CPU-h — the ring, not the corner, is what makes it small.
3. "X's lowest point > 1 (SAME-WALL / meeters_split)": true but weak — H1 with the window gives X_low > 1.406.
4. The thin margins D1 0.0009 / D2, U2 0.0016 are indeed equalities in the limit, and the limits are the JAM domain's
   open boundary (§5), as the brief guessed.  5. Not in the brief: STRIP₂ is [M] TRUE on every violator (`probe271`),
   so the gap is in A267's proof technique for wide wedges, not in the statement.

## 8. Lean, reproduce

`Statements/Open/RingDomain.lean`: theorems `low_core`, `lh_gt_one`, `lh_gt_one_steep`, `tangent_core` (Lemma LOW's arithmetic, all tilts of A), `u1_core`, `u9_core`,
`x_high` ((F1)); `JamCorner` (H1–H3), `RingIneq` ((U3)–(U6) + (U8)) opaque — together they replace A267's opaque `RingDomain`;
axiom [T-prose] `strip_two_in_jam`; theorem `strip_two_in_ring_of_jam` (A267's `strip_in_ring_of_enclosure` with the new domain);
build + audit 0 sorry.  Reproduce (each ≤ 6 min, `JAM_COARSE=1`): `python check271.py`, `python adv271.py 300`,
`python probe271.py 360 two`, `python probe271.py 200 three`, `python mc271.py 20000 walk`, `python pages271.py`.
