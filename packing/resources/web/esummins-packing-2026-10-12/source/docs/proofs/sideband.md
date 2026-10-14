# The sideband lemma and the doubly-met-corner requirement — A169, 2026-09-09

Two lemmas about a corner box met by two squares, stated for any n, needed by the k0 cascade
(A168; `docs/proofs/k0_route.md` §3–4).  Tags: [T] proved here, [S] supported, [M] measured,
[F] false (with the counterexample), [C] Lean obligation.  Lean:
`lean/PackingCertMathlib/PackingCertMathlib/Sideband.lean` (§5).  Numerics and scripts:
`attempts/A169-sideband-lemma/` (the derivations in `notes/derivation.md`, the picture in
`docs/residue_map/sideband_lemma.svg`).

## 0. Verdicts

* **SIDEBAND (a) [T, sharp].**  Two interior-disjoint unit squares both meeting the OPEN corner
  box (0, c)² (BL corner, container coordinates) never both have centres in [c, ∞)²: at least one
  centre has x < c or y < c.  The constant is **c itself** — for the unit box the band is
  x < 1 or y < 1; for the K0-WIDEN box c = 1 + w = 1.025509 the band is x < 1 + w.  No quadrant
  hypothesis and no restriction on c are needed (Lean `Sideband.not_both_ne`, `sideband_a`).
  The claim "within 1 of a wall" for the WIDENED box is **[F]**: two 45° diamonds centred
  (1.01, 1.7226) and (1.7226, 1.01) are interior-disjoint (SAT gap 0.00777), inside the container,
  both meet (0, 1 + w)², and both centres exceed 1 in both coordinates.  Sharpness at c: for every
  ε > 0 the diamonds at (c − ε, c + 1/√2 − ε′) / (c + 1/√2 − ε′, c − ε) (ε′ < ε) are a disjoint
  pair with both centres > c − ε.  On the window the sharp band on F = Δ_λ P is x < λ ≤ λ_max =
  s0/3.82 = 1.014944 (apply (a) to P at the unit box and dilate), which beats 1 + w.
* **SIDEBAND (b) [F as stated, T in the cell form].**  "The other centre lies outside that
  band" is false: Q1 = [0.1, 1.1] × [0, 1] (centre (0.6, 0.5)) and Q2 at tilt 2.866°, centre
  (0.5244, 1.5220), are interior-disjoint (gap 1.0·10⁻⁴), both meet (0,1)², and both centres
  have x < 1.  What is true and sharp: **the two centres lie in two DIFFERENT cells of the 2×2
  grid {x < c, x ≥ c} × {y < c, y ≥ c}** (Lemma A2, Lean `distinct_cells`), because any two
  interior-disjoint unit squares have centres at ℓ∞-distance ≥ 1/√2 (Lemma A1, sharp, Lean
  `linf_sep`) and every cell restricted to meeter centres has ℓ∞-diameter < 1/√2 whenever
  c < 1/2 + 1/√2 = 1.2071.
