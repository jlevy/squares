# rectfront: R_n = {(w, h) : n unit squares fit in w x h}, small n  (2026-10-20)

Code: `frontier.py` (fq rectangle mode, container [0, h + dx] x [0, h], min h; random / tilt-alphabet / band starts
+ kicks).  Runs: `runs/rectfront/f1` (n = 2..8, dx step 0.05, 40 + 40 quenches), `runs/rectfront/f3fine` (n = 3, 4,
dx 0.6..2.2 step 0.02, 150 + 150).  Lean: `lean/Sqpack/Rect.lean`.  Labels: [proved] Lean; [measured] float.

## Results

* **R_2** [proved, `rect2`]: two unit squares need max(w, h) >= 2.  Proof: with w, h < 2 every unit square
  contains the rectangle's centre in its interior (`centre_mem_sqInt`; `|dx|, |dy| < 1 - k`, `k = (|C|+|S|)/2`,
  and `2k(1 - k) <= 1/2`).
* **R_3 has a tilted piece** [measured; known: it is the piece x + 2y = 4 + 2√2 of Friedman's Math Magic, June 2010 (erich-friedman.github.io/mathmagic/0610.html; boundary of S_2, no individual attribution; the problem's solvers were Maurizio Morandi, Evert Stenlund, David W. Cantrell and Hiroaki Hosono), which we missed until 10-21]: two uprights in the bottom corners, a 45 deg square in the gap touching
  their inner top corners and the top wall: `h = 2 + sqrt2 - w/2`, below the grid for `2 sqrt2 < w < 3`
  (e.g. 2.942809 x 1.942809, = (2 + 2sqrt2/3) x (1 + 2sqrt2/3)).  Every sub-grid optimum the search found matches
  this formula to 1e-12; nothing else beat the grid.  Conjecture (w >= h): `h_3(w) = 2` on [2, 2sqrt2],
  `2 + sqrt2 - w/2` on [2sqrt2, 3), `1` from 3.
* **R_4** [measured]: two uprights at opposite corners and a tilted pair (39.3-43 deg, angle varying along the
  frontier, not 45) between them: below the grid for w in about (3.72, 4), e.g. 3.912287 x 1.912287 at 39.95 deg.
* **R_5** [measured]: the s(5) packing stretches: four corner uprights + a central 45 deg square touching the four
  inner corners: `w + h = 4 + sqrt2` for w in [2 + 1/sqrt2, 3) (h from 2.707 down to 2.414); at w = 3 the grid
  (h = 2) takes over.
* n = 6, 7, 8 [measured]: tilted pieces at h < 2 (strip-of-height-<2 family, x.91-ish) and n = 7 = R_5 piece + a
  column of two (w = 3.7071 at h = 2.7071, w + h = 6 + sqrt2 - ...); not yet read closely.

