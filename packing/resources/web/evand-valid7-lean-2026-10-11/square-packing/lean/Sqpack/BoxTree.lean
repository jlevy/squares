import Sqpack.S32

/-!
# A generic box-tree verifier for point certificates (the Lean lower-bound ladder)

A **point certificate** is a finite list of entries `(X, Y, w)` — the point `(X/D, Y/D)` with
weight `w/W` — such that every closed unit square inside `[0, Mq/D]²`, at every angle, contains
entries of total weight `≥ 1`.  With total weight `< n` it proves `s(n) ≥ Mq/D` (`Basic.lean`,
`S32.lean`).  This file checks the covering statement **in the kernel**, from a *box tree*: a
subdivision of pose space `(c_x, c_y, u)`, `u = tan(θ/2)`, into boxes, each leaf naming points
that lie in every admissible square of its box.  Nothing here is specific to one certificate;
a certificate is data plus one call of `le_minSide` (`S12Lower.lean`).  Design, measurements and
the ladder: `lean/LADDER.md`.

## The computation (`check`, natural-number arithmetic only)

Everything is scaled to integers: centres over `Q = D·S`, the angle parameter over `R`.

* **Containment** (`ptOk`).  With `θ = 2 arctan u`, `p ∈ sq c θ 1` iff the four violation
  polynomials `G_k` of `ZeroMargin.lean` are `≤ 0` (`mem_sq_iff_gval`).  Each `G_k` is affine in
  the centre with coefficients of fixed sign for `u ∈ [0,1]`, so its maximum over a centre
  rectangle is at one corner (Lemma A of `ZeroMargin.lean`), and it is quadratic in `u`, so on a
  bin `[U0,U1]` it is bounded by its three degree-2 Bernstein coefficients `G(U0)`, `G(U1)` and
  the polar value `G(U0,U1)` (`lin3`).  All twelve tests are linear in the point: `triOk`.
* **Walls** (`wlo`, `leafW`).  A square at angle `θ` fits in the container iff its centre is in
  `[w/2, m − w/2]²`, `w = |cos θ| + |sin θ|` (`sq_subset_box_iff`).  On a bin, `w/2` is bounded
  below by the rational `wlo/Q`; the centre rectangle is clipped by it before the corners are
  taken, and a leaf whose clipped rectangle is empty holds vacuously.
* **Counting** (`capSel`).  A leaf lists which candidates it claims (gaps into the candidate
  list); they must all pass `ptOk` and weigh `≥ W`.
* **Pruning** (`near`, node `F`) shrinks the candidate list; it can only make the check fail.

## Soundness

`sound`: `check … t box c = true → Cov … box`.  `Cov` (the semantic statement) glues along
splits (`Cov.splitX/Y/U`), so a large tree is checked as many separate kernel declarations.
`le_minSide`: a covered D4 fundamental region, a D4-invariant point set (`d4Check`) and total
weight `< n` give `Mq/D ≤ minSide n`.
-/

namespace SquarePacking

namespace BoxTree

/-- A pose-space subdivision tree.  `L sel` is a leaf; `sel` selects the candidate points the
leaf claims (as gaps: skip `k` candidates, take the next one).  `X l r`, `Y l r`, `U l r` split the
current box at the midpoint of the centre `x`, the centre `y`, or the angle parameter
`u = tan(θ/2)`.  `F t` prunes the candidate list to the points near the current box (only an
efficiency device: pruning can only make the check fail). -/
inductive BT
  | L (sel : List ℕ)
  | X (l r : BT)
  | Y (l r : BT)
  | U (l r : BT)
  | F (t : BT)

/-- The four containment tests of one direction triple `(α, β, γ)` (all natural numbers): with
`(α, β, γ) ∝ (2(1−u²), 4u, 1+u²)` (or its polar form on a bin) these are the violation polynomials
`G₀..G₃` of `ZeroMargin.lean` at the worst centre corner, with all negative terms moved across. -/
def triOk (G α β xl xh yl yh aX bY bX aY : ℕ) : Bool :=
  Nat.ble (Nat.add aX bY) (Nat.add (Nat.add G (Nat.mul α xl)) (Nat.mul β yl)) &&
  Nat.ble (Nat.add (Nat.mul α xh) (Nat.mul β yh)) (Nat.add (Nat.add G aX) bY) &&
  Nat.ble (Nat.add aY (Nat.mul β xh)) (Nat.add (Nat.add G bX) (Nat.mul α yl)) &&
  Nat.ble (Nat.add bX (Nat.mul α yh)) (Nat.add (Nat.add G aY) (Nat.mul β xl))

/-- `triOk` at the point `(X, Y)`. -/
def triPt (Q α β γ xl xh yl yh X Y : ℕ) : Bool :=
  triOk (Nat.mul γ Q) α β xl xh yl yh (Nat.mul α X) (Nat.mul β Y) (Nat.mul β X) (Nat.mul α Y)

/-- The point `(X/Q, Y/Q)` lies in every closed unit square with centre in `[xl,xh]×[yl,yh]`
(over `Q`) and `u ∈ [U0/R, U1/R]`: the three Bernstein (polar-form) coefficients of each
violation polynomial are `≤ 0`. -/
def ptOk (Q R U0 U1 xl xh yl yh X Y : ℕ) : Bool :=
  triPt Q (Nat.mul 2 (Nat.sub (Nat.mul R R) (Nat.mul U0 U0))) (Nat.mul 4 (Nat.mul R U0))
    (Nat.add (Nat.mul R R) (Nat.mul U0 U0)) xl xh yl yh X Y &&
  triPt Q (Nat.mul 2 (Nat.sub (Nat.mul R R) (Nat.mul U1 U1))) (Nat.mul 4 (Nat.mul R U1))
    (Nat.add (Nat.mul R R) (Nat.mul U1 U1)) xl xh yl yh X Y &&
  triPt Q (Nat.mul 2 (Nat.sub (Nat.mul R R) (Nat.mul U0 U1)))
    (Nat.mul 2 (Nat.mul R (Nat.add U0 U1))) (Nat.add (Nat.mul R R) (Nat.mul U0 U1)) xl xh yl yh X Y

/-- Do the selected candidates all pass `ptOk`, and weigh at least `need`?  `sel` lists gaps:
skip `k` candidates, then test and take the next one. -/
def capSel (S Q R U0 U1 xl xh yl yh : ℕ) : ℕ → List ℕ → List (ℕ × ℕ × ℕ) → Bool
  | 0, _, _ => true
  | _ + 1, [], _ => false
  | need + 1, k :: ks, c =>
    match c.drop k with
    | [] => false
    | e :: t => ptOk Q R U0 U1 xl xh yl yh (Nat.mul e.1 S) (Nat.mul e.2.1 S) &&
        capSel S Q R U0 U1 xl xh yl yh (Nat.sub (need + 1) e.2.2) ks t

