import Sqlean.Glue
import Sqlean.Pieces.N211
import Sqlean.Pieces.N241
import Sqlean.Pieces.N273
import Sqlean.Pieces.N308
import Sqlean.Pieces.N343
import Sqlean.Pieces.N381
import Sqlean.Pieces.N421
import Sqlean.Pieces.N463
import Sqlean.Pieces.N507
import Sqlean.Pieces.N553
import Sqlean.Pieces.N601
import Sqlean.Pieces.N651
import Sqlean.Pieces.M110
import Sqlean.Pieces.M132
import Sqlean.Pieces.M156
import Sqlean.Pieces.M182
import Sqlean.Pieces.R257

/-!
# Theorem 1: `s(n² − n + 1) < n` for every `n ≥ 15`

All packings below are at the uniform squeeze `d₀ = 1/10000`.

* `base`: `15 ≤ n ≤ 26` from the kernel-checked certificates (`n = 18` from `308` squares by
  dropping one).
* `small`: `m² − m` squares for `11 ≤ m ≤ 14` (Daniel's exact certificates of the packings of
  Ellsworth and of Arslanov–Mustafin–Shangitbayev).
* `step`: Lemma 3 with `A = R` (`257` squares in `(17 − d₀) × (16 − d₀)`) and a square `B`.
* `main`: strong induction (`27 ≤ n ≤ 30` from `small`, `n ≥ 31` from `n − 16`).
-/

namespace UnitSquarePacking

/-- `n² − n + 1` unit squares in a square of side `n − 1/10000`, `15 ≤ n ≤ 26`. -/
theorem base (n : ℕ) (h1 : 15 ≤ n) (h2 : n ≤ 26) :
    Packs (n ^ 2 - n + 1) ((n : ℝ) - 1 / 10000) := by
  interval_cases n
  · convert packs_iff_packsR.2 Data.N211.packsR using 2 <;> norm_num
  · convert packs_iff_packsR.2 Data.N241.packsR using 2 <;> norm_num
  · convert packs_iff_packsR.2 Data.N273.packsR using 2 <;> norm_num
  · convert packs_of_le (packs_iff_packsR.2 Data.N308.packsR) (by norm_num : 307 ≤ 308)
      using 2 <;> norm_num
  · convert packs_iff_packsR.2 Data.N343.packsR using 2 <;> norm_num
  · convert packs_iff_packsR.2 Data.N381.packsR using 2 <;> norm_num
  · convert packs_iff_packsR.2 Data.N421.packsR using 2 <;> norm_num
  · convert packs_iff_packsR.2 Data.N463.packsR using 2 <;> norm_num
  · convert packs_iff_packsR.2 Data.N507.packsR using 2 <;> norm_num
  · convert packs_iff_packsR.2 Data.N553.packsR using 2 <;> norm_num
  · convert packs_iff_packsR.2 Data.N601.packsR using 2 <;> norm_num
  · convert packs_iff_packsR.2 Data.N651.packsR using 2 <;> norm_num

/-- `m² − m` unit squares in a square of side `m − 1/10000`, `11 ≤ m ≤ 14`. -/
theorem small (m : ℕ) (h1 : 11 ≤ m) (h2 : m ≤ 14) :
    Packs (m ^ 2 - m) ((m : ℝ) - 1 / 10000) := by
  interval_cases m
  · convert packs_iff_packsR.2 Data.M110.packsR using 2 <;> norm_num
  · convert packs_iff_packsR.2 Data.M132.packsR using 2 <;> norm_num
  · convert packs_iff_packsR.2 Data.M156.packsR using 2 <;> norm_num
  · convert packs_iff_packsR.2 Data.M182.packsR using 2 <;> norm_num

/-- The rectangle `R`: `257` unit squares in `(17 − 1/10000) × (16 − 1/10000)`. -/
theorem rectR : PacksR 257 (((17 : ℕ) : ℝ) - 1 / 10000) (((16 : ℕ) : ℝ) - 1 / 10000) := by
  convert Data.R257.packsR using 2 <;> norm_num

/-- One gluing step: `R` on top, `B` (side `m − 1/10000`) bottom right, `n = m + 16`. -/
theorem step {m NB : ℕ} (hm : 11 ≤ m) (hB : Packs NB ((m : ℝ) - 1 / 10000)) :
    Packs (257 + (m + 16 - 17) * 16 + (m + 16 - m) * (m + 16 - 16) + NB)
      (((m + 16 : ℕ) : ℝ) - 1 / 10000) := by
  have hm' : (11 : ℝ) ≤ m := by exact_mod_cast hm
  exact glue_sq (a := 17) (b := 16) rectR hB (by omega) (by norm_num) (by norm_num) (by linarith)
    (by omega) (by norm_num)

lemma count_small {m : ℕ} (hm : 1 ≤ m) :
    257 + (m + 16 - 17) * 16 + (m + 16 - m) * (m + 16 - 16) + (m ^ 2 - m) =
      (m + 16) ^ 2 - (m + 16) + 1 := by
  rw [show m + 16 - 17 = m - 1 by omega, show m + 16 - m = 16 by omega,
    show m + 16 - 16 = m by omega]
  have h4 : m ≤ m ^ 2 := by nlinarith
  have h5 : m + 16 ≤ (m + 16) ^ 2 := by nlinarith
  zify [h4, h5, hm]
  ring

lemma count_step {m : ℕ} (hm : 1 ≤ m) :
    257 + (m + 16 - 17) * 16 + (m + 16 - m) * (m + 16 - 16) + (m ^ 2 - m + 1) =
      (m + 16) ^ 2 - (m + 16) + 2 := by
  rw [show m + 16 - 17 = m - 1 by omega, show m + 16 - m = 16 by omega,
    show m + 16 - 16 = m by omega]
  have h4 : m ≤ m ^ 2 := by nlinarith
  have h5 : m + 16 ≤ (m + 16) ^ 2 := by nlinarith
  zify [h4, h5, hm]
  ring

/-- **`n² − n + 1` unit squares fit in a square of side `n − 1/10000`, for every `n ≥ 15`.** -/
theorem main (n : ℕ) (h : 15 ≤ n) : Packs (n ^ 2 - n + 1) ((n : ℝ) - 1 / 10000) := by
  induction n using Nat.strong_induction_on with
  | _ n ih =>
    by_cases h26 : n ≤ 26
    · exact base n h h26
    obtain ⟨m, rfl⟩ : ∃ m, n = m + 16 := ⟨n - 16, by omega⟩
    by_cases h30 : m ≤ 14
    · have := step (by omega) (small m (by omega) h30)
      rwa [count_small (by omega)] at this
    · have := step (by omega) (ih m (by omega) (by omega))
      rw [count_step (by omega)] at this
      exact packs_of_le this (by omega)

/-- **Theorem 1.** `s(n² − n + 1) < n` for every integer `n ≥ 15`. -/
theorem theorem1 (n : ℕ) (h : 15 ≤ n) : minSide (n ^ 2 - n + 1) < n :=
  lt_of_le_of_lt (minSide_le_of_packs (by omega) (main n h)) (by linarith)

end UnitSquarePacking
