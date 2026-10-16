import Sq19Lean.Milp.Geometry

/-!
# Rows of the local step (LOCAL_THEOREM.md, Lean piece 2)

Real inequalities for the centre of square 13 derived from separations (`Sep`, whose existence on H is
`Sq19Lean/Endgame/Separations.lean`) and the walls. Supports are kept exact:
`supp φ ψ = (|cos (ψ - φ)| + |sin (ψ - φ)|)/2` is the support of the unit square at angle `φ` in
direction `e1 ψ = (cos ψ, sin ψ)`. The certificate's closed forms (sign-split supports, `anch`, `g`)
are these supports evaluated where the signs are fixed; that identification is a later step.

* `sep_gap`: face `k` of `A` separating `B` gives `e1 ψ . (c_B - c_A) ≥ 1/2 + supp φ_B ψ`, `ψ = φ_A + kπ/2`.
* `wall_bounds`: a square in `[0, L]^2` has `supp φ 0 ≤ c_x ≤ L - supp φ 0`, same in `y` with `supp φ (π/2)`.
* `shift_x_lb`: the anchor step used for `c2x_lo`, `c8y_lo`, `c8x_hi`.
* `rowP_b`, `rowQ_b`: the P and Q half-planes when the 13-14 (13-11) separation is owned by 14 (11).
* `rowF1_pos_owner8`, `rowF1_pos_owner5`, `rowF1_neg`: the floor half-plane F1.
-/
namespace Sq19.Endgame
open Sq19.Milp

noncomputable def supp (φ ψ : ℝ) : ℝ := (|Real.cos (ψ - φ)| + |Real.sin (ψ - φ)|) / 2

theorem supp_add_pi (φ ψ : ℝ) : supp φ (ψ + Real.pi) = supp φ ψ := by
  unfold supp
  rw [show ψ + Real.pi - φ = (ψ - φ) + Real.pi by ring, Real.cos_add_pi, Real.sin_add_pi, abs_neg, abs_neg]

theorem supp_ge_half (φ ψ : ℝ) : 1/2 ≤ supp φ ψ := by
  unfold supp
  have h := Real.sin_sq_add_cos_sq (ψ - φ)
  have : (1:ℝ) ≤ (|Real.cos (ψ - φ)| + |Real.sin (ψ - φ)|)^2 := by
    nlinarith [sq_abs (Real.cos (ψ - φ)), sq_abs (Real.sin (ψ - φ)), abs_nonneg (Real.cos (ψ - φ)),
      abs_nonneg (Real.sin (ψ - φ)), mul_nonneg (abs_nonneg (Real.cos (ψ - φ))) (abs_nonneg (Real.sin (ψ - φ)))]
  nlinarith [abs_nonneg (Real.cos (ψ - φ)), abs_nonneg (Real.sin (ψ - φ))]

theorem nx_ny (φ : ℝ) (k : ℕ) : nx φ k = Real.cos (φ + k * (Real.pi / 2)) ∧ ny φ k = Real.sin (φ + k * (Real.pi / 2)) :=
  ⟨rfl, rfl⟩

/-- Separation gap along the separating face normal. -/
theorem sep_gap {cA cB : ℝ × ℝ} {φA φB : ℝ} {k : ℕ} (h : Sep cA φA cB φB k) :
    Real.cos (φA + k * (Real.pi / 2)) * (cB.1 - cA.1) + Real.sin (φA + k * (Real.pi / 2)) * (cB.2 - cA.2) ≥
      1/2 + supp φB (φA + k * (Real.pi / 2)) := by
  have hs := sep_support cA cB φA φB k h
  set ψ := φA + k * (Real.pi / 2)
  have e1 : nx φA k * Real.cos φB + ny φA k * Real.sin φB = Real.cos (ψ - φB) := by
    simp only [nx, ny, ψ]; rw [Real.cos_sub]
  have e2 : -nx φA k * Real.sin φB + ny φA k * Real.cos φB = Real.sin (ψ - φB) := by
    simp only [nx, ny, ψ]; rw [Real.sin_sub]; ring
  rw [e1, e2] at hs
  exact hs

/-- A vertex attains the support in any direction. -/
theorem vertex_attains (φ n1 n2 : ℝ) : ∃ j : Fin 4, n1 * vx φ j + n2 * vy φ j =
    (|n1 * Real.cos φ + n2 * Real.sin φ| + |-n1 * Real.sin φ + n2 * Real.cos φ|) / 2 := by
  set P := n1 * Real.cos φ + n2 * Real.sin φ
  set Q := -n1 * Real.sin φ + n2 * Real.cos φ
  have key : ∀ j : Fin 4, n1 * vx φ j + n2 * vy φ j = ox j * P + oy j * Q := by
    intro j; simp only [vx, vy, P, Q]; ring
  rcases le_or_gt 0 P with hP | hP <;> rcases le_or_gt 0 Q with hQ | hQ
  · exact ⟨2, by rw [key, abs_of_nonneg hP, abs_of_nonneg hQ]; norm_num [ox, oy]; ring⟩
  · exact ⟨1, by rw [key, abs_of_nonneg hP, abs_of_neg hQ]; norm_num [ox, oy]; ring⟩
  · exact ⟨3, by rw [key, abs_of_neg hP, abs_of_nonneg hQ]; norm_num [ox, oy]; ring⟩
  · exact ⟨0, by rw [key, abs_of_neg hP, abs_of_neg hQ]; norm_num [ox, oy]; ring⟩

