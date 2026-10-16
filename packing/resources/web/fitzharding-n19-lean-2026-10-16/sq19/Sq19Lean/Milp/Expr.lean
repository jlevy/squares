import Sq19Lean.Milp.Taylor
import Sq17Lean.PropagationTrig

/-!
# Expressions in the square angles and their Taylor enclosures

`Ex` is a small expression language: rational constants, `cos (M π/4 + θ_s)`, `sin (M π/4 + θ_s)`,
sums, products and negation. `Ex.real θ e` is its value; `Ex.tf T H e` is a first-order Taylor
form on the angle box `θ_s = T.cen s + δ_s`, `|δ_s| ≤ H s`. `Ex.tf_encl` proves the enclosure for
every expression. `cos T.cen`, `sin T.cen` come from the 17 project's rational Taylor polynomials
(`cosTaylor_error`, `sinTaylor_error`).
-/
namespace Sq19.Milp
open Sq17.Propagation

/-! ## Bounds for small angles -/

theorem abs_cos_sub_one_le (x : ℝ) : |Real.cos x - 1| ≤ x^2/2 := by
  have h1 := Real.one_sub_sq_div_two_le_cos (x := x)
  have h2 := Real.cos_le_one x
  rw [abs_le]; constructor <;> nlinarith [sq_nonneg x]

theorem abs_sin_sub_self_le (x : ℝ) : |Real.sin x - x| ≤ |x|^3/6 := by
  have pos : ∀ y : ℝ, 0 ≤ y → |Real.sin y - y| ≤ y^3/6 := by
    intro y hy
    rcases eq_or_lt_of_le hy with h | h
    · subst h; simp
    · have h1 := Real.sin_le hy
      have h2 := Real.sin_gt_sub_cube h
      rw [abs_le]; constructor <;> linarith
  rcases le_total 0 x with hx | hx
  · rw [abs_of_nonneg hx]; exact pos x hx
  · have h := pos (-x) (by linarith)
    rw [Real.sin_neg] at h
    rw [abs_of_nonpos hx]
    have e : -Real.sin x - -x = -(Real.sin x - x) := by ring
    rw [e, abs_neg] at h
    exact h

/-- Remainder of the first-order expansion of `cos` and `sin` on `|δ| ≤ H`. -/
def trigRem (H : ℚ) : ℚ := H^2/2 + H^3/6

theorem trig_rem_bound (a b δ : ℝ) (H : ℚ) (ha : |a| ≤ 1) (hb : |b| ≤ 1) (hδ : |δ| ≤ H) :
    |a * (Real.cos δ - 1) + b * (Real.sin δ - δ)| ≤ (trigRem H : ℝ) := by
  have h1 := abs_cos_sub_one_le δ
  have h2 := abs_sin_sub_self_le δ
  have hH : 0 ≤ (H : ℝ) := (abs_nonneg _).trans hδ
  have e1 : δ^2 ≤ (H:ℝ)^2 := by rw [← sq_abs]; exact pow_le_pow_left₀ (abs_nonneg _) hδ 2
  have e2 : |δ|^3 ≤ (H:ℝ)^3 := pow_le_pow_left₀ (abs_nonneg _) hδ 3
  have t1 : |a * (Real.cos δ - 1)| ≤ δ^2/2 := by
    rw [abs_mul]; nlinarith [abs_nonneg a, abs_nonneg (Real.cos δ - 1)]
  have t2 : |b * (Real.sin δ - δ)| ≤ |δ|^3/6 := by
    rw [abs_mul]; nlinarith [abs_nonneg b, abs_nonneg (Real.sin δ - δ)]
  simp only [trigRem]; push_cast
  calc _ ≤ |a * (Real.cos δ - 1)| + |b * (Real.sin δ - δ)| := abs_add_le _ _
    _ ≤ _ := by linarith

/-! ## Multiples of π/4 -/

/-- An enclosure of `√2/2`. -/
def s2 : Iv := ⟨7071067811865475/10000000000000000, 7071067811865476/10000000000000000⟩

theorem mem_s2 : Iv.mem (Real.sqrt 2 / 2) s2 := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hp : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
  simp only [Iv.mem, s2]; push_cast
  constructor <;> nlinarith

def ivOne : Iv := Iv.pt 1
def ivZero : Iv := Iv.pt 0
def ivMOne : Iv := Iv.pt (-1)

