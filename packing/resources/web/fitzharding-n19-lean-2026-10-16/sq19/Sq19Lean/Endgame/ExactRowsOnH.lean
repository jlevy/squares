import Sq19Lean.Endgame.RowsOnH

/-!
Exact 5–8 anchor support on each relative-angle sign cone. Keeping this term
preserves the first-order contribution lost by replacing support with 1/2.
-/
namespace Sq19.Endgame
open Sq19.Milp Sq19.Endgame.Hull

/-- Exact anchor support, with `bd` the sign of θ8−θ5. -/
def anchor58E (bd : Bool) : Ex :=
  .mul (.c (1/2)) (.add (cosD 8 0 5 0) (.mul (.c (sg bd)) (sinD 8 0 5 0)))

theorem supp_quarter (a b : ℝ) : supp a (b + Real.pi / 2) = supp a b := by
  unfold supp
  rw [show b + Real.pi / 2 - a = (b-a) + Real.pi / 2 by ring,
    Real.cos_add_pi_div_two, Real.sin_add_pi_div_two, abs_neg]
  ring

theorem supp_symm (a b : ℝ) : supp a b = supp b a := by
  unfold supp
  rw [show b-a = -(a-b) by ring, Real.cos_neg, Real.sin_neg, abs_neg]

section
variable {θ dx dy : ℕ → ℝ} {L : ℝ}

set_option maxRecDepth 100000 in
theorem anchor58E_real (hg : Good prob θ dx dy L) {bd : Bool}
    (hd : 0 ≤ (sg bd : ℝ) * (θ 8 - θ 5)) :
    (anchor58E bd).real θ = supp (angE θ 5 0) (angE θ 8 2) ∧
    (anchor58E bd).real θ = supp (angE θ 8 0) (angE θ 5 2) := by
  have hs := sin_orth2 hg (s := 8) (t := 5) (M := 0) (by simp) (by simp) hd
  have hc : 0 ≤ Real.cos (angE θ 8 0 - angE θ 5 0) := by
    rw [← cosD_real]
    exact nonneg_of_rngH hg (cosD 8 0 5 0) (by decide +kernel)
  have habs : |Real.sin (angE θ 8 0 - angE θ 5 0)| =
      (sg bd : ℝ) * Real.sin (angE θ 8 0 - angE θ 5 0) := by
    cases bd <;> simp [sg] at hs ⊢
    · exact hs
    · exact hs
  have hbase : (anchor58E bd).real θ = supp (angE θ 5 0) (angE θ 8 0) := by
    simp only [anchor58E, Ex.real, cosD_real, sinD_real, supp, abs_of_nonneg hc, habs]
    push_cast
    ring
  have a82 : angE θ 8 2 = angE θ 8 0 + Real.pi/2 := by simp [angE]; ring
  have a52 : angE θ 5 2 = angE θ 5 0 + Real.pi/2 := by simp [angE]; ring
  rw [a82, a52, supp_quarter, supp_quarter, ← supp_symm (angE θ 5 0) (angE θ 8 0)]
  exact ⟨hbase, hbase⟩

set_option maxRecDepth 100000 in
/-- F1, `θ8 ≥ 0`, 5-8 owned by 8, on H. -/
theorem F1rowPos8_exact_H (hg : Good prob θ dx dy L) (h58 : Sep (cH dx dy 4) (φH θ 4) (cH dx dy 2) (φH θ 2) 3)
    {b5 bd : Bool} (h5 : 0 ≤ (sg b5 : ℝ) * θ 5) (h8 : 0 ≤ θ 8) (hd : 0 ≤ (sg bd : ℝ) * (θ 8 - θ 5)) :
    (F1rowPos8 (absX 2).hi (sg b5, 1) (1, 1) (anchor58E bd)).Holds θ (cH dx dy 7).1 (cH dx dy 7).2 L := by
  have t0 := theta0 hg
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, t0]; ring
  have s5 := sin_orth hg (k := 5) (by simp) h5
  have c5 : 0 < Real.cos (θ 5) := by
    rw [← angE_axis θ 5]; exact pos_of_rngH hg (.cs 5 0) (by decide +kernel)
  have s8 := sin_orth hg (k := 8) (b := true) (by simp) (by simp [sg]; exact h8)
  simp only [sg, ↓reduceIte] at s8; push_cast at s8
  refine F1rowPos8_holds t0 (sep_8_13 hg) h58 (cxy_mem hg (i := 2) (by decide)).1.2
    (fit_walls hg (i := 2) (by decide)).2.2.1 (by rw [angE_axis]; linarith)
    (nonneg_of_rngH hg (.cs 8 0) (by decide +kernel)) ?_ (anchor58E_real hg hd).1.le ?_
  · show (suppE (sg b5) 1 0 2 5 0).real θ = _
    refine suppE_real (sg_pm b5) (Or.inl rfl) ?_ ?_
    · rw [a02, angE_axis, Real.cos_pi_div_two_sub]; exact s5
    · rw [a02, angE_axis, Real.sin_pi_div_two_sub]; push_cast; linarith
  · show (suppE 1 1 8 2 13 1).real θ = _
    refine suppE_real (Or.inl rfl) (Or.inl rfl) ?_ ?_
    · rw [← cosD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (cosD 8 2 13 1)) (by decide +kernel)
    · rw [← sinD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (sinD 8 2 13 1)) (by decide +kernel)

