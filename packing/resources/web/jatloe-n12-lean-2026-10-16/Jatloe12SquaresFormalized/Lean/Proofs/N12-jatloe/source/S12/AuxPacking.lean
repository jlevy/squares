import S12.DomainSpecs
import S12.FamilyTransport

namespace S12
open S12Pilot
set_option maxHeartbeats 0

def auxKind (k : Fin 2) : Fin 3 := ⟨k.val,by omega⟩
def auxExempt (k : Fin 2) : Finset Nat := if k.val=0 then exempt0 else exempt1

def gInverseIndex (i : Fin 10) : Fin 10 :=
  match i.val with
  | 0 => 2 | 1 => 5 | 2 => 0 | 3 => 8 | 4 => 3
  | 5 => 6 | 6 => 1 | 7 => 9 | 8 => 4 | _ => 7

theorem aux_f_point (i : Fin 10) : (auxPoints 0)[i.val]! = (fPoint i) := by
  fin_cases i <;> rfl
theorem aux_g_point (i : Fin 10) : (auxPoints 1)[(gInverseIndex i).val]! = (fPoint i).swap := by
  fin_cases i <;> rfl
theorem aux_kind_length (k : Fin 2) : (auxPoints (auxKind k)).length=10 := by
  fin_cases k <;> decide

noncomputable def sortedAuxOwners (p : NormalizedPacking) (k : Fin 2) (i : Fin 12) : Finset (Fin 10) := by
  classical
  exact Finset.univ.filter fun j =>
    (p.square i).Inside ((auxPoints (auxKind k))[j.val]!).1 ((auxPoints (auxKind k))[j.val]!).2
noncomputable def auxExemptIndices (p : NormalizedPacking) (k : Fin 2) : Finset (Fin 12) :=
  Finset.univ.filter fun i => markerCode p i∈auxExempt k
noncomputable def natAuxOwners (p : NormalizedPacking) (k : Fin 2) (i : Fin 12) : Finset Nat :=
  (sortedAuxOwners p k i).image Fin.val

theorem sorted_aux_disjoint (p : NormalizedPacking) (k : Fin 2) (i j : Fin 12) (hij : i≠j) :
    Disjoint (sortedAuxOwners p k i) (sortedAuxOwners p k j) := by
  classical
  apply Finset.disjoint_left.mpr
  intro m hi hj
  exact p.disjoint i j hij _ _ ⟨(Finset.mem_filter.mp hi).2,(Finset.mem_filter.mp hj).2⟩

theorem sorted_aux_forced (p : NormalizedPacking) (k : Fin 2) (i : Fin 12)
    (hi : i∉auxExemptIndices p k) : (sortedAuxOwners p k i).Nonempty := by
  classical
  by_contra he
  have hempty : ∀ j : Fin 10,
      ¬(p.square i).Inside ((auxPoints (auxKind k))[j.val]!).1 ((auxPoints (auxKind k))[j.val]!).2 := by
    intro j hj
    exact he ⟨j,Finset.mem_filter.mpr ⟨Finset.mem_univ _,hj⟩⟩
  have ha : 1<(p.square i).side := by rw [p.congruent]; exact p.side_gt_one
  fin_cases k
  · have hf : AvoidsF (p.square i) := by
      intro j hj
      apply hempty j
      change (p.square i).Inside ((auxPoints 0)[j.val]!).1 ((auxPoints 0)[j.val]!).2
      rw [aux_f_point]
      exact hj
    have hc := (code_f_exempt p i).mpr (avoidingF_forces_pair _ ha (p.contained i) hf)
    exact hi (by simpa [auxExemptIndices,auxExempt] using hc)
  · have hg : AvoidsG (p.square i) := by
      intro j hj
      apply hempty (gInverseIndex j)
      change (p.square i).Inside ((auxPoints 1)[(gInverseIndex j).val]!).1 ((auxPoints 1)[(gInverseIndex j).val]!).2
      rw [aux_g_point]
      exact hj
    have hc := (code_g_exempt p i).mpr (avoidingG_forces_pair _ ha (p.contained i) hg)
    exact hi (by simpa [auxExemptIndices,auxExempt] using hc)

