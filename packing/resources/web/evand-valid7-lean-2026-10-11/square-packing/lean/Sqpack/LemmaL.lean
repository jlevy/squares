import Sqpack.ZMTreeM

/-!
# Lemma L (linear chord ends on an axis line), kernel form

`ZM_MIXED.md` §2, Lemma L, "general ends", Corollary L.  For an axis line (`x = K/Q` if `dir = 0`,
`y = K/Q` otherwise) and a pose box, the chord of the square on the line is bounded below at every
pose by `[b − y, a + x]`, where `a` (up end) and `b` (down end) are points certified for the *typed*
conditions and `x`, `y` are how far the chord ends move beyond them.  Each typed condition `k` is, along
the line, `G_k(t) = G_k(a) + σ_k(u) (t − a)` with slope `σ_k = ±4u` (type `S`) or `±2(1 − u²)` (type `C`),
so its threshold is `t_k = a − G_k(a)/σ_k`: a *rational function of `u`, affine in the centre*.  The
mass gained at the up end is at least `min(cap, s·x + i)` for an affine minorant `s x + i` (`s ≥ 0`) of
the gain function, i.e. `≥ min(cap, min_k (i + s (t_k − a)))`: a minimum of functions affine in the
centre.  Summed over lines and ends this is concave in the centre, so its minimum over the box is at
a corner (`concave_corners`); at a corner every option is `N(v)/σ̂(v)` with `N` quadratic in `v = R u`,
and the kernel checks the per-corner choices and slacks by the degree-4 Bernstein test of `ZMTree`.

This file: polynomials of degree `≤ 4` (`P5`), the rational inequality at a corner (`ratOk`), and the
concavity lemma.  The L-block itself is in `LBlock.lean`.
-/

namespace SquarePacking

namespace ZMTreeM

open BoxTree ZMTree

/-! ## 1.  Quartics in `v` -/

/-- A polynomial `p₀ + p₁ v + … + p₄ v⁴` with signed coefficients. -/
abbrev P5 := SP × SP × SP × SP × SP

def z0 : SP := (0, 0)

noncomputable def e5 (p : P5) (v : ℝ) : ℝ :=
  sv p.1 + sv p.2.1 * v + sv p.2.2.1 * v ^ 2 + sv p.2.2.2.1 * v ^ 3 + sv p.2.2.2.2 * v ^ 4

def p5add (p q : P5) : P5 :=
  (sadd p.1 q.1, sadd p.2.1 q.2.1, sadd p.2.2.1 q.2.2.1, sadd p.2.2.2.1 q.2.2.2.1,
    sadd p.2.2.2.2 q.2.2.2.2)
def p5neg (p : P5) : P5 := (sneg p.1, sneg p.2.1, sneg p.2.2.1, sneg p.2.2.2.1, sneg p.2.2.2.2)

@[simp] lemma e5_add (p q : P5) (v : ℝ) : e5 (p5add p q) v = e5 p v + e5 q v := by
  simp only [e5, p5add, sv_sadd]; ring
@[simp] lemma e5_neg (p : P5) (v : ℝ) : e5 (p5neg p) v = -e5 p v := by
  simp only [e5, p5neg, sv_sneg]; ring
@[simp] lemma e5_zero (v : ℝ) : e5 (z0, z0, z0, z0, z0) v = 0 := by
  simp [e5, z0, sv]

/-- The denominators: `1`, `4Rv` (type `S`: `4u`), `2(R² − v²)` (type `C`: `2(1 − u²)`), both. -/
noncomputable def fval (f R : ℕ) (v : ℝ) : ℝ :=
  match f with
  | 0 => 1
  | 1 => 4 * R * v
  | 2 => 2 * ((R : ℝ) ^ 2 - v ^ 2)
  | _ => 4 * R * v * (2 * ((R : ℝ) ^ 2 - v ^ 2))

