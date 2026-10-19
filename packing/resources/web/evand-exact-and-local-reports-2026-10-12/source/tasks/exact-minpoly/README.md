# Exact forms for the best-known packings, n ≤ 324 (opened 2026-10-06)

**Deliverable (Evan, 10-07).**
1. A table of analytically derived exact forms of S for the register records.
2. A handful of Lean proofs of local optimality.

That table and those proofs are the first publishable unit; full coverage is not required.  n = 83 (degree 672) was
the benchmark for the symbolic route.  It is now optional: drop it and the other hard cases if they stay hard, and
formalize further instead.  Citable from the eventual s(11) explainer (`notes/local-optimality-explainer-draft.md`).

## Deliverable per n

1. `p ∈ ℤ[x]`, irreducible and primitive, and rationals `a < b` with exactly one root of `p` in `[a, b]`: `S* :=` that
   root.
2. An exact configuration over `K = ℚ[t]/f(t)` (`f` irreducible, real root `t*` in an isolating interval).  Each
   square's `(x_i, y_i, c_i, s_i)` and `S` lie in `K`, with `c_i² + s_i² ≡ 1` and `p(S(t)) ≡ 0 (mod f)`.  The contact
   list is part of the data.
3. Checks independent of how the data was produced (msolve, LLL, ...): contacts ≡ 0 mod f (exact); every other pair
   separated and every square inside the container (intervals at `t*`); `S(t*) ∈ [a, b]`.  This gives `s(n) ≤ S*`
   exactly.
4. Cross-checks: `S*` matches `S_exact` in `search/exact/batch/results.json` (80 digits); the degree matches independent
   sources where they exist.

The polynomial for S depends only on the contact structure.  The placement of rattlers and flat families (below) only
changes the field the coordinates live in.

## State (10-07)

