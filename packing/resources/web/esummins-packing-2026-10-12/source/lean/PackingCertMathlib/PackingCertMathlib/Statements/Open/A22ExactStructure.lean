import PackingCertMathlib.TopLevel

/-!
# -- OPEN (certified outside Lean): `a22_exact_structure` — A22's content at `ẑ`

**What it asserts.**  Three facts about the Lean-defined `ẑ` (`Rigidity.lean`, the unique zero
of A22's 34-row contact system in `box(z0, 1e-50)`): (1) the common tilt of squares 6–10 has
`t̂ = tan(θ̂/2) ∈ [3/10, 2/5]`; (2) the intrinsic side `ŝ_A22` lies in the octic's isolating
interval `[3.877083, 3.877084]`; (3) the 13 reduced contact-row generators `Cidl.gens` vanish at
the 13-coordinate point `(t̂, y₄, x₆, y₆, …, x₁₀, y₁₀, ŝ_A22)` of `ẑ`.  Nothing algebraic is
assumed: the ideal-membership identity `e(t)·Δ(t)⁸·octic(S) = Σ q_j·G_j` and its sign gates
are machine-checked (`CidlCheck.lean`, `native_decide` over ℚ), so with this axiom
`ŝ_A22 = ŝ` is a THEOREM (`shatA22_eq_shat`).

**Where the certificate lives.**  `attempts/A22-local-rigidity/notes.md` (headline items 1–3:
the Krawczyk enclosure `F̃` of `θ̂` within `1e-50` of the A03 rational angle, the side within
`1e-50` of the A03 rational side, all 38 curated rows vanishing at `ẑ`), the exact-rational
re-check `a22_recheck_exact.py` (A70), and `certs/verify_cidl.py` (the generators, rebuilt
byte-for-byte in `CidlGen.lean`).  Prose: `docs/proofs/attainment_ub.md` §7.5.

**Status (2026-09-14).**  Certified by mpmath.iv Krawczyk + the exact re-check; not yet a Lean
theorem — its content is within reach of `Rigidity.lean`'s witness lemmas (the tilt and side
enclosures are read off the replayed box; the row-vanishing needs the contact rows evaluated
at the Lean `ẑ`).  Declared in `TopLevel.lean`; restated here for `#print axioms`.
-/

namespace PackingCert.S11.OpenLemmas

open Set

/-- **[OPEN] A22's exact structure at `ẑ`** — a restatement of the axiom
`a22_exact_structure`. -/
theorem a22_exact_structure_open :
    (zhat 6).t ∈ Icc (3 / 10 : ℝ) (2 / 5) ∧
      shatA22 ∈ Icc (3877083 / 1000000 : ℝ) (3877084 / 1000000) ∧
      ∀ g ∈ Cidl.gens, Cidl.eval g
        (Cidl.pt13 (zhat 6).t (zhat 4).cy (zhat 6).cx (zhat 6).cy (zhat 7).cx (zhat 7).cy
          (zhat 8).cx (zhat 8).cy (zhat 9).cx (zhat 9).cy (zhat 10).cx (zhat 10).cy
          shatA22) = 0 :=
  a22_exact_structure

#print axioms a22_exact_structure_open

end PackingCert.S11.OpenLemmas