/-- A quadratic `n₀ + n₁ v + n₂ v²` times the factor `f ∈ {1, S, C}`. -/
def tmul (f R : ℕ) (n : SP × SP × SP) : P5 :=
  match f with
  | 0 => (n.1, n.2.1, n.2.2, z0, z0)
  | 1 => (z0, sk (Nat.mul 4 R) n.1, sk (Nat.mul 4 R) n.2.1, sk (Nat.mul 4 R) n.2.2, z0)
  | _ => (sk (Nat.mul 2 (Nat.mul R R)) n.1, sk (Nat.mul 2 (Nat.mul R R)) n.2.1,
      ssub (sk (Nat.mul 2 (Nat.mul R R)) n.2.2) (sk 2 n.1), sneg (sk 2 n.2.1), sneg (sk 2 n.2.2))

/-- A constant times the factor `f ∈ {1, S, C, SC}`. -/
def cmul (f R : ℕ) (c : SP) : P5 :=
  match f with
  | 0 => (c, z0, z0, z0, z0)
  | 1 => (z0, sk (Nat.mul 4 R) c, z0, z0, z0)
  | 2 => (sk (Nat.mul 2 (Nat.mul R R)) c, z0, sneg (sk 2 c), z0, z0)
  | _ => (z0, sk (Nat.mul 8 (Nat.mul R (Nat.mul R R))) c, z0, sneg (sk (Nat.mul 8 R) c), z0)

lemma e5_tmul (f R : ℕ) (hf : f ≤ 2) (n : SP × SP × SP) (v : ℝ) :
    e5 (tmul f R n) v = fval f R v * (sv n.1 + sv n.2.1 * v + sv n.2.2 * v ^ 2) := by
  rcases f with _ | _ | _ | f
  · simp only [tmul, e5, fval, z0, sv]; push_cast; ring
  · simp only [tmul, e5, fval, z0, sv_sk, nat_mul_eq]; simp only [sv]; push_cast; ring
  · simp only [tmul, e5, fval, z0, sv_sk, sv_ssub, sv_sneg, nat_mul_eq]; simp only [sv]; push_cast
    ring
  · omega

lemma e5_cmul (f R : ℕ) (hf : f ≤ 3) (c : SP) (v : ℝ) :
    e5 (cmul f R c) v = fval f R v * sv c := by
  rcases f with _ | _ | _ | _ | f
  · simp only [cmul, e5, fval, z0, sv]; push_cast; ring
  · simp only [cmul, e5, fval, z0, sv_sk, nat_mul_eq]; simp only [sv]; push_cast; ring
  · simp only [cmul, e5, fval, z0, sv_sk, sv_sneg, nat_mul_eq]; simp only [sv]; push_cast; ring
  · simp only [cmul, e5, fval, z0, sv_sk, sv_sneg, nat_mul_eq]; simp only [sv]; push_cast; ring
  · omega

/-- The factors are positive on the bin: `S` needs `v > 0`, `C` needs `v < R`. -/
lemma fval_pos {f R : ℕ} {v : ℝ} (hR : 0 < R) (hf : f ≤ 3) (hS : f % 2 = 1 → 0 < v)
    (hC : 2 ≤ f → v < R) (hv : 0 ≤ v) : 0 < fval f R v := by
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  rcases f with _ | _ | _ | _ | f
  · simp [fval]
  · simp only [fval]; have := hS (by norm_num); positivity
  · simp only [fval]; have := hC (by norm_num); nlinarith
  · simp only [fval]
    have h1 := hS (by norm_num); have h2 := hC (by norm_num)
    have : 0 < 2 * ((R : ℝ) ^ 2 - v ^ 2) := by nlinarith
    positivity
  · omega

/-- The degree-4 Bernstein test `≤ 0`, read back. -/
lemma bOk5_e5 {p : P5} {U0 U1 : ℕ} (h : bOk5 p U0 U1 = true) (hU : U0 ≤ U1) {v : ℝ}
    (h0 : (U0 : ℝ) ≤ v) (h1 : v ≤ U1) : e5 p v ≤ 0 := by
  have := bOk_sound h hU h0 h1
  simpa [e5] using this

