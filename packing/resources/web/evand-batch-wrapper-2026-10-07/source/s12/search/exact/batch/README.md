# batch — exact KKT points and certificates for every record in jlevy's register (2026-10-05)

**What.**  For every n = 1–324 in [jlevy's register](https://jlevy.github.io/squares/) we took the known-best packing
(the register's `witnesses/known-best/n-N.yaml`), solved for the nearby exact KKT point of *min S subject to
non-overlap* with `../exactsolve.py` (80 digits), and wrote an exact rational certificate `certs/n-N.cert` of
`s(n) <= S'` (`S' - S ~ 1e-19`).

**Result** (`results.md`, `results.json`; summary as of the final run):
* 323 of 324 certified; both independent exact verifiers accept every certificate (`./verify_all.sh`).
* 317 are numerically KKT local minima: multipliers λ ≥ 0 at the exact point (equilibrium residual 0), reduced Hessian
  PSD/PD modulo exact flat motions, first-order jammed in every corner–corner branch.  6 are certified bounds only
  (n = 177, 211, 230, 261, 263, 272: zero or no multipliers, or negative curvature in a flat direction).
* **Every n ≤ 291 is certified; every n ≤ 176 is a KKT local minimum.**
* 50 certified S' lie below the register's printed value, by 3e-13 … 5e-11: the analytic optimum of the same packing (the
  f64 slack removed), not a new structure.  Most are Francisco Couzo's packings of 2026-09-27 and 2026-10-03.
* Records already in closed form agree with S' to ~1e-15 or better (e.g. the (7+√7)/2 family n = 18, 53, 86, …).
* n = 292 (added 2026-10-07): the slp2 polish with square 0 (top-left corner) set to exactly 0°; at ~1e-6 rad its corner-on-corner touch gave a spurious load path and a nearly singular contact subset, so exactsolve stalled.  Log: `../../packer/s292.md`; the failed run is kept as `work/n-292/failed_polished.*` (gitignored).  Now 324/324.
* n = 105 and 130 added 10-05 (evening) after two exactsolve fixes: at n = 105 the register witness is not a local minimum
  (a first-order descent with corner–corner touches as disjunctions); its slp2 polish is jammed only with corner–corner
  touches as equations (one branch), and is a KKT local minimum there.  At n = 130 Newton's Jacobian turned singular near
  convergence (the independent contact subset chosen at the f64 input became dependent); exactsolve now re-chooses it.
* Curiosity: s(172) ≤ 13.6189889568993984289… and s(199) ≤ 14.6189889568993984290…, exactly 1 apart.

**Inputs** (`inputs/n-N.txt`, the exact file each certificate was solved from).  Column *input* in `results.md`:
`W` = the register witness converted to our text format (centres, angle in degrees mod 90); `P` (17 records) = that
witness polished by our SLP squeeze (a local optimizer, not yet published).  A `P` input is just an f64 packing: the
certificate's validity does not depend on how it was produced.

**Checking.**
```
./verify_all.sh                 # both exact verifiers on all 323 certificates (~2 min)
./reproduce.sh [-j 8] [n ...]   # re-solve from inputs/ and compare with certs/ byte for byte (~1-2 CPU-hours for all)
```
`../verify_cert.py` (separating axes) and `../verify_cert2.py` (vertex-in-polygon and edge-intersection tests) share no
geometry code; both are stdlib Python with exact rationals.  Both were written by the same author and agent as the solver.

**Data.**  Register data: CC BY 4.0, Joshua Levy, the squares project; local clone of 2026-10-03, with the frontier files
and 10 witnesses that changed by 2026-10-05 (n = 69, 83, 87, 208, 209, 228, 263, 272, 303, 306) fetched from GitHub on
2026-10-05.  The packings are their finders' (named in `results.md`); a certificate here is an exactly verified copy of the
same packing at its analytic optimum.

`register.py` (reads the register data), `summarize.py` (builds the tables, runs both verifiers).