/-- A lower bound (over `Q`) for `w(θ)/2` on the bin:
`⌊Q (R² + 2 U0 R − U1²) / (2 (R² + U1²))⌋`. -/
def wlo (Q R U0 U1 : ℕ) : ℕ :=
  Nat.div (Nat.mul Q (Nat.sub (Nat.add (Nat.mul R R) (Nat.mul 2 (Nat.mul U0 R))) (Nat.mul U1 U1)))
    (Nat.mul 2 (Nat.add (Nat.mul R R) (Nat.mul U1 U1)))

/-- The leaf test on the clipped centre rectangle `[xl,xh]×[yl,yh]`. -/
def leafClip (W S Q R U0 U1 xl xh yl yh : ℕ) (sel : List ℕ) (c : List (ℕ × ℕ × ℕ)) : Bool :=
  Nat.blt xh xl || Nat.blt yh yl || capSel S Q R U0 U1 xl xh yl yh W sel c

/-- The leaf test with the wall bound `WL`. -/
def leafW (W S Q M R x0 x1 y0 y1 U0 U1 WL : ℕ) (sel : List ℕ) (c : List (ℕ × ℕ × ℕ)) : Bool :=
  leafClip W S Q R U0 U1 (max x0 WL) (min x1 (Nat.sub M WL)) (max y0 WL)
    (min y1 (Nat.sub M WL)) sel c

/-- Candidate filter (efficiency only): points within `F/Q` of the centre rectangle. -/
def near (S F x0 x1 y0 y1 : ℕ) (c : List (ℕ × ℕ × ℕ)) : List (ℕ × ℕ × ℕ) :=
  c.filter fun e => Nat.ble x0 (Nat.add (Nat.mul e.1 S) F) &&
    Nat.ble (Nat.mul e.1 S) (Nat.add x1 F) &&
    Nat.ble y0 (Nat.add (Nat.mul e.2.1 S) F) && Nat.ble (Nat.mul e.2.1 S) (Nat.add y1 F)

/-- The tree check on the box `[x0,x1]×[y0,y1]×[u0,u1]` with candidate list `c`. -/
def check (W S Q M R F : ℕ) : BT → ℕ → ℕ → ℕ → ℕ → ℕ → ℕ → List (ℕ × ℕ × ℕ) → Bool
  | .L sel, x0, x1, y0, y1, u0, u1, c =>
    Nat.ble u1 R && leafW W S Q M R x0 x1 y0 y1 u0 u1 (wlo Q R u0 u1) sel c
  | .F t, x0, x1, y0, y1, u0, u1, c =>
    check W S Q M R F t x0 x1 y0 y1 u0 u1 (near S F x0 x1 y0 y1 c)
  | .X l r, x0, x1, y0, y1, u0, u1, c =>
    check W S Q M R F l x0 (Nat.div (Nat.add x0 x1) 2) y0 y1 u0 u1 c &&
    check W S Q M R F r (Nat.div (Nat.add x0 x1) 2) x1 y0 y1 u0 u1 c
  | .Y l r, x0, x1, y0, y1, u0, u1, c =>
    check W S Q M R F l x0 x1 y0 (Nat.div (Nat.add y0 y1) 2) u0 u1 c &&
    check W S Q M R F r x0 x1 (Nat.div (Nat.add y0 y1) 2) y1 u0 u1 c
  | .U l r, x0, x1, y0, y1, u0, u1, c =>
    check W S Q M R F l x0 x1 y0 y1 u0 (Nat.div (Nat.add u0 u1) 2) c &&
    check W S Q M R F r x0 x1 y0 y1 (Nat.div (Nat.add u0 u1) 2) u1 c

/-! ### Compact encoding of trees

A tree is shipped as one natural number, read as a stream of base-`B` digits (least significant
first): `0 k g₁ … g_k` is a leaf `L [g₁, …, g_k]`, and `1`, `2`, `3`, `4` are `X`, `Y`, `U`, `F`
followed by their subtrees.  One numeral elaborates in no time, where a nested term of tens of
thousands of constructors costs as much elaboration as its kernel check.  The decoder needs no
proof: `sound` holds for *every* tree, in particular for whatever `dec` returns. -/

/-- Decode `k` leaf-selection digits. -/
def decSel (B : ℕ) : ℕ → ℕ → List ℕ × ℕ
  | 0, n => ([], n)
  | k + 1, n => (Nat.mod n B :: (decSel B k (Nat.div n B)).1, (decSel B k (Nat.div n B)).2)

/-- Decode a tree of depth `≤ fuel`; returns the tree and the rest of the stream. -/
def dec (B : ℕ) : ℕ → ℕ → BT × ℕ
  | 0, n => (.L [], n)
  | f + 1, n =>
    match Nat.mod n B with
    | 0 => (.L (decSel B (Nat.mod (Nat.div n B) B) (Nat.div (Nat.div n B) B)).1,
            (decSel B (Nat.mod (Nat.div n B) B) (Nat.div (Nat.div n B) B)).2)
    | 1 => (.X (dec B f (Nat.div n B)).1 (dec B f (dec B f (Nat.div n B)).2).1,
            (dec B f (dec B f (Nat.div n B)).2).2)
    | 2 => (.Y (dec B f (Nat.div n B)).1 (dec B f (dec B f (Nat.div n B)).2).1,
            (dec B f (dec B f (Nat.div n B)).2).2)
    | 3 => (.U (dec B f (Nat.div n B)).1 (dec B f (dec B f (Nat.div n B)).2).1,
            (dec B f (dec B f (Nat.div n B)).2).2)
    | _ => (.F (dec B f (Nat.div n B)).1, (dec B f (Nat.div n B)).2)

/-! ## Soundness -/

section sound

/-- Unfolding the kernel-friendly spellings. -/
lemma nat_add_eq (a b : ℕ) : Nat.add a b = a + b := rfl
lemma nat_mul_eq (a b : ℕ) : Nat.mul a b = a * b := rfl
lemma nat_sub_eq (a b : ℕ) : Nat.sub a b = a - b := rfl
lemma nat_div_eq (a b : ℕ) : Nat.div a b = a / b := rfl

