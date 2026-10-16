import Sq19Lean.Assembly.CensusBridge
import Sq19Lean.Basic

/-! The lower bound, assembled from the cover and two remaining links taken as hypotheses:
`hexcl` (census and branch-tree exclusions, in the form `census_excluded` and
`Sq19.Survivors.excluded_with_trees` prove), `hroute` (every census orbit not excluded is one of the
captured states) and `hcap` (a packing below side19 whose census mask is a captured state's is
impossible: capture, then the step into H, then the endgame). The instantiation with the built
modules is a separate file on the build machine, since the census and capture modules are generated. -/
namespace Sq19.Assembly
open Sq17.Propagation

theorem side19_lt_cover : side19 < 2443/500 := by
  unfold side19
  have h2 : Real.sqrt 2 < 14143/10000 := by
    rw [Real.sqrt_lt' (by norm_num)]; norm_num
  linarith

theorem side19_le_of_routes (Excluded : ℕ → Prop)
    (hexcl : ∀ m, Excluded m → ∀ {n : ℕ} (assign : Fin n → Fin 25),
      (∀ d : Fin 25, m.testBit d = true → ∃ j, assign j = d) → ¬ Sq19.Census.Packs assign)
    (capIdx : List ℕ)
    (hroute : ∀ k : Fin Sq19.Cover.censusMasks.length,
      ¬ Excluded (Sq19.Cover.censusMasks.get k) → k.val ∈ capIdx)
    (hcap : ∀ k ∈ capIdx, ∀ L : ℝ, L < side19 →
      ∀ (q u : Fin 19 → ℝ × ℝ) (c : Fin 19 → Fin 25),
      (∀ i, (u i).1^2+(u i).2^2 = 1) →
      (∀ i, Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2 ⊆ Sq19.Cover.frameBox L) →
      (∀ i j, i ≠ j → Disjoint
        (interior (Sq17.sq (q i).1 (q i).2 (u i).1 (u i).2))
        (interior (Sq17.sq (q j).1 (q j).2 (u j).1 (u j).2))) →
      (∀ i, q i ∈ Sq19.Cover.cell (c i)) →
      Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.getD k 0) → False)
    (L : ℝ) (p u : Fin 19 → ℝ × ℝ) (hunit : ∀ i, (u i).1^2+(u i).2^2=1)
    (hfit : ∀ i, Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2 ⊆ containerBox L)
    (hdis : ∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (p j).1 (p j).2 (u j).1 (u j).2))) :
    side19 ≤ L := by
  by_contra hnot
  have hlt : L < side19 := lt_of_not_ge hnot
  have hL : L ≤ 2443/500 := (le_of_lt hlt).trans (le_of_lt side19_lt_cover)
  obtain ⟨g, k, hu, hf, hd, c, hinj, himg, hcell⟩ :=
    Sq19.Cover.packing_reaches_census L hL p u hunit hfit hdis
  by_cases hE : Excluded (Sq19.Cover.censusMasks.get k)
  · refine hexcl _ hE c (sub_of_image c himg) ⟨fun i => Sq19.Cover.actG g (Sq19.Cover.shifted L (p i)),
      fun i => Sq19.Cover.dirG g (u i), hu, fun i => ?_,
      fun i => (hf i).trans (Sq19.Cover.frame_in_container L hL), hd⟩
    rw [← cell_eq]; exact hcell i
  · have hk := hroute k hE
    have hget : Sq19.Cover.censusMasks.getD k.val 0 = Sq19.Cover.censusMasks.get k := by
      simp [List.getD_eq_getElem?_getD]
    exact hcap k.val hk L hlt _ _ c hu hf hd hcell (by rw [hget]; exact himg)

end Sq19.Assembly

#print axioms Sq19.Assembly.side19_le_of_routes
