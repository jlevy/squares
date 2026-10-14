# θ ↔ t coordinate transfer and a concrete rBasin (F5 discharge) — A63, 2026-09-01

Target: A62 finding F5. The rigidity/basin certificates (A22 r_N = 5e-4, A36 h = 37/10000 =
3.7e-3) are ∞-norm boxes in (c, θ, s) — raw angles; the composition's configuration space,
every case/parametric certificate, and `TopLevel.lean` use t = tan(θ/2) ∈ [0, 1]. Radii do not
transfer verbatim (dθ/dt = 2/(1+t²) ≠ 1). This file proves the exact transfer constants and
derives a concrete, sound value for the Lean `rBasin`. Labels: [T] proved, [M] computed exact.

## X.1 [T] Global Lipschitz constants on t ∈ [0, 1] (θ ∈ [0, π/2])

θ(t) = 2 arctan t, t(θ) = tan(θ/2); both strictly increasing bijections [0,1] ↔ [0, π/2].
dθ/dt = 2/(1+t²) ∈ [1, 2] on [0, 1]; dt/dθ = (1+t²)/2 ∈ [1/2, 1]. Hence for t₁, t₂ ∈ [0, 1]
with θᵢ = θ(tᵢ) (mean value theorem, or the arctan subtraction identity
arctan a − arctan b = arctan((a−b)/(1+ab)) with 1 ≤ 1+ab ≤ 2 and x/2 ≤ arctan x ≤ x on [0,1]):

  |t₁ − t₂| ≤ |θ₁ − θ₂| ≤ 2·|t₁ − t₂|,  equivalently  ½|θ₁ − θ₂| ≤ |t₁ − t₂| ≤ |θ₁ − θ₂|.

On a subinterval [t_lo, t_hi] the sharp factor interval for dθ/dt is
[2/(1+t_hi²), 2/(1+t_lo²)] (exact rationals for rational endpoints). At Trump's tilt
(t̂ ≈ 0.3655, θ̂ ≈ 40.18°): dθ/dt ∈ [1.759, 1.771] on t ∈ [0.36, 0.37] — the "≈ 1.77" of the
findings, now bounded exactly on a rational bracket.

**Transfer rules** (all directions the lab needs):
* a t-box of radius r_t around t̂ = tan(θ̂/2) maps INTO the θ-box of radius 2·r_t around θ̂;
* a θ-box of radius r_θ around θ̂ maps INTO the t-box of radius r_θ around t̂ (contraction);
* a θ-certificate consumed by t-world clients may quote radius r_t = r_θ/2 (sound, factor-2
  loss); a t-certificate consumed by θ-world clients may quote r_θ = r_t (no loss).
Centre alignment is by definition (t̂ := tan(θ̂/2)); certificates using rational approximations
of t̂ or θ̂ must add their rounding radius to the deviation before applying the rules.

## X.2 [T] Corner-perturbation lemma (needed for the s-slab case of `basin`)

For a square with centre c, angle θ, each corner is c + R(θ)v, |v| = √2/2. If |Δc_x|, |Δc_y| ≤
r_c and |Δθ| ≤ r_θ then every corner coordinate moves by at most r_c + (√2/2)·r_θ. In
particular, for a configuration z with |c − ĉ|∞ ≤ r and |t − t̂|∞ ≤ r (hence |Δθ| ≤ 2r by X.1):

  every corner coordinate of z is within r·(1 + √2) of the corresponding corner of ẑ.

Since ẑ's squares touch all four walls of [0, ŝ]² (max corner-x = ŝ, etc.), any container
[0, s]² for z must have  s ≥ ŝ − r(1 + √2).

## X.3 [T+M] A concrete rBasin: **rBasin = 3/2000 = 1.5e-3**

Claim: with rBasin = 3/2000, the Lean axiom `basin` is exactly what A36's certified theorem
(σ ≥ ŝ on the 34-dim ∞-box of radius h = 37/10000 around (ẑ, ŝ) in (c, θ, s), equality iff
(ẑ, ŝ)) asserts, transferred to the (c, t)-world. Two conditions, both checked exactly:

* **(a) tilt transfer:** t-deviation ≤ rBasin ⇒ θ-deviation ≤ 2·rBasin = 3/1000 ≤ 37/10000. ✓
* **(b) s-slab closure:** the axiom quantifies over ALL s with `CfgPacking s z`. For s ≥ ŝ the
  first clause is trivial. For s < ŝ, X.2 gives s ≥ ŝ − rBasin(1+√2), and exactly
  (3/2000)·(1+√2) < (3/2000)·(24143/10000) = 72429/20000000 < 37/10000, so
  |s − ŝ| ≤ h and the 34-dim point (z, s) lies in A36's box; A36's σ ≥ ŝ (with feasibility =
  containment in [0, s]², the A22 row semantics) forbids s < ŝ. The second clause (s = ŝ,
  equality iff ẑ) is the box's equality clause at the centre slab. ✓

So `rBasin` is DEFINABLE (A63 makes it a Lean definition, removing one axiom); the `basin`
axiom remains an axiom but now asserts A36's theorem verbatim-after-transfer, with the
transfer's two conditions proved here. Slack ledger: (b) is binding; (a) has a 5.8e-4 reserve;
A36's certified maximum 3.779e-3 would allow rBasin up to ~1.55e-3 — 3/2000 leaves a
clean margin. The A60 residual tree's landing radius (conditioning radius 4.45e-4, level-24
boxes) sits at 0.30·rBasin — the containment obligation D.S6 is unchanged in kind but now has
a CONCRETE target box: all 33 coordinates within 3/2000 of ẑ (t-world), mod G.

## X.3½ LEAN-PROVED (A68, 2026-09-01)

`lean/PackingCertMathlib/PackingCertMathlib/ThetaT.lean` (axioms propext/Choice/Quot.sound):
`cosT_eq_cos` / `sinT_eq_sin` (the rational parametrisation IS the trigonometry of
θ(t) = 2·arctan t — the formal tie between the lab's t-world and the certificates' θ-world);
X.1 both directions (`theta_lipschitz`: |Δθ| ≤ 2|Δt| for ALL reals, arctan 1-Lipschitz by MVT;
`sub_le_theta`: |Δt| ≤ |Δθ| on [0,1], tan 2-Lipschitz on [0, π/4]); the circle bound
(Δcos)² + (Δsin)² ≤ (Δθ)² via 2 − 2cos x ≤ x²; X.2 as `corner_perturb` with the SHARP constant
r_c + (√2)·r_t — the formalisation confirms sharpness is load-bearing: the naive per-component
estimate r_c + 2·r_t gives 3r = 4.5e-3 > 3.7e-3 and does NOT close (b); and the two X.3 gates
as `TopLevel.lean` theorems `rBasin_gate_tilt` (2·rBasin ≤ 37/10000) and `rBasin_gate_slab`
(rBasin·(1+√2) < 37/10000; note (3/2000)·(1 + 22/15) = 37/10000 EXACTLY, so the gate is
equivalent to √2 < 22/15). The wall-touching step of X.3(b) (s ≥ ŝ − r(1+√2) for containers of
perturbed configurations) consumes properties of the opaque `zhat` and stays inside the `basin`
axiom's justification, its arithmetic now machine-checked.

## X.4 What this does NOT discharge (E.COORD residue, checklist F6)

* The mpmath.iv trust item: the transfer constants are exact, but A22/A36's own interval
  evaluations remain Python-interval-certified. The cure is still the t-reparametrised
  re-emission (cos θ = (1−t²)/(1+t²), sin θ = 2t/(1+t²) — rational trig, the measure-checker
  trick), which would make the rigidity chain Lean-replayable AND coordinate-native; X.1's
  factor-2 loss then disappears from the trust chain. The re-emission contract: emit the
  Krawczyk/basin boxes directly as t-boxes of radius ≥ rBasin·(safety), with X.1 needed only
  for the historical cross-check.
* The basin-boundary/collar questions (A35/A36 G1) and everything in D.TREE/D.SLAB.