/-- **The degree-2 Bernstein bound.**  `E(v) = 2(R²−v²)a + 4Rvb − (R²+v²)Q` is quadratic in `v`;
on `[U0,U1]` it is a convex combination of `E(U0)`, `E(U1)` and its polar form `E(U0,U1)`. -/
lemma lin3 {Q R U0 U1 v a b : ℝ} (h0 : U0 ≤ v) (h1 : v ≤ U1)
    (e0 : 2 * (R ^ 2 - U0 ^ 2) * a + 4 * R * U0 * b ≤ (R ^ 2 + U0 ^ 2) * Q)
    (e1 : 2 * (R ^ 2 - U1 ^ 2) * a + 4 * R * U1 * b ≤ (R ^ 2 + U1 ^ 2) * Q)
    (em : 2 * (R ^ 2 - U0 * U1) * a + 2 * R * (U0 + U1) * b ≤ (R ^ 2 + U0 * U1) * Q) :
    2 * (R ^ 2 - v ^ 2) * a + 4 * R * v * b ≤ (R ^ 2 + v ^ 2) * Q := by
  have key : (U1 - U0) ^ 2 * (2 * (R ^ 2 - v ^ 2) * a + 4 * R * v * b - (R ^ 2 + v ^ 2) * Q) =
      (U1 - v) ^ 2 * (2 * (R ^ 2 - U0 ^ 2) * a + 4 * R * U0 * b - (R ^ 2 + U0 ^ 2) * Q)
      + 2 * ((v - U0) * (U1 - v)) *
          (2 * (R ^ 2 - U0 * U1) * a + 2 * R * (U0 + U1) * b - (R ^ 2 + U0 * U1) * Q)
      + (v - U0) ^ 2 * (2 * (R ^ 2 - U1 ^ 2) * a + 4 * R * U1 * b - (R ^ 2 + U1 ^ 2) * Q) := by
    ring
  rcases eq_or_lt_of_le (le_trans h0 h1) with h | h
  · have hv : v = U0 := by linarith
    subst hv; linarith
  · have hpos : 0 < (U1 - U0) ^ 2 := pow_pos (by linarith) 2
    have t1 := mul_nonpos_of_nonneg_of_nonpos (sq_nonneg (U1 - v))
      (by linarith : 2 * (R ^ 2 - U0 ^ 2) * a + 4 * R * U0 * b - (R ^ 2 + U0 ^ 2) * Q ≤ 0)
    have t2 := mul_nonpos_of_nonneg_of_nonpos
      (mul_nonneg (by norm_num : (0:ℝ) ≤ 2)
        (mul_nonneg (by linarith : 0 ≤ v - U0) (by linarith : 0 ≤ U1 - v)))
      (by linarith : 2 * (R ^ 2 - U0 * U1) * a + 2 * R * (U0 + U1) * b - (R ^ 2 + U0 * U1) * Q ≤ 0)
    have t3 := mul_nonpos_of_nonneg_of_nonpos (sq_nonneg (v - U0))
      (by linarith : 2 * (R ^ 2 - U1 ^ 2) * a + 4 * R * U1 * b - (R ^ 2 + U1 ^ 2) * Q ≤ 0)
    have hle :
        (U1 - U0) ^ 2 * (2 * (R ^ 2 - v ^ 2) * a + 4 * R * v * b - (R ^ 2 + v ^ 2) * Q) ≤ 0 := by
      rw [key]; linarith
    have := (mul_nonpos_iff.mp hle)
    rcases this with ⟨_, h2⟩ | ⟨h1', _⟩
    · linarith
    · linarith

/-- The four tests of `triOk`, over `ℝ`. -/
lemma triOk_sound {G α β xl xh yl yh X Y : ℕ}
    (h : triOk G α β xl xh yl yh (Nat.mul α X) (Nat.mul β Y) (Nat.mul β X) (Nat.mul α Y) = true) :
    (α : ℝ) * ((X : ℝ) - xl) + β * ((Y : ℝ) - yl) ≤ G ∧
    (α : ℝ) * ((xh : ℝ) - X) + β * ((yh : ℝ) - Y) ≤ G ∧
    (α : ℝ) * ((Y : ℝ) - yl) + β * ((xh : ℝ) - X) ≤ G ∧
    (α : ℝ) * ((yh : ℝ) - Y) + β * ((X : ℝ) - xl) ≤ G := by
  simp only [triOk, Bool.and_eq_true, Nat.ble_eq, nat_add_eq, nat_mul_eq] at h
  obtain ⟨⟨⟨h1, h2⟩, h3⟩, h4⟩ := h
  have c1 : ((α * X + β * Y : ℕ) : ℝ) ≤ ((G + α * xl + β * yl : ℕ) : ℝ) := by exact_mod_cast h1
  have c2 : ((α * xh + β * yh : ℕ) : ℝ) ≤ ((G + α * X + β * Y : ℕ) : ℝ) := by exact_mod_cast h2
  have c3 : ((α * Y + β * xh : ℕ) : ℝ) ≤ ((G + β * X + α * yl : ℕ) : ℝ) := by exact_mod_cast h3
  have c4 : ((β * X + α * yh : ℕ) : ℝ) ≤ ((G + α * Y + β * xl : ℕ) : ℝ) := by exact_mod_cast h4
  push_cast at c1 c2 c3 c4
  refine ⟨by linarith, by linarith, by linarith, by linarith⟩

/-- The violation polynomials `G₁, G₂, G₃` are `G₀` at transformed offsets. -/
lemma gval_one (a b u : ℝ) : gval 1 a b u = gval 0 (-a) (-b) u := by
  simp only [gval, gc]; ring
lemma gval_two (a b u : ℝ) : gval 2 a b u = gval 0 b (-a) u := by
  simp only [gval, gc]; ring
lemma gval_three (a b u : ℝ) : gval 3 a b u = gval 0 (-b) a u := by
  simp only [gval, gc]; ring

/-- `G₀ ≤ 0` from the corner inequality (the centre is monotone: the coefficients of the offsets
are `≥ 0` for `u ∈ [0,1]`). -/
lemma gval0_le {Q R u p q ac bc : ℝ} (hQ : 0 < Q) (hR : 0 < R) (hu0 : 0 ≤ u) (hu1 : u ≤ 1)
    (ha : p * Q ≤ ac) (hb : q * Q ≤ bc)
    (hc : 2 * (R ^ 2 - (u * R) ^ 2) * ac + 4 * R * (u * R) * bc ≤ (R ^ 2 + (u * R) ^ 2) * Q) :
    gval 0 p q u ≤ 0 := by
  have key : Q * R ^ 2 * gval 0 p q u
      = 2 * (R ^ 2 - (u * R) ^ 2) * (p * Q) + 4 * R * (u * R) * (q * Q)
        - (R ^ 2 + (u * R) ^ 2) * Q := by
    simp only [gval, gc]; ring
  have h2 : 0 ≤ 2 * (R ^ 2 - (u * R) ^ 2) := by
    have : (u * R) ^ 2 ≤ R ^ 2 := by
      rw [mul_pow]; nlinarith [sq_nonneg R, mul_le_mul hu1 hu1 hu0 zero_le_one]
    linarith
  have h3 : 0 ≤ 4 * R * (u * R) := by positivity
  have hle : Q * R ^ 2 * gval 0 p q u ≤ 0 := by
    rw [key]
    nlinarith [mul_le_mul_of_nonneg_left ha h2, mul_le_mul_of_nonneg_left hb h3]
  by_contra hg
  have := mul_pos (by positivity : 0 < Q * R ^ 2) (not_le.mp hg)
  linarith

