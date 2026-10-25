import S12.CornerCover

namespace S12
open S12Pilot

/-- Owning the two near-corner points forces ownership of (1,1). The
nontrivial outward face is controlled by the two container walls. -/
theorem corner_pair_forces (q : OpenSquare) (ha : 1<q.side)
    (hwall : ∀ x y, q.Inside x y → 0≤x ∧ 0≤y)
    (b : ℝ) (hb : b≤1) (hp : q.Inside 1 b) (hq : q.Inside b 1) :
    q.Inside 1 1 := by
  obtain ⟨r,hc,hs,hside,hcenX,hcenY,hinside⟩ := exists_positive_frame q
  have hw : ∀ x y, r.Inside x y → 0≤x ∧ 0≤y := by
    intro x y hi; exact hwall x y ((hinside x y).mp hi)
  obtain ⟨hwX,hwY⟩ := positive_frame_wall_bounds r hc hs hw
  have hup := corner_upper_projection r.side r.c r.s (centerX r) (centerY r)
    (by simpa [hside] using ha) hc hs r.unit_normal hwX hwY
  have hp' := (inside_centered_iff r 1 b).mp ((hinside 1 b).mpr hp)
  have hq' := (inside_centered_iff r b 1).mp ((hinside b 1).mpr hq)
  apply (hinside 1 1).mp
  apply (inside_centered_iff r 1 1).mpr
  dsimp [InBands] at hp' hq' ⊢
  have hs' := mul_nonneg hs (sub_nonneg.mpr hb)
  have hc' := mul_nonneg hc (sub_nonneg.mpr hb)
  exact ⟨by nlinarith [hp'.1], by linarith, by nlinarith [hp'.2.2.1],
    by nlinarith [hq'.2.2.2]⟩

#print axioms corner_pair_forces
end S12
