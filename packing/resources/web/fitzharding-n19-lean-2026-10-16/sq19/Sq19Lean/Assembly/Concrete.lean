import Sq19Lean.Assembly.Final
import Sq19Lean.Assembly.CaptureIndexRoute
import Sq19Lean.Census.Complete
import Sq19Lean.Capture.Hcap

/-! Concrete assembly of the lower bound. This module must be built against the
accepted complete census and all three generated capture-state proofs. It adds
no geometric hypothesis: every argument of `side19_le_of_routes` is supplied
by a theorem. Successful checking of this module is the lower-bound milestone. -/
namespace Sq19.Assembly
open Sq17.Propagation

/-- Definitional equality checks the generated census's count, survivor-image
list and empty exceptions against the routing interface. -/
theorem complete_census_exclusion : CensusExclusion :=
  Sq19.Census.Complete.census_excluded

/-- Exclude both the census patterns and the four branch-tree survivors. -/
abbrev FinalExcluded (m : ℕ) : Prop :=
  CensusRoute.Excluded m ∨ Sq19.Survivors.TreeExcluded m

theorem final_exclusion_dispatch :
    ∀ m, FinalExcluded m → ∀ {n : ℕ} (assign : Fin n → Fin 25),
      (∀ d : Fin 25, m.testBit d = true → ∃ j, assign j = d) →
      ¬ Sq19.Census.Packs assign :=
  Sq19.Survivors.excluded_with_trees CensusRoute.Excluded
    (census_exclusion_dispatch complete_census_exclusion)

/-- Nineteen unit squares with disjoint interiors inside `[0,L]²` require
`L ≥ 3 + 4√2/3`. Positions and unit directions are unrestricted. -/
theorem side19_le (L : ℝ) (p u : Fin 19 → ℝ × ℝ)
    (hunit : ∀ i, (u i).1 ^ 2 + (u i).2 ^ 2 = 1)
    (hfit : ∀ i, Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2 ⊆ containerBox L)
    (hdis : ∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (p j).1 (p j).2 (u j).1 (u j).2))) :
    side19 ≤ L := by
  apply side19_le_of_routes FinalExcluded final_exclusion_dispatch
    CensusRoute.captureIndices CensusRoute.full_route ?_ L p u hunit hfit hdis
  intro k hk
  have hk' : k = 3435 ∨ k = 3438 ∨ k = 3442 := by
    simpa only [CensusRoute.captureIndices, List.mem_cons, List.mem_singleton, List.not_mem_nil,
      or_false] using hk
  rcases hk' with rfl | rfl | rfl
  · exact Sq19.Capture.S3435.hcap
  · exact Sq19.Capture.S3438.hcap
  · exact Sq19.Capture.S3442.hcap

end Sq19.Assembly

#print axioms Sq19.Assembly.complete_census_exclusion
#print axioms Sq19.Assembly.final_exclusion_dispatch
#print axioms Sq19.Assembly.side19_le