/-- Casts of the direction triples. -/
lemma cast_alpha {R U V : ℕ} (h : U * V ≤ R * R) :
    ((Nat.mul 2 (Nat.sub (Nat.mul R R) (Nat.mul U V)) : ℕ) : ℝ) = 2 * ((R : ℝ) ^ 2 - U * V) := by
  simp only [nat_mul_eq, nat_sub_eq]
  rw [Nat.cast_mul, Nat.cast_sub h]; push_cast; ring

/-- **Soundness of `ptOk`**: the point lies in every closed unit square of the clipped box. -/
theorem ptOk_mem {Q R U0 U1 xl xh yl yh X Y : ℕ} (hQ : 0 < Q) (hR : 0 < R) (hU : U0 ≤ U1)
    (hU1 : U1 ≤ R) (h : ptOk Q R U0 U1 xl xh yl yh X Y = true) (c : ℝ × ℝ) (u : ℝ)
    (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R)
    (hx0 : (xl : ℝ) / Q ≤ c.1) (hx1 : c.1 ≤ (xh : ℝ) / Q)
    (hy0 : (yl : ℝ) / Q ≤ c.2) (hy1 : c.2 ≤ (yh : ℝ) / Q) :
    ((X : ℝ) / Q, (Y : ℝ) / Q) ∈ sq c (2 * Real.arctan u) 1 := by
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hUr : (U0 : ℝ) ≤ U1 := by exact_mod_cast hU
  have hU1r : (U1 : ℝ) ≤ R := by exact_mod_cast hU1
  have hU0r : (0 : ℝ) ≤ U0 := Nat.cast_nonneg _
  simp only [ptOk, triPt, Bool.and_eq_true] at h
  obtain ⟨⟨h0, h1⟩, hm⟩ := h
  have T0 := triOk_sound h0
  have T1 := triOk_sound h1
  have Tm := triOk_sound hm
  have n00 : U0 * U0 ≤ R * R := Nat.mul_le_mul (le_trans hU hU1) (le_trans hU hU1)
  have n11 : U1 * U1 ≤ R * R := Nat.mul_le_mul hU1 hU1
  have n01 : U0 * U1 ≤ R * R := Nat.mul_le_mul (le_trans hU hU1) hU1
  rw [cast_alpha n00] at T0
  rw [cast_alpha n11] at T1
  rw [cast_alpha n01] at Tm
  simp only [nat_mul_eq, nat_add_eq] at T0 T1 Tm
  push_cast at T0 T1 Tm
  -- the angle parameter
  set v := u * R with hv
  have hv0 : (U0 : ℝ) ≤ v := by rw [div_le_iff₀ hRr] at hu0; linarith
  have hv1 : v ≤ (U1 : ℝ) := by rw [le_div_iff₀ hRr] at hu1; linarith
  have hu0' : 0 ≤ u := le_trans (div_nonneg hU0r hRr.le) hu0
  have hu1' : u ≤ 1 := le_trans hu1 ((div_le_one hRr).mpr hU1r)
  -- the centre
  have cx0 : (xl : ℝ) ≤ c.1 * Q := by rw [div_le_iff₀ hQr] at hx0; linarith
  have cx1 : c.1 * Q ≤ (xh : ℝ) := by rw [le_div_iff₀ hQr] at hx1; linarith
  have cy0 : (yl : ℝ) ≤ c.2 * Q := by rw [div_le_iff₀ hQr] at hy0; linarith
  have cy1 : c.2 * Q ≤ (yh : ℝ) := by rw [le_div_iff₀ hQr] at hy1; linarith
  have eX : ((X : ℝ) / Q - c.1) * Q = X - c.1 * Q := by field_simp
  have eY : ((Y : ℝ) / Q - c.2) * Q = Y - c.2 * Q := by field_simp
  have L := fun {a b : ℝ}
      (e0 : 2 * ((R : ℝ) ^ 2 - U0 * U0) * a + 4 * R * U0 * b ≤ (R ^ 2 + U0 * U0) * Q)
      (e1 : 2 * ((R : ℝ) ^ 2 - U1 * U1) * a + 4 * R * U1 * b ≤ (R ^ 2 + U1 * U1) * Q)
      (em : 2 * ((R : ℝ) ^ 2 - U0 * U1) * a + 2 * R * (U0 + U1) * b ≤ (R ^ 2 + U0 * U1) * Q) =>
    lin3 (Q := (Q : ℝ)) (R := (R : ℝ)) (v := v) (a := a) (b := b) hv0 hv1
      (by rw [pow_two]; linarith) (by rw [pow_two]; linarith) em
  rw [mem_sq_iff_gval]
  intro k
  fin_cases k
  · -- `G₀`, corner `(xl, yl)`
    refine gval0_le hQr hRr hu0' hu1' (ac := X - xl) (bc := Y - yl) (by rw [eX]; linarith)
      (by rw [eY]; linarith) (L ?_ ?_ ?_) <;> linarith [T0.1, T1.1, Tm.1]
  · -- `G₁`, corner `(xh, yh)`
    change gval 1 _ _ _ ≤ 0
    rw [gval_one]
    refine gval0_le hQr hRr hu0' hu1' (ac := xh - X) (bc := yh - Y)
      (by rw [neg_mul, eX]; linarith)
      (by rw [neg_mul, eY]; linarith) (L ?_ ?_ ?_) <;> linarith [T0.2.1, T1.2.1, Tm.2.1]
  · -- `G₂`, corner `(xh, yl)`
    change gval 2 _ _ _ ≤ 0
    rw [gval_two]
    refine gval0_le hQr hRr hu0' hu1' (ac := Y - yl) (bc := xh - X) (by rw [eY]; linarith)
      (by rw [neg_mul, eX]; linarith) (L ?_ ?_ ?_) <;> linarith [T0.2.2.1, T1.2.2.1, Tm.2.2.1]
  · -- `G₃`, corner `(xl, yh)`
    change gval 3 _ _ _ ≤ 0
    rw [gval_three]
    refine gval0_le hQr hRr hu0' hu1' (ac := yh - Y) (bc := X - xl)
      (by rw [neg_mul, eY]; linarith)
      (by rw [eX]; linarith) (L ?_ ?_ ?_) <;> linarith [T0.2.2.2, T1.2.2.2, Tm.2.2.2]

