import PackingCertMathlib.Parametrize

/-!
# -- OPEN: Lemma CEIL — the simple packing bounds `s(n)` by `⌈√n⌉` (A219)

**What it asserts** (`docs/proofs/wall_torque.md` §1, any `n`).  The axis-aligned grid packing puts
`⌈√n⌉² ≥ n` unit squares into `[0, ⌈√n⌉]²`, so `n` unit squares FIT at side `⌈√n⌉`:
`Fits n ⌈√n⌉`.  Hence `s(n) ≤ ⌈√n⌉`, and every packing of side `≥ ⌈√n⌉` is beaten or tied by
the simple packing.  The PI's limitation L1 ("WLOG `S < ⌈√n⌉`") holds for a MINIMISER exactly
when `s(n) < ⌈√n⌉` — false for `n = k²`, `k² − 1`, `k² − 2` (there `s(n) = k`), true at `n = 11`
where the certified upper bound `ŝ = 3.877084 < 4` is the stronger statement used everywhere.

**Corollary (n = 11)** `Fits 11 4` (`⌈√11⌉ = 4`, proved below by `Nat.ceil_eq_iff` with
`3 = √9 < √11 ≤ √16 = 4`).  The readable layer's own upper bound is Trump's packing at `ŝ`
(`Statements/Attainment.lean`, `attained_thm`), so nothing downstream uses this file.

**Status (2026-09-14).**  [T] in prose (the grid construction, one line).  Lean obligation: build
the grid family `Q i := [a_i, a_i + 1] × [b_i, b_i + 1]` with `(a_i, b_i) = (i mod k, i div k)`,
`k = ⌈√n⌉`, and check `IsUnitSquare`, containment (`i div k < k` from `i < n ≤ k²`) and interior
disjointness of distinct grid cells — routine, not done.
-/

namespace PackingCert.S11.OpenLemmas

/-- **[OPEN] Lemma CEIL.**  `n` unit squares fit in the square of side `⌈√n⌉` (the grid packing). -/
axiom simple_packing_fits (n : ℕ) : Fits n (Nat.ceil (Real.sqrt (n : ℝ)))

theorem ceil_sqrt_eleven : Nat.ceil (Real.sqrt ((11 : ℕ) : ℝ)) = 4 := by
  have h11 : ((11 : ℕ) : ℝ) = 11 := by norm_num
  rw [h11, Nat.ceil_eq_iff (by norm_num)]
  refine ⟨?_, ?_⟩
  · have h9 : Real.sqrt 9 = 3 := by
      rw [show (9 : ℝ) = 3 ^ 2 by norm_num]
      exact Real.sqrt_sq (by norm_num)
    have h : Real.sqrt 9 < Real.sqrt 11 := Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
    rw [h9] at h
    exact_mod_cast h
  · have h16 : Real.sqrt 16 = 4 := by
      rw [show (16 : ℝ) = 4 ^ 2 by norm_num]
      exact Real.sqrt_sq (by norm_num)
    have h : Real.sqrt 11 ≤ Real.sqrt 16 := Real.sqrt_le_sqrt (by norm_num)
    rw [h16] at h
    exact_mod_cast h

/-- **Corollary (n = 11).**  Eleven unit squares fit at side 4. -/
theorem fits_eleven_four : Fits 11 4 := by
  have h := simple_packing_fits 11
  rw [ceil_sqrt_eleven] at h
  exact_mod_cast h

#print axioms simple_packing_fits
#print axioms fits_eleven_four

end PackingCert.S11.OpenLemmas
