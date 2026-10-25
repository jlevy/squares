import S12.Diameter

namespace S12
open S12Pilot

/-- Strict interval membership is preserved at all points of a closed segment,
including either endpoint. -/
theorem interval_segment (l a x y t : ℝ) (hx0 : l < x) (hx1 : x < l+a)
    (hy0 : l < y) (hy1 : y < l+a) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    l < (1-t)*x+t*y ∧ (1-t)*x+t*y < l+a := by
  by_cases hz : t = 0
  · subst t; simpa using And.intro hx0 hx1
  have hp : 0 < t := lt_of_le_of_ne ht0 (Ne.symm hz)
  have ha0 := mul_nonneg (sub_nonneg.mpr ht1) (le_of_lt (sub_pos.mpr hx0))
  have ha1 := mul_nonneg (sub_nonneg.mpr ht1) (le_of_lt (sub_pos.mpr hx1))
  have hb0 := mul_pos hp (sub_pos.mpr hy0)
  have hb1 := mul_pos hp (sub_pos.mpr hy1)
  constructor <;> nlinarith

theorem inside_segment (q : OpenSquare) (x y x' y' t : ℝ)
    (hp : q.Inside x y) (hp' : q.Inside x' y') (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    q.Inside ((1-t)*x+t*x') ((1-t)*y+t*y') := by
  obtain ⟨h0,h1,h2,h3⟩ := hp
  obtain ⟨h4,h5,h6,h7⟩ := hp'
  have hu := interval_segment q.loU q.side _ _ t h0 h1 h4 h5 ht0 ht1
  have hv := interval_segment q.loV q.side _ _ t h2 h3 h6 h7 ht0 ht1
  dsimp [OpenSquare.Inside, InBands]
  constructor
  · nlinarith [hu.1]
  constructor
  · nlinarith [hu.2]
  constructor
  · nlinarith [hv.1]
  · nlinarith [hv.2]

/-- A three-point rational hull certificate uses two successive segments.
This avoids trusting a convex-hull implementation. -/
structure TriangleCertificate where
  p0 : ℚ × ℚ
  p1 : ℚ × ℚ
  p2 : ℚ × ℚ
  target : ℚ × ℚ
  s : ℚ
  t : ℚ

def TriangleCertificate.Check (w : TriangleCertificate) : Prop :=
  0 ≤ w.s ∧ w.s ≤ 1 ∧ 0 ≤ w.t ∧ w.t ≤ 1 ∧
  w.target.1 = (1-w.t)*((1-w.s)*w.p0.1+w.s*w.p1.1)+w.t*w.p2.1 ∧
  w.target.2 = (1-w.t)*((1-w.s)*w.p0.2+w.s*w.p1.2)+w.t*w.p2.2
instance TriangleCertificate.decidableCheck (w : TriangleCertificate) : Decidable w.Check := inferInstanceAs (Decidable (_ ∧ _))

theorem triangle_certificate_sound (w : TriangleCertificate) (hw : w.Check)
    (q : OpenSquare) (h0 : q.Inside w.p0.1 w.p0.2)
    (h1 : q.Inside w.p1.1 w.p1.2) (h2 : q.Inside w.p2.1 w.p2.2) :
    q.Inside w.target.1 w.target.2 := by
  obtain ⟨hs0,hs1,ht0,ht1,hx,hy⟩ := hw
  have hs0' : (0 : ℝ) ≤ w.s := by exact_mod_cast hs0
  have hs1' : (w.s : ℝ) ≤ 1 := by exact_mod_cast hs1
  have ht0' : (0 : ℝ) ≤ w.t := by exact_mod_cast ht0
  have ht1' : (w.t : ℝ) ≤ 1 := by exact_mod_cast ht1
  have hs := inside_segment q _ _ _ _ w.s h0 h1 hs0' hs1'
  have ht := inside_segment q _ _ _ _ w.t hs h2 ht0' ht1'
  rw [hx,hy]
  push_cast
  exact ht

#print axioms triangle_certificate_sound
end S12
