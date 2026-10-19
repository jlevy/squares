import PackingCertMathlib.TopLevel

/-!
# -- OPEN: `trump_residual` — Trump's class lands in the rigidity basin

**What it asserts.**  Every packing in Trump's stratum (`k = 5`, `((2,1),(1),(1),∅)` up to D4)
at a side `s ∈ [3.82, ŝ]` is, after a container symmetry and a relabelling, a packing lying in
the basin box `InBasin` (all 33 coordinates within `3/2000` of `ẑ`), where the basin theorem
(`Statements/Basin.lean`) finishes: side `≥ ŝ`, and `= ẑ` at `ŝ`.

**Where the proof lives.**  A60's residual tree at `s₀` (zone cover + residue ladders +
confinement, every kill an exact certificate) and A212's trump5 tree — A211's coarse tree with
the Trump-containment gate and the TUBE LEAF (`attempts/A212-trump5-tree/notes/trump5_tree.md`
§2, `Statements/Open/TubeLeaf.lean`): a fully named pad-0 node whose pieces lie within the tube
radii of `g·ẑ` hands over to Theorem T1 (`Statements/Tube.lean`) on the scale-ray tube
`certs/tube_scale_T5.71e-2_window.json`, which reaches the whole window `[3.82, ŝ]`.  With the
tube the basin box of this axiom is no longer the landing target: `Composition.lean`'s
`classKilledAt_of_tree` consumes the tree directly (`ClassKilledAt trumpStratum m`).
Prose: `docs/proofs/contraction_tube.md` §4 (Lemma SEAM), `unique_transfer.md` §3.

**Status (2026-09-14).**  OPEN — A212's tree running; declared in `TopLevel.lean`, restated
here only for `#print axioms`.
-/

namespace PackingCert.S11.OpenLemmas

/-- **[OPEN] trump5 residual** — a restatement of the axiom `trump_residual`. -/
theorem trump_residual_open : ∀ s ∈ wnd, ∀ z : Cfg, CfgPacking s z →
    InStratum trumpStratum s z →
    ∃ (z' : Cfg) (f : RP → RP) (e : Equiv.Perm (Fin 11)),
      IsCtrSym s f ∧ CfgPacking s z' ∧ InBasin z' ∧ ∀ j, (z (e j)).set = f '' (z' j).set :=
  trump_residual

#print axioms trump_residual_open

end PackingCert.S11.OpenLemmas
