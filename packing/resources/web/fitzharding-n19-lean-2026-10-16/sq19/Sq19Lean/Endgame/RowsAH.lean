import Sq19Lean.Endgame.RowsH
import Sq19Lean.Endgame.RowsA

/-!
# Owner-a rows as expressions

Positive cosine factors clear the divisions in the geometric owner-a inequalities.
The result has the same `RowE.Holds` interface as the owner-b and floor rows, so
`combine` accepts every owner choice. `O` is a certified lower bound for the
signed offset term; it may be either end of an offset enclosure, according to sign.
-/
namespace Sq19.Endgame
open Sq19.Milp

/-- P row with square 13 owning the face, scaled by `cos g_j * cos (φ14-φ13)`. -/
def ProwA (j : ℕ) (Y O : ℚ) (σ : PSigns) : RowE :=
  let cj := Ex.cs j 0
  let cd := cosD 14 1 13 1
  let sd := sinD 14 1 13 1
  let h1x := suppE σ.h1x.1 σ.h1x.2 0 0 1 0
  let h2y := suppE σ.h2y.1 σ.h2y.2 0 2 2 0
  let h2n := suppE σ.h2n.1 σ.h2n.2 13 3 2 0
  let h14n := suppAbsE 13 3 14 1
  let xbound := Ex.add (.add (.mul cj h1x) (.add (.c (1/2)) σ.anc))
    (.neg (.mul (.sn j 0) (.c Y)))
  let base := Ex.add (.mul (.cs 13 3) xbound)
    (.mul cj (.add (.add (.add (.neg (.mul (.sn 13 3) h2y)) (.neg h2n)) (.c (-1/2))) (.neg h14n)))
  ⟨.mul (.mul cj cd) (.cs 13 3), .mul (.mul cj cd) (.sn 13 3),
   .add (.mul cd base) (.neg (.mul cj (.add (.c (1/2)) (.mul sd (.c O))))),
   .mul (.mul cj cd) (.sn 13 3)⟩

