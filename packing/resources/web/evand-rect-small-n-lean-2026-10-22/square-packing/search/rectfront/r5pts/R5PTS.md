# R₅, short side ≥ 2: the 4-point unavoidable set (numerics + paper proofs), 2026-10-21

Scripts here; outputs `runs/rectfront/r5pts/`.  Labels: [measured] float optimiser / sampling; [proved on paper]
argument below, each step also checked on 4·10⁵ random samples (`checkproofs.py`, 0 failures).

Notation: a unit square with centre m and angle θ; for a point P, d = P − m, u = d·(c, s), v = d·(−s, c)
(c = cos θ, s = sin θ; same as `coord` in `Basic.lean`).  P ∈ closed square ⟺ |u|, |v| ≤ ½.  The square is
unchanged by θ ↦ θ + 90°, so take c, s ≥ 0 (a frame, as in `RectChain.framed`); k = (c + s)/2, p = c + s ∈ [1, √2].
"Outside" a corner/point below means outside the *closed* square: |u| > ½ or |v| > ½.

## 1. Centre-rectangle lemma [measured; proved on paper]

**Statement (closed).**  X, Y ≥ 0, X ≤ 1, Y ≤ 1, X + Y ≤ √2.  If m ∈ [x₁, x₁+X] × [y₁, y₁+Y], the closed unit
square (any θ) contains one of the four corners.  (Strict version: X, Y < 1, X + Y < √2 ⇒ a corner in the open
interior; same proof.)

[measured] `crect.py`: G(X, Y) := max over m, θ of min over corners of max(|u|, |v|) equals
max(max(X, Y)/2, (X + Y)/(2√2)) (11 X values, on / ±0.01 off the boundary, Nelder–Mead from the 20 best grid points);
worst pose = rectangle centre, at 45° on X + Y = √2 and upright on max = 1.  So the conditions are exactly sharp.

**Proof.**  Write m's offsets to the corners: d₁ = (A, B), d₂ = (−A′, B), d₃ = (−A′, −B′), d₄ = (A, −B′) with
A, A′, B, B′ ≥ 0, A + A′ = X, B + B′ = Y (corners NE, NW, SW, SE, cyclic; adjacent corners differ by (X, 0) or (0, Y)).
WLOG c ≥ s ≥ 0 (else reflect x ↦ −x, which maps the rectangle to a rectangle and (c, s) to the frame (s, c)).
Suppose every corner is outside.
1. *Witnesses.*  Because A, B, … ≥ 0 and c ≥ s ≥ 0, each corner has only two possible witnesses:
   d₁: u > ½ or v > ½ (−u₁ ≤ 0, −v₁ = As − Bc ≤ u₁);  d₂: v > ½ or −u > ½ (−v₂ ≤ 0, u₂ ≤ v₂);
   d₃: −u > ½ or −v > ½ (u₃ ≤ 0, v₃ ≤ −u₃);  d₄: u > ½ or −v > ½ (v₄ ≤ 0, −u₄ ≤ −v₄).
   Index the witnesses u, v, −u, −v as 0, 1, 2, 3: corner j's witness is j−1 ("first") or j ("second") mod 4.
2. *Adjacent corners cannot have opposite witnesses*: e.g. u₁ > ½, −u₂ > ½ ⇒ u₁ − u₂ = Xc > 1, but X ≤ 1;
   likewise v₂ − v₃ = Yc, u₄ − u₃ = Xc, v₁ − v₄ = Yc, all ≤ 1.
3. If the choices are not all equal, somewhere cyclically corner j takes "first" (j−1) and corner j+1 "second"
   (j+1): opposite, excluded by 2.  So all first or all second.
4. *All first* (u₁, v₂, −u₃, −v₄ > ½): (u₁ − u₃) + (v₂ − v₄) = (Xc + Ys) + (Xs + Yc) = (X + Y)(c + s) > 2, but
   X + Y ≤ √2 and c + s ≤ √2.  *All second* (v₁, −u₂, −v₃, u₄ > ½): (v₁ − v₃) + (u₄ − u₂) = (Yc − Xs) + (Xc − Ys) =
   (X + Y)(c − s) > 2, but ≤ √2.  Contradiction.  ∎

So 16 sign cases, each one `linarith` (14 by step 2, 2 by step 4).  This is DS7's quadrant idea (Lemma 3) made
discrete; it replaces the triangle lemma (X² + Y² ≤ 1) by the sharp X + Y ≤ √2.

## 2. Side-strip lemma [measured; proved on paper]