* **REQUIREMENT [T].**  Theorem B is an exact characterisation: a unit square Q1 in the
  quadrant admits a second meeter of (0, c)², c ≥ 1, iff one of four one-parameter support
  inequalities holds ((NE), (W), (S), (P) in §3; (P) is vacuous at c = 1).  Consequences, all
  [T] (§4): a PRESSED first meeter (touching both walls) admits no second meeter of the UNIT box
  at any tilt (Cor. B1); the deepest mode-(a) second meeter of a first meeter slid δ along the
  floor at tilt θ has lowest point at height sec θ − δ tan θ, so it exists iff δ > tan(θ/2) = t
  (unit box), with intrusion depth (δ − t) tan θ = 2t(δ − t)/(1 − t²) (Cor. B2); at tilt 0 the
  exact non-lonely region is b < F(a) or a < F(b), F parametrised by u ∈ [0, 1]: a = u(2 − u²),
  F = u²√(1 − u²) (F(a) ≈ a²/4, F(1) = 0.300) (Cor. B3); the exact slide threshold is
  δ_min(θ) = tan(θ/2) for θ ≤ θ* = 56.76° and the crossing (W)-mode minimum (a partner resting on
  Q1's upper vertex, ζ* < θ) beyond it: 0.5727 / 0.6118 / 0.6335 / 0.6302 / 0.5887 / 0.4778 at
  60° / 65° / 70° / 75° / 80° / 85° (Cor. B4, [T] formula, [M] values).  The atlas thresholds
  d*(θ) = 0.18/0.34/0.38/0.56/0.64/0.72 (`two_meeter_atlas_v2.svg`) are pitch artefacts [M]:
  the true unit-box thresholds are 0 / 0.1317 / 0.2679 / 0.4142 / 0.5727 / 0.6302.  The pressed
  square admits a second meeter of the WIDENED box iff cos θ + sin θ < c + √(c² − 1), i.e.
  θ < 17.35° or θ > 72.65° (clause (NE) at α = θ: a partner with a vertex at the box corner),
  and the mode-(a) partner at height sec θ < 1 + w (θ < 12.8°) is only the second-best witness.
  The lonely set is LARGE (59–82 % of the raster of unit-box meeter poses, 54–74 % widened, §4),
  which is the k0 consequence: **every corner meeter of a K0-BLOCKED packing is a non-lonely
  pose — a NO-family row on the WIDENED box that the case-LP consumes on its free columns and
  the crowd covers consume on their boxes (§6).**

## 1. Setting

Container [0, s]², s ≥ 3.82; BL corner box C_c = [0, c]² with c = 1 (unit) or c = 1 + w
(K0-WIDEN, w = 0.025509).  A unit square Q with centre z = (x, y) and tilt θ (edges at θ and
θ + 90°) is Q = {z + a e + b e⊥ : |a|, |b| ≤ 1/2}, e = (cos θ, sin θ), e⊥ = (−sin θ, cos θ).
Half-width in a unit direction n: g_Q(n) = (|n·e| + |n·e⊥|)/2 = w(∠n − θ)/2 with
w(φ) := |cos φ| + |sin φ| ∈ [1, √2] (period 90°, = cos φ + sin φ on [0°, 90°]); support
h_Q(n) = n·z + g_Q(n).  Q **meets** C_c means int Q ∩ int C_c ≠ ∅, equivalently Q ∩ (0, c)² ≠ ∅
(Lean `Meets`).  "Meeter" = a square of the packing meeting C_c.  Facts used throughout:

* (F1) every point p of Q has |p − z| ≤ 1/√2 (|p − z|² = a² + b² ≤ 1/2; Lean
  `sqdist_centre_le_half`);
* (F2) Q ⊆ {x ≥ 0} iff x ≥ g_Q(1,0) ≥ 1/2, same for y (Lean `centre_ge_half`, one direction);
* (F3) SAT: two closed convex polygons with disjoint interiors are weakly separated by a line
  whose normal is an edge normal of one of them (Lean: `SatInterior.sat_selection_thm`).

## 2. [T] Lemma A — the sideband, in its sharp form

**Lemma A1 (ℓ∞ separation).**  Two interior-disjoint unit squares Q, Q′ (any tilts, no
container needed) have centres z, z′ with max(|Δx|, |Δy|) ≥ 1/√2, Δ = z′ − z.  Sharp: two 45°
diamonds with Δ = (1/√2, 1/√2) touch along an edge.

*Proof.*  By (F3) there is a unit normal n, an edge normal of (say) Q, with
h_Q(n) ≤ min_{Q′} n·q, i.e. n·z + 1/2 ≤ n·z′ − g_{Q′}(n).  Hence n·Δ ≥ 1/2 + g_{Q′}(n) ≥ 1.
But n·Δ ≤ |n₁||Δx| + |n₂||Δy| ≤ (|n₁| + |n₂|)·max(|Δx|,|Δy|) ≤ √2·max(|Δx|,|Δy|), since
(|n₁| + |n₂|)² = 1 + 2|n₁n₂| ≤ 2.  ∎  (Lean: `linf_sep` proves `1/2 ≤ Δx² ∨ 1/2 ≤ Δy²` via
|Δ|₂ ≥ 1 (Cauchy–Schwarz on the selection row); `linf_sep_sqrt` is the √ form.)

**Lemma A2 (cells).**  Let 1/2 ≤ c < 1/2 + 1/√2.  Two interior-disjoint unit squares in the
quadrant {x ≥ 0, y ≥ 0}, both meeting (0, c)², have centres in two DIFFERENT cells of the grid
{x < c, x ≥ c} × {y < c, y ≥ c}.  In particular (the PI's (a)): not both centres lie in
[c, ∞)², so one of them has x < c or y < c — and THIS part needs neither the quadrant nor the
bound on c.

*Proof.*  A meeter Q with centre z has a point p ∈ Q with p < (c, c); by (F1), if x ≥ c then
(x − c)² < (x − p_x)² ≤ 1/2, so the NE-side coordinate range is [c, c + 1/√2) (half-open); by
(F2), x, y ≥ 1/2, so the SW-side range is [1/2, c), of length c − 1/2 < 1/√2.  Two centres in
one cell therefore have |Δx| < 1/√2 and |Δy| < 1/√2, contradicting Lemma A1.  The NE cell
alone uses only (F1), which is why the [c, ∞)² statement is unconditional.  ∎
(Lean: `meeter_cx/cy`, `sq_sub_lt_of_ge/lt`, `distinct_cells`, `not_both_ne`, `sideband_a`.)

**Sharpness of the constant c (the PI's "sharp constant as a function of w").**  With c = 1 + w
and any τ < c, the pair of 45° diamonds centred (τ + ε, c + 1/√2 − ε′) and
(c + 1/√2 − ε′, τ + ε), 0 < ε < ε′ < c − τ + ε, is interior-disjoint (the separating axis
(−1, 1)/√2 has gap √2(c − τ − ε′ + ε) > 0), lies in the container, and both squares meet
(0, c)² (the lower vertex of the first is at (τ + ε, c − ε′), and the interior points just
above it are in the open box).  So no threshold below c works.  For the widened box that is
the [F] verdict on "within 1 of a wall"; numerically (`results/check_a.json`): gap 0.007769,
both meet the widened box, neither meets the unit box.

**Corollary A3 (window form).**  Let P be a packing at side m ∈ [3.82, s0), F = Δ_λ P,
λ = s0/m ≤ λ_max = s0/3.82 = 1.014944.  If two squares of P meet the unit corner box of P then
their images in F have centres in distinct cells of the grid at threshold λ, hence at least one
image centre has x < λ_max or y < λ_max (the band of width λ_max on F); and, directly on F at
the widened box, distinct cells at threshold 1 + w.  Both bands are sharp for their hypotheses.

*Proof.*  Δ_λ scales centres by λ (K0-WIDEN, `k0_route.md` §4.1); apply Lemma A2 to P with c = 1
and multiply, or to F with c = 1 + w.  ∎

**What (b) cannot mean.**  Both centres in the same BAND {x < c} is possible (§0: (0.6, 0.5)
and (0.5244, 1.5220), both x < 1, tilt 0° and 2.866°, gap 1.0·10⁻⁴; `results/check_a.json`
`theta0_delta01`).  The centres are then in cells SW and NW.  The strongest true replacement
is Lemma A2; the sampled check (`cells_unit`, `cells_widened`: 1 873 + 3 068 disjoint meeter
pairs, 0 in a common cell) agrees.

## 3. [T] Theorem B — exactly when a second meeter exists

Fix c ≥ 1 and Q1 (centre z₁ = (x₁, y₁), tilt θ ∈ [0°, 90°)) in the quadrant and meeting (0, c)²;
write h(n) = h_{Q1}(n) = n·z₁ + w(∠n − θ)/2.  For ζ ∈ (0°, 90°) put n_W(ζ) = (−sin ζ, cos ζ),
n_S(ζ) = (cos ζ, −sin ζ); for α, γ ∈ [0°, 90°] n_NE(α) = (cos α, sin α) and
m(γ) = min_{Q1}(cos γ x + sin γ y) = −h(−n_NE(γ)).

**Two support inequalities.**  Both are proved by the same device: on each quadrant of its
argument w(φ) = √2 cos(φ − 45°) is concave, so a positive combination of shifted copies of w is
concave on the pieces between the break points and takes its minimum at a break point.

*Lemma B0 (wedge).*  For ζ ∈ [0°, 90°] and every φ: w(φ) − (cos ζ − sin ζ) w(ζ + φ) ≥ 2 sin² ζ,
with equality at φ ≡ 0 (mod 90°).
*Proof.*  Let a = cos ζ − sin ζ, f(φ) = w(φ) − a w(ζ + φ), T = 2 sin²ζ = 1 − cos 2ζ = 1 − a w(ζ)
= f(0); by 90°-periodicity take φ ∈ [0°, 90°], break point φ₀ = 90° − ζ.  If ζ ≥ 45° (a ≤ 0)
f is concave on both pieces; f(0) = f(90°) = T and f(φ₀) − T = (w(ζ) − 1)(1 + a) ≥ 0.  If ζ < 45°
(a > 0), expanding: f = (1 − cos 2ζ) cos φ + sin 2ζ sin φ on [0, φ₀] and
f = (1 + a²) cos φ + (1 − cos 2ζ) sin φ on [φ₀, 90°]; both are nonnegative combinations of
cos φ, sin φ, hence concave on their pieces, with f(0) = f(90°) = T and f(φ₀) = 2 sin ζ ≥ T.  ∎

*Lemma B0′ (triangle).*  For γ ∈ [0°, 90°] and every ψ: (cos γ + sin γ) w(ψ) + w(ψ − γ) ≥
2 (cos γ + sin γ), with equality at ψ ≡ 0.
*Proof.*  b = cos γ + sin γ ∈ [1, √2]; g(ψ) = b w(ψ) + w(ψ − γ) is concave on the pieces of
[0°, 90°] cut at ψ = γ; g(0) = g(90°) = 2b and g(γ) = b² + 1 ≥ 2b.  ∎

**Theorem B.**  There is a unit square Q2 in the quadrant, interior-disjoint from Q1 and
meeting (0, c)², if and only if one of
  (NE) ∃α ∈ [0°, 90°]:  h(n_NE(α)) < c (cos α + sin α);
  (W)  ∃ζ ∈ (0°, 90°):  h(n_W(ζ)) < c cos ζ − sin² ζ;
  (S)  ∃ζ ∈ (0°, 90°):  h(n_S(ζ)) < c cos ζ − sin² ζ;
  (P)  ∃γ ∈ [0°, 90°]:  m(γ) ≥ cos γ + sin γ.
(P) says that the pressed axis square [0, 1]² is weakly separated from Q1 by a line through
(1, 1); it is impossible when c = 1 (a meeter of (0, 1)² has a point p₁ < (1, 1), and
m(γ) ≤ n_NE(γ)·p₁ < cos γ + sin γ), so for the unit box the criterion is (NE) ∨ (W) ∨ (S).
The witnesses are explicit: for (W) with margin μ > 0, Q2 = the square of tilt ζ whose leftmost
vertex is on the wall x = 0 and whose lowest vertex is at (sin ζ, c − ε), 0 < ε ≤ μ/cos ζ; for
(S) the mirror image; for (NE) the square with a vertex at v = (c, c) − ε n_NE(α) and diagonal
along n_NE(α), 0 < ε ≤ min(μ, c − 1/√2); for (P) the pressed square [0, 1]².  A pose is
called **lonely** when none of the clauses holds.

*Proof.*  (⇐)  (W): Q2 = v₀ + a e + b e⊥, a, b ∈ [0, 1], e = (cos ζ, sin ζ), v₀ = (sin ζ, c − ε).
Its x-coordinates are sin ζ + a cos ζ − b sin ζ ≥ 0 and its y-coordinates ≥ c − ε > 0, so Q2 is
in the quadrant; v₀ ∈ Q2 ∩ (0, c)² since 0 < sin ζ < 1 ≤ c; and n = n_W(ζ) = e⊥ gives
n·q = n·v₀ + b ≥ n·v₀ = c cos ζ − sin² ζ − ε cos ζ ≥ h(n) on Q2, the weak separation from Q1.
(S): reflect in the diagonal.  (NE): Q2 = v + a e₁ + b e₂ with e₁, e₂ at angles α ∓ 45°;
n·e₁ = n·e₂ = 1/√2 > 0 so n·q ≥ n·v = c (cos α + sin α) − ε ≥ h(n) on Q2; the coordinates of
Q2 are ≥ c − ε − 1/√2 ≥ 0; and the points v + a e₁, 0 < a < ε√2, have both coordinates in
(0, c), so Q2 meets the open box.  (P): [0, 1]² lies in {n_NE(γ)·q ≤ cos γ + sin γ} (the form is
maximised at (1, 1)), Q1 in {≥}; [0, 1]² is in the quadrant and contains (1/2, 1/2) ∈ (0, c)².

(⇒)  Let Q2 be a second meeter, p ∈ Q2 ∩ (0, c)², z₂ its centre, ψ its tilt, and let n (at
angle α) be a SAT normal (F3): Q1 ⊆ {n·q ≤ β}, Q2 ⊆ {n·q ≥ β}.  Then β ≥ h(n) and
n·z₂ − g_{Q2}(n) = min_{Q2} n·q ≥ β ≥ h(n).  Nothing else about n is used, so which square owns
the normal is irrelevant.  Write g = w(ψ)/2 for Q2's half-width in the axis directions.

α ∈ [0°, 90°]:  h(n) ≤ n·z₂ − g_{Q2}(n) ≤ n·p < c (cos α + sin α), since p < (c, c) and the
coefficients are ≥ 0 and not both 0: (NE).

α ∈ (90°, 180°), ζ = α − 90°, n = n_W(ζ):  x₂ ≥ g (Q2 in the quadrant) and y₂ ≤ p_y + g < c + g,
so h(n) + g_{Q2}(n) ≤ −sin ζ x₂ + cos ζ y₂ < −g sin ζ + (c + g) cos ζ, i.e.
h(n) < c cos ζ − [g_{Q2}(n) − g (cos ζ − sin ζ)].  With φ = ψ − ζ, g_{Q2}(n) = w(φ)/2 and
g = w(ζ + φ)/2, so the bracket is ≥ sin² ζ by Lemma B0: (W).  α ∈ (270°, 360°): the mirror
image, (S).

α ∈ [180°, 270°], γ = α − 180°, n = −n_NE(γ):  Q2 ⊆ {cos γ x + sin γ y ≤ −β}, so
−β ≥ cos γ x₂ + sin γ y₂ + g_{Q2}(n_NE(γ)) ≥ (cos γ + sin γ) w(ψ)/2 + w(ψ − γ)/2 ≥ cos γ + sin γ
by Lemma B0′ (x₂, y₂ ≥ g), while −β ≤ −h(n) = m(γ): (P).  ∎

*Remark (what (P) is).*  For c > 1, (P) holds iff the pressed square [0, 1]² is itself a second
meeter of Q1: a separating line for the open square (0, 1)² and Q1 ⊆ quadrant has, up to the
sign of its normal, either a NE normal (then it passes through (1, 1) and gives (P) directly),
a NW or SE normal (then Q1 ⊆ {y ≥ 1} or {x ≥ 1}, which is (P) at γ = 90° or 0°), or a SW normal
(impossible: Q1 would be the origin).  The strict inequalities in (NE), (W), (S) come from the
OPEN box; the closed-box version replaces < by ≤ and characterises touching.

## 4. [T] Corollaries — what a doubly-met corner requires (derivations in `notes/derivation.md`)

**Cor. B1 (pressed ⇒ lonely, unit box).**  The pressed square (centre (g, g), g = w(θ)/2, any
tilt θ) admits no second meeter of (0, 1)².  *Proof.*  (NE) needs w(α − θ) < (2 − w(θ)) w(α)
for some α; but D(α) = w(α − θ) − (2 − w(θ)) w(α) is a sinusoid with coefficients of one sign on
each of [0, θ] and [θ, 90°] (monotone towards α = θ on both), and D(θ) = √2 (u − 1/√2)² ≥ 0 with
u = sin(θ + 45°).  (W) needs w(θ)(cos ζ − sin ζ) + w(ζ − θ) < 2 cos ζ − 2 sin² ζ for some ζ; for
ζ < 45° the left side is a positive combination of shifted w's in θ, minimal at θ ≡ 0 (value
2 cos ζ) or θ ≡ ζ (value 1 + cos 2ζ), both ≥ the right side; for ζ ≥ 45° the left side is
≥ 1 + √2 (cos ζ − sin ζ) ≥ 2 cos ζ − 2 sin² ζ (termwise: 2 sin² ζ ≥ 1, (√2 − 2) cos ζ ≥ 1 − √2,
−√2 sin ζ ≥ −√2, sum ≥ 0.17).  (S) is (W) for the pressed square at 90° − θ; (P) is vacuous.  ∎

**Cor. B2 (the slide family, mode (a)).**  Q1 slid δ ≥ 0 along the floor at tilt θ (centre
(g + δ, g)).  Clause (W) at ζ = θ (Q2 resting on Q1's upper-left edge, the "mode-(a)" partner)
reads 1 − δ sin θ < c cos θ; for c = 1: δ > tan(θ/2) = t.  The partner's lowest point is at
height sec θ − δ tan θ, so its intrusion below y = 1 is (δ − t) tan θ = 2t(δ − t)/(1 − t²).
(Numerics `results/check_b.json` `depth`: closed form vs grid, grid ≤ closed form by ≤ 0.026 at
pitch 0.04.)  For general c the mode-(a) threshold is δ = (1 − c cos θ)/sin θ.

**Cor. B3 (tilt 0, exact).**  Q1 = [a, 1 + a] × [b, 1 + b], 0 ≤ a, b < 1.  (NE) never holds
(a cos α + b sin α < 0 is impossible); (W) holds iff b < F(a) := max_{0 < s < min(a,1)}
s(a − s)/√(1 − s²); the maximiser solves s³ − 2s + a = 0, so with u = s: a = u(2 − u²),
F = u²√(1 − u²), u ∈ [0, 1] (F(a) = a²/4 + O(a⁴); F(1) = 0.300 at u = (√5 − 1)/2); (S) is the
mirror a < F(b).  Non-lonely iff b < F(a) or a < F(b).  (`lonely_exact.json` `theta0_law`.)

**Cor. B4 (the exact slide threshold).**  For the slide family at c = 1, (NE) and (S) fail for
every δ (they fail at δ = 0 by B1 and their left sides increase with δ), so
  δ_min(θ) = inf_{0 < ζ < 90°} R_θ(ζ)/sin ζ,  R_θ(ζ) = g (cos ζ − sin ζ) + w(ζ − θ)/2 − cos ζ + sin² ζ,
an explicit one-parameter minimisation [T].  At ζ = θ the quotient is tan(θ/2) (B2); the
minimiser is ζ = θ exactly for θ ≤ θ* = 56.76° [M], and beyond θ* it moves to ζ* < θ (the
partner's edge no longer rests on Q1's edge; Q1's upper vertex touches the partner's edge — the
crossing mode; ζ* = 47.3° / 41.5° / 36.2° / 30.8° / 24.7° / 17.2° at θ = 60°/65°/70°/75°/80°/85°),
giving δ_min = 0.5727 / 0.6118 / 0.6335 / 0.6302 / 0.5887 / 0.4778 [M, `results/slide169.json`]
against tan(θ/2) = 0.5774 / 0.6371 / 0.7002 / 0.7673 / 0.8391 / 0.9163.  At θ = 0 the infimum
is 0 (not attained: ζ → 0).  Widened box: the same formula with c cos ζ; δ_min = 0 for
θ ≤ 17.35° and θ ≥ 72.65° because the pressed square already admits the (NE) partner at α = θ
(w(θ) < c + √(c² − 1), the exact pressed-square condition at α = θ), and 0.1062 / 0.2238 /
0.3887 / 0.5472 / 0.5970 at 20°/30°/45°/60°/70°.  **The atlas thresholds** d*(θ) =
0.18/0.34/0.38/0.56/0.64/0.72 at 0°/15°/30°/45°/60°/75° (`two_meeter_atlas_v2.svg`) are the
first raster pitch at which a coarse Q2 search succeeded, not thresholds: the true values are
0 / 0.1317 / 0.2679 / 0.4142 / 0.5727 / 0.6302 [T formula, M values].

**The size of the lonely set [M].**  `results/lonely_exact.json` (pitch 0.02 raster of meeter
centres, Theorem B's clauses scanned at 1/4° with certified SAT witnesses for every non-lonely
cell): lonely fraction of unit-box meeter poses 0.80 / 0.82 / 0.79 / 0.76 / 0.72 / 0.68 / 0.64 /
0.62 / 0.60 / 0.59 at tilt 0° / 5° / … / 45° (symmetric beyond); widened 0.69 / 0.74 / 0.70 /
0.68 / 0.65 / 0.61 / 0.58 / 0.55 / 0.54 / 0.54.  `crit_vs_raster.json`: the criterion agrees with
the independent search raster (`lonely.json`, pitch 0.08) on all 783 cells at six tilts.

## 5. Lean — `Sideband.lean` (builds with no `sorry`, no new axiom; imports `SatInterior`, `Ceil`)

| name | statement | status |
|---|---|---|
| `sqdist_centre_le_half` | (F1): p ∈ q.set ⇒ (p − z)² ≤ 1/2 | [T] |
| `wrel_ge_one`, `proj_sq_le`, `sep_of_gsel` | a nonnegative selection row gives Δx² + Δy² ≥ 1 | [T] |
| `linf_sep` | **Lemma A1**: interior-disjoint ⇒ 1/2 ≤ Δx² ∨ 1/2 ≤ Δy² (from `sat_selection_thm`) | [T] |
| `inv_sqrt_two_le_abs`, `linf_sep_sqrt` | the same with 1/√2 ≤ \|Δx\| ∨ 1/√2 ≤ \|Δy\| | [T] |
| `Meets q c`, `InQuadrant q` | ∃ p ∈ q.set in (0, c)²; q.set ⊆ quadrant | defs |
| `vertex_mem` | z + a e + b e⊥ ∈ q.set for \|a\|, \|b\| ≤ 1/2 | [T] |
| `quad_centre_ge_half` | (F2): InQuadrant, t ∈ [0,1] ⇒ 1/2 ≤ cx, cy | [T] |
| `meeter_cx`, `meeter_cy` | Meets q c, c ≤ cx ⇒ (cx − c)² < 1/2 | [T] |
| `sq_sub_lt_of_ge`, `sq_sub_lt_of_lt`, `same_side_sq_lt` | one cell ⇒ Δ² < 1/2 (NE side unconditional; SW side needs (c − 1/2)² < 1/2) | [T] |
| `cell_hyp_of_lt` | 1/2 ≤ c < 1/2 + 1/√2 ⇒ (c − 1/2)² < 1/2 | [T] |
| `distinct_cells` | **Lemma A2**: two interior-disjoint meeters in the quadrant, (c − 1/2)² < 1/2, t ∈ [0,1] ⇒ ¬((cx < c ↔ cx′ < c) ∧ (cy < c ↔ cy′ < c)) | [T] |
| `not_both_ne`, `sideband_a` | **SIDEBAND (a)**: ¬(c ≤ cx ∧ c ≤ cy ∧ c ≤ cx′ ∧ c ≤ cy′); cx < c ∨ cy < c ∨ cx′ < c ∨ cy′ < c — no quadrant, no bound on c | [T] |
| `supp`, `ClauseNE/W/S/P`, `SecondMeeterCriterion c` | **Theorem B** as a proposition: for every q with t ∈ [0,1] in the quadrant meeting (0, c)², (∃ q2 second meeter) ↔ (NE ∨ W ∨ S ∨ P) | [C] stated |
| `clauseP_second_meeter` | (P) ⇒ the pressed square ⟨1/2, 1/2, 0⟩ is a second meeter (1 ≤ c) | [T] |

Obligations left for `SecondMeeterCriterion` [C], each a finite computation in the document's
proof: (i) the (W)/(S)/(NE) witness squares as `PSq` values with `t = tan(ζ/2) = sin ζ/(1 + cos ζ)`
and their `Meets`/`InQuadrant`/separation facts (needs the "separated ⇒ interior-disjoint"
direction of SAT for one axis, which is elementary from `mem_interior_iff_uv`); (ii) Lemma B0
and B0′ as inequalities between `wrel`-type expressions (piecewise `nlinarith` after a case split
on the signs of the four cos/sin products); (iii) the four-quadrant case analysis of the
selection axis returned by `sat_selection_thm`.  Everything the k0 rows of §6 consume today
(R1, R2) is covered by the [T] rows; R3 (the lonely NO-family) rests on Theorem B's (⇒)
direction, which is [T] on paper and [C] in Lean.

## 6. Consumption by the k0 cascade (A168) — the exact rows

All statements are on F = Δ_λ P at the WIDENED box (c = 1 + w), the form K0-BLOCKED is stated
in (`k0_route.md` §4.2); every square of F is a unit square in [0, s0]².  Lemma K0-WIDEN gives the
transfer to P: a corner of F met (at the widened box) by ≤ 1 square is a corner of P met (at the
unit box) by ≤ 1 square, hence K0-FREE kills P.

**Row R1 (cells) — a PAIR row for the crowd covers.**  At each corner the two crowd squares
have centres in distinct cells of the grid at threshold c = 1 + w (Lemma A2), and their centres
satisfy max(|Δx|, |Δy|) ≥ 1/√2 (Lemma A1).  Consumption: the corner-first branching of §4.2 over
pairs (B_i, B_j) of reach-cover boxes drops every pair whose centre boxes lie in one cell, and
every pair with max over the two boxes of the ℓ∞ centre distance < 1/√2 (this is exactly
`cores_meet` for the axis core of half-side 1/(2√2) = 0.35355, so it subsumes the 0.34 cores of
A60's covers and is implied by A135's exact cores on narrow bins; its value is the cell
bookkeeping).  Boxes straddling x = c or y = c are split at the line first.  This is a
box-list row (a prune of the YES-pair list), not an LP row.

**Row R2 (band / outside) — the split A168 asked for, BL, H absent.**  The two crowd centres
z₁, z₂ lie in M := [1/2, c + 1/√2)² ∩ {(x − c)⁺² + (y − c)⁺² < 1/2} (the meeter-centre set; the
quarter-disc clause is the exact NE reach, (F1)) and in distinct cells, so the corner case
splits into the six unordered cell pairs
  {SW, NW}, {SW, SE}, {SW, NE}, {NW, SE}, {NW, NE}, {SE, NE},
with SW = [1/2, c)², NW = [1/2, c) × [c, c + 1/√2), SE its mirror, NE = {(x, y) ≥ (c, c) :
(x − c)² + (y − c)² < 1/2}.  The BAND meeter of A168's step is any centre in SW ∪ NW ∪ SE
(x < c or y < c); it hugs the wall whose band it is in (NW: the left wall, x < c; SE: the
floor; SW: both), and is priced by A144's chord row on that wall: `minchord` on the clipped pose
box against the wall-parallel guard line at distance c from the wall.  The OUTSIDE meeter is the
NE one, confined to the quarter-disc of radius 1/√2 at the box corner (c, c); in pose space its
tilt must point a vertex at (c, c) (centre distance r ∈ [1/2, 1/√2) from the corner admits only
tilts with the vertex direction within arccos(1/(2r)) of the diagonal), which A161's exact reach
test decides per box.  {NW, SE} is the "one up the wall, one along the floor" case; {SW, ·} are
the "deep meeter" cases; and by SIDEBAND (a) the pair {NE, NE} never occurs.

**Row R3 (lonely poses) — a NO-family for EVERY square, consumed by the LP columns AND by
the covers.**  Theorem B (with clause (P) for c > 1) decides, for a pose (x, y, θ), whether a
second meeter of (0, c)² can exist.  In a K0-BLOCKED packing no square of F is in a lonely pose
at any corner: if Q ∈ F were lonely at corner c′, the corner would be met by Q alone at the
widened box, and K0-WIDEN + K0-FREE kill P.  So the lonely set L_c′ ⊂ pose space is a
NO-family at the root of T_B, hence at every node: (i) LP columns (free placements) meeting
L_c′ are dropped from the pool; (ii) crowd-cover boxes contained in L_c′ are dead (T leaf);
(iii) a conditioned box B_H is clipped to B_H ∖ L_c′.  Box test (sound): a box B is inside
L_c′ iff for every pose in B all four clauses fail; the clauses are "∃ζ: linear(x, y) +
w(θ − ζ)/2 < r(ζ)" with w ≥ 1, so
  B ⊆ L_c′  ⇐  ∀ζ ∈ [0°, 90°]: min_{corners of B} (y cos ζ − x sin ζ) + 1/2 ≥ c cos ζ − sin² ζ,
  and the mirror, and ∀α: min_{corners}(x cos α + y sin α) + 1/2 ≥ c (cos α + sin α),
  and [c > 1] the pressed square [0, 1]² is NOT interior-disjoint from every pose of B
  (the polygon-core test against the pressed square's core, `polycore`),
each a one-parameter check in ζ (rational in T = tan(ζ/2): sin ζ = 2T/(1 + T²), cos ζ =
(1 − T²)/(1 + T²), so the inequality clears to a polynomial in T of degree 4 and is decided by
Bernstein positivity on [0, 1], A126/A133's `posCheck` machinery).  Size of the family [M]
(§4): the lonely fraction of widened-box meeter poses is 0.54–0.74 across tilts, so R3 removes
the majority of the corner reach set from the crowd covers.  This is the row the PI's "the deep
meeter's gap ≥ δ_min(θ)" becomes: for a meeter sitting on the floor at tilt θ the non-lonely
poses are exactly δ > δ_min(θ) (Cor. B4: tan(θ/2) up to θ*, the crossing mode beyond, and 0 for
the widened box below 17.35°), and for a meeter off the floor the two-dimensional region of
Theorem B.

**With a conditioned square H present (BL, H = the k0 hard square).**  Nothing in R1–R3 uses
H; H enters through A158's mutual clip: every crowd box is clipped against K′(H) BEFORE R1–R3
are applied, and R3's clause test is run on the clipped box (a clipped box is a union of
sub-boxes; test each).  The exact regions for BL with H present are therefore the H-absent
regions intersected with the complement of the poses meeting K′(H) — no new formula, and
Theorem B's witnesses (which lie at the corner, far from H's core for the k0 cells where
|z_H − corner| ≥ 1.57, A166) are unaffected, so R3's lonely set is the SAME set with H present.

**What A168 should do with it, exactly.**  (1) Apply R3 to the four corner reach covers at the
root (drops most boxes); (2) branch the surviving boxes by cell (R2) and pairs by R1;
(3) price the band meeter by A144's chord row on the wall it hugs (`minchord` per clipped box)
and the NE meeter by A161's exact reach test on the quarter-disc; (4) the K0-PAIR census of
`k0_route.md` §4.4 (N_pair ≈ 3.4·10⁴ per corner at A60's box width) should be re-run with R3 +
R1: the expected reduction is by the non-lonely fraction squared on the pair list, i.e. to roughly
(0.4)² · 3.4·10⁴ ≈ 5·10³ pairs per corner [S].
