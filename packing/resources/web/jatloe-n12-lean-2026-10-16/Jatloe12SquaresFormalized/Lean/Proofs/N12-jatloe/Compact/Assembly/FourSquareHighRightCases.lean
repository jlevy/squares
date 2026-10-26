import Compact.Cases.FourSquareHighRight
import Completion.Contracts
import Compact.Assembly.RowIdentity

/-! All thirteen original obligations of the higher-right family. -/
namespace N12Compact.FourSquareHighRightCases
open S12 S12Completion
set_option Elab.async false
set_option maxRecDepth 10000
set_option maxHeartbeats 0

def coveredIds : Finset Nat := {678,680,691,694,711,846,847,852,853,886,887,1073,1074}

def coveredFamilies : List (Nat × Finset Nat) :=
  [(678,family678),(680,family680),(691,family691),(694,family694),(711,family711),(846,family846),(847,family847),(852,family852),(853,family853),(886,family886),(887,family887),(1073,family1073),(1074,family1074)]

theorem covered_families_excluded : ∀ entry ∈ coveredFamilies, ExcludesFamily entry.2 := by
  intro entry h
  simp only [coveredFamilies, List.mem_cons, List.not_mem_nil, or_false] at h
  rcases h with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl
  · exact case678_impossible
  · exact case680_impossible
  · exact case691_impossible
  · exact case694_impossible
  · exact case711_impossible
  · exact case846_impossible
  · exact case847_impossible
  · exact case852_impossible
  · exact case853_impossible
  · exact case886_impossible
  · exact case887_impossible
  · exact case1073_impossible
  · exact case1074_impossible

private theorem row678_checked :
    (RowIdentity.rowAt 359).originalId = 678 ∧
    (RowIdentity.rowAt 359).groups = family678 := by decide +kernel

private theorem row680_checked :
    (RowIdentity.rowAt 361).originalId = 680 ∧
    (RowIdentity.rowAt 361).groups = family680 := by decide +kernel

private theorem row691_checked :
    (RowIdentity.rowAt 372).originalId = 691 ∧
    (RowIdentity.rowAt 372).groups = family691 := by decide +kernel

private theorem row694_checked :
    (RowIdentity.rowAt 375).originalId = 694 ∧
    (RowIdentity.rowAt 375).groups = family694 := by decide +kernel

private theorem row711_checked :
    (RowIdentity.rowAt 392).originalId = 711 ∧
    (RowIdentity.rowAt 392).groups = family711 := by decide +kernel

private theorem row846_checked :
    (RowIdentity.rowAt 433).originalId = 846 ∧
    (RowIdentity.rowAt 433).groups = family846 := by decide +kernel

private theorem row847_checked :
    (RowIdentity.rowAt 434).originalId = 847 ∧
    (RowIdentity.rowAt 434).groups = family847 := by decide +kernel

private theorem row852_checked :
    (RowIdentity.rowAt 439).originalId = 852 ∧
    (RowIdentity.rowAt 439).groups = family852 := by decide +kernel

private theorem row853_checked :
    (RowIdentity.rowAt 440).originalId = 853 ∧
    (RowIdentity.rowAt 440).groups = family853 := by decide +kernel

private theorem row886_checked :
    (RowIdentity.rowAt 473).originalId = 886 ∧
    (RowIdentity.rowAt 473).groups = family886 := by decide +kernel

private theorem row887_checked :
    (RowIdentity.rowAt 474).originalId = 887 ∧
    (RowIdentity.rowAt 474).groups = family887 := by decide +kernel

private theorem row1073_checked :
    (RowIdentity.rowAt 557).originalId = 1073 ∧
    (RowIdentity.rowAt 557).groups = family1073 := by decide +kernel

private theorem row1074_checked :
    (RowIdentity.rowAt 558).originalId = 1074 ∧
    (RowIdentity.rowAt 558).groups = family1074 := by decide +kernel

theorem covered_rows_checked : ∀ r ∈ retainedRows, r.originalId ∈ coveredIds →
    (r.originalId, r.groups) ∈ coveredFamilies := by
  intro r hr hid
  simp only [coveredIds, Finset.mem_insert, Finset.mem_singleton] at hid
  rcases hid with h | h | h | h | h | h | h | h | h | h | h | h | h
  · have hf := RowIdentity.family_at 359 678 family678 row678_checked r hr h
    simpa only [h, hf] using
      (show (678, family678) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 361 680 family680 row680_checked r hr h
    simpa only [h, hf] using
      (show (680, family680) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 372 691 family691 row691_checked r hr h
    simpa only [h, hf] using
      (show (691, family691) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 375 694 family694 row694_checked r hr h
    simpa only [h, hf] using
      (show (694, family694) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 392 711 family711 row711_checked r hr h
    simpa only [h, hf] using
      (show (711, family711) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 433 846 family846 row846_checked r hr h
    simpa only [h, hf] using
      (show (846, family846) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 434 847 family847 row847_checked r hr h
    simpa only [h, hf] using
      (show (847, family847) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 439 852 family852 row852_checked r hr h
    simpa only [h, hf] using
      (show (852, family852) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 440 853 family853 row853_checked r hr h
    simpa only [h, hf] using
      (show (853, family853) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 473 886 family886 row886_checked r hr h
    simpa only [h, hf] using
      (show (886, family886) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 474 887 family887 row887_checked r hr h
    simpa only [h, hf] using
      (show (887, family887) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 557 1073 family1073 row1073_checked r hr h
    simpa only [h, hf] using
      (show (1073, family1073) ∈ coveredFamilies from by simp [coveredFamilies])
  · have hf := RowIdentity.family_at 558 1074 family1074 row1074_checked r hr h
    simpa only [h, hf] using
      (show (1074, family1074) ∈ coveredFamilies from by simp [coveredFamilies])

theorem covered_cases_excluded (id : Nat) (hid : id ∈ coveredIds) : ExcludesCase id := by
  intro r hr he
  exact covered_families_excluded (r.originalId, r.groups)
    (covered_rows_checked r hr (by simpa only [he] using hid))

#print axioms covered_cases_excluded
end N12Compact.FourSquareHighRightCases
