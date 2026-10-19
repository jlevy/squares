import PackingCertMathlib.TopLevel

/-!
# The rigidity basin at Trump's configuration (A22 + A36)

**What it says.**  Inside the box of radius `rBasin = 3/2000` (∞-norm, all 33 coordinates
`(cx, cy, t)`) around `ẑ`: every packing has side `≥ ŝ`, and a packing at side exactly `ŝ` IS
`ẑ`.

**Why it matters.**  It is the last step of both clauses of the theorem.  The lower bound needs
"no packing near Trump at a side below `ŝ`"; uniqueness needs "a packing at `ŝ` near Trump is
Trump".  Every residual tree (trump5, and each class tree's (D) leaves) only has to LAND in this
box, or in the tube of `Statements/Tube.lean`, which hands over to the same theorem.

**How it is proved** (`Rigidity.lean`, `RigidBasin*.lean`, A79; prose
`docs/proofs/theta_t_transfer.md`, `attempts/A22-local-rigidity/`, `attempts/A36-*`).  A36's
UNIVERSAL basin certificate `G3_UNIVERSAL` at radius `3689/10⁶` in the θ frame — the (V′) chain
(a certified descent direction on every face of the box) — composed with A22 §5's Farkas
optimality at the handover radius, and the exact θ ↔ t transfer (`ThetaT.lean`: `|Δθ| ≤ 2|Δt|`,
corner motion `≤ r_c + √2·r_t`), whose slab gate `(3/2000)(1 + √2) < 3689/10⁶` is machine-checked.
`ẑ` itself is the unique zero of A22's contact system in `box(z0, 1e-50)` (Krawczyk, replayed by
`native_decide`), and its side is `ŝ` by the CIDL identity — so the ONLY assumption left is
`a22_exact_structure` (`Statements/Open/A22ExactStructure.lean`).
-/

namespace PackingCert.S11

/-- **The basin theorem.** -/
theorem rigidity_basin : ∀ z : Cfg, InBasin z →
    (∀ s : ℝ, CfgPacking s z → shat ≤ s) ∧ (CfgPacking shat z → z = zhat) :=
  basin

/-- Trump's configuration is a packing at side `ŝ`. -/
theorem trump_packs : CfgPacking shat zhat := trump_packs_at_shat

#print axioms rigidity_basin
#print axioms trump_packs

end PackingCert.S11
