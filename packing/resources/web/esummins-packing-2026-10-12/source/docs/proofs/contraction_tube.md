# The contraction tube: an anisotropic basin along the dilation ray — A83, 2026-09-03

PI idea (2026-09-03): grow Trump's certified basin SELECTIVELY toward the smaller-side
configurations that regime 2 of the seam needs — the contracted Trump configurations
ẑ − t·ĉ/ŝ — because contraction COMPRESSES every contact instead of breaking one, so the
basin should reach far beyond its isotropic radius in that direction.  This file states and
proves the tube theorem (T1), the compression lemma (§2), Lemma SEAM with the exact
side-to-depth map (§4), and records the measured (T, r) curve and its wall (§3).  Labels:
[T] proved, [M] computed exact (stdlib rationals, `certs/verify_tube.py`), [F] finding.
Lean-readiness note: `lean/tube_obligation_A83.md`.

Conventions.  A22's coordinates: z ∈ ℝ³⁴, z[3i..3i+2] = (cx_i, cy_i, θ_i) for squares
i = 0..10 (θ in radians), z[33] = s.  ẑ = A22's jam, z0 = its rational centre
(|ẑ − z0|∞ ≤ r0 = 10⁻⁵⁰), ŝ = ẑ_s.  *Feasible* = eleven closed unit squares with pairwise
disjoint interiors, all inside [0, z_s]² (A22's row semantics).  Rows g_k are A22's 36
contact rows and the two aux dist rows (A36 positions 44, 45); the universal barrier
ω = `G3_UNIVERSAL`'s (rows 0..35 + 44, 45; no branch rows), pins P = A22's S, Y = A22's Y.

## 0. Verdict

> **Tube theorem certified, exact, 12 certificates (11 tubes + the A36 universal box as
> a T = 0 regression), 289 checks, 0 failures, 10/10 corruption gates FAIL as required;
> independent Opus review (`notes/review_opus.md`): SOUND.**  Along the slot-consistent ray (trump5's pins on their slot lines,
> free squares scaled — the direction the residual tree's (D) leaves pull back to) the
> tube is certified to depth **T = 0.045** at the A60 landing radii (r_c = 1.6·10⁻³,
> r_θ = 2.1·10⁻³ rad) — 21 times A82's largest measured crossover (5·10⁻³) and 4.5 times the
> brief's target — and to **T = 0.0571 ≥ ŝ − 3.82** (the whole window) at r = 6.5·10⁻⁴.
> Along the pure scaling ray the tube reaches **T = 0.13** at the landing radii (2.3× the
> window).  The isotropic radius is unchanged from A36 (3.68·10⁻³ at T = 0; 3.5·10⁻³ at
> T = 0.02).  **Measured wall (slot ray): validity of A22 row `E3c2-7e3`** — corner 2 of
> the pinned square 3 sliding along the left edge of the free square 7 — at
> ~0.39 per unit depth; scale ray: `E7c2-9e3` (the 7–9 flush pair) at ~0.1 per unit depth.
> Seam condition (Lemma SEAM, trump5): δ_basin = min(T_tube, T_K(δ_pin)) = **0.0257 with
> δ_pin = 10⁻² slack pins** (tube 0.045; the (K)-leaf pin slack binds; 0.0457 at
> δ_pin ≥ 1.8·10⁻²) versus δ_LP: A82's near-ŝ extrapolations 1.7·10⁻³ (k4_08) / 5·10⁻³
> (k4_11) — **×5–15** — but A82's one deep point (k4_08 at ŝ − 0.044: η = −0.38,
> unconverged) says the protected classes' crossovers lie deeper than those
> extrapolations; trump5's own crossover is unmeasured (§4.2).  Protected classes: the
> tube route through s0-Theorem-U caps at T′ ≈ 3·10⁻⁴ (§4.3) — U must be re-emitted along
> the slab.  Compute obligations in §4.4.  Canary safe: ẑ − T·v violates a strictly compressed wall row
> at every certified T; ẑ is the unique equality point (A22 handover).

## 1. [T] Theorem T1 — the tube theorem and its certificate

### 1.1 The tube

Let v ∈ ℝ³⁴ be a **centre-only direction**: v_θ = 0 on every tilt, v_s = 1, v ≥ 0.  Two
instances are used:

* **scale**: v_i = ẑ_i/ŝ on every centre coordinate — the pull-back of a dilation about the
  origin (a packing at side m = ŝ − t dilated to side ŝ lands near ẑ iff the packing is
  near ẑ − t·v);
* **slot(pins)**: for the trump5 pins {0,1,2,3,5} each centre coordinate rides its slot line,
  v_i = β_i ∈ {0, 1} (slot k(s) = α + β s; A56 P1), free squares scale as above — the
  direction along which a packing at side m with its pins EXACTLY at slots(m) and its free
  squares near their dilated Trump positions moves (§4.2).

For T ≥ 0 and radii r = (r_c on centres, r_θ on tilts, r_s on s):

    Tube_v(T, r) = { ẑ − t·v + w : 0 ≤ t ≤ T, |w_i| ≤ r_i }.

It is convex (segment ⊕ box).  Its point at depth t has side coordinate ŝ − t + w_s, i.e.
Tube_v(T, r) contains, for every m ∈ [ŝ − T, ŝ], the side-m configurations obtained by
contracting ẑ along v and perturbing by w.  WLOG r_s = 0: Tube_v(T, (r_c, r_θ, r_s)) ⊆
Tube_v(T + r_s, (r_c + r_s·max v_c, r_θ, 0)) by re-parametrising t' = t − w_s.

**Theorem T1.** Let the certificate checks of §1.3 pass for (v, T, r).  Then every feasible
z ∈ Tube_v(T, r) has z_s ≥ ŝ, with equality only for z = ẑ.  In particular, since
z_s = ŝ − t + w_s ≤ ŝ − t + r_s, **no feasible point exists at depth t > r_s**: with r_s = 0
the tube minus its t = 0 slice is packing-free, and the slice contains one packing, ẑ.

### 1.2 [T] Proof — A36's (V′) dichotomy re-based on the tube

Fix a feasible z = ẑ − t v + w in the tube; d := z − ẑ, x := |d|∞.  W(z) := Σ_k ω_k g_k(z).

*Validity.*  Every loaded row is ≥ 0 at every feasible point of the tube: walls and dist
rows unconditionally (containment; centre distance ≥ 1 for interior-disjoint unit squares),
the 16 edge rows by A22's lemma (corner q of square i against edge e of square j: if
|t_k| < 1/2 and d_k > −1/2 on the region then g < 0 would put q in int(Q_j)) with the two
margins enclosed **on the tube** (§1.4).  Hence W(z) ≥ 0, and Σ_{k∈P} ω_k g_k(z) ≤ W(z)
(ω ≥ 0, all terms ≥ 0).

