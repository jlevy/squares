import Compact.Cases.FourSquareVariant
import Completion.Contracts
import Compact.Assembly.RowIdentity

/-! Complete original case obligations for the eleven row-barrier variants. -/
namespace N12Compact.FourSquareVariantCases
open S12 S12Completion
set_option Elab.async false
set_option maxRecDepth 10000
set_option maxHeartbeats 0

def coveredIds : Finset Nat := {405,424,985,990,993,994,999,1063,1064,1069,1070}

def coveredFamilies : List (Nat × Finset Nat) :=
  [(405,family405),(424,family424),(985,family985),(990,family990),(993,family993),(994,family994),(999,family999),(1063,family1063),(1064,family1064),(1069,family1069),(1070,family1070)]

theorem covered_families_excluded : ∀ entry ∈ coveredFamilies, ExcludesFamily entry.2 := by
  intro entry h
  simp only [coveredFamilies, List.mem_cons, List.not_mem_nil, or_false] at h
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact case405_impossible
  · exact case424_impossible
  · exact case985_impossible
  · exact case990_impossible
  · exact case993_impossible
  · exact case994_impossible
  · exact case999_impossible
  · exact case1063_impossible
  · exact case1064_impossible
  · exact case1069_impossible
  · exact case1070_impossible

private theorem row405_checked :
    (RowIdentity.rowAt 202).originalId = 405 ∧
    (RowIdentity.rowAt 202).groups = family405 := by decide +kernel

private theorem row424_checked :
    (RowIdentity.rowAt 221).originalId = 424 ∧
    (RowIdentity.rowAt 221).groups = family424 := by decide +kernel

private theorem row985_checked :
    (RowIdentity.rowAt 516).originalId = 985 ∧
    (RowIdentity.rowAt 516).groups = family985 := by decide +kernel

private theorem row990_checked :
    (RowIdentity.rowAt 521).originalId = 990 ∧
    (RowIdentity.rowAt 521).groups = family990 := by decide +kernel

private theorem row993_checked :
    (RowIdentity.rowAt 524).originalId = 993 ∧
    (RowIdentity.rowAt 524).groups = family993 := by decide +kernel

private theorem row994_checked :
    (RowIdentity.rowAt 525).originalId = 994 ∧
    (RowIdentity.rowAt 525).groups = family994 := by decide +kernel

private theorem row999_checked :
    (RowIdentity.rowAt 530).originalId = 999 ∧
    (RowIdentity.rowAt 530).groups = family999 := by decide +kernel

private theorem row1063_checked :
    (RowIdentity.rowAt 547).originalId = 1063 ∧
    (RowIdentity.rowAt 547).groups = family1063 := by decide +kernel

private theorem row1064_checked :
    (RowIdentity.rowAt 548).originalId = 1064 ∧
    (RowIdentity.rowAt 548).groups = family1064 := by decide +kernel

private theorem row1069_checked :
    (RowIdentity.rowAt 553).originalId = 1069 ∧
    (RowIdentity.rowAt 553).groups = family1069 := by decide +kernel

private theorem row1070_checked :
    (RowIdentity.rowAt 554).originalId = 1070 ∧
    (RowIdentity.rowAt 554).groups = family1070 := by decide +kernel

theorem covered_rows_checked : ∀ r ∈ retainedRows, r.originalId ∈ coveredIds →
    (r.originalId, r.groups) ∈ coveredFamilies := by
  intro r hr hid
  simp only [coveredIds, Finset.mem_insert, Finset.mem_singleton] at hid
  rcases hid with h | h | h | h | h | h | h | h | h | h | h
  · have hf := RowIdentity.family_at 202 405 family405 row405_checked r hr h
    simpa only [h, hf] using
      (show (405, family405) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 221 424 family424 row424_checked r hr h
    simpa only [h, hf] using
      (show (424, family424) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 516 985 family985 row985_checked r hr h
    simpa only [h, hf] using
      (show (985, family985) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 521 990 family990 row990_checked r hr h
    simpa only [h, hf] using
      (show (990, family990) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 524 993 family993 row993_checked r hr h
    simpa only [h, hf] using
      (show (993, family993) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 525 994 family994 row994_checked r hr h
    simpa only [h, hf] using
      (show (994, family994) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 530 999 family999 row999_checked r hr h
    simpa only [h, hf] using
      (show (999, family999) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 547 1063 family1063 row1063_checked r hr h
    simpa only [h, hf] using
      (show (1063, family1063) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 548 1064 family1064 row1064_checked r hr h
    simpa only [h, hf] using
      (show (1064, family1064) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 553 1069 family1069 row1069_checked r hr h
    simpa only [h, hf] using
      (show (1069, family1069) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 554 1070 family1070 row1070_checked r hr h
    simpa only [h, hf] using
      (show (1070, family1070) ∈ coveredFamilies from by simp [coveredFamilies])

theorem covered_cases_excluded (id : Nat) (hid : id ∈ coveredIds) : ExcludesCase id := by
  intro r hr he
  exact covered_families_excluded (r.originalId, r.groups)
    (covered_rows_checked r hr (by simpa only [he] using hid))

#print axioms covered_cases_excluded
end N12Compact.FourSquareVariantCases
