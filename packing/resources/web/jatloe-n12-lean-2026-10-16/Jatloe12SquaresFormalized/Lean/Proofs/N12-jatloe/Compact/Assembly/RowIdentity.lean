import Completion.Contracts

/-! Direct identities for original retained rows. The historical classification
already proves that the 117 retained identifiers are distinct. Reuse that fact
rather than repeatedly evaluating the full table and its unused domain data.
`retainedRows_ids` retains its original native-certificate dependency. -/
namespace N12Compact.RowIdentity
open S12
set_option Elab.async false

/-- A position in the unchanged original table, without copying its row data. -/
def rowAt (i : Fin 577) : CoverRow :=
  coverRows.get ⟨i.val, by simpa only [coverRows_count] using i.isLt⟩

theorem rowAt_mem (i : Fin 577) : rowAt i ∈ coverRows :=
  List.get_mem _ _

theorem retained_id_injective (r s : CoverRow)
    (hr : r ∈ retainedRows) (hs : s ∈ retainedRows)
    (he : r.originalId = s.originalId) : r = s := by
  have hn : (retainedRows.map CoverRow.originalId).Nodup := by
    rw [retainedRows_ids]
    exact survivors_distinct
  exact List.inj_on_of_nodup_map hn hr hs he

/-- A checked lookup binds every retained row of the named ID, not just one
selected row, to the actual family excluded by the geometric proof. -/
theorem family_at (i : Fin 577) (id : Nat) (family : Finset Nat)
    (checked : (rowAt i).originalId = id ∧ (rowAt i).groups = family)
    (r : CoverRow) (hr : r ∈ retainedRows) (he : r.originalId = id) :
    r.groups = family := by
  have hExpected : id ∈ expectedIds := by
    have h : r.originalId ∈ expectedIds :=
      of_decide_eq_true (List.mem_filter.mp hr).2
    simpa only [he] using h
  have hw : rowAt i ∈ retainedRows :=
    List.mem_filter.mpr ⟨rowAt_mem i,
      decide_eq_true (by simpa only [checked.1] using hExpected)⟩
  have heq : r = rowAt i :=
    retained_id_injective r (rowAt i) hr hw (he.trans checked.1.symm)
  rw [heq]
  exact checked.2

#print axioms family_at
end N12Compact.RowIdentity
