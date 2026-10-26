import Compact.Cases.MergedLower.Complete
import Compact.Assembly.RowIdentity

/-! Bind all four compact exclusions to every original retained row of its ID.
No historical lower-bar pose or refined-domain entrance is assumed. -/
namespace N12Compact.MergedLowerCases
open S12 S12Completion MergedLower
set_option Elab.async false
set_option maxRecDepth 10000
set_option maxHeartbeats 0

def coveredIds : Finset Nat := {71,80,589,590}

private theorem row71_checked :
    (RowIdentity.rowAt 110).originalId = 71 ∧
    (RowIdentity.rowAt 110).groups = family71 := by decide +kernel

private theorem row80_checked :
    (RowIdentity.rowAt 119).originalId = 80 ∧
    (RowIdentity.rowAt 119).groups = family80 := by decide +kernel

private theorem row589_checked :
    (RowIdentity.rowAt 330).originalId = 589 ∧
    (RowIdentity.rowAt 330).groups = family589 := by decide +kernel

private theorem row590_checked :
    (RowIdentity.rowAt 331).originalId = 590 ∧
    (RowIdentity.rowAt 331).groups = family590 := by decide +kernel

theorem covered_cases_excluded (id : Nat) (hid : id ∈ coveredIds) : ExcludesCase id := by
  intro r hr he p hf
  simp only [coveredIds, Finset.mem_insert, Finset.mem_singleton] at hid
  rcases hid with rfl | rfl | rfl | rfl
  · exact case71_impossible p (hf.trans
      (RowIdentity.family_at 110 71 family71 row71_checked r hr he))
  · exact case80_impossible p (hf.trans
      (RowIdentity.family_at 119 80 family80 row80_checked r hr he))
  · exact case589_impossible p (hf.trans
      (RowIdentity.family_at 330 589 family589 row589_checked r hr he))
  · exact case590_impossible p (hf.trans
      (RowIdentity.family_at 331 590 family590 row590_checked r hr he))

#print axioms covered_cases_excluded
end N12Compact.MergedLowerCases
