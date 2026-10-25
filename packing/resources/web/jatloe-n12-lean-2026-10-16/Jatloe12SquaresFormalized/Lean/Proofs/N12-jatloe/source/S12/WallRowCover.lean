import S12.CornerCover

namespace S12
open S12Pilot
set_option maxHeartbeats 0

/-- The narrow wall-row instance needed for the 16 markers. -/
theorem wall_row_frame (a c s X Y b : ℝ)
    (ha : 1<a) (hc : 0≤c) (hs : 0≤s) (hn : c^2+s^2=1)
    (hw : a*(c+s)/2≤Y) (hX0 : 0≤X) (hX1 : X≤1)
    (hY : Y≤b) (hb : b≤457/500) :
    InBands (-a/2) (-a/2) a (-c*X+s*(b-Y)) (s*X+c*(b-Y)) ∨
    InBands (-a/2) (-a/2) a (c*(1-X)+s*(b-Y)) (-s*(1-X)+c*(b-Y)) := by
  have hc1 : c≤1 := by nlinarith [sq_nonneg s,sq_nonneg (c-1)]
  have hs1 : s≤1 := by nlinarith [sq_nonneg c,sq_nonneg (s-1)]
  have hcs := mul_nonneg hc hs
  have ht1 : 1≤c+s := by nlinarith [sq_nonneg (c+s-1)]
  have htmax : c+s≤99/70 := by nlinarith [sq_nonneg (c-s),sq_nonneg (c+s-99/70)]
  have hstrict : 0<(a-1)*(c+s) := mul_pos (by linarith) (by linarith)
  have hcX := mul_nonneg hc hX0
  have hsX := mul_nonneg hs hX0
  have hcX1 := mul_nonneg hc (sub_nonneg.mpr hX1)
  have hsX1 := mul_nonneg hs (sub_nonneg.mpr hX1)
  have hcd := mul_nonneg hc (sub_nonneg.mpr hY)
  have hsd := mul_nonneg hs (sub_nonneg.mpr hY)
  have hcw := mul_nonneg hc (sub_nonneg.mpr hw)
  have hsw := mul_nonneg hs (sub_nonneg.mpr hw)
  have hcb := mul_nonneg hc (show 0≤1-b by linarith)
  have hsb := mul_nonneg hs (show 0≤1-b by linarith)
  have hstrictS : 0<(a-1)*(1+s*(c+s)) := mul_pos (by linarith)
    (by nlinarith [sq_nonneg s])
  have hstrictC : 0<(a-1)*(1+c*(c+s)) := mul_pos (by linarith)
    (by nlinarith [sq_nonneg c])
  have hupS : s*(b-Y)<a/2 := by nlinarith [sq_nonneg (s-1)]
  have hupC : c*(b-Y)<a/2 := by nlinarith [sq_nonneg (c-1)]
  have hnormD : (b-Y)*c^2+(b-Y)*s^2=b-Y := by
    calc
      _ = (b-Y)*(c^2+s^2) := by ring
      _ = b-Y := by rw [hn,mul_one]
  by_contra he
  obtain ⟨hp,hq⟩ := not_or.mp he
  have hp' : -c*X+s*(b-Y)≤-a/2 ∨ a/2≤s*X+c*(b-Y) := by
    simp only [InBands,not_and_or,not_lt] at hp
    rcases hp with hp | hp | hp | hp
    · exact Or.inl hp
    · exfalso; linarith
    · exfalso; linarith
    · right; linarith
  have hq' : a/2≤c*(1-X)+s*(b-Y) ∨ -s*(1-X)+c*(b-Y)≤-a/2 := by
    simp only [InBands,not_and_or,not_lt] at hq
    rcases hq with hq | hq | hq | hq
    · exfalso; linarith
    · left; linarith
    · exact Or.inr hq
    · exfalso; linarith
  rcases hp' with hp' | hp'
  · rcases hq' with hq' | hq'
    · linarith
    · have p := mul_nonneg hs (sub_nonneg.mpr hp')
      have q := mul_nonneg hc (sub_nonneg.mpr hq')
      nlinarith [sq_nonneg (c-s)]
  · rcases hq' with hq' | hq'
    · have p := mul_nonneg hc (sub_nonneg.mpr hp')
      have q := mul_nonneg hs (sub_nonneg.mpr hq')
      have hbound := mul_nonneg (show 0≤99/70-(c+s) by linarith)
        (show 0≤c+s-1+29/70 by linarith)
      nlinarith
    · linarith

/-- One wall suffices for the corresponding center bound. -/
theorem bottom_wall_bound (q : OpenSquare)
    (hwall : ∀ x y, q.Inside x y → 0≤y) : q.side*(q.c+q.s)/2≤centerY q := by
  have hy : 0≤q.s*q.loU+q.c*q.loV := by
    apply affine_endpoint_nonnegative q.side (q.c+q.s) _ q.side_pos
    intro t ht0 ht1
    let u := q.loU+t
    let v := q.loV+t
    have hi : q.Inside (q.c*u-q.s*v) (q.s*u+q.c*v) := by
      apply (inside_iff_rotated_box q _ _).mpr
      refine ⟨u,v,?_,rfl,rfl⟩
      dsimp [u,v,InBands]; refine ⟨?_,?_,?_,?_⟩ <;> linarith
    have hh := hwall _ _ hi
    dsimp [u,v] at hh
    nlinarith
  dsimp [centerY]
  nlinarith

theorem wall_row_nonavoidance (q : OpenSquare) (ha : 1<q.side)
    (hwall : ∀ x y, q.Inside x y → 0≤y)
    (hX0 : 0≤centerX q) (hX1 : centerX q≤1)
    (hY : centerY q≤457/500) :
    q.Inside 0 (457/500) ∨ q.Inside 1 (457/500) := by
  obtain ⟨r,hc,hs,hside,hcenX,hcenY,hinside⟩ := exists_positive_frame q
  have hw : ∀ x y, r.Inside x y → 0≤y := by
    intro x y hi; exact hwall x y ((hinside x y).mp hi)
  have h := wall_row_frame r.side r.c r.s (centerX r) (centerY r) (457/500)
    (by simpa [hside] using ha) hc hs r.unit_normal (bottom_wall_bound r hw)
    (by simpa [hcenX] using hX0) (by simpa [hcenX] using hX1)
    (by simpa [hcenY] using hY) (by rfl)
  have h0 : r.Inside 0 (457/500) ∨ r.Inside 1 (457/500) := by
    simpa [inside_centered_iff] using h
  exact h0.imp ((hinside _ _).mp) ((hinside _ _).mp)

#print axioms wall_row_nonavoidance
end S12
