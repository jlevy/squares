import S12.Enumeration
import Mathlib.Data.Fintype.Card
import Mathlib.Order.Fin.Basic

namespace S12
set_option Elab.async false

/- The arithmetic solver sees only scalar bounds, not the ownership predicates
or the finite sets from which those bounds were derived. -/
private theorem pair_budget_arithmetic (e : Nat) (he : e ≤ 12)
    (h : 12-e ≤ 10) : 2 ≤ e := by omega

private theorem exempt_budget_arithmetic (e n : Nat)
    (he : e ≤ 12) (hp : 2 ≤ e) (hn : n ≤ 10)
    (h : 12-e ≤ 10-n) : n ≤ e-2 := by omega

private theorem forced_budget_arithmetic (e n : Nat)
    (he : e ≤ 12) (hp : 2 ≤ e) (hn : n ≤ 10)
    (h : 12-e-1 ≤ 10-n) : n ≤ e-2+1 := by omega

/-- Twelve disjoint owners of ten points: at least two owners must be exempt
from the rule that each owns a point. This does not assume the geometric F/G
rule; that rule supplies `hforced` when the theorem is applied. -/
theorem pair_budget (owners : Fin 12 → Finset (Fin 10)) (exempt : Finset (Fin 12))
    (hdis : ∀ i j, i ≠ j → Disjoint (owners i) (owners j))
    (hforced : ∀ i, i ∉ exempt → (owners i).Nonempty) :
    2 ≤ exempt.card := by
  let chosen := Finset.univ \ exempt
  have ha : Admissible (List.finRange 12) owners Finset.univ chosen := by
    constructor
    · intro i hi
      refine ⟨by simp, hforced i (Finset.mem_sdiff.mp hi).2, Finset.subset_univ _⟩
    · intro i hi j hj hne; exact hdis i j hne
  have h := admissible_card_le _ _ _ _ ha
  have he : exempt.card ≤ 12 := by
    exact le_trans (Finset.card_le_card (Finset.subset_univ exempt)) (by simp)
  have hc : chosen.card = 12 - exempt.card := by
    dsimp [chosen]
    rw [Finset.card_sdiff_of_subset (Finset.subset_univ _)]
    rfl
  rw [hc] at h
  have hh : (Finset.univ : Finset (Fin 10)).card = 10 := Finset.card_fin 10
  rw [hh] at h
  exact pair_budget_arithmetic exempt.card he h

/-- The upper bound used in the F/G domain enumeration: an exempt owner gets
at most e-2 points; any other owner gets at most e-1. -/
theorem individual_budget (owners : Fin 12 → Finset (Fin 10)) (exempt : Finset (Fin 12))
    (hdis : ∀ i j, i ≠ j → Disjoint (owners i) (owners j))
    (hforced : ∀ i, i ∉ exempt → (owners i).Nonempty) (j : Fin 12) :
    (owners j).card ≤ exempt.card - 2 + (if j ∈ exempt then 0 else 1) := by
  let chosen := (Finset.univ \ exempt).erase j
  have ha : Admissible (List.finRange 12) owners (Finset.univ \ owners j) chosen := by
    constructor
    · intro i hi
      obtain ⟨hne, hi'⟩ := Finset.mem_erase.mp hi
      refine ⟨by simp, hforced i (Finset.mem_sdiff.mp hi').2, ?_⟩
      intro p hp
      exact Finset.mem_sdiff.mpr ⟨Finset.mem_univ _, fun hj =>
        Finset.disjoint_left.mp (hdis i j hne) hp hj⟩
    · intro i hi k hk hne; exact hdis i k hne
  have h := admissible_card_le _ _ _ _ ha
  have he : exempt.card ≤ 12 := le_trans
    (Finset.card_le_card (Finset.subset_univ exempt)) (by simp)
  have ho : (owners j).card ≤ 10 := le_trans
    (Finset.card_le_card (Finset.subset_univ (owners j))) (by simp)
  have hp := pair_budget owners exempt hdis hforced
  have hc : (Finset.univ \ exempt).card = 12 - exempt.card := by
    rw [Finset.card_sdiff_of_subset (Finset.subset_univ _)]
    rfl
  have hr : (Finset.univ \ owners j).card = 10 - (owners j).card := by
    rw [Finset.card_sdiff_of_subset (Finset.subset_univ _)]
    rfl
  rw [hr] at h
  by_cases hj : j ∈ exempt
  · have hn : j ∉ Finset.univ \ exempt := by simp [hj]
    have hh : chosen.card = 12 - exempt.card := by
      dsimp [chosen]; rw [Finset.erase_eq_of_notMem hn, hc]
    rw [hh] at h
    simpa only [ite_eq_left hj, Nat.add_zero] using
      exempt_budget_arithmetic exempt.card (owners j).card he hp ho h
  · have hm : j ∈ Finset.univ \ exempt := by simp [hj]
    have hh : chosen.card = 12 - exempt.card - 1 := by
      dsimp [chosen]; rw [Finset.card_erase_of_mem hm, hc]
    rw [hh] at h
    simpa only [ite_eq_right hj] using
      forced_budget_arithmetic exempt.card (owners j).card he hp ho h

#print axioms pair_budget
#print axioms individual_budget
end S12
