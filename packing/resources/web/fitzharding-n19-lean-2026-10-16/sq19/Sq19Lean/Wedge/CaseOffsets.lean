import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Sq19Lean.Basic
import Sq19Lean.Wedge.CaseBB
import Sq19Lean.Wedge.Cases
import Sq19Lean.Wedge.OffsetAB
import Sq19Lean.Wedge.OffsetBA
import Sq19Lean.Wedge.OffsetAA

/-!
# The wedge lemma for all four owner cases

On the capture box `a11 in [-0.1661, 0.1140]`, `a13 in [-0.1377, 0.0082]`, `a14 in [-0.2292, 0.0082]`
and with offset ranges `o1 in [0.155, 0.293]`, `o2 in [-0.133, 0.0365]`, every owner case
of the wedge bound is at least `side19`. In particular `wedge_hull` covers all three tilted angles
in [-0.0082, 0.0082] and the offset ranges needed by the full capture hull.
What this does not cover: the derivation of the offset ranges from the capture region, the anchors,
feature validity and capture itself (see `s19/ENDGAME.md`).
-/

set_option linter.unusedVariables false

namespace Sq19.Wedge

open Real

set_option maxHeartbeats 4000000 in
/-- Owner case ab (`pa = true`, `qa = false`) on the capture box with the widened offset ranges. -/
theorem PhiCase_ab_ge_side19 {a11 a13 a14 o1 o2 : ℝ}
    (h11l : -1661/10000 ≤ a11) (h11h : a11 ≤ 1140/10000)
    (h13l : -1377/10000 ≤ a13) (h13h : a13 ≤ 82/10000)
    (h14l : -2292/10000 ≤ a14) (h14h : a14 ≤ 82/10000)
    (ho1l : 155/1000 ≤ o1) (ho1h : o1 ≤ 293/1000) :
    side19 ≤ PhiCase true false a11 a13 a14 o1 o2 := by
  have hs : √2 ^ 2 = 2 := sq_sqrt (by norm_num)
  have hs0 : 0 < √2 := by positivity
  obtain ⟨hCl, hSl, hSh, hcpl, hspl, hsph, hcql, hsql, hsqh, hC14, hS14l, hS14h, hC11, hS11l, hS11h⟩ :=
    capture_facts h11l h11h h13l h13h h14l h14h
  obtain ⟨c14, s14, c11, s11⟩ := angle_add_facts a11 a13 a14
  have hC : cos a13 ^ 2 + sin a13 ^ 2 = 1 := by rw [add_comm]; exact sin_sq_add_cos_sq a13
  have hpp : cos (a14 - a13) ^ 2 + sin (a14 - a13) ^ 2 = 1 := by
    rw [add_comm]; exact sin_sq_add_cos_sq _
  have hqq : cos (a11 - a13) ^ 2 + sin (a11 - a13) ^ 2 = 1 := by
    rw [add_comm]; exact sin_sq_add_cos_sq _
  have hcp0 : 0 < cos (a14 - a13) := by linarith
  have hcq0 : 0 < cos (a11 - a13) := by linarith
  have d1 : (π / 4 + a14) - (π / 4 + a13) = a14 - a13 := by ring
  have d2 : (π / 4 + a11) - (π / 4 + a13) = a11 - a13 := by ring
  have dd : (π / 4 + a13) - (π / 4 + a11) = -(a11 - a13) := by ring
  have hcoef : 0 < coefC true false a11 a13 a14 := by
    have e : coefC true false a11 a13 a14 = √2 ^ 2 / 4 * (2 * ((cos a13 + sin a13) * cos a11)
        + (cos a11 - sin a11) * (cos a13 - sin a13)) := by
      simp only [coefC, f1C, f2C, Bool.cond_true, Bool.cond_false, cos_pi4_add, sin_pi4_add]
      ring
    rw [e]
    have h1 : 0 < cos a13 + sin a13 := by linarith
    have h2 : 0 < cos a11 := by linarith
    have h3 : 0 < cos a11 - sin a11 := by linarith
    have h4 : 0 < cos a13 - sin a13 := by linarith
    exact mul_pos (by positivity) (add_pos (mul_pos two_pos (mul_pos h1 h2)) (mul_pos h3 h4))
  unfold PhiCase
  have hsub : side19 = 1 + (2 + 4 * √2 / 3) := by rw [side19]; ring
  rw [hsub, add_le_add_iff_left, le_div_iff₀ hcoef, ← sub_nonneg]
  have hmult : 0 < cos (a14 - a13) := by positivity
  have hred := reduce_ab (√2) (cos a13) (sin a13) (cos (a14 - a13)) (sin (a14 - a13))
    (cos (a11 - a13)) (sin (a11 - a13)) (cos (a14 - a13))⁻¹ (cos (a11 - a13))⁻¹ o1 o2
    |sin (a14 - a13)| |sin (a11 - a13)| (inv_mul_cancel₀ hcp0.ne') (inv_mul_cancel₀ hcq0.ne') hs
    (sin_sq_add_cos_sq _) (sin_sq_add_cos_sq _) (sin_sq_add_cos_sq _)
  have h13c : 0 ≤ √2 / 2 * (cos a13 - sin a13) := mul_nonneg (by positivity) (by linarith)
  have h13s : 0 ≤ √2 / 2 * (cos a13 + sin a13) := mul_nonneg (by positivity) (by linarith)
  have hrest : (restC true false a11 a13 a14 o1 o2 - (2 + 4 * √2 / 3) * coefC true false a11 a13 a14) * cos (a14 - a13)
      = √2 / 2 * Gab (cos a13) (sin a13) (cos (a14 - a13)) (sin (a14 - a13))
          (cos (a11 - a13)) (sin (a11 - a13)) o1 o2 |sin (a14 - a13)| |sin (a11 - a13)| := by
    rw [← hred]
    simp only [restC, coefC, A1C, A2C, f1C, f2C, ownerA, gk, Bool.cond_true, Bool.cond_false]
    simp only [d1, d2, dd, cos_neg]
    simp only [cos_pi4_add, sin_pi4_add, tan_eq_sin_div_cos]
    simp only [abs_of_nonneg h13c, abs_of_nonneg h13s, abs_of_pos hcp0, abs_of_pos hcq0, c14, s14, c11, s11]
    ring
  have hG := Gab_nonneg (o1 := o1) (o2 := o2) hC hpp hqq (by linarith) (cos_le_one _) (by linarith) (by linarith)
    (by linarith) (cos_le_one _) (by linarith) (by linarith)
    (by linarith) (cos_le_one _) (by linarith) (by linarith) (by linarith) (by linarith)
  have : 0 ≤ (restC true false a11 a13 a14 o1 o2 - (2 + 4 * √2 / 3) * coefC true false a11 a13 a14) * cos (a14 - a13) := by
    rw [hrest]; exact mul_nonneg (by positivity) hG
  exact (mul_nonneg_iff_of_pos_right hmult).1 this