/-- Enclosures of `(cos (r π/4), sin (r π/4))` for `r < 8`. -/
def quarterTab (r : ℕ) : Iv × Iv :=
  match r with
  | 0 => (ivOne, ivZero)
  | 1 => (s2, s2)
  | 2 => (ivZero, ivOne)
  | 3 => (s2.neg, s2)
  | 4 => (ivMOne, ivZero)
  | 5 => (s2.neg, s2.neg)
  | 6 => (ivZero, ivMOne)
  | _ => (s2, s2.neg)

theorem quarter_mem (M : ℕ) :
    Iv.mem (Real.cos (M * Real.pi / 4)) (quarterTab (M % 8)).1 ∧
    Iv.mem (Real.sin (M * Real.pi / 4)) (quarterTab (M % 8)).2 := by
  have hM : (M : ℝ) * Real.pi / 4 = ((M % 8 : ℕ) : ℝ) * Real.pi / 4 + ((M / 8 : ℕ) : ℝ) * (2 * Real.pi) := by
    have := Nat.mod_add_div M 8
    have e : (M : ℝ) = ((M % 8 : ℕ) : ℝ) + 8 * ((M / 8 : ℕ) : ℝ) := by exact_mod_cast this.symm
    rw [e]; ring
  rw [hM, Real.cos_add_nat_mul_two_pi, Real.sin_add_nat_mul_two_pi]
  have hr : M % 8 < 8 := Nat.mod_lt _ (by norm_num)
  have hs := mem_s2
  have hsn := Iv.mem_neg hs
  have p4 : Real.pi / 4 + Real.pi / 2 = 3 * Real.pi / 4 := by ring
  have c3 : Real.cos (3 * Real.pi / 4) = -(Real.sqrt 2 / 2) := by
    rw [← p4, Real.cos_add_pi_div_two, Real.sin_pi_div_four]
  have s3 : Real.sin (3 * Real.pi / 4) = Real.sqrt 2 / 2 := by
    rw [← p4, Real.sin_add_pi_div_two, Real.cos_pi_div_four]
  interval_cases h : M % 8
  · simp [quarterTab, ivOne, ivZero, Iv.pt, Iv.mem]
  · simp only [Nat.cast_one, one_mul, quarterTab, Real.cos_pi_div_four, Real.sin_pi_div_four]
    exact ⟨hs, hs⟩
  · have e : ((2:ℕ):ℝ) * Real.pi / 4 = Real.pi / 2 := by push_cast; ring
    rw [e, Real.cos_pi_div_two, Real.sin_pi_div_two]
    simp [quarterTab, ivOne, ivZero, Iv.pt, Iv.mem]
  · have e : ((3:ℕ):ℝ) * Real.pi / 4 = 3 * Real.pi / 4 := by push_cast; ring
    rw [e, c3, s3]; exact ⟨hsn, hs⟩
  · have e : ((4:ℕ):ℝ) * Real.pi / 4 = Real.pi := by push_cast; ring
    rw [e, Real.cos_pi, Real.sin_pi]
    simp [quarterTab, ivMOne, ivZero, Iv.pt, Iv.mem]
  · have e : ((5:ℕ):ℝ) * Real.pi / 4 = Real.pi / 4 + Real.pi := by push_cast; ring
    rw [e, Real.cos_add_pi, Real.sin_add_pi, Real.cos_pi_div_four, Real.sin_pi_div_four]
    exact ⟨hsn, hsn⟩
  · have e : ((6:ℕ):ℝ) * Real.pi / 4 = Real.pi / 2 + Real.pi := by push_cast; ring
    rw [e, Real.cos_add_pi, Real.sin_add_pi, Real.cos_pi_div_two, Real.sin_pi_div_two]
    simp [quarterTab, ivMOne, ivZero, Iv.pt, Iv.mem]
  · have e : ((7:ℕ):ℝ) * Real.pi / 4 = 3 * Real.pi / 4 + Real.pi := by push_cast; ring
    rw [e, Real.cos_add_pi, Real.sin_add_pi, c3, s3, neg_neg]
    exact ⟨hs, hsn⟩

/-! ## Trig table of the box centres -/

/-- Degree of the Taylor polynomials for the box centres. -/
def taylorDeg : ℕ := 20

def cosIv (x : ℚ) : Iv :=
  ⟨rdn (cosTaylor taylorDeg x - trigRemainder taylorDeg x),
   rup (cosTaylor taylorDeg x + trigRemainder taylorDeg x)⟩