**269 of 324 verified** (`search/exact/minpoly/results.md`; 10-07 evening: + 53, 106, 129, 177 from settling flat
angle directions).  That is all 176 axis-parallel records (S an integer) plus 93 tilted ones, up to field degree 48.
Field degrees: 1: 182, 2: 61, 4–8: 12, 16–48: 14.  **86 cross-checks agree, none differ** (findpoly on the 68-digit
values; Ellsworth's degrees, now including 129).  255 of the 269 have field degree ≤ 8.

Open (55); below 83 only 29, 55, 68, 71 remain:

| group | # | n | what it needs |
|---|---|---|---|
| many angle classes, large system (timeout) | 26 | 103, 105, 110, 131, 132, 154–156, 180, 181, 208–211, 238–241, 263, 270, 272, 273, 302, 304, 306, 307 | block-triangular (Dulmage–Mendelsohn) elimination: rigid clusters in dependency order |
| force balance in > 1 angle direction | 11 | 88, 123, 130, 172, 179, 199, 236, 237, 259, 269, 297 | multi-direction Lagrange conditions (today: one direction, a determinant) |
| flat rotation parallel to fixed squares (rest) | 6 | 207, 268 (Lagrange determinant ≡ 0), 271, 305 (timeout), 301, 303 (12G cap) | 53, 106, 129, 177 done by pinning flat angle classes |
| msolve too slow or fails | 9 | 29, 55, 68, 71, 83, 126, 182, 228, 235 | genuinely large systems, not a factor-choice problem (below); 83 also needs force balance |
| field too large | 2 | 108 (field 144), 206 (field 56) | — |
| no exact point | 1 | 292 | packer agent, 10-07 (`search/packer/s292.md`) |

Ellsworth publishes polynomials for some open n (83, 88, 108, 129, 179, 235): the table can cite those, marked as
cited rather than derived.

### Local optimality (grades from exactsolve's checks over the register)

The notion is `IsLocalMinPacking` (`lean/Sqpack/LocalMin.lean`): a pose-space ball around the record contains no
packing in a smaller square.

* **A** (20): first-order rigid with all forces > 0.  These are n = 1, 11, 28 and the perfect squares.  The
  certificate (`localmin.py`) has exact λ ∈ K with Σλ L = e_S, λ > 0, a rational G with ‖GL − I‖ ≤ 1/2, and margins.
  It is valid for n = 11 and 28.
* **B** (1): n = 5, strict only at second order.
* **C** (295): strict modulo flat motions.  The paper proof is in `grade-C.md`.  Exact certificate `gradec.py`
  (10-11; exact in K, signs by intervals; hypothesis 2 via affine null vectors, `grade-C.md` §Hypothesis 2): VALID for
  233 of the 250 records with field degree ≤ 4; the other 17 timed out at 30 min (large flat families).  Field degree
  > 4 and n = 29 (degree 7213): not yet (n = 29 plan in `search/exact/homotopy/N29.md` §Pickup).
* No strictly positive forces: 177, 211, 230, 261, 263.  230 and 261 are VALID once their zero-force rows are dropped
  (`GRADEC_DROPZERO=1`, a relaxation); 177, 211, 263 not tried (field degree > 4).  Out of scope: 272 (not a local
  min), 292.
* The definition fails on broad plateaus with a far downhill exit (s(7)'s L arrangements); accepted for now.

### Lean (`lean/Sqpack/`, no `native_decide`)

* `ExactPack`, `ExactCheck`: exact data ⇒ `Packs n S*` (kernel `decide` over ℚ[T]/f).  Instances: `Exact/N5c`, `Exact/N11c`.
* `LocalMin`, `LocalMinRows` (`isLocalMin_of_rows`), `LocalMinCheck` (soundness `isLocalMin_of_lcert`).  Instance:
  `Exact/N11L`, the s(11) record is a local minimum (kernel-checked, standard axioms).
* `Exact/N28L`: **the s(28) record is a local minimum** (10-07; kernel-checked, standard axioms).  `Exact/N17c`: the
  exact s(17) packing.  Both outside the default build (`lake env lean Sqpack/Exact/N28L.lean`).
* `ChainLocalMin` (10-07, `chain-lemma.md`): **every integer-side record is a local minimum**, by a band lemma (k
  squares meeting one horizontal line force side ≥ k; no multipliers).  `Exact/N8Chain` (default build) and
  `Exact/ChainUpTo82` (all 53 integer-side records n ≤ 82, ~92 s, outside the default build); generator
  `search/exact/chain_lean.py`.
* `ShadowCheck` (10-07): general rational-shadow validity checker, independent of number fields.  Per-square rational
  enclosures of (x, y, c, s); far pairs by a disc test (centres ≥ √2 apart); near pairs and walls by interval
  arithmetic; `packs_of_shadow` takes an exact proof only where those fail.  `ExactCheck` proves each enclosure
  once in the field (`enclOK`) and falls back to field arithmetic per wall/pair (`boxOKx`, `pairOKx`).  At n = 28
  only 52 of 378 pairs and 16 of 28 walls need the field.
* Compile cost (10-07, `lake env lean`, peak RSS):

  | file | before | sparse G | + shadows |
  |---|---|---|---|
  | N11L | ? | 52 s / 9 GB | 48 s / 9 GB |
  | N17c | 402 s / 15.6 GB | | 112 s / 14 GB |
  | N28L | killed > 40 GB | 185 s / 18 GB | 152 s / 17 GB |

  The old N28L was dominated by the dense left-inverse check (`G_ok` > 40 GB; `bnd_ok` 25 GB, `Gn_ok` 15 GB):
  dense `![…]` table lookups, not field arithmetic.  Now: G as lists, the linear parts as sparse rational midpoints
  plus one radius ε, the G check as sparse dot products plus (3n+1)·Gn·ε.  What remains at n = 28 is mostly
  the local-min rows and the ~1100 field conditions; ~6 GB is the baseline for loading Mathlib and the data.

## Next (10-07)

1. **Table**: n, S* (30 digits), p (or its degree and height plus a link), field degree, and how it was obtained
   (derived / derived + cross-checked / cited).  Cover the 265, plus cited polynomials where we have them.  A site page
   and/or jlevy (#375 thread); ask Evan before posting.
2. **Lean local minima, a handful**: n = 11 and 28 (grade A) done.  Next grade B (n = 5, a second-order lemma), then
   one grade C (n = 10 or 19, field degree 2): the exact certificate exists now (`gradec.py`, 10-11).
   Packing-only Lean certificates for the field-degree ≤ 8 records (254) are now cheap enough to batch.
3. Coverage, by cost: flat-rotation rest (6), multi-direction force balance (11), then block-triangular elimination
   (26 + most of the msolve-hard ones).  n = 83 only if it falls out.

## Numerics: what is it needed for? (Evan's question, 10-07; to revisit)

* **Finding the contact graph**: an optimizer must reach a jammed / locally optimal configuration first.  This is
  the essential use.
* **Choosing the root**: the contact system's real solutions include mirror images, other angle branches and
  overlapping configurations; the eliminating polynomial factors, and only one root of one factor is the
  record.  This needs only a coarse t*: isolate every candidate factor's real roots exactly (flint) and take the
  interval containing t*.  `verify_exact.py` then checks the configuration exactly, so a wrong pick cannot pass.
* **Done (10-07)**: `minpoly.py` picks the univariate factor (k = 1) and msolve's root (k ≥ 2) by exact real-root
  isolation (`pick_root`: flint's certified root balls, refined until one candidate maps to t*; it fails loudly
  otherwise).  Regression: 5, 10, 11, 17, 37, 39, 51, 87, 102, 202 give the same polynomials and verify.
* **n = 29, 68, 71, 126, 228 were not a factor-choice problem.**  Their "k factors vanishing at t*" are k
  *multivariate* polynomials in k class parameters (n = 29: 5 in t1..t5, total degrees 12–26, up to 2773 terms),
  which together cut out t*: that is the expected input to msolve, not an ambiguity.  msolve times out (600 s);
  even its F4 run mod a single prime had not finished after 15 min.  Shortcuts tried at n = 29: (a) no small
  subsystems: every dependency at t* involves ≥ 99 of the 152 contact rows; (b) resultants explode (eliminating t5
  alone: total degree 112, 431k terms); (c) LLL on S and t1 refined to 15000 digits finds no relation of degree
  ≤ 120 with height ≤ ~120 digits, so the field degree is probably > 120.  These need the block-triangular work or a
  much better solver.
* **n = 55**: S depends only on t5, t6; the Lagrange determinant of the 5 consistency factors has total degree 85
  and 5.7M terms, and msolve fails on it.  A multiplier formulation (11 variables) is the next thing to try.
* Open question: work purely from contact graphs (e.g. perturbations of known graphs), with every real root a
  candidate and validity / local optimality checked exactly: a combinatorial search, different from the record
  pipeline.

## Tools (`search/exact/`, run via `./env.sh`)

`env.sh` pins numpy 2.4.2, scipy 1.17.0, python-flint 0.9.0, and msolve from nixpkgs.

* `exactsolve.py` → `NAME.contacts.json` (closed contacts, load-bearing set, corner-corner touches, free squares).
* `minpoly.py`: the number field, the exact configuration and the minimal polynomial of S.
  * Angle classes (parallel or mirror mod 90°, t = tan(θ/2)); centres eliminated over ℚ(t₁..t_k).
  * k = 1: gcd of the consistency numerators.  k ≥ 2: their irreducible factors through t*, then msolve's
    parametrization.
  * Force balance when the contacts leave one direction (Lagrange determinant).
  * Flat directions settled on near-contacts, then pinned at 30-digit rationals; angle classes S does not depend on
    are pinned too when more than one angle direction is left.
  * Factor and root choice by exact real-root isolation (`pick_root`).
  * Refuses invalid exactsolve points.
* `verify_exact.py`: an independent stdlib checker (exact identities mod f, rational intervals).  It does not trust
  msolve, whose ℚ arithmetic is multimodular.
* `minpoly/solve_all.sh`, `minpoly/run_minpoly.sh` (systemd MemoryMax caps; the machine is shared), `minpoly/summary.py`
  → `minpoly/results.md`.
* `localmin.py` (grade A certificates); `lean_cert.py`, `localmin_lean.py` (Lean certificates).

## Cross-check sources

* **Ellsworth's page** (https://kingbird.myphotos.cc/packing/squares_in_squares.html; checked 10-06).  It gives
  polynomials for every record of degree ≥ 3, in a hidden `<span class="frames">`, some over ℤ[√2].  n = 83's is a
  Mathematica `Root[…]` in the comment of `square-83.svg`.  Raw downloads: `private/downloads/kingbird-2026-10-06/` (not
  republished).  Parse and verdicts: `results/kingbird_crosscheck.json` (`proto/parse2.py`, `proto/cmp.py`).
  * 22 agree: 11, 17, 28, 37, 39, 41, 51, 69, 70, 83 (degree 672), 87, 88, 108, 128, 129, 146, 153, 179, 205, 235,
    266 (register's), 300.
  * 12 describe an older packing (Couzo's 2026-09/10 records are newer than the page): 102, 106, 123, 130, 172, 177,
    199, 206, 228, 259, 269, 302.
* The register's frontier `minimal_polynomial` fields are older snapshots of Ellsworth's page and add nothing
  independent.
* `mpmath.findpoly` on the 68-digit `S_exact` (`results/findpoly68_tilted.txt`) is our own, but independent of the
  contact graph.

## Canonical placement for non-rigid packings (Evan, 10-06)

* Make as many squares as possible axis-parallel or parallel to an existing angle class.
* Make as many side-to-side contacts as possible.
* A square sliding between a side-to-side contact and a corner contact goes to the side-to-side end.
* Rattlers: rotate to a neighbour's or the grid's angle if they fit, then push them to two side-to-side contacts.

Settling adds equations and usually lowers the field degree.  `minpoly.py` currently settles on near-contacts and pins
the rest at rationals: valid, not yet canonical.  The tie-break order is still to be fixed.

## History and pitfalls (10-06 prototypes in `proto/`; they hard-code scratch paths)

* LLL at high precision (`proto/lll2.py`) found n = 17 (degree 18) at 2000 digits.  It is useless beyond degree ×
  height of a few thousand digits (n = 83 would need ~5·10⁵).  It needed exactsolve's precision fix (residuals
  underflowed f64 below 1e-308), which is now in `exactsolve.py`.
* Gröbner bases on the raw system without angle classes blew up at degree 5 (a 171k × 211k matrix).
* msolve needs integer coefficients (`c12/2` came back as "no solution").  It picks a separating linear form when S
  repeats across solutions, so a resultant is needed.
* `findpoly` with `maxcoeff = 10⁶` missed n = 37 (coefficients ~10⁸).  The 68-digit files support identification only
  up to degree ~12.
