# exact — exact-contact solver for packings of unit squares

Input: an approximate packing (text: `n s`, then `x y theta_deg` per square, centres, lower-left origin).
Output: a nearby **exact KKT point** of *min S subject to non-overlap* (`--dps`, default 80; 2000 tested at n = 17), numerical optimality checks, and an
**exact rational certificate** of `s(n) <= S'`, with `S' - S ~ 1e-19`.

```
python3 exactsolve.py in.txt [--dps 80] [--eps 1e-20] [--out DIR] [--algdeg 16] [--tol T]
python3 verify_cert.py  results/NAME.cert     # exact check, separating axes (stdlib Fractions only)
python3 verify_cert2.py results/NAME.cert     # independent exact check, polygon intersection (stdlib Fractions only)
./run_all.sh                                  # the test set below (~2 min); python3 summary.py results/*.json
```
Outputs in `results/` (or `--out`): `NAME.log` (report), `NAME.json`, `NAME.exact.txt` (configuration, dps-10 digits),
`NAME.cert` (certificate).  Uses one core (BLAS threads pinned to 1); n = 110 takes ~5 s at 80 digits, n = 300 a few minutes.
Requires python3 with numpy, scipy (HiGHS LP/MILP), mpmath.  The verifiers need only the standard library.

**`batch/`: every record in jlevy's register (n = 1–324), 2026-10-05.**  323 certified (317 numerically KKT local
minima), every n ≤ 291 included; 50 certified values lie 3e-13 … 5e-11 below the register's printed bounds (the exact
optimum of the same packing).  See `batch/README.md`.

**Exact forms and local-minimum certificates (2026-10-07; details and state: `../../tasks/exact-minpoly/README.md`).**
`exactsolve.py` also writes `NAME.contacts.json`, the input for the following tools (run via `./env.sh`):

| tool | does |
|---|---|
| `minpoly.py` | contact graph → number field `K = ℚ[t]/f`, exact configuration over `K`, the minimal polynomial of S and an isolating interval |
| `verify_exact.py` | independent stdlib check of `minpoly.py`'s output: contacts ≡ 0 mod f, the rest separated by interval arithmetic |
| `minpoly/run_minpoly.sh`, `minpoly/summary.py` | batch over the register → `minpoly/results.md` (269/324 verified 10-07) |
| `localmin.py` | grade-A local-minimum certificates (exact multipliers in `K`, rational left inverse) |
| `lean_cert.py`, `localmin_lean.py` | Lean certificates (`lean/Sqpack/Exact/`) |
| `minpoly/data/n-N.minpoly.json.gz` | the committed exact forms (only VALID ones); `minpoly/verify_data.sh` replays `verify_exact.py` on all |
| `EXACT_FORMS.md`, `exact_forms.json` | the table: S*, p, isolating interval, field, checks per n (`minpoly/table.py`) |
| `lean_batch.py` | Lean `Packs n S*` for every exact form (`lean_cert.py --split`: data + chunk modules); results in `lean_batch/results.{tsv,md}`, generated Lean gitignored |
| (quadratic `S*`) | `lean_cert.py` also emits `packs_closed : Packs n (a + b * √d)` and `minSide_le_closed : minSide n ≤ a + b * √d` (generic lemma `lean/Sqpack/ExactQuad.lean`: rational check that the root of `pS` in `[Sa, Sb]` is `a + b√d`); list in `lean_batch/results.md` § Closed forms; committed example `Exact/N5c.lean` |
| `chain_lean.py` | band-lemma local-minimum certificates for the integer-side records (`lean/Sqpack/Exact/ChainUpTo82.lean`, `Exact/Chain/N*.lean`) |

## Method

1. **Contacts** (`find_contacts`).  Features: corner *a* of square *j* on side *k* of square *i*
   (`g = n_ik·(P_ja − c_i) − ½ ≥ 0`), corner on wall (`g = Px, S−Px, Py, S−Py`).  An incidence needs |g| < tol, a side
   line that separates the pair (all four corners of *j* outside it) and a corner projecting onto the side.
   Side–side contacts are two incidences (the two ends of the overlap segment; four when exactly aligned).
   Pure **corner–corner** touches (every incidence at a side end or ≤ 1e-4 past it, no side holding two corners: e.g.
   diagonal neighbours in an axis grid) are disjunctive and are set aside from the equations; they are checked by SAT
   afterwards and handled exactly in the MILP test (5).  The tolerance is chosen automatically: the smallest of 1e-9 …
   1e-6 for which the contacts admit an equilibrium (jam-LP dual residual < 1e-8, then a second pass at < 1e-7: at
   n ≈ 250–300, f64 round-off alone reaches ~1.5e-8).  If none does, the corner–corner MILP (5) is run on the input: a
   descent means "not a local minimum" (the input must be re-optimised first); otherwise "near side–side" incidences are tried (other
   corners of an already touching side within 1e-6 … 3e-3: nearly parallel sides whose angle has not converged in f64).
   A contact set whose equations are inconsistent (the projection in 4 stalls) is refused.