def sinIv (x : ℚ) : Iv :=
  ⟨rdn (sinTaylor taylorDeg x - trigRemainder taylorDeg x),
   rup (sinTaylor taylorDeg x + trigRemainder taylorDeg x)⟩

/-- Box centres `cen s` with enclosures of `cos (cen s)` and `sin (cen s)`. -/
structure Trig where
  cen : ℕ → ℚ
  tab : List (Iv × Iv)

/-- Tabulated enclosure of `cos (cen s)` (computed directly off the table). -/
def Trig.cc (T : Trig) (s : ℕ) : Iv :=
  if s < T.tab.length then (T.tab.getD s (ivOne, ivZero)).1 else cosIv (T.cen s)
def Trig.sc (T : Trig) (s : ℕ) : Iv :=
  if s < T.tab.length then (T.tab.getD s (ivOne, ivZero)).2 else sinIv (T.cen s)

def Trig.Valid (T : Trig) : Prop :=
  ∀ s, Iv.mem (Real.cos (T.cen s)) (T.cc s) ∧ Iv.mem (Real.sin (T.cen s)) (T.sc s)

theorem mem_cosIv (x : ℚ) : Iv.mem (Real.cos x) (cosIv x) := by
  have he := abs_le.mp (cosTaylor_error taylorDeg x)
  have rem : (trigRemainder taylorDeg x : ℝ) = |(x : ℝ)|^(taylorDeg+1) / ((taylorDeg+1).factorial : ℝ) := by
    simp [trigRemainder]
  have h1 := rdn_le_real (cosTaylor taylorDeg x - trigRemainder taylorDeg x)
  have h2 := le_rup_real (cosTaylor taylorDeg x + trigRemainder taylorDeg x)
  push_cast at h1 h2
  rw [rem] at h1 h2
  exact ⟨by simp only [cosIv]; linarith [he.1], by simp only [cosIv]; linarith [he.2]⟩

theorem mem_sinIv (x : ℚ) : Iv.mem (Real.sin x) (sinIv x) := by
  have he := abs_le.mp (sinTaylor_error taylorDeg x)
  have rem : (trigRemainder taylorDeg x : ℝ) = |(x : ℝ)|^(taylorDeg+1) / ((taylorDeg+1).factorial : ℝ) := by
    simp [trigRemainder]
  have h1 := rdn_le_real (sinTaylor taylorDeg x - trigRemainder taylorDeg x)
  have h2 := le_rup_real (sinTaylor taylorDeg x + trigRemainder taylorDeg x)
  push_cast at h1 h2
  rw [rem] at h1 h2
  exact ⟨by simp only [sinIv]; linarith [he.1], by simp only [sinIv]; linarith [he.2]⟩

/-- The trig table of a list of centres (index = list position). -/
def Trig.ofCentres (cen : ℕ → ℚ) (n : ℕ) : Trig :=
  ⟨cen, (List.range n).map (fun s => (cosIv (cen s), sinIv (cen s)))⟩

theorem Trig.ofCentres_valid (cen : ℕ → ℚ) (n : ℕ) : (Trig.ofCentres cen n).Valid := by
  intro s
  simp only [Trig.cc, Trig.sc, Trig.ofCentres, List.length_map, List.length_range]
  split_ifs with h
  · have e : ((List.range n).map (fun s => (cosIv (cen s), sinIv (cen s)))).getD s (ivOne, ivZero)
        = (cosIv (cen s), sinIv (cen s)) := by
      simp [List.getD_eq_getElem?_getD, h]
    rw [e]; exact ⟨mem_cosIv _, mem_sinIv _⟩
  · exact ⟨mem_cosIv _, mem_sinIv _⟩

/-- Enclosures of `cos (M π/4 + cen)`, `sin (M π/4 + cen)`. -/
def Trig.cosAt (T : Trig) (s M : ℕ) : Iv :=
  ((quarterTab (M % 8)).1.mul (T.cc s)).sub ((quarterTab (M % 8)).2.mul (T.sc s))
def Trig.sinAt (T : Trig) (s M : ℕ) : Iv :=
  ((quarterTab (M % 8)).2.mul (T.cc s)).add ((quarterTab (M % 8)).1.mul (T.sc s))

