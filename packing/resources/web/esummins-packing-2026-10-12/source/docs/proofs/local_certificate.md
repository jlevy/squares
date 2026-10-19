# LOCAL — the selection tree around a known minimum: Theorem LOCAL, Lemmas LEAF / COVER / RELAX / STAB, the Trump boundary, and the measured radius — A116, 2026-09-06

Target (A116 BRIEF; PI sharpening of the same day: the stability radii of the minimum's own contacts as the
primary object): a fast, sound certificate that a NEIGHBOURHOOD N of a known minimum z* (radius ~0.1 in position,
≥ 10° in tilt) contains no packing of side ≤ s0, built from the load-bearing squares L of z* and the class pins P
alone.  Labels: [T] proved, [S] routine given cited items, [M] measured (`attempts/A116-local-selection-tree/
{code,results,logs,notes}`, ≤ 2 BLAS-pinned processes, pure geometry/LP, read-only on every campaign), [F]
finding, [C] open.  Conventions as in `grain_flood.md`: s0 = 969271/250000 = 3.877084, ŝ = 3.877083590022814,
W = [3.82, s0]; S07 = A108's exact packing (s* = 2 + 4√2/3 = 3.885618083, tilts 45°), S02 = the k7 pinwheel
(s* = Λ(θ*) = 3.886746029, θ* = 48.43512°); the class frames are A57's: pins on slot lines c = α + βs (β ∈ {0,1})
in slack cores of half-width h = δ/√2, δ = 10⁻², tilt exactly 0; k5_11 = {BL(0,0), BL(0,1), TL(0,0), BL(1,0),
BR(0,0)}, trump5 = {BL(0,0), BL(1,0), BL(0,1), BR(0,0), TR(0,0)}.  The chain menu Λ, Y, D, F_T, A is A110's
(`grain_flood.md` §2).  n-general means: n unit squares, any target side s0, any class, any minimum z*.

## 0. Verdict