set_option maxRecDepth 100000 in
/-- F1, `θ8 ≤ 0`, on H; `j` owns the 5-8 separation (anchor from `anchor58_5` or `anchor58_8`). -/
theorem F1rowNeg_exact_H (hg : Good prob θ dx dy L) {j o : ℕ} (hjo : (j = 5 ∧ o = 8) ∨ (j = 8 ∧ o = 5))
    (hanch : -Real.sin (angE θ j 0) * ((cH dx dy 4).1 - (cH dx dy 2).1) +
      Real.cos (angE θ j 0) * ((cH dx dy 4).2 - (cH dx dy 2).2) ≥ 1/2 + supp (angE θ o 0) (angE θ j 2))
    {b5 bj bd : Bool} (h5 : 0 ≤ (sg b5 : ℝ) * θ 5) (hjb : 0 ≤ (sg bj : ℝ) * θ j) (h8 : θ 8 ≤ 0) (hd : 0 ≤ (sg bd : ℝ) * (θ 8 - θ 5)) :
    (F1rowNeg j o (if bj then dX58.lo else dX58.hi) dX813.hi (sg b5, 1) (1, 1) (anchor58E bd)).Holds
      θ (cH dx dy 7).1 (cH dx dy 7).2 L := by
  have t0 := theta0 hg
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, t0]; ring
  have s5 := sin_orth hg (k := 5) (by simp) h5
  have c5 : 0 < Real.cos (θ 5) := by
    rw [← angE_axis θ 5]; exact pos_of_rngH hg (.cs 5 0) (by decide +kernel)
  have s8 := sin_orth hg (k := 8) (b := false) (by simp) (by simp [sg]; exact h8)
  simp only [sg, Bool.false_eq_true, ↓reduceIte] at s8; push_cast at s8
  have hj : j = 5 ∨ j = 8 := hjo.elim (fun h => Or.inl h.1) (fun h => Or.inr h.1)
  have hjm : j ∈ [1, 2, 5, 7, 8, 10, 11, 13, 14] := by rcases hj with rfl | rfl <;> simp
  have hsj := sin_orth hg hjm hjb
  rw [← angE_axis θ j] at hsj
  have p2 := hg.pos _ (prob.sq_mem (i := 2) (by decide))
  have p4 := hg.pos _ (prob.sq_mem (i := 4) (by decide))
  have p7 := hg.pos _ (prob.sq_mem (i := 7) (by decide))
  have hx58 : Iv.mem _ dX58 := mem_dIv (rA := (prob.sq 2).rx) (rB := (prob.sq 4).rx) p2.1 p4.1
  have hx813 : Iv.mem _ dX813 := mem_dIv (rA := (prob.sq 4).rx) (rB := (prob.sq 7).rx) p4.1 p7.1
  have hX := mul_choose_lb hx58 hsj
  have hcj : 0 < Real.cos (angE θ j 0) := by
    rcases hj with rfl | rfl
    · exact pos_of_rngH hg (.cs 5 0) (by decide +kernel)
    · exact pos_of_rngH hg (.cs 8 0) (by decide +kernel)
  refine F1rowNeg_holds t0 (sep_8_13 hg) hanch (by simpa [cH, cenOf] using hX)
    (fit_walls hg (i := 2) (by decide)).2.2.1 (by simpa [cH, cenOf] using hx813.2) hcj
    (by rw [angE_axis]; linarith) (pos_of_rngH hg (.cs 8 0) (by decide +kernel)) ?_ ?_
    (by rcases hjo with ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
        · exact (anchor58E_real hg hd).2.le
        · exact (anchor58E_real hg hd).1.le)
  · show (suppE (sg b5) 1 0 2 5 0).real θ = _
    refine suppE_real (sg_pm b5) (Or.inl rfl) ?_ ?_
    · rw [a02, angE_axis, Real.cos_pi_div_two_sub]; exact s5
    · rw [a02, angE_axis, Real.sin_pi_div_two_sub]; push_cast; linarith
  · show (suppE 1 1 8 2 13 1).real θ = _
    refine suppE_real (Or.inl rfl) (Or.inl rfl) ?_ ?_
    · rw [← cosD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (cosD 8 2 13 1)) (by decide +kernel)
    · rw [← sinD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (sinD 8 2 13 1)) (by decide +kernel)

