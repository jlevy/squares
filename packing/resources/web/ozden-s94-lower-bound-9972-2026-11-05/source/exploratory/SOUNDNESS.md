# Soundness of `rdcheck` (our rectangle-density + angle-net checker)

Code: `results/checker/prep.py` (exact front end, Python `Fraction`), `results/checker/rdcheck.c` +
`geom.h` (branch and bound, double with a long-double fallback, outward error terms).
Written from the mathematics below; no published checker source was read (only the README/soundness prose
of the published packets and `docs/sqverify_fast-SOUNDNESS.md`).

## 1. The claim

A certificate gives exact rationals `n, L, B`, a half-angle net `(D, m)` (`proof_net`, else the standard
`D = 83/40000, m = 200`), and orbit representatives `R_j = [x1,x2]×[y1,y2]` with masses `w_j ≥ 0`.
The measure is `μ = Σ_j Σ_{S∈D4} (w_j/8) · Unif(S(R_j))`, i.e. density `g = Σ_j w_j/(8|R_j|) Σ_S 1_{S(R_j)}`,
`D4` the symmetry group of `K = [0,L]²`. So `g ≥ 0`, `g` is `D4`-invariant, `μ(K) = M = Σ w_j`.

Net: `t_r = r D` (r = 0..m), `θ_r = 2 arctan t_r`, `c_r = (1-t_r²)/(1+t_r²)`, `s_r = 2t_r/(1+t_r²)` (exact).
Core `Q_r(p)` = closed square of side `B`, centre `p`, sides in directions `θ_r`, `θ_r + π/2`:
`Q_r(p) = {q : |u_r·(q-p)| ≤ B/2, |v_r·(q-p)| ≤ B/2}`, `u_r = (c_r, s_r)`, `v_r = (-s_r, c_r)`.

**Theorem.** Suppose (exact) `M < n`; `0 < B < 1`; `B(1+D) < 1`; `t_m² + 2t_m − 1 > 0` (i.e. `t_m > tan(π/8)`);
`t_m ≤ 1/2`; all rectangles inside `K`. Let `a_r = max(0, t_r − D/2)`, `ρ(a) = (1+2a−a²)/(2(1+a²))`,
`μ_r = max(ρ(a_r), B(c_r+s_r)/2)`, `U_r = L − μ_r`. If for every `r` and every `p ∈ [L/2, U_r]²`,
`μ(Q_r(p)) ≥ 1`, then `n` non-overlapping unit squares do not fit in `K`; hence `s(n) ≥ L`.

*Proof.*
1. *Fold.* A unit square's orientation `φ` is defined mod `π/2`; take `φ ∈ [0, π/2)`. If `φ > π/4` reflect the whole
   packing in the diagonal `y = x` (maps `K` to `K`, preserves `g` and disjointness, sends `φ ↦ π/2 − φ`). So all
   `φ ∈ [0, π/4]`, `τ = tan(φ/2) ∈ [0, tan π/8] ⊂ [0, t_m]`.
2. *Net.* Consecutive `t_r` differ by `D`, so some `r` has `|τ − t_r| ≤ D/2`. With `δ = φ − θ_r`,
   `z = |tan(δ/2)| = |τ − t_r|/(1 + τ t_r) ≤ D/2`.
3. *Shrink.* In the unit square's own frame the concentric core at angle `θ_r` is a square of side `B` rotated by `δ`;
   its extent along each axis of the unit square is `B(|cos δ| + |sin δ|) = B(1 + 2z − z²)/(1 + z²) ≤ B(1 + 2z) ≤ B(1 + D) < 1`
   (`(1+2z)(1+z²) − (1+2z−z²) = 2z² + 2z³ ≥ 0`). So the closed core lies in the open unit square.
4. *Domain.* The unit square lies in `K`, so its centre is at distance `≥ (cos φ + sin φ)/2` from each wall; on `[0, π/4]`
   this half-width increases with `φ`, and `τ ≥ a_r`, so the distance is `≥ ρ(a_r)` (`ρ(τ)` is the half-width written in
   the half-angle tangent). The core lies in the unit square, hence in `K`, so the distance is also `≥ B(c_r+s_r)/2`.
   Thus the centre `p ∈ [μ_r, L − μ_r]²`.
