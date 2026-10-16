import Sq19Lean.Endgame.HullData

/-!
# Separations on the hull box H (LOCAL_THEOREM.md, Lean pieces 1 and 6)

`prob` is the hull box H for squares 1, 2, 5, 7, 8, 10 (record angle 0) and 11, 13, 14 (record angle
45 deg), generated from `s19/data/capture/coarse/hull2_box.txt` around the pose
`s19/data/capture/poses/state3435.txt` (boxes widened by 4e-4 and 2e-3 deg as in feature_check.c).
List positions: 0 ↦ 1, 1 ↦ 2, 2 ↦ 5, 3 ↦ 7, 4 ↦ 8, 5 ↦ 10, 6 ↦ 11, 7 ↦ 13, 8 ↦ 14.

`hull_pairs`: the pairs near enough to touch, and for each the faces that the interval face test
(`facePossible`, proved sound) cannot exclude on H. With `exists_optSep` this gives, for every
packing in H, a separating face from the listed ones. Face `k` of a square at angle `φ` has normal
`(cos (φ + kπ/2), sin (φ + kπ/2))`: `k = 0, 1, 2, 3` is `+e1, +e2, -e1, -e2`.

In particular (F2 empty) square 13's face `-e2` cannot separate 8: only 8's top face `+e2` does.
-/
namespace Sq19.Endgame
open Sq19.Milp Sq19.Endgame.Hull

/-- The near pairs of H with their possible faces `(owner is the second square?, k)`. -/
def hullPairs : List Pair := [
  ⟨0, 1, [⟨false, 0⟩, ⟨true, 2⟩]⟩,
  ⟨1, 8, [⟨true, 1⟩]⟩,
  ⟨2, 3, [⟨false, 0⟩, ⟨false, 1⟩, ⟨true, 2⟩, ⟨true, 3⟩]⟩,
  ⟨2, 4, [⟨false, 1⟩, ⟨true, 3⟩]⟩,
  ⟨3, 4, [⟨false, 2⟩, ⟨true, 0⟩]⟩,
  ⟨4, 7, [⟨false, 1⟩]⟩,
  ⟨5, 6, [⟨true, 0⟩]⟩,
  ⟨6, 7, [⟨false, 2⟩, ⟨true, 0⟩]⟩,
  ⟨6, 8, [⟨false, 1⟩, ⟨false, 2⟩, ⟨true, 0⟩, ⟨true, 3⟩]⟩,
  ⟨7, 8, [⟨false, 1⟩, ⟨true, 3⟩]⟩]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
theorem hull_pairs : prob.pairs = hullPairs := by decide +kernel

section
variable {θ dx dy : ℕ → ℝ} {L : ℝ}

/-- Centre and angle of the square at list position `i`. -/
noncomputable abbrev cH (dx dy : ℕ → ℝ) (i : ℕ) : ℝ × ℝ := cenOf dx dy (prob.sq i)
noncomputable abbrev φH (θ : ℕ → ℝ) (i : ℕ) : ℝ := angOf θ (prob.sq i)

theorem sep_of_pair (hg : Good prob θ dx dy L) {pr : Pair} (h : pr ∈ hullPairs) :
    ∃ o ∈ pr.opts, OptSep prob θ dx dy pr o := by
  rw [← hull_pairs] at h; exact exists_optSep hg h

/-- Pair `(i, j)` of `hullPairs` with option list `os`: one of the listed faces separates. -/
private theorem sep_list (hg : Good prob θ dx dy L) {i j : ℕ} {os : List Opt}
    (h : (⟨i, j, os⟩ : Pair) ∈ hullPairs) :
    ∃ o ∈ os, (if o.own then Sep (cH dx dy j) (φH θ j) (cH dx dy i) (φH θ i) o.k
      else Sep (cH dx dy i) (φH θ i) (cH dx dy j) (φH θ j) o.k) := by
  obtain ⟨o, ho, hs⟩ := sep_of_pair hg h
  refine ⟨o, ho, ?_⟩
  unfold OptSep optSqs at hs
  cases hown : o.own <;> simp only [hown, if_true, if_false, Bool.false_eq_true] at hs ⊢ <;> exact hs

/-- 1-2: 1's face `+e1` or 2's face `-e1`. -/
theorem sep_1_2 (hg : Good prob θ dx dy L) :
    Sep (cH dx dy 0) (φH θ 0) (cH dx dy 1) (φH θ 1) 0 ∨ Sep (cH dx dy 1) (φH θ 1) (cH dx dy 0) (φH θ 0) 2 := by
  obtain ⟨o, ho, hs⟩ := sep_list hg (i := 0) (j := 1) (os := [⟨false, 0⟩, ⟨true, 2⟩]) (by simp [hullPairs])
  simp only [List.mem_cons, List.not_mem_nil, or_false] at ho
  rcases ho with rfl | rfl
  · exact Or.inl hs
  · exact Or.inr hs

