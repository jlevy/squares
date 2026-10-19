import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Sq19Lean.Basic
import Sq19Lean.Wedge.BBPoly

/-!
# Case bb of the wedge lemma

`PhiBB a11 a13 a14` is `phi(a11, a13, a14, pa = 0, qa = 0, ...)` of `s19/tools/wedge_cases.c`:
anchors `P = (2, L-1)`, `Q = (L-1, L-1)`, floor `y = 2`, tilted squares 11, 13, 14 at angles
`b = pi/4 + a`, 13-14 separated by 14's normal and 13-11 by 11's normal. The bound is the least `L`
with `coefL * (L - 1) >= rest`. Main result `PhiBB_ge_side19`: on the capture ranges,
`side19 <= PhiBB`.
-/

namespace Sq19.Wedge

open Real

/-- `g(d) = (|cos d| + |sin d|) / 2`, the support of a unit square at relative angle `d`. -/
noncomputable def gk (d : ℝ) : ℝ := (|cos d| + |sin d|) / 2

/-- Coefficient of `L - 1` in case bb. -/
noncomputable def coefBB (a11 a14 : ℝ) : ℝ :=
  sin (π / 4 + a14) * (cos (π / 4 + a11) + sin (π / 4 + a11)) + cos (π / 4 + a11) * cos (π / 4 + a14)

/-- Constant side in case bb. -/
noncomputable def restBB (a11 a13 a14 : ℝ) : ℝ :=
  cos ((π / 4 + a14) - (π / 4 + a11)) * (2 + (|cos (π / 4 + a13)| + |sin (π / 4 + a13)|) / 2)
    + sin (π / 4 + a14) * (1 + gk ((π / 4 + a11) - (π / 4 + a13)))
    + cos (π / 4 + a11) * (2 * sin (π / 4 + a14) + 1 + gk ((π / 4 + a14) - (π / 4 + a13)))

/-- The case-bb wedge bound, exactly `phi(..., 0, 0, ...)` of `wedge_cases.c`. -/
noncomputable def PhiBB (a11 a13 a14 : ℝ) : ℝ := 1 + restBB a11 a13 a14 / coefBB a11 a14

/-- `sin x` lies between `x` and `0` for `|x| <= pi`. -/
theorem sin_between {x : ℝ} (h1 : -π ≤ x) (h2 : x ≤ π) : min x 0 ≤ sin x ∧ sin x ≤ max x 0 := by
  rcases le_total 0 x with hx | hx
  · exact ⟨le_trans (min_le_right _ _) (sin_nonneg_of_nonneg_of_le_pi hx h2),
      le_trans (sin_le hx) (le_max_left _ _)⟩
  · have := sin_le (neg_nonneg.2 hx)
    rw [sin_neg] at this
    exact ⟨le_trans (min_le_left _ _) (by linarith),
      le_trans (sin_nonpos_of_nonpos_of_neg_pi_le hx h1) (le_max_right _ _)⟩

theorem sin_lo {x lo : ℝ} (hlo : lo ≤ x) (hl : lo ≤ 0) (h1 : -π ≤ x) (h2 : x ≤ π) : lo ≤ sin x := by
  have h := (sin_between h1 h2).1
  rcases le_total x 0 with hx | hx
  · rw [min_eq_left hx] at h; linarith
  · rw [min_eq_right hx] at h; linarith

theorem sin_hi {x hi : ℝ} (hhi : x ≤ hi) (hh : 0 ≤ hi) (h1 : -π ≤ x) (h2 : x ≤ π) : sin x ≤ hi := by
  have h := (sin_between h1 h2).2
  rcases le_total x 0 with hx | hx
  · rw [max_eq_right hx] at h; linarith
  · rw [max_eq_left hx] at h; linarith