set_option maxHeartbeats 4000000 in
/-- Owner case ba (`pa = false`, `qa = true`) on the capture box with the widened offset ranges. -/
theorem PhiCase_ba_ge_side19 {a11 a13 a14 o1 o2 : ℝ}
    (h11l : -1661/10000 ≤ a11) (h11h : a11 ≤ 1140/10000)
    (h13l : -1377/10000 ≤ a13) (h13h : a13 ≤ 82/10000)
    (h14l : -2292/10000 ≤ a14) (h14h : a14 ≤ 82/10000)
    (ho2l : -133/1000 ≤ o2) (ho2h : o2 ≤ 365/10000) :
    side19 ≤ PhiCase false true a11 a13 a14 o1 o2 := by
  have hs : √2 ^ 2 = 2 := sq_sqrt (by norm_num)
  have hs0 : 0 < √2 := by positivity
  obtain ⟨hCl, hSl, hSh, hcpl, hspl, hsph, hcql, hsql, hsqh, hC14, hS14l, hS14h, hC11, hS11l, hS11h⟩ :=
    capture_facts h11l h11h h13l h13h h14l h14h
  obtain ⟨c14, s14, c11, s11⟩ := angle_add_facts a11 a13 a14
  have hC : cos a13 ^ 2 + sin a13 ^ 2 = 1 := by rw [add_comm]; exact sin_sq_add_cos_sq a13
  have hpp : cos (a14 - a13) ^ 2 + sin (a14 - a13) ^ 2 = 1 := by
    rw [add_comm]; exact sin_sq_add_cos_sq _
  have hqq : cos (a11 - a13) ^ 2 + sin (a11 - a13) ^ 2 = 1 := by
    rw [add_comm]; exact sin_sq_add_cos_sq _
  have hcp0 : 0 < cos (a14 - a13) := by linarith
  have hcq0 : 0 < cos (a11 - a13) := by linarith
  have d1 : (π / 4 + a14) - (π / 4 + a13) = a14 - a13 := by ring
  have d2 : (π / 4 + a11) - (π / 4 + a13) = a11 - a13 := by ring
  have dd : (π / 4 + a14) - (π / 4 + a13) = a14 - a13 := by ring
  have hcoef : 0 < coefC false true a11 a13 a14 := by
    have e : coefC false true a11 a13 a14 = √2 ^ 2 / 4 * (2 * ((cos a14 + sin a14) * cos a13)
        + (cos a13 - sin a13) * (cos a14 - sin a14)) := by
      simp only [coefC, f1C, f2C, Bool.cond_true, Bool.cond_false, cos_pi4_add, sin_pi4_add]
      ring
    rw [e]
    have h1 : 0 < cos a14 + sin a14 := by linarith
    have h2 : 0 < cos a13 := by linarith
    have h3 : 0 < cos a13 - sin a13 := by linarith
    have h4 : 0 < cos a14 - sin a14 := by linarith
    exact mul_pos (by positivity) (add_pos (mul_pos two_pos (mul_pos h1 h2)) (mul_pos h3 h4))
  unfold PhiCase
  have hsub : side19 = 1 + (2 + 4 * √2 / 3) := by rw [side19]; ring
  rw [hsub, add_le_add_iff_left, le_div_iff₀ hcoef, ← sub_nonneg]
  have hmult : 0 < cos (a11 - a13) := by positivity
  have hred := reduce_ba (√2) (cos a13) (sin a13) (cos (a14 - a13)) (sin (a14 - a13))
    (cos (a11 - a13)) (sin (a11 - a13)) (cos (a14 - a13))⁻¹ (cos (a11 - a13))⁻¹ o1 o2
    |sin (a14 - a13)| |sin (a11 - a13)| (inv_mul_cancel₀ hcp0.ne') (inv_mul_cancel₀ hcq0.ne') hs
    (sin_sq_add_cos_sq _) (sin_sq_add_cos_sq _) (sin_sq_add_cos_sq _)
  have h13c : 0 ≤ √2 / 2 * (cos a13 - sin a13) := mul_nonneg (by positivity) (by linarith)
  have h13s : 0 ≤ √2 / 2 * (cos a13 + sin a13) := mul_nonneg (by positivity) (by linarith)
  have hrest : (restC false true a11 a13 a14 o1 o2 - (2 + 4 * √2 / 3) * coefC false true a11 a13 a14) * cos (a11 - a13)
      = √2 / 2 * Gba (cos a13) (sin a13) (cos (a14 - a13)) (sin (a14 - a13))
          (cos (a11 - a13)) (sin (a11 - a13)) o1 o2 |sin (a14 - a13)| |sin (a11 - a13)| := by
    rw [← hred]
    simp only [restC, coefC, A1C, A2C, f1C, f2C, ownerA, gk, Bool.cond_true, Bool.cond_false]
    simp only [d1, d2, dd]
    simp only [cos_pi4_add, sin_pi4_add, tan_eq_sin_div_cos]
    simp only [abs_of_nonneg h13c, abs_of_nonneg h13s, abs_of_pos hcp0, abs_of_pos hcq0, c14, s14, c11, s11]
    ring
  have hG := Gba_nonneg (o1 := o1) (o2 := o2) hC hpp hqq (by linarith) (cos_le_one _) (by linarith) (by linarith)
    (by linarith) (cos_le_one _) (by linarith) (by linarith)
    (by linarith) (cos_le_one _) (by linarith) (by linarith) (by linarith) (by linarith)
  have : 0 ≤ (restC false true a11 a13 a14 o1 o2 - (2 + 4 * √2 / 3) * coefC false true a11 a13 a14) * cos (a11 - a13) := by
    rw [hrest]; exact mul_nonneg (by positivity) hG
  exact (mul_nonneg_iff_of_pos_right hmult).1 this