/-- **The wall bound** (`clip_bin` with a rational lower bound): an admissible square at angle
`2 arctan u`, `u ∈ [U0/R, U1/R] ⊆ [0,1]`, has `w(θ)/2 ≥ wlo/Q`. -/
theorem wlo_le {Q R U0 U1 : ℕ} (hQ : 0 < Q) (hR : 0 < R) (hU1 : U1 ≤ R) {u : ℝ}
    (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) :
    (wlo Q R U0 U1 : ℝ) / Q ≤ wid (2 * Real.arctan u) / 2 := by
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hU1r : (U1 : ℝ) ≤ R := by exact_mod_cast hU1
  have hU0r : (0 : ℝ) ≤ U0 := Nat.cast_nonneg _
  have hu0' : 0 ≤ u := le_trans (div_nonneg hU0r hRr.le) hu0
  have hu1' : u ≤ 1 := le_trans hu1 ((div_le_one hRr).mpr hU1r)
  rw [wid_two_arctan hu0' hu1', widU]
  set v := u * R with hv
  have hv0 : (U0 : ℝ) ≤ v := by rw [div_le_iff₀ hRr] at hu0; linarith
  have hv1 : v ≤ (U1 : ℝ) := by rw [le_div_iff₀ hRr] at hu1; linarith
  -- the integer inequality defining `wlo`
  have n11 : U1 * U1 ≤ R * R + 2 * (U0 * R) :=
    le_trans (Nat.mul_le_mul hU1 hU1) (Nat.le_add_right _ _)
  have hdiv : wlo Q R U0 U1 * (2 * (R * R + U1 * U1)) ≤ Q * (R * R + 2 * (U0 * R) - U1 * U1) := by
    simp only [wlo, nat_mul_eq, nat_add_eq, nat_sub_eq, nat_div_eq]
    exact Nat.div_mul_le_self _ _
  have hdivr : (wlo Q R U0 U1 : ℝ) * (2 * (R * R + U1 * U1))
      ≤ Q * (R * R + 2 * (U0 * R) - U1 * U1) := by
    have := (Nat.cast_le (α := ℝ)).mpr hdiv
    push_cast [Nat.cast_sub n11] at this
    linarith
  have hW0 : (0 : ℝ) ≤ wlo Q R U0 U1 := Nat.cast_nonneg _
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  rw [div_le_iff₀ hQr]
  rw [div_div, div_mul_eq_mul_div, le_div_iff₀ (by positivity)]
  -- `wlo·2(R²+v²) ≤ wlo·2(R²+U1²) ≤ Q(R²+2U0R−U1²) ≤ Q(R²+2vR−v²)`, divided by `R²`
  have hR2 : (0 : ℝ) < R ^ 2 := by positivity
  have e1 : (wlo Q R U0 U1 : ℝ) * (2 * (R * R + v * v))
      ≤ (wlo Q R U0 U1 : ℝ) * (2 * (R * R + U1 * U1)) := by
    apply mul_le_mul_of_nonneg_left _ hW0
    nlinarith
  have e2 : (Q : ℝ) * (R * R + 2 * (U0 * R) - U1 * U1) ≤ Q * (R * R + 2 * (v * R) - v * v) := by
    apply mul_le_mul_of_nonneg_left _ hQr.le
    nlinarith
  have e3 : (wlo Q R U0 U1 : ℝ) * (2 * (R * R + v * v)) ≤ Q * (R * R + 2 * (v * R) - v * v) := by
    linarith
  have ev1 : R * R + v * v = R ^ 2 * (1 + u ^ 2) := by rw [hv]; ring
  have ev2 : R * R + 2 * (v * R) - v * v = R ^ 2 * (1 - u ^ 2 + 2 * u) := by rw [hv]; ring
  rw [ev1, ev2] at e3
  nlinarith

/-- Counting: `capSel` accepts only if it has selected a sublist of certified candidates
weighing `≥ need`. -/
theorem capSel_sub {S Q R U0 U1 xl xh yl yh : ℕ} :
    ∀ (sel : List ℕ) (c : List (ℕ × ℕ × ℕ)) (need : ℕ),
      capSel S Q R U0 U1 xl xh yl yh need sel c = true →
      ∃ L : List (ℕ × ℕ × ℕ), L.Sublist c ∧
        (∀ e ∈ L, ptOk Q R U0 U1 xl xh yl yh (Nat.mul e.1 S) (Nat.mul e.2.1 S) = true) ∧
        need ≤ (L.map fun e => e.2.2).sum := by
  intro sel
  induction sel with
  | nil =>
    intro c need h
    cases need with
    | zero => exact ⟨[], List.nil_sublist _, by simp, le_refl _⟩
    | succ n => simp [capSel] at h
  | cons k ks ih =>
    intro c need h
    cases need with
    | zero => exact ⟨[], List.nil_sublist _, by simp, Nat.zero_le _⟩
    | succ n =>
      simp only [capSel] at h
      split at h
      · simp at h
      · rename_i e t hdrop
        rw [Bool.and_eq_true] at h
        obtain ⟨L, hL, hall, hsum⟩ := ih t _ h.2
        refine ⟨e :: L, ?_, ?_, ?_⟩
        · have : (e :: t).Sublist c := hdrop ▸ List.drop_sublist k c
          exact (hL.cons_cons e).trans this
        · intro e' he'
          rcases List.mem_cons.mp he' with rfl | he'
          · exact h.1
          · exact hall e' he'
        · rw [List.map_cons, List.sum_cons]
          simp only [nat_sub_eq] at hsum
          omega

/-- A certified sublist of a duplicate-free list weighs at most the captured weight. -/
theorem sum_le_captured {pts c : List (ℕ × ℕ × ℕ)} (hnd : pts.Nodup) (hc : c.Sublist pts)
    (T : Set (ℕ × ℕ × ℕ)) (hT : ∀ e ∈ c, e ∈ T) :
    open Classical in (c.map fun e => e.2.2).sum ≤ ∑ e ∈ pts.toFinset.filter (· ∈ T), e.2.2 := by
  classical
  have hcn : c.Nodup := hc.nodup hnd
  rw [← List.sum_toFinset _ hcn]
  apply Finset.sum_le_sum_of_subset
  intro e he
  rw [List.mem_toFinset] at he
  simp only [Finset.mem_filter, List.mem_toFinset]
  exact ⟨hc.subset he, hT e he⟩

/-- The real point of an entry `(X, Y, w)`: `(X/D, Y/D)`. -/
noncomputable def ptR (D : ℕ) (e : ℕ × ℕ × ℕ) : ℝ × ℝ := ((e.1 : ℝ) / D, (e.2.1 : ℝ) / D)

