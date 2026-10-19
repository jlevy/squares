import PackingCertMathlib.Parametrize

/-!
# Parametrisation — every packing is a configuration of 33 real coordinates

**What it says.**  Every closed unit square in the plane is `PSq.set ⟨cx, cy, t⟩` for a centre
`(cx, cy)` and a half-angle tangent `t = tan(θ/2) ∈ [0, 1]`; hence every set-level packing
`Q : Fin n → Set RP` is the image of a configuration `z : Fin n → PSq` with all tilts in `[0,1]`.

**Why it matters.**  It is the bridge from the set-level definition of "packing" (the one in
`Fits`, hence in the top-level theorem) to the coordinate world in which every certificate
speaks — 33 numbers for eleven squares, with `cos θ = (1−t²)/(1+t²)`, `sin θ = 2t/(1+t²)` rational
in `t`.  No transcendental function is needed anywhere downstream.

**How it is proved** (`Parametrize.lean`, A64; prose `docs/proofs/parametrization.md`).  The
square's own 90° symmetry (`sqSet_rot`) brings its edge vector into the closed first quadrant;
the half-angle substitution `t = e₂/(1 + e₁)` is exact polynomial algebra.  Only the `unit` field
of `IsPacking` is used.

**For any `n`.**  Stated and proved for every `n`.
-/

namespace PackingCert.S11

open Set

/-- **Parametrisation.**  Every packing of `n` unit squares is a configuration with tilts in
`[0,1]`. -/
theorem parametrization : ∀ {n : ℕ} {s : ℝ} (Q : Fin n → Set RP), IsPacking n s Q →
    ∃ z : Fin n → PSq, (∀ i, (z i).t ∈ Icc (0 : ℝ) 1) ∧ ∀ i, Q i = (z i).set :=
  parametrize

#print axioms parametrization

end PackingCert.S11