## Caveat
The search misses known optima often (n = 3: found h = 2 at dx = 0.84, 0.86, 0.92, 0.94 where the 45 deg family
gives less; n = 8 long thin cells worse than the trivial row).  Below-grid hits are real (checked feasible by fq);
"no hit" means little.  A continuation along the frontier (seed dx + 0.02 from dx's best) would fix most of it.

## Literature (scan `literature/rectangles-small-n-2026-10-20.md`)
No paper proves R_n for n >= 2.  The boundaries (constructions) for n <= 10 are in Friedman's Math Magic, June 2010
(boundary of S_{n-1}; R_3's, with the 45 deg piece, is S_2's); the scan missed this (corrected 10-21).  Yang (arXiv
2608.13595, G_3) settles R_3 by rescaling except 1.5 <= w < 2, max(w, 3 - w/2) <= h < 3 (w short); the scan's "natural
conjecture" (that region infeasible) is refuted by Friedman's 45 deg piece, which lies inside it.  R_4: Stenlund 2010 (Friedman's Squares in Dominoes) has 4 in 1.930 x 3.861, the
same shape as our tilted-pair family.  No rectangle result in any proof assistant.

## R_3 lower bound: method and status (10-20/21)

Claim: three unit squares in [0,w] x [0,h], w < 2, h < 3 force 2w + h >= 4 + 2sqrt2.  With rect2 and the
constructions (rect3_wedge, grid, column) this gives R_3 exactly (w <= h): fits iff w >= 1 and (h >= 3 or w >= 2 or
2w + h >= 4 + 2sqrt2).

* Certificate (`r3bb.py`): SAT for squares makes each configuration one of 512 separation types (per pair, an edge
  normal of one square).  For weights lambda >= 0 on the pairs, with net pair forces G_K on the squares
  (sum G_K = 0), LP duality for the centres gives  sum lambda S <= sum_K |G_Kx|(w/2 - k_K) + |G_Ky|(h/2 - k_K).
  The right side is linear increasing in (w, h), so checking it fails at the two upper corners V1 = (2, 2sqrt2),
  V2 = ((1 + 2sqrt2)/2, 3) of the excluded region excludes the open region (margin >= 0 suffices).
* Tilt map (`tiltlp.py`, `tiltmap.py`, 5 deg grid, w0 = 1.95, 1.99): no tilt triple beats the boundary; the only
  exact tie is the wedge (two upright, one at 45).  But margin 0 holds on whole lines: two tilts = 0, third free
  (two upright squares side by side, tight at V1, w = 2).  So the tilt-space search has a tube around three lines.
* On the line, wedge types: weights (cos t, sin t) cancel the middle square's vertical force and give exactly
  w + ((p^2 - 1)/2) h >= p + p^2, p = cos t + sin t; at V1, V2 the margins p + p^2(1 - sqrt2) - 2 + sqrt2 and
  p - p^2/2 + 1 - sqrt2 are concave in p with zeros only at p = 1, sqrt2 (exact).
* Global search `runs/rectfront/r3bb2` (symmetry-reduced: labels sorted, mirror): 86,416 boxes certified, 423 tube
  boxes set aside, **no failure outside the tube**.  Float64 with an explicit 1e-9 margin over padded trig
  enclosures (exact-arithmetic replay still to do).
* Tube (`r3local.py`, `iad.py`): tilt-dependent weights (support and zero force components of the LP optimum at a
  probe; secondary weights proportional to the distance from the line), directed-rounding interval AD along rays
  from the line, sector/rho/beta subdivision.  Works on the side-by-side and wedge types tested; too slow on the
  raw tube boxes, so first `r3line1`: refine the tube, keeping only boxes that touch a zero line.

## 2026-10-21: chain reduction for R_3 (replaces the tube/origin interval search)

Tube run r3tube6 stopped at 42/423 (0 failures) in favour of this.  Scripts: `chain/`.

Setup: strip of height H < 2, length L; three unit squares sorted by centre x (a, b, c).
1. Wall clearance: x_a >= k_a, x_c <= L - k_c, k = (|cos| + |sin|)/2 (Lean: `half_extent`).
2. Pair separation: disjoint interiors give a separating edge normal u; u_x <= 0 would force |dy| >= 1,
   impossible since |dy| <= H - 1 < 1.  So dx >= (h_A(u) + h_B(u) - u_y dy)/u_x.
3. The resulting bound on L is linear in the centre heights, so b sits on the floor or ceiling
   (vertical mirror: floor).  The sides then decouple: L >= P(beta) + P(-beta), where P(beta) is the
   least x_b with b on the floor and some square to its left.
4. Numerically (lemP3.py) the neighbour can be taken upright, giving the closed form
   P(t) = min(1+k, U, V'),  P(-t) = min(1+k, V, U')  (t in [0,45], c=cos t, s=sin t, k=(c+s)/2):
     U  = 1/2 + (k+1/2 - s(k-1/2))/c        V  = 1/2 + (k+1/2 - s(H-1/2-k))/c
     U' = 1/2 + (k+1/2 - c(k-1/2))/s        V' = 1/2 + (k+1/2 - c(H-1/2-k))/s
   Closed form matches brute force over all neighbour tilts to 1.6e-15.
5. Target L >= 2 m(H), m = min(3/2, 2+sqrt2-H).  Splits into 9 term pairs, each linear in H on
   either side of the kink H = 1/2+sqrt2, so only H in {max(1,c+s), 1/2+sqrt2, 2} need checking
   (combos.py): all >= 0, zeros only at t=0 (all upright) and t=45 with pair (V', V) (the wedge).

Grid evidence only so far.  To prove: (i) the upright neighbour is worst (step 4); (ii) the 1-variable trig
inequalities in step 5; (iii) step 2 needs the separating-axis direction (disjoint => separating normal), or
in Lean its contrapositive with an explicit common interior point.

### 2026-10-21 (later): steps (i) and (ii) proved on paper

(i) Upright neighbour is worst — for every direction phi (cos phi > 0), not only edge normals:
  replace a (tilt alpha, height y_a) by an upright square at y' = y_a - sgn(sin phi)(k_alpha - 1/2), which stays in
  the strip.  The bound k + (h_a(phi) + h_b(phi) - sin phi (y_b - y))/cos phi does not increase iff
      k_alpha (c + |s|) + h_alpha(phi) >= c + |s|          (c = cos phi, s = sin phi).
  WLOG s >= 0 (reflect).  With d = alpha - phi this is 2cos d + |sin d| + sin(alpha+phi) >= 2(c+s).  On alpha in
  [0, phi] and in [phi, 90] the left side is one sinusoid in alpha, positive at both ends of an interval shorter
  than 180 deg, hence concave there, so its minimum is at an endpoint: alpha = 0 or 90 gives equality, alpha = phi
  gives 2 + sin 2phi = 1 + p^2 >= 2p (p = c + s).  Then for the upright square the support-line bound in any
  direction is >= the octagon boundary rho, so the term is >= P(beta) closed form.  (famA.py: grid check.)
(ii) The 9 pairs x 3 H-checkpoints become rational functions of u = tan(t/2) on (0, sqrt2 - 1] (ii.py prints all 27
  numerators/denominators).  Signs are elementary: zeros at u = 0 (all upright) and a double root at
  u = sqrt2 - 1 for (V', V) (the wedge): at H = 2 the numerator is (u - (sqrt2-1))^2, at the kink it is
  (u-(sqrt2-1))^2 ((1+2sqrt2)u^2 - 2(1+sqrt2)u - 1) over 4u(u^2-1).

Remaining for a complete proof: (iii) the separating-axis step for two squares, plus a clean write-up.

## 2026-10-21: R_3 exactly, in Lean (`lean/Sqpack/Rect3.lean`)

**Attribution.** The boundary, including the 45° wedge piece x + 2y = 4 + 2√2, is already in Friedman, Math Magic, June 2010 (erich-friedman.github.io/mathmagic/0610.html) (boundary of S_2; constructions only; no individual credit for this piece).  Our 10-20 literature scan missed it (corrected there); we did not find the wedge first.  What is new here, as far as we know, is the proof of the lower bound.  wand125/square-packing `problems/rectangles/` lists the same edge (k = 3) with certified constructions and no lower bounds.

`rect3_iff`: three unit squares (any angles) fit in [0,w] × [0,h] iff 1 ≤ w, 1 ≤ h and
(2 ≤ w ∧ 2 ≤ h) ∨ 3 ≤ w ∨ 3 ≤ h ∨ (h < 2 ∧ w + 2h ≥ 4 + 2√2) ∨ (w < 2 ∧ h + 2w ≥ 4 + 2√2).
Standard axioms only; 706 lines; compiles in ~16 s.  No interval search, LP, or separating-axis enumeration.

Proof (`rect3_lower`: strip height H < 2 gives L ≥ 3 or L + 2H ≥ 4 + 2√2):
1. Sort the squares by centre x: a, b, c (`rect3_lower`, 6 orderings).
2. `separate`: Mathlib's `geometric_hahn_banach_open_open` on the open squares, extended to the closed squares
   along segments to the centre (`lim_le`); `support_le/ge` turn it into u·c ± (|u·e| + |u·e⊥|)/2 vs s.
   `u1_pos`: the normal points right, since the vertical centre offset is < H − 1 < 1.
3. Shelves (`left_shelf`, `right_shelf`): the upright square [0,1] × [lo, lo+1], lo = y_a − k_a or y_a + k_a − 1 by
   the sign of u₂, lies on a's side of the line (`upright_repl`:
   2(u₁+|u₂|) ≤ (|C|+|S|)(u₁+|u₂|) + |u₁C+u₂S| + |u₂C−u₁S|, polynomial after symmetry reduction to C, S, u₂ ≥ 0).
   Hence every point of b at heights in [lo, lo+1] has x ≥ 1 (mirror: x ≤ L − 1).
4. `middle`: in a frame (P, Q ≥ 0) of b, the witness on each side is the side vertex if the shelf band contains
   its height, else the point on the adjacent edge at the band's bottom (edge above) or top (edge below).
   This gives 3 × 3 real inequalities (`case_*`), seven closed by nlinarith; the two wedge cases (`case_UU`, `case_DD`)
   go through `wedge_core`: CS(A+B) ≥ C³ + S³ − G, and p − 2√2 q ≥ G(1 − 2q) for G < 1 (p = C+S, q = CS).
5. Constructions: row, L, wedge (`rect3_wedge` from Rect.lean), and `RectPacks.swap`.

The step "neighbour may be taken upright" (found numerically on 10-21) is what makes this short: after it, b
alone against two upright shelves carries the whole boundary.  Equality cases: all upright (L = 3) and the wedge.

### 2026-10-21 (later): golf; reusable chain tools

`Rect3.lean` 707 → 171 lines; the general steps now live in `lean/Sqpack/RectChain.lean` (369 lines) for n ≥ 4.
* Everything after `framed` works in a frame `(P, Q)`, `P, Q ≥ 0` (a quarter turn of `(cos θ, sin θ)`), so the
  sign reductions of `upright_repl` collapse to one vertical mirror (`u₂ < 0` swaps `P` and `Q`).
* `right_shelf` is `left_shelf` of the mirror image `x ↦ L − x` (`mir`); the right witness is the left
  `witness` with `(P, Q)` swapped (`witnesses`); `Wit` names the three alternatives.
* The nine case lemmas are one `chain_bound`.  Seven cases give `L ≥ 3` outright (so `√2` is not needed
  there); only UU and DD (b hanging from the ceiling / standing on the floor between both shelves) give the wedge bound.
* Build: ~15 s wall, ~20 s CPU (was ~15 s wall, ~100 s CPU); standard axioms.

## 2026-10-21: R_4 plan — the chain relaxation is exact, and reduces to one square

Scripts `search/rectfront/r4/`; outputs `runs/rectfront/r4*.txt`.

* **Target** (`frontier4.py`).  For H < 2: 4 squares fit iff L >= 4 or L >= F(H) = min_t L(t, H),
  `L(t, H) = 2 + (1 - 2(H - k - 1)S)/C + (1 - (H - 2k)C)/S`, C = cos t, S = sin t, k = (C + S)/2
  (point-symmetric: uprights in opposite corners, b on the ceiling and c on the floor at tilt t; contacts
  a-corner/b-edge, b-c edge to edge, c-edge/d-corner).  Agrees to 1e-15 with Friedman's piece 3.2 of S_3
  (mostly Morandi), as listed in closed form by wand125 `problems/rectangles/data/edges/k04.json` (fetched a6c0dbb).
  Range 1.8816489 <= H < 2, from L = 4 down to 4√2 − 2 at H = 2 (t = 45°).
* **Relaxation is exact** (`relax.py`, `sweep.py`): sort a, b, c, d by centre x; keep only the left shelf on b,
  the right shelf on c (bands chosen adversarially) and b, c disjoint.  Its minimum equals min(4, F(H)) to
  1e-15 at 32 heights in [1.2, 2), minimiser = Friedman's configuration.  `tilts.py`: minimum over heights at
  fixed (tb, tc) is >= F, zero only at tb = tc = t* (parallel middle squares).
* **One-square reduction.**  Let the b-c separating line have slope m = u₂/u₁ (u₁ > 0).  Its two support
  bounds split into a b-term and a c-term; rotating the c half by 180° about the rectangle's centre turns c
  into another square with a left shelf.  Hence
      L >= σ_b(m) + σ_c'(m) − mH >= G(m) := 2φ(m) − mH,
  σ_X(m) = max_{p∈X} (p_x + m p_y), φ(m) = min of σ over one square right of a left shelf in the strip.
  G(−m) = G(m) (vertical flip), and min_m G = the relaxation, exactly.
* **φ in closed form** (`phi.py`, `lemma1.py`, 104 grid points, all tight to 1e-14): for m = −cot t <= 0,
      φ(m) = min(2 + mH/2, Φ(t, H)),  Φ = 1 + (1/2 − (H − k − 1)S)/C + (1 − 2(H − k)C)/(2S),
  and 2Φ − mH = L(t, H).  The minimising square has its edge parallel to the separating line, which is why
  the frontier's tilt is the separating direction.
* **Lean statement this suggests**: three unit squares' tools plus four squares in [0,L] × [0,H], H < 2 ⇒
  4 <= L ∨ L(C, S, H) <= L for the unit direction (C, S) of the b-c separating line (so ∃ (C, S)).
  Work: (1) the one-square lemma (witness cases V/U/D for b against its shelf, a polynomial inequality in
  b's frame, (C, S), y, lo, H); (2) the 180° rotation and vertical flip; (3) Friedman's construction for the
  converse (valid t range to check).

## 2026-10-21: R_4 exactly, in Lean (`lean/Sqpack/Rect4.lean`, `Rect4Core.lean`)

`rect4_iff`: four unit squares fit in [0,w] × [0,h] iff 1 ≤ w, 1 ≤ h and (both ≥ 2, or one ≥ 4, or for the short
side s < 2: `Fried4 ℓ s`, i.e. some unit (C, S), C, S > 0, with S C ℓ ≥ 2C(S − C) + 2(1 + C + S − s) + C² s, which is
ℓ ≥ L(t, s)).  Standard axioms; 592 lines (472 + 120); ~15 s.  Boundary credit: Friedman, Math Magic June 2010
(piece of S₃, mostly Morandi), closed form also in wand125 k04.json.  New here: the proof.

* Lower bound `rect4_lower` exactly as planned above: sort, left shelf on b, right shelf on c, `separate_lr` for
  b, c (unit direction (C, S); vertical mirror when u₂ > 0), `one_square` on b and on the half-turned c, `combine4`.
* `one_square` (support T of a square with a left shelf in direction (S, −C)): T ≥ 2S − C(H − 1) or
  C T ≥ C(S − C) + 1 + C + S − H.  Cases: V → `upright_repl`; U → upright bound (σ ≤ 0: `upright_repl` + 2C(1 − Q);
  σ > 0: worst at H → 2, residual (1 − Q)(CQ + S(1 − P))); D → P T ≥ P(S − C) + Pσ⁺ + γ(1 + P + Q − H), then
  D1 (σ ≥ 0: weights CQ/(SP), 1 − CQ/(SP) on the two branches; H drops out) or D2 (σ ≤ 0: worst at H = 2).
  D1, D2 factor in half angles (u, v): −4uv(u − v)R₁ and 2(1 − u)(u − v)(1 − v)R₂, R concave in u
  (chord identities).  Certificates: `search/rectfront/r4/certs.py` (exact multipliers of the circle relations).
* `rect4_friedman`: the configuration at any (C, S) with L(t, H) < 4 is a packing (grid check `construct.py`,
  then proved: H ≥ 3/2 > C + S, x_b ≥ k, x_c − k ≥ 1 via `core_g` = 2v(1 − v)(2v⁴ + v³ + v² − v + 1)/(1+v²)³ ≥ 0;
  pairs split by b's edge line, the common b–c edge line, and x = 1 / x = L − 1).

## 2026-10-21: R_5 — plan (strip part numerically settled; s(5) part open)

Target (Friedman's S_4 pieces, closed forms in wand125 k05.json, fetched a6c0dbb), short side a, long side b:
4.1 a < 1.8713: b = 5; 4.2 1.8713 ≤ a < 2: 4a + b = 4 + 6√2; 4.3/4.4 2 ≤ a ≤ 1 + √2: b = 3;
4.5 1 + √2 ≤ a ≤ 2 + 1/√2: a + b = 4 + √2 (its corner a = b is s(5) = 2 + 1/√2, Göbel 1979).

**Strip part (a < 2)**, scripts `search/rectfront/r5/`, outputs `runs/rectfront/r5*.txt`:
* Piece 4.2's packing: uprights in both bottom corners, b and d at 45° on the ceiling against their corners,
  c at 45° on the floor between them (edge to edge with b and d).  Mirror-symmetric, angle fixed.
* `relax5.py`: chain relaxation (left shelf on b, right shelf on d, b|c and c|d disjoint; no b–d needed) equals
  min(5, 4 + 6√2 − 4H) to 3e-15 at 10 heights; minimiser = the zigzag above H ≈ 1.8713, the row below.
* `split5.py`: L ≥ B_b(line 1) + W_c(line 1, line 2) + B_d(line 2), B from the Lean one-square lemma in its four
  orientations, W = min over c of max(x + m₂y) − min(x + m₁y): still exact (grid), tight only at t₁ = t₂ = 45°,
  opposite slopes.
* Decoupling: full (`halves5.py`) and partial (c's tilt or height per half, `partial5.py`) LOSE up to 0.1, so c's
  pose must be shared.  Lines first is lossless: L ≥ X(c) + X(mirror c), X = min over the line of
  B(t) − m y + h_c(m)/2; but X's minimising line is not always along c's edges (`xpos5.py`: c at 10° on the
  floor, H = 1.95, best line 42.9°).
* `cands5.py`: for fixed lines, c's width (height at its worst end) is homogeneous linear in (cos θ, sin θ) on
  each piece between kinks, positive, hence concave: min at c aligned with line 1, with line 2, or upright.
  Matches the θ grid to 1e-14.  Candidates "aligned" are tight at the zigzag; "upright" has slack ≥ 0.005.
  Lean form of the reduction: on an arc between unit vectors e₁, e₂ (< 90° apart), (P, Q) = λe₁ + μe₂ with
  λ, μ ≥ 0, λ + μ ≥ 1, so a linear form nonnegative at both ends is ≥ its smaller end value.
* What remains for the strip: the final two-angle (+ H) inequalities B₁(t₁) + W_cand(t₁, t₂) + B₂(t₂) ≥ target,
  over 3 candidates × 4 slope signs × 2 × 2 one-square branches.  Only (aligned, signs (−, +), Ψ/Ψ) is tight
  (a line of equality t₁ = t₂ = 45°, H ∈ [1.8713, 2)); the rest have slack, except near the vertical-line corner
  (C → 0) where the row bound 5 is approached.

**Part a ≥ 2**: the chain breaks (squares can stack), and it contains s(5).  Not started; read how s(5) has been
proved before designing anything.

## 2026-10-21 (paused): see `LESSONS.md`
Techniques, what worked (chain, one-square lemma), what failed (tube search, decouplings, certificate pipeline cost), R₅ status and Plan B.

## 2026-10-21 (resumed): R₅ constructions and the four-point piece, in Lean

* `lean/Sqpack/Rect5Pack.lean`: `rect5_upper` — every construction on R₅'s boundary (row, 2×3 grid, zigzag
  piece 4.2 for √2 ≤ H ≤ 2, stretched s(5) piece 4.5 for w, h ≥ 2), both orientations.  All tilts are 45°, so
  each square gives four linear bounds (`int_lin`) and one tactic (`pairs5`) splits every pair by `linarith`.
* `lean/Sqpack/Rect5Pts.lean`: `rect5_pts_lower` — 2 ≤ a, b < 2√2 and a + b < 4 + √2 ⇒ ¬ RectPacks 5 a b
  (piece 4.5 exactly for 4 − √2 ≤ a ≤ 2 + 1/√2, with `rect5_stretch`; includes s(5) ≥ 2 + 1/√2).  Four points
  (1,1), (a−1,1), (1,b−1), (a−1,b−1) (`rect5_cover`, 9 cells), then scaling + `packing_le_weight`.  Core lemmas
  are real inequalities on `In dx dy c s` (corner, DS7 side strip, new centre-rectangle lemma X + Y ≤ √2);
  reflections only swap c, s.  Paper proofs and numerics: `r5pts/R5PTS.md`.  339 lines, ~10 s.
* Left for R₅, short side ≥ 2: by monotonicity in a, the b = 3 piece reduces to a = 1 + √2, b → 3; plus the
  slanted line for 1 + √2 ≤ a < 4 − √2.  No 4-point set works there (`R5PTS.md` §6: best escape ≈ 0.015);
  the escapers of the rectangular set are long-wall sitters (centre within ~0.085 of the wall, height within
  ~0.1 of b/2, any tilt).

## 2026-10-21 (later): R₅ with both sides ≥ 2, exactly, in Lean (`lean/Sqpack/Rect5Line.lean`)

`rect5_wide_iff`: for a, b ≥ 2, five unit squares fit iff a ≥ 3, b ≥ 3 or a + b ≥ 4 + √2 (Friedman's pieces
4.3–4.5 of S₄; includes s(5) = 2 + 1/√2).  Standard axioms; 533 lines, ~12 s.
* Reduction: widen to a, b ≥ 1 + √2 (monotone), scale onto the line a + b = 4 + √2 (`no_pack_of_cover`).
* On the line, a ≥ 4 − √2: the four points (`rect5_cover`).  1 + √2 ≤ a ≤ 4 − √2: **cover C**, ten points with
  weights 2/3 ((0.91, 1) and mirrors) and 1/3 ((1, 1) and mirrors, (1, b/2), (a − 1, b/2)), total 14/3.  Every
  closed square contains a block of weight 1 (`quadC`, three cells: row `In_corner`/`In_row`; wall band
  `In_side2`; centre `In_far` + `In_mp`), the mirrors give the other quadrants (`coverC`).
* Indexed weighted pigeonhole `packing_le_idx` (points may repeat).
* History: the 4-point set cannot reach a ≈ 2.4 (R5PTS §6); an escaper second stage needs all five squares (§7);
  an LP found fractional point covers (§8); the 2/3–1/3 block cover C (§9); paper proofs (§10).
Open for R₅: only the strip part (short side < 2, `Final5`, LESSONS.md §5).  (Closed later the same day, below.)

## 2026-10-21 (evening): R₅ done in Lean, `rect5_iff` (`lean/Sqpack/Rect5Thm.lean`)

`rect5_iff : RectPacks 5 w h ↔ Fits5 w h` (`Fits5` in `Rect5Iff.lean`: row; both sides ≥ 2 with a side ≥ 3 or
w + h ≥ 4 + √2; strip h < 2 with w + 4h ≥ 4 + 6√2, or swapped).  Standard axioms.
* Strip, H < 2√2 − 1: `rect5_low`, midline points (i, H/2), i = 1..4 (`Rect5Low.lean`).
* Strip, 2√2 − 1 ≤ H < 2: `final5_high : Final5Hi` (`Rect5Final.lean` + generated `Rect5Hi*.lean`, ~14k
  lines, ~16 min to build one file at a time).  64 case theorems, 160 leaves: 144 Handelman certificates at the
  H endpoints, 16 tight zigzag leaves by (1 + u)ᵐ G = R + kQ, 2 corner leaves by hand.  Generator
  `r5strip/hi5.py`; details `r5strip/FINAL5.md`.  The lower bound H ≥ 2√2 − 1 is what let the old 10-21
  pipeline (stalled at 120/160) close.
* Style is machine-generated; a structured strip proof is a later task.
