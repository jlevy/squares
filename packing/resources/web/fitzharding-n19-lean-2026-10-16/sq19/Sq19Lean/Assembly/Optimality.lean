import Sq19Lean.Assembly.Concrete
import Sq19Lean.Assembly.PlainPacking

/-! Final theorem: all computational and geometric obligations are discharged
by imported theorems. Do not describe this as verified until this file builds
against the complete census and all three accepted capture-state modules. -/
namespace Sq19

theorem square19_optimality (L : ℝ) :
    Feasible19 L ↔ 3 + 4 * Real.sqrt 2 / 3 ≤ L := by
  simpa only [side19] using feasible19_iff_of_lower Assembly.side19_le L

end Sq19

#print axioms Sq19.square19_optimality
