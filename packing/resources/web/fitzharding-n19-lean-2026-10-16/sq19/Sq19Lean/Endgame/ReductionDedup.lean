import Sq19Lean.Endgame.ReductionCases

/-! Exact, symbolic removal of endpoint bits which are unused in case-b rows.
This reduces 4096 encodings to 2304 expressions/cones without assuming any
numerical derivative check. -/
namespace Sq19.Endgame.Reduction

/-- Case-b rows do not depend on the case-a offset endpoint selector. -/
def Case.normalize (c : Case) : Case :=
  { c with pd := c.pa && c.pd, qd := c.qa && c.qd }

theorem Case.normalize_idem (c : Case) : c.normalize.normalize = c.normalize := by
  cases c
  simp only [Case.normalize, Bool.and_self_left]

@[simp] theorem Case.normalize_P (c : Case) : c.normalize.P = c.P := by
  cases hp : c.pa <;> simp [Case.P, Case.normalize, Case.j12, hp]

@[simp] theorem Case.normalize_Q (c : Case) : c.normalize.Q = c.Q := by
  cases hq : c.qa <;> simp [Case.Q, Case.normalize, hq]

@[simp] theorem Case.normalize_F (c : Case) : c.normalize.F = c.F := rfl

@[simp] theorem Case.normalize_directions (c : Case) :
    c.normalize.directions = c.directions := rfl

@[simp] theorem Case.normalize_margin (c : Case) : c.normalize.margin = c.margin := by
  simp only [Case.margin, Case.normalize_P, Case.normalize_Q, Case.normalize_F]

@[simp] theorem geometryCheck_normalize (c : Case) :
    geometryCheck c.normalize = geometryCheck c := by
  simp only [geometryCheck, Case.normalize_P, Case.normalize_Q, Case.normalize_F]

@[simp] theorem slopeCheck_normalize (c : Case) :
    slopeCheck c.normalize = slopeCheck c := by
  simp only [slopeCheck, Case.normalize_directions, Case.normalize_margin]

@[simp] theorem check_normalize (c : Case) : check c.normalize = check c := by
  simp only [check, geometryCheck_normalize, slopeCheck_normalize]

/-- A proved normalized check supplies the original case, with no replay. -/
theorem check_of_normalize (c : Case) (h : check c.normalize = true) :
    check c = true := by
  simpa only [check_normalize] using h

/-- Opposite signed angles determine their relative sign without magnitude order.
Only their single-coordinate prefix direction still depends on the order bit. -/
theorem Case.bd58_of_opposite (c : Case) (h : c.b5 ≠ c.b8) : c.bd58 = c.b8 := by
  simp [Case.bd58, h]

/-- Flipping magnitude order in an opposite-sign orthant preserves all rows.
It does NOT preserve the directions, so it is not by itself a check equivalence. -/
def Case.flipOrder (c : Case) : Case := {c with fiveLarger := !c.fiveLarger}

theorem Case.flipOrder_rows (c : Case) (h : c.b5 ≠ c.b8) :
    c.flipOrder.P = c.P ∧ c.flipOrder.Q = c.Q ∧ c.flipOrder.F = c.F := by
  refine ⟨rfl, rfl, ?_⟩
  have hb : c.flipOrder.bd58 = c.bd58 := by
    simp [Case.bd58, Case.flipOrder, h]
  unfold Case.F
  rw [hb]
  rfl

theorem Case.flipOrder_margin (c : Case) (h : c.b5 ≠ c.b8) :
    c.flipOrder.margin = c.margin := by
  rcases c.flipOrder_rows h with ⟨hp, hq, hf⟩
  simp only [Case.margin, hp, hq, hf]

end Sq19.Endgame.Reduction
#print axioms Sq19.Endgame.Reduction.check_of_normalize
#print axioms Sq19.Endgame.Reduction.Case.flipOrder_margin