/-! ## 2.  Concave functions on a rectangle -/

/-- A minimum of affine functions of `(x, y)` is concave: its value at a convex combination is at
least the combination of the values (one coordinate at a time). -/
lemma min_affine_x {ι : Type*} (s : Finset ι) (hs : s.Nonempty) (K A B : ι → ℝ) {x0 x1 x y : ℝ}
    (hx0 : x0 ≤ x) (hx1 : x ≤ x1) :
    min (s.inf' hs fun i => K i + A i * x0 + B i * y) (s.inf' hs fun i => K i + A i * x1 + B i * y)
      ≤ s.inf' hs fun i => K i + A i * x + B i * y := by
  rcases eq_or_lt_of_le (le_trans hx0 hx1) with h | h
  · have : x = x0 := by linarith
    rw [this]; exact min_le_left _ _
  have hd : 0 < x1 - x0 := by linarith
  set l := (x1 - x) / (x1 - x0) with hl
  have hl0 : 0 ≤ l := div_nonneg (by linarith) hd.le
  have hl1 : l ≤ 1 := by rw [hl, div_le_one hd]; linarith
  have hxx : x = l * x0 + (1 - l) * x1 := by rw [hl]; field_simp; ring
  rw [Finset.le_inf'_iff]
  intro i hi
  have e : K i + A i * x + B i * y
      = l * (K i + A i * x0 + B i * y) + (1 - l) * (K i + A i * x1 + B i * y) := by
    rw [hxx]; ring
  rw [e]
  have h1 := Finset.inf'_le (fun i => K i + A i * x0 + B i * y) hi
  have h2 := Finset.inf'_le (fun i => K i + A i * x1 + B i * y) hi
  have m1 := min_le_left (s.inf' hs fun i => K i + A i * x0 + B i * y)
    (s.inf' hs fun i => K i + A i * x1 + B i * y)
  have m2 := min_le_right (s.inf' hs fun i => K i + A i * x0 + B i * y)
    (s.inf' hs fun i => K i + A i * x1 + B i * y)
  nlinarith [mul_le_mul_of_nonneg_left (le_trans m1 h1) hl0,
    mul_le_mul_of_nonneg_left (le_trans m2 h2) (by linarith : (0 : ℝ) ≤ 1 - l)]

/-- **Concave on a rectangle ⇒ minimum at a corner.**  A function `f` on the plane with
`min (f x₀ y) (f x₁ y) ≤ f x y` and the same in `y` is, on `[x₀,x₁]×[y₀,y₁]`, at least its smallest
corner value. -/
lemma concave_corners {f : ℝ → ℝ → ℝ} {x0 x1 y0 y1 x y : ℝ}
    (hxc : ∀ y', ∀ x', x0 ≤ x' → x' ≤ x1 → min (f x0 y') (f x1 y') ≤ f x' y')
    (hyc : ∀ x', ∀ y', y0 ≤ y' → y' ≤ y1 → min (f x' y0) (f x' y1) ≤ f x' y')
    (hx0 : x0 ≤ x) (hx1 : x ≤ x1) (hy0 : y0 ≤ y) (hy1 : y ≤ y1) {L : ℝ}
    (h00 : L ≤ f x0 y0) (h01 : L ≤ f x0 y1) (h10 : L ≤ f x1 y0) (h11 : L ≤ f x1 y1) :
    L ≤ f x y := by
  have a0 := hyc x0 y hy0 hy1
  have a1 := hyc x1 y hy0 hy1
  have b := hxc y x hx0 hx1
  have c0 : L ≤ f x0 y := le_trans (le_min h00 h01) a0
  have c1 : L ≤ f x1 y := le_trans (le_min h10 h11) a1
  exact le_trans (le_min c0 c1) b

end ZMTreeM

end SquarePacking