2. **Load-bearing set A** = max-support solution of the jam-LP dual: λ ≥ 0, Σ λ_k ∇g_k = ∇S (equilibrium with unit
   pressure), maximising the support (Goldman–Tucker: a contact is in A iff it can carry force in some equilibrium).
   Squares with no contact in A are **free** (rattlers or force-free).  It is recomputed at the exact point.
3. **KKT system.**  Unknowns: (x, y, θ) of the squares in the system, S, and λ.  Equations: g_b = 0 for an independent
   subset B of the closed contacts, and stationarity ∂S/∂v − Σ λ_b ∂g_b/∂v = 0 for every variable v.  This covers
   the rigid case (contacts fix everything, λ follows) and the under-determined case (the stationarity rows close the
   system: eliminating λ from them gives exactly David Ellsworth's nested Jacobian-determinant conditions
   [kingbird.myphotos.cc/packing/squares_in_squares__analytic_minimization.html]).  Over-determined/redundant contacts:
   B = rank-revealing QR subset (preferring large λ), the rest verified afterwards.  Exact flat directions (e.g. a square
   sliding between parallel sides) make the KKT Jacobian singular: the variable is frozen (dropped with its stationarity
   row, verified afterwards).  Force-free contacts that are closed (within tol) between squares in the system are kept
   closed too (otherwise a flat motion could open them into overlap).  Free squares that cannot be given positive
   clearance are promoted into the system.
4. **Solve.**  Minimum-norm Gauss–Newton projection onto an independent subset of the contact equations (rank-revealing
   QR; at degenerate configurations such as the (7+√7)/2 family, redundant contacts agree only to second order and
   projecting on all of them stalls at ~(input error)²; the rest are checked afterwards) (removes the f64 noise, ~1e-7 → 1e-70),
   then chord Newton on the KKT system: residuals in mpmath at `dps` digits, Jacobian (with analytic Hessians of the
   contact functions) in f64, LU per step.  Converges ~10–16 digits per step.  Free squares are then moved (iterated
   LP) to clearance ≥ 1e-6 where possible.
5. **Verification (numerical, high precision).**
   * redundant contacts and frozen stationarity rows: residual ≤ 1e-70 (dps 80);
   * every pair and wall: SAT gap in mp (active pairs ≈ 0, others reported with their minimum);
   * multipliers: LP over all λ ≥ 0 with J_Aᵀλ = e_S at the exact point: report max-min λ (> 0 ⇒ strict complementarity);
   * second order: Hessian of the Lagrangian (with that λ) on null(J_A); negative modes are tested against the critical
     cone (weakly active contacts, convex QP over zero modes) and against all valid multipliers (LP); **zero modes** are
     probed by moving 1e-3 along them and projecting back onto {g_A = 0}: an exact flat family converges with |ΔS| ≤ 1e-30;
   * first-order rigidity (squares with zero rows in null(J_A));
   * **corner–corner MILP**: min first-order dS over motions |z| ≤ 1 with every smooth contact linearised and every
     corner–corner touch as a disjunction (one binary per candidate separating line).  dS* = 0 ⇒ first-order jammed in every
     branch of the true (non-smooth) feasible set.
6. **Certificate** (`certificate`, `verify_cert.py`).  Scale the exact configuration about the origin corner by 1 + ε
   (ε = 1e-20): every gap grows by ≥ ε·(centre distance along the separating normal ≥ 1) and walls by ≥ ε/2.  Round
   centres to 10⁻³⁵ and rotations to rational t = tan(θ/2) (c, s) = ((1−t²)/(1+t²), 2t/(1+t²)), so c² + s² = 1 exactly;
   S' = S(1+ε) rounded up.  `verify_cert.py` checks with exact rationals: each square inside the open box, each pair
   with |Δc|² ≤ 2 separated by one of the 4 face normals (SAT), others by disjoint circumscribed discs.
7. **Algebraic identification** (`--algdeg D`): `mpmath.findpoly` on S (small coefficients only; see results).


   **Active-set step.**  Squares in exact flat motions can drift during the solve into a pair that was open (by more than
   the contact tolerance) at the input.  If the final SAT check finds such an overlap, that pair's incidences
   (|g| < 1e-4 at the input, both ends of a nearly parallel side contact) are added as equations and the solve is
   repeated (up to 4 times).  The multiplier LP at the exact point then decides whether the result is still a KKT point.

## What is certified exactly, and what only numerically