open Classical in
/-- **What a box-tree node certifies**: every closed unit square inside `[0, Mq/D]²` with centre
in `[x0,x1]×[y0,y1]` (over `Q = D·S`) and angle `2 arctan u`, `u ∈ [u0/R, u1/R]`, contains
entries of total weight `≥ W` (weights over `W`, i.e. total `≥ 1`). -/
def Cov (D S Mq R W : ℕ) (pts : List (ℕ × ℕ × ℕ)) (x0 x1 y0 y1 u0 u1 : ℕ) : Prop :=
  ∀ (c : ℝ × ℝ) (u : ℝ),
    (x0 : ℝ) / (D * S) ≤ c.1 → c.1 ≤ (x1 : ℝ) / (D * S) →
    (y0 : ℝ) / (D * S) ≤ c.2 → c.2 ≤ (y1 : ℝ) / (D * S) →
    (u0 : ℝ) / R ≤ u → u ≤ (u1 : ℝ) / R →
    sq c (2 * Real.arctan u) 1 ⊆ box ((Mq : ℝ) / D) →
    (W : ℝ) ≤ ∑ e ∈ pts.toFinset.filter (fun e => ptR D e ∈ sq c (2 * Real.arctan u) 1),
      (e.2.2 : ℝ)

/-- Gluing along `x`. -/
theorem Cov.splitX {D S Mq R W : ℕ} {pts : List (ℕ × ℕ × ℕ)} {x0 x1 y0 y1 u0 u1 : ℕ} (m : ℕ)
    (h1 : Cov D S Mq R W pts x0 m y0 y1 u0 u1) (h2 : Cov D S Mq R W pts m x1 y0 y1 u0 u1) :
    Cov D S Mq R W pts x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  rcases le_total c.1 ((m : ℝ) / (D * S)) with h | h
  · exact h1 c u hx0 h hy0 hy1 hu0 hu1 hsub
  · exact h2 c u h hx1 hy0 hy1 hu0 hu1 hsub

/-- Gluing along `y`. -/
theorem Cov.splitY {D S Mq R W : ℕ} {pts : List (ℕ × ℕ × ℕ)} {x0 x1 y0 y1 u0 u1 : ℕ} (m : ℕ)
    (h1 : Cov D S Mq R W pts x0 x1 y0 m u0 u1) (h2 : Cov D S Mq R W pts x0 x1 m y1 u0 u1) :
    Cov D S Mq R W pts x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  rcases le_total c.2 ((m : ℝ) / (D * S)) with h | h
  · exact h1 c u hx0 hx1 hy0 h hu0 hu1 hsub
  · exact h2 c u hx0 hx1 h hy1 hu0 hu1 hsub

/-- Gluing along `u`. -/
theorem Cov.splitU {D S Mq R W : ℕ} {pts : List (ℕ × ℕ × ℕ)} {x0 x1 y0 y1 u0 u1 : ℕ} (m : ℕ)
    (h1 : Cov D S Mq R W pts x0 x1 y0 y1 u0 m) (h2 : Cov D S Mq R W pts x0 x1 y0 y1 m u1) :
    Cov D S Mq R W pts x0 x1 y0 y1 u0 u1 := by
  intro c u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  rcases le_total u ((m : ℝ) / R) with h | h
  · exact h1 c u hx0 hx1 hy0 hy1 hu0 h hsub
  · exact h2 c u hx0 hx1 hy0 hy1 h hu1 hsub

