import PackingCertMathlib.TopLevel

/-!
# Eleven unit squares — the top-level statement (A216, 2026-09-14)

**In plain language.**  Every packing of eleven unit squares needs a square container of side
at least `ŝ = 3.877083590022813…` (the second real root of Trump's octic
`x⁸ − 20x⁷ + 178x⁶ − 842x⁵ + 1923x⁴ − 496x³ − 6754x² + 12420x − 6865`), and at side exactly
`ŝ` the only packing is Trump's configuration, up to a symmetry of the container and a
relabelling of the squares.

**What this file is.**  Nothing is proved here.  The three theorems below are the theorems
`s_eleven_ge / s_eleven_eq / s_eleven_unique` of `TopLevel.lean` under readable names, and the
`#print axioms` commands at the bottom list exactly what they rest on.  The rule for reading
that list: Lean's three standard axioms (`propext`, `Classical.choice`, `Quot.sound`) and the
`native_decide` evaluation axiom (`Lean.ofReduceBool`, the compiled `Bool` checkers replayed on
certificate files) are the trusted base; everything else is a named leaf of the proof plan that
still lives in prose or in certificate files — listed in *What you must believe*.

**The words.**  `Fits n s` (`Parametrize.lean`): some family of `n` closed unit squares with
pairwise disjoint interiors lies in `[0,s]²`.  `sPack n = sInf {s | Fits n s}` is `s(n)`.
`shat` is the unique root of `trumpOctic` in `[3.877083, 3.877084]` (`TopLevel.lean`).  `zhat`
is Trump's configuration — the unique zero of A22's contact system, a Lean definition since
A79 (`Rigidity.lean`).  `IsCtrSym s f`: an isometry of the plane mapping `[0,s]²` onto itself.
One small file per key result of the proof lives in `Statements/`; the obligations that are
not yet Lean theorems are stated as named axioms in `Statements/Open/`; `lean/AUDIT.md` (from
`lean/audit.py`) tabulates every statement with the axioms it depends on.
-/

namespace PackingCert.S11

/-- **Lower bound.**  No eleven unit squares pack into a square of side below `ŝ`. -/
theorem main_lower_bound : ∀ s : ℝ, Fits 11 s → shat ≤ s := s_eleven_ge

/-- **The value.**  `s(11) = ŝ`. -/
theorem main_value : sPack 11 = shat := s_eleven_eq

/-- **Uniqueness.**  Every packing at side `ŝ` is Trump's configuration up to a container
symmetry and a relabelling. -/
theorem main_uniqueness : ∀ Q : Fin 11 → Set RP, IsPacking 11 shat Q →
    ∃ (f : RP → RP) (e : Equiv.Perm (Fin 11)),
      IsCtrSym shat f ∧ ∀ i, Q i = f '' (zhat (e i)).set := s_eleven_unique

/-! ## What you must believe

Beyond `propext`, `Classical.choice`, `Quot.sound` and `Lean.ofReduceBool`, the three theorems
depend on exactly three named axioms (`TopLevel.lean`; readable copies in `Statements/Open/`):

* `stratum_kill` — no packing at any side `s ∈ [3.82, ŝ]` has skeleton exactly of a non-Trump
  census class (163 classes, 162 of them here).  Prose/certificates: the class trees and slab
  kills of A57/A60/A86/A93 and the shadow-tree campaigns A180–A215 (`docs/proofs/k0_route.md`,
  `k0_blocked_side.md`, `instratum_bridge.md`, `unique_transfer.md`; `Composition.lean`
  reduces it to per-class `ClassKilledAt` obligations).  Status: OPEN — the residue map
  `docs/residue_map/current/` lists the classes still alive.
* `trump_residual` — every packing in Trump's class at a side in `[3.82, ŝ]` lands, after a
  container symmetry and a relabelling, in the rigidity basin of `zhat`.  Prose/certificates:
  A60's residual tree, A212's trump5 tree with the tube leaf (`attempts/A212-trump5-tree/notes/
  trump5_tree.md`, `docs/proofs/contraction_tube.md`).  Status: OPEN (tree running).
* `a22_exact_structure` — A22's certified content on the exact-structure slice of `zhat`: the
  tilt of squares 6–10 is in `[3/10, 2/5]`, the side is in the octic's isolating interval, and
  the 13 reduced contact rows vanish at `zhat`.  Certificate: `attempts/A22-local-rigidity/`,
  `certs/verify_cidl.py`, exact re-check `a22_recheck_exact.py`
  (`docs/proofs/attainment_ub.md` §7.5).  Status: certified outside Lean; within reach of
  `Rigidity.lean`'s witness lemmas.

`Lean.ofReduceBool` enters through `lb_382` (`checkMeasureI` on
`certs/measure_certificate_3.82.json`), the A22/A36 replays (`checkA22`, `checkA36`) and the
CIDL identity (`CidlCheck.lean`); the compiled checkers are the same `Bool` functions whose
soundness is proved in `MeasureBridge.lean`, `CaseBridge.lean`, `Rigid*.lean`.
-/

#print axioms main_lower_bound
#print axioms main_value
#print axioms main_uniqueness

end PackingCert.S11