* **Exact (rational arithmetic, independent of the solver):** the certificate — n disjoint closed unit squares inside
  [0, S']², hence **s(n) ≤ S'**.  `verify_cert.py` is 80 lines of stdlib Python.
* **Numerical (mpmath, 80 digits; not interval arithmetic):** that S is (to ~70 digits) the value at an exact KKT
  point of the given contact structure; λ > 0; the second-order status; the flat-mode probe; the MILP jamming test
  (f64 LP/MILP at the high-precision point).  None of this is a proof of local optimality; an interval-Newton (Krawczyk)
  enclosure of the KKT root would be the next step toward a rigorous statement.
* Not addressed: global optimality, and second-order effects of corner–corner disjunctions.


## Test set

Columns: S exact = value at the exact KKT point (80 digits computed, 30 shown); certified S' = side of the exactly
verified rational certificate; free = squares carrying no force (rattlers / force-free); min λ = largest achievable
minimum multiplier over the load-bearing set (> 0: strict complementarity); 2nd order = reduced Hessian on null(J_A),
"exact flat modes" = zero modes verified to be exact motions at fixed S; MILP = first-order jamming with corner–corner
touches as disjunctions.  Inputs: site JSON (n = 5, 10, 11, 17, 71), the s(110) record before and after Couzo's
2026-09-27 improvement (rec110, couzo110: our independent rediscovery of his packing).

| input | n | S input | S exact (KKT point) | certified S' | free squares | min λ | 2nd order | corner-corner MILP |
| site5 | 5 | 2.7071067811865475 | 2.707106781186547524400844362104 | 2.707106781186547524427915429917 | [] | 1.25e-01 | PD (strict) | jammed |
| site10 | 10 | 3.7071067811865475 | 3.707106781186547524400844362104 | 3.707106781186547524437915429917 | [3, 7] | 6.25e-02 | PSD, 2 exact flat modes | jammed |
| site11 | 11 | 3.8770835900228142 | 3.877083590022814177307897060100 | 3.877083590022814177346667896002 | [] | 3.58e-02 | rigid (null J_A = 0) | jammed |
| site17 | 17 | 4.675530093604551 | 4.675530093604550951634111270483 | 4.67553009360455095168086657142 | [5] | 6.08e-03 | PSD, 3 exact flat modes | jammed |
| site71 | 71 | 8.9440715575703155 | 8.944071557570315506565203868717 | 8.944071557570315506654644584293 | [2, 22] | 1.87e-05 | PSD, 25 exact flat modes | jammed |
| **rec110** | 110 | 10.996793274019572 | **10.99679327395374924222302219937** | 10.99679327395374924233299013211 | [67, 77] | 5.80e-05 | PSD, 10 exact flat modes | jammed |
| **couzo110** | 110 | 10.996783403149346 | **10.99678339663159163950277843399** | **10.99678339663159163961274626795** | [77] | 1.08e-04 | PSD, 17 exact flat modes | jammed |

All 7 certificates check VALID with `verify_cert.py`.  Known values reproduced: s(5) = 2 + 1/√2 (`--algdeg` finds
2x² − 8x + 7), s(10) = 3 + 1/√2 (2x² − 12x + 17), s(11), s(17), s(71) to all 28–30 digits given on the site.  At 300
digits `--algdeg 16` finds for s(11) the irreducible octic
**x⁸ − 20x⁷ + 178x⁶ − 842x⁵ + 1923x⁴ − 496x³ − 6754x² + 12420x − 6865**.  No polynomial of degree ≤ 16 with
small coefficients was found for s(17), s(71), rec110 or couzo110 (150–200 digits).


## Limitations

* Local optimality is numerical (f64 LP/MILP/eigenvalues at an 80-digit point), not interval-certified.  Only the
  upper bound S' is exact.  Corner–corner disjunctions are handled at first order only (no branch-wise second order).
* The contact model needs a reasonably converged input.  Contacts open by more than 1e-6, or nearly parallel sides off
  by more than 3e-3 rad, are not recognised.  A wrong guess is caught (no λ ≥ 0, inconsistent equations, SAT
  violations, MILP descent) rather than silently accepted, but then no exact KKT point is produced.  In the batch this
  happened at n = 292 (n = 105, 130 resolved 10-05 evening, below).
* Jammed only with corner–corner touches (MILP: jammed in every branch, no smooth equilibrium): every branch is then
  jammed and has an equilibrium, so exactsolve takes one branch (each touch on its best separating line) as equations
  before trying near side–side incidences.  Second-order and KKT statements are for that branch.  (Added 10-05; n = 105.)
* If Newton's Jacobian turns singular near convergence (cond > 1e13 at residual < 1e-8: the independent contact subset
  chosen at the f64 input becomes dependent at the exact point), the subset is re-chosen at the current point, up to 3
  times (`kkt_resetups` in the JSON).  (Added 10-05; n = 130.)
