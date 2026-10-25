import Compact.Bridge.C84Complete
import Compact.Assembly.RowIdentity

/-! The shared continuous pair contradiction fills the whole original
case84 contract. Source only, awaiting the final full-proof replay. -/
namespace N12Compact.C84Assembly
open S12 S12Completion
set_option Elab.async false

private theorem row84 :
    (RowIdentity.rowAt 123).originalId=84 ∧
    (RowIdentity.rowAt 123).groups=C84Ownership.family := by decide +kernel

theorem excludes_case : ExcludesCase 84 := by
  intro r hr hid p hf
  exact C84Complete.family_impossible p
    (hf.trans (RowIdentity.family_at 123 84 C84Ownership.family row84 r hr hid))

#print axioms excludes_case
end N12Compact.C84Assembly
