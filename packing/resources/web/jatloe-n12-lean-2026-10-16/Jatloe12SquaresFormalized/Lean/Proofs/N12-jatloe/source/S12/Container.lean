import S12.SquareFrame
import S12.SymmetryBase

/-! Original containment and center-transform facts, independent of marker coverage. -/
namespace S12
open S12Pilot
set_option maxHeartbeats 0

def InsideContainer (q : OpenSquare) : Prop :=
  ∀ x y, q.Inside x y → 0≤x ∧ x≤4 ∧ 0≤y ∧ y≤4

theorem container_pullX (q : OpenSquare) (h : InsideContainer q) : InsideContainer (pullX q) := by
  intro x y hi
  obtain ⟨h0,h1,h2,h3⟩ := h _ _ ((inside_pullX q x y).mp hi)
  exact ⟨by linarith,by linarith,h2,h3⟩
theorem container_pullY (q : OpenSquare) (h : InsideContainer q) : InsideContainer (pullY q) := by
  intro x y hi
  obtain ⟨h0,h1,h2,h3⟩ := h _ _ ((inside_pullY q x y).mp hi)
  exact ⟨h0,h1,by linarith,by linarith⟩
theorem container_pullSwap (q : OpenSquare) (h : InsideContainer q) : InsideContainer (pullSwap q) := by
  intro x y hi
  obtain ⟨h0,h1,h2,h3⟩ := h _ _ ((inside_pullSwap q x y).mp hi)
  exact ⟨h2,h3,h0,h1⟩

@[simp] theorem center_pullX_x (q : OpenSquare) : centerX (pullX q)=4-centerX q := by
  dsimp [centerX,pullX]; nlinarith [q.unit_normal]
@[simp] theorem center_pullX_y (q : OpenSquare) : centerY (pullX q)=centerY q := by
  dsimp [centerY,pullX]; ring
@[simp] theorem center_pullY_x (q : OpenSquare) : centerX (pullY q)=centerX q := by
  dsimp [centerX,pullY]; ring
@[simp] theorem center_pullY_y (q : OpenSquare) : centerY (pullY q)=4-centerY q := by
  dsimp [centerY,pullY]; nlinarith [q.unit_normal]
@[simp] theorem center_pullSwap_x (q : OpenSquare) : centerX (pullSwap q)=centerY q := by
  dsimp [centerX,centerY,pullSwap]; ring
@[simp] theorem center_pullSwap_y (q : OpenSquare) : centerY (pullSwap q)=centerX q := by
  dsimp [centerX,centerY,pullSwap]; ring

end S12