**Statement (closed; DS7 Lemma 2 orientation).**  Wall y = 0, the square in y ≥ 0 (so m₂ ≥ k, `half_extent`).
Points P = (0, y₀), Q = (x₀, y₀).  Hypotheses: 0 ≤ x₀ ≤ 1, y₀ ≤ 1, x₀ + 2y₀ ≤ 2√2.  If 0 ≤ m₁ ≤ x₀ and m₂ ≤ y₀,
the closed square contains P or Q.  (Our use: y₀ = 1, x₀ = gap = b − 2 on a long wall, a − 2 on a short wall;
so the condition is gap ≤ 2√2 − 2.)  Only the wall the strip lies on is used.

**Proof.**  WLOG c ≥ s ≥ 0 (else reflect x ↦ x₀ − x: swaps P and Q).  d_Q = (A, B), d_P = (−A′, B) with
A = x₀ − m₁, A′ = m₁, B = y₀ − m₂ ≥ 0, A + A′ = x₀.  Witnesses as in §1: Q: u or v; P: v or −u.
* Q with v: v_Q = Bc − As ≤ Bc ≤ (y₀ − p/2)c ≤ (1 − p/2) ≤ ½ (p ≥ 1).  Impossible (the wall).
* Q: u, P: −u: u_Q − u_P = x₀c > 1, impossible (x₀ ≤ 1).
* Q: u, P: v: s·u_Q + c·v_P = cs·x₀ + B > p/2 (weights s, c kill A), and B ≤ y₀ − p/2, so
  g(p) := x₀(p² − 1)/2 + y₀ − p > 0 (cs = (p² − 1)/2).  But g is convex in p with g(1) = y₀ − 1 ≤ 0 and
  g(√2) = x₀/2 + y₀ − √2 ≤ 0; exactly: g(p) = [(√2 − p)g(1) + (p − 1)g(√2)]/(√2 − 1) + (x₀/2)(p − 1)(p − √2) ≤ 0.  ∎

Sharp at θ = 45° (DS7).  Note it does need the closed form: at θ = 0, y₀ = 1 the upright square on the wall has
P, Q on its edge (g(1) = 0), so **no open-interior version exists with y₀ = 1** — that is why Göbel pulls the points
in by ε and DS7 scales.  [measured: `checkproofs.py` conclusion + every case inequality, 0 failures.]

## 3. Corner lemma [proved on paper]
Walls x = 0, y = 0, point (1, 1), centre m ∈ [k, 1]² (k from `half_extent`).  A = 1 − m₁, B = 1 − m₂ ∈ [0, 1 − k]:
|u| = Ac + Bs ≤ (1 − k)(c + s) = p − p²/2 ≤ ½ ((p − 1)² ≥ 0), |v| = |Bc − As| ≤ max(Bc, As) ≤ 1 − k ≤ ½.  No WLOG
needed.  (Closed twin of `mem_sqInt_of_close`.)

## 4. Assembly and strictness (recommendation)

**Cover lemma (closed).**  2 ≤ a ≤ 2√2, 2 ≤ b ≤ 2√2, a + b ≤ 4 + √2: every closed unit square in `rbox a b` contains
one of (1, 1), (a − 1, 1), (1, b − 1), (a − 1, b − 1).  Split m₁ at 1 and a − 1, m₂ at 1 and b − 1 (needs a, b ≥ 2):
4 corner cells (§3, + mirrors), 4 side cells (§2 with y₀ = 1, x₀ = a − 2 or b − 2 ≤ 2√2 − 2 < 1), centre cell
(§1, X = a − 2, Y = b − 2: X, Y ≤ 2√2 − 2 < 1, X + Y ≤ √2).  Cells overlap on their edges; harmless (closed).

**Lower bound.**  a, b ≥ 2, a, b < 2√2, a + b < 4 + √2 ⇒ ¬ RectPacks 5 a b.  Take λ > 1 with λa, λb, λ(a + b)
still within the cover lemma's region; the scaled packing has λ-squares in `rbox (λa) (λb)`; apply
`packing_le_weight` (Basic.lean: closed unit squares concentric with side-λ squares, weights 1 on the 4 points)
⇒ 5 ≤ 4.  Needs one small scaling lemma (`coord (λc) θ (λp) = λ • coord c θ p`, so `sq (λc) θ λ = λ • sq c θ 1`).
Recommended over (i) pulled-in points (ε bookkeeping in every lemma) and (ii) strict hypotheses (impossible, §2).
The theorem covers R₅'s piece a + b = 4 + √2 for 4 − √2 ≤ a ≤ 2 + 1/√2 (there b < 4 + √2 − a ≤ 2√2), including
s(5) ≥ 2 + 1/√2, and also the region a ∈ [2, 4 − √2), b < 2√2 (below the true boundary b = 3 there).

## 5. Coverage of the rectangular set [measured] (`cover.py`, `cover_dense.py`, `escape.py`)
Escape = max over squares in the container of min over points (gauge − ½); ≤ 0 ⟺ unavoidable (closed).
* 208 containers (16 × 8 grid + 80 random) in 4 − √2 ≤ a ≤ b ≤ 4 + √2 − a: max escape 2.2·10⁻¹⁶ (0 = upright
  squares touching a point).
