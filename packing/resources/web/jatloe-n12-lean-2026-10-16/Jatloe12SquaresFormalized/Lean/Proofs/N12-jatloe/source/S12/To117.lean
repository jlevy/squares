import S12.CoreData
import S12.DiagonalPacking

namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0

/-- The named 117 representatives, with the original marker groups intact. -/
def retainedRows : List CoverRow := coverRows.filter (fun r => decide (r.originalId∈expectedIds))

theorem retainedRows_count : retainedRows.length=117 := by native_decide
theorem retainedRows_ids : retainedRows.map CoverRow.originalId=expectedIds := by native_decide

/-- Every discarded representative has either a diagonal contradiction or a
certified inconsistent core. The imported domains of retained rows are unused. -/
theorem exclusion_coverage : ∀ r∈coverRows,
    r.originalId∈expectedIds ∨ (∃ m∈r.groups,diagonalBad m=true) ∨
    ∃ w∈coreProofs,w.val.family=r.groups := by native_decide

theorem representative_retained (p : NormalizedPacking) (r : CoverRow)
    (hr : r∈coverRows) (hf : codedMarkerFamily p=r.groups) : r∈retainedRows := by
  rcases exclusion_coverage r hr with h | h | h
  · exact List.mem_filter.mpr ⟨hr,decide_eq_true h⟩
  · obtain ⟨m,hm,he⟩ := h
    have hh := packing_no_diagonal p m (by rw [hf]; exact hm)
    rw [hh] at he
    contradiction
  · obtain ⟨w,_,he⟩ := h
    exact False.elim (w.val.sound w.property p (hf.trans he.symm))

/-- Every normalized packing belongs, after one checked square symmetry,
to one of the explicit 117 marker assignments. No cover or domain hypothesis
is supplied by the caller. -/
theorem packing_reduction_to_117 (p : NormalizedPacking) :
    ∃ t∈allTransforms, ∃ r∈retainedRows, codedMarkerFamily (t.pullPacking p)=r.groups := by
  obtain ⟨t,ht,r,hr,hf⟩ := packing_reduction_to_577_representatives p
  exact ⟨t,ht,r,representative_retained (t.pullPacking p) r hr hf,hf⟩

#print axioms packing_reduction_to_117
end S12