theorem ProwA_holds {θ : ℕ → ℝ} {c1 c2 c13 c14 : ℝ × ℝ} {L : ℝ}
    {j o : ℕ} {Y O : ℚ} {σ : PSigns}
    (hθ0 : θ 0 = 0)
    (h214 : Sep c14 (angE θ 14 1) c2 (angE θ 2 0) 1)
    (h1314 : Sep c13 (angE θ 13 1) c14 (angE θ 14 1) 1)
    (hanch : Real.cos (angE θ j 0) * (c2.1 - c1.1) + Real.sin (angE θ j 0) * (c2.2 - c1.2) ≥
      1/2 + supp (angE θ o 0) (angE θ j 0))
    (hw1 : supp (angE θ 1 0) 0 ≤ c1.1) (hw2 : c2.2 ≤ L - supp (angE θ 2 0) (Real.pi/2))
    (hY : Real.sin (angE θ j 0) * (c2.2-c1.2) ≤ Real.sin (angE θ j 0) * Y)
    (hcj : 0 < Real.cos (angE θ j 0))
    (hs : 0 ≤ Real.sin (angE θ 13 1)) (hc : 0 ≤ Real.cos (angE θ 13 1))
    (hs2 : 0 ≤ Real.sin (angE θ 13 1-angE θ 2 0)) (hc2 : 0 ≤ Real.cos (angE θ 13 1-angE θ 2 0))
    (hd : 0 < Real.cos (angE θ 14 1-angE θ 13 1))
    (hO : Real.sin (angE θ 14 1-angE θ 13 1) * O ≤
      Real.sin (angE θ 14 1-angE θ 13 1) * offsetP c2 c14 (angE θ 2 0) (angE θ 13 1))
    (e1 : (suppE σ.h1x.1 σ.h1x.2 0 0 1 0).real θ = supp (angE θ 1 0) (angE θ 0 0))
    (e2 : (suppE σ.h2y.1 σ.h2y.2 0 2 2 0).real θ = supp (angE θ 2 0) (angE θ 0 2))
    (e3 : (suppE σ.h2n.1 σ.h2n.2 13 3 2 0).real θ = supp (angE θ 2 0) (angE θ 13 3))
    (e5 : σ.anc.real θ ≤ supp (angE θ o 0) (angE θ j 0)) :
    (ProwA j Y O σ).Holds θ c13.1 c13.2 L := by
  have a00 : angE θ 0 0 = 0 := by simp [angE, hθ0]
  have a02 : angE θ 0 2 = Real.pi/2 := by simp [angE, hθ0]; ring
  have a133 : angE θ 13 3 = angE θ 13 1 + Real.pi/2 := by
    have := angE_add θ 13 1 1; simpa using this
  have e4 := suppAbsE_real θ 13 3 14 1
  rw [a00] at e1; rw [a02] at e2; rw [a133] at e3 e4
  set X2 := supp (angE θ 1 0) 0 +
    (1/2 + σ.anc.real θ - Real.sin (angE θ j 0) * Y) / Real.cos (angE θ j 0)
  have hX2 : X2 ≤ c2.1 := by
    have ha : Real.cos (angE θ j 0) * (c2.1-c1.1) + Real.sin (angE θ j 0) * (c2.2-c1.2) ≥
        1/2 + σ.anc.real θ := by linarith
    have hh := shift_x_lb hcj ha hY
    dsimp only [X2]; linarith
  have hr := rowP_a h214 h1314 hX2 hw2 hs hc hs2 hc2 hd
  have ho := div_le_div_of_nonneg_right (add_le_add_left hO (1/2)) hd.le
  have hb : proj2 (angE θ 13 1) c13 ≤
      -Real.sin (angE θ 13 1) * X2 + Real.cos (angE θ 13 1) * (L - supp (angE θ 2 0) (Real.pi/2)) -
      supp (angE θ 2 0) (angE θ 13 1 + Real.pi/2) -
      ((1/2 + Real.sin (angE θ 14 1-angE θ 13 1) * O) / Real.cos (angE θ 14 1-angE θ 13 1) +
        1/2 + supp (angE θ 14 1) (angE θ 13 1 + Real.pi/2)) := by
    linear_combination hr + ho
  have hm := mul_le_mul_of_nonneg_left hb (mul_pos hcj hd).le
  have ex : Real.cos (angE θ j 0) * X2 = Real.cos (angE θ j 0) * supp (angE θ 1 0) 0 +
      (1/2 + σ.anc.real θ - Real.sin (angE θ j 0) * Y) := by
    dsimp only [X2]; field_simp
  unfold RowE.Holds ProwA
  simp only [Ex.real, e1, e2, e3, e4, cosD_real, sinD_real]
  have ce : Real.cos (((3:ℕ):ℝ) * Real.pi/4 + θ 13) = -Real.sin (angE θ 13 1) := by
    change Real.cos (angE θ 13 3) = _; rw [a133, Real.cos_add_pi_div_two]
  have se : Real.sin (((3:ℕ):ℝ) * Real.pi/4 + θ 13) = Real.cos (angE θ 13 1) := by
    change Real.sin (angE θ 13 3) = _; rw [a133, Real.sin_add_pi_div_two]
  rw [ce, se]
  have ecost : Real.cos (angE θ 14 1-angE θ 13 1) *
      ((1/2 + Real.sin (angE θ 14 1-angE θ 13 1) * O) / Real.cos (angE θ 14 1-angE θ 13 1)) =
      1/2 + Real.sin (angE θ 14 1-angE θ 13 1) * O := by field_simp
  simp only [proj2] at hm
  have exm := congrArg (fun z : ℝ => Real.cos (angE θ 14 1-angE θ 13 1) * Real.sin (angE θ 13 1) * z) ex
  have ecm := congrArg (fun z : ℝ => Real.cos (angE θ j 0) * z) ecost
  simp only [angE] at hm exm ecm ⊢
  push_cast
  nlinarith only [hm, exm, ecm]