* Just beyond the line (+10⁻³, +10⁻²) for a ≥ 4 − √2: escape = Δ/(2√2) (45° square at the centre), as §1 predicts.
* For a < 4 − √2 on or near the line: escape > 0 (45° square on the long wall, centre (k, b/2)), up to 0.05 at
  a = 2.45; matches §2's condition b ≤ 2√2.

## 6. The corner a = 1 + √2, b → 3 [measured] (`escapers.py`, `ptopt.py`, `ptopt2.py`)
* **Escapers of the rectangular set (p = q = 1)** at b = 2.95, 2.99, 2.999: only in the two long-wall side cells,
  hugging the wall: centre within ≈ 0.06–0.085 of its wall position k (x ≤ k + 0.085), height within ≈ 0.1 of b/2,
  **any tilt** in (0°, 90°) at b → 3 (b = 2.95: 7°–83°; b = 2.999: 0.35°–89.65°), largest escape at 45°
  (0.043, 0.057, 0.060).  So not "near 45°" only: as b → 3 the near-upright wall sitter (touching (1, 1) and
  (1, b − 1) with its edge) also escapes.  No escapers in the corner, short-side or centre cells.
* **Best 4-point sets** (multistart Nelder–Mead on a pose sample, then 8 rounds of cutting planes with the full
  escape optimiser; families: rectangular (p, q), mirror-symmetric, left/right-mirror, point-symmetric, free 8-dim):
  | (a, b) | rect | mirror | psym | free |
  |---|---|---|---|---|
  | (2.4142, 2.99) | +0.0157 (p 0.957, q 1.016) | +0.0161 | +0.0159 | +0.0160 |
  | (2.40, 2.99) | +0.0142 | +0.0145 | +0.0144 | +0.0154 |
  All families converge to ≈ the rectangular set with p ≈ 0.95 (squeezed between the side strip and the centre
  cell), escape ≈ 0.015 > 0.  Local search only, but every start and family lands at the same value: **no 4-point
  unavoidable set near the corner** (consistent with the literature note's crude search).  Pigeonhole on 4 points
  does not reach the b = 3 piece at a ≈ 2.4; a second stage on the long-wall sitters is the natural next step.

## 7. Second stage: escaper + holders relaxation [measured] (`stage2.py`, 96 SLSQP starts per case)
Relaxation: E avoids all four points; S_j contains P_j for j in a set J; all disjoint, in the box; maximise the
common slack t (t ≥ 0 feasible).  E starts on the left wall (mirror).  "E" prefix = a second escaper on the right.
| (a, b) | J = 0123 | any 3 of 4 | two escapers + 2 | two escapers + 3 |
|---|---|---|---|---|
| (1+√2, 2.90) | −0.0246 | — | — | — |
| (1+√2, 2.95) | — | feasible (all 4 choices) | feasible (all 6) | −0.007 to −0.0125 |
| (1+√2, 2.99) | −0.0025 | — | — | — |
| (2.5, 2.89) (line at 2.914) | −0.0140 | feasible (all 4) | — | −0.0035, −0.025 |
* So the relaxation is infeasible below the boundary and t ≈ (b − 3)/4 at the corner, apparently sharp; its
  near-optimum is the grid-like stack (E upright mid-left wall, 2 + 2 + 1 rows) at the corner, and the stretched
  s(5) layout on the line.  **Every proper sub-relaxation is feasible**: the second stage needs all five squares
  (E with S₀ and S₂ alone fit: S₀, S₂ slide right; S₁, S₃ are what push them back).

## 8. Weighted point covers reach the corner and the line [measured] (`mixlp.py`, `ptcover.py`, `structlp.py`, `cand*.py`)

**Answer: yes, with points only (weights < 1), total < 5, all the way to the boundary.**  Segment densities were
offered to the LP (`mixlp.py`, pitch 0.1, plus the lines y = 1, b − 1, x = 1, a − 1) and always got weight 0.
The parent's "points alone fail" argument assumed weight-1 points; fractional weights get around it: a square
typically catches 2/3 + 1/3 or three 1/3's, and the wall sitters catch row points at x ≈ 0.6–0.9 on *both* rows.

Checker (`ptcover.min_capture`): for each angle on a grid (1800–7200 angles over 90°), the minimum of
Σ w_p [p ∈ closed square] over centres is attained in an open cell of the arrangement of the tilted unit squares
around the points (plus the centre box); every arrangement vertex is probed in 16 directions at offset 1e−7.
Much sharper than grid + Nelder–Mead on a step function (which missed a 0.667 hole in an LP solution at b = 2.95).
Still sampled in the angle and float only: **not a proof**, and every cover below is tight (min capture exactly 1
on most angles: closed covers at the boundary have no slack).

**Two parameterised covers** (12 points, D2-symmetric; rows y = 1 and y = b − 1; total 4 + 4γ):

| | row x (and a − x) | weights | interior points (and mirrors) | γ | total | valid on the line (sampled) |
|---|---|---|---|---|---|---|
| A | 0.84, 1 | 2/3, 1/3 | (1, 1.25), (1, b − 1.25), (a−1, ·) | 1/6 | 14/3 | a ∈ [1+√2, ≈2.502] (13 points; fails 2.511) |
| B | 0.78, 1 | 0.4, 0.6 | (1, 1.45), (1, b − 1.45), (a−1, ·) | 0.1 | 4.4 | a ∈ [2.48, 4−√2] (10 points; fails 2.45) |

"Line" = R₅'s boundary: b = 3 at a = 1+√2, b = 4 + √2 − a after.  `runs/rectfront/r5pts/cand3_dense.txt`.
* A at a = 1+√2: valid for b = 2.9, 2.95, 2.99, 2.999, 3.0 (7200 angles at 3.0, 2.99); fails at b = 3.05 (0.333).
  Valid **at b = 3 itself** although the 2×3 grid fits there: shared edges let closed squares share points, as
  for the 4-point set at a + b = 4 + √2.  So the scaling argument of §4 works unchanged: a packing strictly below
  the line, scaled up to the line, gives 5 ≤ 14/3 (or 4.4).
* An earlier hand cover with 1/3 at x ∈ {0.6, 0.9, 1} and 1/6 at (0.9, 1.2) (`cand.py`) also works at a = 1+√2,
  b ∈ [2.9, 3] (14/3), but not on the line beyond.
* LP optima on the line (`structlp.py`, fine row atoms, interior columns; `runs/rectfront/r5pts/structlp_line.txt`):
  14/3 at the corner, 4.4 at a = 2.45, 2.5, 2.55, and 4 (the 4-point set) at a = 4 − √2.
* Control (2.6, 2.80): LP = 4.000 (the 4-point set), as expected.
* Earlier LP numbers from `ptcover.run` (4.217 at (2.414, 2.95), …) came from an orbit-key bug (fixed: it tied
  unrelated atoms); the covers were still checked on their actual weights, but they weren't optimal.

**What this means for the proof.**  The corner and the slanted line need no second stage: two weighted 12-point
covers, parameterised by (a, b) only through the mirror positions a − x, b − y, cover the whole remaining
boundary (piece A to a ≈ 2.50, piece B from 2.48), and the 4-point set takes over at a ≥ 4 − √2.  The Lean cost
is a weighted cover lemma (each closed square catches weight ≥ 1) per piece: more cases than §4, since captures
are sums of fractional weights, and the covers are tight on whole families of poses, so each case needs exact
equality structure (as in §1–§3).  Next numerics if pursued: list the tight pose families (which weight
combinations reach exactly 1) to plan the case split, and look for one family with x, y, γ linear in a.

## 9. A simple cover for the whole remaining line: 10 points, weights 2/3 and 1/3 [measured] (`c10.py`, `scanA.py`, `tightC.py`, `minsetsC.py`, `blocksC.py`)

**Cover C** (total 14/3), for a + b = 4 + √2 (b = 3 at the corner a = 1 + √2), with c₀ = 9/10:

| point | weight | count |
|---|---|---|
| (c₀, 1), (a − c₀, 1), (c₀, b − 1), (a − c₀, b − 1) | 2/3 | 4 |
| (1, 1), (a − 1, 1), (1, b − 1), (a − 1, b − 1) — our 4-point set | 1/3 | 4 |
| (1, b/2), (a − 1, b/2) — on the midline | 1/3 | 2 |

Each corner's row pair weighs 1 (the 4-point set with its weight split 2/3 + 1/3 and moved 0.1 toward the wall);
the spare 2/3 sits on the midline, where the long-wall sitters are.
* Valid (closed) for c₀ ∈ [≈ 0.879, √2 − ½ ≈ 0.9142] at 1800 angles; the upper end is the 45° wall sitter at the
  corner (it catches row points only for x ≤ √2 − ½), the lower end a tilted square near (1.27, 2.14) at a = 4 − √2.
* c₀ = 9/10: min capture exactly 1 at 61 points of the line a ∈ [1 + √2, 2 + 1/√2] with 36,000 angles, for
  a ≤ ≈ 2.624; fails (2/3) from a ≈ 2.629 (`runs/rectfront/r5pts/c10_dense36k.txt`).  So it covers the whole of
  [1 + √2, 4 − √2] with margin; the 4-point set (`rect5_pts_lower`) takes over beyond.  One cover, no split.
* Found by scanning the §8 family: the interior points can sit on the column x = 1 and merge on the midline.

**Blocks** (`blocksC.py`): every closed unit square on the line contains a full **block** of weight exactly 1:
* corner pairs {(c₀, 1), (1, 1)} (×4 by the mirrors);
* wall blocks {(c₀, 1), (1, b/2)} and {(c₀, b − 1), (1, b/2)} (×2 sides);
* centre blocks {(1, 1), (1, b/2), (a − 1, b/2)} (×4: either row point, either side… i.e. one row-(1) point + both
  midline points).
Checked on all 4.6·10⁸ arrangement-vertex probes (41 points of the line, 3600 angles): no probe without a block.
So the proof is "every square contains a block; blocks weigh 1; total 14/3 < 5" — the weights are bookkeeping.

**Tight families** (`tightC.py`, capture exactly 1; centre folded to the lower-left quadrant):
| centre cell | caught set (exactly) | angles |
|---|---|---|
| y < 1 (any x ≤ a/2) | corner pair r + s | all |
| x < c₀, 1 < y ≤ b/2 (wall band) | r + s; m + r; m + r^ (wall sitters) | all |
| c₀ < x < 1, 1 < y | r + s | all |
| 1 < x ≤ a/2, 1 < y ≤ b/2 (centre) | m + m′ + s (and the top-row twin) | 29°–61° |
(r = (c₀, 1), s = (1, 1), m = (1, b/2); ′ mirror in x, ^ mirror in y.)  Inclusion-minimal caught sets per cell
(`minsetsC.py`) all contain a block, and give the case split below.

**Proof plan** (one quadrant; mirrors as in `Rect5Pts.lean`; centre m = (x, y), k = (c + s)/2):
1. *Row cells*, k ≤ y ≤ 1, k ≤ x ≤ a/2 ⇒ the square contains r and s.
   * x ≤ 1: both by `In_corner` (offsets |·| ≤ 1 − k).  **In Lean.**
   * 1 ≤ x ≤ a/2: s by `In_corner`; r needs a new one-line lemma: offsets dx ∈ [−δ, 0], dy ∈ [0, 1 − k] ⇒ In,
     since |u| ≤ max(δc, (1−k)s) and |v| ≤ δs + (1 − k)c ≤ ½ for δ ≤ δ* ≈ 0.39411 (max at θ = 0 below δ*).
     Here δ = a/2 − c₀ ≤ 2 − 1/√2 − 9/10 ≈ 0.39289: **margin only 0.0012** (c₀ = 0.91 gives 0.011; the cover is
     valid up to c₀ ≈ 0.914).  Consider c₀ = 0.91 or another value in [0.899, 0.914] for slack here.
2. *Wall band*, k ≤ x ≤ 1, 1 ≤ y ≤ b/2 ⇒ {r, s} or {r, m} or {r^, m}.  New lemma (side-strip type: the square
   always catches a c₀-row point, plus s or m).
3. *Centre*, 1 ≤ x ≤ a/2, 1 ≤ y ≤ b/2 ⇒ {r, s} or {s, m, m′} or {s^, m, m′}.  New lemma (centre-rectangle type;
   tight at 29°–61° with three points).  `In_rect` alone gives only one corner of [1, a − 1] × [1, b/2].
Then `packing_le_weight` with the 10 weighted points and the scaling of §4, on the line.  Reduction to the line:
a packing with a ≤ 1 + √2, b < 3 also fits at a = 1 + √2 (monotone); scaling by (4 + √2)/(a + b) lands on the line
at a′ ∈ [1 + √2, 2 + 1/√2]; for a′ ≥ 4 − √2 the 4-point cover applies (b′ ≤ 2√2).

**Exact checking.**  `search/zeromargin.py` and `verify2` (`zmcheck`) both handle *weighted* closed covers exactly,
but only for square containers [0, m]² with rational data.  Two obstacles: the container is a rectangle (the
admissible-pose bounds; a small change in a copy), and every point of the line a + b = 4 + √2 (and the corner
(1 + √2, 3)) is irrational, so exact checks need Q(√2) arithmetic, not Fractions.  Not adapted.

**Web view.**  Like the s(12) ≥ 35/9 page: the box with the 10 points (two weights), a draggable/rotatable square
that highlights the block it contains, and the capture map (min over angles per centre).  The block picture
(corner pairs, wall blocks, centre blocks) is the explanation.
* c₀ = 0.91 also passes: blocks on all 4.65·10⁸ probes, min capture 1 at 41 points of [1 + √2, 4 − √2] with
  36,000 angles (`runs/rectfront/r5pts/c10_091_36k.txt`; `C0=0.91 python3 blocksC.py`).  Recommended for the
  row-lemma margin (δ* − δ = 0.011 instead of 0.0012).

## 10. Paper proofs for cover C, c₀ = 91/100 [proved on paper; every step checked on 2·10⁶ samples, 0 failures] (`wz_*.py`, `checkproofs2.py`)

Setting: the line a + b = 4 + √2, 1 + √2 ≤ a ≤ 4 − √2 (so 2√2 ≤ b ≤ 3).  Centre (x, y) in the lower-left quadrant
[k, a/2] × [k, b/2] (mirrors x ↦ a − x, y ↦ b − y map the point set and the blocks to themselves).  Frame (c, s),
c, s ≥ 0, p = c + s ∈ [1, √2], k = p/2 ≤ √2/2.  `In dx dy c s` as in `Rect5Pts.lean`.  Points r = (c₀, 1),
s = (1, 1), m = (1, b/2), r^ = (c₀, b − 1), s^ = (1, b − 1), m′ = (a − 1, b/2).

**Restructured statement** (replaces the W / Z split of §9 by three cells; the numerics of W, Z as stated hold too,
worst 0 = tight, `wz_check.py`, `wz_refine.py`, but Z's natural proof needs the wall blocks):
| cell | block | proof |
|---|---|---|
| 1: y ≤ 2 − k (any x ∈ [k, a/2]) | r, s | s: `In_corner`.  r: `In_corner` if x ≤ 1; **row lemma** if x ≥ 1 |
| 2: y ≥ 2 − k, x ≤ 11/10 | m, and r or r^ | m: `In_corner`; r ∨ r^: **`In_side2`** (frame swapped) |
| 3: y ≥ 2 − k, x ≥ 11/10 | m, m′, and s or s^ | m: `In_corner`; m′: **m′ bound**; s ∨ s^: **`In_far`** (frame swapped) |
Margins (worst sampled gauge − ½): cell 2's r ∨ r^ −0.0004 (tight only at b = 3, `In_side2`'s g(√2) = −0.004);
cell 3's m ∧ m′ −0.027; s ∨ s^ tight at 45° on the line (equality case of `In_far`).  Split point 11/10: r ∨ r^
fails from x ≈ 1.13, m ∧ m′ fails below x ≈ 1.07 (`wz_split.py`).

`In_corner` hypotheses used (all from k ≤ √2/2, a ≤ 4 − √2, b ≤ 3, c₀ = 0.91):
|1 − x| ≤ a/2 − 1 ≤ 1 − √2/2 ≤ 1 − k;  |c₀ − x| ≤ 1 − k for k ≤ x ≤ 1;  |1 − y| ≤ 1 − k in cell 1;
|b/2 − y| ≤ b/2 − 2 + k ≤ 1 − k in cells 2–3 (b ≤ 6 − 4k ⇐ b ≤ 3 < 6 − 2√2);  x − 1 ≤ 1/10 ≤ 1 − k in cell 2.

**Row lemma.**  |dx| ≤ 39/100, |dy| ≤ 1 − k ⇒ In dx dy c s.  (Used with dx = c₀ − x, |dx| ≤ a/2 − c₀ ≤ 0.3829.)
|u| ≤ |dx|c + |dy|s, |v| ≤ |dx|s + |dy|c, so it suffices that F(c, s) := δc + (1 − (c+s)/2)s ≤ ½ (and F(s, c), the
same statement with the frame swapped).  ½ − F = (1 − s)²/2 + c(s/2 − δ).  If s ≥ 2δ done.  Else
(1 − s)³ ≥ (1 + s)(2δ − s)², exactly (δ = 39/100): (1 − s)³ − (1 + s)(39/50 − s)² = (s − ½)²(39/25 − 2s) + 29s/2500 + 1/625;
times (1 − s), with c² = (1 − s)(1 + s): (c(2δ − s))² ≤ ((1 − s)²)², so c(2δ − s) ≤ (1 − s)².  Tight at θ = 90°
(F = ½ there for every δ); δ* ≈ 0.39411.  **Lean: compiles** (scratch test, `nlinarith` with the hint
`mul_nonneg (sq_nonneg (s - 1/2)) (39/25 - 2s ≥ 0)`, then `abs_le_of_sq_le_sq'`).

**`In_side2`** (DS7 Lemma 2, general point distance y₀, centre allowed slightly past the point row).  Side
orientation as `In_side`: offsets (A, B) and (−A′, B), X = A + A′.  Hypotheses: c, s ≥ 0, c² + s² = 1; A, A′ ≥ 0;
X ≤ 1; y₀ ≤ 1; X/2 + y₀ ≤ √2; B ≤ y₀ − (c + s)/2; −(√2 − 1)/2 ≤ B.  Conclusion In A B ∨ In (−A′) B.
(y₀ = 1, B ≥ 0 recovers `In_side`.)  WLOG s ≤ c (reflection A ↔ A′, `In_negx`).
* B ≥ 0 (as `In_side_le`): Q's witness is u_Q = Ac + Bs > ½ (v_Q > ½ impossible: Bc ≤ B ≤ y₀ − ½ ≤ ½;
  −v_Q > ½ ⇒ u_Q ≥ As − Bc > ½); P: u_P > ½ impossible (Bs ≤ ½), −u_P > ½ ⇒ Xc > 1 ✗, −v_P > ½ impossible (≥ 0);
  v_P > ½: s·u_Q + c·v_P = csX + B > p/2 (c > 0), B ≤ y₀ − p/2 ⇒ g(p) = X(p² − 1)/2 + y₀ − p > 0; but
  X(p² − 1)/2 ≤ X(√2 + 1)(p − 1)/2 and L(p) := X(√2 + 1)(p − 1)/2 + y₀ − p is linear with L(1) = y₀ − 1 ≤ 0,
  L(√2) = X/2 + y₀ − √2 ≤ 0, i.e. (√2 − 1)L(p) = (√2 − p)L(1) + (p − 1)L(√2) ≤ 0.  ✗
