import PackingCertMathlib.Statements.Open.StuckExist

/-!
# -- OPEN: the PERIMETER WALK -- closed-form kills of walks around the twelve border cells (A247)

`docs/proofs/perimeter_walk.md`.  The PI (2026-09-16, 23:30): set down BL's two meeters and chase
the meeter counts around the twelve cells.  A247 catalogues the cell-sets one unit square can meet
(every subset of a corner's five-cell neighbourhood `N_c`, nothing else -- the PROJECTION lemma),
enumerates the walks the catalogue and the certified pair table allow, and kills walks by
bounded interval searches.  Two of the kills are closed-form and n-general; they are recorded
here as prose axioms [T] with the consequences they buy as theorems.

**TWO-FAR** [T] (`perimeter_walk.md` §2.2).  At a side `m > 7/2` two interior-disjoint unit
squares cannot both meet the corner box `(0,1)²` and the far floor slot `(m-2, m-1) × (0,1)`:
each contains a segment at height `< 1` from `x < 1` to `x > m - 2`; the separating line is not
vertical, so one square, say `B`, lies under the other's segment on the strip `(1, m-2)`, its
vertical chord there is shorter than `1`, and a unit square's vertical chord is `< 1` only within
`sin θ cos θ ≤ 1/2 < m - 3` of its two ends -- the strip cannot fit in either end.  Stated for the
corner `BL` and its floor; every other corner and wall is a D4 image.  Consequence: in a walk no
two meeters of one corner share a far slot (`ADJ` supply into a far slot comes from at most one
meeter of the adjacent corner).

**UPPER-END** [T] (`perimeter_walk.md` §2.3).  No packing of eleven unit squares at a side
`m ≥ 4 + √2` is 12-stuck.  Above `4 + √2` the cells' along-wall intervals `(1,2)` and `(m-2,m-1)`
are more than `√2` apart, so every square meets cells of ONE corner only (the projection lemma);
a corner with exactly two meeters gets at most 3 of its 4 slot incidences from them
(NOT-SELF-SUFFICIENT, A246) and needs a free square dedicated to it, while a corner with `t ≥ 3`
meeters costs a free square; with `n = 11`: `4 - t` corners need `≤ 3 - t` free squares.  This is
the theorem form of A244's conditional bound; the twelve-cell window for `n = 11` is
`[2 + √2, 4 + √2)`.

**Status (2026-09-16).**  `two_far`, `upper_end_twelve_stuck`: axioms [T] (prose proofs in the
note, n-general, D4-symmetric).  `twelve_stuck_side_lt`, `no_twelve_stuck_of_upper`: theorems.
The window statement STUCK-EXIST(11) itself is unchanged (`stuck_exist_eleven`).
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- **Lemma TWO-FAR** [T]: at a side `m > 7/2`, two interior-disjoint unit squares of a packing
cannot both meet the open corner box `(0,1)²` and the open far floor slot `(m-2, m-1) × (0,1)`. -/
axiom two_far (n : ℕ) (m : ℝ) (hm : (7 : ℝ) / 2 < m) (Q : Fin n → Set RP) (hP : IsPacking n m Q)
    (i j : Fin n) (hij : i ≠ j)
    (hi0 : MeetsCell (Q i) 0 1 0 1) (hi1 : MeetsCell (Q i) (m - 2) (m - 1) 0 1)
    (hj0 : MeetsCell (Q j) 0 1 0 1) (hj1 : MeetsCell (Q j) (m - 2) (m - 1) 0 1) : False

/-- **Theorem UPPER-END** [T]: no packing of eleven unit squares at a side `m ≥ 4 + √2` is
12-stuck (the twelve-cell window for `n = 11` ends at `4 + √2`). -/
axiom upper_end_twelve_stuck (m : ℝ) (hm : 4 + Real.sqrt 2 ≤ m) (z : Cfg) (hz : CfgPacking m z)
    (h12 : TwelveStuck m z) : False

/-- A 12-stuck packing of eleven squares has side below `4 + √2`. -/
theorem twelve_stuck_side_lt (m : ℝ) (z : Cfg) (hz : CfgPacking m z) (h12 : TwelveStuck m z) :
    m < 4 + Real.sqrt 2 := by
  by_contra h
  exact upper_end_twelve_stuck m (not_lt.mp h) z hz h12

/-- The contrapositive form used by the walk list: at or above `4 + √2` nothing is 12-stuck. -/
theorem no_twelve_stuck_of_upper (m : ℝ) (hm : 4 + Real.sqrt 2 ≤ m) (z : Cfg) (hz : CfgPacking m z) :
    ¬ TwelveStuck m z :=
  fun h12 => upper_end_twelve_stuck m hm z hz h12

/-- With STUCK-EXIST(11) (still an axiom) the 12-stuck sides of eleven squares would lie in
`[4, 4 + √2)`; A244 certifies 482 of them from `4.000010` to `4.5`. -/
theorem twelve_stuck_sides (m : ℝ) (z : Cfg) (hz : CfgPacking m z) (h12 : TwelveStuck m z) :
    4 ≤ m ∧ m < 4 + Real.sqrt 2 := by
  refine ⟨?_, twelve_stuck_side_lt m z hz h12⟩
  by_contra h
  exact stuck_exist_eleven m (not_le.mp h) z hz h12

#print axioms two_far
#print axioms upper_end_twelve_stuck
#print axioms twelve_stuck_side_lt
#print axioms no_twelve_stuck_of_upper
#print axioms twelve_stuck_sides

end PackingCert.S11.OpenLemmas
