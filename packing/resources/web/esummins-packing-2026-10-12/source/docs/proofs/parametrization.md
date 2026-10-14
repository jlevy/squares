# The parametrisation lemma (A64, depgraph node A.PARAM)

Target: the `parametrize` axiom of `lean/PackingCertMathlib/PackingCertMathlib/TopLevel.lean`
— "every set-level packing is represented by a configuration `(cx, cy, t)`, `t ∈ [0,1]`" —
stated in the headers of `certs/verify_measure.py` and `lean/PackingCert/PackingCert/
MeasureInt.lean` and load-bearing for EVERY certificate family (each quantifies over exactly
this domain), but never written out.  Status after A64: **proved in prose here AND in Lean**
(`lean/PackingCertMathlib/PackingCertMathlib/Parametrize.lean`; the packing-level theorem
`parametrize` in `TopLevel.lean` is now a theorem — the axiom is discharged).
Labels: [T] proved, [D] definition, [R] remark.

## 0 [D] The objects

A **closed unit square** (`IsUnitSquare`, `Bridge.lean`) is a set of the form

    sqSet p₀ e = { p₀ + a·e + b·e⊥ : (a, b) ∈ [0,1]² },   e a unit vector,

where `e⊥ = (−e₂, e₁)`; `(a,b) ↦ p₀ + a·e + b·e⊥` is a Euclidean isometry (`aff_sqdist`), so
these are exactly the congruent copies of `[0,1]²` given by an oriented base corner and edge.

A **parametrised square** (`PSq`) is a triple `(cx, cy, t)` denoting the closed unit square
with centre `(cx, cy)` and edge direction `(cos θ, sin θ)`, `t = tan(θ/2)`, via the rational
functions

    cos θ = (1 − t²)/(1 + t²),    sin θ = 2t/(1 + t²)      (`cosT`, `sinT`),

realised as `sqSet (baseCorner) (edir)` with `baseCorner = centre − (e + e⊥)/2`.  Note
`cosT t² + sinT t² = 1` is a polynomial identity valid for EVERY real `t` — no trigonometry
enters anywhere in this file.

**Lemma (A.PARAM, single square).** *Every closed unit square `S` equals `PSq.set (cx,cy,t)`
for some `(cx, cy, t)` with `t ∈ [0, 1]`.*

**Corollary (A.PARAM, packing form = the Lean axiom).** *If `(Q_i)_{i<n}` is a packing (each
`Q_i` a closed unit square), there is a configuration `z : Fin n → PSq` with `t_i ∈ [0,1]` and
`Q_i = (z_i).set` for all `i`.*  (Apply the lemma to each square and choose; only the
`unit` field of `IsPacking` is used.)

## 1 [T] Step 1 — the square's own 90° symmetry brings the edge into the first quadrant

For any `p₀, e` (no unit hypothesis needed):

    sqSet (p₀ + e) (e⊥) = sqSet p₀ e                                   (`sqSet_rot`)

*Proof.* `p₀ + e + a·e⊥ + b·(e⊥)⊥ = p₀ + (1−b)·e + a·e⊥` since `(e⊥)⊥ = −e`; the parameter
map `(a, b) ↦ (1−b, a)` is a bijection of `[0,1]²`.  ∎

The four vectors `e, e⊥, e⊥⊥ = −e, e⊥⊥⊥` are the successive 90° rotations of `e`, and
`|e⊥| = |e|`.  The four closed quadrants cover the plane, so **some** rotation of `e` has both
components ≥ 0 (explicitly: if `e₁ ≥ 0 ≥ e₂` take `e⊥ = (−e₂, e₁)`; if `e₁, e₂ ≤ 0` take
`−e`; if `e₂ ≥ 0 ≥ e₁` take `(e₂, −e₁)`).  Iterating `sqSet_rot` accordingly:

**Step-1 conclusion** (`exists_nonneg_dir`): every closed unit square has a representation
`sqSet p₀ e` with `e` a unit vector, `e₁ ≥ 0`, `e₂ ≥ 0` — i.e. `θ ∈ [0°, 90°]`.

