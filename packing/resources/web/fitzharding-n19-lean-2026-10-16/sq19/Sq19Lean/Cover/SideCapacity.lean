import Sq17Lean.WallCapacityRectangle

/-!
# Capacity one for the side cells against one wall

All twelve side cells fit, after a symmetry of the container, in a box
`[x0, x0 + 7287/10000] × (-∞, 1387/1000]` next to the wall `y = 0`. The 17 project's
`wall_rectangle_capacity` applies with width `w = 7287/10000` and depth `d = 887/1000`; its
two numeric premises are proved here: the circle slack, and positivity of `wallPoly w d` on
`[0, 1]` by degree-4 Bernstein coefficients on three subintervals (least coefficient about
0.0017). This replaces the external certificate `capacity_cert side 7287 10000 887 1000 4000`.
-/
namespace Sq19.Cover
open Sq17.WallCapacity

private theorem bernstein_pos (x c0 c1 c2 c3 c4 : ℝ)
    (hx0 : 0 ≤ x) (hx1 : x ≤ 1)
    (hc0 : 0 < c0) (hc1 : 0 < c1) (hc2 : 0 < c2) (hc3 : 0 < c3) (hc4 : 0 < c4) :
    0 < c0 * (1-x)^4 + 4*c1*x*(1-x)^3 + 6*c2*x^2*(1-x)^2 +
      4*c3*x^3*(1-x) + c4*x^4 := by
  by_cases hx : x = 0
  · subst x
    simpa using hc0
  · have hp : 0 < x := lt_of_le_of_ne hx0 (Ne.symm hx)
    have hm : 0 ≤ 1-x := sub_nonneg.mpr hx1
    have h0 : 0 ≤ c0 * (1-x)^4 := by positivity
    have h1 : 0 ≤ 4*c1*x*(1-x)^3 := by positivity
    have h2 : 0 ≤ 6*c2*x^2*(1-x)^2 := by positivity
    have h3 : 0 ≤ 4*c3*x^3*(1-x) := by positivity
    have h4 : 0 < c4*x^4 := by positivity
    linarith

private theorem side_0 (b : ℝ) (hlo : 0 ≤ b) (hhi : b ≤ 1/3) :
    0 < wallPoly (7287/10000) (887/1000) b := by
  have h := bernstein_pos (3*b-0) (46899631/100000000) (89566393/300000000)
    (1012287343/5400000000) (627071881/5400000000) (144036383/2025000000)
    (by linarith) (by linarith) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num)
  convert h using 1
  unfold wallPoly
  ring

private theorem side_1 (b : ℝ) (hlo : 1/3 ≤ b) (hhi : b ≤ 2/3) :
    0 < wallPoly (7287/10000) (887/1000) b := by
  have h := bernstein_pos (3*b-1) (144036383/2025000000) (84673297/3240000000)
    (121163713/16200000000) (7081937/4050000000) (2750359/1620000000)
    (by linarith) (by linarith) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num)
  convert h using 1
  unfold wallPoly
  ring

private theorem side_2 (b : ℝ) (hlo : 2/3 ≤ b) (hhi : b ≤ 1) :
    0 < wallPoly (7287/10000) (887/1000) b := by
  have h := bernstein_pos (3*b-2) (2750359/1620000000) (1111643/675000000)
    (39289027/5400000000) (6804131/600000000) (12769/1000000)
    (by linarith) (by linarith) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num)
  convert h using 1
  unfold wallPoly
  ring

theorem side_poly_pos (b : ℝ) (hb0 : 0 ≤ b) (hb1 : b ≤ 1) :
    0 < wallPoly (7287/10000) (887/1000) b := by
  by_cases h1 : b ≤ 1/3
  · exact side_0 b hb0 h1
  by_cases h2 : b ≤ 2/3
  · exact side_1 b (by linarith) h2
  exact side_2 b (by linarith) hb1

/-- **One-wall side lemma.** Two unit squares above the wall `y = 0` whose centres lie in
`[x0, x0 + 7287/10000] × (-∞, 1387/1000]` do not have disjoint interiors. -/
theorem side_capacity (x0 : ℝ) (p q : ℝ × ℝ) (ux uy vx vy : ℝ)
    (hu : ux^2+uy^2=1) (hv : vx^2+vy^2=1)
    (hpfit : Sq17.sq p.1 p.2 ux uy ⊆ {z | 0 ≤ z.2})
    (hqfit : Sq17.sq q.1 q.2 vx vy ⊆ {z | 0 ≤ z.2})
    (hpx : x0 ≤ p.1 ∧ p.1 ≤ x0+7287/10000) (hqx : x0 ≤ q.1 ∧ q.1 ≤ x0+7287/10000)
    (hpy : p.2 ≤ 1387/1000) (hqy : q.2 ≤ 1387/1000) :
    ¬ Disjoint (interior (Sq17.sq p.1 p.2 ux uy)) (interior (Sq17.sq q.1 q.2 vx vy)) :=
  wall_rectangle_capacity (7287/10000) (887/1000) x0 p q ux uy vx vy
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) (by norm_num) side_poly_pos
    hu hv hpfit hqfit hpx hqx (by linarith) (by linarith)

end Sq19.Cover

#print axioms Sq19.Cover.side_capacity
