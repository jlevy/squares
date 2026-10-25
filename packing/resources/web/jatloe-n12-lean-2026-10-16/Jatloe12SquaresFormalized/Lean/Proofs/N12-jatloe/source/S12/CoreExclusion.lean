import S12.SpecPacking
import Mathlib.Data.List.Forall2

namespace S12
set_option maxHeartbeats 0

inductive OwnerSpec where
  | single (k : Fin 2) (w : SingleSpec) (checked : w.Check)
  | combined (w : CombinedSpec) (checked : w.Check)

def OwnerSpec.mask : OwnerSpec → Nat
  | .single _ w _ => w.mask | .combined w _ => w.mask
def OwnerSpec.kind : OwnerSpec → Fin 3
  | .single k _ _ => auxKind k | .combined _ _ => 2
def OwnerSpec.allowed : OwnerSpec → List (Finset Nat)
  | .single _ w _ => w.allowed | .combined w _ => w.allowed
def OwnerSpec.Matches (s : OwnerSpec) (family : Finset Nat) : Prop :=
  match s with
  | .single k w _ => w.Matches family k
  | .combined w _ => w.Matches family
instance (s : OwnerSpec) (family : Finset Nat) : Decidable (s.Matches family) := by
  cases s <;> unfold OwnerSpec.Matches <;> infer_instance

noncomputable def ownersForKind (p : NormalizedPacking) (kind : Fin 3) (i : Fin 12) : Finset Nat :=
  if h : kind.val<2 then natAuxOwners p ⟨kind.val,h⟩ i else natCombinedOwners p i

theorem ownersForKind_single (p : NormalizedPacking) (k : Fin 2) (i : Fin 12) :
    ownersForKind p (auxKind k) i=natAuxOwners p k i := by simp [ownersForKind,auxKind,k.isLt]
theorem ownersForKind_combined (p : NormalizedPacking) (i : Fin 12) :
    ownersForKind p 2 i=natCombinedOwners p i := by simp [ownersForKind]

theorem ownersForKind_disjoint (p : NormalizedPacking) (kind : Fin 3) (i j : Fin 12) (hij : i≠j) :
    Disjoint (ownersForKind p kind i) (ownersForKind p kind j) := by
  unfold ownersForKind
  split_ifs
  · exact nat_aux_disjoint p _ i j hij
  · exact nat_combined_disjoint p i j hij

theorem OwnerSpec.actual (s : OwnerSpec) (family : Finset Nat) (hmatch : s.Matches family)
    (p : NormalizedPacking) (i : Fin 12) (hf : codedMarkerFamily p=family)
    (hm : markerCode p i=s.mask) : ownersForKind p s.kind i∈s.allowed := by
  cases s with
  | single k w hw =>
    change ownersForKind p (auxKind k) i∈w.allowed
    rw [ownersForKind_single]
    exact w.actual hw family k hmatch p i hf hm
  | combined w hw =>
    change ownersForKind p 2 i∈w.allowed
    rw [ownersForKind_combined]
    exact w.actual hw family hmatch p i hf hm

noncomputable def ownerIndex (p : NormalizedPacking) (m : Nat) : Fin 12 :=
  if h : ∃ i,markerCode p i=m then Classical.choose h else 0

theorem ownerIndex_spec (p : NormalizedPacking) (m : Nat) (hm : m∈codedMarkerFamily p) :
    markerCode p (ownerIndex p m)=m := by
  obtain ⟨i,_,he⟩ := Finset.mem_image.mp hm
  have hex : ∃ i,markerCode p i=m := ⟨i,he⟩
  simp only [ownerIndex,dif_pos hex]
  exact Classical.choose_spec hex

structure CoreProof where
  family : Finset Nat
  mode : Fin 3
  specs : List OwnerSpec

def CoreProof.Check (w : CoreProof) : Prop :=
  (∀ s∈w.specs, s.mask∈w.family ∧ s.kind=w.mode ∧ s.Matches w.family) ∧
  w.specs.Pairwise (fun s t => s.mask≠t.mask) ∧
  feasible (w.specs.map OwnerSpec.allowed) ∅=false
instance (w : CoreProof) : Decidable w.Check := inferInstanceAs (Decidable (_ ∧ _))

/-- A rejected core of owner domains excludes the complete real packing.
All owner indices, point-order conventions and disjointness are proved here. -/
theorem CoreProof.sound (w : CoreProof) (hw : w.Check) (p : NormalizedPacking)
    (hf : codedMarkerFamily p=w.family) : False := by
  let actual := fun s : OwnerSpec => ownersForKind p w.mode (ownerIndex p s.mask)
  have hcode : ∀ s∈w.specs, markerCode p (ownerIndex p s.mask)=s.mask := by
    intro s hs
    apply ownerIndex_spec
    rw [hf]
    exact (hw.1 s hs).1
  have hmem : ∀ s∈w.specs,actual s∈s.allowed := by
    intro s hs
    have hh := hw.1 s hs
    have ha := s.actual w.family hh.2.2 p (ownerIndex p s.mask) hf (hcode s hs)
    simpa only [actual,hh.2.1] using ha
  have hmapped : List.Forall₂ (fun m d => m∈d) (w.specs.map actual)
      (w.specs.map OwnerSpec.allowed) := by
    rw [List.forall₂_map_left_iff,List.forall₂_map_right_iff,List.forall₂_same]
    exact hmem
  have hpair : (w.specs.map actual).Pairwise Disjoint := by
    rw [List.pairwise_map]
    apply (List.Pairwise.and_mem.mp hw.2.1).imp
    intro s t h
    apply ownersForKind_disjoint
    intro he
    exact h.2.2 ((hcode s h.1).symm.trans ((congrArg (markerCode p) he).trans (hcode t h.2.1)))
  exact rejected_domain_impossible _ hw.2.2
    (actual_owners_give_assignment _ _ ∅ hmapped (by intros; exact Finset.disjoint_empty_right _) hpair)

#print axioms CoreProof.sound
end S12
