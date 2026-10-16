import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds

/-!
# Rational intervals with outward rounding

Endpoints are rationals rounded outward to multiples of `2^-64`, which keeps denominators
bounded during long evaluations. `x ∈ᵢ I` means `I.lo ≤ x ≤ I.hi` for a real `x`.
-/
namespace Sq19.Milp

def prec : ℕ := 64

/-- Round down to the grid `2^-prec`. -/
def rdn (q : ℚ) : ℚ := (⌊q * 2^prec⌋ : ℚ) / 2^prec

/-- Round up to the grid `2^-prec`. -/
def rup (q : ℚ) : ℚ := (⌈q * 2^prec⌉ : ℚ) / 2^prec

theorem rdn_le (q : ℚ) : rdn q ≤ q := by
  unfold rdn
  rw [div_le_iff₀ (by positivity)]
  exact Int.floor_le _

theorem le_rup (q : ℚ) : q ≤ rup q := by
  unfold rup
  rw [le_div_iff₀ (by positivity)]
  exact Int.le_ceil _

theorem rdn_le_real (q : ℚ) : ((rdn q : ℚ) : ℝ) ≤ (q : ℝ) := by exact_mod_cast rdn_le q
theorem le_rup_real (q : ℚ) : (q : ℝ) ≤ ((rup q : ℚ) : ℝ) := by exact_mod_cast le_rup q

structure Iv where
  lo : ℚ
  hi : ℚ
deriving Repr

/-- Membership of a real number. -/
def Iv.mem (x : ℝ) (I : Iv) : Prop := (I.lo : ℝ) ≤ x ∧ x ≤ (I.hi : ℝ)

def Iv.pt (q : ℚ) : Iv := ⟨q, q⟩
def Iv.add (I J : Iv) : Iv := ⟨rdn (I.lo + J.lo), rup (I.hi + J.hi)⟩
def Iv.neg (I : Iv) : Iv := ⟨-I.hi, -I.lo⟩
def Iv.sub (I J : Iv) : Iv := I.add J.neg
def Iv.mul (I J : Iv) : Iv :=
  let a := I.lo * J.lo
  let b := I.lo * J.hi
  let c := I.hi * J.lo
  let d := I.hi * J.hi
  ⟨rdn (min (min a b) (min c d)), rup (max (max a b) (max c d))⟩
/-- Widen by `r` on both sides. -/
def Iv.widen (I : Iv) (r : ℚ) : Iv := ⟨rdn (I.lo - r), rup (I.hi + r)⟩
/-- An upper bound of `|x|` on the interval. -/
def Iv.mag (I : Iv) : ℚ := max |I.lo| |I.hi|
def Iv.mid (I : Iv) : ℚ := (I.lo + I.hi) / 2
def Iv.rad (I : Iv) : ℚ := (I.hi - I.lo) / 2

theorem Iv.mem_pt (q : ℚ) : Iv.mem (q : ℝ) (Iv.pt q) := ⟨le_rfl, le_rfl⟩

theorem Iv.mem_add {x y : ℝ} {I J : Iv} (hx : Iv.mem x I) (hy : Iv.mem y J) :
    Iv.mem (x + y) (I.add J) := by
  have h1 := rdn_le_real (I.lo + J.lo)
  have h2 := le_rup_real (I.hi + J.hi)
  push_cast at h1 h2
  exact ⟨by simp only [Iv.add]; linarith [hx.1, hy.1], by simp only [Iv.add]; linarith [hx.2, hy.2]⟩

theorem Iv.mem_neg {x : ℝ} {I : Iv} (hx : Iv.mem x I) : Iv.mem (-x) I.neg := by
  simp only [Iv.mem, Iv.neg, Rat.cast_neg]
  exact ⟨by linarith [hx.2], by linarith [hx.1]⟩

theorem Iv.mem_sub {x y : ℝ} {I J : Iv} (hx : Iv.mem x I) (hy : Iv.mem y J) :
    Iv.mem (x - y) (I.sub J) := by
  rw [sub_eq_add_neg]; exact Iv.mem_add hx (Iv.mem_neg hy)

