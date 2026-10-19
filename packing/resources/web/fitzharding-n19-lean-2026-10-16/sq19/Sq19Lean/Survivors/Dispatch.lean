import Sq19Lean.Survivors.All

/-! The four branch-tree exclusions in the census mask/subfamily interface.
The assignment may have any owner order or additional squares. Both the direct
representative and all eight square symmetries are covered. No new native check
is needed: the four 19-entry roster facts below are reduced by the kernel. -/
namespace Sq19.Survivors
open Sq19.Census

/-- The representative masks excluded by the four checked branch trees. -/
def treeMasks : List ℕ := [0x00f7fff, 0x00ff7ff, 0x103ffff, 0x10ffff6]

/-- This predicate can be supplied directly to `Assembly.survivor_of_packing`. -/
def TreeExcluded (m : ℕ) : Prop := m ∈ treeMasks

private theorem excluded_image_of_roster {k n : ℕ} (m : ℕ)
    (roster : Fin k → Fin 25) (hinj : Function.Injective roster)
    (hfree : ¬ Packs roster) (hbits : ∀ i, m.testBit (roster i) = true)
    (g : Fin 8) (assign : Fin n → Fin 25)
    (hsub : ∀ c : Fin 25, m.testBit c = true → ∃ j, assign j = perm g c) :
    ¬ Packs assign :=
  not_packs_of_sub assign (fun i => perm g (roster i))
    ((perm_injective g).comp hinj) (not_packs_perm roster hfree g)
    (fun i => hsub (roster i) (hbits i))

/-- Every symmetry image of a tree mask excludes every family containing its cells. -/
theorem tree_excluded_perm (m : ℕ) (hm : TreeExcluded m) (g : Fin 8)
    {n : ℕ} (assign : Fin n → Fin 25)
    (hsub : ∀ c : Fin 25, m.testBit c = true → ∃ j, assign j = perm g c) :
    ¬ Packs assign := by
  simp only [TreeExcluded, treeMasks, List.mem_cons, List.not_mem_nil, or_false] at hm
  rcases hm with rfl | rfl | rfl | rfl
  · exact excluded_image_of_roster _ O1.roster (by decide) orbit1_free (by decide) g assign hsub
  · exact excluded_image_of_roster _ O2.roster (by decide) orbit2_free (by decide) g assign hsub
  · exact excluded_image_of_roster _ O5423.roster (by decide) orbit5423_free (by decide) g assign hsub
  · exact excluded_image_of_roster _ O5453.roster (by decide) orbit5453_free (by decide) g assign hsub

private theorem perm_zero : ∀ c : Fin 25, perm 0 c = c := by decide

/-- Exactly the exclusion-dispatch type required by `Assembly.survivor_of_packing`. -/
theorem tree_excluded (m : ℕ) (hm : TreeExcluded m)
    {n : ℕ} (assign : Fin n → Fin 25)
    (hsub : ∀ c : Fin 25, m.testBit c = true → ∃ j, assign j = c) :
    ¬ Packs assign :=
  tree_excluded_perm m hm 0 assign (fun c hc => by simpa only [perm_zero] using hsub c hc)

/-- A census assignment which actually packs cannot have any of the four tree masks. -/
theorem not_tree_excluded_of_packs {n : ℕ} (assign : Fin n → Fin 25)
    (hp : Packs assign) (m : ℕ)
    (hsub : ∀ c : Fin 25, m.testBit c = true → ∃ j, assign j = c) :
    ¬ TreeExcluded m := fun hm => tree_excluded m hm assign hsub hp

/-- Add all four trees to any existing census exclusion dispatcher, without changing its API. -/
theorem excluded_with_trees (Excluded : ℕ → Prop)
    (hexcl : ∀ m, Excluded m → ∀ {n : ℕ} (assign : Fin n → Fin 25),
      (∀ c : Fin 25, m.testBit c = true → ∃ j, assign j = c) → ¬ Packs assign)
    (m : ℕ) (hm : Excluded m ∨ TreeExcluded m)
    {n : ℕ} (assign : Fin n → Fin 25)
    (hsub : ∀ c : Fin 25, m.testBit c = true → ∃ j, assign j = c) :
    ¬ Packs assign :=
  hm.elim (fun h => hexcl m h assign hsub) (fun h => tree_excluded m h assign hsub)

end Sq19.Survivors

#print axioms Sq19.Survivors.tree_excluded_perm
#print axioms Sq19.Survivors.tree_excluded
#print axioms Sq19.Survivors.excluded_with_trees
