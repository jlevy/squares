import Sq19Lean.Endgame.ReductionAssembly
import Sq19Lean.Endgame.ReductionEncodingPure

/-! The final local-hull interface for the finite replay certificates.
Enumeration coverage is proved by arithmetic, not by an additional native check. -/
namespace Sq19.Endgame.Reduction
open Sq19.Milp

theorem side19_le_of_hull_of_index_checks
    (checks : ∀ n < 4096, checkNat n = true)
    {θ dx dy : ℕ → ℝ} {L : ℝ} (hg : Good Hull.prob θ dx dy L) : side19 ≤ L :=
  side19_le_of_hull_of_all_checks (all_cases_of_all_indices_pure checks) hg

end Sq19.Endgame.Reduction

#print axioms Sq19.Endgame.Reduction.side19_le_of_hull_of_index_checks
