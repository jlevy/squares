import S12.AuxCoverGeometry
import S12.WallNormalBounds

namespace S12
open S12Pilot

theorem general_segment_hit (q : OpenSquare) (ha : 1<q.side)
    (hw : ∀ x y, q.Inside x y → 0≤y) (x0 x1 b d : ℝ)
    (hX0 : x0≤centerX q) (hX1 : centerX q≤x1) (hY : centerY q≤d)
    (hlen : x1-x0≤1) (hb : 3/4≤b) (hbd : b≤d) (hd : d≤1)
    (hlength : (x1-x0)^2+(d-b)^2≤1)
    (hupper : ∀ c s : ℝ, 0≤c → 0≤s → c^2+s^2=1 →
      c^2*b+s^2*d+(x1-x0)*c*s≤c+s) :
    q.Inside x0 b ∨ q.Inside x1 d := by
  have h := general_wall_nonavoidance (q.translated x0 0) ha
    (by intro x y hi; simpa using hw _ _ ((inside_translated_iff q x0 0 x y).mp hi))
    (x1-x0) b d (by simp; linarith) (by simp; linarith) (by simpa using hY)
    (by linarith) hlen hb hbd hd hlength hupper
  simpa only [inside_translated_iff,add_zero,zero_add,
    show x0+(x1-x0)=x1 by ring] using h

theorem general_segment_descending (q : OpenSquare) (ha : 1<q.side)
    (hw : ∀ x y, q.Inside x y → 0≤y) (x0 x1 b d : ℝ)
    (hX0 : x0≤centerX q) (hX1 : centerX q≤x1) (hY : centerY q≤b)
    (hlen : x1-x0≤1) (hd : 3/4≤d) (hdb : d≤b) (hb : b≤1)
    (hlength : (x1-x0)^2+(b-d)^2≤1)
    (hupper : ∀ c s : ℝ, 0≤c → 0≤s → c^2+s^2=1 →
      c^2*d+s^2*b+(x1-x0)*c*s≤c+s) :
    q.Inside x0 b ∨ q.Inside x1 d := by
  have h := general_segment_hit (pullX q) ha
    (by intro x y hi; exact hw _ _ ((inside_pullX q x y).mp hi)) (4-x1) (4-x0) d b
    (by simp; linarith) (by simp; linarith) (by simpa using hY)
    (by linarith) hd hdb hb
    (by convert hlength using 1 <;> ring)
    (by intro c s hc hs hn; convert hupper c s hc hs hn using 1 <;> ring)
  simp only [inside_pullX, show 4-(4-x0)=x0 by ring, show 4-(4-x1)=x1 by ring] at h
  exact h.symm

end S12
