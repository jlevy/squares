import Sq17Lean.WallCapacityRectangle

/-!
# Capacity one for a corner cell against two walls

Two unit squares inside the quadrant `x, y ≥ 0` whose centres both satisfy
`x ≤ 27/20` and `y ≤ 27/20` cannot have disjoint interiors.

The proof uses a unit separating normal `(a, b)` of the two squares (17 project,
`square_disjoint_unit_separator`) and splits on the signs of `a` and `b`.
* Same signs: the walls bound both centre coordinates of the lower square from below by its
  axis supports, and `corner_support_bound` below shows the sum of three supports is too large.
  Its proof writes the direction of the square as a nonnegative combination of `(1,0)` and the
  normal, so the bound reduces to its value at those two directions.
* Opposite signs: each square meets one wall in the separating direction, and the 17 project's
  `mixed_support_normal` bounds both, leaving the scalar inequality `opposite_scalar`.
This replaces the external certificate `s19/tools/capacity_cert.c corner 17 20 2000`.
-/
namespace Sq19.Cover
open Sq17.WallCapacity

/-- First-quadrant core of the same-sign case. -/
private theorem corner_core (a b c s : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c)
    (hs : 0 ≤ s) (hab : a^2+b^2 = 1) (hcs : c^2+s^2 = 1) (hsec : a*s ≤ b*c) :
    0 < 2*c*(a+b)+2*b*s+1-27/10*(a+b) := by
  have hσ : (a+b)^2 ≤ 2 := by nlinarith [sq_nonneg (a-b)]
  have hσ1 : 1 ≤ a+b := by nlinarith
  have hσ2 : a+b < 10/7 := by nlinarith
  have ha1 : a ≤ 1 := by nlinarith
  -- values at the directions (1,0) and (a,b)
  have hE0 : 0 < 1-7/10*(a+b) := by linarith
  have hE1 : 0 < 2*a*(a+b)+2*b^2+1-27/10*(a+b) := by nlinarith [sq_nonneg (a+b-27/20)]
  obtain ⟨l, hl⟩ : ∃ l, l = b*c-a*s := ⟨_, rfl⟩
  have hl0 : 0 ≤ l := by rw [hl]; linarith
  -- b (c,s) = l (1,0) + s (a,b), so b ≤ l + s
  have hnorm : b^2 = (l+s*a)^2+(s*b)^2 := by
    rw [hl]; linear_combination (-b^2) * hcs
  have hbls : b ≤ l+s := by
    have e : (l+s)^2-b^2 = 2*l*s*(1-a) := by linear_combination (-s^2)*hab - hnorm
    have h2 : b^2 ≤ (l+s)^2 := by
      have := mul_nonneg (mul_nonneg hl0 hs) (sub_nonneg.mpr ha1)
      linarith
    by_contra hc
    push Not at hc
    have := mul_lt_mul'' hc hc (add_nonneg hl0 hs) (add_nonneg hl0 hs)
    nlinarith
  have hK : 1-27/10*(a+b) < 0 := by linarith
  have hid : b*(2*c*(a+b)+2*b*s+1-27/10*(a+b)) =
      l*(1-7/10*(a+b)) + s*(2*a*(a+b)+2*b^2+1-27/10*(a+b)) +
      (b-l-s)*(1-27/10*(a+b)) := by rw [hl]; ring
  rcases eq_or_lt_of_le hb with hb0 | hbpos
  · subst hb0
    have ha1 : a = 1 := by nlinarith
    subst ha1
    have hs0 : s = 0 := by linarith
    subst hs0
    have hc1 : c = 1 := by nlinarith
    subst hc1
    norm_num
  · have hpos : 0 < l*(1-7/10*(a+b)) + s*(2*a*(a+b)+2*b^2+1-27/10*(a+b)) := by
      rcases eq_or_lt_of_le hl0 with hl' | hl'
      · have : 0 < s := by linarith
        rw [← hl', zero_mul, zero_add]
        exact mul_pos this hE1
      · exact add_pos_of_pos_of_nonneg (mul_pos hl' hE0) (mul_nonneg hs hE1.le)
    have hrest : 0 ≤ (b-l-s)*(1-27/10*(a+b)) :=
      mul_nonneg_of_nonpos_of_nonpos (by linarith) hK.le
    have : 0 < b*(2*c*(a+b)+2*b*s+1-27/10*(a+b)) := by
      rw [hid]; exact add_pos_of_pos_of_nonneg hpos hrest
    exact pos_of_mul_pos_right this hb

/-- First-quadrant form of the same-sign bound. -/
private theorem corner_quadrant (a b c s : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : 0 ≤ c)
    (hs : 0 ≤ s) (hab : a^2+b^2 = 1) (hcs : c^2+s^2 = 1) :
    27/10*(a+b) < |a*c+b*s|+|b*c-a*s|+(a+b)*(c+s)+1 := by
  rw [abs_of_nonneg (by positivity : 0 ≤ a*c+b*s)]
  rcases le_total (a*s) (b*c) with h | h
  · rw [abs_of_nonneg (by linarith : 0 ≤ b*c-a*s)]
    have := corner_core a b c s ha hb hc hs hab hcs h
    nlinarith
  · rw [abs_of_nonpos (by linarith : b*c-a*s ≤ 0)]
    have := corner_core b a s c hb ha hs hc (by linarith) (by linarith) h
    nlinarith

/-- Same-sign case: for a normal `(a, b)` in the closed first quadrant and any unit
direction `(ux, uy)`, the sum `2 h(a,b) + (a+b)(|ux|+|uy|) + 1` exceeds `27/10 (a+b)`,
where `2 h(a,b) = |a ux + b uy| + |b ux - a uy|` is twice the square's support. -/
theorem corner_support_bound (a b ux uy : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hab : a^2+b^2 = 1) (hu : ux^2+uy^2 = 1) :
    27/10*(a+b) < |a*ux+b*uy|+|b*ux-a*uy|+(a+b)*(|ux|+|uy|)+1 := by
  rcases le_total 0 ux with hx | hx <;> rcases le_total 0 uy with hy | hy
  · rw [abs_of_nonneg hx, abs_of_nonneg hy]
    exact corner_quadrant a b ux uy ha hb hx hy hab hu
  · -- (ux,uy) = quarter turn of (-uy, ux)
    have h := corner_quadrant a b (-uy) ux ha hb (by linarith) hx hab (by nlinarith)
    rw [abs_of_nonneg hx, abs_of_nonpos hy]
    have e1 : a*(-uy)+b*ux = b*ux-a*uy := by ring
    have e2 : b*(-uy)-a*ux = -(a*ux+b*uy) := by ring
    rw [e1, e2, abs_neg] at h
    linarith
  · have h := corner_quadrant a b uy (-ux) ha hb hy (by linarith) hab (by nlinarith)
    rw [abs_of_nonpos hx, abs_of_nonneg hy]
    have e1 : a*uy+b*(-ux) = -(b*ux-a*uy) := by ring
    have e2 : b*uy-a*(-ux) = a*ux+b*uy := by ring
    rw [e1, e2, abs_neg] at h
    linarith
  · have h := corner_quadrant a b (-ux) (-uy) ha hb (by linarith) (by linarith) hab
      (by nlinarith)
    rw [abs_of_nonpos hx, abs_of_nonpos hy]
    have e1 : a*(-ux)+b*(-uy) = -(a*ux+b*uy) := by ring
    have e2 : b*(-ux)-a*(-uy) = -(b*ux-a*uy) := by ring
    rw [e1, e2, abs_neg, abs_neg] at h
    linarith

/-- Opposite-sign scalar inequality, `x = |a|`, `y = |b|`. -/
theorem opposite_scalar (x y : ℝ) (hx : 0 ≤ x) (hy : 0 ≤ y) (h : x^2+y^2 = 1) :
    27/10*(x+y) < min (y+2*x) (1+y*x+x^2) + min (x+2*y) (1+x*y+y^2) := by
  have hσ1 : 1 ≤ x+y := by nlinarith
  have hσ : (x+y)^2 ≤ 2 := by nlinarith [sq_nonneg (x-y)]
  rcases min_choice (y+2*x) (1+y*x+x^2) with h1 | h1 <;>
    rcases min_choice (x+2*y) (1+x*y+y^2) with h2 | h2 <;> rw [h1, h2]
  · nlinarith
  · nlinarith [sq_nonneg (y-3/10), sq_nonneg (x+y-27/20), mul_nonneg hx hy]
  · nlinarith [sq_nonneg (x-3/10), sq_nonneg (x+y-27/20), mul_nonneg hx hy]
  · nlinarith [sq_nonneg (x+y-27/20), mul_nonneg hx hy]


/-- Twice the support of a square, written out. -/
private theorem two_support (ux uy a b : ℝ) :
    2*squareSupport ux uy a b = |a*ux+b*uy|+|b*ux-a*uy| := by
  unfold squareSupport; ring

private theorem support_axis_x (ux uy : ℝ) : 2*squareSupport ux uy 1 0 = |ux|+|uy| := by
  rw [two_support]; simp [abs_neg]

private theorem support_axis_y (ux uy : ℝ) : 2*squareSupport ux uy 0 1 = |ux|+|uy| := by
  rw [two_support]; simp [add_comm]

/-- The left wall bounds the centre's first coordinate by the horizontal support. -/
theorem squareSupport_wall_bound_x (cx cy ux uy : ℝ) (hu : ux^2+uy^2=1)
    (hfit : Sq17.sq cx cy ux uy ⊆ {p | 0 ≤ p.1}) :
    squareSupport ux uy 1 0 ≤ cx := by
  obtain ⟨z,hz,he⟩ := squareSupport_attained cx cy ux uy (-1) 0 hu
  have hs : squareSupport ux uy (-1) 0 = squareSupport ux uy 1 0 := by
    simpa using squareSupport_neg ux uy 1 0
  rw [hs] at he
  have h0 : 0 ≤ z.1 := hfit hz
  linarith

/-- Same-sign separator: the square `P` is the lower-left one. -/
private theorem corner_same_sign (p q : ℝ × ℝ) (ux uy vx vy a b : ℝ)
    (hu : ux^2+uy^2=1) (hv : vx^2+vy^2=1) (hm : a^2+b^2=1) (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hpx : squareSupport ux uy 1 0 ≤ p.1) (hpy : squareSupport ux uy 0 1 ≤ p.2)
    (hq1 : q.1 ≤ 27/20) (hq2 : q.2 ≤ 27/20)
    (hsep : squareSupport ux uy a b+squareSupport vx vy a b ≤ a*(q.1-p.1)+b*(q.2-p.2)) :
    False := by
  have hQ := squareSupport_ge_half vx vy a b hv hm
  have hK := corner_support_bound a b ux uy ha hb hm hu
  rw [← two_support, ← support_axis_x] at hK
  have e : squareSupport ux uy 1 0 = squareSupport ux uy 0 1 := by
    have h1 := support_axis_x ux uy; have h2 := support_axis_y ux uy; linarith
  have h1 := mul_le_mul_of_nonneg_left hpx ha
  have h2 := mul_le_mul_of_nonneg_left hpy hb
  have h3 := mul_le_mul_of_nonneg_left hq1 ha
  have h4 := mul_le_mul_of_nonneg_left hq2 hb
  rw [e] at h1 hK
  nlinarith

/-- Opposite-sign separator `a ≥ 0 ≥ b`: `P` meets the left wall, `Q` the bottom wall. -/
private theorem corner_opposite_sign (p q : ℝ × ℝ) (ux uy vx vy a b : ℝ)
    (hu : ux^2+uy^2=1) (hv : vx^2+vy^2=1) (hm : a^2+b^2=1) (ha : 0 ≤ a) (hb : b ≤ 0)
    (hpx : squareSupport ux uy 1 0 ≤ p.1) (hqy : squareSupport vx vy 0 1 ≤ q.2)
    (hq1 : q.1 ≤ 27/20) (hp2 : p.2 ≤ 27/20)
    (hsep : squareSupport ux uy a b+squareSupport vx vy a b ≤ a*(q.1-p.1)+b*(q.2-p.2)) :
    False := by
  have hU := mixed_support_normal b a uy ux ha (by linarith) (by linarith)
  have hV := mixed_support_normal (-a) (-b) vx vy (by linarith) (by linarith) (by linarith)
  have hS := opposite_scalar a (-b) ha (by linarith) (by linarith)
  have eU : |b*uy+a*ux|+|a*uy-b*ux|+a*(|uy|+|ux|) =
      2*squareSupport ux uy a b + a*(2*squareSupport ux uy 1 0) := by
    rw [two_support, support_axis_x]
    have e1 : b*uy+a*ux = a*ux+b*uy := by ring
    have e2 : a*uy-b*ux = -(b*ux-a*uy) := by ring
    rw [e1, e2, abs_neg]; ring
  have eV : |(-a)*vx+(-b)*vy|+|(-b)*vx-(-a)*vy|+(-b)*(|vx|+|vy|) =
      2*squareSupport vx vy a b + (-b)*(2*squareSupport vx vy 0 1) := by
    rw [two_support, support_axis_y]
    have e1 : (-a)*vx+(-b)*vy = -(a*vx+b*vy) := by ring
    have e2 : (-b)*vx-(-a)*vy = -(b*vx-a*vy) := by ring
    rw [e1, e2, abs_neg, abs_neg]
  rw [eU] at hU
  rw [eV] at hV
  have eabs : |b| = -b := abs_of_nonpos hb
  have eabs' : |-a| = a := by rw [abs_neg, abs_of_nonneg ha]
  rw [eabs] at hU
  rw [eabs'] at hV
  have hmin : 27/10*(a+-b) < 2*squareSupport ux uy a b + a*(2*squareSupport ux uy 1 0) +
      (2*squareSupport vx vy a b + (-b)*(2*squareSupport vx vy 0 1)) := by
    have e3 : (1+(-b)*a+a^2) = 1+-b*a+a^2 := by ring
    have e4 : (1+a*(-b)+(-b)^2) = 1+a*-b+(-b)^2 := by ring
    linarith
  have h1 := mul_le_mul_of_nonneg_left hpx ha
  have h2 := mul_le_mul_of_nonneg_left hqy (by linarith : 0 ≤ -b)
  have h3 := mul_le_mul_of_nonneg_left hq1 ha
  have h4 := mul_le_mul_of_nonneg_left hp2 (by linarith : 0 ≤ -b)
  nlinarith

/-- **Two-wall corner lemma.** Two unit squares inside the quadrant `x, y ≥ 0` with both
centres in `(-∞, 27/20]^2` do not have disjoint interiors. -/
theorem corner_capacity (p q : ℝ × ℝ) (ux uy vx vy : ℝ)
    (hu : ux^2+uy^2=1) (hv : vx^2+vy^2=1)
    (hpfit : Sq17.sq p.1 p.2 ux uy ⊆ {z | 0 ≤ z.1 ∧ 0 ≤ z.2})
    (hqfit : Sq17.sq q.1 q.2 vx vy ⊆ {z | 0 ≤ z.1 ∧ 0 ≤ z.2})
    (hp1 : p.1 ≤ 27/20) (hp2 : p.2 ≤ 27/20) (hq1 : q.1 ≤ 27/20) (hq2 : q.2 ≤ 27/20) :
    ¬ Disjoint (interior (Sq17.sq p.1 p.2 ux uy)) (interior (Sq17.sq q.1 q.2 vx vy)) := by
  intro hdis
  obtain ⟨a,b,hm,hsep⟩ := square_disjoint_unit_separator p q ux uy vx vy hu hv hdis
  have hpx := squareSupport_wall_bound_x p.1 p.2 ux uy hu (fun z hz => (hpfit hz).1)
  have hpy := squareSupport_wall_bound p.1 p.2 ux uy hu (fun z hz => (hpfit hz).2)
  have hqx := squareSupport_wall_bound_x q.1 q.2 vx vy hv (fun z hz => (hqfit hz).1)
  have hqy := squareSupport_wall_bound q.1 q.2 vx vy hv (fun z hz => (hqfit hz).2)
  -- the separator read from `q` to `p`
  have hsep' : squareSupport vx vy (-a) (-b)+squareSupport ux uy (-a) (-b) ≤
      (-a)*(p.1-q.1)+(-b)*(p.2-q.2) := by
    rw [squareSupport_neg, squareSupport_neg]; linarith
  have hm' : (-a)^2+(-b)^2 = 1 := by linarith [neg_sq a, neg_sq b]
  rcases le_total 0 a with ha | ha <;> rcases le_total 0 b with hb | hb
  · exact corner_same_sign p q ux uy vx vy a b hu hv hm ha hb hpx hpy hq1 hq2 hsep
  · exact corner_opposite_sign p q ux uy vx vy a b hu hv hm ha hb hpx hqy hq1 hp2 hsep
  · exact corner_opposite_sign q p vx vy ux uy (-a) (-b) hv hu hm' (by linarith)
      (by linarith) hqx hpy hp1 hq2 hsep'
  · exact corner_same_sign q p vx vy ux uy (-a) (-b) hv hu hm' (by linarith) (by linarith)
      hqx hqy hp1 hp2 hsep'

end Sq19.Cover

#print axioms Sq19.Cover.corner_capacity
