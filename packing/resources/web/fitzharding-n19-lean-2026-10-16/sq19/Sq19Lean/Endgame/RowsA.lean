import Sq19Lean.Endgame.Rows

/-!
# The owner-a P and Q rows

Here square 13 owns the separating face. The offsets are the actual projections
of the corners used by `mkcap.c`, not independent coordinates. The statements
require no sign assumption on the relative angles of the tilted squares.
Numerical enclosure of the offsets on H remains a separate obligation.
-/
namespace Sq19.Endgame
open Sq19.Milp

noncomputable def proj1 (φ : ℝ) (p : ℝ × ℝ) : ℝ :=
  Real.cos φ * p.1 + Real.sin φ * p.2
noncomputable def proj2 (φ : ℝ) (p : ℝ × ℝ) : ℝ :=
  -Real.sin φ * p.1 + Real.cos φ * p.2
noncomputable def corner (c : ℝ × ℝ) (φ : ℝ) (j : Fin 4) : ℝ × ℝ :=
  (c.1 + vx φ j, c.2 + vy φ j)

/-- P is the bottom-right corner of square 2. -/
noncomputable def offsetP (c2 c14 : ℝ × ℝ) (φ2 φ13 : ℝ) : ℝ :=
  proj1 φ13 (corner c2 φ2 1 - c14)
/-- Q is the bottom-left corner of square 10. -/
noncomputable def offsetQ (c10 c11 : ℝ × ℝ) (φ10 φ13 : ℝ) : ℝ :=
  proj2 φ13 (c11 - corner c10 φ10 0)

private theorem proj1_sub (φ : ℝ) (p q : ℝ × ℝ) :
    proj1 φ (p - q) = proj1 φ p - proj1 φ q := by
  simp only [proj1, Prod.fst_sub, Prod.snd_sub]; ring
private theorem proj2_sub (φ : ℝ) (p q : ℝ × ℝ) :
    proj2 φ (p - q) = proj2 φ p - proj2 φ q := by
  simp only [proj2, Prod.fst_sub, Prod.snd_sub]; ring

/-- Change of normal, retaining the tangential displacement exactly. -/
theorem proj1_rotate (a b : ℝ) (p : ℝ × ℝ) :
    proj1 a p = Real.cos (a-b) * proj1 b p + Real.sin (a-b) * proj2 b p := by
  simp only [proj1, proj2, Real.cos_sub, Real.sin_sub]
  linear_combination -(Real.cos a * p.1 + Real.sin a * p.2) * (Real.sin_sq_add_cos_sq b)

theorem proj2_rotate (a b : ℝ) (p : ℝ × ℝ) :
    proj2 a p = Real.cos (a-b) * proj2 b p - Real.sin (a-b) * proj1 b p := by
  simp only [proj1, proj2, Real.cos_sub, Real.sin_sub]
  linear_combination -(-Real.sin a * p.1 + Real.cos a * p.2) * (Real.sin_sq_add_cos_sq b)

/-- The bottom-right corner minimises projection on the upper tilted normal. -/
theorem cornerP_support (c : ℝ × ℝ) (φ b : ℝ)
    (hs : 0 ≤ Real.sin (b-φ)) (hc : 0 ≤ Real.cos (b-φ)) :
    proj2 b (corner c φ 1) = proj2 b c - supp φ (b + Real.pi/2) := by
  have es : supp φ (b + Real.pi/2) = (Real.sin (b-φ) + Real.cos (b-φ))/2 := by
    unfold supp
    rw [show b + Real.pi/2 - φ = (b-φ) + Real.pi/2 by ring,
      Real.cos_add_pi_div_two, Real.sin_add_pi_div_two, abs_neg, abs_of_nonneg hs, abs_of_nonneg hc]
  rw [es]
  norm_num [proj2, corner, vx, vy, ox, oy, Real.sin_sub, Real.cos_sub]
  ring

/-- The bottom-left corner minimises projection on the right tilted normal. -/
theorem cornerQ_support (c : ℝ × ℝ) (φ b : ℝ)
    (hs : 0 ≤ Real.sin (b-φ)) (hc : 0 ≤ Real.cos (b-φ)) :
    proj1 b (corner c φ 0) = proj1 b c - supp φ b := by
  have es : supp φ b = (Real.cos (b-φ) + Real.sin (b-φ))/2 := by
    simp only [supp, abs_of_nonneg hs, abs_of_nonneg hc]
  rw [es]
  norm_num [proj1, corner, vx, vy, ox, oy, Real.sin_sub, Real.cos_sub]
  ring

