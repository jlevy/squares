import PackingCertMathlib.Attain

/-!
# Attainment — `s(11)` is a minimum, not just an infimum (drain lemma D1)

**What it says.**  The set of container sides at which eleven unit squares fit,
`{s | Fits 11 s}`, has a least element.  So `s(11) = sInf {s | Fits 11 s}` is realised by an
actual packing, and the optimality theorem may be argued at the single side `m = s(11)`.

**Why it matters.**  Every downstream step (census, per-class kills, the rigidity basin) is a
statement about a packing at the minimal side.  Without attainment each leaf lemma would have
to be stated for limits of packings.

**How it is proved** (`Attain.lean`, A68; prose `docs/proofs/drain_lemma.md` D1).  The feasible
region in coordinates — the 33 square coordinates `(cx, cy, t)` and the side, cut out by
`t ∈ [0,1]`, the containment inequalities and pairwise non-overlap — is closed and bounded, hence
compact, and the side projection is continuous.  Non-overlap is a closed condition because the
interior of a parametrised square is exactly the open `u/v` box (`mem_interior_iff_uv`).

**For any `n`.**  Nothing about `11` is used beyond finiteness; the same proof gives attainment
of `s(n)` for every `n`.
-/

namespace PackingCert.S11

/-- **Attainment.**  `{s | Fits 11 s}` has a least element. -/
theorem attainment : ∃ m, IsLeast {s : ℝ | Fits 11 s} m := attained_thm

#print axioms attainment

end PackingCert.S11