> **The certificate exists, is n-general, and its radius is set by ONE thing: the tangential slack of the
> minimum's own contacts — the distance the riding vertex of each load-bearing contact can slide before it
> reaches the end of its edge (Lemma STAB).**  Where that slack is large the neighbourhood is a single leaf;
> where it is small (S07: f0's vertex sits 0.057 below BL(0,1)'s corner (1,2) — the Trump boundary; S02: f1's
> corner hangs 0.085 over f3's corner) the pair must be case-split, and the split leaf carries a DIFFERENT chain
> formula (S07: the gap chain F_T; S02: the diagonal chain D alone), which dips below s0 exactly at Trump's tilt
> and at its mirror image — so the neighbourhood must be CUT there, at a single inequality per shadow, and the cut
> is the only place the other squares of the packing are missed.  Numbers: §5–§6 (the measured grid), §7 (the
> consumer).

## 1. The objects (n-general)

**Configurations, packings.**  n closed unit squares Q(c_i, θ_i) ⊂ [0, s]², pairwise interior-disjoint.  For a
pair (i, j) and a *signed selection* σ = (owner o ∈ {i, j}, axis k ∈ {1, 2}, sign ε ∈ {±1}) the row is

  g_σ(c, θ) := ε (c_other − c_o)·a_k(θ_o) − 1/2 − w(θ_o − θ_other)/2 ≥ 0,   a_1(θ) = (cos θ, sin θ), a_2 = a_1(θ + 90°),
  w(d) = |cos d| + |sin d|.

**Lemma SAT [T; `lean/…/CaseSat.lean` `sat_squares`].**  Two unit squares are interior-disjoint iff g_σ ≥ 0 for
some one of their eight signed selections.  (⇐: the projections on a_k(θ_o) do not overlap in their interiors.
⇒: if all eight gaps are < 0 the four projection overlaps are proper intervals, so a slight shrink of both squares
still satisfies the four overlap inequalities of `sat_squares`, which then gives a common point of the shrunk
squares, i.e. an interior point of both originals.)  The sign ε is the sign of the centre projection: `le_total`.

**The local hypothesis N.**  Fix z* with load-bearing set L, the class pins P (slack h), a side window W =
[s_lo, s_hi] ∋ s0, radii (r, ρ), a tilt cut.  N is the hypothesis on a configuration at side s: s ∈ W; for each
p ∈ P some square has centre in α_p + β_p s + [−h, h]² and tilt 0; for each ℓ ∈ L some OTHER square has pose in
F_ℓ = [c_ℓ ± r]² × ([θ_ℓ ± ρ] ∩ cut) — all these squares distinct.  The anchors c_ℓ are z*'s poses in the class
frame at s0 (the dilation c·s0/s* for the tilted squares, the slot position at s0 for a load-bearing slot square
that is not a pin).  Dead(N, s0): no packing of n squares at side ≤ s0 satisfies N.

**Reduction DROP [T].**  If a packing of n squares at side s satisfies N, the |P| + |L| squares that witness N form
a packing of |P| + |L| squares at side s satisfying N.  So Dead_{L∪P}(N, s0) (the statement for |P| + |L| squares)
implies Dead(N, s0).  Everything below is about Dead_{L∪P}; the other squares never appear, and §4 says exactly
what that costs.

**Near and far pairs; leaves.**  Bodies B = L ∪ P.  Over a tilt cell K (a product of tilt intervals, one per free
body; pins have tilt {0}) and the boxes, every g_σ has an interval enclosure [g_σ]_K (a111lib.IV, iv_cos, the exact
envelope w_range of |cos| + |sin|).  A pair is FAR on K if some σ has [g_σ]_K ⊆ [0, ∞) (the pair is disjoint on
every configuration of K: no row, no branch); NEAR otherwise; a selection σ is POSSIBLE on K if sup [g_σ]_K ≥ 0,
IMPOSSIBLE otherwise; a pair with no possible selection makes K IMPOSSIBLE (no disjoint configuration on it).  A
*leaf* λ on K assigns one possible selection to every near pair; the number of leaves is Π_pairs (#possible) ≤ 8^k,
k = number of near pairs.  The leaf polyhedron at fixed tilts θ ∈ K:

  P_λ(θ) := {(s, c, u) : s ∈ W, pins α + βs + u, |u| ≤ h, c_ℓ ∈ [c_ℓ ± r]², container rows c·e ≥ h(θ), s − c·e ≥ h(θ),
             g_{λ(i,j)}(c, θ) ≥ 0 for every near pair}.

Square–wall contacts need no selection (the container is convex).  Walls are the rows c·e − h(θ) ≥ 0.

## 2. Lemma COVER and Lemma LEAF

**Lemma COVER [T] (the selections cover every disjoint configuration).**  Let K be a tilt cell and z a packing of
L ∪ P at side s satisfying N with tilts θ ∈ K.  Then (s, c, u) ∈ P_λ(θ) for some leaf λ on K, and λ's selections
are all possible on K.  *Proof.*  For each near pair pick, by Lemma SAT, a selection with g ≥ 0 at z; it is
possible on K because its enclosure contains the value g(z) ≥ 0.  The container and pin rows hold at z by
hypothesis.  Far pairs impose no row.  ∎  Consequently the packings satisfying N with tilts in K are contained in
⋃_λ ⋃_{θ∈K} P_λ(θ) over the possible leaves — a finite case split (≤ 8^k cases; in Lean, `sat_squares` per near
pair and `le_total` on the projection sign, then `rcases`).

**Lemma LEAF [T] (a fixed selection forces the side ≥ a chain length).**  Fix λ and θ.  v_λ(θ) := min{s : (s, c, u)
∈ P_λ(θ)} (+∞ if empty) is the value of a linear programme whose rows are affine in (s, c, u) (Fact A of
`nocrit_k0_blocked.md` §1: at fixed tilts every row is affine).  By LP duality there are multipliers y ≥ 0 on the
rows with Σ y_k a_k(θ) = 0 on the (c, u) block and Σ y_k b_k = 1 on s, and then for EVERY point of P_λ(θ)

  s = Σ_k y_k (b_k s + a_k·(c, u)) ≥ Σ_k y_k d_k(θ) = v_λ(θ)          (rows written a_k·(c,u) + b_k s − d_k ≥ 0),

the "pairwise separating-axis inequalities summed along the chain": the sum Σ y_k g_k ≥ 0 of the leaf's rows with
the centre coefficients cancelling is one `linarith` step.  By Lemma GRAIN-LP (`grain_flood.md` §1) the support of y
is a balanced contact-force system with unit load on the far walls, i.e. a wall-to-wall load path; by Lemma GRAIN
(chain form) its value along a chain of the support reads Σ_j Δ_j(θ_j) + gap terms — the chain formula of the leaf.
If the support uses a box row (c_ℓ ≤ c_ℓ* + r) or a core row (u ≤ h), the formula carries the corresponding term
(−r, −h·coefficient): these are the "s* − r" and pin-slack losses of A111; if it uses none, v_λ is a closed-form
function of θ alone (Λ, Y, D, F_T, … or their two-tilt generalisations), independent of r.  ∎

## 3. Theorem LOCAL and the certificate

**Theorem LOCAL [T] (the local certificate; n-general).**  Let 𝒦 be a finite cover of N's tilt box by cells.
Then

  Dead_{L∪P}(N, s0)  ⟺  for every cell K ∈ 𝒦 and every possible leaf λ on K:  inf_{θ∈K} v_λ(θ) > s0.

Hence Dead(N, s0) follows, with no dependence on the other n − |L| − |P| squares (Reduction DROP).

*Proof.*  ⇐: a packing at side ≤ s0 satisfying N has tilts in some K and lies in some P_λ(θ) (Lemma COVER), so
s ≥ v_λ(θ) > s0 (Lemma LEAF).  ⇒: if v_λ(θ) ≤ s0 for some θ ∈ K, the LP minimiser (s, c, u) ∈ P_λ(θ) is a
configuration of L ∪ P at side s ≤ s0: it lies in the boxes and cores, in the container, and every pair is
interior-disjoint — the near pairs by their selected rows (Lemma SAT), the far pairs by the definition of far —
so it is a packing satisfying N.  ∎

**The certificate.**  For each (K, λ): the affine relaxation of Lemma RELAX (§3.1) over K, an LP in (s, c, u, t)
whose infeasibility or value > s0 is witnessed by Farkas multipliers (the leaf certificate, one `linarith` on the
relaxed rows per cell), plus the finite case split of Lemma COVER (per near pair, `sat_squares` + `le_total`) and
the cell cover (a bisection tree: a `Finset` cover, trivial to check).  The IMPOSSIBLE selections are discharged by
the interval enclosure (a polynomial inequality in (cos, sin) at the endpoints — `nlinarith`-sized, as A111's O1).
This is A111's leaf O1–O4 with two changes: **every near pair is case-split, never dropped** (O1), and the
relaxation is that of §3.1, second-order in the cell width (O3).

### 3.1 Lemma RELAX (the affine rows over a tilt cell) [T]

Fix a cell K, a row g_σ ≥ 0 of a leaf (owner o with tilt interval [θ* − hw, θ* + hw], hw ≤ 60°), and write, with
a* = a_k(θ*), a*⊥ = a_k(θ* + 90°), the two affine functions of the LP variables p = ε (c_other − c_o)·a*,
q = ε (c_other − c_o)·a*⊥, and φ = t_o − θ* for the owner's tilt variable t_o ∈ [−hw, hw] + θ*.  Then on K

  ε (c_other − c_o)·a_k(θ_o) = p cos φ + q sin φ ≤ p + |q| sin hw + max(0, −p_lo)(1 − cos hw)         (A)
  q sin φ ≤ q φ + Q hw³/6,   q φ ≤ min(q_hi φ − hw q + q_hi hw,  q_lo φ + hw q − q_lo hw)                (B)

where [q_lo, q_hi] is the range of q over the boxes (Q = max |q|), p_lo the minimum of p; |q| in (A) is replaced
by its chord over [q_lo, q_hi]; and w(t_o − t_x), h(t) = w(t)/2 in the support and wall terms are replaced by
affine LOWER bounds in the tilt variables: the chord of the concave piece when the relative-tilt cell contains no
multiple of 90°, and at an interior kink k·90° the two lines w ≥ cos h′ ± (sin h′/h′)(t − k), h′ the larger
distance from the kink to the cell's ends.  Every resulting affine row is implied by the true row for every
configuration of the cell; the loss is ≤ p(1 − cos hw) + (1 − cos h′) + Q hw³/6 (second order) plus the McCormick
term (q_hi − q_lo)·hw/2 of (B), which halves under a split of the q-range (a valid LP case split: q ≤ m or q ≥ m).

*Proof.*  (A): for p ≥ 0 the maximum of p cos φ + q sin φ over |φ| ≤ hw is √(p² + q²) ≤ p + q²/2p when |q| ≤ p tan hw
(and q²/2p ≤ |q| sin hw for hw ≤ 60°) and p cos hw + |q| sin hw otherwise; for p < 0 the cosine term is ≤ p cos hw
= p + (−p)(1 − cos hw).  |q| ≤ chord by convexity.  (B): |sin φ − φ| ≤ hw³/6, and the McCormick planes are the
concave envelope of the bilinear q φ on a box.  The w-bounds: w is concave on each 90° piece (its chord lies
below it); at a kink, |sin d| ≥ |d| sin h′/h′ and cos d ≥ cos h′ for |d| ≤ h′.  Each replacement weakens the row
(a larger left side, a smaller right side), so the relaxed row is implied.  ∎

*Remark (why A111's leaf stopped at r < s* − s0 and this one does not).*  A111 dropped AMBIGUOUS pairs, so the
chain rows were missing and the LP escaped to the box rows, whose contribution is exactly −r (the "s* − r"
law measured there); it also used the chord bound |a(θ) − a(θ*)| ≤ Δ on the whole product, a first-order loss
|d|·hw ≈ 1.2 hw per row, so 4°-wide cells lost ≈ 0.01, the whole margin.  With every pair case-split, the chain rows
are present and r enters only through the McCormick term, i.e. through the product of the position range and the
tilt-cell width — not through the value (§5: the certified minimum is within 10 % of s* at every certified N).

### 3.2 Lemma STAB — the stability radius of a contact (the PI's route) [T + M]

Let (i, j) be a contact of z* with selection σ* = (owner j, edge e with outward normal n, ε), the riding vertex v
of Q_i (its extreme vertex in direction −n) at tangential coordinate τ ∈ [−1/2, 1/2] along e from e's midpoint.
Say σ* is FORCED on a box B of poses of (i, j) if every interior-disjoint configuration in B satisfies g_{σ*} ≥ 0
(so the row of σ* may be used on B without any case split).

(i) [T] If σ* is not forced on B, some configuration in B is interior-disjoint with g_{σ*} < 0, i.e. Q_i's extreme
vertex is strictly below the line of e while Q_i ∩ Q_j has empty interior; then the chord Q_i ∩ line(e) lies
entirely outside the segment e — the riding vertex has passed an END of e (mechanism (a)), or the extreme vertex of
Q_i in direction −n is a different vertex than at z* (mechanism (b), which needs the relative tilt to cross a
multiple of 90°).  *Proof.*  If the chord met the open segment e at a point p, Q_i (convex, with v strictly below
the line and its top above it) would contain a small disc-sector around p below the line, inside Q_j: an
interior overlap; meeting e at an endpoint only is the corner-touching configuration, which is exactly the
transition of mechanism (a).  ∎  So the forced radius is governed by the tangential slack 1/2 − |τ| (mechanism
(a)) and the relative-tilt margin (mechanism (b)); to first order, with per-square centre boxes of half-width δ
and tilt half-width ρ, the riding vertex drifts tangentially by at most 2δ (|t_x| + |t_y|) + ρ√2 (both squares
rotate a lever of length 1/√2), so δ_est = slack / (2(|t_x| + |t_y|) + √2 κ) for ρ = κ δ (κ in radians per unit).

(ii) [T] FLUSH contacts (parallel edges, overlap ℓ): both owners' rows are tight at z* and neither alone is forced
at any δ > 0 (tilting Q_i by ε and sliding it by more than ε/2 dips a vertex below the other's edge line while a
different axis separates), but the DISJUNCTION "σ_i or σ_j" is forced until the tangential slide reaches ℓ; a
flush contact therefore costs one binary case split (two leaves with the same chain value to first order).  This is
the "~2^k" of the live leaf count.

(iii) [T] Decision.  Forcedness on B is decided by interval bisection over the pair's 6-dimensional pose box: a
sub-box is cleared if [g_{σ*}] ⊆ [0, ∞) (σ* holds throughout) or if every other selection has sup [g_σ′] < 0 on it
(any disjoint configuration must then use σ*, by Lemma SAT).  The largest δ that passes (ρ = κδ) is the forced
radius (`a116lib.forced_test`, `radius_search`).  For a non-contact pair the FAR radius is the largest δ at which
some selection has inf [g_σ] ≥ 0 on the whole box.

(iv) [M] The tables (`notes/stability_table.md`, `results/stability.json`; pins in A57's slack cores, s ∈
[3.82, s0 + 0.02]).  Chain contacts (the rows the kill needs), forced radius at ρ = 100δ° / at ρ = 0:

| shadow | contact | type | τ | slack | forced radius (ρ = 100δ°) | forced radius (ρ = 0) |
|---|---|---|---|---|---|---|
| S07 | f0 – BL(0,1) (f0's vertex on the face x = 1) | vertex-on-edge | 0.443 | **0.057** | **0.024** | **0.053** |
| S07 | f2 – TR(0,0) (corner on f2's right edge) | vertex-on-edge | −0.167 | 0.333 | 0.178 | 0.210 |
| S07 | f4 – BR(0,0) (corner on f4's bottom edge) | vertex-on-edge | 0.126 | 0.374 | 0.198 | 0.254 |
| S07 | f0 – f4 (partial flush, overlap 0.96) | flush | | 0.960 | 0.223 | 0.338 |
| S07 | f0 – f2 (full flush) | flush | | 1.000 | 0.232 | 0.353 |
| S07 | f2 – f4 (incidental, overlap 0.04) | flush | | 0.040 | 0.008 | 0.014 |
| S02 | f1 – f3 (f1's corner over f3's corner, overlap 0.085) | flush | | **0.085** | **0.019** | **0.032** |
| S02 | f3 – BR(0,1) (corner (s−1, 2) on f3's edge) | vertex-on-edge | −0.163 | 0.337 | 0.083 | 0.128 |
| S02 | f1 – TL(0,0) (corner (1, s−1) on f1's edge) | vertex-on-edge | −0.163 | 0.337 | 0.179 | 0.227 |
| S02 | f2 – f3 (f2's vertex on f3's top edge) | flush | | 0.915 | 0.215 | 0.324 |
| S02 | f1 – f2 (full flush) | flush | | 1.000 | 0.229 | 0.353 |
| S02 | f1 – BL(0,1) (corner (1,2) on f1's edge) | vertex-on-edge | 0.088 | 0.412 | 0.231 | 0.297 |
| S02 | BR(0,1) – BR(0,0) (column) | flush | | 1.000 | ≥ 0.400 | ≥ 0.400 |

The non-contact pairs of L ∪ P are far to ≥ 0.156 (S02: f2–BR(0,1) 0.156, f2–TL(0,0) 0.209, f1–BR(0,1) 0.190; S07:
f0–BL(1,0) 0.224; every other pair ≥ 0.35), and the first-order estimate matches the rigorous radius to ±0.02 in
every row (the PI's reading of f4 – BR(0,0), "~0.25", is the ρ = 0 entry 0.254).  So:

> **The PI's single-leaf neighbourhood N_PI = min over the chain contacts is 0.024 (S07, limiter f0 – BL(0,1)) and
> 0.019 (S02, limiter f1 – f3) at ρ = 100δ°, 0.053 / 0.032 at ρ = 0; the NEXT limiters are 0.18 (S07) and 0.08 –
> 0.18 (S02).**  Both limiters are mechanism (a) at a short edge slack, and both are the contacts whose OTHER
> selection carries the dipping chain of §4: the single-leaf route stops exactly at the Trump boundary and at its
> mirror.  The fallback — the general tree with that one pair case-split — is §5.

## 4. Where the chain can dip: the Trump boundary, as a single inequality

**S07.**  In the trump5 frame with L = {f0, f2, f4}, the leaf that keeps z*'s selections has value Λ(θ) ≥ 2 + 4√2/3
on every tilt (A110 §2.1) — nothing dips.  The pair f0 – BL(0,1) has, within the boxes, exactly two possible
selections once δ > 0.024: the face selection (owner BL(0,1), axis e_x: f0's vertex on the face x = 1) and the
CORNER selection (owner f0, its lower-left edge normal: BL(0,1)'s corner (1,2) on f0's edge).  On the corner leaf
the support is the gap chain {corner (1,2) on f0's edge, the f0 – f2 row, TR(0,0)'s corner on f2's right edge} and
the value is F_T(θ) = 2 + (2 + sin θ)/(cos θ + sin θ) [T, A110 §2.4], increasing on θ > 24.3°, with F_T(θ) = s0 at

  **θ_0 = 40.181998° = θ_T + 6.1·10⁻⁵ °**  (θ_T = 40.181937° Trump's tilt, F_T(θ_T) = ŝ: Corollary TRUMP-GAP).

So with exact pins the corner leaf is dead iff the tilt cell lies above θ_0: N must be cut by the single inequality
F_T(θ) > s0, i.e. θ > θ_0 — Trump's own tilt, not the grain boundary 41.565° (where F_T = Λ = S02's value: that is
where the FORMULA changes, A110 §3.3; the value stays above s0 for another 1.38°).  With the slack cores the corner
leaf loses up to ≈ 2h(cos θ + sin θ) through the two pin corners and its dip point moves up: measured in §5 (the
uncut runs find the corner leaf LIVE at ρ ≥ 5°, i.e. at 40°, with a witness packing of L ∪ P at side ≤ s0 — Trump's
three squares).  The cut at 41.565° used for the grid is safe by 0.0097 = Λ(41.565°) − s0 and is what the grid
reports; the cut at θ_T + 0.02° is measured separately.  Below θ_0 the dip is real for L ∪ P and unavoidable for
the full packing too: Trump is a packing at ŝ < s0 satisfying trump5's pins, so no N containing Trump's tilt can
ever be dead — the cut is the canary.

**S02 — the mirror.**  In the k5_11 frame with L = {f1, f2, f3, BR(0,1)}, the leaf keeping z*'s selections has
value max(Λ, D) ≥ s* — nothing dips.  The pair f1 – f3 (f1's corner 0.085 over f3's corner) splits at δ > 0.019
into f1-above-f3 (z*'s row, the diagonal chain D and the ladder) and f1-beside-f3 (owner f3's top-left … ) and
the pair f2 – top wall / f2 – f3 release the ladder; the leaf that keeps only the diagonal rows {TL(0,0)'s corner
on f1, f1 – f3 (row role), f3 – BR(0,1)} has value D(θ) = F_T(90° − θ) [T, A110 §2.2], DECREASING in θ, with

  **D(θ) = s0 at θ_0′ = 49.818002° = 90° − θ_T (to 6·10⁻⁵ °).**

This is A111's identity in the tilt: S02's three load-bearing squares are Trump's three tilted squares under the
diagonal reflection with a tilt offset of 1.383° = θ_0′ − θ*.  So for L ∪ P the S02 neighbourhood dips as soon as
ρ ≥ 1.383° and r ≥ 0.0175 (the diagonal image of Trump's three squares IS a packing of L ∪ P at side ŝ < s0 — the
pins of k5_11 are satisfied by the slot squares of that image, which is why the restricted problem cannot see the
difference), and N must be cut from ABOVE by D(θ) > s0, θ < θ_0′.  Unlike S07's, this cut is an artefact of the
restriction: no D4 image of Trump satisfies k5_11's pins with all eleven squares (A111 `trump_lp.canary`), and the
full-packing sweep of A110 §3.4 stays at Λ(θ) ≥ s* above θ* — the squares that block the diagonal image are the
ones DROPPED here (the strut f0 and TR(0,0)).  Including them in L (as boxes) is the route past θ_0′; measured in
§5.  In both shadows the dipping leaf is the SAME object: the minimum's short-slack contact case-split to its
other side, and the chain there is F_T (S07) or its mirror D (S02) — one inequality each.

## 5. [M] The measured radius (T2; `notes/t2_table.md`, `results/t2_*.jsonl`)

Pins in A57's slack cores, side in [3.82, s0 + 0.02], every DEAD verdict followed by 10⁴ samples (0 hits everywhere),
the SLSQP minimum ("measured") and the Trump canary; time cap 900 s per N (one BLAS-pinned process).  "certified"
= the minimum of the relaxed LP over the final cell cover (a rigorous lower bound on the side over N; phase 2 spends
4 000 nodes tightening it); the 10 % criterion is met at the small radii and degrades to "just above s0" at the
large ones, where the tightening budget runs out (the KILL does not depend on it).

**S02, k5_11 frame, L = {f1, f2, f3, BR(0,1)}** (near pairs 10–13 of 36; leaves after the interval census 64–192,
the 8^k = 10⁹ never enumerated; the DFS visits 2 000–70 000 nodes; branch = selection splits, bisect = tilt cells):

| r \ ρ | 2° | 5° | 10° | 20° | 40° |
|---|---|---|---|---|---|
| 0.02 | DEAD 3.885781 / 3.886746, 7 s | DEAD 3.879768, 14 s | DEAD 3.879720, 19 s | DEAD 3.878424, 40 s | CAP (900 s) |
| 0.05 | DEAD 3.879681, 13 s | DEAD 3.877085 / 3.885852, 21 s | DEAD 3.877176, 40 s | DEAD 3.877148, 96 s | CAP |
| 0.10 | DEAD 3.877836, 16 s | DEAD 3.877381, 34 s | DEAD 3.877303 / 3.885618, 105 s | CAP | CAP |
| 0.20 | DEAD 3.877131, 27 s | DEAD 3.877152, 97 s | **DEAD 3.877105 / 3.885618, 445 s** | CAP | CAP |
| 0.30 | ALIVE: witness 3.873295 | CAP | CAP | CAP | CAP |

(entries: certified minimum [/ measured minimum], tree wall time.)  **Largest certified: (r, ρ) = (0.2, 10°)** — ten
times A111's 0.0097 in position and the tilt range [38.4°, 58.4°] — and (0.05, 20°), (0.02, 20°).  What limits it:
(i) at r = 0.3 a genuine rearrangement of L ∪ P: the witness (a checked packing of the nine squares at side
3.873295) has BR(0,1) 0.3 to the LEFT of its slot (x = 3.077, tilt −2°) with f3 sitting on top of it — the box of a
slot square is too large for a slot square, and the dropped squares (f0, TR(0,0)) are what would block it (the
`slot_r0.05` extras below); (ii) at ρ ≥ 20° with r ≥ 0.1 the time cap: the census leaves 768–10⁷ leaves and the tilt
cells must reach ≈ 1° in each of the three tilted squares before the relaxation is tight (the loss is the McCormick
term (q-range)·hw/2 ≈ 2.8 r·hw per row) — 10⁵–2.5·10⁵ nodes in 900 s were not enough; no witness and no dip were
found there, so those cells are open, not dead.  The lowest closed leaf at every certified N is z*'s own selection
(the ladder Λ / diagonal D chain with the BR column and the top wall), never a different chain; and the mirror dip
D(θ) < s0 predicted in §4 for θ > 49.818° does NOT materialise in the k5_11 frame: (0.1, 10°) covers [38.4°, 58.4°]
and is dead — the pure-diagonal leaf is infeasible there because the k5_11 pins BL(1,0) and TL(0,0) and the row
BL(0,1)-corner-on-f1 leave no room for the diagonal image of Trump's squares (the `ceil49.80` extras: (0.1, 10°)
gives the same verdict and value with and without the ceiling).  k5_16 frame (extras): DEAD at (0.05, 5°) 3.885789
and (0.1, 10°) 3.878207, CAP at (0.2, 20°).  Exact pins (h = 0): the same verdicts and values to 10⁻⁴ at (0.05, 5°),
(0.1, 10°) — the slack cores cost nothing here because the chain pushes the pin corners against their walls.

> **Correction (A119, 2026-09-07, `71d18eba`).** Three of the four ρ ≥ 20° cells tabulated as `capped` are ALIVE, not
> open: a checked packing of L ∪ P below s0 exists inside N — S07 (0.2, 20°) at 3.873374 (f0, f2, f4 all at 65°, the
> ladder shears), S07 (0.2, 40°) at 3.869626, S02 (0.2, 40°) at 3.876703. `t2_S07.jsonl` already recorded the first
> witness with `witness_valid: true` under the `capped` verdict; re-running this attempt's own tree with its own
> parameters returns ALIVE in 2–9 s. S02 (0.2, 20°) remains genuinely open (633,660 nodes at the cap). The certified
> radii of §4 are unaffected. Adding the blocking squares as boxes does not widen them (A119 T3).

**S07, trump5 frame, L = {f0, f2, f4}, tilt boxes of f0, f2, f4 cut at 41.565°** (near pairs 10–12; leaves 64–768):

| r \ ρ | 2° | 5° | 10° | 20° | 40° |
|---|---|---|---|---|---|
| 0.02 | DEAD 3.884785 / 3.885618, 4 s | DEAD 3.884765, 9 s | DEAD 3.884768, 11 s | DEAD 3.884765, 11 s | DEAD 3.884770, 14 s |
| 0.05 | DEAD 3.884781, 7 s | DEAD 3.884770, 14 s | DEAD 3.881568, 23 s | DEAD 3.882167, 23 s | DEAD 3.882465, 25 s |
| 0.10 | DEAD 3.884134, 12 s | DEAD 3.879308, 18 s | DEAD 3.878273, 32 s | DEAD 3.878828, 43 s | **DEAD 3.878622 / 3.886746, 52 s** |
| 0.20 | DEAD 3.877522, 15 s | DEAD 3.877410, 33 s | DEAD 3.877380 / 3.885644, 58 s | CAP | CAP |
| 0.30 | CAP, witness 3.856379 | ALIVE: witness 3.858296 | ALIVE 3.875193 | ALIVE 3.869558 | ALIVE 3.820000 |

**Largest certified: (0.1, 40°) — the tilt range [41.565°, 85°] — and (0.2, 10°).**  Limiter at r = 0.3: a
rearrangement of L ∪ P (the ladder shears: f2 slides 0.3 up its flush contact with f0 and f4 0.3 to the right; the
x-chain no longer spans the container; a checked packing of the eight squares at 3.856 — the dropped f1, f3 and
BL(0,2) are what would block it); at (0.2, ≥ 20°) the time cap.  The lowest closed leaf is always the x-chain
(f0–BL(0,1) face, f0–f2, f2–TR(0,0), f0–f4, f4–BR(0,0), Λ).  With f1 added to L (extras `with_f1`): (0.1, 10°) DEAD
3.877136 in 199 s, (0.2, 20°) CAP — a fourth tilted square costs a factor 5 in nodes and buys nothing (Λ ≥ s* needs
no y-chain).  Exact pins: the same values to 10⁻³.

**The Trump boundary, measured** (S07 uncut and cut at θ_T + 0.02° = 40.202°):

| N | uncut | cut at 40.202° | cut at 41.565° |
|---|---|---|---|
| (0.02, 2°) / (0.05, 2°) / (0.1, 2°) | DEAD (tilts ≥ 43°) | – | DEAD |
| (0.02, 5°) | DEAD, measured 3.878731 (F_T at 40°, r too small for the corner leaf) | – | DEAD |
| (0.05, 5°), (0.1, 5°) | **ALIVE: witness side 3.875871 = F_T(40°) at tilt 40.0°, selection f0–BL(0,1) = the CORNER (1,2) on f0's lower-left edge; Trump inside N** | DEAD 3.877086 / measured 3.877218 = F_T(40.202°) | DEAD |
| (0.02, 10°) | DEAD, certified 3.877123, measured 3.877787 (the corner leaf at 39.6°) | – | DEAD |
| (0.05, 10°), (0.1, 10°) | ALIVE: witness 3.865807 = F_T(35°) at 35°; Trump inside | DEAD 3.877093 / 3.877218 | DEAD |
| (0.2, 5°) | – | UNRESOLVED (3 088 cells at the 0.05° floor: the margin 1.3·10⁻⁴ is below the relaxation loss) | DEAD |
| (0.2, 10°), (0.05, 20°), (0.1, 20°) | – | DEAD 3.877086–3.877130 / 3.877218 | DEAD / DEAD / DEAD |
| (0.2, 20°) | – | CAP | CAP |

So the dipping leaf is exactly §4's: the corner selection of f0–BL(0,1) with value F_T(θ), live for θ < θ_T (the
witnesses sit at the cell's lower end, 40° or 35°, with side F_T of that tilt), dead for θ > 40.202° with the
measured minimum F_T(40.202°) = s0 + 1.3·10⁻⁴ — the slack cores did NOT lower it (both pin corners of the gap chain
are pressed against their walls by the chain), and the certified bound 3.877086–3.877130 sits 2–50·10⁻⁶ above s0.
The cut at θ_T + 0.02° is therefore sound and tight for r ≤ 0.2, ρ ≤ 20°, and the grain boundary 41.565° is a
comfortable (Λ(41.565°) − s0 = 0.0097) alternative that costs 1.4° of tilt.

**The r = 0.3 limiter, dissected** (extras `slot_r0.05`, `with_f0_TR`).  Confining the slot square BR(0,1) to a
0.05 box while f1, f2, f3 keep r = 0.3 does NOT restore the kill: the tree finds at once (14 nodes, < 1 s) a checked
packing of the nine squares at side 3.875307 — f1 slides 0.3 right and 0.26 down to sit under TL(0,0), f3 climbs
onto BR(0,1) (f3 at (2.91, 2.71), 48.4°), f2 stays on the top wall — a rearrangement that TR(0,0), dropped from L ∪ P,
would forbid (its cell [s−1, s]² meets f3).  With the strut f0 and TR(0,0) added as boxes (L = f1, f2, f3, f0,
TR(0,0), BR(0,1); slot boxes 0.05), (0.1, 5°) is DEAD with certified 3.877091 / measured 3.886746 in 346 s — 16 near
pairs, 2 048 leaves after the census, 42 527 nodes: the extra tilt dimension costs ×10 in nodes and the kill is
unchanged, (0.1, 10°) hits the 900 s cap, and the r = 0.3 case with the two extra boxes was not run (time); the
consumer count for that six-box N drops to 1 of 184 (the supports do not hold f0 and TR(0,0) at the shadow's
poses), so the extra boxes are a device for the certificate, not for the node cut.  So the position radius of the L ∪ P
certificate is 0.2 < r < 0.3 for BOTH shadows, set by the first rearrangement of the |L| + |P| squares alone, and
the way past it is the blocking squares as boxes — a larger tree, not a different leaf.

**The PI's single-leaf N** (extras `PI_N_single_leaf`, δ = the chain contacts' minimum forced radius at ρ = 100δ°):
S07 (0.024, 2.4°): DEAD, certified 3.884789 / measured 3.885618, 287 tree nodes, 62 s (7 selection branches — the two
flush disjunctions f0–f2, f0–f4 and the column pins, as Lemma STAB (ii) says); S02 (0.019, 1.9°): DEAD, 3.885780 /
3.886746, 103 s.  Both are within 10 % of s* and both are ≈ 10 × smaller than the general tree's radius: the
single-leaf route stops at the short-slack contact, the tree case-splits it and keeps going.

## 6. [M] Canaries

* S02 at r = 10⁻⁶, ρ = 10⁻⁴ °, exact pins, anchored at s*, side free: the tree's value is **3.886745** (= s* −
  10⁻⁶ from the box), measured 3.886746; S07 the same: **3.885617** / 3.885618 (`extras`, canary rows).  PASS.
* Trump is OUTSIDE every certified S07 N (`trump_in_N`: no D4 image of Trump satisfies trump5's pin cores AND the
  three boxes with the cut) — and INSIDE the uncut N from (0.05, 5°) on, exactly where the tree turns ALIVE with
  witnesses at side F_T(θ) < s0.  Trump is outside every S02 N (no D4 image of Trump satisfies k5_11's pins).  PASS.
* 10⁴ samples in every certified N: 0 packings of L ∪ P at side ≤ s0 (the free-pair rejects overlap by up to 0.7;
  the accepted samples fail the pin/wall/side test at every one of 30 sides).  PASS.
* The exact-LP witness of every ALIVE verdict is re-checked as a packing (worst pair gap ≥ −10⁻⁷, worst wall gap
  ≥ −10⁻⁷) before it counts.  PASS (176 / 192 / 16 valid witnesses per ALIVE run, the first one settles the run).

## 7. [M] The consumer and the price (T3; `results/t3_consumer.json`)

**(a) The node cut.**  The YES leaf of A112's region tree at a stalled node of class C with the shadow's L: hypothesis
= C's pins + one box F_ℓ per ℓ ∈ L (+ the tilt cut); the certificate = this attempt's leaf list (per closed leaf:
its cell, its selection, its Farkas multipliers on the relaxed rows; per near pair the IMPOSSIBLE selections by
interval) — `results/t2_*.jsonl` `certified_min_leaf` shows one; the Lean shape is §8.  The NO side is A111/A112's.

**(b) Counts** — A107's alive nodes whose LP support (the 11-square representative at s0, canonicalised into the
shadow frame) has a distinct square inside every box of a certified N:

| N | nodes of the class | inside N |
|---|---|---|
| S02 / k5_11 (0.02, 2°) … (0.2, 2°) | 184 | 19 – 29 |
| S02 / k5_11 (0.05, 5°) / (0.1, 5°) / (0.2, 5°) | 184 | 32 / 40 / 42 |
| S02 / k5_11 (0.05, 10°) / (0.1, 10°) / **(0.2, 10°)** | 184 | 53 / 65 / **72** |
| S02 / k5_11 (0.05, 20°) | 184 | 59 |
| S02 / k5_16 (0.05, 5°) / (0.1, 10°) | 68 | 18 / 23 |
| S07 / trump5, every certified N up to (0.1, 10°) | 18 | 0 |
| S07 / trump5 (0.1, 20°) / (0.1, 40°) | 18 | 1 / 2 |

The distance census says what radius would be needed: S02/k5_11 supports within (r, ρ) of the anchor: 32 / 65 / 100
/ 124 of 184 at (0.05, 5°) / (0.1, 10°) / (0.2, 20°) / (0.3, 40°); k5_16: 18 / 23 / 28 / 42 of 68; S07/trump5: 3 / 6
/ 10 / 16 of 18 (but the S07 supports sit at 21°–44° or 58°–69°, A110 §5: below the cut or far in tilt, so the
certified N catch 0–2).  So at the largest certified S02 N, **72 + 23 = 95 of the 252 A57 S02-explained nodes have
their whole load-path support inside a certified neighbourhood and their YES leaf is dead by this certificate**;
the remaining ones need (0.2, 20°)–(0.3, 40°), which is the time-cap frontier of §5.  A57's 14 deep S02 nodes (L3/L4)
are among the 184/68 and are counted where they fall.

**(c) Price.**  One certified N costs 4–445 s (S02) / 4–58 s (S07) of one process INCLUDING the 10⁴-sample and SLSQP
checks (the tree alone 4–105 s at (r, ρ) ≤ (0.1, 10°); 445 s at (0.2, 10°)); one N serves every node whose support
lies in it.  Against it: A57 ≈ 290–336 s per CHILD at level 2 (A96) and A60 ≈ 1 100 s per cover leaf at δ = 10⁻²
(A110 §5), per NODE, on the NO side as well; the YES side of a load-path branch is otherwise a Farkas leaf valid
only for r < 0.0097 (A111).  Per node the certificate is free (it is shared); the price that remains is the NO side.

**If the radius is to grow past (0.2, 10°) / (0.1, 40°):** (iii) is solved (second-order relaxation; the McCormick
term is the only first-order remnant and it is split-able); (ii) is solved (anchor at s0, pins cost nothing); what
limits now is NEW: the restriction to L ∪ P — at r = 0.3 the |L| + |P| squares rearrange into a packing at side <
s0 that the dropped squares would forbid — and the tilt-cell count at ρ ≥ 20° with r ≥ 0.1 (10⁵–10⁶ cells at 1°).
The first is removed by adding the blocking squares to L (S02: f0 and TR(0,0), or simply a smaller box for the slot
square BR(0,1) — `slot_r0.05` extras; S07: f1, f3), at the cost of more tilt dimensions; the second by a C
implementation of the census + LP (the Python node costs 5–7 ms; the counts are 10⁴–10⁶) or by an adaptive cell
width (the margin grows away from θ*, the cells could).

## 8. Lean shape

* **COVER** is a finite case split: per near pair, `sat_squares` (CaseSat.lean, the four-axis overlap ⇒
  intersection) in contrapositive form gives one of the four axes with non-overlapping projections, and `le_total`
  on the centre projection gives the sign — eight cases, `rcases`; IMPOSSIBLE cases are closed by the interval
  enclosure (a polynomial inequality in cos θ, sin θ at the box corners, `nlinarith` with sin² + cos² = 1, the shape
  of A111's O1).  The tilt-cell cover is a bisection tree (a `Finset` of intervals covering the product).
* **LEAF** per (cell, leaf): the relaxed rows of Lemma RELAX are each a two-line consequence of the true row and
  the elementary bounds (cos φ ≤ 1, |sin φ| ≤ sin hw, the chord of a concave function, McCormick), and the kill is
  `linarith` with the Farkas multipliers on the relaxed rows (the multipliers are exported per closed leaf,
  `results/*.jsonl` `certified_min_leaf.support`; the float dual bound is re-derived there — the rational form is
  A111's O4).
* **The node cut** (T3 (a)): the YES leaf of A112's region tree is `loadpath_yes_dead` of `A111/notes/
  leaf_shape.md` with hypotheses = class pins (`PinBox`) + one box per ℓ ∈ L (`F ℓ`, distinct witnesses) + the tilt
  cut, and conclusion `False` at every side s ∈ W; it is a `ClassKilledAt`-shaped clause on a sub-hypothesis
  consumed like SLOT-CROWD's row (Composition.lean's `ClassKilledAt`, `classKilledAt_of_kill`); the NO side is
  unchanged (A111/A112: NO-families at the node LP, fixed-side certificates).  Nothing in `lean/` is edited here.
* Selection.lean's teleport/CC-2 is not involved: the certificate never moves a square; it only enumerates the
  separating axes of the pairs of L ∪ P.

## 9. Obligations ledger

| # | item | status |
|---|---|---|
| A116-O1 | Lemma SAT (interior-disjoint ⟺ some signed selection), Lemma COVER, Lemma LEAF (LP duality = chain), Theorem LOCAL (iff, n-general, DROP) | [T] §1–3 |
| A116-O2 | Lemma RELAX: second-order affine relaxation over a tilt cell with tilt variables; McCormick term and q-range splits | [T] §3.1, [M] tightness §5 |
| A116-O3 | Lemma STAB: forced selection, mechanisms (a)/(b), flush disjunction, interval decision; the stability tables | [T] §3.2, [M] tables |
| A116-O4 | the Trump boundary as F_T(θ) > s0 (θ > θ_T + 6·10⁻⁵°); S02's mirror D(θ) > s0 (θ < 90° − θ_T); what the dropped squares cost | [T] §4, [M] §5 |
| A116-O5 | the measured grid, sampling confirmation, canaries | [M] §5–6 |
| A116-O6 | consumer counts and price | [M] §7 |
| A116-G1 | rational Farkas certificates per leaf (A111 O4) and the Lean file | [C] |
| A116-G2 | the S02 neighbourhood beyond 49.8° with f0 and TR(0,0) as boxes | [C]/[M] §5 |