/-- Wall bounds of a square inside `[0, L]^2`. -/
theorem wall_bounds (c : ℝ × ℝ) (φ L : ℝ)
    (hfit : Sq17.sq c.1 c.2 (Real.cos φ) (Real.sin φ) ⊆ Sq17.Propagation.containerBox L) :
    supp φ 0 ≤ c.1 ∧ c.1 ≤ L - supp φ 0 ∧
    supp φ (Real.pi / 2) ≤ c.2 ∧ c.2 ≤ L - supp φ (Real.pi / 2) := by
  have sx : supp φ 0 = (|1 * Real.cos φ + 0 * Real.sin φ| + |-1 * Real.sin φ + 0 * Real.cos φ|) / 2 := by
    unfold supp; simp [abs_neg]
  have sx' : supp φ 0 = (|-1 * Real.cos φ + 0 * Real.sin φ| + |-(-1) * Real.sin φ + 0 * Real.cos φ|) / 2 := by
    unfold supp; simp [abs_neg]
  have sy : supp φ (Real.pi / 2) = (|0 * Real.cos φ + 1 * Real.sin φ| + |-0 * Real.sin φ + 1 * Real.cos φ|) / 2 := by
    unfold supp; rw [Real.cos_pi_div_two_sub, Real.sin_pi_div_two_sub]; simp [add_comm]
  have sy' : supp φ (Real.pi / 2) = (|0 * Real.cos φ + -1 * Real.sin φ| + |-0 * Real.sin φ + -1 * Real.cos φ|) / 2 := by
    unfold supp; rw [Real.cos_pi_div_two_sub, Real.sin_pi_div_two_sub]; simp [abs_neg, add_comm]
  obtain ⟨j1, h1⟩ := vertex_attains φ 1 0
  obtain ⟨j2, h2⟩ := vertex_attains φ (-1) 0
  obtain ⟨j3, h3⟩ := vertex_attains φ 0 1
  obtain ⟨j4, h4⟩ := vertex_attains φ 0 (-1)
  have v1 := vertex_in_container c φ L hfit j1
  have v2 := vertex_in_container c φ L hfit j2
  have v3 := vertex_in_container c φ L hfit j3
  have v4 := vertex_in_container c φ L hfit j4
  rw [← sx] at h1; rw [← sx'] at h2; rw [← sy] at h3; rw [← sy'] at h4
  refine ⟨?_, ?_, ?_, ?_⟩ <;> linarith [v1.1, v1.2.1, v2.1, v2.2.1, v3.2.2.1, v3.2.2.2, v4.2.2.1, v4.2.2.2]

/-- Anchor step: `cos g Δx + sin g Δy ≥ S` with `cos g > 0` and a bound on `sin g Δy` gives `Δx`. -/
theorem shift_x_lb {g Δx Δy S B : ℝ} (hc : 0 < Real.cos g) (h : Real.cos g * Δx + Real.sin g * Δy ≥ S)
    (hb : Real.sin g * Δy ≤ B) : (S - B) / Real.cos g ≤ Δx := by
  rw [div_le_iff₀ hc]; linarith

/-! ## P side, case b: 13-14 separated by 14's face `-e2` -/