* B = −β < 0: Q: u_Q = Ac − βs, v_Q = −As − βc ≤ 0; P: u_P = −A′c − βs ≤ 0, v_P = A′s − βc.
  Impossible singles: u_Q < −½ (βs ≤ ½), u_P > ½, v_Q > ½, v_P < −½ (βc ≤ ½).  Pairs:
  (u_Q > ½, −u_P > ½): Xc > 1 ✗;  (u_Q, v_P > ½): s·u_Q + c·v_P = csX − β > p/2, but csX = X(p² − 1)/2 ≤ (p² − 1)/2
  ≤ p/2 ✗;  (−v_Q > ½, −u_P > ½): c·(As + βc) + s·(A′c + βs) = csX + β > p/2, but (p² − 1)/2 + β ≤ p/2 because
  p − p² + 1 ≥ √2 + 1 − √2p ≥ √2 − 1 ≥ 2β (from (p − 1)(p − √2) ≤ 0) ✗;  (−v_Q, v_P > ½): sX > 1 ✗.
Use in cell 2 (frame (s, c), `In_swap`): along-wall offsets A = b − 1 − y, A′ = y − 1 (y ≥ 2 − k ≥ 1), X = b − 2,
y₀ = c₀, B = c₀ − x ∈ [c₀ − 11/10, c₀ − k] = [−0.19, ·]; X/2 + c₀ ≤ √2 ⇔ b ≤ 2√2 + 0.18 ✓.