theorem cos_lo {x lo hi c : ℝ} (hlo : lo ≤ x) (hhi : x ≤ hi) (hc1 : c ≤ 1 - lo ^ 2 / 2)
    (hc2 : c ≤ 1 - hi ^ 2 / 2) (hl : lo ≤ 0) (hh : 0 ≤ hi) : c ≤ cos x := by
  have := one_sub_sq_div_two_le_cos (x := x)
  rcases le_total x 0 with hx | hx
  · nlinarith
  · nlinarith

theorem cos_pi4_add (x : ℝ) : cos (π / 4 + x) = √2 / 2 * (cos x - sin x) := by
  rw [cos_add, cos_pi_div_four, sin_pi_div_four]; ring

theorem sin_pi4_add (x : ℝ) : sin (π / 4 + x) = √2 / 2 * (cos x + sin x) := by
  rw [sin_add, cos_pi_div_four, sin_pi_div_four]; ring

/-- The algebraic reduction: `rest - (side19 - 1) coefL = (sqrt 2 / 2) Gbb`. -/
theorem bb_reduce (s C S cp sp cq sq ap aq : ℝ) (hs : s ^ 2 = 2) (hC : C ^ 2 + S ^ 2 = 1) :
    ((cp*cq + sp*sq) * (2 + s*C/2)
      + s/2*((C*cp - S*sp) + (S*cp + C*sp)) * (1 + (cq + aq)/2)
      + s/2*((C*cq - S*sq) - (S*cq + C*sq))
        * (2 * (s/2*((C*cp - S*sp) + (S*cp + C*sp))) + 1 + (cp + ap)/2))
    - (2 + 4 * s / 3) *
      (s/2*((C*cp - S*sp) + (S*cp + C*sp))
          * (s/2*((C*cq - S*sq) - (S*cq + C*sq)) + s/2*((C*cq - S*sq) + (S*cq + C*sq)))
        + s/2*((C*cq - S*sq) - (S*cq + C*sq)) * (s/2*((C*cp - S*sp) - (S*cp + C*sp))))
    = s / 2 * Gbb C S cp sp cq sq ap aq := by
  unfold Gbb
  linear_combination (-(3*C^2*cp*cq*s + 3*C^2*cp*cq - C^2*cp*s*sq + C^2*cq*s*sp + C^2*s*sp*sq
    + 3*C^2*sp*sq - 2*C*S*cp*s*sq - 2*C*S*cq*s*sp + S^2*cp*cq*s + 3*S^2*cp*cq - S^2*cp*s*sq
    + S^2*cq*s*sp + 3*S^2*s*sp*sq + 3*S^2*sp*sq)/3) * hs + (-2*(cp*cq + sp*sq)) * hC