set_option maxHeartbeats 4000000 in
/-- Owner case aa (`pa = true`, `qa = true`) on the capture box with the widened offset ranges. -/
theorem PhiCase_aa_ge_side19 {a11 a13 a14 o1 o2 : ℝ}
    (h11l : -1661/10000 ≤ a11) (h11h : a11 ≤ 1140/10000)
    (h13l : -1377/10000 ≤ a13) (h13h : a13 ≤ 82/10000)
    (h14l : -2292/10000 ≤ a14) (h14h : a14 ≤ 82/10000)
    (ho1l : 155/1000 ≤ o1) (ho1h : o1 ≤ 293/1000)
    (ho2l : -133/1000 ≤ o2) (ho2h : o2 ≤ 365/10000) :
    side19 ≤ PhiCase true true a11 a13 a14 o1 o2 := by
  have hs : √2 ^ 2 = 2 := sq_sqrt (by norm_num)
  have hs0 : 0 < √2 := by positivity
  obtain ⟨hCl, hSl, hSh, hcpl, hspl, hsph, hcql, hsql, hsqh, hC14, hS14l, hS14h, hC11, hS11l, hS11h⟩ :=
    capture_facts h11l h11h h13l h13h h14l h14h
  obtain ⟨c14, s14, c11, s11⟩ := angle_add_facts a11 a13 a14
  have hC : cos a13 ^ 2 + sin a13 ^ 2 = 1 := by rw [add_comm]; exact sin_sq_add_cos_sq a13
  have hpp : cos (a14 - a13) ^ 2 + sin (a14 - a13) ^ 2 = 1 := by
    rw [add_comm]; exact sin_sq_add_cos_sq _
  have hqq : cos (a11 - a13) ^ 2 + sin (a11 - a13) ^ 2 = 1 := by
    rw [add_comm]; exact sin_sq_add_cos_sq _
  have hcp0 : 0 < cos (a14 - a13) := by linarith
  have hcq0 : 0 < cos (a11 - a13) := by linarith
  have d1 : (π / 4 + a14) - (π / 4 + a13) = a14 - a13 := by ring
  have d2 : (π / 4 + a11) - (π / 4 + a13) = a11 - a13 := by ring
  have dd : (π / 4 + a13) - (π / 4 + a13) = 0 := by ring
  have hcoef : 0 < coefC true true a11 a13 a14 := by
    have e : coefC true true a11 a13 a14 = √2 ^ 2 / 4 * (2 * ((cos a13 + sin a13) * cos a13)
        + (cos a13 - sin a13) * (cos a13 - sin a13)) := by
      simp only [coefC, f1C, f2C, Bool.cond_true, Bool.cond_false, cos_pi4_add, sin_pi4_add]
      ring
    rw [e]
    have h1 : 0 < cos a13 + sin a13 := by linarith
    have h2 : 0 < cos a13 := by linarith
    have h3 : 0 < cos a13 - sin a13 := by linarith
    have h4 : 0 < cos a13 - sin a13 := by linarith
    exact mul_pos (by positivity) (add_pos (mul_pos two_pos (mul_pos h1 h2)) (mul_pos h3 h4))
  unfold PhiCase
  have hsub : side19 = 1 + (2 + 4 * √2 / 3) := by rw [side19]; ring
  rw [hsub, add_le_add_iff_left, le_div_iff₀ hcoef, ← sub_nonneg]
  have hmult : 0 < (cos (a14 - a13) * cos (a11 - a13)) := by positivity
  have hred := reduce_aa (√2) (cos a13) (sin a13) (cos (a14 - a13)) (sin (a14 - a13))
    (cos (a11 - a13)) (sin (a11 - a13)) (cos (a14 - a13))⁻¹ (cos (a11 - a13))⁻¹ o1 o2
    |sin (a14 - a13)| |sin (a11 - a13)| (inv_mul_cancel₀ hcp0.ne') (inv_mul_cancel₀ hcq0.ne') hs
    (sin_sq_add_cos_sq _) (sin_sq_add_cos_sq _) (sin_sq_add_cos_sq _)
  have h13c : 0 ≤ √2 / 2 * (cos a13 - sin a13) := mul_nonneg (by positivity) (by linarith)
  have h13s : 0 ≤ √2 / 2 * (cos a13 + sin a13) := mul_nonneg (by positivity) (by linarith)
  have hrest : (restC true true a11 a13 a14 o1 o2 - (2 + 4 * √2 / 3) * coefC true true a11 a13 a14) * (cos (a14 - a13) * cos (a11 - a13))
      = √2 / 2 * Gaa (cos a13) (sin a13) (cos (a14 - a13)) (sin (a14 - a13))
          (cos (a11 - a13)) (sin (a11 - a13)) o1 o2 |sin (a14 - a13)| |sin (a11 - a13)| := by
    rw [← hred]
    simp only [restC, coefC, A1C, A2C, f1C, f2C, ownerA, gk, Bool.cond_true, Bool.cond_false]
    simp only [d1, d2, dd, cos_zero]
    simp only [cos_pi4_add, sin_pi4_add, tan_eq_sin_div_cos]
    simp only [abs_of_nonneg h13c, abs_of_nonneg h13s, abs_of_pos hcp0, abs_of_pos hcq0, c14, s14, c11, s11]
    ring
  have hG := Gaa_nonneg (o1 := o1) (o2 := o2) hC hpp hqq (by linarith) (cos_le_one _) (by linarith) (by linarith)
    (by linarith) (cos_le_one _) (by linarith) (by linarith)
    (by linarith) (cos_le_one _) (by linarith) (by linarith) (by linarith) (by linarith) (by linarith) (by linarith)
  have : 0 ≤ (restC true true a11 a13 a14 o1 o2 - (2 + 4 * √2 / 3) * coefC true true a11 a13 a14) * (cos (a14 - a13) * cos (a11 - a13)) := by
    rw [hrest]; exact mul_nonneg (by positivity) hG
  exact (mul_nonneg_iff_of_pos_right hmult).1 this

