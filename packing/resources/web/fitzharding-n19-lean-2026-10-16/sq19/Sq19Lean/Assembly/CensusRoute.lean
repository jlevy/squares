import Sq19Lean.Assembly.CensusBridge
import Sq19Lean.Assembly.CensusRouteData
import Sq19Lean.Survivors.Dispatch

/-! Route a genuine packing to one of the three capture masks. The expensive
generated `Census.Complete` module is deliberately an input, not an import.
The assembly supplies `Sq19.Census.Complete.census_excluded` as `hexcl`; its
count, survivor-image list, and empty exception list must match definitionally.
-/
namespace Sq19.Assembly
open Sq17.Propagation

/-- The exact argument shape of the generated complete census theorem. -/
abbrev CensusExclusion : Prop :=
  ∀ (m : ℕ), m < 2 ^ 25 → CensusRoute.count m = 19 →
    CensusRoute.isSurvivor m = false → m ∉ CensusRoute.exceptions →
    ∀ {n : ℕ} (assign : Fin n → Fin 25),
      (∀ d : Fin 25, m.testBit d = true → ∃ j, assign j = d) →
      ¬ Sq19.Census.Packs assign

theorem census_route (m : ℕ) (hm : m ∈ Sq19.Cover.censusMasks) :
    CensusRoute.Excluded m ∨ Sq19.Survivors.TreeExcluded m ∨
      m ∈ CensusRoute.captureMasks :=
  CensusRoute.route m hm

/-- Turn the concrete census signature into the generic dispatch signature. -/
theorem census_exclusion_dispatch (hexcl : CensusExclusion)
    (m : ℕ) (hm : CensusRoute.Excluded m) {n : ℕ} (assign : Fin n → Fin 25)
    (hsub : ∀ d : Fin 25, m.testBit d = true → ∃ j, assign j = d) :
    ¬ Sq19.Census.Packs assign :=
  hexcl m hm.1 hm.2.1 hm.2.2.1 hm.2.2.2 assign hsub

/-- A surviving census packing can only belong to one of the three capture masks. -/
theorem capture_mask_of_census_packs (hexcl : CensusExclusion)
    (m : ℕ) (hm : m ∈ Sq19.Cover.censusMasks) {n : ℕ} (assign : Fin n → Fin 25)
    (hsub : ∀ d : Fin 25, m.testBit d = true → ∃ j, assign j = d)
    (hp : Sq19.Census.Packs assign) : m ∈ CensusRoute.captureMasks := by
  rcases census_route m hm with he | ht | hc
  · exact False.elim (census_exclusion_dispatch hexcl m he assign hsub hp)
  · exact False.elim (Sq19.Survivors.tree_excluded m ht assign hsub hp)
  · exact hc

/-- Use this form on an already chosen cover witness, preserving its original
symmetry, positions and smaller-container frame for the capture bridge. -/
theorem capture_mask_of_image (hexcl : CensusExclusion)
    (k : Fin Sq19.Cover.censusMasks.length) (c : Fin 19 → Fin 25)
    (himg : Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.get k))
    (hp : Sq19.Census.Packs c) :
    Sq19.Cover.censusMasks.get k ∈ CensusRoute.captureMasks :=
  capture_mask_of_census_packs hexcl _ (List.get_mem _ k) c (sub_of_image c himg) hp

/-- The cover, complete census exclusions and four survivor trees leave only the
three capture masks, with an injective owner assignment and an actual census packing. -/
theorem capture_of_packing (hexcl : CensusExclusion)
    (L : ℝ) (hL : L ≤ 2443/500)
    (p u : Fin 19 → ℝ × ℝ) (hunit : ∀ i, (u i).1^2+(u i).2^2=1)
    (hfit : ∀ i, Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2 ⊆ containerBox L)
    (hdis : ∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (p j).1 (p j).2 (u j).1 (u j).2))) :
    ∃ k : Fin Sq19.Cover.censusMasks.length,
      Sq19.Cover.censusMasks.get k ∈ CensusRoute.captureMasks ∧
      ∃ c : Fin 19 → Fin 25, Function.Injective c ∧
        Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.get k) ∧
        Sq19.Census.Packs c := by
  obtain ⟨k, hnot, c, hinj, himg, hp⟩ := survivor_of_packing
    (fun m => CensusRoute.Excluded m ∨ Sq19.Survivors.TreeExcluded m)
    (Sq19.Survivors.excluded_with_trees CensusRoute.Excluded
      (census_exclusion_dispatch hexcl)) L hL p u hunit hfit hdis
  refine ⟨k, ?_, c, hinj, himg, hp⟩
  rcases census_route _ (List.get_mem _ k) with he | ht | hc
  · exact False.elim (hnot (Or.inl he))
  · exact False.elim (hnot (Or.inr ht))
  · exact hc

end Sq19.Assembly

#print axioms Sq19.Assembly.CensusRoute.route_checked
#print axioms Sq19.Assembly.CensusRoute.capture_indices
#print axioms Sq19.Assembly.census_route
#print axioms Sq19.Assembly.capture_mask_of_census_packs
#print axioms Sq19.Assembly.capture_mask_of_image
#print axioms Sq19.Assembly.capture_of_packing
