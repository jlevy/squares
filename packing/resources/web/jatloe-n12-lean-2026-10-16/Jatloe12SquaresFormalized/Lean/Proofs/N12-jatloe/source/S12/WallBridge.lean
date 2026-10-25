import S12.CornerForcing

namespace S12
open S12Pilot
set_option maxHeartbeats 0

theorem left_wall_vertex (q : OpenSquare)
    (hwall : ∀ x y, q.Inside x y → 0≤x) :
    0≤q.c*q.loU-q.s*(q.loV+q.side) := by
  apply affine_endpoint_nonnegative q.side (q.c+q.s) _ q.side_pos
  intro t ht0 ht1
  let u := q.loU+t
  let v := q.loV+q.side-t
  have hi : q.Inside (q.c*u-q.s*v) (q.s*u+q.c*v) := by
    apply (inside_iff_rotated_box q _ _).mpr
    refine ⟨u,v,?_,rfl,rfl⟩
    dsimp [u,v,InBands]; refine ⟨?_,?_,?_,?_⟩ <;> linarith
  have hh := hwall _ _ hi
  dsimp [u,v] at hh
  nlinarith

/-- A rational polynomial estimate replaces the square-root calculation in
the informal wall-bridge argument. -/
theorem wall_bridge_algebra (a c s t : ℝ) (ha : 1<a)
    (hc : 0≤c) (hs : 0≤s) (hn : c^2+s^2=1)
    (ht : t≤7/4) (hang : c*(457/500)+2*s<c+s*t)
    (hbound : a*c≤c^2+(457/500)*s^2-(2-t)*c*s) : False := by
  have hts := mul_nonneg hs (show 0≤7/4-t by linarith)
  have hsc : s≤(43/125)*c := by nlinarith
  have hcs : s≤c := by nlinarith
  have hc1 : c≤1 := by nlinarith [sq_nonneg s,sq_nonneg (c-1)]
  have hc2 : 2/3≤c := by
    by_contra he
    have he' : c<2/3 := lt_of_not_ge he
    have hs2 : s<2/3 := lt_of_le_of_lt hcs he'
    nlinarith [mul_nonneg hc (show 0≤2/3-c by linarith),
      mul_nonneg hs (show 0≤2/3-s by linarith)]
  have htC := mul_nonneg hc (show 0≤7/4-t by linarith)
  have hcoef : (457/500-2/5)*s≤(2-t)*c := by nlinarith
  have hcross := mul_nonneg hs (sub_nonneg.mpr hcoef)
  have hpoly := mul_nonneg (show 0≤1-c by linarith) (show 0≤c-2/3 by linarith)
  have haC : 0<(a-1)*c := mul_pos (by linarith) (by linarith)
  nlinarith

theorem wall_bridge_upper (q : OpenSquare) (ha : 1<q.side)
    (hc : 0≤q.c) (hs : 0≤q.s)
    (hw : 0≤q.c*q.loU-q.s*(q.loV+q.side))
    (hp : q.Inside (457/500) 2) (t : ℝ) (ht : t≤7/4) :
    q.c+q.s*t<q.loU+q.side := by
  by_contra he
  have he' : q.loU+q.side≤q.c+q.s*t := le_of_not_gt he
  dsimp [OpenSquare.Inside,InBands] at hp
  apply wall_bridge_algebra q.side q.c q.s t ha hc hs q.unit_normal ht
    (by linarith [hp.2.1])
  have hc' := mul_nonneg hc (sub_nonneg.mpr he')
  have hs' := mul_nonneg hs (sub_nonneg.mpr hp.2.2.2.le)
  nlinarith

/-- Reflection in y=3/2, followed by face re-indexing, keeps both normal
components nonnegative and exchanges the two possible excluding faces. -/
noncomputable def wallBridgeReflect (q : OpenSquare) : OpenSquare where
  c := q.s
  s := q.c
  loU := -q.loV-q.side+3*q.c
  loV := -q.loU-q.side+3*q.s
  side := q.side
  side_pos := q.side_pos
  unit_normal := by nlinarith [q.unit_normal]

theorem wallBridgeReflect_inside (q : OpenSquare) (x y : ℝ) :
    (wallBridgeReflect q).Inside x y ↔ q.Inside x (3-y) := by
  dsimp [wallBridgeReflect,OpenSquare.Inside,InBands]
  constructor <;> rintro ⟨h0,h1,h2,h3⟩ <;> refine ⟨?_,?_,?_,?_⟩ <;> linarith

/-- The full closed interval of compulsory wall-bridge points, with strict
interior ownership at both endpoints. -/
theorem wall_bridge_forces (q : OpenSquare) (ha : 1<q.side)
    (hwall : ∀ x y, q.Inside x y → 0≤x)
    (hp : q.Inside (457/500) 1) (hq : q.Inside (457/500) 2)
    (t : ℝ) (ht0 : 5/4≤t) (ht1 : t≤7/4) : q.Inside 1 t := by
  obtain ⟨r,hc,hs,hside,hcenX,hcenY,hinside⟩ := exists_positive_frame q
  have hw : ∀ x y, r.Inside x y → 0≤x := by
    intro x y hi; exact hwall x y ((hinside x y).mp hi)
  have hra : 1<r.side := by simpa [hside] using ha
  have hp' := (hinside _ _).mpr hp
  have hq' := (hinside _ _).mpr hq
  have hup := wall_bridge_upper r hra hc hs (left_wall_vertex r hw) hq' t ht1
  have hrefwall : ∀ x y, (wallBridgeReflect r).Inside x y → 0≤x := by
    intro x y hi; exact hw _ _ ((wallBridgeReflect_inside r x y).mp hi)
  have hrefp : (wallBridgeReflect r).Inside (457/500) 2 := by
    simpa [wallBridgeReflect_inside, show (3:ℝ)-2=1 by norm_num] using hp'
  have hlo := wall_bridge_upper (wallBridgeReflect r) hra hs hc
    (left_wall_vertex _ hrefwall) hrefp (3-t) (by linarith)
  dsimp [wallBridgeReflect] at hlo
  apply (hinside 1 t).mp
  dsimp [OpenSquare.Inside,InBands] at hp' hq' ⊢
  have htS := mul_nonneg hs (show 0≤t-1 by linarith)
  have htC := mul_nonneg hc (show 0≤2-t by linarith)
  have hdC := mul_nonneg hc (show (0:ℝ)≤1-457/500 by norm_num)
  have hdS := mul_nonneg hs (show (0:ℝ)≤1-457/500 by norm_num)
  exact ⟨by nlinarith [hp'.1], by simpa using hup, by linarith, by nlinarith [hq'.2.2.2]⟩

#print axioms wall_bridge_forces
end S12
