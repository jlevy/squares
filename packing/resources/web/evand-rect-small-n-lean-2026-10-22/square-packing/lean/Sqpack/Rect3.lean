import Sqpack.RectChain

/-!
# Three unit squares in a rectangle

`rect3_lower`: if three unit squares (any angles) pack `[0,L] × [0,H]` with `H < 2`, then
`L ≥ 3` or `L + 2H ≥ 4 + 2√2`.  With the constructions this gives `R₃` exactly (`rect3_iff`).
The boundary (with the wedge) is the boundary of `S₂` in Friedman's Math Magic, June 2010, given there
by constructions; this file proves the lower bound.

The proof is a *chain* argument (tools in `RectChain.lean`), no case enumeration over separating axes:
1. Sort the squares by the x-coordinate of their centres: `a`, `b`, `c`.
2. `left_shelf a b`: every point of `b` at the heights of some band `[lo, lo + 1]` has `x ≥ 1` (the
   upright square at the left wall lies on `a`'s side of the separating line).  `right_shelf b c` is
   the mirror image.
3. `witnesses`: on each side, `b`'s side vertex or a point on an adjacent edge at the band's near end.
4. `chain_bound`: the resulting `3 × 3` real inequalities.  Equality: all squares upright (`L = 3`),
   or the wedge (`L + 2H = 4 + 2√2`, `b` at `45°`, cases `UU` and `DD`).
-/

namespace SquarePacking

/-! ## The final inequalities -/

/-- Core of the two wedge cases: `C S T ≥ C³ + S³ - G` gives `T ≥ 2√2 - 2G - C - S` (`s = √2`). -/
theorem wedge_core {C S s G T : ℝ} (hC0 : 0 < C) (hS0 : 0 < S) (hCS : C^2 + S^2 = 1)
    (hs : 0 < s) (hs2 : s^2 = 2) (hG : G < 1)
    (h : C ^ 3 + S ^ 3 - G ≤ C * S * T) : 2 * s - 2 * G - C - S ≤ T := by
  have hp : C + S ≤ s := by nlinarith [sq_nonneg (C - S), sq_nonneg (C + S - s)]
  have hq : 0 ≤ 1 - 2 * (C * S) := by nlinarith [sq_nonneg (C - S)]
  have key : 1 - 2 * (C * S) ≤ C + S - 2 * s * (C * S) := by
    have : 0 ≤ (C + S - 1) * (1 - (s - 1) * (C + S + 1)) :=
      mul_nonneg (by nlinarith [mul_pos hC0 hS0]) (by nlinarith)
    nlinarith
  have hcs : 0 < C * S := mul_pos hC0 hS0
  have h3 : C ^ 3 + S ^ 3 = (C + S) * (1 - C * S) := by nlinarith
  have : C * S * (2 * s - 2 * G - C - S) ≤ C * S * T := by
    nlinarith [mul_le_mul_of_nonneg_right hG.le hq]
  exact le_of_mul_le_mul_left this hcs

/-- **The `3 × 3` cases.**  `b` has frame `(P, Q)`, centre height `y`, left gap `A`, right gap `B`
(so `L = A + B + 2 + P + Q`), shelves at `lo` (left) and `lo2` (right).  Seven cases give `L ≥ 3` by one
`nlinarith`; only `UU` (both shelves above the side vertices: `b` hangs from the top) and its mirror `DD`
need the wedge bound. -/
theorem chain_bound {P Q H y lo lo2 A B s : ℝ} (hP : 0 ≤ P) (hQ : 0 ≤ Q) (hPQ : P^2 + Q^2 = 1)
    (hH : H < 2) (hy : (P + Q) / 2 ≤ y) (hy2 : y ≤ H - (P + Q) / 2) (hlo : 0 ≤ lo) (hlo' : lo ≤ H - 1)
    (hlo2 : 0 ≤ lo2) (hlo2' : lo2 ≤ H - 1) (hs : 0 < s) (hs2 : s^2 = 2)
    (hl : Wit P Q y lo A) (hr : Wit Q P y lo2 B) :
    3 ≤ A + B + 2 + P + Q ∨ 4 + 2 * s ≤ A + B + 2 + P + Q + 2 * H := by
  have hP1 : P ≤ 1 := by nlinarith
  have hQ1 : Q ≤ 1 := by nlinarith
  rcases hl with hA | ⟨l1, l2, l3⟩ | ⟨l1, l2, l3⟩ <;> rcases hr with hB | ⟨r1, r2, r3⟩ | ⟨r1, r2, r3⟩
  rotate_left 4
  · -- UU: the wedge
    right
    have := wedge_core (G := H - 1) (T := A + B) (by linarith) (by linarith) hPQ hs hs2 (by linarith)
      (by nlinarith [mul_le_mul_of_nonneg_left (by linarith : lo - (y + (P - Q) / 2) ≤ H - 1 - P)
            (sq_nonneg P), mul_le_mul_of_nonneg_left
            (by linarith : lo2 - (y + (Q - P) / 2) ≤ H - 1 - Q) (sq_nonneg Q)])
    linarith
  rotate_left 3
  · -- DD: the mirrored wedge
    right
    have := wedge_core (G := H - 1) (T := A + B) (by linarith) (by linarith) hPQ hs hs2 (by linarith)
      (by nlinarith [mul_le_mul_of_nonneg_left (by linarith : y + (P - Q) / 2 - lo - 1 ≤ H - 1 - Q)
            (sq_nonneg Q), mul_le_mul_of_nonneg_left
            (by linarith : y + (Q - P) / 2 - lo2 - 1 ≤ H - 1 - P) (sq_nonneg P)])
    linarith
  all_goals
    left; clear hs hs2
    nlinarith [mul_nonneg hP hQ, mul_nonneg (sub_nonneg.2 hP1) (sub_nonneg.2 hQ1)]

/-! ## Three squares -/

/-- The chain for three squares ordered by centre `x`. -/
theorem chain3 {ca cb cc : ℝ × ℝ} {θa θb θc L H : ℝ} (hA : sq ca θa 1 ⊆ rbox L H)
    (hB : sq cb θb 1 ⊆ rbox L H) (hC : sq cc θc 1 ⊆ rbox L H)
    (hab : Disjoint (sqInt ca θa 1) (sqInt cb θb 1)) (hbc : Disjoint (sqInt cb θb 1) (sqInt cc θc 1))
    (h1 : ca.1 ≤ cb.1) (h2 : cb.1 ≤ cc.1) (hH : H < 2) :
    3 ≤ L ∨ 4 + 2 * Real.sqrt 2 ≤ L + 2 * H := by
  obtain ⟨lo, l0, l1, hl⟩ := left_shelf hA hB hab h1 hH
  obtain ⟨lo2, r0, r1, hr⟩ := right_shelf hB hC hbc h2 hH
  obtain ⟨P, Q, hP, hQ, hPQ, -, -, hy1, hy2, hpt⟩ := framed hB
  have hk : 1 ≤ P + Q := by nlinarith
  obtain ⟨wl, wr⟩ := witnesses hk hH hy1 hy2 l0 l1 r0 r1 hpt hl hr
  have := chain_bound hP hQ hPQ hH hy1 hy2 l0 l1 r0 r1 (by positivity)
    (Real.sq_sqrt (by norm_num)) wl wr
  rcases this with h | h
  · left; linarith
  · right; linarith

/-- **Three unit squares, lower bound.**  If three unit squares pack `[0,L] × [0,H]` and `H < 2`, then
`L ≥ 3` or `L + 2H ≥ 4 + 2√2`. -/
theorem rect3_lower {L H : ℝ} (hp : RectPacks 3 L H) (hH : H < 2) :
    3 ≤ L ∨ 4 + 2 * Real.sqrt 2 ≤ L + 2 * H := by
  obtain ⟨ctr, ang, hin, hd⟩ := hp
  have go : ∀ i j k : Fin 3, i ≠ j → j ≠ k → (ctr i).1 ≤ (ctr j).1 → (ctr j).1 ≤ (ctr k).1 →
      3 ≤ L ∨ 4 + 2 * Real.sqrt 2 ≤ L + 2 * H := fun i j k hij hjk h1 h2 =>
    chain3 (hin i) (hin j) (hin k) (hd i j hij) (hd j k hjk) h1 h2 hH
  rcases le_total (ctr 0).1 (ctr 1).1 with a | a <;>
  rcases le_total (ctr 1).1 (ctr 2).1 with b | b <;>
  rcases le_total (ctr 0).1 (ctr 2).1 with c | c
  all_goals first
    | exact go 0 1 2 (by decide) (by decide) a b
    | exact go 0 2 1 (by decide) (by decide) c b
    | exact go 2 0 1 (by decide) (by decide) c a
    | exact go 1 0 2 (by decide) (by decide) a c
    | exact go 1 2 0 (by decide) (by decide) b c
    | exact go 2 1 0 (by decide) (by decide) b a

/-! ## Constructions and the exact region -/

/-- Upright squares from their centres, when the centres are pairwise `1` apart in some axis. -/
lemma upright_pack {n : ℕ} {w h : ℝ} (c : Fin n → ℝ × ℝ) (hin : ∀ i, sq (c i) 0 1 ⊆ rbox w h)
    (hsep : ∀ i j, i ≠ j → 1 ≤ |(c i).1 - (c j).1| ∨ 1 ≤ |(c i).2 - (c j).2|) :
    RectPacks n w h := by
  refine ⟨c, fun _ => 0, hin, fun i j hij => ?_⟩
  rw [Set.disjoint_left]
  intro p hp hq
  rw [sqInt_zero] at hp hq
  rcases hsep i j hij with h | h
  · have := abs_sub_le ((c i).1) p.1 ((c j).1)
    rw [abs_sub_comm ((c i).1) p.1] at this; linarith [hp.1, hq.1]
  · have := abs_sub_le ((c i).2) p.2 ((c j).2)
    rw [abs_sub_comm ((c i).2) p.2] at this; linarith [hp.2, hq.2]

/-- Three in a row. -/
theorem rect3_row {w h : ℝ} (hw : 3 ≤ w) (hh : 1 ≤ h) : RectPacks 3 w h := by
  apply upright_pack ![(1 / 2, 1 / 2), (3 / 2, 1 / 2), (5 / 2, 1 / 2)]
  · intro i; fin_cases i <;> exact sq_zero_subset (by norm_num) (by simp; linarith)
      (by norm_num) (by simp; linarith)
  · intro i j hij; left
    fin_cases i <;> fin_cases j <;> simp at hij ⊢ <;> norm_num [abs_of_pos, abs_of_neg]

/-- An L of three. -/
theorem rect3_ell {w h : ℝ} (hw : 2 ≤ w) (hh : 2 ≤ h) : RectPacks 3 w h := by
  apply upright_pack ![(1 / 2, 1 / 2), (3 / 2, 1 / 2), (1 / 2, 3 / 2)]
  · intro i; fin_cases i <;> exact sq_zero_subset (by norm_num) (by simp; linarith)
      (by norm_num) (by simp; linarith)
  · intro i j hij
    fin_cases i <;> fin_cases j <;> simp at hij ⊢ <;> norm_num [abs_of_pos, abs_of_neg]

/-- **`R₃` exactly.**  Three unit squares (any angles) fit in `[0,w] × [0,h]` iff both sides are at
least `1` and: both are at least `2`, or one is at least `3`, or the short side `s < 2` and the long
side `ℓ` satisfy `ℓ + 2s ≥ 4 + 2√2` (the wedge). -/
theorem rect3_iff {w h : ℝ} : RectPacks 3 w h ↔ 1 ≤ w ∧ 1 ≤ h ∧
    ((2 ≤ w ∧ 2 ≤ h) ∨ 3 ≤ w ∨ 3 ≤ h ∨ (h < 2 ∧ 4 + 2 * Real.sqrt 2 ≤ w + 2 * h) ∨
      (w < 2 ∧ 4 + 2 * Real.sqrt 2 ≤ h + 2 * w)) := by
  have hs : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hs1 : 1 < Real.sqrt 2 := by nlinarith [Real.sqrt_nonneg 2]
  constructor
  · intro hp
    obtain ⟨hw, hh⟩ := one_le_sides (hp.choose_spec.choose_spec.1 0)
    refine ⟨hw, hh, ?_⟩
    rcases lt_or_ge h 2 with hh2 | hh2
    · rcases rect3_lower hp hh2 with h3 | h3 <;> tauto
    rcases lt_or_ge w 2 with hw2 | hw2
    · rcases rect3_lower hp.swap hw2 with h3 | h3 <;> tauto
    · tauto
  · rintro ⟨hw, hh, h2 | h3 | h3 | ⟨hh2, hwe⟩ | ⟨hw2, hwe⟩⟩
    · exact rect3_ell h2.1 h2.2
    · exact rect3_row h3 hh
    · exact (rect3_row h3 hw).swap
    · rcases le_or_gt 3 w with h3 | h3
      · exact rect3_row h3 hh
      · exact rect3_wedge (by nlinarith) h3.le (by linarith)
    · rcases le_or_gt 3 h with h3 | h3
      · exact (rect3_row h3 hw).swap
      · exact (rect3_wedge (by nlinarith) h3.le (by linarith)).swap

end SquarePacking
