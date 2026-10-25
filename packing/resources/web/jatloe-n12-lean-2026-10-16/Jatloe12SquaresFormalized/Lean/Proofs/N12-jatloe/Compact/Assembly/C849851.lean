import Compact.Cases.C849851.Complete
import Compact.Assembly.RowIdentity

/-! Whole original 849/851 exclusions, with both continuous orientation
sectors and their unchanged retained-row identities. Source only. -/
namespace N12Compact.C849851Assembly
open S12 S12Completion
set_option Elab.async false

private theorem row849 :
    (RowIdentity.rowAt 436).originalId = 849 ∧
    (RowIdentity.rowAt 436).groups = C849851.family false := by decide +kernel

private theorem row851 :
    (RowIdentity.rowAt 438).originalId = 851 ∧
    (RowIdentity.rowAt 438).groups = C849851.family true := by decide +kernel

theorem excludes849 : ExcludesCase 849 := by
  intro r hr hid p hf
  exact C849851.impossible false p
    (hf.trans (RowIdentity.family_at 436 849 (C849851.family false) row849 r hr hid))

theorem excludes851 : ExcludesCase 851 := by
  intro r hr hid p hf
  exact C849851.impossible true p
    (hf.trans (RowIdentity.family_at 438 851 (C849851.family true) row851 r hr hid))

#print axioms excludes849
#print axioms excludes851
end N12Compact.C849851Assembly
