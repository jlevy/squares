import Compact.Cases.OppositeCentralWalls.Complete
import Compact.Assembly.RowIdentity

/-! Eight whole original cases use one shared continuous geometric argument.
Source assembly only; the full Lean replay remains deferred. -/
namespace N12Compact.OppositeCentralWallsAssembly
open S12 S12Completion
set_option Elab.async false

private theorem row709 :
    (RowIdentity.rowAt 390).originalId = 709 ∧
    (RowIdentity.rowAt 390).groups = OppositeCentralWalls.family .c709 := by decide +kernel

theorem excludes709 : ExcludesCase 709 := by
  intro r hr hid p hf
  exact OppositeCentralWalls.impossible .c709 p
    (hf.trans (RowIdentity.family_at 390 709
      (OppositeCentralWalls.family .c709) row709 r hr hid))

private theorem row882 :
    (RowIdentity.rowAt 469).originalId = 882 ∧
    (RowIdentity.rowAt 469).groups = OppositeCentralWalls.family .c882 := by decide +kernel

theorem excludes882 : ExcludesCase 882 := by
  intro r hr hid p hf
  exact OppositeCentralWalls.impossible .c882 p
    (hf.trans (RowIdentity.family_at 469 882
      (OppositeCentralWalls.family .c882) row882 r hr hid))

private theorem row890 :
    (RowIdentity.rowAt 477).originalId = 890 ∧
    (RowIdentity.rowAt 477).groups = OppositeCentralWalls.family .c890 := by decide +kernel

theorem excludes890 : ExcludesCase 890 := by
  intro r hr hid p hf
  exact OppositeCentralWalls.impossible .c890 p
    (hf.trans (RowIdentity.family_at 477 890
      (OppositeCentralWalls.family .c890) row890 r hr hid))

private theorem row1075 :
    (RowIdentity.rowAt 559).originalId = 1075 ∧
    (RowIdentity.rowAt 559).groups = OppositeCentralWalls.family .c1075 := by decide +kernel

theorem excludes1075 : ExcludesCase 1075 := by
  intro r hr hid p hf
  exact OppositeCentralWalls.impossible .c1075 p
    (hf.trans (RowIdentity.family_at 559 1075
      (OppositeCentralWalls.family .c1075) row1075 r hr hid))

private theorem row1077 :
    (RowIdentity.rowAt 561).originalId = 1077 ∧
    (RowIdentity.rowAt 561).groups = OppositeCentralWalls.family .c1077 := by decide +kernel

theorem excludes1077 : ExcludesCase 1077 := by
  intro r hr hid p hf
  exact OppositeCentralWalls.impossible .c1077 p
    (hf.trans (RowIdentity.family_at 561 1077
      (OppositeCentralWalls.family .c1077) row1077 r hr hid))

private theorem row1078 :
    (RowIdentity.rowAt 562).originalId = 1078 ∧
    (RowIdentity.rowAt 562).groups = OppositeCentralWalls.family .c1078 := by decide +kernel

theorem excludes1078 : ExcludesCase 1078 := by
  intro r hr hid p hf
  exact OppositeCentralWalls.impossible .c1078 p
    (hf.trans (RowIdentity.family_at 562 1078
      (OppositeCentralWalls.family .c1078) row1078 r hr hid))

private theorem row1081 :
    (RowIdentity.rowAt 565).originalId = 1081 ∧
    (RowIdentity.rowAt 565).groups = OppositeCentralWalls.family .c1081 := by decide +kernel

theorem excludes1081 : ExcludesCase 1081 := by
  intro r hr hid p hf
  exact OppositeCentralWalls.impossible .c1081 p
    (hf.trans (RowIdentity.family_at 565 1081
      (OppositeCentralWalls.family .c1081) row1081 r hr hid))

private theorem row1083 :
    (RowIdentity.rowAt 567).originalId = 1083 ∧
    (RowIdentity.rowAt 567).groups = OppositeCentralWalls.family .c1083 := by decide +kernel

theorem excludes1083 : ExcludesCase 1083 := by
  intro r hr hid p hf
  exact OppositeCentralWalls.impossible .c1083 p
    (hf.trans (RowIdentity.family_at 567 1083
      (OppositeCentralWalls.family .c1083) row1083 r hr hid))

#print axioms excludes709
#print axioms excludes882
#print axioms excludes890
#print axioms excludes1075
#print axioms excludes1077
#print axioms excludes1078
#print axioms excludes1081
#print axioms excludes1083
end N12Compact.OppositeCentralWallsAssembly
