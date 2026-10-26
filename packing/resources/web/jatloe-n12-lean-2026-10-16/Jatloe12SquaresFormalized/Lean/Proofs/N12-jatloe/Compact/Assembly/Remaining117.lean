import Completion.Contracts

/-! A proof-bearing completion boundary over the original 117 cases.
Known IDs are derived from actual ExcludesCase proof terms, never from a
status list. The empty registry leaves all117 obligations pending. This
route invokes the genuine117-case classification directly and never assumes
the unfinished historical117-to18 reduction. -/

namespace N12Compact.Remaining117

open S12 S12Completion

/-- Every original classified ID, rather than only the final eighteen. -/
def allIds : Finset Nat := expectedIds.toFinset

/-- A registry entry contains the full retained-row exclusion proof. -/
structure ProvenCase where
  id : Nat
  exclusion : ExcludesCase id

/-- Only actual proof entries remove cases from the remaining work.
The intersection also excludes irrelevant IDs outside the original list. -/
def knownIds (proofs : List ProvenCase) : Finset Nat :=
  allIds ∩ (proofs.map ProvenCase.id).toFinset

def remainingIds (proofs : List ProvenCase) : Finset Nat :=
  allIds \ knownIds proofs

/-- Proposed future bindings: fifteen shared four-square applications and
C898. This list never changes the actual backlog without proof entries. -/
def candidateIds : Finset Nat :=
  {28,78,537,556,565,567,569,570,575,576,577,585,898,1085,1086,1087}

theorem allIds_card : allIds.card = 117 := by decide +kernel

theorem candidateIds_card : candidateIds.card = 16 := by decide +kernel

theorem candidateIds_subset : candidateIds ⊆ allIds := by decide +kernel

/-- Finite conditional accounting only; no candidate proof is asserted. -/
theorem after_candidates_card : (allIds \ candidateIds).card = 101 := by decide +kernel

theorem knownIds_subset (proofs : List ProvenCase) : knownIds proofs ⊆ allIds := by
  intro id hi
  exact (Finset.mem_inter.mp hi).1

theorem complete_partition (proofs : List ProvenCase) :
    knownIds proofs ∪ remainingIds proofs = allIds := by
  ext id
  simp only [Finset.mem_union,remainingIds,Finset.mem_sdiff]
  constructor
  · rintro (h | h)
    · exact knownIds_subset proofs h
    · exact h.1
  · intro h
    by_cases hk : id ∈ knownIds proofs
    · exact Or.inl hk
    · exact Or.inr ⟨h,hk⟩

theorem partition_disjoint (proofs : List ProvenCase) :
    Disjoint (knownIds proofs) (remainingIds proofs) := by
  apply Finset.disjoint_left.mpr
  intro id hk hr
  exact (Finset.mem_sdiff.mp hr).2 hk

/-- No proof entries means no completed case is silently assumed. -/
theorem empty_remaining : remainingIds [] = allIds := by
  simp [remainingIds,knownIds]

theorem known_exclusions (proofs : List ProvenCase) (id : Nat)
    (hi : id ∈ knownIds proofs) : ExcludesCase id := by
  have hm : id ∈ proofs.map ProvenCase.id :=
    List.mem_toFinset.mp (Finset.mem_inter.mp hi).2
  obtain ⟨entry,_,he⟩ := List.mem_map.mp hm
  exact he ▸ entry.exclusion

/-- Each pending field is the full original case obligation. -/
def Remaining (proofs : List ProvenCase) : Prop :=
  ∀ id ∈ remainingIds proofs, ExcludesCase id

theorem all_exclusions (proofs : List ProvenCase)
    (remainingExclusions : Remaining proofs) : ∀ id ∈ allIds, ExcludesCase id := by
  intro id hi
  by_cases hk : id ∈ knownIds proofs
  · exact known_exclusions proofs id hk
  · exact remainingExclusions id (Finset.mem_sdiff.mpr ⟨hi,hk⟩)

theorem retained_exclusions (proofs : List ProvenCase)
    (remainingExclusions : Remaining proofs) :
    ∀ r ∈ retainedRows, ExcludesFamily r.groups := by
  intro r hr
  have hExpected : r.originalId ∈ expectedIds :=
    of_decide_eq_true (List.mem_filter.mp hr).2
  have hi : r.originalId ∈ allIds := List.mem_toFinset.mpr hExpected
  exact all_exclusions proofs remainingExclusions r.originalId hi r hr rfl

/-- Conditional global assembly from actual registered proofs and every
remaining original case. This module supplies no pending exclusion. -/
theorem optimality (proofs : List ProvenCase)
    (remainingExclusions : Remaining proofs) : packingConstant12 = 4 := by
  apply packingConstant12_eq_four_of_exclusion
  intro p
  obtain ⟨t,_,r,hr,hf⟩ := packing_reduction_to_117 p
  exact retained_exclusions proofs remainingExclusions r hr (t.pullPacking p) hf

#print axioms complete_partition
#print axioms known_exclusions
#print axioms optimality
end N12Compact.Remaining117
