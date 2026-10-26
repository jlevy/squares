import Compact.Cases.FourSquareConvex
import Completion.Contracts
import Compact.Assembly.RowIdentity

/-! Original whole-case obligations, with exact convex entrance proofs. -/
namespace N12Compact.FourSquareConvexCases
open S12 S12Completion
set_option Elab.async false
set_option maxRecDepth 10000
set_option maxHeartbeats 0

def coveredIds : Finset Nat := {445,454,862,864,992,995,998,1001,1002}

def coveredFamilies : List (Nat × Finset Nat) :=
  [(445,family445),(454,family454),(862,family862),(864,family864),(992,family992),(995,family995),(998,family998),(1001,family1001),(1002,family1002)]

theorem covered_families_excluded : ∀ entry ∈ coveredFamilies, ExcludesFamily entry.2 := by
  intro entry h
  simp only [coveredFamilies, List.mem_cons, List.not_mem_nil, or_false] at h
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact case445_impossible
  · exact case454_impossible
  · exact case862_impossible
  · exact case864_impossible
  · exact case992_impossible
  · exact case995_impossible
  · exact case998_impossible
  · exact case1001_impossible
  · exact case1002_impossible

private theorem row445_checked :
    (RowIdentity.rowAt 242).originalId = 445 ∧
    (RowIdentity.rowAt 242).groups = family445 := by decide +kernel

private theorem row454_checked :
    (RowIdentity.rowAt 251).originalId = 454 ∧
    (RowIdentity.rowAt 251).groups = family454 := by decide +kernel

private theorem row862_checked :
    (RowIdentity.rowAt 449).originalId = 862 ∧
    (RowIdentity.rowAt 449).groups = family862 := by decide +kernel

private theorem row864_checked :
    (RowIdentity.rowAt 451).originalId = 864 ∧
    (RowIdentity.rowAt 451).groups = family864 := by decide +kernel

private theorem row992_checked :
    (RowIdentity.rowAt 523).originalId = 992 ∧
    (RowIdentity.rowAt 523).groups = family992 := by decide +kernel

private theorem row995_checked :
    (RowIdentity.rowAt 526).originalId = 995 ∧
    (RowIdentity.rowAt 526).groups = family995 := by decide +kernel

private theorem row998_checked :
    (RowIdentity.rowAt 529).originalId = 998 ∧
    (RowIdentity.rowAt 529).groups = family998 := by decide +kernel

private theorem row1001_checked :
    (RowIdentity.rowAt 532).originalId = 1001 ∧
    (RowIdentity.rowAt 532).groups = family1001 := by decide +kernel

private theorem row1002_checked :
    (RowIdentity.rowAt 533).originalId = 1002 ∧
    (RowIdentity.rowAt 533).groups = family1002 := by decide +kernel

theorem covered_rows_checked : ∀ r ∈ retainedRows, r.originalId ∈ coveredIds →
    (r.originalId, r.groups) ∈ coveredFamilies := by
  intro r hr hid
  simp only [coveredIds, Finset.mem_insert, Finset.mem_singleton] at hid
  rcases hid with h | h | h | h | h | h | h | h | h
  · have hf := RowIdentity.family_at 242 445 family445 row445_checked r hr h
    simpa only [h, hf] using
      (show (445, family445) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 251 454 family454 row454_checked r hr h
    simpa only [h, hf] using
      (show (454, family454) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 449 862 family862 row862_checked r hr h
    simpa only [h, hf] using
      (show (862, family862) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 451 864 family864 row864_checked r hr h
    simpa only [h, hf] using
      (show (864, family864) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 523 992 family992 row992_checked r hr h
    simpa only [h, hf] using
      (show (992, family992) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 526 995 family995 row995_checked r hr h
    simpa only [h, hf] using
      (show (995, family995) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 529 998 family998 row998_checked r hr h
    simpa only [h, hf] using
      (show (998, family998) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 532 1001 family1001 row1001_checked r hr h
    simpa only [h, hf] using
      (show (1001, family1001) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 533 1002 family1002 row1002_checked r hr h
    simpa only [h, hf] using
      (show (1002, family1002) ∈ coveredFamilies from by simp [coveredFamilies])

theorem covered_cases_excluded (id : Nat) (hid : id ∈ coveredIds) : ExcludesCase id := by
  intro r hr he
  exact covered_families_excluded (r.originalId, r.groups)
    (covered_rows_checked r hr (by simpa only [he] using hid))

#print axioms covered_cases_excluded
end N12Compact.FourSquareConvexCases
