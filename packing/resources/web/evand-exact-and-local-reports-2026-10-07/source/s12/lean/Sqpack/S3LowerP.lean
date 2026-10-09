import Sqpack.M2p.Cov

/-!
# `s(3) ≥ 2` from a mixed cover with points and segments (toy, exercises Lemma P)

The cover `M2p` (`lean/toys/M2p.txt`, `lean/scripts/mk_toys.py`): the lines `x = 1`, `y = 1` of `[0,2]²`
at density `1/2` (40 segments, mass 2) plus points of mass `0.2` at the four tile centres and `0.05` at
`(1,1)`: total `2.85 < 3`.  Neither the segments (a square can hold only `≈ 0.83`) nor the points alone
suffice, so most leaves combine an L-block or S-block piece bound with `ADM` point witnesses for the remaining
`W − Lp` (`ZMTreeX.checkM`, Lemma P).
-/

namespace SquarePacking

open ZMTreeM

/-- **`s(3) ≥ 2`**, from a points-plus-segments mixed cover. -/
theorem s3_ge_2_mixed : (2 : ℝ) ≤ minSide 3 := by
  have h := le_minSide_mixed 1000 4096 2000 4294967296 2147483648 1000000 M2p.pts M2p.segs
    (by norm_num) (by norm_num) (by norm_num) (by norm_num) M2p.pts_nodup M2p.pts_d4 M2p.segs_d4
    M2p.cov_root 3 2 M2p.wsum_lt (by norm_num)
  have e : ((2000 : ℕ) : ℝ) / ((1000 : ℕ) : ℝ) = 2 := by norm_num
  rw [e] at h
  exact h

end SquarePacking
