import Mathlib.Data.Finset.Card
import Lean.Elab.Tactic.Omega
import Mathlib.Tactic.Linarith

namespace ElevenSquare

/-- Pair a finite set by an involution. A weight that is never tied on a pair
selects exactly half of the set. -/
theorem card_weight_representatives {α : Type*} [DecidableEq α]
    (s : Finset α) (f : α → α) (w : α → ℕ)
    (hf : Function.Involutive f)
    (hs : ∀ a ∈ s, f a ∈ s)
    (hne : ∀ a ∈ s, w (f a) ≠ w a) :
    2 * (s.filter (fun a => w (f a) ≤ w a)).card = s.card := by
  have hcard : (s.filter (fun a => w (f a) ≤ w a)).card =
      (s.filter (fun a => ¬ w (f a) ≤ w a)).card := by
    apply Finset.card_bij (fun a _ => f a)
    · intro a ha
      rcases Finset.mem_filter.mp ha with ⟨ha, hw⟩
      apply Finset.mem_filter.mpr
      refine ⟨hs a ha, ?_⟩
      rw [hf]
      have hn := hne a ha
      omega
    · intro a _ b _ hab
      exact hf.injective hab
    · intro b hb
      rcases Finset.mem_filter.mp hb with ⟨hb, hw⟩
      refine ⟨f b, ?_, hf b⟩
      apply Finset.mem_filter.mpr
      refine ⟨hs b hb, ?_⟩
      rw [hf]
      omega
  have hsum := Finset.card_filter_add_card_filter_not
    (s := s) (fun a => w (f a) ≤ w a)
  omega

/-- Sixteen binary membership indicators with a palindromic binary weight
cannot have odd total cardinality eleven. Only small linear integer arithmetic
is used; this avoids enumerating all 4,368 subsets in the kernel. -/
theorem binary_weight_odd_no_tie
    (x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 x13 x14 x15 : ℕ)
    (h0 : x0 ≤ 1)
    (h1 : x1 ≤ 1)
    (h2 : x2 ≤ 1)
    (h3 : x3 ≤ 1)
    (h4 : x4 ≤ 1)
    (h5 : x5 ≤ 1)
    (h6 : x6 ≤ 1)
    (h7 : x7 ≤ 1)
    (h8 : x8 ≤ 1)
    (h9 : x9 ≤ 1)
    (h10 : x10 ≤ 1)
    (h11 : x11 ≤ 1)
    (h12 : x12 ≤ 1)
    (h13 : x13 ≤ 1)
    (h14 : x14 ≤ 1)
    (h15 : x15 ≤ 1)
    (hcount : x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9 + x10 + x11 + x12 + x13 + x14 + x15 = 11)
    (hweight :
      32768*x0 + 16384*x1 + 8192*x2 + 4096*x3 + 2048*x4 + 1024*x5 + 512*x6 + 256*x7 + 128*x8 + 64*x9 + 32*x10 + 16*x11 + 8*x12 + 4*x13 + 2*x14 + 1*x15 =
      1*x0 + 2*x1 + 4*x2 + 8*x3 + 16*x4 + 32*x5 + 64*x6 + 128*x7 + 256*x8 + 512*x9 + 1024*x10 + 2048*x11 + 4096*x12 + 8192*x13 + 16384*x14 + 32768*x15) : False := by
  have hp0 : x0 = x15 := by
    apply Nat.le_antisymm
    · by_contra h
      linarith
    · by_contra h
      linarith
  have hp1 : x1 = x14 := by
    apply Nat.le_antisymm
    · by_contra h
      linarith
    · by_contra h
      linarith
  have hp2 : x2 = x13 := by
    apply Nat.le_antisymm
    · by_contra h
      linarith
    · by_contra h
      linarith
  have hp3 : x3 = x12 := by
    apply Nat.le_antisymm
    · by_contra h
      linarith
    · by_contra h
      linarith
  have hp4 : x4 = x11 := by
    apply Nat.le_antisymm
    · by_contra h
      linarith
    · by_contra h
      linarith
  have hp5 : x5 = x10 := by
    apply Nat.le_antisymm
    · by_contra h
      linarith
    · by_contra h
      linarith
  have hp6 : x6 = x9 := by
    apply Nat.le_antisymm
    · by_contra h
      linarith
    · by_contra h
      linarith
  have hp7 : x7 = x8 := by
    apply Nat.le_antisymm
    · by_contra h
      linarith
    · by_contra h
      linarith
  clear hweight
  omega

end ElevenSquare