**`In_far`** (centre on the far side of the point row, no wall).  Offsets (A, −β), (−A′, −β); hypotheses A, A′ ≥ 0,
X = A + A′ ∈ [√2 − 1, 1], β ≥ 0, X + 2β ≤ √2 (so β ≤ ½).  Conclusion In A (−β) ∨ In (−A′) (−β).  WLOG s ≤ c.
Same four pairs as `In_side2`'s B < 0 case; only (−v_Q, −u_P) changes: csX + β > p/2, but
csX + β ≤ X(p² − 1)/2 + (√2 − X)/2 and X(p² − 2) + √2 − p = (√2 − p)(1 − X(√2 + p)) ≤ 0 (X(√2 + p) ≥ (√2 − 1)(√2 + 1)
= 1).  **Equality** at p = √2 (45°) with X + 2β = √2: the centre-of-box 45° square on the line; all steps are ≤.
Use in cell 3 (frame (s, c)): A = b − 1 − y, A′ = y − 1, X = b − 2 ∈ [2√2 − 2, 1], β = x − 1 ∈ [1/10, a/2 − 1];
X + 2β ≤ b − 2 + a − 2 = √2 ✓.

**m′ bound** (cell 3).  μ = a − 1 − x ∈ [0, a − 21/10] ⊂ [0, ½], ν = b/2 − y ∈ [0, b/2 − 2 + k] ⊂ [0, ½]:
|v| ≤ max(μs, νc) ≤ ½; u = μc + νs ≤ (a − 2.1)c + (b/2 − 2 + p/2)s, and with ½ = (c² + s²)/2,
½ − that = H(β′) := c(c − s)/2 − (a − 2.1)c + (2 − β′)s, β′ = b/2, a − 2.1 = 1.9 + √2 − 2β′: linear in β′ ∈ [√2, 3/2],
so ≥ min of the endpoints E₁ = c(c − s)/2 − (1.9 − √2)c + (2 − √2)s (min 0.014 at θ = 0) and
E₂ = c(c − s)/2 − (√2 − 1.1)c + s/2.  **Lean: both compile** (`nlinarith` with `mul_nonneg hc hs`,
`sq_nonneg (c - 1)`, `sq_nonneg (s - 1/4)`, `mul_nonneg hs (1 - c ≥ 0)`; resp. `sq_nonneg (c - 1/3)`), given
√2 bounds 1.4142 < √2 < 1.4143.

