import S12.LocalQueryData
import S12.Cliques

namespace S12
open S12Pilot
set_option maxRecDepth 100000
set_option maxHeartbeats 0

def queryArray : Array LocalQuery := localQueries.toArray
@[irreducible] def queryAt (i : Nat) : LocalQuery := queryArray[i]?.getD localQuery0

/-- Even an out-of-range lookup returns a certified query. Its mask, kind,
and complete owner set must still match before it can exclude anything. -/
theorem queryAt_checked (i : Nat) : (queryAt i).Check := by
  simp only [queryAt,queryArray,List.getElem?_toArray]
  cases h : localQueries[i]? with
  | none =>
    simp only [Option.getD_none]
    exact of_decide_eq_true (List.all_eq_true.mp queryChunk0_checked localQuery0
      (by simp [queryChunk0]))
  | some w =>
    simp only [Option.getD_some]
    exact localQueries_checked w (List.mem_of_getElem? h)

def allAuxSubsets : List (Finset Nat) := cliques (fun _ _ : Nat => True) (List.range 10)

theorem allAuxSubsets_complete (s : Finset Nat) (hs : s⊆Finset.range 10) : s∈allAuxSubsets := by
  apply cliques_complete
  · intro i hi
    exact List.mem_range.mpr (Finset.mem_range.mp (hs hi))
  · intros; trivial

def RefutationMatches (i m : Nat) (kind : Fin 3) (owned : Finset Nat) : Prop :=
  (queryAt i).mask=m ∧ (queryAt i).kind=kind ∧ (queryAt i).owned=owned
instance decidableRefutationMatches (i m : Nat) (kind : Fin 3) (owned : Finset Nat) :
    Decidable (RefutationMatches i m kind owned) := inferInstanceAs (Decidable (_ ∧ _))

theorem refutation_matches_sound (i m : Nat) (kind : Fin 3) (owned : Finset Nat)
    (he : RefutationMatches i m kind owned) (q : OpenSquare) (ha : 1<q.side)
    (hsize : q.side≤1001/1000) (hbox : InsideContainer q)
    (hm : ExactMarkers q (maskSupport m)) (ho : AuxExact q kind owned) : False :=
  (queryAt i).sound (queryAt_checked i) q ha hsize hbox
    (by simpa only [he.1] using hm) (by simpa only [he.2.1,he.2.2] using ho)

structure SingleSpec where
  mask : Nat
  kind : Fin 3
  lower : Nat
  upper : Nat
  allowed : List (Finset Nat)
  refutations : List Nat

def SingleSpec.Check (w : SingleSpec) : Prop :=
  w.kind.val<2 ∧ ∀ s∈allAuxSubsets, w.lower≤s.card → s.card≤w.upper →
    s∈w.allowed ∨ ∃ i∈w.refutations, RefutationMatches i w.mask w.kind s
instance SingleSpec.decidableCheck (w : SingleSpec) : Decidable w.Check :=
  inferInstanceAs (Decidable (_ ∧ _))

/-- Finite coverage of every subset in the size interval upgrades local
rejections to a necessary domain for a real square. -/
theorem SingleSpec.sound (w : SingleSpec) (hw : w.Check) (q : OpenSquare)
    (ha : 1<q.side) (hsize : q.side≤1001/1000) (hbox : InsideContainer q)
    (hm : ExactMarkers q (maskSupport w.mask)) (owned : Finset Nat)
    (ho : AuxExact q w.kind owned) (hsub : owned⊆Finset.range 10)
    (hlo : w.lower≤owned.card) (hhi : owned.card≤w.upper) : owned∈w.allowed := by
  rcases hw.2 owned (allAuxSubsets_complete owned hsub) hlo hhi with h | h
  · exact h
  · obtain ⟨i,_,he⟩ := h
    exact False.elim (refutation_matches_sound i _ _ _ he q ha hsize hbox hm ho)

def combinedOwners (x y : Finset Nat) : Finset Nat := x ∪ y.image (fun i => i+10)

structure CombinedSpec where
  mask : Nat
  first : {w : SingleSpec // w.Check}
  second : {w : SingleSpec // w.Check}
  allowed : List (Finset Nat)
  refutations : List Nat

def CombinedSpec.Check (w : CombinedSpec) : Prop :=
  w.first.val.mask=w.mask ∧ w.second.val.mask=w.mask ∧
  w.first.val.kind=0 ∧ w.second.val.kind=1 ∧
  ∀ x∈w.first.val.allowed, ∀ y∈w.second.val.allowed,
    combinedOwners x y∈w.allowed ∨
      ∃ i∈w.refutations, RefutationMatches i w.mask 2 (combinedOwners x y)
instance CombinedSpec.decidableCheck (w : CombinedSpec) : Decidable w.Check :=
  inferInstanceAs (Decidable (_ ∧ _))

theorem CombinedSpec.sound (w : CombinedSpec) (hw : w.Check) (q : OpenSquare)
    (ha : 1<q.side) (hsize : q.side≤1001/1000) (hbox : InsideContainer q)
    (hm : ExactMarkers q (maskSupport w.mask)) (x y : Finset Nat)
    (hx : x∈w.first.val.allowed) (hy : y∈w.second.val.allowed)
    (ho : AuxExact q 2 (combinedOwners x y)) : combinedOwners x y∈w.allowed := by
  rcases hw.2.2.2.2 x hx y hy with h | h
  · exact h
  · obtain ⟨i,_,he⟩ := h
    exact False.elim (refutation_matches_sound i _ _ _ he q ha hsize hbox hm ho)

#print axioms SingleSpec.sound
#print axioms CombinedSpec.sound
end S12
