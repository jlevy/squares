import Sq17Lean.HalfPlaneLastCase
import Sq17Lean.HalfPlaneTrees.T1563.Dispatch

/-! Exact optimality for seventeen independently translated and rotated closed
unit squares with pairwise disjoint interiors in an axis-aligned square.
The theorem has no remaining case-exclusion or certificate-acceptance premise.
Concrete certificate checks use Lean's `native_decide`; the axiom report below
records that trust boundary in addition to the standard logical axioms. -/
namespace Sq17

theorem square17_feasible_iff (L : ℝ) :
    HalfPlaneAssembly.Feasible L ↔ EndpointGeometry.side ≤ L :=
  HalfPlaneAssembly.feasible_iff_of_1563
    Propagation.HalfPlaneState.T1563.full_dispatch L

theorem square17_optimality (L : ℝ) :
    HalfPlaneAssembly.PlainPacking L ↔ EndpointGeometry.side ≤ L :=
  HalfPlaneAssembly.plainPacking_iff_of_1563
    Propagation.HalfPlaneState.T1563.full_dispatch L

end Sq17

#print axioms Sq17.square17_optimality
#check Sq17.square17_optimality
