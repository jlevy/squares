import Sqpack.BernsteinZ

/-!
# Rational functions of `u` with a known denominator (for Lemma E's vertex bounds)

At a vertex `v(u) = (X(u)/Δ(u), Y(u)/Δ(u))` of Lemma E every quantity is a rational function of
`u = tan(θ/2)` whose denominator is a product of powers of `Δ`, `C = 1 − u²`, `S = 2u`, `N = 1 + u²`
and a positive integer (`sin θ = S/N`, `cos θ = C/N`).  An `RF` stores the numerator (an integer
polynomial, `BernZ.Poly`) and the exponents; sums align the exponents, so no polynomial division is
ever needed and degrees stay small.  On `0 < u < 1` the factors `C`, `S`, `N` are positive, so the
sign of an `RF` is the sign of its numerator times `sign(Δ)^e` (`nonneg_of_checkRF`).
-/

namespace SquarePacking

namespace RatU

open BernZ

/-- `C = 1 − u²`, `S = 2u`, `N = 1 + u²`. -/
def Cp : Poly := [1, 0, -1]
def Sp : Poly := [0, 2]
def Np : Poly := [1, 0, 1]

lemma eval_Cp (u : ℝ) : eval Cp u = 1 - u ^ 2 := by simp [Cp]; ring
lemma eval_Sp (u : ℝ) : eval Sp u = 2 * u := by simp [Sp]; ring
lemma eval_Np (u : ℝ) : eval Np u = 1 + u ^ 2 := by simp [Np]; ring

/-- `pᵐ`. -/
def ppow (p : Poly) : ℕ → Poly
  | 0 => [1]
  | n + 1 => mul p (ppow p n)

lemma eval_ppow (p : Poly) (u : ℝ) : ∀ n, eval (ppow p n) u = eval p u ^ n
  | 0 => by simp [ppow]
  | n + 1 => by rw [ppow, eval_mul, eval_ppow p u n, pow_succ, mul_comm]

/-- `num / (Δ^e · C^i · S^j · N^k · d)`. -/
structure RF where
  num : Poly
  e : ℕ
  i : ℕ
  j : ℕ
  k : ℕ
  d : ℕ

/-- The denominator's value, `δ` standing for `Δ(u)`. -/
noncomputable def den (r : RF) (δ u : ℝ) : ℝ :=
  δ ^ r.e * (1 - u ^ 2) ^ r.i * (2 * u) ^ r.j * (1 + u ^ 2) ^ r.k * r.d

noncomputable def RF.eval (r : RF) (δ u : ℝ) : ℝ := BernZ.eval r.num u / den r δ u

/-- The constant `n / d`. -/
def RF.const (n : ℤ) (d : ℕ) : RF := ⟨[n], 0, 0, 0, 0, d⟩

/-- Multiply the numerator by `Δ^a C^b S^c N^g m` (raising the exponents accordingly). -/
def raise (Δ : Poly) (r : RF) (a b c g m : ℕ) : RF :=
  ⟨mul (smul (m : ℤ) r.num) (mul (ppow Δ a) (mul (ppow Cp b) (mul (ppow Sp c) (ppow Np g)))),
    r.e + a, r.i + b, r.j + c, r.k + g, r.d * m⟩

/-- The sum, over the common denominator (the constants aligned to their least common multiple). -/
def RF.add (Δ : Poly) (r s : RF) : RF :=
  let e := max r.e s.e; let i := max r.i s.i; let j := max r.j s.j; let k := max r.k s.k
  let l := Nat.lcm r.d s.d
  let r' := raise Δ r (e - r.e) (i - r.i) (j - r.j) (k - r.k) (l / r.d)
  let s' := raise Δ s (e - s.e) (i - s.i) (j - s.j) (k - s.k) (l / s.d)
  ⟨BernZ.add r'.num s'.num, e, i, j, k, l⟩

lemma RF.add_d (Δ : Poly) {r s : RF} (hr : r.d ≠ 0) (hs : s.d ≠ 0) : (RF.add Δ r s).d ≠ 0 :=
  Nat.lcm_ne_zero hr hs

def RF.mul (r s : RF) : RF := ⟨BernZ.mul r.num s.num, r.e + s.e, r.i + s.i, r.j + s.j, r.k + s.k, r.d * s.d⟩

def RF.neg (r : RF) : RF := ⟨smul (-1) r.num, r.e, r.i, r.j, r.k, r.d⟩

/-- The admissible values: `0 < u < 1`, `δ ≠ 0`. -/
structure Ok (δ u : ℝ) : Prop where
  hu0 : 0 < u
  hu1 : u < 1
  hδ : δ ≠ 0

