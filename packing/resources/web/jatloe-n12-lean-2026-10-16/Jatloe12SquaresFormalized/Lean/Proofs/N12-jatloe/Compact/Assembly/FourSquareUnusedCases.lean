import Compact.Cases.FourSquareUnused
import Completion.Contracts
import Compact.Assembly.RowIdentity

/-! Original whole-case obligations, with exact convex entrance proofs. -/
namespace N12Compact.FourSquareUnusedCases
open S12 S12Completion
set_option Elab.async false
set_option maxRecDepth 10000
set_option maxHeartbeats 0

def coveredIds : Finset Nat := {841,842}

def coveredFamilies : List (Nat × Finset Nat) :=
  [(841,family841),(842,family842)]

theorem covered_families_excluded : ∀ entry ∈ coveredFamilies, ExcludesFamily entry.2 := by
  intro entry h
  simp only [coveredFamilies, List.mem_cons, List.not_mem_nil, or_false] at h
  rcases h with rfl | rfl
  · exact case841_impossible
  · exact case842_impossible

private theorem row841_checked :
    (RowIdentity.rowAt 428).originalId = 841 ∧
    (RowIdentity.rowAt 428).groups = family841 := by decide +kernel

private theorem row842_checked :
    (RowIdentity.rowAt 429).originalId = 842 ∧
    (RowIdentity.rowAt 429).groups = family842 := by decide +kernel

theorem covered_rows_checked : ∀ r ∈ retainedRows, r.originalId ∈ coveredIds →
    (r.originalId, r.groups) ∈ coveredFamilies := by
  intro r hr hid
  simp only [coveredIds, Finset.mem_insert, Finset.mem_singleton] at hid
  rcases hid with h | h
  · have hf := RowIdentity.family_at 428 841 family841 row841_checked r hr h
    simpa only [h, hf] using
      (show (841, family841) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 429 842 family842 row842_checked r hr h
    simpa only [h, hf] using
      (show (842, family842) ∈ coveredFamilies from by simp [coveredFamilies])

theorem covered_cases_excluded (id : Nat) (hid : id ∈ coveredIds) : ExcludesCase id := by
  intro r hr he
  exact covered_families_excluded (r.originalId, r.groups)
    (covered_rows_checked r hr (by simpa only [he] using hid))

#print axioms covered_cases_excluded
end N12Compact.FourSquareUnusedCases