/-- Q row with square 13 owning the face, scaled by `cos (φ11-φ13)`. -/
def QrowA (O : ℚ) (σ : QSigns) : RowE :=
  let cd := cosD 11 1 13 1
  let sd := sinD 11 1 13 1
  let h10x := suppE σ.h10x.1 σ.h10x.2 0 0 10 0
  let h10y := suppE σ.h10y.1 σ.h10y.2 0 2 10 0
  let h10n := suppE σ.h10n.1 σ.h10n.2 13 1 10 0
  let h11n := suppAbsE 13 1 11 1
  let base := Ex.add (.add (.add (.neg (.mul (.cs 13 1) h10x)) (.neg (.mul (.sn 13 1) h10y))) (.neg h10n))
    (.add (.c (-1/2)) (.neg h11n))
  ⟨.mul cd (.cs 13 1), .mul cd (.sn 13 1),
   .add (.mul cd base) (.neg (.add (.c (1/2)) (.mul sd (.c O)))),
   .mul cd (.add (.cs 13 1) (.sn 13 1))⟩

theorem QrowA_holds {θ : ℕ → ℝ} {c10 c11 c13 : ℝ × ℝ} {L : ℝ} {O : ℚ} {σ : QSigns}
    (hθ0 : θ 0 = 0)
    (h1011 : Sep c11 (angE θ 11 1) c10 (angE θ 10 0) 0)
    (h1311 : Sep c13 (angE θ 13 1) c11 (angE θ 11 1) 0)
    (hx : c10.1 ≤ L - supp (angE θ 10 0) 0) (hy : c10.2 ≤ L - supp (angE θ 10 0) (Real.pi/2))
    (hc : 0 ≤ Real.cos (angE θ 13 1)) (hs : 0 ≤ Real.sin (angE θ 13 1))
    (hs10 : 0 ≤ Real.sin (angE θ 13 1-angE θ 10 0)) (hc10 : 0 ≤ Real.cos (angE θ 13 1-angE θ 10 0))
    (hd : 0 < Real.cos (angE θ 11 1-angE θ 13 1))
    (hO : Real.sin (angE θ 11 1-angE θ 13 1) * O ≤
      Real.sin (angE θ 11 1-angE θ 13 1) * offsetQ c10 c11 (angE θ 10 0) (angE θ 13 1))
    (e1 : (suppE σ.h10x.1 σ.h10x.2 0 0 10 0).real θ = supp (angE θ 10 0) (angE θ 0 0))
    (e2 : (suppE σ.h10y.1 σ.h10y.2 0 2 10 0).real θ = supp (angE θ 10 0) (angE θ 0 2))
    (e3 : (suppE σ.h10n.1 σ.h10n.2 13 1 10 0).real θ = supp (angE θ 10 0) (angE θ 13 1)) :
    (QrowA O σ).Holds θ c13.1 c13.2 L := by
  have a00 : angE θ 0 0 = 0 := by simp [angE, hθ0]
  have a02 : angE θ 0 2 = Real.pi/2 := by simp [angE, hθ0]; ring
  rw [a00] at e1; rw [a02] at e2
  have e4 := suppAbsE_real θ 13 1 11 1
  have hr := rowQ_a h1011 h1311 hx hy hc hs hs10 hc10 hd
  have ho := div_le_div_of_nonneg_right (add_le_add_left hO (1/2)) hd.le
  have hb : proj1 (angE θ 13 1) c13 ≤
      Real.cos (angE θ 13 1) * (L - supp (angE θ 10 0) 0) +
      Real.sin (angE θ 13 1) * (L - supp (angE θ 10 0) (Real.pi/2)) - supp (angE θ 10 0) (angE θ 13 1) -
      ((1/2 + Real.sin (angE θ 11 1-angE θ 13 1) * O) / Real.cos (angE θ 11 1-angE θ 13 1) +
        1/2 + supp (angE θ 11 1) (angE θ 13 1)) := by
    linear_combination hr + ho
  have hm := mul_le_mul_of_nonneg_left hb hd.le
  have ecost : Real.cos (angE θ 11 1-angE θ 13 1) *
      ((1/2 + Real.sin (angE θ 11 1-angE θ 13 1) * O) / Real.cos (angE θ 11 1-angE θ 13 1)) =
      1/2 + Real.sin (angE θ 11 1-angE θ 13 1) * O := by field_simp
  unfold RowE.Holds QrowA
  simp only [Ex.real, e1, e2, e3, e4, cosD_real, sinD_real]
  simp only [proj1] at hm
  simp only [angE] at hm ecost ⊢
  push_cast
  nlinarith only [hm, ecost]

end Sq19.Endgame

#print axioms Sq19.Endgame.ProwA_holds
#print axioms Sq19.Endgame.QrowA_holds