/-- `n = e2 φ14 = (-sin φ14, cos φ14)`. Chain: square 2 lies beyond 14's top face, 13 beyond 14's
bottom face; square 2's centre is bounded by `X2 ≤ c2x` and the top wall. -/
theorem rowP_b {c2 c13 c14 : ℝ × ℝ} {φ2 φ13 φ14 L X2 : ℝ}
    (h214 : Sep c14 φ14 c2 φ2 1) (h1314 : Sep c14 φ14 c13 φ13 3)
    (hx : X2 ≤ c2.1) (hy : c2.2 ≤ L - supp φ2 (Real.pi / 2))
    (hs : 0 ≤ Real.sin φ14) (hc : 0 ≤ Real.cos φ14) :
    -Real.sin φ14 * c13.1 + Real.cos φ14 * c13.2 ≤
      -Real.sin φ14 * X2 + Real.cos φ14 * (L - supp φ2 (Real.pi / 2)) - supp φ2 (φ14 + Real.pi / 2)
        - 1 - supp φ13 (φ14 + Real.pi / 2) := by
  have g1 := sep_gap h214
  have g2 := sep_gap h1314
  have a1 : φ14 + ((1:ℕ):ℝ) * (Real.pi / 2) = φ14 + Real.pi / 2 := by push_cast; ring
  have a3 : φ14 + ((3:ℕ):ℝ) * (Real.pi / 2) = (φ14 + Real.pi / 2) + Real.pi := by push_cast; ring
  rw [a1, Real.cos_add_pi_div_two, Real.sin_add_pi_div_two] at g1
  rw [a3, supp_add_pi, Real.cos_add_pi, Real.sin_add_pi, Real.cos_add_pi_div_two,
    Real.sin_add_pi_div_two] at g2
  have m1 := mul_le_mul_of_nonneg_left hx hs
  have m2 := mul_le_mul_of_nonneg_left hy hc
  nlinarith

/-! ## Q side, case b: 13-11 separated by 11's face `-e1` -/

/-- `n = e1 φ11`. Chain: square 10 beyond 11's face `+e1`, inside the right and top walls; 13 beyond
11's face `-e1`. -/
theorem rowQ_b {c10 c11 c13 : ℝ × ℝ} {φ10 φ11 φ13 L : ℝ}
    (h1011 : Sep c11 φ11 c10 φ10 0) (h1311 : Sep c11 φ11 c13 φ13 2)
    (hx : c10.1 ≤ L - supp φ10 0) (hy : c10.2 ≤ L - supp φ10 (Real.pi / 2))
    (hc : 0 ≤ Real.cos φ11) (hs : 0 ≤ Real.sin φ11) :
    Real.cos φ11 * c13.1 + Real.sin φ11 * c13.2 ≤
      Real.cos φ11 * (L - supp φ10 0) + Real.sin φ11 * (L - supp φ10 (Real.pi / 2)) - supp φ10 φ11
        - 1 - supp φ13 φ11 := by
  have g1 := sep_gap h1011
  have g2 := sep_gap h1311
  have a0 : φ11 + ((0:ℕ):ℝ) * (Real.pi / 2) = φ11 := by push_cast; ring
  have a2 : φ11 + ((2:ℕ):ℝ) * (Real.pi / 2) = φ11 + Real.pi := by push_cast; ring
  rw [a0] at g1
  rw [a2, supp_add_pi, Real.cos_add_pi, Real.sin_add_pi] at g2
  have m1 := mul_le_mul_of_nonneg_left hx hc
  have m2 := mul_le_mul_of_nonneg_left hy hs
  nlinarith

/-! ## Floor F1: 8's top face `+e2` separates 13 -/

/-- `g8 ≥ 0`, 5-8 separated by 8's face `-e2`: with `w = e2 φ8`, `W8 = -sin φ8 X5 + cos φ8 Y5 + 1/2 + supp φ5 (φ8 + π/2)`
where `c5x ≤ X5`, `Y5 ≤ c5y`. -/
theorem rowF1_pos_owner8 {c5 c8 c13 : ℝ × ℝ} {φ5 φ8 φ13 X5 Y5 : ℝ}
    (h813 : Sep c8 φ8 c13 φ13 1) (h58 : Sep c8 φ8 c5 φ5 3)
    (hx : c5.1 ≤ X5) (hy : Y5 ≤ c5.2) (hs : 0 ≤ Real.sin φ8) (hc : 0 ≤ Real.cos φ8) :
    Real.sin φ8 * c13.1 - Real.cos φ8 * c13.2 ≤
      -((-Real.sin φ8 * X5 + Real.cos φ8 * Y5 + 1/2 + supp φ5 (φ8 + Real.pi / 2)) + 1/2
        + supp φ13 (φ8 + Real.pi / 2)) := by
  have g1 := sep_gap h813
  have g2 := sep_gap h58
  have a1 : φ8 + ((1:ℕ):ℝ) * (Real.pi / 2) = φ8 + Real.pi / 2 := by push_cast; ring
  have a3 : φ8 + ((3:ℕ):ℝ) * (Real.pi / 2) = (φ8 + Real.pi / 2) + Real.pi := by push_cast; ring
  rw [a1, Real.cos_add_pi_div_two, Real.sin_add_pi_div_two] at g1
  rw [a3, supp_add_pi, Real.cos_add_pi, Real.sin_add_pi, Real.cos_add_pi_div_two,
    Real.sin_add_pi_div_two] at g2
  have m1 := mul_le_mul_of_nonneg_left hx hs
  have m2 := mul_le_mul_of_nonneg_left hy hc
  nlinarith