5. *Quarter turn.* Let `σ` be the rotation by `π/2` about `(L/2, L/2)`. `σ(Q_r(p)) = Q_r(σp)` (a square is invariant
   under a quarter turn about its centre) and `g∘σ = g`, so `μ(Q_r(p)) = μ(Q_r(σp))`. `σ` preserves `[μ_r, L−μ_r]²`, and every
   point of it has an image under a power of `σ` in the closed quadrant `[L/2, L−μ_r]²`. So checking `[L/2, U_r]²` suffices.
6. *Count.* Cores of different squares lie in the open interiors of disjoint-interior squares, so they are pairwise
   disjoint; each has `μ ≥ 1`; so `n ≤ μ(K) = M < n`, contradiction. ∎

`prep.py` checks every premise except coverage in exact `Fraction` arithmetic (`premises()`), and computes `U_r`, `L/2`
exactly, emitting them rounded **outward** (`U_r` up, `L/2` down: the searched box contains the exact quadrant).
Decimal inputs are read as exact decimals (JSON floats are parsed as strings).

## 2. Reduction to a lower-bound measure (input rounding)

`prep.py` expands each orbit into its 8 images (coincident images are kept as separate, additive terms, which is
exactly the definition of `g`) and writes each image with its coordinates rounded **inward** (x1,y1 up; x2,y2 down; 28
significant digits) and its density `w/(8|R|)` rounded **down**. `rdcheck` parses these with `strtold` and nudges each
value one more `long double` ulp inward/down, then converts to double rounding inward/down again. So every stored
rectangle `R'_k ⊆ R_k` and every stored density `ρ'_k ≤ ρ_k`, and `g' = Σ ρ'_k 1_{R'_k} ≤ g` pointwise. Any lower bound
for `∫_Q g'` is one for `μ(Q)`.

The core is also replaced by a smaller square: double (or long double) `c̃, s̃` are the correctly rounded quotients of the
exact integers `c_r·den, s_r·den, den` (< 2^53). With `|c̃ − c|, |s̃ − s| ≤ 2^-53`, for `|q − p|_1 ≤ 2` the slab values
differ by `< 3·10^-16`, so the computed square with half side `h_in = (B/2)↓ − 3·10^-15` (double path; `(B/2)↓ − 10^-15` in
the long-double path) is contained in the exact core whenever the relevant points are within the core's bounding box
(the area routine first clips to a superset of that box). So `F'(p) = ∫_{Q̃(p)} g' ≤ μ(Q_r(p))`.

## 3. Branch and bound over centres (per direction)

Boxes `C = [x0 ± dx] × [y0 ± dy]` (doubles; all coordinates in `[L/2, L]`, so `hi − mid` is exact by Sterbenz; children are
`[lo, mid]`, `[mid, hi]` and cover the parent). For each box the rectangles are classified (inherited from the parent):

* **inside** (R ⊆ Q̃(p) for all p ∈ C): with `Δ = m − p0`, `d_u = |c̃Δx + s̃Δy|`, `e_u = c̃ w_x + s̃ w_y`, `b_u = c̃ dx + s̃ dy`
  (and `v` likewise), if `d_u + e_u + b_u ≤ h_in − τ` and `d_v + e_v + b_v ≤ h_in − τ`, `τ = 10^-11` (covers the
  double rounding of these few operations; `w_x, w_y` are rounded up to contain the stored rectangle). Triangle
  inequality. Inside rectangles contribute their mass `ρ'|R'|` (rounded down) for every `p ∈ C` and are removed.
* **dropped**: rectangles certified disjoint from all cores of the box are removed. *Soundness does not depend on this
  test*: removing any rectangles from the sum only lowers the function being bounded, and all later bounds (value and
  derivative) are bounds for the reduced sum. Hence a misclassified "outside" rectangle can never cause a false accept.
* **boundary**: the rest.

For the box, the function bounded is `G(p) = I + Σ_{k∈bd} ρ'_k |R'_k ∩ Q̃(p)|` (`I` = inherited inside mass), and
`G ≤ F' ≤ μ(Q_r(·))` on `C`. Two lower bounds on `min_C G` are used and the larger taken:

* **(E) erosion.** `∩_{p∈C} Q̃(p) ⊇ Q⁻ := {q : |ũ·(q−p0)| ≤ h_in − b_u, |ṽ·(q−p0)| ≤ h_in − b_v}` (since `|ũ·(p−p0)| ≤ b_u`).
  So `G(p) ≥ I + Σ ρ'_k |R'_k ∩ Q⁻|` on `C`.
