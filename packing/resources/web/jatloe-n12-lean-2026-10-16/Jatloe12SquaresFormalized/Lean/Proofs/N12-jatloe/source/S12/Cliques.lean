import Mathlib.Data.Finset.Card

namespace S12
variable {M : Type} [DecidableEq M]

def cliques (compatible : M → M → Prop) [DecidableRel compatible] : List M → List (Finset M)
  | [] => [∅]
  | i :: vs =>
    let rest := cliques compatible vs
    rest ++ (rest.filter fun g => decide (∀ j ∈ g, compatible i j)).map (insert i)

/-- Complete generation of compatible subsets, without enumerating subsets
that already contain an incompatible pair. -/
theorem cliques_complete (compatible : M → M → Prop) [DecidableRel compatible]
    (vs : List M) (g : Finset M) (hsub : ∀ i ∈ g, i ∈ vs)
    (hpair : ∀ i ∈ g, ∀ j ∈ g, compatible i j) : g ∈ cliques compatible vs := by
  induction vs generalizing g with
  | nil =>
    have hg : g = ∅ := Finset.eq_empty_iff_forall_notMem.mpr (by
      intro i hi; simpa using hsub i hi)
    simp [hg, cliques]
  | cons i vs ih =>
    by_cases hi : i ∈ g
    · have hs : ∀ j ∈ g.erase i, j ∈ vs := by
        intro j hj
        obtain ⟨hne, hg⟩ := Finset.mem_erase.mp hj
        have hh := hsub j hg
        simpa only [List.mem_cons, hne, false_or] using hh
      have hp : ∀ j ∈ g.erase i, ∀ k ∈ g.erase i, compatible j k := by
        intro j hj k hk
        exact hpair j (Finset.mem_of_mem_erase hj) k (Finset.mem_of_mem_erase hk)
      have hm := ih (g.erase i) hs hp
      rw [cliques]
      apply List.mem_append_right
      apply List.mem_map.mpr
      refine ⟨g.erase i, List.mem_filter.mpr ⟨hm, ?_⟩, Finset.insert_erase hi⟩
      apply decide_eq_true
      intro j hj
      exact hpair i hi j (Finset.mem_of_mem_erase hj)
    · have hs : ∀ j ∈ g, j ∈ vs := by
        intro j hj
        have hh := hsub j hj
        rcases List.mem_cons.mp hh with he | he
        · subst j; exact (hi hj).elim
        · exact he
      exact List.mem_append_left _ (ih g hs hpair)

#print axioms cliques_complete
end S12