lemma den_ne_zero {r : RF} {δ u : ℝ} (h : Ok δ u) (hd : r.d ≠ 0) : den r δ u ≠ 0 := by
  have h1 : (0 : ℝ) < 1 - u ^ 2 := by nlinarith [h.hu0, h.hu1]
  have h2 : (0 : ℝ) < 2 * u := by linarith [h.hu0]
  have h3 : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have h4 : (0 : ℝ) < r.d := by exact_mod_cast Nat.pos_of_ne_zero hd
  unfold den
  exact mul_ne_zero (mul_ne_zero (mul_ne_zero (mul_ne_zero (pow_ne_zero _ h.hδ)
    (pow_pos h1 _).ne') (pow_pos h2 _).ne') (pow_pos h3 _).ne') h4.ne'

lemma eval_raise {Δ : Poly} {r : RF} {δ u : ℝ} (h : Ok δ u) (hΔ : BernZ.eval Δ u = δ)
    (hd : r.d ≠ 0) {a b c g m : ℕ} (hm : m ≠ 0) :
    (raise Δ r a b c g m).eval δ u = r.eval δ u := by
  have hm' : (m : ℝ) ≠ 0 := by exact_mod_cast hm
  have h1 : (1 : ℝ) - u ^ 2 ≠ 0 := by nlinarith [h.hu0, h.hu1]
  have h2 : (2 : ℝ) * u ≠ 0 := by linarith [h.hu0]
  have h3 : (1 : ℝ) + u ^ 2 ≠ 0 := by positivity
  have hδ := h.hδ
  have hd' : (r.d : ℝ) ≠ 0 := by exact_mod_cast hd
  have hu : u ≠ 0 := h.hu0.ne'
  simp only [RF.eval, raise, den, eval_mul, eval_smul, eval_ppow, eval_Cp, eval_Sp, eval_Np, hΔ,
    pow_add]
  push_cast
  field_simp

lemma eval_add {Δ : Poly} {r s : RF} {δ u : ℝ} (h : Ok δ u) (hΔ : BernZ.eval Δ u = δ)
    (hr : r.d ≠ 0) (hs : s.d ≠ 0) :
    (RF.add Δ r s).eval δ u = r.eval δ u + s.eval δ u := by
  set l := Nat.lcm r.d s.d with hl
  have hl0 : 0 < l := Nat.lcm_pos (Nat.pos_of_ne_zero hr) (Nat.pos_of_ne_zero hs)
  have hmr : l / r.d ≠ 0 := (Nat.div_pos (Nat.le_of_dvd hl0 (Nat.dvd_lcm_left _ _))
    (Nat.pos_of_ne_zero hr)).ne'
  have hms : l / s.d ≠ 0 := (Nat.div_pos (Nat.le_of_dvd hl0 (Nat.dvd_lcm_right _ _))
    (Nat.pos_of_ne_zero hs)).ne'
  have cr : r.d * (l / r.d) = l := Nat.mul_div_cancel' (Nat.dvd_lcm_left _ _)
  have cs : s.d * (l / s.d) = l := Nat.mul_div_cancel' (Nat.dvd_lcm_right _ _)
  have e1 := eval_raise (r := r) (a := max r.e s.e - r.e) (b := max r.i s.i - r.i)
    (c := max r.j s.j - r.j) (g := max r.k s.k - r.k) h hΔ hr hmr
  have e2 := eval_raise (r := s) (a := max r.e s.e - s.e) (b := max r.i s.i - s.i)
    (c := max r.j s.j - s.j) (g := max r.k s.k - s.k) h hΔ hs hms
  rw [← e1, ← e2]
  simp only [RF.eval, RF.add, raise, den, BernZ.eval_add]
  have k1 : r.e + (max r.e s.e - r.e) = max r.e s.e := by omega
  have k2 : r.i + (max r.i s.i - r.i) = max r.i s.i := by omega
  have k3 : r.j + (max r.j s.j - r.j) = max r.j s.j := by omega
  have k4 : r.k + (max r.k s.k - r.k) = max r.k s.k := by omega
  have k5 : s.e + (max r.e s.e - s.e) = max r.e s.e := by omega
  have k6 : s.i + (max r.i s.i - s.i) = max r.i s.i := by omega
  have k7 : s.j + (max r.j s.j - s.j) = max r.j s.j := by omega
  have k8 : s.k + (max r.k s.k - s.k) = max r.k s.k := by omega
  rw [k1, k2, k3, k4, k5, k6, k7, k8, ← hl, cr, cs, add_div]

lemma eval_mul {r s : RF} {δ u : ℝ} (h : Ok δ u) (hr : r.d ≠ 0) (hs : s.d ≠ 0) :
    (RF.mul r s).eval δ u = r.eval δ u * s.eval δ u := by
  have a := den_ne_zero h hr
  have b := den_ne_zero h hs
  simp only [RF.eval, RF.mul, den, BernZ.eval_mul] at a b ⊢
  push_cast
  field_simp
  ring

lemma eval_neg (r : RF) (δ u : ℝ) : (RF.neg r).eval δ u = -r.eval δ u := by
  simp only [RF.eval, RF.neg, den, BernZ.eval_smul]; push_cast; ring

lemma eval_const (n : ℤ) (d : ℕ) (δ u : ℝ) : (RF.const n d).eval δ u = n / d := by
  simp [RF.eval, RF.const, den]

/-! ## The sign test -/

/-- `r ≥ 0` on the bin `[U0/R, U1/R]`, given that `Δ` has sign `σ` there (`σ = true`: positive):
the numerator times `σ^e` has non-negative Bernstein coefficients of degree `n`. -/
def checkRF (σ : Bool) (r : RF) (n U0 U1 R : ℕ) : Bool :=
  BernZ.check (if σ || r.e % 2 == 0 then r.num else smul (-1) r.num) n U0 U1 R

/-- `r ≥ 0` from the sign of its numerator (times `σ^e`). -/
lemma nonneg_of_snumP {σ : Bool} {r : RF} {δ u : ℝ} (h : Ok δ u) (hσ : if σ then 0 < δ else δ < 0)
    (hd : r.d ≠ 0) (hnum : 0 ≤ BernZ.eval (if σ || r.e % 2 == 0 then r.num else smul (-1) r.num) u) :
    0 ≤ r.eval δ u := by
  have h1 : (0 : ℝ) < 1 - u ^ 2 := by nlinarith [h.hu0, h.hu1]
  have h2 : (0 : ℝ) < 2 * u := by linarith [h.hu0]
  have h3 : (0 : ℝ) < 1 + u ^ 2 := by positivity
  have h4 : (0 : ℝ) < r.d := by exact_mod_cast Nat.pos_of_ne_zero hd
  have hrest : 0 < (1 - u ^ 2) ^ r.i * (2 * u) ^ r.j * (1 + u ^ 2) ^ r.k * (r.d : ℝ) := by positivity
  unfold RF.eval den
  rw [show δ ^ r.e * (1 - u ^ 2) ^ r.i * (2 * u) ^ r.j * (1 + u ^ 2) ^ r.k * (r.d : ℝ) =
    δ ^ r.e * ((1 - u ^ 2) ^ r.i * (2 * u) ^ r.j * (1 + u ^ 2) ^ r.k * r.d) by ring]
  by_cases hpos : σ = true ∨ r.e % 2 = 0
  · have hsel : (if σ || r.e % 2 == 0 then r.num else smul (-1) r.num) = r.num := by
      rcases hpos with hp | hp <;> simp [hp]
    rw [hsel] at hnum
    have hδe : 0 < δ ^ r.e := by
      rcases hpos with hp | hp
      · simp only [hp, if_true] at hσ; exact pow_pos hσ _
      · exact (Even.pow_pos (Nat.even_iff.mpr hp) h.hδ)
    exact div_nonneg hnum (mul_pos hδe hrest).le
  · simp only [not_or, Bool.not_eq_true] at hpos
    obtain ⟨hp1, hp2⟩ := hpos
    have hσf : σ = false := hp1
    have hsel : (if σ || r.e % 2 == 0 then r.num else smul (-1) r.num) = smul (-1) r.num := by
      simp [hσf, hp2]
    rw [hsel, eval_smul] at hnum
    simp only [hσf, Bool.false_eq_true, if_false] at hσ
    have hodd : Odd r.e := Nat.odd_iff.mpr (by omega)
    have hδe : δ ^ r.e < 0 := hodd.pow_neg hσ
    push_cast at hnum
    exact div_nonneg_of_nonpos (by linarith) (mul_neg_of_neg_of_pos hδe hrest).le

lemma nonneg_of_checkRF {σ : Bool} {r : RF} {n U0 U1 R : ℕ} (hc : checkRF σ r n U0 U1 R = true)
    (hR : 0 < R) {δ u : ℝ} (h : Ok δ u) (hσ : if σ then 0 < δ else δ < 0) (hd : r.d ≠ 0)
    (hu0 : (U0 : ℝ) / R ≤ u) (hu1 : u ≤ (U1 : ℝ) / R) : 0 ≤ r.eval δ u := by
  exact nonneg_of_snumP h hσ hd (BernZ.nonneg_of_check hc hR hu0 hu1)

end RatU

end SquarePacking
