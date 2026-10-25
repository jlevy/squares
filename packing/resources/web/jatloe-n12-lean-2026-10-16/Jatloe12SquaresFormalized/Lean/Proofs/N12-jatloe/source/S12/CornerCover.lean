import S12.WallGeometry
import S12.Symmetry

namespace S12
open S12Pilot
set_option maxHeartbeats 0

theorem corner_upper_projection (a c s X Y : ℝ)
    (ha : 1<a) (hc : 0≤c) (hs : 0≤s) (hn : c^2+s^2=1)
    (hwX : a*(c+s)/2≤X) (hwY : a*(c+s)/2≤Y) :
    c*(1-X)+s*(1-Y)<a/2 := by
  have hx := mul_nonneg hc (sub_nonneg.mpr hwX)
  have hy := mul_nonneg hs (sub_nonneg.mpr hwY)
  have hp : 0<(a-1)*(1+(c+s)^2) := mul_pos (by linarith)
    (by nlinarith [sq_nonneg (c+s)])
  have hn' : a*c^2+a*s^2=a := by
    calc
      _ = a*(c^2+s^2) := by ring
      _ = a := by rw [hn,mul_one]
  nlinarith [sq_nonneg (c+s-1)]

/-- The corner-cover estimate underlying the initial marker set. -/
theorem corner_frame_point (a c s X Y b : ℝ)
    (ha : 1<a) (hc : 0≤c) (hs : 0≤s) (hn : c^2+s^2=1)
    (hwX : a*(c+s)/2≤X) (hwY : a*(c+s)/2≤Y)
    (hX : X≤1) (hY : Y≤1) (hb0 : 9/10≤b) (hb1 : b≤1) :
    InBands (-a/2) (-a/2) a (c*(b-X)+s*(1-Y)) (-s*(b-X)+c*(1-Y)) := by
  have hc1 : c≤1 := by nlinarith [sq_nonneg s,sq_nonneg (c-1)]
  have hs1 : s≤1 := by nlinarith [sq_nonneg c,sq_nonneg (s-1)]
  have hcs := mul_nonneg hc hs
  have hcx := mul_nonneg hc (sub_nonneg.mpr hX)
  have hsy := mul_nonneg hs (sub_nonneg.mpr hY)
  have hcy := mul_nonneg hc (sub_nonneg.mpr hY)
  have hsx := mul_nonneg hs (sub_nonneg.mpr hX)
  have hcb := mul_nonneg hc (sub_nonneg.mpr hb0)
  have hcb1 := mul_nonneg hc (sub_nonneg.mpr hb1)
  have hsb := mul_nonneg hs (sub_nonneg.mpr hb0)
  have hsb1 := mul_nonneg hs (sub_nonneg.mpr hb1)
  have hwc := mul_nonneg hc (sub_nonneg.mpr hwY)
  have hws := mul_nonneg hs (sub_nonneg.mpr hwX)
  have hup := corner_upper_projection a c s X Y ha hc hs hn hwX hwY
  have hstrictS : 0<(a-1)*(1+s*(c+s)) := mul_pos (by linarith)
    (by nlinarith [sq_nonneg s])
  have hstrictC : 0<(a-1)*(1+c*(c+s)) := mul_pos (by linarith)
    (by nlinarith [sq_nonneg c])
  have hpoly : 0≤1+c*(c+s)-2*c-s/5 := by
    by_cases hh : c≤1/5
    · nlinarith [sq_nonneg c]
    · have hp := mul_nonneg hs (show 0≤c-1/5 by linarith)
      nlinarith [sq_nonneg (c-1)]
  dsimp [InBands]
  refine ⟨?_,?_,?_,?_⟩ <;>
    nlinarith [sq_nonneg (s-1)]

/-- A square centered in the unit corner and contained in the first quadrant
contains every (b,1) with 0.9 ≤ b ≤ 1. -/
theorem corner_nonavoidance_horizontal (q : OpenSquare) (ha : 1<q.side)
    (hwall : ∀ x y, q.Inside x y → 0≤x ∧ 0≤y)
    (hX : centerX q≤1) (hY : centerY q≤1) (b : ℝ)
    (hb0 : 9/10≤b) (hb1 : b≤1) : q.Inside b 1 := by
  obtain ⟨r,hc,hs,hside,hcenX,hcenY,hinside⟩ := exists_positive_frame q
  have hw : ∀ x y, r.Inside x y → 0≤x ∧ 0≤y := by
    intro x y hi; exact hwall x y ((hinside x y).mp hi)
  obtain ⟨hwX,hwY⟩ := positive_frame_wall_bounds r hc hs hw
  apply (hinside b 1).mp
  apply (inside_centered_iff r b 1).mpr
  apply corner_frame_point r.side r.c r.s (centerX r) (centerY r) b
    (by simpa [hside] using ha) hc hs r.unit_normal hwX hwY
    (by simpa [hcenX] using hX) (by simpa [hcenY] using hY) hb0 hb1

#print axioms corner_nonavoidance_horizontal
end S12
