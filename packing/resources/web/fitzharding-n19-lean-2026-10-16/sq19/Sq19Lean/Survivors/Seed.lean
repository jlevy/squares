import Sq19Lean.Census.Pattern
import Sq17Lean.HalfPlaneSeed
import Sq17Lean.HalfPlaneBranchComposition

/-! Bridge from an excluded branch-tree root to the census packing predicate.
The root is seeded from the census's exact 25-cell polygons; no 17-square roster
or frame translation is involved. The finite trace and split certificates are
separate hypotheses, discharged by concrete tree modules. -/
namespace Sq19.Survivors
open Sq17.Propagation Sq17.Propagation.HalfPlaneState
open Sq17.Propagation.HalfPlaneState.BranchComposition

/-- An excluded correctly seeded root excludes the named census pattern. -/
theorem not_packs_of_excluded {n : ℕ} (pat : Fin n → Fin 25)
    (T : Array Entry) (S : HState) (side shift : ℚ)
    (hseed : stateSeedOK T (-initialAngleRadius) initialAngleRadius
      (List.ofFn (fun i => Sq19.Census.vertices (pat i))) S = true)
    (hlen : S.length = n)
    (hside : (2443/500 : ℚ) ≤ side + shift) (hshift : 0 ≤ shift)
    (hex : Excluded T S side shift) : ¬ Sq19.Census.Packs pat := by
  apply Sq19.Census.not_packs_of_trace pat
    (List.ofFn (fun i => Sq19.Census.vertices (pat i))) side shift
    (Sq19.Census.getD_ofFn pat) hside hshift
  intro c u hu hc hd hf
  obtain ⟨p, hrep, hsq⟩ := seed_unit_squares T _ S hseed c u
    (by simpa only [hlen] using hu) (by simpa only [hlen] using hc)
  apply hex p hrep
  · intro i j hi hj hij
    rw [hsq i hi, hsq j hj]
    exact hd i j (by simpa only [hlen] using hi) (by simpa only [hlen] using hj) hij
  · intro i hi
    rw [hsq i hi]
    exact hf i (by simpa only [hlen] using hi)

end Sq19.Survivors
#print axioms Sq19.Survivors.not_packs_of_excluded