/-- **Soundness of a leaf.** -/
theorem leaf_sound {D S Mq R W F : ℕ} {pts : List (ℕ × ℕ × ℕ)} (hD : 0 < D) (hS : 0 < S)
    (hR : 0 < R) (hnd : pts.Nodup) {x0 x1 y0 y1 u0 u1 : ℕ} {c : List (ℕ × ℕ × ℕ)}
    {sel : List ℕ} (hc : c.Sublist pts)
    (h : check W S (D * S) (Mq * S) R F (.L sel) x0 x1 y0 y1 u0 u1 c = true) :
    Cov D S Mq R W pts x0 x1 y0 y1 u0 u1 := by
  classical
  intro cc u hx0 hx1 hy0 hy1 hu0 hu1 hsub
  simp only [check, Bool.and_eq_true, Nat.ble_eq] at h
  obtain ⟨hu1R, h⟩ := h
  set Q := D * S with hQdef
  set M := Mq * S with hMdef
  have hQ : 0 < Q := Nat.mul_pos hD hS
  have hQr : (0 : ℝ) < Q := by exact_mod_cast hQ
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hSr : (0 : ℝ) < S := by exact_mod_cast hS
  have hQc : ((D : ℝ) * S) = (Q : ℝ) := by rw [hQdef]; push_cast; ring
  rw [hQc] at hx0 hx1 hy0 hy1
  have hU : u0 ≤ u1 := by
    have : (u0 : ℝ) / R ≤ (u1 : ℝ) / R := le_trans hu0 hu1
    rw [div_le_div_iff_of_pos_right hRr] at this
    exact_mod_cast this
  -- admissibility and the wall bound
  obtain ⟨a1, a2, a3, a4⟩ := (sq_subset_box_iff _ cc _).mp hsub
  have hWL := wlo_le (U0 := u0) hQ hR hu1R hu0 hu1
  set WL := wlo Q R u0 u1 with hWLdef
  have hm : (Mq : ℝ) / D = (M : ℝ) / Q := by
    rw [hMdef, hQdef]; push_cast; field_simp
  rw [hm] at a2 a4
  have hMWL : ((M : ℝ) - WL) / Q ≤ ((Nat.sub M WL : ℕ) : ℝ) / Q := by
    apply div_le_div_of_nonneg_right _ hQr.le
    rw [nat_sub_eq]
    rcases le_total WL M with h' | h'
    · rw [Nat.cast_sub h']
    · rw [Nat.sub_eq_zero_of_le h']
      have : (M : ℝ) ≤ WL := by exact_mod_cast h'
      simp only [Nat.cast_zero]; linarith
  have eMW : ((M : ℝ) - WL) / Q = (M : ℝ) / Q - (WL : ℝ) / Q := by ring
  have lo : ∀ (z0 : ℕ) (z : ℝ), (z0 : ℝ) / Q ≤ z → WL / (Q : ℝ) ≤ z →
      ((max z0 WL : ℕ) : ℝ) / Q ≤ z := by
    intro z0 z h1 h2
    rcases le_total z0 WL with h' | h'
    · rw [max_eq_right h']; exact h2
    · rw [max_eq_left h']; exact h1
  have hi : ∀ (z1 : ℕ) (z : ℝ), z ≤ (z1 : ℝ) / Q → z ≤ (M : ℝ) / Q - WL / Q →
      z ≤ ((min z1 (Nat.sub M WL) : ℕ) : ℝ) / Q := by
    intro z1 z h1 h2
    rcases le_total z1 (Nat.sub M WL) with h' | h'
    · rw [min_eq_left h']; exact h1
    · rw [min_eq_right h']; linarith
  have cx0 := lo x0 cc.1 hx0 (by linarith)
  have cx1 := hi x1 cc.1 hx1 (by linarith)
  have cy0 := lo y0 cc.2 hy0 (by linarith)
  have cy1 := hi y1 cc.2 hy1 (by linarith)
  -- the leaf test: the clipped rectangle is non-empty, so the count succeeded
  simp only [leafW, leafClip, Bool.or_eq_true] at h
  have hxle : max x0 WL ≤ min x1 (Nat.sub M WL) := by
    have : ((max x0 WL : ℕ) : ℝ) ≤ ((min x1 (Nat.sub M WL) : ℕ) : ℝ) := by
      have := le_trans cx0 cx1
      rwa [div_le_div_iff_of_pos_right hQr] at this
    exact_mod_cast this
  have hyle : max y0 WL ≤ min y1 (Nat.sub M WL) := by
    have : ((max y0 WL : ℕ) : ℝ) ≤ ((min y1 (Nat.sub M WL) : ℕ) : ℝ) := by
      have := le_trans cy0 cy1
      rwa [div_le_div_iff_of_pos_right hQr] at this
    exact_mod_cast this
  rcases h with (h | h) | h
  · rw [Nat.blt_eq] at h; omega
  · rw [Nat.blt_eq] at h; omega
  -- the count
  obtain ⟨L, hLc, hall, hcnt⟩ := capSel_sub sel c W h
  have hLs : L.Sublist pts := hLc.trans hc
  have hT : ∀ e ∈ L, e ∈ {e : ℕ × ℕ × ℕ | ptR D e ∈ sq cc (2 * Real.arctan u) 1} := by
    intro e he
    have hm := ptOk_mem hQ hR hU hu1R (hall e he) cc u hu0 hu1 cx0 cx1 cy0 cy1
    have e1 : ((Nat.mul e.1 S : ℕ) : ℝ) / Q = (e.1 : ℝ) / D := by
      rw [nat_mul_eq, hQdef]; push_cast; field_simp
    have e2 : ((Nat.mul e.2.1 S : ℕ) : ℝ) / Q = (e.2.1 : ℝ) / D := by
      rw [nat_mul_eq, hQdef]; push_cast; field_simp
    rw [e1, e2] at hm
    exact hm
  have hsum := le_trans hcnt (sum_le_captured hnd hLs _ hT)
  have hsumr : (W : ℝ) ≤ ((∑ e ∈ pts.toFinset.filter
      (· ∈ {e : ℕ × ℕ × ℕ | ptR D e ∈ sq cc (2 * Real.arctan u) 1}), e.2.2 : ℕ) : ℝ) := by
    exact_mod_cast hsum
  rw [Nat.cast_sum] at hsumr
  simpa using hsumr

/-- **Soundness of the box-tree check.**  If `check` accepts the tree `t` on a box, with
candidates drawn from a duplicate-free list of entries, then the box is covered (`Cov`). -/
theorem sound (D S Mq R W F : ℕ) (pts : List (ℕ × ℕ × ℕ)) (hD : 0 < D) (hS : 0 < S)
    (hR : 0 < R) (hnd : pts.Nodup) :
    ∀ (t : BT) (x0 x1 y0 y1 u0 u1 : ℕ) (c : List (ℕ × ℕ × ℕ)), c.Sublist pts →
      check W S (D * S) (Mq * S) R F t x0 x1 y0 y1 u0 u1 c = true →
      Cov D S Mq R W pts x0 x1 y0 y1 u0 u1 := by
  intro t
  induction t with
  | L sel => intro x0 x1 y0 y1 u0 u1 c hc h; exact leaf_sound hD hS hR hnd hc h
  | F t ih =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check] at h
    exact ih _ _ _ _ _ _ _ ((List.filter_sublist).trans hc) h
  | X l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check, Bool.and_eq_true] at h
    exact Cov.splitX _ (ihl _ _ _ _ _ _ _ hc h.1) (ihr _ _ _ _ _ _ _ hc h.2)
  | Y l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check, Bool.and_eq_true] at h
    exact Cov.splitY _ (ihl _ _ _ _ _ _ _ hc h.1) (ihr _ _ _ _ _ _ _ hc h.2)
  | U l r ihl ihr =>
    intro x0 x1 y0 y1 u0 u1 c hc h
    simp only [check, Bool.and_eq_true] at h
    exact Cov.splitU _ (ihl _ _ _ _ _ _ _ hc h.1) (ihr _ _ _ _ _ _ _ hc h.2)

end sound

/-! ## From a covered root box to `s(n) ≥ Mq/D` -/

section final

/-- For `θ ∈ [0, π/4]`, `u = tan(θ/2)` satisfies `θ = 2 arctan u` and `0 ≤ u ≤ 29/70`
(`29/70 > √2 − 1 = tan(π/8)`). -/
lemma exists_u_of_theta' {θ : ℝ} (hθ : θ ∈ Set.Icc 0 (Real.pi / 4)) :
    ∃ u : ℝ, 0 ≤ u ∧ 70 * u ≤ 29 ∧ 2 * Real.arctan u = θ := by
  obtain ⟨h0, h1⟩ := hθ
  have hpi := Real.pi_pos
  set u := Real.tan (θ / 2) with hu
  have he : 2 * Real.arctan u = θ := by
    rw [hu, Real.arctan_tan (by linarith) (by linarith)]; ring
  have hu0 : 0 ≤ u := Real.tan_nonneg_of_nonneg_of_le_pi_div_two (by linarith) (by linarith)
  refine ⟨u, hu0, ?_, he⟩
  have hs : Real.sin θ ≤ Real.sin (Real.pi / 4) :=
    Real.sin_le_sin_of_le_of_le_pi_div_two (by linarith) (by linarith) h1
  have hc : Real.cos (Real.pi / 4) ≤ Real.cos θ :=
    Real.cos_le_cos_of_nonneg_of_le_pi h0 (by linarith) h1
  rw [Real.sin_pi_div_four] at hs
  rw [Real.cos_pi_div_four] at hc
  rw [← he, sin_two_arctan] at hs
  rw [← he, cos_two_arctan] at hc
  have hN : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have key : 2 * u ≤ 1 - u ^ 2 := by
    have := le_trans hs hc
    rwa [div_le_div_iff_of_pos_right hN] at this
  nlinarith

/-- The D4 data check: every point has `X ≤ Mq`, and its images under `x ↦ Mq − x` and
`x ↔ y`, with the same weight, are points. -/
def d4Check (Mq : ℕ) (pts : PTree) : Bool :=
  pts.all fun e => Nat.ble e.1 Mq && pts.mem (Mq - e.1, e.2.1, e.2.2) && pts.mem (e.2.1, e.1, e.2.2)

/-- **The generic lower bound.**  A point certificate `pts` (entries `(X, Y, w)`: the point
`(X/D, Y/D)` with weight `w/W`), D4-invariant in `[0, Mq/D]²`, with total weight `< n`, whose
box tree covers the D4 fundamental region `[0, Mq/(2D)]² × {u ∈ [0, 29/70]}`, proves
`s(n) ≥ Mq/D`.  (`hk`: some `k × k` grid holds `n` squares, so `s(n)` is an infimum over a
non-empty set.) -/
theorem le_minSide (D S Mq R Um W : ℕ) (pts : PTree) (hD : 0 < D) (hS : 0 < S) (hR : 0 < R)
    (hUm : 29 * R ≤ 70 * Um) (hnd : pts.toList.Nodup) (hsym : d4Check Mq pts = true)
    (hcov : Cov D S Mq R W pts.toList 0 (Mq * S - Mq * S / 2) 0 (Mq * S - Mq * S / 2) 0 Um)
    (n k : ℕ) (hn : pts.wsum < n * W) (hk : n ≤ k * k) :
    (Mq : ℝ) / D ≤ minSide n := by
  classical
  set m : ℝ := (Mq : ℝ) / D with hm
  set E := pts.toList.toFinset with hE
  let wt : ℕ × ℕ × ℕ → ℝ := fun e => (e.2.2 : ℝ) / W
  have hW : 0 < W := by
    rcases Nat.eq_zero_or_pos W with h | h
    · rw [h] at hn; simp at hn
    · exact h
  have hWr : (0 : ℝ) < W := by exact_mod_cast hW
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hSr : (0 : ℝ) < S := by exact_mod_cast hS
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  -- the data facts
  have entry_ok : ∀ e ∈ E, e.1 ≤ Mq ∧ (Mq - e.1, e.2.1, e.2.2) ∈ E ∧ (e.2.1, e.1, e.2.2) ∈ E := by
    intro e he
    have h2 := (PTree.all_iff _ pts).mp hsym e (List.mem_toFinset.mp he)
    simp only [Bool.and_eq_true, Nat.ble_eq] at h2
    exact ⟨h2.1.1, List.mem_toFinset.mpr (PTree.mem_sound _ _ h2.1.2),
      List.mem_toFinset.mpr (PTree.mem_sound _ _ h2.2)⟩
  have hinv : D4Inv m (coverA E (ptR D)) (coverW E (ptR D) wt) := by
    refine D4Inv_cover m E (ptR D) wt (fun e => (Mq - e.1, e.2.1, e.2.2))
      (fun e => (e.2.1, e.1, e.2.2)) ?_ ?_
    · intro e he
      obtain ⟨hx, hgX, _⟩ := entry_ok e he
      refine ⟨hgX, ?_, rfl, ?_⟩
      · simp only [ptR, reflX, hm, Nat.cast_sub hx]
        ext
        · simp only; field_simp
        · simp
      · obtain ⟨a, b, c⟩ := e
        simp only at hx ⊢
        ext <;> simp; omega
    · intro e he
      exact ⟨(entry_ok e he).2.2, rfl, rfl, rfl⟩
  have hw : ∀ a ∈ coverA E (ptR D), 0 ≤ coverW E (ptR D) wt a := by
    intro a _
    unfold coverW
    exact Finset.sum_nonneg fun e _ => by positivity
  -- the region statement, from the box tree
  have hreg : ∀ (c : ℝ × ℝ) (θ : ℝ), c.1 ∈ Set.Icc 0 (m / 2) → c.2 ∈ Set.Icc 0 (m / 2) →
      θ ∈ Set.Icc 0 (Real.pi / 4) → sq c θ 1 ⊆ box m →
        1 ≤ ∑ a ∈ (coverA E (ptR D)).filter (fun a => a ∈ sq c θ 1), coverW E (ptR D) wt a := by
    intro c θ h1 h2 hθ hsub
    rw [sum_filter_coverA]
    obtain ⟨u, hu0, hu1, rfl⟩ := exists_u_of_theta' hθ
    have hhalf : m / 2 ≤ (((Mq * S - Mq * S / 2 : ℕ) : ℝ)) / (D * S) := by
      have h2 : Mq * S ≤ 2 * (Mq * S - Mq * S / 2) := by omega
      have h2r : ((Mq * S : ℕ) : ℝ) ≤ 2 * ((Mq * S - Mq * S / 2 : ℕ) : ℝ) := by exact_mod_cast h2
      rw [hm, div_div, div_le_div_iff₀ (by positivity) (by positivity)]
      push_cast at h2r
      nlinarith
    have hU : ((0 : ℕ) : ℝ) / R ≤ u := by simpa using hu0
    have hU1 : u ≤ (Um : ℝ) / R := by
      rw [le_div_iff₀ hRr]
      have : (29 : ℝ) * R ≤ 70 * Um := by exact_mod_cast hUm
      nlinarith
    have hc := hcov c u (by simpa using h1.1) (le_trans h1.2 hhalf) (by simpa using h2.1)
      (le_trans h2.2 hhalf) hU hU1 hsub
    have e : ∑ e ∈ E.filter (fun e => ptR D e ∈ sq c (2 * Real.arctan u) 1), wt e
        = (∑ e ∈ E.filter (fun e => ptR D e ∈ sq c (2 * Real.arctan u) 1), (e.2.2 : ℝ)) / W := by
      rw [Finset.sum_div]
    rw [e, le_div_iff₀ hWr, one_mul]
    exact hc
  have hcover := d4_reduction m _ _ hinv hreg
  -- the total weight
  have htot : ∑ a ∈ coverA E (ptR D), coverW E (ptR D) wt a < n := by
    rw [sum_coverA]
    have hs : ∑ e ∈ E, e.2.2 = pts.wsum := by
      rw [hE, List.sum_toFinset _ hnd, PTree.wsum_eq]
    have hsr : ∑ e ∈ E, (e.2.2 : ℝ) = pts.wsum := by rw [← hs]; push_cast; rfl
    have hlt : (pts.wsum : ℝ) < n * W := by exact_mod_cast hn
    change ∑ e ∈ E, (e.2.2 : ℝ) / W < n
    rw [← Finset.sum_div, hsr, div_lt_iff₀ hWr]
    exact hlt
  -- `s(n)`
  have hne : ({s | Packs n s} : Set ℝ).Nonempty := ⟨k, packs_grid k n hk⟩
  refine le_csInf hne fun s hs => ?_
  by_contra hlt
  exact not_packs_of_cover m _ _ hw hcover n htot (not_le.mp hlt) hs

end final

end BoxTree

end SquarePacking