Checks (`checkproofs2.py`, 2·10⁶ samples each, 0 violations): `In_side2` conclusion on its full hypothesis set, its
key and majorant inequalities, its B < 0 bound; `In_far` conclusion, its key bound and factor form; row lemma
(δ = 0.39) and its polynomial; E₁, E₂; and the three cells on the line (1.75·10⁶ / 1.8·10⁵ / 6.3·10⁴ samples).

## 11. Point covers for the strip part (short side H < 2) [measured] (`strip_lp.py`, `strip_cand.py`, `strip_dual.py`, `strip_flex*.py`)

Box [0, L] × [0, H] on the curve L_b(H) = 5 (H ≤ h₀ = (6√2 − 1)/4 ≈ 1.8713), 4 + 6√2 − 4H (h₀ ≤ H < 2); closed squares.
(Note: `ptcover.min_capture_angle` now returns ∞ for an empty centre box, e.g. H = 1 exactly.)

**H ≤ 2√2 − 1 ≈ 1.8284: a 4-point cover, and it is already provable.**  Points (1, H/2), (2, H/2), (3, H/2), (4, H/2),
weight 1, total 4 (in a 5 × H box).  min capture = 1 at H ∈ {1.02, 1.1, …, 1.82, 1.828, 2√2 − 1} (3600 angles,
`runs/rectfront/r5pts/strip_mid4_3600.txt`); fails (0) at H = 1.83: a ≈ 42° square at (1.485, 1.124) slips between two
midline points.  The threshold is exactly DS7's side-strip condition with gap X = 1 and point distance y₀ = H/2 from the
floor: X/2 + y₀ ≤ √2 ⇔ H ≤ 2√2 − 1.  Proof (fold y ≤ H/2 by the vertical mirror, x by the horizontal one):
* centre x ∈ [k, 1]: `In_corner` with (1, H/2) (|1 − x| ≤ 1 − k, 0 ≤ H/2 − y ≤ H/2 − k ≤ 1 − k);
* x ∈ [i, i + 1], i = 1, 2 (3 by mirror): `In_side2` with A = i + 1 − x, A′ = x − i, X = 1, y₀ = H/2, B = H/2 − y ≥ 0
  (no frame swap); hypotheses X ≤ 1, y₀ ≤ 1, X/2 + y₀ ≤ √2, B ≤ y₀ − k.