[R] This is the square's OWN symmetry group (rotation of the description by 90° about the
square's centre), NOT the container's D4 — the lemma needs no container at all, which is why
`parametrize` can be stated for a single square and used by the measure bridge before any
packing structure exists.  `θ ∈ [0°, 90°]` closed at both ends means the representation is
not unique (`t = 0` and `t = 1` denote the same axis-parallel square — findings F8); the
certificates only need existence.

## 2 [T] Step 2 — the half-angle substitution is exact algebra

Let `e` be a unit vector with `e₁, e₂ ≥ 0` and put

    t := e₂ / (1 + e₁)     (well-defined: e₁ ≥ 0 ⇒ 1 + e₁ ≥ 1 > 0).

Then, writing `N := (1+e₁)² `:

* `1 + t² = ((1+e₁)² + e₂²)/N = (2 + 2e₁)/N = 2/(1+e₁)` — using `e₁² + e₂² = 1`;
* `1 − t² = ((1+e₁)² − e₂²)/N = (2e₁ + 2e₁²)/N = 2e₁/(1+e₁)`;

hence

    cosT t = (1 − t²)/(1 + t²) = e₁,        sinT t = 2t/(1 + t²) = e₂,

and `t ∈ [0, 1]`: `t ≥ 0` is clear, and `t ≤ 1 ⟺ e₂ ≤ 1 + e₁`, true because `e₂ ≤ 1`
(unit vector) and `e₁ ≥ 0`.  (This is of course `t = tan(θ/2)` by the half-angle formulas,
but the proof never says so: it is four polynomial identities in `(e₁, e₂)` modulo
`e₁² + e₂² = 1`.)  ∎  (`halfAngle_denom/num`, `cosT_halfAngle`, `sinT_halfAngle`,
`halfAngle_mem_Icc`.)

## 3 [T] Step 3 — reading off the centre

Given `S = sqSet p₀ e` from Step 1 and `t` from Step 2, set

    cx := p₀x + (e₁ − e₂)/2,    cy := p₀y + (e₁ + e₂)/2.

Then `baseCorner (cx, cy, t) = (cx − (cosT t − sinT t)/2, cy − (cosT t + sinT t)/2) = p₀`
and `edir (cx, cy, t) = (cosT t, sinT t) = e`, so `PSq.set (cx, cy, t) = sqSet p₀ e = S`.  ∎
(`isUnitSquare_exists_psq`.)

## 4 [R] What the Lean file also provides (inputs to the measure bridge A.F2)

Formalised alongside, because the measure-checker soundness proof consumes them and they are
the same orthonormal-basis computation:

* `mem_sqSet_iff_coords` / `mem_set_iff_uv`: for unit `e`, `p ∈ Q(c, t) ⟺ |u| ≤ ½ ∧ |v| ≤ ½`
  with `u = e·(p−c)`, `v = e⊥·(p−c)` — the verifiers' membership predicate;
* `set_subset_container_iff`: for `t ∈ [0,1]`, `Q ⊆ [0,s]² ⟺ w/2 ≤ cx, cy ≤ s − w/2` with
  `w = cosT t + sinT t` — the verifiers' containment predicate (uses `cos, sin ≥ 0`, i.e.
  Step 1's quadrant);
* `wT_ge_one` (`w ≥ 1` on `[0,1]`: `cos + sin ≥ cos² + sin² = 1`) — the root-box argument;
* `wT_ge_min` (quasiconcavity of `w` on sub-intervals of `[0,1]`) — the clipping step.
  Key identity: `w(b) − w(a) = 2(a−b)(a + b + ab − 1)/((1+a²)(1+b²))`, so the superlevel
  sets of `w` are intervals and `min` over `[t₀,t₁]` is at an endpoint.

## 5 [R] Status ledger

* Lean: `parametrize` is a THEOREM (`TopLevel.lean`, axioms only
  `propext, Classical.choice, Quot.sound`); axiom roster 13 → 12.
* The configuration layer (`cosT … PSq.set`) moved from `TopLevel.lean` to
  `Parametrize.lean` verbatim (same namespace `PackingCert.S11`); no statement changed.
* Depgraph: A.PARAM → lean-proved.
