import Sq19Lean.Assembly.CensusRoute

/-! Reverse routing from the three capture masks to their census indices.
The finite check traverses `censusMasks.zipIdx` once, avoiding repeated indexing
into the 22,475-element list. No census trace or capture trace is replayed here. -/
namespace Sq19.Assembly.CensusRoute

/-- State numbers are zero-based positions in the census representative list. -/
def captureIndices : List ℕ := [3435, 3438, 3442]

def captureIndexCheck : Bool := Sq19.Cover.censusMasks.zipIdx.all fun entry =>
  decide (entry.1 ∈ captureMasks → entry.2 ∈ captureIndices)

/-- One finite native check of the mask-to-index direction. -/
theorem captureIndex_checked : captureIndexCheck = true := by native_decide

theorem index_of_capture_mask (k : Fin Sq19.Cover.censusMasks.length)
    (hm : Sq19.Cover.censusMasks.get k ∈ captureMasks) : k.val ∈ captureIndices := by
  have hmem : (Sq19.Cover.censusMasks.get k, k.val) ∈ Sq19.Cover.censusMasks.zipIdx := by
    apply List.mk_mem_zipIdx_iff_getElem?.mpr
    simp
  have h := List.all_eq_true.mp captureIndex_checked _ hmem
  exact (of_decide_eq_true h) hm

/-- Every representative not excluded by the complete census or four trees has
one of the three indices expected by the capture-to-endgame theorems. -/
theorem full_route (k : Fin Sq19.Cover.censusMasks.length)
    (hn : ¬ (Excluded (Sq19.Cover.censusMasks.get k) ∨
      Sq19.Survivors.TreeExcluded (Sq19.Cover.censusMasks.get k))) :
    k.val ∈ captureIndices := by
  rcases Sq19.Assembly.census_route _ (List.get_mem _ k) with he | ht | hc
  · exact False.elim (hn (Or.inl he))
  · exact False.elim (hn (Or.inr ht))
  · exact index_of_capture_mask k hc

end Sq19.Assembly.CensusRoute

#print axioms Sq19.Assembly.CensusRoute.captureIndex_checked
#print axioms Sq19.Assembly.CensusRoute.full_route