/-- 2-14: 14's face `+e2`. -/
theorem sep_2_14 (hg : Good prob θ dx dy L) : Sep (cH dx dy 8) (φH θ 8) (cH dx dy 1) (φH θ 1) 1 := by
  obtain ⟨o, ho, hs⟩ := sep_list hg (i := 1) (j := 8) (os := [⟨true, 1⟩]) (by simp [hullPairs])
  simp only [List.mem_cons, List.not_mem_nil, or_false] at ho
  subst ho; exact hs

/-- 5-8: 5's face `+e2` or 8's face `-e2`. -/
theorem sep_5_8 (hg : Good prob θ dx dy L) :
    Sep (cH dx dy 2) (φH θ 2) (cH dx dy 4) (φH θ 4) 1 ∨ Sep (cH dx dy 4) (φH θ 4) (cH dx dy 2) (φH θ 2) 3 := by
  obtain ⟨o, ho, hs⟩ := sep_list hg (i := 2) (j := 4) (os := [⟨false, 1⟩, ⟨true, 3⟩]) (by simp [hullPairs])
  simp only [List.mem_cons, List.not_mem_nil, or_false] at ho
  rcases ho with rfl | rfl
  · exact Or.inl hs
  · exact Or.inr hs

/-- 7-8: 7's face `-e1` or 8's face `+e1`. -/
theorem sep_7_8 (hg : Good prob θ dx dy L) :
    Sep (cH dx dy 3) (φH θ 3) (cH dx dy 4) (φH θ 4) 2 ∨ Sep (cH dx dy 4) (φH θ 4) (cH dx dy 3) (φH θ 3) 0 := by
  obtain ⟨o, ho, hs⟩ := sep_list hg (i := 3) (j := 4) (os := [⟨false, 2⟩, ⟨true, 0⟩]) (by simp [hullPairs])
  simp only [List.mem_cons, List.not_mem_nil, or_false] at ho
  rcases ho with rfl | rfl
  · exact Or.inl hs
  · exact Or.inr hs

/-- 8-13 (F2 empty): only 8's face `+e2` separates. -/
theorem sep_8_13 (hg : Good prob θ dx dy L) : Sep (cH dx dy 4) (φH θ 4) (cH dx dy 7) (φH θ 7) 1 := by
  obtain ⟨o, ho, hs⟩ := sep_list hg (i := 4) (j := 7) (os := [⟨false, 1⟩]) (by simp [hullPairs])
  simp only [List.mem_cons, List.not_mem_nil, or_false] at ho
  subst ho; exact hs

/-- 10-11: 11's face `+e1`. -/
theorem sep_10_11 (hg : Good prob θ dx dy L) : Sep (cH dx dy 6) (φH θ 6) (cH dx dy 5) (φH θ 5) 0 := by
  obtain ⟨o, ho, hs⟩ := sep_list hg (i := 5) (j := 6) (os := [⟨true, 0⟩]) (by simp [hullPairs])
  simp only [List.mem_cons, List.not_mem_nil, or_false] at ho
  subst ho; exact hs

/-- 11-13 (Q): 11's face `-e1` or 13's face `+e1`. -/
theorem sep_11_13 (hg : Good prob θ dx dy L) :
    Sep (cH dx dy 6) (φH θ 6) (cH dx dy 7) (φH θ 7) 2 ∨ Sep (cH dx dy 7) (φH θ 7) (cH dx dy 6) (φH θ 6) 0 := by
  obtain ⟨o, ho, hs⟩ := sep_list hg (i := 6) (j := 7) (os := [⟨false, 2⟩, ⟨true, 0⟩]) (by simp [hullPairs])
  simp only [List.mem_cons, List.not_mem_nil, or_false] at ho
  rcases ho with rfl | rfl
  · exact Or.inl hs
  · exact Or.inr hs

/-- 13-14 (P): 13's face `+e2` or 14's face `-e2`. -/
theorem sep_13_14 (hg : Good prob θ dx dy L) :
    Sep (cH dx dy 7) (φH θ 7) (cH dx dy 8) (φH θ 8) 1 ∨ Sep (cH dx dy 8) (φH θ 8) (cH dx dy 7) (φH θ 7) 3 := by
  obtain ⟨o, ho, hs⟩ := sep_list hg (i := 7) (j := 8) (os := [⟨false, 1⟩, ⟨true, 3⟩]) (by simp [hullPairs])
  simp only [List.mem_cons, List.not_mem_nil, or_false] at ho
  rcases ho with rfl | rfl
  · exact Or.inl hs
  · exact Or.inr hs

end

end Sq19.Endgame

#print axioms Sq19.Endgame.hull_pairs
#print axioms Sq19.Endgame.sep_1_2
#print axioms Sq19.Endgame.sep_8_13
#print axioms Sq19.Endgame.sep_13_14
