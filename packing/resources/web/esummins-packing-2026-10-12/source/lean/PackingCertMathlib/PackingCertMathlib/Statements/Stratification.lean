import PackingCertMathlib.TopLevel

/-!
# Stratification — every packing on the window has a skeleton in the census

**What it says.**  For every side `s ∈ (3, 4)` and every packing `z` at side `s`, the
Young-form SKELETON of `z` — the largest set of exactly-on-grid axis-aligned squares at each
corner (A53 L1) — is one of the 1110 census tuples (`skeleton_mem_census`), hence a D4-image of
one of the 163 class representatives (`exists_stratum`).  So a minimiser at a side in the
window `[3.82, ŝ]` lies in some stratum (`stratification`), and the optimality proof splits
into one obligation per class: `stratum_kill` for the 162 non-Trump classes, `trump_residual`
for Trump's class `((2,1),(1),(1),∅)`.

**Why it matters.**  It is the case split of the whole proof.  The census is a Lean DEFINITION
(`Census.lean`: `skeleton`, `censusL`, `classCodes`, the D4 action) and its exhaustiveness a
THEOREM, so no axiom carries the list of cases; the per-class obligations are the only debt.

**How it is proved** (`Census.lean`, A78; prose `docs/proofs/contact_census.md`,
`instratum_bridge.md`): at `s ∈ (3, 4)` the cells of a skeleton form Young diagrams at each
corner inside the `3 × 3` box, and two pins at the same wall are far apart; both are decided by
the exact geometry of on-grid squares.  `stratify` is `parametrize` + exhaustiveness.

**For any `n`.**  The census of Young 4-tuples depends on the side range `(3, 4)`, not on `n`;
the same construction gives the skeleton census of any `n` at any side range with an integer
part.
-/

namespace PackingCert.S11

open Set

/-- **Census exhaustiveness.**  Every packing at a side in `(3, 4)` has its skeleton in the
census. -/
theorem skeleton_in_census {s : ℝ} (hs3 : 3 < s) (hs4 : s < 4) {z : Fin 11 → PSq}
    (hP : IsPacking 11 s fun i => (z i).set) : skeleton s z ∈ censusF :=
  skeleton_mem_census hs3 hs4 hP

/-- **Every packing on the window lies in some stratum.** -/
theorem exists_stratum_stmt {m : ℝ} (hm : m ∈ wnd) {z : Cfg} (hz : CfgPacking m z) :
    ∃ i : StratumIdx, InStratum i m z :=
  exists_stratum hm hz

/-- **Stratification of the minimiser.**  If the minimum is attained at `m ∈ [3.82, ŝ]`, some
minimising configuration lies in some stratum. -/
theorem stratification : ∀ m : ℝ, IsLeast {s : ℝ | Fits 11 s} m → m ∈ wnd →
    ∃ (z : Cfg) (i : StratumIdx), CfgPacking m z ∧ InStratum i m z :=
  stratify

#print axioms skeleton_in_census
#print axioms exists_stratum_stmt
#print axioms stratification

end PackingCert.S11