* **(MV) mean value.** `G` is Lipschitz, so absolutely continuous on segments. For an axis rectangle `R` and a translated
  convex `Q(p)`, `∂_x |R ∩ Q(p)| = ℓ(left edge ∩ Q(p)) − ℓ(right edge ∩ Q(p))` and `∂_y` = bottom − top, for a.e. `p`
  (moving the square by `+t` is moving `R` by `−t` relative to it; differentiate the 1-D sections, Fubini).
  For `p ∈ C`, `Q⁻ ⊆ Q̃(p) ⊆ Q⁺ := {|ũ·(q−p0)| ≤ h + b_u, |ṽ·(q−p0)| ≤ h + b_v}`, so each edge length is enclosed by
  `[ℓ(edge ∩ Q⁻), ℓ(edge ∩ Q⁺)]` (each widened by `10^-11`). Summing `ρ'·` intervals gives enclosures `[gx_lo, gx_hi]`,
  `[gy_lo, gy_hi]` of `∂G` a.e. on `C`; with `G_x = max(|gx_lo|, |gx_hi|)`, along the path `p0 → (p_x, y0) → p` inside `C`,
  `G(p) ≥ G(p0) − G_x dx − G_y dy`. `G(p0)` uses the area of each boundary rectangle within `Q̃(p0)`.

A box is **accepted** when `max(E, MV) − err ≥ 1`. If the centre value `G(p0) < 1 − 10^-9` the direction is refused with
a counterexample candidate (confirmed afterwards in exact rationals by `prep.exact_F` when reported as a rejection).
Otherwise the box is split along its longer side; boxes below `10^-12` (or depth > 120) are refused as unresolved.
A direction is VERIFIED only if every leaf was accepted; the certificate is accepted only if every direction `r = 0..m`
is VERIFIED and the exact premises hold.

At `θ = 0` (`s = 0`) nothing changes: the formulas hold for every angle (the derivative formula is a.e.).

## 4. Floating-point error terms (lemma F)

Area of `R ∩ (rotated rectangle)`: the axis rectangle is first clipped to a superset of the core's bounding box (exact
min/max), so all coordinates relative to `p0` have magnitude `≤ 0.71`; rotation (2 mul + 1 add per coordinate), four
Sutherland–Hodgman passes (intersection point `P + t(Q−P)` with `t` clamped to `[0,1]`; its error is `O(u|Q−P|)` with
`|Q−P| ≤ 2`), and a shoelace sum over ≤ 8 vertices taken relative to the first vertex. A perturbation of the polygon's
vertices by `ε` changes the area by at most `perimeter·ε ≤ 4ε`; counting operations gives an absolute error below
`100 u` (`u = 2^-53 ≈ 1.1·10^-16` in double, `2^-64 ≈ 5.4·10^-20` in long double). We charge
`2·10^-13` (double; ≥ 18× the estimate) resp. `2·10^-16` (long double; ≥ 37×) **per unit density per boundary term**,
plus `10^-13·I` (double; `10^-16·I` long double) for the summation of the inside masses, plus `10^-15` per term, plus a
relative `10^-12` on the derivative penalty. A box whose double bound falls short of 1 by less than twice its error
term is recomputed entirely in long double (`ld` counts in the logs).
This is an a-priori error analysis with large safety factors, not directed-rounding interval arithmetic; that is the
one place where the verdict rests on a hand analysis rather than on exact arithmetic. Every premise and the D4 expansion
are exact. Rejections are confirmed by exact rational evaluation of a centre (`exact_F`).

## 5. What the verdict proves

`ALL_DIRECTIONS_VERIFIED` on all `m+1` directions + `PREMISES_HOLD` ⇒ `s(n) ≥ L` by §1–§4. Any other outcome proves
nothing.

## 6. Rescaled certificates (`results/rescaled/`)

`rescale.py` builds a new certificate from a published one by a similarity (rectangles ×λ, `B' = λB`, masses unchanged,
optionally a finer uniform net). The resulting file is an ordinary certificate. Its premises (including
`B'(1+D') < 1`) are checked exactly by `prep.py`, and its coverage on the **whole** new net by `rdcheck`, exactly as
for any other input. No property of the original certificate or of the rescaling is assumed.
