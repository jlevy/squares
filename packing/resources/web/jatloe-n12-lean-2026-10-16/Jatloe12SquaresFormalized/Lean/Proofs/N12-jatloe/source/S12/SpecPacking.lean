import S12.CombinedPacking

namespace S12
open S12Pilot
set_option maxHeartbeats 0

def SingleSpec.Matches (w : SingleSpec) (family : Finset Nat) (k : Fin 2) : Prop :=
  w.kind=auxKind k ∧ w.lower=(if w.mask∈auxExempt k then 0 else 1) ∧
  w.upper=(family∩auxExempt k).card-2+w.lower
instance (w : SingleSpec) (family : Finset Nat) (k : Fin 2) : Decidable (w.Matches family k) :=
  inferInstanceAs (Decidable (_ ∧ _))

theorem SingleSpec.actual (w : SingleSpec) (hw : w.Check) (family : Finset Nat)
    (k : Fin 2) (hmatch : w.Matches family k) (p : NormalizedPacking) (i : Fin 12)
    (hf : codedMarkerFamily p=family) (hm : markerCode p i=w.mask) :
    natAuxOwners p k i∈w.allowed := by
  have ha : 1<(p.square i).side := by rw [p.congruent]; exact p.side_gt_one
  have hsize : (p.square i).side≤1001/1000 := by rw [p.congruent]; exact p.side_le
  have hb := nat_aux_budget p k i
  rw [hf,hm] at hb
  apply w.sound hw _ ha hsize (p.contained i)
    (by simpa only [hm] using coded_exact p i) _
    (by simpa only [hmatch.1] using nat_aux_exact p k i) (nat_aux_subset p k i)
  · simpa only [hmatch.2.1] using hb.1
  · simpa only [hmatch.2.2,hmatch.2.1] using hb.2

def CombinedSpec.Matches (w : CombinedSpec) (family : Finset Nat) : Prop :=
  w.first.val.Matches family 0 ∧ w.second.val.Matches family 1
instance (w : CombinedSpec) (family : Finset Nat) : Decidable (w.Matches family) :=
  inferInstanceAs (Decidable (_ ∧ _))

theorem CombinedSpec.actual (w : CombinedSpec) (hw : w.Check) (family : Finset Nat)
    (hmatch : w.Matches family) (p : NormalizedPacking) (i : Fin 12)
    (hf : codedMarkerFamily p=family) (hm : markerCode p i=w.mask) :
    natCombinedOwners p i∈w.allowed := by
  have ha : 1<(p.square i).side := by rw [p.congruent]; exact p.side_gt_one
  have hsize : (p.square i).side≤1001/1000 := by rw [p.congruent]; exact p.side_le
  exact w.sound hw _ ha hsize (p.contained i)
    (by simpa only [hm] using coded_exact p i) _ _
    (w.first.val.actual w.first.property family 0 hmatch.1 p i hf (hm.trans hw.1.symm))
    (w.second.val.actual w.second.property family 1 hmatch.2 p i hf (hm.trans hw.2.1.symm))
    (nat_combined_exact p i)

end S12
