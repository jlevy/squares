# Local minima with flat motions (grade C): the paper argument (10-07)

Notion: `IsLocalMinPacking` (lean/Sqpack/LocalMin.lean): a pose-space ball around the record (centres within ε,
angles within ε mod 90°, squares matched by index) contains no packing in a smaller square.

## Setting

* Remove the squares carrying no force (rattlers, force-free squares): a packing of the n squares near the record
  restricts to a packing of the rest, so a local minimum of the load-bearing subsystem is one of the whole record.
* Coordinates `z = (x_i, y_i, w_i, S)` with `w_i = sin δ_i`, `δ_i` the angle change (`u_i = cos δ_i − 1`, `|u_i| ≤ w_i²`).
  Record `z*`.  Every row function `h_r` is affine in the centres at fixed angles and polynomial in `(w, u)`.
* **Rows**: every load-bearing incidence "corner of j on side k of i" (and corner-on-wall).  Near `z*`, a valid
  packing gives `h_r(z) ≥ −K|z − z*|²` (the slack is needed only for corners at a side end; see "Relaxation" below).
* `L_r(z) = ∇h_r(z)`; `L = L(z*)`.  KKT at `z*`: `Σ λ*_r L_r = e_S`, all `λ*_r > 0`.

## Relaxation, including corners at a side end

* Corner strictly inside the side (`|τ*| < 1/2`): the corner is a point of closed square `j`, not in the open square
  `i`; the other three side values stay `< 1/2` near `z*`, so `h_r ≥ 0` (as in grade A, `sideVal_ge_of_disjoint`).
* Corner at a side end, with `j`'s edge running *along* `i`'s side from that corner (aligned or partially overlapping
  side-side contacts): points `P(s)` of that edge with `|τ| ≤ 1/2 − Kδ` project strictly inside `i`'s side, so
  `v(s) = n·(P(s) − c_i) − 1/2 ≥ 0` there.  `v` is affine in `s`, and `v(corner) − v(s) = (corner − s)·v'` with
  `v' = O(δ)` (both ends of the edge have `v = 0` at the record).  So the corner's own row has `h_r ≥ −K'δ²`.
  No branching and no separating-axis theorem: the rigidity argument only needs `h_r ≥ −K'δ²`.
  (The other branch, "`i`'s corners beyond `j`'s side", has the *same* linear parts, `L₃ = L₁`, `L₄ = L₂`: checked
  by hand for the aligned axis case; this is why one line per pair suffices.)
* A corner at a side end whose edge leaves the side (a corner-corner touch) is not a row: it was never load-bearing
  in exactsolve's equations, and dropping constraints is always allowed.
* Earlier, grade A used *midpoint* rows for aligned pairs.  That is valid but forces equal forces at both ends (no
  torque through the contact): fine for n = 11, 28; infeasible at `z*` for 17, 19, 37, 50, 66.  With the edge-point
  relaxation every incidence is its own row and the max-min multiplier matches exactsolve's.

## Flat family

`F` = position directions `φ` (centres only, angles fixed) with `L_r φ = 0` for every row.  Since `h_r` is affine in
the centres at fixed angles, `h_r(z* + φ) = h_r(z*) = 0` exactly: `M = z* + F` is an exact affine family of
configurations with every row tight and `S = S*`.  These are the directions minpoly.py pins.  (Flat *rotations*
of load-bearing squares are not covered here; in the cases seen so far they are force-free squares, removed above.)

## Theorem C

Hypotheses:

1. rows valid near `z*` with margin `μ > 0` (projections strictly inside, or edge overlap for side-end corners);
2. **KKT along the family**: for every `m ∈ M` near `z*` there are multipliers `λ(m) ≥ λ_min > 0` with
   `Σ λ_r(m) L_r(m) = e_S` (constants uniform near `z*`);
3. `F ⊂ null L` (automatic), and with `W = null L ∩ F^⊥`, the reduced Hessian `Q = ∇²ℒ(z*)|_W` is positive definite,
   `ζᵀ Q ζ ≥ κ |ζ|²` (`ℒ = S − Σ λ*_r h_r`).

Then `z*` is a local minimum.