/-- The wedge lemma, all four owner cases, on the capture box with the widened offset ranges. -/
theorem wedge_case_ge_side19 (pa qa : Bool) {a11 a13 a14 o1 o2 : ℝ}
    (h11l : -1661/10000 ≤ a11) (h11h : a11 ≤ 1140/10000)
    (h13l : -1377/10000 ≤ a13) (h13h : a13 ≤ 82/10000)
    (h14l : -2292/10000 ≤ a14) (h14h : a14 ≤ 82/10000)
    (ho1l : 155/1000 ≤ o1) (ho1h : o1 ≤ 293/1000)
    (ho2l : -133/1000 ≤ o2) (ho2h : o2 ≤ 365/10000) :
    side19 ≤ PhiCase pa qa a11 a13 a14 o1 o2 := by
  cases pa <;> cases qa
  · rw [PhiCase_false_false]; exact PhiBB_ge_side19 h11l h11h h13l h13h h14l h14h
  · exact PhiCase_ba_ge_side19 h11l h11h h13l h13h h14l h14h ho2l ho2h
  · exact PhiCase_ab_ge_side19 h11l h11h h13l h13h h14l h14h ho1l ho1h
  · exact PhiCase_aa_ge_side19 h11l h11h h13l h13h h14l h14h ho1l ho1h ho2l ho2h