Both lemmas are in `Rect5Pts.lean` / `Rect5Line.lean`.  Scaling: a packing at (L, H) with L < 5, H < 2√2 − 1 also fits
at (L′, H) for L′ ∈ (max(L, 5H/(2√2 − 1)), 5); scale by 5/L′ > 1 onto (5, H′), H′ < 2√2 − 1, where the cover gives 5 ≤ 4.

**2√2 − 1 < H < h₀ (flat piece): covers exist but get expensive.**  LP optima (sampled poses, restricted atoms; converged
to min capture 1 at 900 angles): H = 1.84: 4.75, 1.85: 4.833, 1.86: 4.8, 1.865: 4.8, **1.87: 5.0**
(`runs/rectfront/r5pts/strip_lp_scan2.txt`).  Weights 1/16 … 3/8 on points near the midline and the row y = H − 1, at
x ≈ 1, 1.1–1.8, 2, 2.3 (plus mirrors): no clean structure; the cost rises to 5 at or just below h₀.

**h₀ ≤ H < 2 (zigzag piece): no cover below 5 found.**  LP = 5.000 at H = 1.8713, 1.9, 1.95, 1.99
(`strip_lp_scan.txt`), and still 5.000 at H = 1.9 with atoms added on the zigzag's contact lines (x + y = 2 through
the a–b contact (1, 1), and the b–c edge line through its midline point x* = 2 + 2√2 − 1.5H, `CONTACT=1`).
Not a proof of impossibility: the LP duals tried (`strip_dual.py`) are fractional packings only relative to the
atom set (true depth 1.5, so they certify only ≥ 3.33), and a column-generation run (`strip_dual.py cg`) ran out of
memory (min_capture with hundreds of weighted atoms) and was stopped.  Rigidity of the zigzag (`strip_flex2.py`):
re-optimised perturbed zigzags return to the zigzag (one success at ε = 0.05; SLSQP on the non-smooth SAT gap is
unreliable), so no continuum of boundary packings was seen.
* Upshot: points settle H ≤ 2√2 − 1 cheaply (the L ≥ 5 part below 1.8284); the strip from 2√2 − 1 to 2 (the end of
  the flat piece and all of the zigzag piece) needs the chain argument (`Final5`, LESSONS §5) or a new idea; the
  chain only has to handle H ∈ [2√2 − 1, 2), which may simplify `Final5` (the row-bound-5 cases with lines turning
  vertical are exactly the small-H regime).