Proof.  Let `z` be a packing with `|z − z*| < ε` and `S(z) < S*`.  Let `m ∈ M` be the nearest point (Euclidean
projection of the centre part onto `F`), `Δ = z − m ⊥ F`, `|Δ| < ε`.

* Taylor at `m` with `ℒ_m = S − Σ λ_r(m) h_r` (stationary at `m` by 2):
  `S(z) − S* = Σ λ_r(m) h_r(z) + ½ Δᵀ ∇²ℒ_m(m) Δ + O(|Δ|³)`.
* From `S(z) < S*` and `h_r ≥ −K'|Δ|²`: every `h_r(z) = O(|Δ|²)`, so `|L(m) Δ| = O(|Δ|²)`, and since
  `L(m) − L = O(ε)` (only the torque columns change along `M`, linearly in `φ`): `|L Δ| ≤ C(|Δ| + ε) |Δ|`.
* Split `Δ = ζ + η`, `ζ ∈ null L`, `η ⊥ null L`: `|η| ≤ σ⁻¹ |LΔ| ≤ τ |Δ|` with `τ = O(ε)`.  Since `Δ ⊥ F` and
  `F ⊂ null L`, the `F`-part of `ζ` equals minus the `F`-part of `η`, so `ζ = ζ_W + ζ_F`, `|ζ_F| ≤ |η|`.
* `Δᵀ∇²ℒ_m Δ ≥ κ|ζ_W|² − O(τ + ε)|Δ|² ≥ (κ/2)|Δ|²` for small `ε`.  Hence `S(z) − S* ≥ (κ/4)|Δ|² − O(|Δ|³) ≥ 0`,
  a contradiction (if `Δ = 0` then `z = m` and `S(z) = S*`).  ∎

The key point: expanding around the nearest point `m` of the family (with its own multipliers) rather than around
`z*` keeps the `O(ε)` error from `L(m) − L` multiplied by `|Δ|` in the `η` estimate, where it only weakens the
coercivity constant.  Expanding around `z*` instead leaves a term linear in `Δ` that nothing absorbs.

Grade B (n = 5) is the case `F = 0`; grade A is the case `null L = 0` (no Hessian needed).

## Checks (numerical, 10-07; `proto/flatkkt.py`, run from search/exact with PYTHONPATH=. ./env.sh; to be promoted into localmin.py)

With every load-bearing incidence as a row (one line per aligned pair): max-min `λ > 0` at `z*`, and along every
flat direction (steps ±1e-3, 1e-2) the force balance stays feasible with `λ > 0`:

| n | rows | dim F | max-min λ at z* | along F (min) |
|---|---|---|---|---|
| 10 | 28 | 2 | 0.125 | 0.125 |
| 17 | 52 | 3 | 0.00608 | 0.00601 |
| 19 | 42 | 6 | 0.0786 | 0.0391 |
| 37 | 68 | 15 | 0.0128 | 0.0128 |
| 38 | 104 | 12 | 0.0625 | 0.0312 |
| 50 | 94 | 20 | 0.00625 | 0.00609 |
| 66 | 68 | 16 | 0.0388 | 0.0381 |
| 11, 28 | 40, 116 | 0 | 0.0476, 0.0165 | (grade A) |

Hypothesis 2 is necessary for local optimality (under a constraint qualification: a non-KKT point `m` of the family
would have a descent direction, giving packings near `z*` with `S < S*`), so this is a consistency check, not luck.

## Certificate plan (exact)

* rows and `λ*` as in grade A (exact in `K`), now with every incidence;
* `F`: basis of the flat position directions (exact, rational or in `K`);
* hypothesis 2: solve the KKT system over `K(φ₁..φ_f)` (positions are linear in `φ`, torque columns linear in `φ`)
  for `λ(φ)` with `λ(0) = λ*`; positivity near 0 from `λ* > 0` and an explicit Lipschitz bound;
  or a perturbation bound (Neumann series on a basis block) with explicit constants;
* hypothesis 3: `Q` on `W` exactly in `K` (Hessians of the rows are explicit), positive definite via an `LDLᵀ` with
  interval signs, or a rational approximate Cholesky factor with a residual bound;