set_option maxRecDepth 100000 in
/-- F1, 5-8 owned by 5 (5's face `+e2`), on H; `bd` the sign of `θ8 - θ5`. -/
theorem F1rowPos5_exact_H (hg : Good prob θ dx dy L) (h58 : Sep (cH dx dy 2) (φH θ 2) (cH dx dy 4) (φH θ 4) 1)
    {b5 bd : Bool} (h5 : 0 ≤ (sg b5 : ℝ) * θ 5) (hd : 0 ≤ (sg bd : ℝ) * (θ 8 - θ 5)) :
    (F1rowPos5 (if b5 then (absX 2).hi else (absX 2).lo) (if bd then (absX 4).hi else (absX 4).lo)
      (if bd == b5 then (absY 4).hi else (absY 4).lo) (sg b5, 1) (1, 1) (anchor58E bd)).Holds
      θ (cH dx dy 7).1 (cH dx dy 7).2 L := by
  have t0 := theta0 hg
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, t0]; ring
  have s5 := sin_orth hg (k := 5) (by simp) h5
  have c5 : 0 < Real.cos (θ 5) := by
    rw [← angE_axis θ 5]; exact pos_of_rngH hg (.cs 5 0) (by decide +kernel)
  have sd := sin_orth2 hg (s := 8) (t := 5) (M := 0) (by simp) (by simp) hd
  have m2 := cxy_mem hg (i := 2) (by decide)
  have m4 := cxy_mem hg (i := 4) (by decide)
  have hs5' : 0 ≤ (sg b5 : ℝ) * Real.sin (angE θ 5 0) := by rw [angE_axis]; exact s5
  have hX5 := mul_choose m2.1 hs5'
  have c5' : 0 < Real.cos (angE θ 5 0) := by rw [angE_axis]; exact c5
  have hx := mul_choose m4.1 (s := Real.sin (angE θ 8 0 - angE θ 5 0) * Real.cos (angE θ 5 0)) (b := bd)
    (by rw [← mul_assoc]; exact mul_nonneg sd c5'.le)
  have hy := mul_choose m4.2 (s := Real.sin (angE θ 8 0 - angE θ 5 0) * Real.sin (angE θ 5 0)) (b := bd == b5)
    (by rw [sg_beq]; push_cast
        have := mul_nonneg sd hs5'
        linarith [show (sg bd : ℝ) * sg b5 * (Real.sin (angE θ 8 0 - angE θ 5 0) * Real.sin (angE θ 5 0)) =
          (sg bd : ℝ) * Real.sin (angE θ 8 0 - angE θ 5 0) * ((sg b5 : ℝ) * Real.sin (angE θ 5 0)) by ring])
  refine F1rowPos5_holds t0 (sep_8_13 hg) h58 hX5 c5'.le (fit_walls hg (i := 2) (by decide)).2.2.1
    (by linarith) (by rw [← cosD_real]; exact nonneg_of_rngH hg (cosD 8 0 5 0) (by decide +kernel)) ?_
    (anchor58E_real hg hd).2.le ?_
  · show (suppE (sg b5) 1 0 2 5 0).real θ = _
    refine suppE_real (sg_pm b5) (Or.inl rfl) ?_ ?_
    · rw [a02, angE_axis, Real.cos_pi_div_two_sub]; exact s5
    · rw [a02, angE_axis, Real.sin_pi_div_two_sub]; push_cast; linarith
  · show (suppE 1 1 8 2 13 1).real θ = _
    refine suppE_real (Or.inl rfl) (Or.inl rfl) ?_ ?_
    · rw [← cosD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (cosD 8 2 13 1)) (by decide +kernel)
    · rw [← sinD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (sinD 8 2 13 1)) (by decide +kernel)


end
end Sq19.Endgame

#print axioms Sq19.Endgame.anchor58E_real
#print axioms Sq19.Endgame.F1rowPos8_exact_H
#print axioms Sq19.Endgame.F1rowNeg_exact_H
#print axioms Sq19.Endgame.F1rowPos5_exact_H
