import Compact.Cases.FourSquareHighRightExtra
import Completion.Contracts
import Compact.Assembly.RowIdentity

/-! Original case obligations discharged by the shared higher-right geometry. -/
namespace N12Compact.FourSquareHighRightExtraCases
open S12 S12Completion
set_option Elab.async false
set_option maxRecDepth 10000
set_option maxHeartbeats 0

def coveredIds : Finset Nat := {669,670,673,674,675,690,848,850}

def coveredFamilies : List (Nat × Finset Nat) :=
  [(669,family669),(670,family670),(673,family673),(674,family674),(675,family675),(690,family690),(848,family848),(850,family850)]

theorem covered_families_excluded : ∀ entry ∈ coveredFamilies, ExcludesFamily entry.2 := by
  intro entry h
  simp only [coveredFamilies, List.mem_cons, List.not_mem_nil, or_false] at h
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact case669_impossible
  · exact case670_impossible
  · exact case673_impossible
  · exact case674_impossible
  · exact case675_impossible
  · exact case690_impossible
  · exact case848_impossible
  · exact case850_impossible

private theorem row669_checked :
    (RowIdentity.rowAt 350).originalId = 669 ∧
    (RowIdentity.rowAt 350).groups = family669 := by decide +kernel

private theorem row670_checked :
    (RowIdentity.rowAt 351).originalId = 670 ∧
    (RowIdentity.rowAt 351).groups = family670 := by decide +kernel

private theorem row673_checked :
    (RowIdentity.rowAt 354).originalId = 673 ∧
    (RowIdentity.rowAt 354).groups = family673 := by decide +kernel

private theorem row674_checked :
    (RowIdentity.rowAt 355).originalId = 674 ∧
    (RowIdentity.rowAt 355).groups = family674 := by decide +kernel

private theorem row675_checked :
    (RowIdentity.rowAt 356).originalId = 675 ∧
    (RowIdentity.rowAt 356).groups = family675 := by decide +kernel

private theorem row690_checked :
    (RowIdentity.rowAt 371).originalId = 690 ∧
    (RowIdentity.rowAt 371).groups = family690 := by decide +kernel

private theorem row848_checked :
    (RowIdentity.rowAt 435).originalId = 848 ∧
    (RowIdentity.rowAt 435).groups = family848 := by decide +kernel

private theorem row850_checked :
    (RowIdentity.rowAt 437).originalId = 850 ∧
    (RowIdentity.rowAt 437).groups = family850 := by decide +kernel

theorem covered_rows_checked : ∀ r ∈ retainedRows, r.originalId ∈ coveredIds →
    (r.originalId, r.groups) ∈ coveredFamilies := by
  intro r hr hid
  simp only [coveredIds, Finset.mem_insert, Finset.mem_singleton] at hid
  rcases hid with h | h | h | h | h | h | h | h
  · have hf := RowIdentity.family_at 350 669 family669 row669_checked r hr h
    simpa only [h, hf] using
      (show (669, family669) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 351 670 family670 row670_checked r hr h
    simpa only [h, hf] using
      (show (670, family670) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 354 673 family673 row673_checked r hr h
    simpa only [h, hf] using
      (show (673, family673) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 355 674 family674 row674_checked r hr h
    simpa only [h, hf] using
      (show (674, family674) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 356 675 family675 row675_checked r hr h
    simpa only [h, hf] using
      (show (675, family675) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 371 690 family690 row690_checked r hr h
    simpa only [h, hf] using
      (show (690, family690) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 435 848 family848 row848_checked r hr h
    simpa only [h, hf] using
      (show (848, family848) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 437 850 family850 row850_checked r hr h
    simpa only [h, hf] using
      (show (850, family850) ∈ coveredFamilies from by simp [coveredFamilies])

theorem covered_cases_excluded (id : Nat) (hid : id ∈ coveredIds) : ExcludesCase id := by
  intro r hr he
  exact covered_families_excluded (r.originalId, r.groups)
    (covered_rows_checked r hr (by simpa only [he] using hid))

#print axioms covered_cases_excluded
end N12Compact.FourSquareHighRightExtraCases
