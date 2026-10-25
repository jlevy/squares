import S12.RawData
import S12.TransformFacts
import Mathlib.Data.Finset.Max
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Data.List.Nodup

/-! Generic support transport for the original fold-based natural masks.
The no-carry binary encoding argument applies to every natural mask and
injective marker permutation, without candidate-specific decoding tables. -/
namespace S12.MaskEncoding
open S12
open scoped BigOperators
set_option Elab.async false

private theorem power_sum_lt (n : Nat) :
    (∑ i ∈ Finset.range n, 2^i) < 2^n := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [Finset.sum_range_succ, pow_succ]
    omega

private theorem sparse_power_sum_lt (s : Finset Nat) (n : Nat)
    (hs : ∀ i ∈ s, i < n) : (∑ i ∈ s, 2^i) < 2^n := by
  have sub : s ⊆ Finset.range n := fun i hi => Finset.mem_range.mpr (hs i hi)
  have bound : (∑ i ∈ s, 2^i) ≤ ∑ i ∈ Finset.range n, 2^i :=
    Finset.sum_le_sum_of_subset_of_nonneg sub (fun _ _ _ => Nat.zero_le _)
  exact bound.trans_lt (power_sum_lt n)

/-- No carries occur in a sum of pairwise distinct binary place values. -/
theorem testBit_sum_powers (s : Finset Nat) (k : Nat) :
    (∑ i ∈ s, 2^i).testBit k = decide (k ∈ s) := by
  refine Finset.induction_on_max s ?_ ?_
  · simp
  · intro a s hmax ih
    have ha : a ∉ s := fun h => (lt_irrefl a) (hmax a h)
    have hsmall := sparse_power_sum_lt s a hmax
    rw [Finset.sum_insert ha]
    by_cases hka : k < a
    · rw [Nat.testBit_two_pow_add_gt hka, ih]
      simp [ne_of_lt hka]
    · by_cases he : k = a
      · subst k
        rw [Nat.testBit_two_pow_add_eq, Nat.testBit_lt_two_pow hsmall]
        simp
      · have hak : a < k := lt_of_le_of_ne (Nat.le_of_not_gt hka) (Ne.symm he)
        have hsum : 2^a + (∑ i ∈ s, 2^i) < 2^(a+1) := by
          rw [pow_succ]
          omega
        have hpow : 2^(a+1) ≤ 2^k :=
          Nat.pow_le_pow_right (by decide) hak
        have hbit := Nat.testBit_lt_two_pow (hsum.trans_le hpow)
        have hks : k ∉ s := fun h => (lt_asymm hak) (hmax k h)
        simp [hbit, he, hks]

/-- Encoding a finite marker set by powers of two decodes to exactly it. -/
theorem support_encode (s : Finset Marker) :
    maskSupport (∑ i ∈ s, 2^i.val) = s := by
  have he : (∑ i ∈ s.image Fin.val, 2^i) = ∑ i ∈ s, 2^i.val := by
    apply Finset.sum_image
    intro i _ j _ h
    exact Fin.val_injective h
  ext i
  simp only [maskSupport, Finset.mem_filter, Finset.mem_univ, true_and]
  rw [← he, testBit_sum_powers]
  simp only [decide_eq_true_eq, Finset.mem_image]
  constructor
  · rintro ⟨a, ha, h⟩
    exact Fin.val_injective h ▸ ha
  · intro hi
    exact ⟨i, hi, rfl⟩

private theorem fold_add_toFinset {α : Type} [DecidableEq α]
    (xs : List α) (hn : xs.Nodup) (f : α → Nat) (start : Nat) :
    xs.foldl (fun acc i => acc + f i) start = start + ∑ i ∈ xs.toFinset, f i := by
  induction xs generalizing start with
  | nil => simp
  | cons i xs ih =>
    have h := List.nodup_cons.mp hn
    simp only [List.foldl_cons, List.toFinset_cons]
    rw [ih h.2, Finset.sum_insert (by simpa using h.1)]
    omega

private theorem selected_indices (m : Nat) :
    ((List.range 16).filter (fun i => m.testBit i)).toFinset =
      (maskSupport m).image Fin.val := by
  ext i
  simp only [List.mem_toFinset, List.mem_filter, List.mem_range, Finset.mem_image]
  constructor
  · intro hi
    refine ⟨⟨i,hi.1⟩,?_,rfl⟩
    simpa [maskSupport] using hi.2
  · rintro ⟨j,hj,rfl⟩
    exact ⟨j.isLt,by simpa [maskSupport] using hj⟩

/-- The original fold-based mask action is the finite-set binary encoding
of the permuted support; no candidate-specific arithmetic is needed. -/
theorem permuteMask_encode (σ : Marker → Marker)
    (hσ : Function.Injective σ) (m : Nat) :
    permuteMask ((List.finRange 16).map (fun i => (σ i).val)) m =
      ∑ i ∈ (maskSupport m).image σ, 2^i.val := by
  unfold permuteMask
  rw [fold_add_toFinset _ (List.Nodup.filter _ List.nodup_range) _ 0, zero_add,
    selected_indices]
  rw [Finset.sum_image (fun i _ j _ h => Fin.val_injective h)]
  rw [Finset.sum_image (fun i _ j _ h => hσ h)]
  apply Finset.sum_congr rfl
  intro i _
  congr 1
  simp

/-- Exact original support transport, valid for all natural masks. -/
theorem maskSupport_permuteMask (σ : Marker → Marker)
    (hσ : Function.Injective σ) (m : Nat) :
    maskSupport (permuteMask ((List.finRange 16).map (fun i => (σ i).val)) m) =
      (maskSupport m).image σ := by
  rw [permuteMask_encode σ hσ m, support_encode]

/-- Drop-in support component for `S12.mask_action_spec`. Candidate membership
can continue using the existing eight short sorted-mask permutation facts. -/
theorem transform_support (t : Transform) (m : Nat) :
    maskSupport (permuteMask ((List.finRange 16).map
      (fun i => (t.markerAction i).val)) m) = (maskSupport m).image t.markerAction :=
  maskSupport_permuteMask _ t.markerAction_injective m

#print axioms transform_support
end S12.MaskEncoding
