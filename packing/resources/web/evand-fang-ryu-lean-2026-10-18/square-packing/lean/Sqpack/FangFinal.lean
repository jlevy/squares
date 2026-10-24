import Sqpack.FangTheorem
import Sqpack.Exact.Fang.P110
import Sqpack.Exact.Fang.P132
import Sqpack.Exact.Fang.P156
import Sqpack.Exact.Fang.P182
import Sqpack.Exact.Fang.P211
import Sqpack.Exact.Fang.P241
import Sqpack.Exact.Fang.P273
import Sqpack.Exact.Fang.P308
import Sqpack.Exact.Fang.P343
import Sqpack.Exact.Fang.P381
import Sqpack.Exact.Fang.P421
import Sqpack.Exact.Fang.P463
import Sqpack.Exact.Fang.P507
import Sqpack.Exact.Fang.P553
import Sqpack.Exact.Fang.P601
import Sqpack.Exact.Fang.P651
import Sqpack.Exact.Fang.R257
import Sqpack.Exact.Fang.R443

/-!
# Fang's theorems, unconditionally

K. Fang, *Packing n² − n + 1 unit squares in a square of side less than n, for every n ≥ 15* (draft v0.6,
2026-10-13; jlevy/squares#603, T-163), after Arslanov–Mustafin–Shangitbayev (EJC 28(4) P4.22, 2021).

The pieces (`certificates/fang-gluing/inputs/`, each checked by `decide +kernel` in `Sqpack/Exact/Fang/`):

* `R257`, `R443`: Fang's squeezable rectangles, 257 squares in 17 × 16 and 443 in 22 × 21.
* `P211`, `P241`, `P273`: exact certificates (Daniel) of de Winter's 211 and Ellsworth–Stead's 241 and 273.
* `P308`, `P343`, `P381`, …, `P651`: Fang's direct packings of `m² − m + 1` (308: `+ 2`) squares in side `< m`.
* `P110`, `P132`, `P156`, `P182`: exact certificates (Daniel) of Ellsworth's 110 and Arslanov–Mustafin–
  Shangitbayev's 132, 156, 182 (`m² − m` squares in side `< m`).

`fangPieces : FangPieces`, then `theorem1` and `theorem2`.
-/

namespace UnitSquarePacking.FangGlue

open UnitSquarePacking.Conjectures

/-- A square certificate with side bound `Sb < m`. -/
lemma sq_of_cert {N m : ℕ} {pS : EC.Poly} {Sa Sb : ℚ}
    (h : ∃ s : ℝ, EC.peval pS s = 0 ∧ (Sa : ℝ) ≤ s ∧ s ≤ Sb ∧ Packs N s) (hm : (Sb : ℝ) < m) :
    Squeezable N m m :=
  let ⟨_, _, _, hs, hp⟩ := h; squeezable_of_packs hp (lt_of_le_of_lt hs hm)

/-- A rectangle certificate with side bound `Sb < a` and height `H < b`. -/
lemma rect_of_cert {N a b : ℕ} {pS : EC.Poly} {Sa Sb H : ℚ}
    (h : ∃ s : ℝ, EC.peval pS s = 0 ∧ (Sa : ℝ) ≤ s ∧ s ≤ Sb ∧ PacksIn N (rect s (H : ℝ)))
    (ha : (Sb : ℝ) < a) (hb : (H : ℝ) < b) : Squeezable N a b :=
  let ⟨_, _, _, hs, hp⟩ := h; squeezable_of_packsIn hp (lt_of_le_of_lt hs ha) hb

/-- All of Fang's pieces, from the certificates. -/
theorem fangPieces : FangPieces where
  R := rect_of_cert EC.R257.packs (by norm_num) (by simp only [EC.R257.H]; norm_num)
  R' := rect_of_cert EC.R443.packs (by norm_num) (by simp only [EC.R443.H]; norm_num)
  base r h1 h2 := by
    unfold Excess
    interval_cases r
    · exact sq_of_cert EC.P211.packs (by norm_num)
    · exact sq_of_cert EC.P241.packs (by norm_num)
    · exact sq_of_cert EC.P273.packs (by norm_num)
    · exact (sq_of_cert EC.P308.packs (by norm_num)).drop (by norm_num)
    · exact sq_of_cert EC.P343.packs (by norm_num)
    · exact sq_of_cert EC.P381.packs (by norm_num)
    · exact sq_of_cert EC.P421.packs (by norm_num)
    · exact sq_of_cert EC.P463.packs (by norm_num)
    · exact sq_of_cert EC.P507.packs (by norm_num)
    · exact sq_of_cert EC.P553.packs (by norm_num)
    · exact sq_of_cert EC.P601.packs (by norm_num)
    · exact sq_of_cert EC.P651.packs (by norm_num)
  base0 m h1 h2 := by
    unfold Excess
    interval_cases m
    · exact sq_of_cert EC.P110.packs (by norm_num)
    · exact sq_of_cert EC.P132.packs (by norm_num)
    · exact sq_of_cert EC.P156.packs (by norm_num)
    · exact sq_of_cert EC.P182.packs (by norm_num)

/-- **Fang, Theorem 1.**  `s(n² − n + 1) < n` for every `n ≥ 15`. -/
theorem theorem1 (n : ℕ) (hn : 15 ≤ n) : ∃ s < (n : ℝ), Packs (n * n - n + 1) s :=
  fangPieces.theorem1 n hn

/-- **Fang, Theorem 2.**  For `n ≥ 15` and `16p + 21q ≤ n − 15`, `n² − n + 1 + p + 2q` unit squares pack in a
square of side `< n`. -/
theorem theorem2 (n p q : ℕ) (hn : 15 ≤ n) (hpq : 16 * p + 21 * q ≤ n - 15) :
    ∃ s < (n : ℝ), Packs (n * n - n + (1 + p + 2 * q)) s :=
  (fangPieces.theorem2 n p q hn hpq).packs

end UnitSquarePacking.FangGlue
