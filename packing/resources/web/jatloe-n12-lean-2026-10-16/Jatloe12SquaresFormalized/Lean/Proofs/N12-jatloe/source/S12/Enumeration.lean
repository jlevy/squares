import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Finset.Max

/-! A complete search over disjoint nonempty subsets. Candidate generation,
geometric pruning, and the target list are separate from this theorem. -/
namespace S12

variable {M G : Type} [LinearOrder M] [DecidableEq G]

def Admissible (candidates : List G) (support : G → Finset M)
    (available : Finset M) (chosen : Finset G) : Prop :=
  (∀ g ∈ chosen, g ∈ candidates ∧ (support g).Nonempty ∧ support g ⊆ available) ∧
  (∀ g ∈ chosen, ∀ h ∈ chosen, g ≠ h → Disjoint (support g) (support h))

theorem admissible_card_le (candidates : List G) (support : G → Finset M)
    (available : Finset M) (chosen : Finset G)
    (ha : Admissible candidates support available chosen) :
    chosen.card ≤ available.card := by
  let f : chosen → available := fun g =>
    ⟨(support g.val).min' (ha.1 g.val g.property).2.1,
      (ha.1 g.val g.property).2.2 (Finset.min'_mem _ _)⟩
  apply Finset.card_le_card_of_injective (f := f)
  intro g h heq
  apply Subtype.eq
  by_contra hne
  have hg : (f g).val ∈ support g.val := Finset.min'_mem _ (ha.1 g.val g.property).2.1
  have hh : (f h).val ∈ support h.val := Finset.min'_mem _ (ha.1 h.val h.property).2.1
  have he := congrArg Subtype.val heq
  rw [← he] at hh
  exact Finset.disjoint_left.mp (ha.2 g.val g.property h.val h.property hne) hg hh

def enumerate (candidates : List G) (support : G → Finset M) :
    Nat → Finset M → Nat → List (Finset G)
  | _, _, 0 => [∅]
  | 0, _, _ + 1 => []
  | fuel + 1, available, k + 1 =>
    if available.card < k + 1 then [] else
    if h : available.Nonempty then
      let i := available.min' h
      enumerate candidates support fuel (available.erase i) (k + 1) ++
        candidates.flatMap fun g =>
          if i ∈ support g ∧ support g ⊆ available then
            (enumerate candidates support fuel (available \ support g) k).map (insert g)
          else []
    else []

theorem enumerate_complete (candidates : List G) (support : G → Finset M)
    (fuel : Nat) (available : Finset M) (chosen : Finset G)
    (hfuel : available.card ≤ fuel)
    (ha : Admissible candidates support available chosen) :
    chosen ∈ enumerate candidates support fuel available chosen.card := by
  induction fuel generalizing available chosen with
  | zero =>
    have he : available = ∅ := Finset.card_eq_zero.mp (by omega)
    have hc : chosen = ∅ := by
      apply Finset.eq_empty_iff_forall_notMem.mpr
      intro g hg
      obtain ⟨i, hi⟩ := (ha.1 g hg).2.1
      have := (ha.1 g hg).2.2 hi
      simp [he] at this
    simp [hc, enumerate]
  | succ fuel ih =>
    by_cases hc : chosen = ∅
    · simp [hc, enumerate]
    have hn : chosen.Nonempty := Finset.nonempty_iff_ne_empty.mpr hc
    have hav : available.Nonempty := by
      obtain ⟨g, hg⟩ := hn
      obtain ⟨i, hi⟩ := (ha.1 g hg).2.1
      exact ⟨i, (ha.1 g hg).2.2 hi⟩
    obtain ⟨k, hk⟩ : ∃ k, chosen.card = k + 1 := by
      have := Finset.card_pos.mpr hn
      exact ⟨chosen.card - 1, by omega⟩
    rw [hk, enumerate, if_neg (by have := admissible_card_le candidates support available chosen ha; omega), dif_pos hav]
    let i := available.min' hav
    have hi : i ∈ available := by
      exact Finset.min'_mem _ _
    have herase : (available.erase i).card ≤ fuel := by
      rw [Finset.card_erase_of_mem hi]
      omega
    by_cases hex : ∃ g ∈ chosen, i ∈ support g
    · obtain ⟨g, hg, hig⟩ := hex
      apply List.mem_append_right
      apply List.mem_flatMap.mpr
      refine ⟨g, (ha.1 g hg).1, ?_⟩
      rw [if_pos ⟨hig, (ha.1 g hg).2.2⟩]
      have hs : available \ support g ⊆ available.erase i := by
        intro j hj
        obtain ⟨hja, hjg⟩ := Finset.mem_sdiff.mp hj
        exact Finset.mem_erase.mpr ⟨by intro h; subst j; exact hjg hig, hja⟩
      have hsub : Admissible candidates support (available \ support g) (chosen.erase g) := by
        constructor
        · intro h hh
          obtain ⟨hneq, hmem⟩ := Finset.mem_erase.mp hh
          refine ⟨(ha.1 h hmem).1, (ha.1 h hmem).2.1, ?_⟩
          intro j hj
          refine Finset.mem_sdiff.mpr ⟨(ha.1 h hmem).2.2 hj, ?_⟩
          intro hjg
          exact Finset.disjoint_left.mp (ha.2 h hmem g hg hneq) hj hjg
        · intro x hx y hy hne
          exact ha.2 x (Finset.mem_of_mem_erase hx) y (Finset.mem_of_mem_erase hy) hne
      have ht := ih (available \ support g) (chosen.erase g)
        (le_trans (Finset.card_le_card hs) herase) hsub
      have hcard : (chosen.erase g).card = k := by
        rw [Finset.card_erase_of_mem hg, hk]; omega
      rw [hcard] at ht
      apply List.mem_map.mpr
      exact ⟨chosen.erase g, ht, Finset.insert_erase hg⟩
    · apply List.mem_append_left
      have ha' : Admissible candidates support (available.erase i) chosen := by
        constructor
        · intro g hg
          refine ⟨(ha.1 g hg).1, (ha.1 g hg).2.1, ?_⟩
          intro j hj
          refine Finset.mem_erase.mpr ⟨?_, (ha.1 g hg).2.2 hj⟩
          intro h; subst j
          exact hex ⟨g, hg, hj⟩
        · exact ha.2
      have ht := ih (available.erase i) chosen herase ha'
      simpa [hk] using ht

#print axioms enumerate_complete
end S12
