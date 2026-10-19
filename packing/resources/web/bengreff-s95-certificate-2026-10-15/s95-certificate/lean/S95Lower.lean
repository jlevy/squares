import Sqpack.S95T.Pts
import Sqpack.Attain

/-!
# `s(95) = 10` from a certified covering statement

`S95T.pts`, `S95T.segs` are the mixed cover `s95_cover_v2.txt` (sha256 `8b2d2152867585c82920bc90c6c3ec2a2458ef2ba57311ccd7dd436d1344cb7c`):
48352 points and 11438 axis-parallel segments of `[0,10]²`, masses `w/400000000`, total `< 95`
(kernel-checked in `S95T/Pts.lean`, with its exact D4 invariance).

`S76Cover` is the covering statement on the D4 fundamental region, in the sense of `CovM`:
every closed unit square inside `[0,10]²` with centre in `[0,10/2]²` and angle `2 arctan u`,
`u ∈ [0, 1/2]`, captures mass `≥ 1`. It is the statement the external exact checkers certify
(Evan Daniel's `zm_mixed.py`, and `zmx2`); it is a hypothesis here, not proved in Lean.
From it, `le_minSide_mixed` (Evan Daniel's `Sqpack`, unchanged) gives `s(95) ≥ 10`, and the 10×10
grid gives `s(95) ≤ 10`.
-/

namespace SquarePacking

open BoxTree ZMTreeM S95T

/-- The certified covering statement (hypothesis). -/
def S95Cover : Prop :=
  CovM 8000 4096 80000 4294967296 400000000 pts.toList segs.toList 0 (80000 * 4096 - 80000 * 4096 / 2) 0 (80000 * 4096 - 80000 * 4096 / 2) 0 2147483648

/-- **`s(95) ≥ 10`**, assuming the covering statement. -/
theorem s95_ge_10 (hcov : S95Cover) : (10 : ℝ) ≤ minSide 95 := by
  have h := le_minSide_mixed 8000 4096 80000 4294967296 2147483648 400000000 pts segs (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) pts_nodup pts_d4 segs_d4 hcov 95 10 wsum_lt (by norm_num)
  norm_num at h ⊢
  exact h

/-- **`s(95) = 10`**, assuming the covering statement. -/
theorem s95_eq_10 (hcov : S95Cover) : minSide 95 = 10 := by
  have h1 := s95_ge_10 hcov
  have hp : Packs 95 10 := by
    have h := packs_grid 10 95 (by norm_num)
    simpa using h
  have hb : BddBelow {s | Packs 95 s} := by
    by_contra hnb
    rw [minSide, Real.sInf_of_not_bddBelow hnb] at h1
    norm_num at h1
  exact le_antisymm (csInf_le hb hp) h1

end SquarePacking
