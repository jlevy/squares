import Sq19Lean.Endgame.Separations
import Sq19Lean.Endgame.Rows

/-!
# Three half-planes and the 1-2 anchor (LOCAL_THEOREM.md, Lean pieces 2-3)

* `farkas3`: if a point `x` satisfies `a_i . x ≤ r_i` (i = P, Q, F) and
  `λ = -(a_Q × a_F, a_F × a_P, a_P × a_Q)` has nonnegative entries, then `Σ λ_i r_i ≥ 0`
  (because `Σ λ_i a_i = 0` identically).
* `farkas3_L`: with `r_i = b0_i + b1_i L` and `Σ λ_i b1_i > 0`, `L ≥ -Σ λ_i b0_i / Σ λ_i b1_i`.
* `anchor_1_2`: on H, the 1-2 separation by either owner, in the form used for `c2x_lo`.
-/
namespace Sq19.Endgame
open Sq19.Milp Sq19.Endgame.Hull

def cross (ax ay bx by' : ℝ) : ℝ := ax * by' - ay * bx

theorem farkas3 {aPx aPy aQx aQy aFx aFy rP rQ rF x y : ℝ}
    (hP : aPx * x + aPy * y ≤ rP) (hQ : aQx * x + aQy * y ≤ rQ) (hF : aFx * x + aFy * y ≤ rF)
    (l1 : 0 ≤ -cross aQx aQy aFx aFy) (l2 : 0 ≤ -cross aFx aFy aPx aPy) (l3 : 0 ≤ -cross aPx aPy aQx aQy) :
    0 ≤ -cross aQx aQy aFx aFy * rP + -cross aFx aFy aPx aPy * rQ + -cross aPx aPy aQx aQy * rF := by
  have e : -cross aQx aQy aFx aFy * (aPx * x + aPy * y) + -cross aFx aFy aPx aPy * (aQx * x + aQy * y) +
      -cross aPx aPy aQx aQy * (aFx * x + aFy * y) = 0 := by unfold cross; ring
  have m1 := mul_le_mul_of_nonneg_left hP l1
  have m2 := mul_le_mul_of_nonneg_left hQ l2
  have m3 := mul_le_mul_of_nonneg_left hF l3
  linarith

theorem farkas3_L {lP lQ lF b0P b1P b0Q b1Q b0F b1F L : ℝ}
    (h : 0 ≤ lP * (b0P + b1P * L) + lQ * (b0Q + b1Q * L) + lF * (b0F + b1F * L))
    (hS : 0 < lP * b1P + lQ * b1Q + lF * b1F) :
    -(lP * b0P + lQ * b0Q + lF * b0F) / (lP * b1P + lQ * b1Q + lF * b1F) ≤ L := by
  rw [div_le_iff₀ hS]; nlinarith

section
variable {θ dx dy : ℕ → ℝ} {L : ℝ}

/-- The 1-2 anchor on H: owner 1 (`e1 φ1`) or owner 2 (`e1 φ2`), `Δ = c2 - c1`. -/
theorem anchor_1_2 (hg : Good Hull.prob θ dx dy L) :
    (Real.cos (φH θ 0) * ((cH dx dy 1).1 - (cH dx dy 0).1) + Real.sin (φH θ 0) * ((cH dx dy 1).2 - (cH dx dy 0).2)
        ≥ 1/2 + supp (φH θ 1) (φH θ 0)) ∨
    (Real.cos (φH θ 1) * ((cH dx dy 1).1 - (cH dx dy 0).1) + Real.sin (φH θ 1) * ((cH dx dy 1).2 - (cH dx dy 0).2)
        ≥ 1/2 + supp (φH θ 0) (φH θ 1)) := by
  rcases sep_1_2 hg with h | h
  · left
    have g := sep_gap h
    simpa using g
  · right
    have g := sep_gap h
    have a2 : φH θ 1 + ((2:ℕ):ℝ) * (Real.pi / 2) = φH θ 1 + Real.pi := by push_cast; ring
    rw [a2, supp_add_pi, Real.cos_add_pi, Real.sin_add_pi] at g
    linarith

end

end Sq19.Endgame

#print axioms Sq19.Endgame.farkas3
#print axioms Sq19.Endgame.farkas3_L
#print axioms Sq19.Endgame.anchor_1_2
