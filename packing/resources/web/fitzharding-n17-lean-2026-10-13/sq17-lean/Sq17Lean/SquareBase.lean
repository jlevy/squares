import Mathlib.Basic.Real.Basic

/-!
# Unit squares in the plane

Definitions shared by the packing (upper bound) and the area bound (lower bound).
-/

namespace Sq17

/-- The closed unit square with centre `(cx, cy)` whose sides are parallel to `(ux, uy)` and
`(-uy, ux)`: the points whose two coordinates in that frame are at most 1/2 in absolute value.
It is a genuine unit square exactly when `(ux, uy)` is a unit vector. -/
def sq (cx cy ux uy : ℝ) : Set (ℝ × ℝ) :=
  {p | |(p.1 - cx) * ux + (p.2 - cy) * uy| ≤ 1/2 ∧ |(p.2 - cy) * ux - (p.1 - cx) * uy| ≤ 1/2}

/-- A set is a unit square if it is `sq` of some centre and some unit direction. -/
def IsUnitSquare (S : Set (ℝ × ℝ)) : Prop :=
  ∃ cx cy ux uy : ℝ, ux ^ 2 + uy ^ 2 = 1 ∧ S = sq cx cy ux uy

end Sq17
