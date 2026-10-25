import S12.Diagonal

/-! Original square-center/frame definitions, independent of marker-cover lemmas. -/
namespace S12
open S12Pilot
set_option maxHeartbeats 0

/-- Center coordinates in the square's own orthonormal coordinate system. -/
noncomputable def centerX (q : OpenSquare) : ℝ := q.c*(q.loU+q.side/2)-q.s*(q.loV+q.side/2)
noncomputable def centerY (q : OpenSquare) : ℝ := q.s*(q.loU+q.side/2)+q.c*(q.loV+q.side/2)

theorem center_coordinates (q : OpenSquare) :
    q.c*centerX q+q.s*centerY q=q.loU+q.side/2 ∧
    -q.s*centerX q+q.c*centerY q=q.loV+q.side/2 := by
  constructor
  · calc
      _ = (q.c^2+q.s^2)*(q.loU+q.side/2) := by dsimp [centerX,centerY]; ring
      _ = _ := by rw [q.unit_normal,one_mul]
  · calc
      _ = (q.c^2+q.s^2)*(q.loV+q.side/2) := by dsimp [centerX,centerY]; ring
      _ = _ := by rw [q.unit_normal,one_mul]

noncomputable def relativeU (q : OpenSquare) (x y : ℝ) : ℝ := q.c*x+q.s*y-q.loU-q.side/2
noncomputable def relativeV (q : OpenSquare) (x y : ℝ) : ℝ := -q.s*x+q.c*y-q.loV-q.side/2

theorem relative_inside_iff (q : OpenSquare) (x y : ℝ) :
    InBands (-q.side/2) (-q.side/2) q.side (relativeU q x y) (relativeV q x y) ↔
    q.Inside x y := by
  dsimp [InBands,OpenSquare.Inside,relativeU,relativeV]
  constructor <;> rintro ⟨h0,h1,h2,h3⟩ <;> refine ⟨?_,?_,?_,?_⟩ <;> linarith

theorem inside_centered_iff (q : OpenSquare) (x y : ℝ) :
    q.Inside x y ↔ InBands (-q.side/2) (-q.side/2) q.side
      (q.c*(x-centerX q)+q.s*(y-centerY q))
      (-q.s*(x-centerX q)+q.c*(y-centerY q)) := by
  obtain ⟨h0,h1⟩ := center_coordinates q
  dsimp [OpenSquare.Inside,InBands]
  constructor <;> rintro ⟨a0,a1,a2,a3⟩ <;> refine ⟨?_,?_,?_,?_⟩ <;> linarith

end S12
