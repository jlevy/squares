import Sqpack.ExactPack

/-!
# `s(5) ≤ 2 + √2/2`, from exact data

Demo of the exact-data route (`search/exact/minpoly.py` → `verify_exact.py` → here) on the smallest tilted case.
The data are the output of `minpoly.py` for the register's n = 5 packing: field `ℚ(t)`, `t² + 2t - 1 = 0`
(`t = √2 - 1`), `S = 5/2 + t/2 = 2 + √2/2`; four axis-parallel squares in the corners and one at 45° in the middle
(`c = s = √2/2`).  Written here with `r = √2/2`, so `S = 2 + r`.
-/

namespace UnitSquarePacking.N5

open Real

noncomputable def r : ℝ := √2 / 2
noncomputable def S : ℝ := 2 + r

lemma r_sq : r ^ 2 = 1 / 2 := by
  unfold r; rw [div_pow, sq_sqrt (by norm_num : (0:ℝ) ≤ 2)]; norm_num

lemma r_pos : 0 < r := by unfold r; positivity

lemma r_lt : r < 3 / 4 := by nlinarith [r_sq, r_pos]

noncomputable def xs : Fin 5 → ℝ := ![1/2, S - 1/2, 1/2, S - 1/2, S / 2]
noncomputable def ys : Fin 5 → ℝ := ![S - 1/2, S - 1/2, 1/2, 1/2, S / 2]
noncomputable def cs : Fin 5 → ℝ := ![1, 1, 1, 1, r]
noncomputable def ss : Fin 5 → ℝ := ![0, 0, 0, 0, r]

/-- Proves `SepSide …` for a concrete side: the four corners, then `nlinarith` with `r² = 1/2`. -/
macro "sep_side" : tactic => `(tactic| (
  intro a b ha hb
  rcases ha with ha | ha <;> rcases hb with hb | hb <;> subst ha hb <;>
    simp [nrm, xs, ys, cs, ss, S] <;> nlinarith [r_sq, r_pos, r_lt]))

/-! The separating side line of each pair `(i, j)`, `i < j` (`inl`: a side of `i`; `inr`: a side of `j`). -/

lemma sep01 : SepPair (xs 0) (ys 0) (cs 0) (ss 0) (xs 1) (ys 1) (cs 1) (ss 1) :=
  Or.inl ⟨0, by sep_side⟩

lemma sep02 : SepPair (xs 0) (ys 0) (cs 0) (ss 0) (xs 2) (ys 2) (cs 2) (ss 2) :=
  Or.inl ⟨3, by sep_side⟩

lemma sep03 : SepPair (xs 0) (ys 0) (cs 0) (ss 0) (xs 3) (ys 3) (cs 3) (ss 3) :=
  Or.inl ⟨0, by sep_side⟩

lemma sep04 : SepPair (xs 0) (ys 0) (cs 0) (ss 0) (xs 4) (ys 4) (cs 4) (ss 4) :=
  Or.inr ⟨1, by sep_side⟩

lemma sep12 : SepPair (xs 1) (ys 1) (cs 1) (ss 1) (xs 2) (ys 2) (cs 2) (ss 2) :=
  Or.inr ⟨0, by sep_side⟩

lemma sep13 : SepPair (xs 1) (ys 1) (cs 1) (ss 1) (xs 3) (ys 3) (cs 3) (ss 3) :=
  Or.inl ⟨3, by sep_side⟩

lemma sep14 : SepPair (xs 1) (ys 1) (cs 1) (ss 1) (xs 4) (ys 4) (cs 4) (ss 4) :=
  Or.inr ⟨0, by sep_side⟩

lemma sep23 : SepPair (xs 2) (ys 2) (cs 2) (ss 2) (xs 3) (ys 3) (cs 3) (ss 3) :=
  Or.inl ⟨0, by sep_side⟩

lemma sep24 : SepPair (xs 2) (ys 2) (cs 2) (ss 2) (xs 4) (ys 4) (cs 4) (ss 4) :=
  Or.inr ⟨2, by sep_side⟩

lemma sep34 : SepPair (xs 3) (ys 3) (cs 3) (ss 3) (xs 4) (ys 4) (cs 4) (ss 4) :=
  Or.inr ⟨3, by sep_side⟩

theorem packs_five : Packs 5 (2 + √2 / 2) := by
  have hS : (2 + √2 / 2 : ℝ) = S := rfl
  rw [hS]
  refine packs_of_cert xs ys cs ss ?_ ?_ ?_
  · intro i
    fin_cases i <;> (simp [cs, ss] <;> nlinarith [r_sq])
  · intro i a b ha hb
    fin_cases i <;>
      rcases ha with rfl | rfl <;> rcases hb with rfl | rfl <;>
      simp [xs, ys, cs, ss, S] <;> (repeat' apply And.intro) <;> nlinarith [r_sq, r_pos, r_lt]
  · intro i j hij
    fin_cases i <;> fin_cases j <;> simp at hij <;>
    first
      | exact sep01
      | exact sep02
      | exact sep03
      | exact sep04
      | exact sep12
      | exact sep13
      | exact sep14
      | exact sep23
      | exact sep24
      | exact sep34

end UnitSquarePacking.N5