theorem Trig.mem_cosAt {T : Trig} (hT : T.Valid) (s M : ℕ) :
    Iv.mem (Real.cos (M * Real.pi / 4 + T.cen s)) (T.cosAt s M) := by
  rw [Real.cos_add]
  exact Iv.mem_sub (Iv.mem_mul (quarter_mem M).1 (hT s).1) (Iv.mem_mul (quarter_mem M).2 (hT s).2)

theorem Trig.mem_sinAt {T : Trig} (hT : T.Valid) (s M : ℕ) :
    Iv.mem (Real.sin (M * Real.pi / 4 + T.cen s)) (T.sinAt s M) := by
  rw [Real.sin_add]
  exact Iv.mem_add (Iv.mem_mul (quarter_mem M).2 (hT s).1) (Iv.mem_mul (quarter_mem M).1 (hT s).2)

/-! ## Taylor forms of `cos`, `sin` of a square angle -/

def TF.cosA (T : Trig) (H : ℕ → ℚ) (s M : ℕ) : TF :=
  ⟨(T.cosAt s M).widen (trigRem (H s) + (T.sinAt s M).rad * H s), lsingle s (-(T.sinAt s M).mid)⟩
def TF.sinA (T : Trig) (H : ℕ → ℚ) (s M : ℕ) : TF :=
  ⟨(T.sinAt s M).widen (trigRem (H s) + (T.cosAt s M).rad * H s), lsingle s (T.cosAt s M).mid⟩

private theorem abs_le_one_of_mem {x : ℝ} (h : |x| ≤ 1) : |x| ≤ 1 := h

theorem TF.encl_cosA {T : Trig} (hT : T.Valid) (H : ℕ → ℚ) (s M : ℕ) :
    (TF.cosA T H s M).Encl H (fun δ => Real.cos (M * Real.pi / 4 + (T.cen s + δ s))) := by
  intro δ hδ
  set α := M * Real.pi / 4 + (T.cen s : ℝ)
  have hc := T.mem_cosAt hT s M
  have hs := T.mem_sinAt hT s M
  have hr := Iv.abs_sub_mid hs
  have hR := trig_rem_bound (Real.cos α) (-Real.sin α) (δ s) (H s) (Real.abs_cos_le_one _)
    (by rw [abs_neg]; exact Real.abs_sin_le_one _) (hδ s)
  have hlin : |((T.sinAt s M).mid - Real.sin α) * δ s| ≤ ((T.sinAt s M).rad : ℝ) * H s := by
    rw [abs_mul, abs_sub_comm]
    exact mul_le_mul hr (hδ s) (abs_nonneg _) ((abs_nonneg _).trans hr)
  have htot : |Real.cos α * (Real.cos (δ s) - 1) + -Real.sin α * (Real.sin (δ s) - δ s) +
      ((T.sinAt s M).mid - Real.sin α) * δ s| ≤
      ((trigRem (H s) + (T.sinAt s M).rad * H s : ℚ) : ℝ) := by
    push_cast; exact (abs_add_le _ _).trans (add_le_add hR hlin)
  have h := Iv.mem_widen hc htot
  simp only [TF.cosA, linEval_lsingle]
  convert h using 1
  have e : M * Real.pi / 4 + ((T.cen s : ℝ) + δ s) = α + δ s := by simp only [α]; ring
  rw [e, Real.cos_add]; push_cast; ring

theorem TF.encl_sinA {T : Trig} (hT : T.Valid) (H : ℕ → ℚ) (s M : ℕ) :
    (TF.sinA T H s M).Encl H (fun δ => Real.sin (M * Real.pi / 4 + (T.cen s + δ s))) := by
  intro δ hδ
  set α := M * Real.pi / 4 + (T.cen s : ℝ)
  have hc := T.mem_cosAt hT s M
  have hs := T.mem_sinAt hT s M
  have hr := Iv.abs_sub_mid hc
  have hR := trig_rem_bound (Real.sin α) (Real.cos α) (δ s) (H s) (Real.abs_sin_le_one _)
    (Real.abs_cos_le_one _) (hδ s)
  have hlin : |(Real.cos α - (T.cosAt s M).mid) * δ s| ≤ ((T.cosAt s M).rad : ℝ) * H s := by
    rw [abs_mul]
    exact mul_le_mul hr (hδ s) (abs_nonneg _) ((abs_nonneg _).trans hr)
  have htot : |Real.sin α * (Real.cos (δ s) - 1) + Real.cos α * (Real.sin (δ s) - δ s) +
      (Real.cos α - (T.cosAt s M).mid) * δ s| ≤
      ((trigRem (H s) + (T.cosAt s M).rad * H s : ℚ) : ℝ) := by
    push_cast; exact (abs_add_le _ _).trans (add_le_add hR hlin)
  have h := Iv.mem_widen hs htot
  simp only [TF.sinA, linEval_lsingle]
  convert h using 1
  have e : M * Real.pi / 4 + ((T.cen s : ℝ) + δ s) = α + δ s := by simp only [α]; ring
  rw [e, Real.sin_add]; ring