* `σ`: a rational approximate pseudo-inverse of `L` on `(null L)^⊥`, as `G` in grade A.

Lean: the same layering as grade A (`rigidity` → a second-order lemma; `isLocalMin_of_rows` → a family version);
the projection onto `M` is elementary (an affine subspace of centre coordinates).

## Hypothesis 2 by null vectors (10-11; `search/exact/gradec.py`)

KKT along `M` is an equality condition on a whole family, so it needs an exact certificate.  Polynomial multipliers
`λ(φ)` do not exist in general (n = 19: no `λ(φ)` of degree ≤ 3 satisfies `L(φ)ᵀλ(φ) = e_S` identically; the
min-norm multipliers are rational in `φ`).  The dual object is polynomial:

* `L(φ) = L₀ + Σ φ_k A_k` is affine in `φ` (moving centres only changes the lever arms in the torque columns).
* Certificate: affine vectors `w_j(φ) = w_j0 + Σ φ_k w_jk` with `L(φ) w_j(φ) ≡ 0` (identities `L₀w_j0 = 0`,
  `L₀w_jk + A_k w_j0 = 0`, `A_k w_jl + A_l w_jk = 0`, exact in `K`), S-components 0, whose `w_j0` extend a basis of
  `F` to a basis of `null L₀`.
* Lemma.  Then for `φ` near 0, `null L(φ) = span(F, w_j(φ))` (rank `L(φ) ≥ rank L₀` near 0, and these are
  `dim null L₀` independent null vectors), `e_S ⊥ null L(φ)`, so `e_S ∈ range L(φ)ᵀ` with constant rank, and
  `λ(φ) = λ* + L(φ)ᵀ⁺(e_S − L(φ)ᵀλ*)` is continuous with `λ(0) = λ* > 0`: hypothesis 2.
* The same identities give `λ*ᵀ A_k w_j0 = −(w_jk)_S = 0`: the `F × W` block of `∇²ℒ` vanishes (and `F × F` does
  since rows are affine in the centres), so hypothesis 3 may be checked on `span(w_j0)`, any complement of `F` in
  `null L₀`.
* Degree 1 suffices in every case tried (n = 10, 19, 37).  When `null L₀ = F` (W = 0; n = 29), no `w_j` are needed:
  hypothesis 2 is the open condition `rank L₀ = N − dim F` and hypothesis 3 is vacuous.

`gradec.py` results (exact in K, signs by intervals): n = 10 VALID (36 rows, dim F 2, dim W 2, λ_min 0.0625, minors
0.088, 0.0078); n = 19 VALID (54 rows, dim F 6, dim W 2, λ_min 0.0393, minors 0.079, 0.0062).

**Batch (10-11)**: all 250 records with field degree ≤ 4 (8 parallel jobs, 30 min cap each; per-n status in
`search/exact/gradec_runs/_status.txt`, logs gitignored, certificates `minpoly/solve/n-N.gradec.json` gitignored).
**231 VALID**, including n = 66, 127, 150, 175, whose coordinates carry 1e-16 to 1e-7 offsets: the side-end/interior/
beyond classification is exact in K, so tiny margins are harmless.  Not VALID:
* n = 230, 261: no strictly positive multipliers with the full row set: 24 rows (wall rows and interior incidences,
  the same substructure in both records) carry zero force in every multiplier vector.  `GRADEC_DROPZERO=1` drops them
  (numerical LP for the forced-zero set; a side-end pair goes as a whole).  Dropping constraints only relaxes the
  problem, so a certificate for the smaller row set covers the record.  With them dropped, 12 squares stop being
  load-bearing, null L0 = F (W = 0), and both are **VALID** (λ_min 0.0034; flat families of dim 110 and 122; ~1 min
  each).  Logs `gradec_runs/n-{230,261}.dropzero.log`.  The mutation tests are still rejected with the option on.
  So **233 of the 250 are VALID**.
* 17 timeouts (n = 174, 201, 204, 231, 234, 257, 262, 274, 275, 295, 296, 299, 308–312).  10 of them reached exact
  λ* > 0 and timed out in the Hessian step; 7 (dim F 210–274) timed out in the null-vector elimination.  Pure cost:
  exact sparse elimination with hundreds of flat directions.
