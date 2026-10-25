import Compact.Cases.Endpoint684
import Compact.Assembly.RowIdentity

/-! Original retained-row binding of the whole six-alternative endpoint proof.
This new source has not been compiled. -/
namespace N12Compact.Endpoint684Assembly
open S12 S12Completion
set_option Elab.async false
set_option maxRecDepth 10000

private theorem row_checked :
    (RowIdentity.rowAt 365).originalId = 684 ∧
    (RowIdentity.rowAt 365).groups = Endpoint684.family := by decide +kernel

theorem excludes_case : ExcludesCase 684 := by
  intro r hr hid p hf
  exact Endpoint684.case684_impossible p
    (hf.trans (RowIdentity.family_at 365 684 Endpoint684.family row_checked r hr hid))

#print axioms excludes_case
end N12Compact.Endpoint684Assembly
