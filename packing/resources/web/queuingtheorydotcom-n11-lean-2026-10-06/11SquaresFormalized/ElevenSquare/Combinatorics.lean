import Mathlib.Data.Finset.Powerset
import Mathlib.Data.Fintype.Fin
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Algebra.BigOperators.Fin
import ElevenSquare.CaseCountSupport

/-! Finite reduction to the 2184 half-turn classes of eleven occupied cells.
The numerical case IDs of the Python archive are a separate data interface
in step 6; these definitions describe the underlying mathematical masks.
-/
namespace ElevenSquare

abbrev CellMask := Finset (Fin 16)

def halfTurnMask (m : CellMask) : CellMask := m.image Fin.rev

theorem halfTurnMask_twice (m : CellMask) : halfTurnMask (halfTurnMask m) = m := by
  ext i
  simp [halfTurnMask, Finset.mem_image, Fin.rev_inj]

theorem halfTurnMask_card (m : CellMask) : (halfTurnMask m).card = m.card := by
  apply Finset.card_image_of_injective
  intro a b h
  exact Fin.rev_inj.mp h

def rawMasks : Finset CellMask := (Finset.univ : CellMask).powersetCard 11

theorem mem_rawMasks (m : CellMask) : m ∈ rawMasks ↔ m.card = 11 := by
  simp [rawMasks]

theorem rawMasks_card : rawMasks.card = 4368 := by
  rw [rawMasks, Finset.card_powersetCard]
  norm_num
  decide

/-- Higher bits represent earlier cell indices, so taking the greater weight
chooses the lexicographically earlier increasing eleven-tuple. -/
def maskWeight (m : CellMask) : ℕ := ∑ i ∈ m, 2 ^ (15 - i.val)

def canonicalMasks : Finset CellMask :=
  rawMasks.filter (fun m => maskWeight (halfTurnMask m) ≤ maskWeight m)

theorem mem_canonicalMasks (m : CellMask) : m ∈ canonicalMasks ↔
    m.card = 11 ∧ maskWeight (halfTurnMask m) ≤ maskWeight m := by
  simp [canonicalMasks, mem_rawMasks]

theorem mask_or_halfTurn_canonical (m : CellMask) (hm : m.card = 11) :
    m ∈ canonicalMasks ∨ halfTurnMask m ∈ canonicalMasks := by
  by_cases h : maskWeight (halfTurnMask m) ≤ maskWeight m
  · exact Or.inl ((mem_canonicalMasks m).2 ⟨hm, h⟩)
  · apply Or.inr
    apply (mem_canonicalMasks _).2
    rw [halfTurnMask_card, halfTurnMask_twice]
    exact ⟨hm, (lt_of_not_ge h).le⟩

private theorem sum_indicator (m : CellMask) (f : Fin 16 → ℕ) :
    (∑ i ∈ m, f i) = ∑ i : Fin 16, f i * (if i ∈ m then 1 else 0) := by
  simp_rw [mul_ite, mul_one, mul_zero]
  rw [← Finset.sum_filter]
  congr 1
  ext i
  simp

private theorem reversed_weight (m : CellMask) :
    maskWeight (halfTurnMask m) = ∑ i ∈ m, 2 ^ i.val := by
  unfold maskWeight halfTurnMask
  rw [Finset.sum_image]
  · apply Finset.sum_congr rfl
    intro i _
    congr 1
    rw [Fin.val_rev]
    omega
  · intro a _ b _ h
    exact Fin.rev_inj.mp h

set_option maxHeartbeats 1000000 in
/-- An odd eleven-cell mask cannot tie its reversed binary weight. -/
theorem maskWeight_halfTurn_ne (m : CellMask) (hm : m.card = 11) :
    maskWeight (halfTurnMask m) ≠ maskWeight m := by
  intro h
  have hw := h.symm
  rw [reversed_weight, maskWeight,
    sum_indicator m (fun i => 2 ^ (15 - i.val)),
    sum_indicator m (fun i => 2 ^ i.val)] at hw
  have hc : (∑ i : Fin 16, if i ∈ m then (1 : ℕ) else 0) = 11 := by
    have hh := sum_indicator m (fun _ => 1)
    simp only [Finset.sum_const, smul_eq_mul, mul_one, one_mul] at hh
    exact hh.symm.trans hm
  have hb (i : Fin 16) : (if i ∈ m then (1 : ℕ) else 0) ≤ 1 := by
    split_ifs <;> decide
  simp only [Fin.sum_univ_succ, Fin.sum_univ_zero, add_zero] at hc hw
  norm_num [Fin.succ] at hc hw
  apply binary_weight_odd_no_tie
    (if (0 : Fin 16) ∈ m then 1 else 0) (if (1 : Fin 16) ∈ m then 1 else 0) (if (2 : Fin 16) ∈ m then 1 else 0) (if (3 : Fin 16) ∈ m then 1 else 0) (if (4 : Fin 16) ∈ m then 1 else 0) (if (5 : Fin 16) ∈ m then 1 else 0) (if (6 : Fin 16) ∈ m then 1 else 0) (if (7 : Fin 16) ∈ m then 1 else 0) (if (8 : Fin 16) ∈ m then 1 else 0) (if (9 : Fin 16) ∈ m then 1 else 0) (if (10 : Fin 16) ∈ m then 1 else 0) (if (11 : Fin 16) ∈ m then 1 else 0) (if (12 : Fin 16) ∈ m then 1 else 0) (if (13 : Fin 16) ∈ m then 1 else 0) (if (14 : Fin 16) ∈ m then 1 else 0) (if (15 : Fin 16) ∈ m then 1 else 0)
    (hb 0) (hb 1) (hb 2) (hb 3) (hb 4) (hb 5) (hb 6) (hb 7) (hb 8) (hb 9) (hb 10) (hb 11) (hb 12) (hb 13) (hb 14) (hb 15)
  · simpa only [add_assoc] using hc
  · simpa only [add_assoc, one_mul, mul_ite, mul_one, mul_zero] using hw

set_option maxRecDepth 10000 in
theorem canonicalMasks_card : canonicalMasks.card = 2184 := by
  have h := card_weight_representatives rawMasks halfTurnMask maskWeight
    halfTurnMask_twice
    (by intro m hm; simpa only [mem_rawMasks, halfTurnMask_card] using hm)
    (by intro m hm; exact maskWeight_halfTurn_ne m ((mem_rawMasks m).mp hm))
  rw [rawMasks_card] at h
  have half : ∀ n : ℕ, 2*n = 4368 → n = 2184 := by
    intro n hn
    omega
  dsimp only [canonicalMasks]
  exact half _ h

end ElevenSquare