set_option maxHeartbeats 2000000 in
/-- Case-bb wedge lemma on the capture ranges (radians, relative to 45 degrees):
`a11 in [-0.1661, 0.1140]`, `a13 in [-0.1377, 0.0082]`, `a14 in [-0.2292, 0.0082]`. -/
theorem PhiBB_ge_side19 {a11 a13 a14 : ℝ}
    (h11l : -1661/10000 ≤ a11) (h11h : a11 ≤ 1140/10000)
    (h13l : -1377/10000 ≤ a13) (h13h : a13 ≤ 82/10000)
    (h14l : -2292/10000 ≤ a14) (h14h : a14 ≤ 82/10000) :
    side19 ≤ PhiBB a11 a13 a14 := by
  have hpi := pi_gt_three
  have hs : √2 ^ 2 = 2 := sq_sqrt (by norm_num)
  have hs0 : 0 < √2 := by positivity
  have hC : cos a13 ^ 2 + sin a13 ^ 2 = 1 := by rw [add_comm]; exact sin_sq_add_cos_sq a13
  have hpp : cos (a14 - a13) ^ 2 + sin (a14 - a13) ^ 2 = 1 := by
    rw [add_comm]; exact sin_sq_add_cos_sq _
  have hqq : cos (a11 - a13) ^ 2 + sin (a11 - a13) ^ 2 = 1 := by
    rw [add_comm]; exact sin_sq_add_cos_sq _
  -- angle addition
  have c14 : cos a14 = cos a13 * cos (a14 - a13) - sin a13 * sin (a14 - a13) := by
    rw [← cos_add]; ring_nf
  have s14 : sin a14 = sin a13 * cos (a14 - a13) + cos a13 * sin (a14 - a13) := by
    rw [← sin_add]; ring_nf
  have c11 : cos a11 = cos a13 * cos (a11 - a13) - sin a13 * sin (a11 - a13) := by
    rw [← cos_add]; ring_nf
  have s11 : sin a11 = sin a13 * cos (a11 - a13) + cos a13 * sin (a11 - a13) := by
    rw [← sin_add]; ring_nf
  have d1 : (π / 4 + a14) - (π / 4 + a13) = a14 - a13 := by ring
  have d2 : (π / 4 + a11) - (π / 4 + a13) = a11 - a13 := by ring
  have d3 : (π / 4 + a14) - (π / 4 + a11) = (a14 - a13) - (a11 - a13) := by ring
  have cpq := cos_sub (a14 - a13) (a11 - a13)
  -- bounds
  have hCl : (9905/10000 : ℝ) ≤ cos a13 :=
    cos_lo h13l h13h (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have hCh : cos a13 ≤ 1 := cos_le_one _
  have hSl : (-1377/10000 : ℝ) ≤ sin a13 := sin_lo h13l (by norm_num) (by linarith) (by linarith)
  have hSh : sin a13 ≤ (82/10000 : ℝ) := sin_hi h13h (by norm_num) (by linarith) (by linarith)
  have hpl : (-2374/10000 : ℝ) ≤ a14 - a13 := by linarith
  have hph : a14 - a13 ≤ (1459/10000 : ℝ) := by linarith
  have hql : (-1743/10000 : ℝ) ≤ a11 - a13 := by linarith
  have hqh : a11 - a13 ≤ (2517/10000 : ℝ) := by linarith
  have hcpl : (9718/10000 : ℝ) ≤ cos (a14 - a13) :=
    cos_lo hpl hph (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have hcph : cos (a14 - a13) ≤ 1 := cos_le_one _
  have hspl : (-2374/10000 : ℝ) ≤ sin (a14 - a13) := sin_lo hpl (by norm_num) (by linarith) (by linarith)
  have hsph : sin (a14 - a13) ≤ (1459/10000 : ℝ) := sin_hi hph (by norm_num) (by linarith) (by linarith)
  have hcql : (9683/10000 : ℝ) ≤ cos (a11 - a13) :=
    cos_lo hql hqh (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have hcqh : cos (a11 - a13) ≤ 1 := cos_le_one _
  have hsql : (-1743/10000 : ℝ) ≤ sin (a11 - a13) := sin_lo hql (by norm_num) (by linarith) (by linarith)
  have hsqh : sin (a11 - a13) ≤ (2517/10000 : ℝ) := sin_hi hqh (by norm_num) (by linarith) (by linarith)
  -- bounds for 14 and 11 directly (for coefL > 0)
  have hC14 : (97/100 : ℝ) ≤ cos a14 :=
    cos_lo h14l h14h (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have hS14l : (-2292/10000 : ℝ) ≤ sin a14 := sin_lo h14l (by norm_num) (by linarith) (by linarith)
  have hS14h : sin a14 ≤ (82/10000 : ℝ) := sin_hi h14h (by norm_num) (by linarith) (by linarith)
  have hC11 : (98/100 : ℝ) ≤ cos a11 :=
    cos_lo h11l h11h (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  have hS11l : (-1661/10000 : ℝ) ≤ sin a11 := sin_lo h11l (by norm_num) (by linarith) (by linarith)
  have hS11h : sin a11 ≤ (1140/10000 : ℝ) := sin_hi h11h (by norm_num) (by linarith) (by linarith)
  -- coefL > 0
  have hcoef : 0 < coefBB a11 a14 := by
    unfold coefBB
    simp only [cos_pi4_add, sin_pi4_add]
    have h1 : 0 < cos a14 + sin a14 := by linarith
    have h2 : 0 < cos a11 := by linarith
    have h3 : 0 < cos a11 - sin a11 := by linarith
    have h4 : 0 < cos a14 - sin a14 := by linarith
    have : √2 / 2 * (cos a14 + sin a14) * (√2 / 2 * (cos a11 - sin a11) + √2 / 2 * (cos a11 + sin a11))
        + √2 / 2 * (cos a11 - sin a11) * (√2 / 2 * (cos a14 - sin a14))
        = √2 ^ 2 / 4 * (2 * ((cos a14 + sin a14) * cos a11)
          + (cos a11 - sin a11) * (cos a14 - sin a14)) := by
      ring
    rw [this]
    positivity
  -- reduce to Gbb >= 0
  unfold PhiBB
  have hsub : side19 = 1 + (2 + 4 * √2 / 3) := by rw [side19]; ring
  rw [hsub, add_le_add_iff_left, le_div_iff₀ hcoef, ← sub_nonneg]
  have hred := bb_reduce (√2) (cos a13) (sin a13) (cos (a14 - a13)) (sin (a14 - a13))
    (cos (a11 - a13)) (sin (a11 - a13)) |sin (a14 - a13)| |sin (a11 - a13)| hs hC
  have h13c : 0 ≤ √2 / 2 * (cos a13 - sin a13) := mul_nonneg (by positivity) (by linarith)
  have h13s : 0 ≤ √2 / 2 * (cos a13 + sin a13) := mul_nonneg (by positivity) (by linarith)
  have hrest : restBB a11 a13 a14 - (2 + 4 * √2 / 3) * coefBB a11 a14
      = √2 / 2 * Gbb (cos a13) (sin a13) (cos (a14 - a13)) (sin (a14 - a13))
          (cos (a11 - a13)) (sin (a11 - a13)) |sin (a14 - a13)| |sin (a11 - a13)| := by
    rw [← hred]
    unfold restBB coefBB gk
    rw [d1, d2, d3, cpq]
    simp only [cos_pi4_add, sin_pi4_add]
    rw [abs_of_nonneg h13c, abs_of_nonneg h13s, abs_of_pos (by linarith : 0 < cos (a14 - a13)),
      abs_of_pos (by linarith : 0 < cos (a11 - a13)), c14, s14, c11, s11]
    ring
  rw [hrest]
  apply mul_nonneg (by positivity)
  rcases le_total 0 (sin (a14 - a13)) with hP | hP <;>
    rcases le_total 0 (sin (a11 - a13)) with hQ | hQ
  · rw [abs_of_nonneg hP, abs_of_nonneg hQ]
    exact Gbb_nonneg_pp hC hpp hqq (by linarith) hCh hSl (by linarith) (by linarith) hcph hP (by linarith)
      hcql hcqh hQ (by linarith)
  · rw [abs_of_nonneg hP, abs_of_nonpos hQ]
    exact Gbb_nonneg_pm hC hpp hqq (by linarith) hCh hSl (by linarith) (by linarith) hcph hP (by linarith)
      hcql hcqh hQ (by linarith)
  · rw [abs_of_nonpos hP, abs_of_nonneg hQ]
    exact Gbb_nonneg_mp hC hpp hqq (by linarith) hCh hSl (by linarith) (by linarith) hcph hP (by linarith)
      hcql hcqh hQ (by linarith)
  · rw [abs_of_nonpos hP, abs_of_nonpos hQ]
    exact Gbb_nonneg_mm hC hpp hqq (by linarith) hCh hSl (by linarith) (by linarith) hcph hP (by linarith)
      hcql hcqh hQ (by linarith)

end Sq19.Wedge
