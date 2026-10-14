import PackingCertMathlib.Statements.Open.NoFloat2

/-!
# -- OPEN: the NEST residual of NO-FLOAT2 — A279

`docs/proofs/nest_residual.md` (derivation in `attempts/A279-nest-residual/notes/nest279_part0..N.md`).  Setting as in
`NoFloat2.lean`: BL corner, box `B = (0,1)²`, floaters `C` (upper-left) and `D` (lower-right) meeting `B`, blockers
`X` (of `T_u(C)`, above-left of `C`) and `Y` (of `T_v(D)`, below-right of `D`).  Separator ARCS: `α ∈ [α₋, α₊]` the
slope angles of the D → C separators, `η ∈ [η₋, η₊]` of the Y → D ones, `ξ ∈ [ξ₋, ξ₊]` of the X → C ones.  (NEST) is
`η₊ < α₋ ≤ α₊ < ξ₋` — the condition under which SWEEP (A278 Lemma 2.3) lands neither floater.

**Theorems here (any `n`, any `s`; arithmetic cores of `nest_residual.md` parts 2–3).**
* `nest_not_both_edges` [T] (part 2.2): D's two parallel edges (slope angle `θ_D`) cannot both be separators —
  `η₊ ≥ θ_D` (Y beyond the lower-right edge line) and `α₋ ≤ θ_D` (C beyond the upper-left edge line) contradict (NEST).
* `sigma_core` [T] (part 3.1, (Σ)): inscribed-disc centres on opposite sides of a separator are ≥ 1 apart across it;
  adding the C|D and D|Y separations and using `m_C,y < 1 + r` (C reaches below height 1; `r = w_C/2 ≤ 1/√2`) and
  `m_Y,y ≥ 1/2` (Y touches the floor) gives the horizontal budget
  `(m_Y,x − m_C,x) tan η + (m_D,x − m_C,x)(tan α − tan η) > sec α + sec η − 1/2 − r`: shallow nests are impossible.
* `flat_c_core` [T] (part 3.3): a FLAT `C` at height `y₀ < 1` forces D's left vertex under C's bottom edge, so
  `h_v(D) < 1 − cos θ_D` and `(1 − h_u(D)) tan θ_D < 1 − cos θ_D`.
* `sigma_prime_low` [T] (part 3.2): `h_v(D) ≥ w_Y − (t_Y,x − x_b) tan η` from the Y|D separation of D's bottom vertex
  and Y's top vertex.

**What is not.**  `NestSubResidual` (the sub-residual of L satisfying (NEST)) is opaque; that a residual point whose sweep
region holds no fifth square satisfies (NEST) is A278 part 6 [T-prose] and is not re-axiomatised here; whether
`NestSubResidual` is empty is [C] — the search `nest279` is [M] only (see the doc).  No new axiom; `float2_local`
(NoFloat2.lean) remains the open statement.
-/

namespace PackingCert.S11.OpenLemmas.NestResidual

/-- **Part 2.2** [T]: under (NEST) `η₊ < α₋`, D's lower-right edge line and upper-left edge line (both of slope angle
`θ`) are not both separators. -/
theorem nest_not_both_edges (ηp αm θ : ℝ) (hnest : ηp < αm) (hY : θ ≤ ηp) (hC : αm ≤ θ) : False := by
  linarith

/-- **(Σ), arithmetic core** [T] (part 3.1).  Hypotheses in divided form: `hCD` is `n_α · (m_C − m_D) ≥ 1` divided by
`cos α > 0` (`sα = sec α`, `tα = tan α`), `hDY` likewise for the D|Y separator (`sη`, `tη`); `hC`: C's centre is below
`1 + r`; `hY`: Y's centre is at height ≥ 1/2. -/
theorem sigma_core (Cx Cy Dx Dy Yx Yy sα tα sη tη r : ℝ)
    (hCD : Cy - Dy ≥ sα + (Cx - Dx) * tα) (hDY : Dy - Yy ≥ sη + (Dx - Yx) * tη)
    (hC : Cy < 1 + r) (hY : Yy ≥ 1 / 2) :
    (Yx - Cx) * tη + (Dx - Cx) * (tα - tη) > sα + sη - 1 / 2 - r := by
  nlinarith [hCD, hDY, hC, hY]

/-- **FLAT C, core** [T] (part 3.3): D's left vertex `(h_u, y_L)` pokes under C's flat bottom edge at height `y₀ < 1`
(`hL : y_L < y₀`, `hexit : (1 − h_u) tan θ ≤ y₀ − y_L`), and `y_L = h_v + cos θ` with `h_v ≥ 0`. -/
theorem flat_c_core (hu hv yL y0 tθ cθ : ℝ) (hyL : yL = hv + cθ) (hy0 : y0 < 1) (hL : yL < y0)
    (hexit : (1 - hu) * tθ ≤ y0 - yL) (hhv : 0 ≤ hv) :
    hv < 1 - cθ ∧ (1 - hu) * tθ < 1 - cθ := by
  constructor <;> linarith

/-- **(Σ′), the lower bound on D's height** [T] (part 3.2): the Y|D separation of D's bottom vertex `(x_b, h_v)` and
Y's top vertex `(t_x, w_Y)`, divided by `cos η > 0`: `h_v − w_Y ≥ (x_b − t_x) tan η`. -/
theorem sigma_prime_low (hv wY xb tx tη : ℝ) (h : hv - wY ≥ (xb - tx) * tη) :
    hv ≥ wY - (tx - xb) * tη := by
  linarith

/-- The NEST sub-residual of L (part 1): opaque. -/
opaque NestSubResidual : Prop

#print axioms nest_not_both_edges
#print axioms sigma_core
#print axioms flat_c_core
#print axioms sigma_prime_low

end PackingCert.S11.OpenLemmas.NestResidual