/-- P row when 13's top face separates 14. `offsetP` has the same sign as O1 in mkcap. -/
theorem rowP_a {c2 c13 c14 : ℝ × ℝ} {φ2 φ13 φ14 L X2 : ℝ}
    (h214 : Sep c14 φ14 c2 φ2 1) (h1314 : Sep c13 φ13 c14 φ14 1)
    (hx : X2 ≤ c2.1) (hy : c2.2 ≤ L - supp φ2 (Real.pi/2))
    (hs : 0 ≤ Real.sin φ13) (hc : 0 ≤ Real.cos φ13)
    (hs2 : 0 ≤ Real.sin (φ13-φ2)) (hc2 : 0 ≤ Real.cos (φ13-φ2))
    (hd : 0 < Real.cos (φ14-φ13)) :
    proj2 φ13 c13 ≤ -Real.sin φ13 * X2 + Real.cos φ13 * (L - supp φ2 (Real.pi/2)) -
      supp φ2 (φ13 + Real.pi/2) -
      ((1/2 + Real.sin (φ14-φ13) * offsetP c2 c14 φ2 φ13) / Real.cos (φ14-φ13) +
        1/2 + supp φ14 (φ13 + Real.pi/2)) := by
  have hp : 1/2 ≤ proj2 φ14 (corner c2 φ2 1 - c14) := by
    have h := h214 1
    simpa only [nx, ny, Nat.cast_one, one_mul, Real.cos_add_pi_div_two,
      Real.sin_add_pi_div_two, proj2, corner, Prod.fst_sub, Prod.snd_sub] using h
  rw [proj2_rotate φ14 φ13] at hp
  have hgap : (1/2 + Real.sin (φ14-φ13) * offsetP c2 c14 φ2 φ13) / Real.cos (φ14-φ13) ≤
      proj2 φ13 (corner c2 φ2 1 - c14) := by
    rw [div_le_iff₀ hd]
    dsimp only [offsetP]
    linarith
  have hg := sep_gap h1314
  simp only [Nat.cast_one, one_mul, Real.cos_add_pi_div_two, Real.sin_add_pi_div_two] at hg
  rw [proj2_sub, cornerP_support c2 φ2 φ13 hs2 hc2] at hgap
  have mx := mul_le_mul_of_nonneg_left hx hs
  have my := mul_le_mul_of_nonneg_left hy hc
  simp only [proj2] at hgap ⊢
  linarith

/-- Q row when 13's right face separates 11. `offsetQ` has the same sign as O2 in mkcap. -/
theorem rowQ_a {c10 c11 c13 : ℝ × ℝ} {φ10 φ11 φ13 L : ℝ}
    (h1011 : Sep c11 φ11 c10 φ10 0) (h1311 : Sep c13 φ13 c11 φ11 0)
    (hx : c10.1 ≤ L - supp φ10 0) (hy : c10.2 ≤ L - supp φ10 (Real.pi/2))
    (hc : 0 ≤ Real.cos φ13) (hs : 0 ≤ Real.sin φ13)
    (hs10 : 0 ≤ Real.sin (φ13-φ10)) (hc10 : 0 ≤ Real.cos (φ13-φ10))
    (hd : 0 < Real.cos (φ11-φ13)) :
    proj1 φ13 c13 ≤ Real.cos φ13 * (L - supp φ10 0) + Real.sin φ13 * (L - supp φ10 (Real.pi/2)) -
      supp φ10 φ13 -
      ((1/2 + Real.sin (φ11-φ13) * offsetQ c10 c11 φ10 φ13) / Real.cos (φ11-φ13) +
        1/2 + supp φ11 φ13) := by
  have hq : 1/2 ≤ proj1 φ11 (corner c10 φ10 0 - c11) := by
    have h := h1011 0
    simpa only [nx, ny, Nat.cast_zero, zero_mul, add_zero,
      proj1, corner, Prod.fst_sub, Prod.snd_sub] using h
  rw [proj1_rotate φ11 φ13] at hq
  have eo : proj2 φ13 (corner c10 φ10 0 - c11) = -offsetQ c10 c11 φ10 φ13 := by
    simp only [offsetQ, proj2_sub]; ring
  rw [eo] at hq
  have hgap : (1/2 + Real.sin (φ11-φ13) * offsetQ c10 c11 φ10 φ13) / Real.cos (φ11-φ13) ≤
      proj1 φ13 (corner c10 φ10 0 - c11) := by
    rw [div_le_iff₀ hd]
    linarith
  have hg := sep_gap h1311
  simp only [Nat.cast_zero, zero_mul, add_zero] at hg
  rw [proj1_sub, cornerQ_support c10 φ10 φ13 hs10 hc10] at hgap
  have mx := mul_le_mul_of_nonneg_left hx hc
  have my := mul_le_mul_of_nonneg_left hy hs
  simp only [proj1] at hgap ⊢
  linarith

/-- The quotient in the owner-a rows is exactly the certificate's secant/tangent expression. -/
theorem ownerA_cost (d o : ℝ) :
    (1/2 + Real.sin d * o) / Real.cos d = 1 / (2 * Real.cos d) + Real.tan d * o := by
  rw [Real.tan_eq_sin_div_cos]
  ring

end Sq19.Endgame

#print axioms Sq19.Endgame.rowP_a
#print axioms Sq19.Endgame.rowQ_a
#print axioms Sq19.Endgame.ownerA_cost
