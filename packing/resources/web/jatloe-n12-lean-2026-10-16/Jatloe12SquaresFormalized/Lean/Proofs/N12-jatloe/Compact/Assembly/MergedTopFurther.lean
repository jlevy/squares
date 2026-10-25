import Compact.Cases.MergedTopFurther.Complete
import Compact.Assembly.RowIdentity

/-! The three whole original cases share a single geometric endgame.
No source proof in this file has yet been compiled. -/
namespace N12Compact.MergedTopFurtherAssembly
open S12 S12Completion
set_option Elab.async false

private theorem row697 :
    (RowIdentity.rowAt 378).originalId = 697 ∧
    (RowIdentity.rowAt 378).groups = MergedTopFurther.family .base := by decide +kernel
private theorem row698 :
    (RowIdentity.rowAt 379).originalId = 698 ∧
    (RowIdentity.rowAt 379).groups = MergedTopFurther.family .mergeRight := by decide +kernel
private theorem row699 :
    (RowIdentity.rowAt 380).originalId = 699 ∧
    (RowIdentity.rowAt 380).groups = MergedTopFurther.family .mergeBottom := by decide +kernel

theorem excludes697 : ExcludesCase 697 := by
  intro r hr hid p hf
  exact MergedTopFurther.impossible .base p
    (hf.trans (RowIdentity.family_at 378 697 (MergedTopFurther.family .base) row697 r hr hid))
theorem excludes698 : ExcludesCase 698 := by
  intro r hr hid p hf
  exact MergedTopFurther.impossible .mergeRight p
    (hf.trans (RowIdentity.family_at 379 698 (MergedTopFurther.family .mergeRight) row698 r hr hid))
theorem excludes699 : ExcludesCase 699 := by
  intro r hr hid p hf
  exact MergedTopFurther.impossible .mergeBottom p
    (hf.trans (RowIdentity.family_at 380 699 (MergedTopFurther.family .mergeBottom) row699 r hr hid))

#print axioms excludes697
#print axioms excludes698
#print axioms excludes699
end N12Compact.MergedTopFurtherAssembly