*Taylor along the segment.*  [ẑ, z] ⊂ Tube (convex).  With ∇W(ẑ) = e_s + ρ (ρ the
residual of Aᵀω = e_s, ‖ρ‖₁ ≤ ε_w) and the interval Hessian H of W over the tube:

    W(z) = W(ẑ) + d_s + ρ·d + ½ dᵀH(ξ)d        (Lagrange remainder, ξ ∈ [ẑ, z])
    ⟹  z_s − ŝ = d_s ≥ W(z) − ε₀ − ε_w x − ½|dᵀH(ξ)d|.

*The split remainder (the tube's only new inequality).*  d = −t v + w gives

    |dᵀHd| ≤ t²|vᵀHv| + t|(vᵀH)·w| + t|w·(Hv)| + |wᵀHw|
           ≤ t̄² q_vv + t̄ Σ_b (|(vᵀH)_b| + |(Hv)_b|)/2 · w̄_b · 2/2 … 

written out: ½|dᵀHd| ≤ ½ t̄² q_vv + t̄ Σ_b Hv̄_b w̄_b + ½ Σ_ab |H_ab| w̄_a w̄_b, with
q_vv = mag(Σ_ab v_a v_b H_ab) (interval SUM first — the ray is a straight line for every
wall and edge row, which are linear in the centres and in s; only the two dist rows curve,
so q_vv = 0.022 on the scale ray and exactly 0 on the slot ray), Hv̄_b = (mag(vᵀH)_b +
mag(Hv)_b)/2 (column and row sums both enclosed — no symmetry of the interval Hessian is
assumed), |H_ab| = mag H_ab, and the per-coordinate bounds

    t ≤ t̄(x) := min(T, x + r_s)                      (d_s = −t + w_s, |w_s| ≤ r_s)
    |w_b| ≤ w̄_b(x) := min(r_b, x + t̄(x)|v_b|)         (w = d + t v).

Put E(x) := ε₀ + ε_w x + ½ t̄² q_vv + t̄ Σ Hv̄_b w̄_b + ½ Σ |H_ab| w̄_a w̄_b; E is monotone
non-decreasing in x, and z_s − ŝ ≥ W(z) − E(x).

*Case 1* W(z) > E(x): z_s > ŝ.

*Case 2* W(z) ≤ E(x): the pin rows satisfy 0 ≤ g_k(z), Σ_P ω_k g_k ≤ E, so the max-form
(A36 §3.1) gives |Y F_P(z)|∞ ≤ κ_eff E(x), κ_eff = max_{k∈P} max_i|Y_ik|/ω_k; also
|Y F_P(ẑ)|∞ ≤ κ g_max.  The mean-value identity on the pins with points ξ_k ∈ [ẑ, z] ⊂ Tube,
Y(F_P(z) − F_P(ẑ)) = d − (I − Y A_P(Ξ)) d, and β := sup_Tube ‖I − Y A_P‖∞ < 1 give

    x ≤ ψ(x) := (κ_eff E(x) + κ g_max)/(1 − β).

ψ is monotone in x.  Hence, from x ≤ X_max := max_i(T|v_i| + r_i + 2r0), the downward
iterates x₀ = X_max, x_{n+1} = ψ(x_n) satisfy **x ≤ x_n for every n** (induction:
x ≤ ψ(x) ≤ ψ(x_n) = x_{n+1}) — no convexity, no fixed-point existence is needed.  The checker
rounds each iterate UP (still ≥ the true iterate by monotonicity) and stops at the first n
with x_n + r0 ≤ r_N = 1/2000: then z ∈ N = box(z0, r_N) and A22's strict local optimality
(§5 of A22, `a22_optimal`, exact-checked by A70 and Lean-proved by A79) gives z_s ≥ ŝ with
equality iff z = ẑ.  ∎

With T = 0 and r_c = r_θ = r_s = h this is verbatim A36's chain (E = ε₀ + ε_w x + H̄x²): the
checker reproduces `G3_UNIVERSAL` at h = 3689/10⁶ — β 0.4353, H̄ 7.908, κ_eff 19.316,
ψ/h 0.99781 (A70/A79's numbers) and hands over to A22 in 10 iterations (§1.5).

### 1.3 [M] The certificate and the checker (`certs/tube_*.json`, `certs/verify_tube.py`)

Format `contraction-tube-certificate-v1`: T, r_c, r_θ, r_s (rationals), the direction v (34
rationals, plus the spec `scale` / `slot(pins)` from which the checker recomputes and
matches it), ω (70 rationals; `G3_UNIVERSAL`'s), P, the list of rows declared strictly
compressed, the sha256 of `krawczyk_cert.json`; `claims` are informational only.  Checks,
all in exact rational arithmetic (dyadic 2⁻³³⁰ outward rounding, alternating-Taylor
cos/sin; the A70 kernel transcribed, not imported): [F] direction shape; [S] pins = S,
ω ≥ 0, ω = 0 off the universal rows, ω > 0 on pins; [N] activity at ẑ; [C] compression
(§2); [CANARY] a strictly compressed wall row is violated at ẑ − T v; [V] edge-row margins
on the tube and |θ| ≤ 1; [Z][G] ε₀, ε_w, g_max over box(z0, r0); [H] q_vv, Hv̄, |H|; [K]
β < 1, κ; [E] κ_eff; [P] the iteration reaches r_N; plus the row-kind layout, the sha256
binding to `krawczyk_cert.json`, and a pair-relative translation self-test (§1.4).  Gates
(each must FAIL): omega-sign, drop-pin, T-big (×100), r-big (×8), drop-aux, wrong-ray
(dilation instead of contraction — fails [C]/[CANARY], the informational checks; the
load-bearing chain does not distinguish the sign of v, see §2), omega-sign-free, v-tilt,
false-strict, no-sha.  Load-bearing vs structural checks and the trusted inputs (A22's
z0/r0/r_N/S/Y/rows, A22 optimality, the validity lemmas) are listed in the docstring.
Cost: ~1.5 s per certificate.  `tube_regress_a36.json` is the A36 universal box as a
T = 0 tube with gated regression targets (β, H̄, κ_eff, ψ/X).

### 1.4 [T] Pair-relative evaluation (why the hull box is the wrong region)

The first version of the checker enclosed [V], H and β on the HULL of the tube (the ∞-box
B with coordinate i ranging over [ẑ_i − T v_i − r_i, ẑ_i + r_i]).  On B the centres of a
contact pair vary INDEPENDENTLY (width T(v_i + v_j) + 2r_c) whereas on the tube they move
together (width T|v_i − v_j| + 2r_c): the tangential margins then degrade at ~0.8 per unit
T — an interval dependency artifact that walled the tube at T ≈ 0.02.  Edge and dist rows
are translation invariant in the centres (values, gradients and Hessians depend on c_i, c_j
only through c_i − c_j), so the checker encloses every pair row on the box of RELATIVE
centres (square i's slots carry the interval of c_i − c_j, square j's the point 0); wall
rows keep B (their derivatives carry no centre).  Sound because every mean-value point of
the chain lies in the convex tube, whose image under z ↦ (c_i − c_j, θ_i, θ_j) lies in that
box.  Effect: the [V] drift falls to 0.39 (slot) / 0.10 (scale) per unit T, β at T = 0.045
is 0.33 instead of 0.70, and T_max more than doubles (§3).  The Lean port must state the
relative box (`lean/tube_obligation_A83.md` §2).

### 1.5 [M] Regression and canaries

* T = 0, r = 3689/10⁶ (A36's universal box): β 0.43528, H̄ 7.9079, κ_eff 19.31566,
  ψ/X 0.997810, x* → 3.9·10⁻⁴ < r_N in 10 steps: PASS, constants identical to A70/A79.
* Every certificate: the contracted point ẑ − T v violates a strictly compressed wall row
  (scale: all 12 loaded wall rows of contact squares, e.g. `W0c0[x=0]` = −T·(1/2)/ŝ; slot:
  the free squares' far walls `W6c2[y=s]`, `W10c1[x=s]`, `W4c0[x=0]`, …), so no point of
  the ray with t > 0 is a packing; equality only at ẑ by the A22 handover.

## 2. [T] The compression lemma

Let γ_k := ∇g_k(ẑ)·v for a loaded row k, so g_k(ẑ − t v) = −t γ_k + O(t²) (exactly −tγ_k for
wall and edge rows, which are affine in (c, s) at fixed tilts; for the dist rows
g = (1 − t/ŝ)²|Δĉ|² − 1 on the scale ray).

**Lemma C (scale ray).**  Every one of the 38 rows is strictly compressed: γ_k > 0.
*Proof.*  Wall x=0 / y=0 rows: g = q_x with q_x = c_x + (Rh)_x, so γ = ĉ_x/ŝ > 0 (min: square
0, γ = (1/2)/ŝ = 0.12896).  Wall x=s / y=s rows: g = s − q_x, γ = 1 − ĉ_x/ŝ > 0 (ĉ_x < ŝ).
Edge rows g = n(θ_o)·(q_k(p) − c_o) − 1/2: γ = n·(ĉ_p − ĉ_o)/ŝ, and n·(ĉ_p − ĉ_o) =
[n·(q_k − ĉ_o)] − n·(q_k − ĉ_p) = 1/2 − n·R(θ_p)h_k ≥ 1/2 because the touching corner is the
support point of p in direction −n (n·R h_k ≤ 0 at a contact).  Dist rows: γ = 2|Δĉ|²/ŝ =
2/ŝ.  ∎  [M]: min γ over the 38 rows = 0.12896, all rows negative at ẑ − Tv for every
certified T (checker [C]).

**Lemma C′ (slot ray).**  γ_k ≥ 0 for every row, with γ_k = 0 exactly on the rows internal
to the pin block (walls of pins 0, 1, 3; the x=s walls of pins 2, 5 and their y-walls; the
flush rows and dist rows among pins 0, 1, 3 — 18 rows) and γ_k > 0 on the 20 rows that
involve a free square.  *Proof.*  Pins 0, 1, 3 do not move; pins 2, 5 move with the wall
they touch (s − q_x is invariant).  Rows with a free square: as in Lemma C with
v_free = ĉ/ŝ and v_pin ∈ {0, 1}; the sign follows from the same support-point identity
and from each free square lying on the origin side of its pin contacts.  [M] checked
row-by-row (20 strict, 18 exactly zero).  ∎

**The Farkas identity along the ray.**  Σ_k ω_k γ_k = (Aᵀω)·v = e_s·v + ρ·v = 1 ± ε_w
(ε_w = 7.8·10⁻⁴⁵): the multipliers weight the compression rates to exactly the rate at which
s falls.  This is the first-order content of Theorem T1 (a perturbation w has to buy back
Σ ω_k γ_k t = t of row value with |ωᵀA w| ≤ (1 + ε_w)|w_s| — impossible for t > r_s); the
certificate's job is the second-order accounting.

**Role.**  The compression lemma is not load-bearing in the chain of §1.2 (the chain never
uses the sign of v): it is (i) the reason no contact BREAKS along the ray — so the
branch-free universal rows stay valid on the tube and no L1 axis disjunction (A36 §L1) is
needed, which is what makes the tube a single certificate instead of 16 variants per ring;
(ii) the canary; (iii) the explanation of the cheapness: contraction leaves every wall and
edge row affine, so q_vv is ~0 and the Taylor cost is linear in T (the cross term t·Hv̄·r)
rather than quadratic.

## 3. [M] The (T, r) curve and the wall

Exact-checker bisections (`attempts/A83-contraction-tube/results/sweep.jsonl`,
`curve.json`; r_s = 0; θ-frame radians; relative precision 0.5 %).

**T_max at fixed radii (largest PASS / first FAIL, binding check):**

| ray | r_c | r_θ | T_max | binding | β at T_max | ψ/X | tan margin at T_max |
|---|---|---|---|---|---|---|---|
| slot | 1.6e-3 | 2.1e-3 (A60 landing) | **0.0457** | [V] `E3c2-7e3` | 0.329 | 0.023 | 3e-5 |
| slot | 1.6e-3 | 1.6e-3 | 0.0473 | [V] `E3c2-7e3` | 0.296 | 0.016 | |
| slot | 0.8e-3 | 1.05e-3 | 0.0551 | [V] `E3c2-7e3` | 0.238 | 0.006 | |
| slot | 2e-4 | 2e-4 | **0.0621** (> ŝ − 3.82 = 0.0571) | [V] `E3c2-7e3` | 0.165 | 6e-4 | |
| slot | 2.5e-3 | 3.0e-3 | 0.0362 | [V] `E3c2-7e3` | 0.414 | 0.062 | |
| scale | 1.6e-3 | 2.1e-3 | **0.1305** | [V] `E7c2-9e3` | 0.551 | 0.086 | |
| scale | 1.6e-3 | 1.6e-3 | 0.1363 | [V] `E7c2-9e3` | 0.529 | 0.081 | |
| scale | 0.8e-3 | 1.05e-3 | 0.1602 | [V] `E7c2-9e3` | 0.513 | 0.078 | |
| scale | 2e-4 | 2e-4 | 0.1828 | [V] `E7c2-9e3` | 0.481 | 0.076 | |
| scale | 2.5e-3 | 3.0e-3 | 0.1000 | [V] `E7c2-9e3` | 0.581 | 0.104 | |

(scale ray, isotropic r_max: 3.68e-3 / 3.54e-3 / 3.45e-3 / 3.36e-3 / 3.11e-3 at
T = 0 / 0.01 / 0.02 / 0.03 / 0.0571, all cliff-bound — on the scale ray the cliff, not
validity, sets r_max across the whole window.)

**r_max (isotropic r_c = r_θ) at fixed T, slot ray:**

| T | r_max | binding |
|---|---|---|
| 0 | 3.680e-3 (A36: 3.689e-3 at ψ/h 0.9978) | [P] cliff (iteration stalls at ψ(X) ≥ X) |
| 1e-3 | 3.665e-3 | [P] cliff |
| 1e-2 | 3.572e-3 | [P] cliff |
| 2e-2 | 3.495e-3 | [P] cliff |
| 3e-2 | 3.232e-3 | [V] `E3c2-7e3` |
| 0.05708 (= ŝ − 3.82) | 6.9e-4 | [V] `E3c2-7e3` |

**Anisotropic frontier (slot ray, r_θ_max at fixed T, r_c; all cliff-bound):**
T = 0.01: r_θ_max = 6.98e-3 / 6.13e-3 / 5.10e-3 at r_c = 0.8e-3 / 1.6e-3 / 2.5e-3;
T = 0.02: 6.80e-3 / 5.96e-3 / 4.91e-3.  The tilt radius can be ~3× the centre radius
(the centre coordinates carry the cross term t·Hv̄, the tilts only the wᵀHw block): A60's
tilt landing (2.0e-3 rad) has a 3× reserve, its centre landing (1.45e-3) the binding one.

**The wall, named.**  Slot ray: the tangential validity margin of A22 row 13, `E3c2-7e3`
(corner 2 of pin square 3 — which does not move — on the left edge of free square 7, which
contracts toward the origin at |v_7| = 0.67), 0.0208 at ẑ, spent at 0.39 per unit T plus
≈ 3.3 r_θ + 2.8 r_c from the perturbation radii: T_max ≈ (0.0208 − 3.3 r_θ − 2.8 r_c)/0.39.
Scale ray: row 27, `E7c2-9e3` (the 7–9 flush pinwheel pair, |t| = 0.475 at ẑ), spent at
≈ 0.10 per unit T (relative motion T|v_7 − v_9| only): T_max ≈ 0.13.  Neither β (0.33 /
0.55 at the walls) nor the pinning cliff binds at the landing radii; the cliff binds only
for r ≳ 3.2·10⁻³ and T ≤ 0.02, where it reproduces A36's isotropic reach.  Both walls are
VALIDITY walls of pin rows (13 ∈ S, 27 ∈ S), so they cannot be dropped from ω; the only
lever beyond them is a different pin basis (A22's 512 admissible drop sets) or a branch
(L1-style disjunction at |t_k| ≥ 1/2, which the compression lemma says is never needed for
the contacts that stay closed — but this one is sliding open tangentially).  Not pursued:
the certified reach already exceeds every consumer's need (§4).

## 4. [T] Lemma SEAM — the exact side-to-depth map and the composition obligation

Setting (the seam as articulated 2026-09-03).  s0 = 969271/250000 is the residual tree's
side (s0 − ŝ = 4.0998·10⁻⁷); ẑ has side ŝ.  A stratum S (Young class; trump5 = 5 pins at
slots, or a K1-protected class) has an s0 residual tree whose leaves are (K) — a
`case-lp-certificate-v1` PASS with the pin cores slackened to half-side 1/2 − δ_pin
(A57's G1 convention, δ = 10⁻²) — or (D): every family reaching the leaf has, mod G, its
free squares within (r_land,c, r_land,t) of ẑ's in (c, t) coordinates (A60: 1.4472·10⁻³ /
1.1426·10⁻³, θ-containment 2.0102·10⁻³).

### 4.1 [T] Which side maps to which depth (the map, per coordinate)

Let P be a packing at side m ∈ [ŝ − T′, ŝ] with skeleton in S, pins at slots(m) EXACTLY,
and put **t := ŝ − m ∈ [0, T′]**, λ := s0/m.  F := Δ_λ P is a strictly disjoint closed
11-family in [0, s0]² (Lemma B.0, `closed_disjoint_bridge.md`), with tilts unchanged.

* **Pins under dilation** (B.0(c)): pin centre λ(α + βm) = (α + β s0) + (λ − 1)α, i.e.
  within (λ − 1)|α| per coordinate of slots(s0); for trump5 max|α| = 3/2 (squares 1, 3),
  census-wide ≤ 5/2.  F's pin squares contain the δ_pin-slack cores at slots(s0) iff
  (λ − 1)·A < δ_pin, A = max|α| (Corollary B′, ρ = δ_pin for axis-aligned cores).
* **Leaf selection at s0.**  Under that condition F satisfies the tree's root hypothesis
  (core form), and every node hypothesis is a statement about the family F at side s0
  (box-cores, T5/T11 logic kills, NO-family occupancy dichotomies — all applied to F
  itself, so NO B.2″ widening enters); F reaches some leaf.  (K): Lemma B (pricing of the
  ≥ b core-free strictly disjoint squares of F) — no such P.  (D): ∃ g ∈ G with g·F's free
  squares within r_land of ẑ's; since dilation commutes with G at the respective sides
  (Δ_λ ∘ g_m = g_{s0} ∘ Δ_λ: e.g. s0 − λx = λ(m − x)), replace P by g_m P and take g = id.
* **Pull-back into the tube (per coordinate).**  With v = slot(pins):
  - pinned centre coordinate: P_i = α + β m = α + β ŝ − β t = ẑ_i − t v_i, **w_i = 0**;
  - free centre coordinate: P_i = F_i/λ = (ẑ_i + e_i)(m/s0), |e_i| ≤ r_land,c, and
    ẑ_i m/s0 = ẑ_i(1 − t/ŝ)(ŝ/s0) = ẑ_i − t ẑ_i/ŝ − ẑ_i(1 − t/ŝ)(s0 − ŝ)/s0, so
    P_i = ẑ_i − t v_i + w_i with |w_i| ≤ r_land,c·(m/s0) + |ẑ_i|(s0 − ŝ)/s0 ≤ r_land,c + 3.6·10⁻⁷;
  - tilt: P_θ = F_θ, |w_θ| ≤ r_land,θ (radians) — from a t-world landing r_t:
    r_θ ≤ 2 r_t globally (X.1) or ≤ 1.771 r_t on t ∈ [0.36, 0.37] (X.1 sharp; A60's boxes lie
    there), and A60's measured θ-containment 2.0102·10⁻³ directly;
  - side: P's side is m = ŝ − t: **w_s = 0**.
  Hence (P, m) ∈ Tube_slot(T′, (r_land,c + 3.6·10⁻⁷, r_land,θ, 0)) with t = ŝ − m exactly.
* **Conclusion.**  Theorem T1 at (T, r) ⊇ (T′, r_land) gives m ≥ ŝ, so m = ŝ and P = ẑ
  (mod G).  Every packing of side m ∈ [ŝ − T′, ŝ) in S is excluded; at m = ŝ only Trump.

**Lemma SEAM (trump5).**  Let the s0 residual tree of trump5 terminate in (K)/(D) leaves
with pin-core slack δ_pin and (D) landings (r_land,c, r_land,θ), and let the tube be
certified at (T_tube, r) with r ≥ (r_land,c + 3.6·10⁻⁷, r_land,θ).  Then every packing of
side m ∈ [ŝ − T′, ŝ] with skeleton trump5 is excluded except Trump at m = ŝ, for

    T′ = min( T_tube,  T_K(δ_pin) ),
    T_K(δ_pin) = ( (2/3)·δ_pin·ŝ − (s0 − ŝ) ) / ( 1 + (2/3)·δ_pin )     [A = 3/2 for trump5]

(the (K) condition (λ_max − 1)·(3/2) < δ_pin with λ_max − 1 = (s0 − ŝ + T′)/(ŝ − T′)).
Numbers: T_K(10⁻²) = 0.02567, T_K(10⁻³) = 0.002566, T_K(10⁻⁴) = 0.000253;
T_tube(A60 landing) = 0.0457.  **So δ_basin(trump5) = 0.0257 at δ_pin = 10⁻²** (the slack
binds, not the tube; at δ_pin = 2·10⁻² the tube binds: δ_basin = 0.0457).  ∎

### 4.2 The seam condition as two numbers

    δ_basin(trump5) = 0.0257   (δ_pin = 10⁻², A60 landings; 0.0457 with δ_pin ≥ 1.8·10⁻²)
    δ_LP            = A82 on-disk (all LPs UNCONVERGED, 600 s cap; an unconverged restricted
                      master UNDER-estimates τ*, so these η are optimistic):
                      k4_08: η = −0.027 / −0.050 / −0.377 at ŝ − m = 6·10⁻⁷ / 8.4·10⁻⁵ / 0.0439
                      k4_11: −0.0086 / −0.019 / −0.024 at 6·10⁻⁷ / 8.4·10⁻⁵ / 5.8·10⁻⁴
                      k0_00: −0.000 at 0.0439.  trump5's own crossover NOT yet scanned.
                      The near-ŝ slopes (600 / 200 per unit side) extrapolated to η = −1 gave
                      1.7·10⁻³ / 5·10⁻³; the one deep point (k4_08 at 3.8332: −0.38) says the
                      slope flattens and the protected classes' crossovers lie BELOW
                      ŝ − 0.044, possibly below the window's bottom.

The seam condition is δ_basin ≥ δ_LP(S) per stratum.  For trump5, δ_basin = 0.0257 (up to
0.0457) is 5–15× the near-ŝ extrapolations; against the deep k4_08 point (η = −0.38 at
0.044) it is NOT enough if trump5 behaves like k4_08 — but trump5 is the class whose
aliveness witness is Trump himself (A82: protection is an s ≥ ŝ phenomenon for the
PROTECTED classes because Trump-minus-a-pin realises them; trump5 loses its witness the
moment m < ŝ), so its crossover is expected nearer the near-ŝ extrapolation; it must be
scanned (§4.4 item 3).  Regime 1 (plain kills) then only has to reach sides ≤ ŝ − 0.0257 =
3.8514, and each plain slack-core certificate covers a slab of width (2/A)δ·m ≈ 0.026
(A = 3/2, δ = 10⁻²), so **two plain certificates** would cover [3.82, 3.8514] for trump5 if
they certify there.  With the tiny-r certificate (T = 0.0621 at r = 2·10⁻⁴) the tube alone
spans the window, but no tree lands that tightly; at A60's landings the tube spans
[3.8314, ŝ] = 80 % of the window by itself (δ_pin ≥ 1.8·10⁻² needed for the (K) side).

### 4.3 Protected classes with Theorem U at their (D) leaves

For a K1-protected class the (D) leaf is "10 squares localised, the 11th (the missing pin's
neighbour) placed by Theorem U" (A65/A80).  The tube version needs, for F = Δ_λ P at s0:
(i) the 10 squares contain U's δ_U-slack cores: by Lemma U-C, δ_U ≥ r_land,t + √2(r_land,c +
(λ − 1)·A) for pins (drift) and ≥ r_land,t + √2 r_land,c for free squares; (ii) the 11th
square then lies in the pocket zone Z(δ_U) (A80: radius ≈ 5.8 δ_U for square 6's
top-wall/flush-9/point-4 pocket, 1–2.8 δ_U elsewhere); (iii) the pull-back of ALL 11 squares
into the tube needs r_c, r_θ ≥ max(r_land, pocket radius), which the tube certifies only up
to the cliff, r ≲ 3.2·10⁻³ at T ≤ 0.03 (§3).  So

    pocket(δ_U) ≤ 3.2·10⁻³  ⟹  δ_U ≤ 5.5·10⁻⁴ (square-6 pocket)
    ⟹  r_land,t + √2 r_land,c ≤ 5.5·10⁻⁴  (landings ≈ 2·10⁻⁴, A80's finding unchanged)
    ⟹  drift (λ − 1)·A·√2 ≤ 5.5·10⁻⁴ − (r_land,t + √2 r_land,c):  with landings 10⁻⁴,
        A = 5/2:  λ − 1 ≤ 7.6·10⁻⁵,  T′ ≤ 2.9·10⁻⁴.

**Finding [F]: with Theorem U certified at s0, the protected-class seam reaches only
T′ ≈ 3·10⁻⁴ < δ_LP (2·10⁻³ … 5·10⁻³) — the pin drift enters through U's cores and the
square-6 pocket amplifies it 5.8×.  The tube does not help here (its gain is in T, not r).**
What the tube version of Theorem U needs, exactly: U re-emitted along the slab at grid sides
m_j = ŝ − jΔm with cores at the slot-contracted Trump positions, Δm ≤ (2/A)·m·(δ_U/√2 −
r_land,t/√2 − r_land,c) ≈ 1.7·10⁻⁴ at δ_U = 5.5·10⁻⁴ (A = 5/2) — ~30 sides for T′ = 5·10⁻³,
~150 for 0.0257, 11 re-insertion certificates each (A65: ~3 s, Σw = 0) — applied to P
dilated to the nearest grid side above m, whose pocket then pulls back into the tube.
Alternatively per-square slacks in U (drift-tolerant cores on the pins only, tight cores on
the free squares) if the 11th square's pocket is bounded by free squares — square 6's is
(top wall, free square 9, free square 4 in trump5).  Both are A80's owner's to price; the
tube's obligation to them is stated here.  Note the s0 obligation (landings ~2·10⁻⁴ for the
pocket to fit the basin at all) is prior and unchanged.

### 4.4 Obligations for the composition (D.SLAB), in order

1. **Tree re-emission with δ_pin ≥ 10⁻²** (A60): A60's ledger fixed δ = 10⁻⁴ for the widening
   budget of the slack-core GRID route; in the tube route no widening exists (the tube
   absorbs the dilation displacement exactly, §4.1) and the only pin-slack requirement is
   T_K(δ_pin) ≥ T′, i.e. δ_pin ≥ (3/2)(T′ + 4.1·10⁻⁷)/(ŝ − T′) — 0.0039 for T′ = 10⁻², 0.0100
   for T′ = 0.0257.  A60 measured δ = 10⁻³ at unchanged cost; δ = 10⁻² is A57's G1 operating
   point (V9/E4 gate clean).  **Every A60 (K) leaf must be re-emitted at δ_pin = 10⁻²** (the
   ε-fat and 10⁻⁴ leaves reach T′ = 1.6·10⁻⁹ / 2.5·10⁻⁴ only).
2. **(D) landings** stay as measured (1.4472·10⁻³ / 1.1426·10⁻³ in t, 2.0102·10⁻³ in θ): the
   tube at (1.6·10⁻³, 2.1·10⁻³ rad) covers them with T = 0.045 (`tube_slot_T4.5e-2_landing`);
   the 4.9 % overshoot of A60 §8.3 (landing + widening vs rBasin) is void in the tube route
   (no widening, and the basin radius is the tube's r, not rBasin).  D.S6's pin half is exact
   (w = 0), its mod-G half is §4.1's commutation; the free half is the landing itself.
3. **trump5's own δ_LP** (one A82-style scan) — to state the seam with both numbers measured
   on the same class.  Regime 1 for trump5 = plain slack-core certificates below
   ŝ − δ_basin (two slabs suffice, §4.2).
4. **Protected classes**: the U-slab obligation of §4.3 (A80's owner), gated on landings
   ≈ 2·10⁻⁴; without it the tube route caps their seam at T′ ≈ 3·10⁻⁴.
5. Lean: `lean/tube_obligation_A83.md` (checker port = A79's chain with the relative box,
   the split remainder and the monotone iteration; ~400 lines, no new analysis).

## 5. Findings

* [F] **The tube is cheap because contraction is affine on the contact rows**: q_vv is 0
  (slot) / 0.022 (scale), so the Taylor cost is linear in T; at the landing radii ψ/X is
  0.02–0.09 — the pinning has a 10–50× reserve where A36's isotropic box sits at 0.998.
  The reach is set by VALIDITY of two A22 pin rows (E3c2-7e3 / E7c2-9e3), i.e. by the
  tangential sliding of a corner along an edge under the ray — a geometric wall, named.
* [F] **The hull-box artifact** (§1.4): interval dependency between the two centres of a
  pair row costs a factor > 2 in T and 0.4 in β; pair-relative boxes are the fix and are
  what the Lean port must state.  This is generic advice for every future certificate whose
  region is a thin neighbourhood of a curve rather than a box.
* [F] **The scale ray is the wrong model for pinned squares**: slots are affine in s
  (α + βs), scaling is not; on the scale ray a pin at slot α sits t|α|/ŝ off the ray
  (3.9·10⁻³ at T = 10⁻² for α = 3/2), beyond the cliff.  The slot direction has zero pin
  displacement at zero certificate cost; the certificate machinery accepts any centre-only
  direction, and the compression lemma survives in the weak form γ ≥ 0 (18 rows at exactly 0).
  T_max(slot) = 0.046 < T_max(scale) = 0.13 at the landing radii, because pin-free
  contacts drift at |v_free| rather than |v_i − v_j|.
* [F] **No widening in the tube route**: all tree logic is applied to the dilated family at
  s0; only the pin slack δ_pin enters, and it enters as T_K(δ) ≈ (2/3)δ ŝ.  A60's planned
  δ = 10⁻⁴ (chosen for the grid route's widening budget) would cap the tube route at
  T′ = 2.5·10⁻⁴; δ = 10⁻² is the operating point for the tube route.
* [F] The tube alone cannot span the window at A60's landing radii (T_max 0.046 vs
  0.057 needed) but does at r = 2·10⁻⁴; the seam does not need it to (§4.2).
* [F] Protected classes: the tube leaves the Theorem-U pocket problem exactly where A80
  left it and adds the pin-drift term; the s0-U route caps T′ ≈ 3·10⁻⁴ (§4.3).

## 6. Files, headline table, process (A83's findings note lives here — harness rule)

`certs/verify_tube.py` (checker, 10 gates), `certs/tube_*.json` (12 certificates: slot
T ∈ {0.01, 0.036, 0.042, 0.045, 0.055, 0.0571, 0.062}, scale T ∈ {0.01, 0.0571, 0.13},
plus `tube_regress_a36.json`),
`attempts/A83-contraction-tube/code/{emit_tube,sweep_tube,curve_from_sweep,depgraph_note}.py`,
`results/{sweep.jsonl, sweep_hullbox_v0.jsonl, curve.json, verify_all.report.json,
gate_*.report.json}`, `notes/review_opus.md` (independent Opus review of the checker),
`lean/tube_obligation_A83.md`.  Re-run: `python certs/verify_tube.py certs/tube_*.json`;
gates: `--corrupt {omega-sign,drop-pin,T-big,r-big,drop-aux,wrong-ray}`;
curve: `python code/sweep_tube.py all && python code/curve_from_sweep.py`.

| what | value |
|---|---|
| T at A60 landing radii (r_c 1.6e-3, r_θ 2.1e-3), slot ray | **0.045 certified** (wall 0.0457) |
| T at r = 6.5e-4, slot ray | **0.0571 = ŝ − 3.82** (whole window; wall 0.0621 at r = 2e-4) |
| T at landing radii, scale ray | **0.13 certified** (wall 0.1305) |
| isotropic r_max at T = 0 / 0.02 (slot) | 3.68e-3 (= A36) / 3.49e-3 |
| binding contact at the wall | slot: row 13 `E3c2-7e3`, 0.39 per unit T; scale: row 27 `E7c2-9e3`, 0.10 per unit T |
| ψ/X at the landing point, T = 0.045 | 0.023 (A36's isotropic box sits at 0.998) |
| β at the wall | 0.33 (slot) / 0.55 (scale) — never binds |
| δ_basin(trump5) | 0.0257 at δ_pin = 1e-2 (K-slack-bound); 0.0457 at δ_pin ≥ 1.8e-2 |
| checker | ~1.5 s/certificate; 289 checks / 12 certs / 0 failures; 10/10 gates FAIL as required; Opus review SOUND |

Process.  At most two light single-core Python processes (exact bisections, ~1 s per
evaluation); no LP, no BLAS; A57/A60/A61/A81/A82 untouched (read-only use of A22/A36/A70
certificates and code, A60's ledger, A82's results); frozen verifiers untouched; `certs/`
new files only.  Commit headroom dipped to 5.1 GB during the sweeps (other campaigns);
nothing heavy was launched.  Incidents: a CIM process filter on the string `sweep_tube.py`
matched the invoking PowerShell and killed it (harmless; fixed by filtering on
`Name -like python*`); the first sweep was launched twice (de-duplicated in
`curve_from_sweep.py`); the harness blocked `notes/findings.md` (this section is the fallback).
