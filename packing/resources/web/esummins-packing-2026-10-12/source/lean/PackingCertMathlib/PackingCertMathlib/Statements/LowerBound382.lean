import PackingCertMathlib.Measure382

/-!
# Theorem 1 — `s(11) ≥ 3.82`, end to end

**What it says.**  No eleven closed unit squares with pairwise disjoint interiors fit in a
square of side below `3.82 = 191/50`.  (The published bound before this lab was `3.7889`.)

**Why it matters.**  It is the lower end of the window `[3.82, ŝ]` on which every per-class
obligation of the optimality proof is stated: the census of skeletons is one object on `(3, 4)`,
and the certificate campaigns only ever have to cover `[3.82, ŝ]`.

**How it is proved** (`MeasureBridge.lean` + `Measure382.lean`, A64).  A07's LP measure
certificate `certs/measure_certificate_3.82.json` (atoms with weights; total mass below 11)
is replayed by the exact integer checker `checkMeasureI` under `native_decide`; the
formalised soundness bridge — exact `Int`-interval arithmetic, rational grid trigonometry,
the clip via quasiconcavity of `w = cos + sin`, the sift/split/branch-and-bound induction,
coverage, and the scaling/shrinking + counting argument — turns the `Bool` verdict into this
statement about real packings.

**For any `n`.**  The bridge is stated for a general atom list and a general `n`; only the
certificate is specific to `n = 11` and side `3.82`.
-/

namespace PackingCert.S11

/-- **Theorem 1.**  Eleven unit squares need side at least `3.82`. -/
theorem lower_bound_382 : ∀ s : ℝ, Fits 11 s → (191 / 50 : ℝ) ≤ s := s_eleven_ge_382

#print axioms lower_bound_382

end PackingCert.S11
