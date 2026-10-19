import Sq19Lean.Endgame.ReductionCases

/-! Select the actual row family of a packing. No numerical certificate is assumed
here: the owner choices, signs and offset endpoints are obtained from `Good`. -/
namespace Sq19.Endgame.Reduction
open Sq19.Milp

structure Case.Matches (c : Case) (θ dx dy : ℕ → ℝ) : Prop where
  sign1 : 0 ≤ (sg c.b1 : ℝ) * θ 1
  sign2 : 0 ≤ (sg c.b2 : ℝ) * θ 2
  sign5 : 0 ≤ (sg c.b5 : ℝ) * θ 5
  sign8 : 0 ≤ (sg c.b8 : ℝ) * θ 8
  sign10 : 0 ≤ (sg c.b10 : ℝ) * θ 10
  order58 : if c.fiveLarger then |θ 8| ≤ |θ 5| else |θ 5| ≤ |θ 8|
  signP : 0 ≤ (sg c.pd : ℝ) * (θ 14 - θ 13)
  signQ : 0 ≤ (sg c.qd : ℝ) * (θ 11 - θ 13)
  anchor12 :
    Real.cos (angE θ c.j12 0) * ((cH dx dy 1).1 - (cH dx dy 0).1) +
    Real.sin (angE θ c.j12 0) * ((cH dx dy 1).2 - (cH dx dy 0).2) ≥
      1/2 + supp (angE θ (if c.owner12 then 1 else 2) 0) (angE θ c.j12 0)
  sepP : if c.pa then Sep (cH dx dy 7) (φH θ 7) (cH dx dy 8) (φH θ 8) 1
    else Sep (cH dx dy 8) (φH θ 8) (cH dx dy 7) (φH θ 7) 3
  sepQ : if c.qa then Sep (cH dx dy 7) (φH θ 7) (cH dx dy 6) (φH θ 6) 0
    else Sep (cH dx dy 6) (φH θ 6) (cH dx dy 7) (φH θ 7) 2
  sep58 : if c.owner58 then Sep (cH dx dy 4) (φH θ 4) (cH dx dy 2) (φH θ 2) 3
    else Sep (cH dx dy 2) (φH θ 2) (cH dx dy 4) (φH θ 4) 1

private theorem choose_sign (x : ℝ) : ∃ b : Bool, 0 ≤ (sg b : ℝ) * x := by
  rcases le_total 0 x with h | h
  · exact ⟨true, by simpa [sg] using h⟩
  · exact ⟨false, by simpa [sg] using h⟩

private theorem choose_branch {P Q : Prop} (h : P ∨ Q) :
    ∃ b : Bool, if b then P else Q := by
  rcases h with h | h
  · exact ⟨true, h⟩
  · exact ⟨false, h⟩

theorem exists_matching_case {θ dx dy : ℕ → ℝ} {L : ℝ}
    (hg : Good Hull.prob θ dx dy L) : ∃ c : Case, c.Matches θ dx dy := by
  obtain ⟨b1, h1⟩ := choose_sign (θ 1)
  obtain ⟨b2, h2⟩ := choose_sign (θ 2)
  obtain ⟨b5, h5⟩ := choose_sign (θ 5)
  obtain ⟨b8, h8⟩ := choose_sign (θ 8)
  obtain ⟨b10, h10⟩ := choose_sign (θ 10)
  obtain ⟨pd, hp⟩ := choose_sign (θ 14 - θ 13)
  obtain ⟨qd, hq⟩ := choose_sign (θ 11 - θ 13)
  obtain ⟨order, hord⟩ := choose_branch (le_total |θ 8| |θ 5|)
  obtain ⟨pa, hpa⟩ := choose_branch (sep_13_14 hg)
  obtain ⟨qa, hqa⟩ := choose_branch (sep_11_13 hg).symm
  obtain ⟨owner58, h58⟩ := choose_branch (sep_5_8 hg).symm
  obtain ⟨owner12, h12⟩ := choose_branch (anchor_1_2 hg).symm
  refine ⟨⟨pa, qa, owner12, owner58, b1, b2, b5, b8, b10, order, pd, qd⟩,
    h1, h2, h5, h8, h10, hord, hp, hq, ?_, hpa, hqa, h58⟩
  cases owner12 <;> exact h12

theorem Case.Matches.rows {c : Case} {θ dx dy : ℕ → ℝ} {L : ℝ}
    (hm : c.Matches θ dx dy) (hg : Good Hull.prob θ dx dy L) :
    c.P.Holds θ (cH dx dy 7).1 (cH dx dy 7).2 L ∧
    c.Q.Holds θ (cH dx dy 7).1 (cH dx dy 7).2 L ∧
    c.F.Holds θ (cH dx dy 7).1 (cH dx dy 7).2 L := by
  have hj : c.j12 = 1 ∨ c.j12 = 2 := by
    cases h : c.owner12 <;> simp [Case.j12, h]
  have hs : 0 ≤ (sg (if c.owner12 then c.b2 else c.b1) : ℝ) * θ c.j12 := by
    cases h : c.owner12
    · simpa [Case.j12, h] using hm.sign1
    · simpa [Case.j12, h] using hm.sign2
  have hp : c.P.Holds θ (cH dx dy 7).1 (cH dx dy 7).2 L := by
    cases h : c.pa
    · simpa [Case.P, h] using ProwB_H hg hj hm.anchor12
        (by simpa [h] using hm.sepP) hm.sign1 hm.sign2 hs
    · simpa [Case.P, h] using ProwA_H hg hj hm.anchor12
        (by simpa [h] using hm.sepP) hm.sign1 hm.sign2 hs hm.signP
  have hq : c.Q.Holds θ (cH dx dy 7).1 (cH dx dy 7).2 L := by
    cases h : c.qa
    · simpa [Case.Q, h] using QrowB_H hg (by simpa [h] using hm.sepQ) hm.sign10
    · simpa [Case.Q, h] using QrowA_H hg (by simpa [h] using hm.sepQ) hm.sign10 hm.signQ
  refine ⟨hp, hq, ?_⟩
  have hd := c.relative_sign hm.sign5 hm.sign8 hm.order58
  cases hb : c.b8
  · have h8 : θ 8 ≤ 0 := by simpa [hb, sg] using hm.sign8
    cases ho : c.owner58
    · simpa [Case.F, Case.j58, Case.other58, hb, ho] using
        F1rowNeg_exact_H hg (Or.inl ⟨rfl, rfl⟩)
          (anchor58_5 (by simpa [ho] using hm.sep58)) hm.sign5 hm.sign5 h8 hd
    · simpa [Case.F, Case.j58, Case.other58, hb, ho] using
        F1rowNeg_exact_H hg (Or.inr ⟨rfl, rfl⟩)
          (anchor58_8 (by simpa [ho] using hm.sep58)) hm.sign5 hm.sign8 h8 hd
  · have h8 : 0 ≤ θ 8 := by simpa [hb, sg] using hm.sign8
    cases ho : c.owner58
    · simpa [Case.F, hb, ho] using
        F1rowPos5_exact_H hg (by simpa [ho] using hm.sep58) hm.sign5 hd
    · simpa [Case.F, hb, ho] using
        F1rowPos8_exact_H hg (by simpa [ho] using hm.sep58) hm.sign5 h8 hd

end Sq19.Endgame.Reduction

#print axioms Sq19.Endgame.Reduction.exists_matching_case
#print axioms Sq19.Endgame.Reduction.Case.Matches.rows
