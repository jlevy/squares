import S12.MarkerCoverGeometry

namespace S12
open S12Pilot

theorem inside_center_distance (q : OpenSquare) (x y : ℝ) (hp : q.Inside x y) :
    (x-centerX q)^2+(y-centerY q)^2<q.side^2/2 := by
  have hi := (inside_centered_iff q x y).mp hp
  let du := q.c*(x-centerX q)+q.s*(y-centerY q)
  let dv := -q.s*(x-centerX q)+q.c*(y-centerY q)
  have hi' : InBands (-q.side/2) (-q.side/2) q.side du dv := hi
  dsimp [InBands] at hi'
  have hu := mul_pos (show 0<q.side/2-du by linarith) (show 0<q.side/2+du by linarith)
  have hv := mul_pos (show 0<q.side/2-dv by linarith) (show 0<q.side/2+dv by linarith)
  have hrot : du^2+dv^2=(x-centerX q)^2+(y-centerY q)^2 := by
    calc
      _ = (q.c^2+q.s^2)*((x-centerX q)^2+(y-centerY q)^2) := by dsimp [du,dv]; ring
      _ = _ := by rw [q.unit_normal,one_mul]
  rw [← hrot]
  nlinarith only [hu,hv]

/-- A normalized square owning the bottom-left corner marker has its center
in the left/lower half of the container. No symmetry assumption is used. -/
theorem corner_owner_center (q : OpenSquare) (hsize : q.side≤1001/1000) (hp : Owns q 0) :
    centerX q≤2 ∧ centerY q≤2 := by
  have hi : q.Inside 1 (457/500) := by simpa [Owns,marker] using hp
  have hd := inside_center_distance q _ _ hi
  have hs := q.side_pos
  constructor
  · by_contra he
    have he' : 2<centerX q := lt_of_not_ge he
    nlinarith [sq_nonneg (457/500-centerY q)]
  · by_contra he
    have he' : 2<centerY q := lt_of_not_ge he
    nlinarith [sq_nonneg (1-centerX q)]

#print axioms corner_owner_center
end S12
