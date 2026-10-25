import S12.Diameter

namespace S12
open S12Pilot
set_option maxHeartbeats 0

/-- A segment of length at most one has projection at most one in either
unit-normal direction, including all equality cases. -/
theorem short_projections (q : OpenSquare) (dx dy : ℝ)
    (hd : dx^2+dy^2 ≤ 1) :
    -1 ≤ q.c*dx+q.s*dy ∧ q.c*dx+q.s*dy ≤ 1 ∧
    -1 ≤ -q.s*dx+q.c*dy ∧ -q.s*dx+q.c*dy ≤ 1 := by
  let u := q.c*dx+q.s*dy
  let v := -q.s*dx+q.c*dy
  have hh : u^2+v^2 ≤ 1 := by
    calc
      _ = (q.c^2+q.s^2)*(dx^2+dy^2) := by dsimp [u,v]; ring
      _ = dx^2+dy^2 := by rw [q.unit_normal, one_mul]
      _ ≤ 1 := hd
  have hu : u^2 ≤ 1 := le_trans (le_add_of_nonneg_right (sq_nonneg v)) hh
  have hv : v^2 ≤ 1 := le_trans (le_add_of_nonneg_left (sq_nonneg u)) hh
  have hub : -1 ≤ u ∧ u ≤ 1 := abs_le.mp ((sq_le_one_iff_abs_le_one u).mp hu)
  have hvb : -1 ≤ v ∧ v ≤ 1 := abs_le.mp ((sq_le_one_iff_abs_le_one v).mp hv)
  exact ⟨hub.1,hub.2,hvb.1,hvb.2⟩


end S12