/-- Legacy record-piece interface, now allowing a13 and a14 through +0.0082.
The symmetric cube is covered by `wedge_record_cube` below. -/
theorem wedge_record_piece (pa qa : Bool) {a11 a13 a14 o1 o2 : ℝ}
    (h11 : |a11| ≤ 73/10000) (h13l : -73/10000 ≤ a13) (h13h : a13 ≤ 82/10000)
    (h14l : -73/10000 ≤ a14) (h14h : a14 ≤ 82/10000)
    (ho1l : 155/1000 ≤ o1) (ho1h : o1 ≤ 293/1000)
    (ho2l : -133/1000 ≤ o2) (ho2h : o2 ≤ 365/10000) :
    side19 ≤ PhiCase pa qa a11 a13 a14 o1 o2 := by
  obtain ⟨h11l, h11h⟩ := abs_le.1 h11
  exact wedge_case_ge_side19 pa qa (by linarith) (by linarith) (by linarith) h13h
    (by linarith) h14h ho1l ho1h ho2l ho2h

/-- Full capture-hull interface. All three tilted-angle offsets lie in ±0.0082;
the second tangential offset may be positive, up to 0.0365. The broader theorem
above supplies spare room on the remaining boundaries. These are bounds on the
wedge expression, not a derivation of the enclosures from a packing. -/
theorem wedge_hull (pa qa : Bool) {a11 a13 a14 o1 o2 : ℝ}
    (h11 : |a11| ≤ 82/10000) (h13 : |a13| ≤ 82/10000) (h14 : |a14| ≤ 82/10000)
    (ho1l : 1589/10000 ≤ o1) (ho1h : o1 ≤ 2893/10000)
    (ho2l : -1322/10000 ≤ o2) (ho2h : o2 ≤ 365/10000) :
    side19 ≤ PhiCase pa qa a11 a13 a14 o1 o2 := by
  obtain ⟨h11l, h11h⟩ := abs_le.mp h11
  obtain ⟨h13l, h13h⟩ := abs_le.mp h13
  obtain ⟨h14l, h14h⟩ := abs_le.mp h14
  apply wedge_case_ge_side19 pa qa <;> linarith

/-- The full symmetric record-piece cube, without the former positive-angle cuts. -/
theorem wedge_record_cube (pa qa : Bool) {a11 a13 a14 o1 o2 : ℝ}
    (h11 : |a11| ≤ 73/10000) (h13 : |a13| ≤ 73/10000) (h14 : |a14| ≤ 73/10000)
    (ho1l : 155/1000 ≤ o1) (ho1h : o1 ≤ 293/1000)
    (ho2l : -133/1000 ≤ o2) (ho2h : o2 ≤ 365/10000) :
    side19 ≤ PhiCase pa qa a11 a13 a14 o1 o2 := by
  obtain ⟨h11l, h11h⟩ := abs_le.mp h11
  obtain ⟨h13l, h13h⟩ := abs_le.mp h13
  obtain ⟨h14l, h14h⟩ := abs_le.mp h14
  apply wedge_case_ge_side19 pa qa <;> linarith

end Sq19.Wedge