/-- `g8 ≥ 0`, 5-8 separated by 5's face `+e2`: with `m = e2 φ5`, `t = e1 φ5`, `d = φ8 - φ5`
(`w = cos d m - sin d t`), any lower bound `M0 ≤ m.c5` and any `T0 ≥ sin d (t.c8)` give
`w.c8 ≥ cos d (M0 + 1/2 + supp φ8 (φ5 + π/2)) - T0`. -/
theorem rowF1_pos_owner5 {c5 c8 c13 : ℝ × ℝ} {φ5 φ8 φ13 M0 T0 : ℝ}
    (h813 : Sep c8 φ8 c13 φ13 1) (h58 : Sep c5 φ5 c8 φ8 1)
    (hm : M0 ≤ -Real.sin φ5 * c5.1 + Real.cos φ5 * c5.2)
    (ht : Real.sin (φ8 - φ5) * (Real.cos φ5 * c8.1 + Real.sin φ5 * c8.2) ≤ T0)
    (hcd : 0 ≤ Real.cos (φ8 - φ5)) :
    Real.sin φ8 * c13.1 - Real.cos φ8 * c13.2 ≤
      -((Real.cos (φ8 - φ5) * (M0 + 1/2 + supp φ8 (φ5 + Real.pi / 2)) - T0) + 1/2
        + supp φ13 (φ8 + Real.pi / 2)) := by
  have g1 := sep_gap h813
  have g2 := sep_gap h58
  have a1 : φ8 + ((1:ℕ):ℝ) * (Real.pi / 2) = φ8 + Real.pi / 2 := by push_cast; ring
  have a1' : φ5 + ((1:ℕ):ℝ) * (Real.pi / 2) = φ5 + Real.pi / 2 := by push_cast; ring
  rw [a1, Real.cos_add_pi_div_two, Real.sin_add_pi_div_two] at g1
  rw [a1', Real.cos_add_pi_div_two, Real.sin_add_pi_div_two] at g2
  -- w.c8 = cos d (m.c8) - sin d (t.c8)
  have hw : -Real.sin φ8 * c8.1 + Real.cos φ8 * c8.2 =
      Real.cos (φ8 - φ5) * (-Real.sin φ5 * c8.1 + Real.cos φ5 * c8.2) -
        Real.sin (φ8 - φ5) * (Real.cos φ5 * c8.1 + Real.sin φ5 * c8.2) := by
    rw [Real.cos_sub, Real.sin_sub]
    have h := Real.sin_sq_add_cos_sq φ5
    linear_combination (-(Real.sin φ8) * c8.1 + Real.cos φ8 * c8.2) * (-h) +
      0 * h
  have hmc8 : M0 + 1/2 + supp φ8 (φ5 + Real.pi / 2) ≤ -Real.sin φ5 * c8.1 + Real.cos φ5 * c8.2 := by linarith
  have := mul_le_mul_of_nonneg_left hmc8 hcd
  nlinarith

/-- `g8 < 0` (`sin φ8 ≤ 0`): with `Xh ≥ c13x - c8x` and `Y8 ≤ c8y`,
`c13y ≥ Y8 + (1/2 + supp φ13 (φ8 + π/2) - |sin φ8| Xh) / cos φ8`. -/
theorem rowF1_neg {c8 c13 : ℝ × ℝ} {φ8 φ13 Xh Y8 : ℝ}
    (h813 : Sep c8 φ8 c13 φ13 1) (hs : Real.sin φ8 ≤ 0) (hc : 0 < Real.cos φ8)
    (hX : c13.1 - c8.1 ≤ Xh) (hY : Y8 ≤ c8.2) :
    -c13.2 ≤ -(Y8 + (1/2 + supp φ13 (φ8 + Real.pi / 2) - |Real.sin φ8| * Xh) / Real.cos φ8) := by
  have g1 := sep_gap h813
  have a1 : φ8 + ((1:ℕ):ℝ) * (Real.pi / 2) = φ8 + Real.pi / 2 := by push_cast; ring
  rw [a1, Real.cos_add_pi_div_two, Real.sin_add_pi_div_two] at g1
  rw [abs_of_nonpos hs]
  have m := mul_le_mul_of_nonneg_left hX (neg_nonneg.mpr hs)
  have hy : (1/2 + supp φ13 (φ8 + Real.pi / 2) - -Real.sin φ8 * Xh) / Real.cos φ8 ≤ c13.2 - c8.2 := by
    rw [div_le_iff₀ hc]; nlinarith
  linarith

end Sq19.Endgame

#print axioms Sq19.Endgame.sep_gap
#print axioms Sq19.Endgame.wall_bounds
#print axioms Sq19.Endgame.rowP_b
#print axioms Sq19.Endgame.rowQ_b
#print axioms Sq19.Endgame.rowF1_pos_owner8
#print axioms Sq19.Endgame.rowF1_pos_owner5
#print axioms Sq19.Endgame.rowF1_neg