theorem aux_exempt_image (p : NormalizedPacking) (k : Fin 2) :
    (auxExemptIndices p k).image (markerCode p)=codedMarkerFamily p∩auxExempt k := by
  ext m
  constructor
  · intro hm
    obtain ⟨i,hi,rfl⟩ := Finset.mem_image.mp hm
    exact Finset.mem_inter.mpr ⟨Finset.mem_image.mpr ⟨i,Finset.mem_univ _,rfl⟩,
      (Finset.mem_filter.mp hi).2⟩
  · intro hm
    obtain ⟨hf,he⟩ := Finset.mem_inter.mp hm
    obtain ⟨i,_,rfl⟩ := Finset.mem_image.mp hf
    exact Finset.mem_image.mpr ⟨i,Finset.mem_filter.mpr ⟨Finset.mem_univ _,he⟩,rfl⟩

theorem nat_aux_card (p : NormalizedPacking) (k : Fin 2) (i : Fin 12) :
    (natAuxOwners p k i).card=(sortedAuxOwners p k i).card :=
  Finset.card_image_of_injective _ Fin.val_injective

theorem nat_aux_subset (p : NormalizedPacking) (k : Fin 2) (i : Fin 12) :
    natAuxOwners p k i⊆Finset.range 10 := by
  intro j hj
  obtain ⟨m,_,rfl⟩ := Finset.mem_image.mp hj
  exact Finset.mem_range.mpr m.isLt

theorem nat_aux_exact (p : NormalizedPacking) (k : Fin 2) (i : Fin 12) :
    AuxExact (p.square i) (auxKind k) (natAuxOwners p k i) := by
  classical
  intro j hj
  have hlt : j<10 := by simpa only [aux_kind_length] using List.mem_range.mp hj
  constructor
  · intro hi
    exact Finset.mem_image.mpr ⟨⟨j,hlt⟩,Finset.mem_filter.mpr ⟨Finset.mem_univ _,hi⟩,rfl⟩
  · intro hi
    obtain ⟨m,hm,he⟩ := Finset.mem_image.mp hi
    have h := (Finset.mem_filter.mp hm).2
    simpa only [he] using h

theorem nat_aux_disjoint (p : NormalizedPacking) (k : Fin 2) (i j : Fin 12) (hij : i≠j) :
    Disjoint (natAuxOwners p k i) (natAuxOwners p k j) := by
  apply Finset.disjoint_left.mpr
  intro n hi hj
  obtain ⟨a,ha,he⟩ := Finset.mem_image.mp hi
  obtain ⟨b,hb,hf⟩ := Finset.mem_image.mp hj
  have hab : a=b := Fin.val_injective (he.trans hf.symm)
  subst b
  exact Finset.disjoint_left.mp (sorted_aux_disjoint p k i j hij) ha hb

/-- Cardinality bounds for the exact sorted F/G point ordering used in the
domain data, rather than an implicitly identified transposed ordering. -/
theorem nat_aux_budget (p : NormalizedPacking) (k : Fin 2) (i : Fin 12) :
    (if markerCode p i∈auxExempt k then 0 else 1)≤(natAuxOwners p k i).card ∧
    (natAuxOwners p k i).card≤(codedMarkerFamily p∩auxExempt k).card-2+
      (if markerCode p i∈auxExempt k then 0 else 1) := by
  have hcard : (auxExemptIndices p k).card=(codedMarkerFamily p∩auxExempt k).card := by
    rw [← aux_exempt_image,Finset.card_image_of_injective _ (markerCode_injective p)]
  have hmem : i∈auxExemptIndices p k ↔ markerCode p i∈auxExempt k := by simp [auxExemptIndices]
  have hh := individual_budget (sortedAuxOwners p k) (auxExemptIndices p k)
    (sorted_aux_disjoint p k) (sorted_aux_forced p k) i
  rw [← nat_aux_card,hcard] at hh
  simp only [hmem] at hh
  refine ⟨?_,hh⟩
  by_cases he : markerCode p i∈auxExempt k
  · simp [he]
  · have hn := sorted_aux_forced p k i (by simpa only [hmem] using he)
    rw [nat_aux_card]
    simp only [he,if_false]
    exact Finset.card_pos.mpr hn

#print axioms nat_aux_budget
end S12