/-! ## Expressions -/

inductive Ex where
  | c (q : ℚ)
  | cs (s M : ℕ)
  | sn (s M : ℕ)
  | add (a b : Ex)
  | mul (a b : Ex)
  | neg (a : Ex)
  | abs (a : Ex)

/-- Value at the relative angles `θ`. -/
noncomputable def Ex.real (θ : ℕ → ℝ) : Ex → ℝ
  | .c q => q
  | .cs s M => Real.cos (M * Real.pi / 4 + θ s)
  | .sn s M => Real.sin (M * Real.pi / 4 + θ s)
  | .add a b => a.real θ + b.real θ
  | .mul a b => a.real θ * b.real θ
  | .neg a => -a.real θ
  | .abs a => |a.real θ|

/-- Taylor form on the box `cen ± H`. -/
def Ex.tf (T : Trig) (H : ℕ → ℚ) : Ex → TF
  | .c q => TF.const (Iv.pt q)
  | .cs s M => TF.cosA T H s M
  | .sn s M => TF.sinA T H s M
  | .add a b => (a.tf T H).add (b.tf T H)
  | .mul a b => TF.mul H (a.tf T H) (b.tf T H)
  | .neg a => (a.tf T H).neg
  | .abs a =>
    let t := a.tf T H
    let r := t.range H
    if 0 ≤ r.lo then t else if r.hi ≤ 0 then t.neg else TF.const ⟨0, r.mag⟩

theorem Ex.tf_encl {T : Trig} (hT : T.Valid) (H : ℕ → ℚ) (e : Ex) :
    (e.tf T H).Encl H (fun δ => e.real (fun s => T.cen s + δ s) ) := by
  induction e with
  | c q => exact TF.encl_const H _ _ (fun _ => Iv.mem_pt q)
  | cs s M => exact TF.encl_cosA hT H s M
  | sn s M => exact TF.encl_sinA hT H s M
  | add a b ha hb => exact TF.encl_add ha hb
  | mul a b ha hb => exact TF.encl_mul ha hb
  | neg a ha => exact TF.encl_neg ha
  | abs a ha =>
    simp only [Ex.tf, Ex.real]
    split_ifs with h1 h2
    · intro δ hδ
      have hr := (TF.mem_range ha δ hδ).1
      have h1' : (0:ℝ) ≤ ((a.tf T H).range H).lo := by exact_mod_cast h1
      show Iv.mem (|a.real (fun s => (T.cen s : ℝ) + δ s)| - linEval (a.tf T H).l δ) (a.tf T H).c
      rw [abs_of_nonneg (by linarith)]
      exact ha δ hδ
    · intro δ hδ
      have hr := (TF.mem_range ha δ hδ).2
      have h2' : (((a.tf T H).range H).hi : ℝ) ≤ 0 := by exact_mod_cast h2
      show Iv.mem (|a.real (fun s => (T.cen s : ℝ) + δ s)| - linEval (a.tf T H).neg.l δ) (a.tf T H).neg.c
      rw [abs_of_nonpos (by linarith)]
      exact TF.encl_neg ha δ hδ
    · intro δ hδ
      have hm := Iv.abs_le_mag (TF.mem_range ha δ hδ)
      simp only [TF.const, linEval, sub_zero, Iv.mem, Rat.cast_zero]
      exact ⟨abs_nonneg _, hm⟩

/-- Sum of a list of expressions. -/
def Ex.sum : List Ex → Ex
  | [] => .c 0
  | e :: l => .add e (Ex.sum l)

theorem Ex.real_sum (θ : ℕ → ℝ) (l : List Ex) : (Ex.sum l).real θ = (l.map (·.real θ)).sum := by
  induction l with
  | nil => simp [Ex.sum, Ex.real]
  | cons e l ih => simp [Ex.sum, Ex.real, ih]

end Sq19.Milp
