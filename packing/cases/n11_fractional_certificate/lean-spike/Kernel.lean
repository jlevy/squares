import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Data.Rat.BigOperators
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum

namespace FractionalSpike

/-!
The finite counting kernel behind a fractional unavoidable-set certificate.
`owner a = some i` means that atom `a` lies in the shrunken square assigned to
packed square `i`.  Pairwise disjointness of those shrunken squares is encoded by
the fact that `owner` is a function.
-/

variable {ι α : Type*} [Fintype ι] [DecidableEq ι] [Fintype α]

def assignedMass (w : α → ℚ) (owner : α → Option ι) (i : ι) : ℚ :=
  ∑ a, if owner a = some i then w a else 0

theorem sum_assignedMass_le_total
    (w : α → ℚ) (owner : α → Option ι) (hw : ∀ a, 0 ≤ w a) :
    ∑ i, assignedMass w owner i ≤ ∑ a, w a := by
  unfold assignedMass
  rw [Finset.sum_comm]
  apply Finset.sum_le_sum
  intro a _
  cases h : owner a with
  | none => simp [hw a]
  | some j => simp

theorem finite_nonnegative_counting_contradiction
    (w : α → ℚ) (owner : α → Option ι)
    (hw : ∀ a, 0 ≤ w a)
    (hone : ∀ i, 1 ≤ assignedMass w owner i)
    (htotal : ∑ a, w a < Fintype.card ι) : False := by
  have hlower : (Fintype.card ι : ℚ) ≤ ∑ i, assignedMass w owner i := by
    calc
      (Fintype.card ι : ℚ) = ∑ _ : ι, (1 : ℚ) := by simp
      _ ≤ ∑ i, assignedMass w owner i := Finset.sum_le_sum fun i _ ↦ hone i
  have hupper := sum_assignedMass_le_total w owner hw
  exact (not_lt_of_ge (hlower.trans hupper)) htotal

/-!
The same kernel stated with actual sets.  `huniq` is exactly what follows when
the inner squares lie in pairwise-disjoint interiors.
-/

noncomputable def mass {X : Type*} (w : α → ℚ) (site : α → X) (S : Set X) : ℚ := by
  classical
  exact ∑ a, if site a ∈ S then w a else 0

theorem mass_image_eq_of_permutation {X : Type*}
    (w : α → ℚ) (site : α → X) (σ : Equiv.Perm α) (r : X → X)
    (hr : Function.Involutive r)
    (hsite : ∀ a, site (σ a) = r (site a))
    (hweight : ∀ a, w (σ a) = w a) (S : Set X) :
    mass w site (r '' S) = mass w site S := by
  classical
  have himage : ∀ a, r (site a) ∈ r '' S ↔ site a ∈ S := by
    intro a
    constructor
    · rintro ⟨x, hx, hxa⟩
      simpa [(Function.Involutive.injective hr hxa).symm] using hx
    · intro ha
      exact ⟨site a, ha, rfl⟩
  unfold mass
  calc
    (∑ a, if site a ∈ r '' S then w a else 0) =
        ∑ a, if site (σ a) ∈ r '' S then w (σ a) else 0 :=
      (Equiv.sum_comp σ fun a ↦ if site a ∈ r '' S then w a else 0).symm
    _ = ∑ a, if site a ∈ S then w a else 0 := by
      apply Finset.sum_congr rfl
      intro a _
      rw [hsite, hweight, if_congr (himage a) rfl rfl]

noncomputable def ownerOf {X : Type*} (site : α → X) (P : ι → Set X) :
    α → Option ι := by
  classical
  exact fun a ↦ if h : ∃ i, site a ∈ P i then some (Classical.choose h) else none

omit [DecidableEq ι] [Fintype α] in
theorem ownerOf_eq_some_iff {X : Type*} (site : α → X) (P : ι → Set X)
    (huniq : ∀ a i j, site a ∈ P i → site a ∈ P j → i = j) (a : α) (i : ι) :
    ownerOf site P a = some i ↔ site a ∈ P i := by
  classical
  unfold ownerOf
  by_cases h : ∃ j, site a ∈ P j
  · simp only [h, ↓reduceDIte, Option.some.injEq]
    constructor
    · intro chosen_eq
      simpa [chosen_eq] using Classical.choose_spec h
    · intro hai
      exact huniq a _ i (Classical.choose_spec h) hai
  · simp only [h, ↓reduceDIte]
    constructor
    · intro impossible
      contradiction
    · intro hai
      exact (h ⟨i, hai⟩).elim

omit [DecidableEq ι] in
theorem finite_nonnegative_mass_bound {X : Type*}
    (w : α → ℚ) (site : α → X) (P : ι → Set X)
    (hw : ∀ a, 0 ≤ w a)
    (huniq : ∀ a i j, site a ∈ P i → site a ∈ P j → i = j)
    (hone : ∀ i, 1 ≤ mass w site (P i)) :
    (Fintype.card ι : ℚ) ≤ ∑ a, w a := by
  classical
  let owner := ownerOf site P
  have hmasses : ∀ i, assignedMass w owner i = mass w site (P i) := by
    intro i
    unfold assignedMass mass
    apply Finset.sum_congr rfl
    intro a _
    rw [if_congr (ownerOf_eq_some_iff site P huniq a i) rfl rfl]
  calc
    (Fintype.card ι : ℚ) = ∑ _ : ι, (1 : ℚ) := by simp
    _ ≤ ∑ i, assignedMass w owner i := by
      apply Finset.sum_le_sum
      intro i _
      simpa [hmasses i] using hone i
    _ ≤ ∑ a, w a := sum_assignedMass_le_total w owner hw

/-! The exact scalar checks for the retained `n = 11` certificate. -/

theorem n11_total_mass : (43391 : ℚ) / 4000 < 11 := by norm_num

theorem n11_net_reaches_pi_over_four :
    let t : ℚ := 207107 / 500000
    0 ≤ t ^ 2 + 2 * t - 1 := by
  norm_num

theorem n11_shrink_margin :
    let B : ℚ := 9977 / 10000
    let D : ℚ := 207107 / 90000000
    B * (1 + D) < 1 := by
  norm_num

/-!
This is the algebraic heart of the support-function step.  Once the angle lemma
has supplied `c ≤ 1` and `s ≤ D`, the strict containment margin is immediate.
-/

theorem support_radius_lt_one
    {B c s D : ℝ} (hB : 0 ≤ B) (hc : c ≤ 1) (hs : s ≤ D)
    (hshrink : B * (1 + D) < 1) : B * (c + s) < 1 := by
  exact lt_of_le_of_lt (mul_le_mul_of_nonneg_left (add_le_add hc hs) hB) hshrink

end FractionalSpike
