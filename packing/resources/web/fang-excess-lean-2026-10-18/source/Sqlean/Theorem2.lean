import Sqlean.Main
import Sqlean.Pieces.R443

/-!
# Theorem 2: `s(n² − n + j(n)) < n` for every `n ≥ 15`

`j(n) = max(⌊(n + 1)/16⌋, 1 + 2⌊(n − 15)/21⌋)`.  Two inductions on top of `main`:

* `stepR`: Lemma 3 with `R` (`257` squares in `(17 − d₀) × (16 − d₀)`, waste `15`) adds `16` to
  `n` and `1` to the excess;
* `stepR'`: Lemma 3 with `R'` (`443` squares in `(22 − d₀) × (21 − d₀)`, waste `19`) adds `21` to
  `n` and `2` to the excess.
-/

namespace UnitSquarePacking

/-- The rectangle `R'`: `443` unit squares in `(22 − 1/10000) × (21 − 1/10000)`. -/
theorem rectR' : PacksR 443 (((22 : ℕ) : ℝ) - 1 / 10000) (((21 : ℕ) : ℝ) - 1 / 10000) := by
  convert Data.R443.packsR using 2 <;> norm_num

theorem stepR {m j : ℕ} (hm : 11 ≤ m) (hB : Packs (m ^ 2 - m + j) ((m : ℝ) - 1 / 10000)) :
    Packs ((m + 16) ^ 2 - (m + 16) + (j + 1)) (((m + 16 : ℕ) : ℝ) - 1 / 10000) := by
  have h := step hm hB
  have e : 257 + (m + 16 - 17) * 16 + (m + 16 - m) * (m + 16 - 16) + (m ^ 2 - m + j) =
      (m + 16) ^ 2 - (m + 16) + (j + 1) := by
    rw [show m + 16 - 17 = m - 1 by omega, show m + 16 - m = 16 by omega,
      show m + 16 - 16 = m by omega]
    have h4 : m ≤ m ^ 2 := by nlinarith
    have h5 : m + 16 ≤ (m + 16) ^ 2 := by nlinarith
    zify [h4, h5, (by omega : 1 ≤ m)]
    ring
  rwa [e] at h

theorem stepR' {m j : ℕ} (hm : 11 ≤ m) (hB : Packs (m ^ 2 - m + j) ((m : ℝ) - 1 / 10000)) :
    Packs ((m + 21) ^ 2 - (m + 21) + (j + 2)) (((m + 21 : ℕ) : ℝ) - 1 / 10000) := by
  have hm' : (11 : ℝ) ≤ m := by exact_mod_cast hm
  have h := glue_sq (a := 22) (b := 21) (n := m + 21) rectR' hB (by omega) (by norm_num)
    (by norm_num) (by linarith) (by omega) (by norm_num)
  have e : 443 + (m + 21 - 22) * 21 + (m + 21 - m) * (m + 21 - 21) + (m ^ 2 - m + j) =
      (m + 21) ^ 2 - (m + 21) + (j + 2) := by
    rw [show m + 21 - 22 = m - 1 by omega, show m + 21 - m = 21 by omega,
      show m + 21 - 21 = m by omega]
    have h4 : m ≤ m ^ 2 := by nlinarith
    have h5 : m + 21 ≤ (m + 21) ^ 2 := by nlinarith
    zify [h4, h5, (by omega : 1 ≤ m)]
    ring
  rwa [e] at h

/-- Excess `⌊(n + 1)/16⌋` (uses `R` only). -/
theorem packs_j16 (n : ℕ) (h : 15 ≤ n) :
    Packs (n ^ 2 - n + (n + 1) / 16) ((n : ℝ) - 1 / 10000) := by
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    by_cases h30 : n ≤ 30
    · rw [show (n + 1) / 16 = 1 by omega]; exact main n h
    obtain ⟨m, rfl⟩ : ∃ m, n = m + 16 := ⟨n - 16, by omega⟩
    rw [show (m + 16 + 1) / 16 = (m + 1) / 16 + 1 by omega]
    exact stepR (by omega) (ih m (by omega) (by omega))

/-- Excess `1 + 2⌊(n − 15)/21⌋` (uses `R'` on top of `main`). -/
theorem packs_j21 (n : ℕ) (h : 15 ≤ n) :
    Packs (n ^ 2 - n + (1 + 2 * ((n - 15) / 21))) ((n : ℝ) - 1 / 10000) := by
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    by_cases h35 : n ≤ 35
    · rw [show 1 + 2 * ((n - 15) / 21) = 1 by omega]; exact main n h
    obtain ⟨m, rfl⟩ : ∃ m, n = m + 21 := ⟨n - 21, by omega⟩
    rw [show 1 + 2 * ((m + 21 - 15) / 21) = (1 + 2 * ((m - 15) / 21)) + 2 by omega]
    exact stepR' (by omega) (ih m (by omega) (by omega))

/-- The excess of Theorem 2. -/
def jExc (n : ℕ) : ℕ := max ((n + 1) / 16) (1 + 2 * ((n - 15) / 21))

theorem main2 (n : ℕ) (h : 15 ≤ n) : Packs (n ^ 2 - n + jExc n) ((n : ℝ) - 1 / 10000) := by
  unfold jExc
  rcases le_total ((n + 1) / 16) (1 + 2 * ((n - 15) / 21)) with hle | hle
  · rw [max_eq_right hle]; exact packs_j21 n h
  · rw [max_eq_left hle]; exact packs_j16 n h

/-- **Theorem 2.** `s(n² − n + j(n)) < n` for every `n ≥ 15`,
`j(n) = max(⌊(n + 1)/16⌋, 1 + 2⌊(n − 15)/21⌋)`. -/
theorem theorem2 (n : ℕ) (h : 15 ≤ n) : minSide (n ^ 2 - n + jExc n) < n :=
  lt_of_le_of_lt (minSide_le_of_packs (by unfold jExc; omega) (main2 n h)) (by linarith)

end UnitSquarePacking
