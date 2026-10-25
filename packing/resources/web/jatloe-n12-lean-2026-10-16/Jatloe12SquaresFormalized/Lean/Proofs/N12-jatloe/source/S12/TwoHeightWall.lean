import S12.WallRowCover

namespace S12
open S12Pilot
set_option maxHeartbeats 0

/-- Two nearby points at possibly unequal heights suffice. The rectangle
extends to the higher point, which is convenient for covering subdivisions. -/
theorem two_height_wall_frame (a c s X Y w b d : ℝ)
    (ha : 1<a) (hc : 0≤c) (hs : 0≤s) (hn : c^2+s^2=1)
    (hw : a*(c+s)/2≤Y) (hX0 : 0≤X) (hX1 : X≤w)
    (hw0 : 0≤w) (hw1 : w≤4/5) (hY : Y≤d)
    (hb0 : 9/10≤b) (hbd : b≤d) (hd1 : d≤1) :
    InBands (-a/2) (-a/2) a (-c*X+s*(b-Y)) (s*X+c*(b-Y)) ∨
    InBands (-a/2) (-a/2) a (c*(w-X)+s*(d-Y)) (-s*(w-X)+c*(d-Y)) := by
  have hc1 : c≤1 := by nlinarith [sq_nonneg s,sq_nonneg (c-1)]
  have hs1 : s≤1 := by nlinarith [sq_nonneg c,sq_nonneg (s-1)]
  have hcs := mul_nonneg hc hs
  have ht1 : 1≤c+s := by nlinarith [sq_nonneg (c+s-1)]
  have htmax : c+s≤3/2 := by nlinarith [sq_nonneg (c-s),sq_nonneg (c+s-3/2)]
  have hstrict : 0<(a-1)*(c+s) := mul_pos (by linarith) (by linarith)
  have hcX := mul_nonneg hc hX0
  have hsX := mul_nonneg hs hX0
  have hcX1 := mul_nonneg hc (sub_nonneg.mpr hX1)
  have hsX1 := mul_nonneg hs (sub_nonneg.mpr hX1)
  have hcd := mul_nonneg hc (sub_nonneg.mpr hY)
  have hsd := mul_nonneg hs (sub_nonneg.mpr hY)
  have hcw := mul_nonneg hc (sub_nonneg.mpr hw)
  have hsw := mul_nonneg hs (sub_nonneg.mpr hw)
  have hcb := mul_nonneg hc (show 0≤1-d by linarith)
  have hsb := mul_nonneg hs (show 0≤1-b by linarith)
  have hstrictS : 0<(a-1)*(1+s*(c+s)) := mul_pos (by linarith)
    (by nlinarith [sq_nonneg s])
  have hstrictC : 0<(a-1)*(1+c*(c+s)) := mul_pos (by linarith)
    (by nlinarith [sq_nonneg c])
  have hupS : s*(b-Y)<a/2 := by nlinarith [sq_nonneg (s-1)]
  have hupC : c*(d-Y)<a/2 := by nlinarith [sq_nonneg (c-1)]
  have hloC : -a/2<s*X+c*(b-Y) := by
    have hl := mul_nonneg hc (show 0≤b-Y+1/10 by linarith)
    nlinarith
  have hnormY : Y*c^2+Y*s^2=Y := by
    calc
      _ = Y*(c^2+s^2) := by ring
      _ = Y := by rw [hn,mul_one]
  have hlength : w^2+(d-b)^2≤1 := by
    have hww := mul_nonneg hw0 (sub_nonneg.mpr hw1)
    have hdd := mul_nonneg (sub_nonneg.mpr hbd) (show 0≤1/10-(d-b) by linarith)
    nlinarith
  let normalSquare : OpenSquare := {
    c := c
    s := s
    loU := 0
    loV := 0
    side := 1
    unit_normal := hn
    side_pos := by norm_num }
  obtain ⟨du0,du1,dv0,dv1⟩ := short_projections normalSquare w (d-b) hlength
  dsimp [normalSquare] at du0 du1 dv0 dv1
  by_contra he
  obtain ⟨hp,hq⟩ := not_or.mp he
  have hp' : -c*X+s*(b-Y)≤-a/2 ∨ a/2≤s*X+c*(b-Y) := by
    simp only [InBands,not_and_or,not_lt] at hp
    rcases hp with hp | hp | hp | hp
    · exact Or.inl hp
    · exfalso; linarith
    · exfalso; linarith
    · right; linarith
  have hq' : a/2≤c*(w-X)+s*(d-Y) ∨ -s*(w-X)+c*(d-Y)≤-a/2 := by
    simp only [InBands,not_and_or,not_lt] at hq
    rcases hq with hq | hq | hq | hq
    · exfalso; linarith
    · left; linarith
    · exact Or.inr hq
    · exfalso; linarith
  rcases hp' with hp' | hp'
  · rcases hq' with hq' | hq'
    · nlinarith only [hp',hq',du1,ha]
    · have p := mul_nonneg hs (sub_nonneg.mpr hp')
      have q := mul_nonneg hc (sub_nonneg.mpr hq')
      have hdelta := mul_nonneg (sq_nonneg s) (show 0≤1/10-(d-b) by linarith)
      have hwidth := mul_nonneg hcs (sub_nonneg.mpr hw1)
      have hnormD : d*c^2+d*s^2=d := by
        calc
          _ = d*(c^2+s^2) := by ring
          _ = d := by rw [hn,mul_one]
      nlinarith only [p,q,hnormY,hnormD,hdelta,hwidth,hY,hstrict,ht1,hn,
        sq_nonneg (c-s),sq_nonneg c]
  · rcases hq' with hq' | hq'
    · have p := mul_nonneg hc (sub_nonneg.mpr hp')
      have q := mul_nonneg hs (sub_nonneg.mpr hq')
      have hwidth := mul_nonneg hcs (sub_nonneg.mpr hw1)
      have hb := mul_nonneg (sq_nonneg c) (show 0≤1-b by linarith)
      have hd := mul_nonneg (sq_nonneg s) (show 0≤1-d by linarith)
      have hpoly := mul_nonneg (show 0≤3/5-(2/5)*(c+s) by linarith)
        (show 0≤c+s-1 by linarith)
      nlinarith only [p,q,hnormY,hwidth,hb,hd,hpoly,hw,hstrict,hn]
    · nlinarith only [hp',hq',dv0,ha]

theorem two_height_wall_nonavoidance (q : OpenSquare) (ha : 1<q.side)
    (hwall : ∀ x y, q.Inside x y → 0≤y) (w b d : ℝ)
    (hX0 : 0≤centerX q) (hX1 : centerX q≤w) (hY : centerY q≤d)
    (hw0 : 0≤w) (hw1 : w≤4/5) (hb : 9/10≤b) (hbd : b≤d) (hd : d≤1) :
    q.Inside 0 b ∨ q.Inside w d := by
  obtain ⟨r,hc,hs,hside,hcenX,hcenY,hinside⟩ := exists_positive_frame q
  have hw : ∀ x y, r.Inside x y → 0≤y := by
    intro x y hi; exact hwall x y ((hinside x y).mp hi)
  have h := two_height_wall_frame r.side r.c r.s (centerX r) (centerY r) w b d
    (by simpa [hside] using ha) hc hs r.unit_normal (bottom_wall_bound r hw)
    (by simpa [hcenX] using hX0) (by simpa [hcenX] using hX1) hw0 hw1
    (by simpa [hcenY] using hY) hb hbd hd
  have h0 : r.Inside 0 b ∨ r.Inside w d := by
    simpa [inside_centered_iff] using h
  exact h0.imp ((hinside _ _).mp) ((hinside _ _).mp)

#print axioms two_height_wall_nonavoidance
end S12