private theorem mul_lb {a b c d x y : ℝ} (hx : a ≤ x ∧ x ≤ b) (hy : c ≤ y ∧ y ≤ d) :
    min (min (a*c) (a*d)) (min (b*c) (b*d)) ≤ x*y := by
  have h1 : min (a*c) (a*d) ≤ a*y := by
    rcases le_total 0 a with ha | ha
    · exact (min_le_left _ _).trans (mul_le_mul_of_nonneg_left hy.1 ha)
    · exact (min_le_right _ _).trans (mul_le_mul_of_nonpos_left hy.2 ha)
  have h2 : min (b*c) (b*d) ≤ b*y := by
    rcases le_total 0 b with hb | hb
    · exact (min_le_left _ _).trans (mul_le_mul_of_nonneg_left hy.1 hb)
    · exact (min_le_right _ _).trans (mul_le_mul_of_nonpos_left hy.2 hb)
  rcases le_total 0 y with hy0 | hy0
  · have : a*y ≤ x*y := mul_le_mul_of_nonneg_right hx.1 hy0
    exact (min_le_left _ _).trans (h1.trans this)
  · have : b*y ≤ x*y := mul_le_mul_of_nonpos_right hx.2 hy0
    exact (min_le_right _ _).trans (h2.trans this)

private theorem mul_ub {a b c d x y : ℝ} (hx : a ≤ x ∧ x ≤ b) (hy : c ≤ y ∧ y ≤ d) :
    x*y ≤ max (max (a*c) (a*d)) (max (b*c) (b*d)) := by
  have h1 : a*y ≤ max (a*c) (a*d) := by
    rcases le_total 0 a with ha | ha
    · exact (mul_le_mul_of_nonneg_left hy.2 ha).trans (le_max_right _ _)
    · exact (mul_le_mul_of_nonpos_left hy.1 ha).trans (le_max_left _ _)
  have h2 : b*y ≤ max (b*c) (b*d) := by
    rcases le_total 0 b with hb | hb
    · exact (mul_le_mul_of_nonneg_left hy.2 hb).trans (le_max_right _ _)
    · exact (mul_le_mul_of_nonpos_left hy.1 hb).trans (le_max_left _ _)
  rcases le_total 0 y with hy0 | hy0
  · have : x*y ≤ b*y := mul_le_mul_of_nonneg_right hx.2 hy0
    exact (this.trans h2).trans (le_max_right _ _)
  · have : x*y ≤ a*y := mul_le_mul_of_nonpos_right hx.1 hy0
    exact (this.trans h1).trans (le_max_left _ _)

theorem Iv.mem_mul {x y : ℝ} {I J : Iv} (hx : Iv.mem x I) (hy : Iv.mem y J) :
    Iv.mem (x * y) (I.mul J) := by
  have hl := mul_lb hx hy
  have hu := mul_ub hx hy
  have h1 := rdn_le_real (min (min (I.lo*J.lo) (I.lo*J.hi)) (min (I.hi*J.lo) (I.hi*J.hi)))
  have h2 := le_rup_real (max (max (I.lo*J.lo) (I.lo*J.hi)) (max (I.hi*J.lo) (I.hi*J.hi)))
  push_cast at h1 h2
  exact ⟨by simp only [Iv.mul]; linarith, by simp only [Iv.mul]; linarith⟩

theorem Iv.mem_widen {x e : ℝ} {I : Iv} {r : ℚ} (hx : Iv.mem x I) (he : |e| ≤ r) :
    Iv.mem (x + e) (I.widen r) := by
  have h1 := rdn_le_real (I.lo - r)
  have h2 := le_rup_real (I.hi + r)
  push_cast at h1 h2
  have := abs_le.mp he
  exact ⟨by simp only [Iv.widen]; linarith [hx.1], by simp only [Iv.widen]; linarith [hx.2]⟩

theorem Iv.abs_le_mag {x : ℝ} {I : Iv} (hx : Iv.mem x I) : |x| ≤ (I.mag : ℝ) := by
  simp only [Iv.mag, Rat.cast_max, Rat.cast_abs]
  rcases le_total 0 x with h | h
  · rw [abs_of_nonneg h]; exact (le_abs_self _ |>.trans' hx.2).trans (le_max_right _ _)
  · rw [abs_of_nonpos h]
    exact (neg_le_neg hx.1 |>.trans (neg_le_abs _)).trans (le_max_left _ _)

theorem Iv.abs_sub_mid {x : ℝ} {I : Iv} (hx : Iv.mem x I) : |x - I.mid| ≤ (I.rad : ℝ) := by
  simp only [Iv.mid, Iv.rad]; push_cast
  rw [abs_le]; constructor <;> linarith [hx.1, hx.2]

end Sq19.Milp
