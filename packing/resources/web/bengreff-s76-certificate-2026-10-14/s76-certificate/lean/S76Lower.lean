import Sqpack.S76T.Pts
import Sqpack.Attain

/-!
# `s(76) = 9` from a certified covering statement

`S76T.pts`, `S76T.segs` are the mixed cover `s76_cover_v5.txt` (sha256 `b6a1214b99f00e5dd136d74c8d87bccd178df38a1063b2c7be90517eb2b862b2`):
41633 points and 9744 axis-parallel segments of `[0,9]²`, masses `w/400000000`, total `< 76`
(kernel-checked in `S76T/Pts.lean`, with its exact D4 invariance).

`S76Cover` is the covering statement on the D4 fundamental region, in the sense of `CovM`:
every closed unit square inside `[0,9]²` with centre in `[0,9/2]²` and angle `2 arctan u`,
`u ∈ [0, 1/2]`, captures mass `≥ 1`. It is the statement the external exact checkers certify
(Evan Daniel's `zm_mixed.py`, and `zmx2`); it is a hypothesis here, not proved in Lean.
From it, `le_minSide_mixed` (Evan Daniel's `Sqpack`, unchanged) gives `s(76) ≥ 9`, and the 9×9
grid gives `s(76) ≤ 9`.
-/

namespace SquarePacking

open BoxTree ZMTreeM S76T

/-- The certified covering statement (hypothesis). -/
def S76Cover : Prop :=
  CovM 8000 4096 72000 4294967296 400000000 pts.toList segs.toList 0 (72000 * 4096 - 72000 * 4096 / 2) 0 (72000 * 4096 - 72000 * 4096 / 2) 0 2147483648

/-- **`s(76) ≥ 9`**, assuming the covering statement. -/
theorem s76_ge_9 (hcov : S76Cover) : (9 : ℝ) ≤ minSide 76 := by
  have h := le_minSide_mixed 8000 4096 72000 4294967296 2147483648 400000000 pts segs (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) pts_nodup pts_d4 segs_d4 hcov 76 9 wsum_lt (by norm_num)
  norm_num at h ⊢
  exact h

/-- **`s(76) = 9`**, assuming the covering statement. -/
theorem s76_eq_9 (hcov : S76Cover) : minSide 76 = 9 := by
  have h1 := s76_ge_9 hcov
  have hp : Packs 76 9 := by
    have h := packs_grid 9 76 (by norm_num)
    simpa using h
  have hb : BddBelow {s | Packs 76 s} := by
    by_contra hnb
    rw [minSide, Real.sInf_of_not_bddBelow hnb] at h1
    norm_num at h1
  exact le_antisymm (csInf_le hb hp) h1

end SquarePacking
