import Sq17Lean.HalfPlanePositiveControl

/-! Boundary contact must remain legal: the collision test uses strict overlap,
while both the squares and the outer container are closed sets. -/
namespace Sq17.Propagation.HalfPlaneState.PositiveControl
open HalfPlaneInt

def pointX (x : Int) : List IC :=
  [⟨1, 0, x⟩, ⟨-1, 0, -x⟩, ⟨0, 1, 0⟩, ⟨0, -1, 0⟩]

theorem touching_cores_not_collision :
    collide (pointX 0) (pointX 1) (mkBox (pointX 0)) (mkBox (pointX 1))
      1 0 1 1 1 1 0 1 1 1 = false := by decide +kernel

theorem coincident_cores_collision :
    collide (pointX 0) (pointX 0) (mkBox (pointX 0)) (mkBox (pointX 0))
      1 0 1 1 1 1 0 1 1 1 = true := by decide +kernel

theorem touching_square_interiors_disjoint :
    Disjoint (interior (Sq17.sq 0 0 1 0)) (interior (Sq17.sq 1 0 1 0)) := by
  apply WallCapacity.support_gap_disjoint (0, 0) (1, 0) 1 0 1 0 1 0
  all_goals norm_num [WallCapacity.squareSupport]

theorem touching_squares_share_boundary :
    ((1/2, 0) : ℝ × ℝ) ∈ Sq17.sq 0 0 1 0 ∧
    ((1/2, 0) : ℝ × ℝ) ∈ Sq17.sq 1 0 1 0 := by
  norm_num [Sq17.sq]

end Sq17.Propagation.HalfPlaneState.PositiveControl

#print axioms Sq17.Propagation.HalfPlaneState.PositiveControl.touching_cores_not_collision
#print axioms Sq17.Propagation.HalfPlaneState.PositiveControl.touching_square_interiors_disjoint
