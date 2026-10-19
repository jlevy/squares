# Theorem (A28.★, advisor proof, 2026-08-21)

For all unit vectors u, e in R²:  |u·e| + |u·e⊥| + ‖u‖₁‖e‖₁ ≥ 2‖u‖₁,
with equality iff e is axis-aligned (θ ∈ {0°,90°} mod 90°) or u = ±e, ±e⊥ with ‖e‖₁ = 1.

Consequence (sharp band lemma): two unit squares fit in a square of side B only if B ≥ 2 = s(2);
hence at most ONE of the 11 squares avoids the width-w boundary band whenever w > (s−2)/2 —
w* = 0.92 at s = 3.84, 0.9385 at s′, valid for EVERY s < 4 (A26.1 gave w = 1, s < 3.9142 only).

## Proof

**Reduction.** All three terms are invariant under (i) u → −u, (ii) e → −e, (iii) e → e⊥
(which swaps |u·e| ↔ |u·e⊥| and preserves ‖e‖₁), and (iv) the simultaneous action of the
dihedral group of the square on both u and e. Using (iv) reduce u's angle φ to [0, π/2)
(rotate both by a multiple of 90°, flip signs via (i)); then use (ii)+(iii) to reduce e's angle
θ to [0, π/2) independently. Write u = (cos φ, sin φ), e = (cos θ, sin θ), ψ = φ − θ ∈ (−π/2, π/2).
Then u·e = cos ψ ≥ 0 and u·e⊥ = sin ψ, so |u·e| + |u·e⊥| = cos ψ + |sin ψ|.
Put a = cos φ + sin φ = ‖u‖₁, b = cos θ + sin θ = ‖e‖₁.

**Branch 1 (φ ≥ θ).** Direct expansion of cos ψ + sin ψ = a cos θ + (sin φ − cos φ) sin θ gives

  LHS − RHS = 2·f(φ),  f(φ) := sin φ·(b − 1) − cos φ·(1 − cos θ).

If θ = 0 then f ≡ 0 (equality family). Else b − 1 > 0. If cos φ = 0, f = b − 1 ≥ 0. Otherwise
f ≥ 0 ⟺ tan φ ≥ (1 − cos θ)/(b − 1); since φ ≥ θ it suffices that
tan θ·(b − 1) ≥ 1 − cos θ, i.e. sin θ(cos θ + sin θ − 1) ≥ cos θ(1 − cos θ), i.e.

  1 + sin θ cos θ − sin θ − cos θ ≥ 0 ⟺ (1 − sin θ)(1 − cos θ) ≥ 0.  ∎(branch 1)

**Branch 2 (φ ≤ θ).** Expansion of cos(−ψ) + sin(−ψ) = cos φ·b + sin φ(sin θ − cos θ) gives

  LHS − RHS = 2·g(φ),  g(φ) := cos φ·(b − 1) − sin φ·(1 − sin θ).

If θ = π/2 then b − 1 = 0 = 1 − sin θ, g ≡ 0 (equality family). Else g ≥ 0 ⟺
tan φ ≤ (b − 1)/(1 − sin θ); since φ ≤ θ it suffices that tan θ(1 − sin θ) ≤ b − 1, i.e.
cos θ(cos θ + sin θ − 1) ≥ sin θ(1 − sin θ), which is the SAME identity
(1 − sin θ)(1 − cos θ) ≥ 0.  ∎

**Verification (2026-08-21, advisor):** 200,000 random directions: min LHS−RHS = +3.4e-7 (at
near-equality points); branch decomposition matches the original expression to 7e-16; the key
identity to 2e-16. Status: rigorous human proof; Lean formalisation pending (the two-branch
reduction makes it nlinarith-friendly; needs Mathlib, blocked on ~10 GB disk at the moment).
