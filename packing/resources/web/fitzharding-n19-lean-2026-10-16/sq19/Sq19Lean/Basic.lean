import Mathlib.Analysis.Real.Sqrt

/-! Environment check for the s(19) project. Proves nothing about packings. -/
namespace Sq19

/-- The conjectured optimal side for nineteen unit squares. -/
noncomputable def side19 : ℝ := 3 + 4 * Real.sqrt 2 / 3

theorem side19_pos : 0 < side19 := by
  unfold side19
  positivity

end Sq19

#print axioms Sq19.side19_pos
