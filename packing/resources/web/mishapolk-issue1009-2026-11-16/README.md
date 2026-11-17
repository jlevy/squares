# Polkovskyi’s Thirteen Certificates at b637e6c

This packet retains part of
[Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records/tree/b637e6cf59c23781c813e8442bfdccb5aa5f3954)
at `b637e6cf59c23781c813e8442bfdccb5aa5f3954` (committed 2026-11-16T23:31:56Z), the
repository’s head and the commit
[issue #1009](https://github.com/jlevy/squares/issues/1009) names, opened at 23:38:22Z by
Mykhailo Polkovskyi (Mishapolk).
Intake lane c-import-1009-1117 (bead think-i38n) fetched it at 01:40Z on 17 November
2026, when `git ls-remote` read the same head.

GitHub’s activity log for the repository, read here, shows how the commit was published.
At 23:27:18Z a push moved `main` from `52aa267`, the last read, to `b9b7fa7a01` (committed
23:27:09Z, parent `52aa267`), and at 23:32:03Z a force-push replaced it with `b637e6c`.
`b9b7fa7` holds the 13 certificates, the 13 Witness/v2 files, both `SHA256SUMS` lists,
the figures and the two new verifiers byte for byte as `b637e6c` does.
It differs only in `SUBMISSION_2026_11_16.md`, whose heading and prose were rewritten,
and in the two indexes, whose generated times differ and whose credit at the 13 counts
read “Mykhailo Polkovskyi after” each standing holder in `b9b7fa7` and “Mykhailo
Polkovskyi (Mishapolk)” in `b637e6c`. `b9b7fa7` is on no branch now; it was fetched by
its id. So the certificates were first committed at 23:27:09Z and first public at
23:27:18Z, 11 minutes before the issue, and the pin stays `b637e6c`, the commit the
issue names.

Intake lane c-import-1009-1117 retained, replayed and measured it on 17 November 2026
and registers it as **T-314** to **T-326**, one result a count.
Eight stand at V3/C3 on the replay; the five refinements at 156, 180, 270, 299 and 307,
each at its house’s padding, are held at V0 for the owner’s RV-3 question
(think-ruu2), as T-280, T-285 and T-286 are.
The blind stage 4 review is lane R2 (think-evxy).

## What the Source Claims

- **Thirteen certificates.** `certificates/0000-0999/nN.cert` states each packing in
  Evan Daniel’s format, `n S` and then one `x y t` row a square, centres in `[0, S]²`
  and `t` the tangent of half the rotation, all exact rationals; the issue calls it the
  Weierstrass form, since `(1 − t²)/(1 + t²)` and `2t/(1 + t²)` make each rotation
  exact. `witnesses/2026-11-16/n-N.yaml` states the same packing as a
  `packing.squares:Witness/v2` document of rational corners.
  The issue prints each side rounded up at 12 places and lists both files’ SHA-256,
  which match the retained files and both `SHA256SUMS` lists.
- **Two parts.** Part A, seven lowered upper bounds: new arrangements at 210, 262,
  272, 292 and 295, and improved packings at 260 after Evan Daniel and at 268 after
  Doğa Özden. Part B, six “exact rational refinements lowering the 12-place print
  (subject to RV-3)” at 147, 156, 180, 270, 299 and 307, refinements of the registered
  arrangements whose credit the issue leaves with the standing authors.
- **The earlier reports.** At 262 and 295 the issue says each side lies below #1007,
  and at 292 below #1005 and #1006; `verify_algebraic_bounds.py` states #1007’s and
  #1006’s exact sides, which this lane read again from their pins and found equal.
- **The checkers.** It says `verify_bound_certificate.py --strict` (Evan Daniel’s
  separating-axis verifier as Francisco Couzo modified it) and `verify_area_exact.py
  --strict` (the author’s exact polygon-clipping verifier, sharing no geometry code with
  it) accept every certificate in Fraction arithmetic, and that this repository’s
  `check_rational_witness_independent.py` at `f9ddfeeef` reports VERIFIED on every
  Witness/v2 file. No source program ran here.
- **Not claimed.** No formal optimality proof and no minimal polynomial.
  The issue says the packings were “Discovered by Mykhailo Polkovskyi, assisted by
  Gemini”.

## Retained Here

Under `source/`, at their upstream paths:

- the 13 certificates the issue names, `certificates/0000-0999/nN.cert` for N in 147,
  156, 180, 210, 260, 262, 268, 270, 272, 292, 295, 299 and 307;
- the 13 Witness/v2 corner files of the same packings, `witnesses/2026-11-16/n-N.yaml`,
  and their `SHA256SUMS`;
- `SUBMISSION_2026_11_16.md`, and the two new verifiers `verify_area_exact.py` and
  `verify_algebraic_bounds.py`, as data: neither was run here.

Pinned by digest in `acquisition/sources.json`, not copied: the MIT `LICENSE` (against the
issue-732 packet’s copy), the `README.md` (against the issue-846 packet’s), Evan Daniel’s
`verify_bound_certificate.py` and `BOUND_VERIFIER_LICENSE.txt` (against the issue-678
packet’s), `certificates/SHA256SUMS` over the whole repository, the two indexes
`certified_bounds.json` and `upper_bounds.json`, and the 13 figures under
`figures/2026-11-16/`.

## Against the Record

Each certificate is read by the `evand-cert` reader, held to its Witness/v2 file by the
`witness-corners` reader, and admitted at the issue’s print
(`acquisition/claims.json`). Each lies below its house; at 295 the house is T-193’s
exact form (22 + 22√2)/3, compared by one exact sign against its number field.
The margins and identities below are `devtools.contraction_margin` and
`devtools.measure_identity` receipts under [measure/](measure/); at 295 the
measurements are against T-146’s rational certificate of the arrangement T-193 solves.

| n | Print | House | Gain | House margin | Gain / margin | Identity against the house | Disposition |
| ---: | --- | --- | ---: | ---: | ---: | --- | --- |
| 147 | 12.651043553173 | T-302 | 3.415e-09 | 2.934e-09 | 1.1639 | not one to one, 8 beyond 0.1, largest 0.647942 | further arrangement, S2 |
| 156 | 12.977053087495 | T-287 | 2.589e-12 | 2.417e-12 | 1.0709 | one to one, 0 beyond 0.1, largest 1.44264e-05 | held for RV-3, S1 |
| 180 | 13.915618502788 | T-288 | 2.710e-12 | 2.584e-12 | 1.0485 | one to one, 0 beyond 0.1, largest 1.42864e-05 | held for RV-3, S1 |
| 210 | 14.971214601589 | T-174 | 1.787e-03 | 0.000e+00 | – | not one to one, 61 beyond 0.1, largest 0.973003 | new arrangement, S3 |
| 260 | 16.633520939840 | T-269 | 1.105e-08 | 1.662e-11 | 664.8643 | one to one, 0 beyond 0.1, largest 0.039705 | further arrangement, S2 |
| 262 | 16.698115018700 | T-101 | 8.992e-03 | 1.671e-19 | 5.38e+16 | not one to one, 78 beyond 0.1, largest 0.89057 | continues #1007, S3 |
| 268 | 16.871868135103 | T-289 | 1.617e-04 | 3.204e-12 | 5.05e+07 | not one to one, 10 beyond 0.1, largest 0.809253 | continued arrangement, S3 |
| 270 | 16.928148603340 | T-283 | 3.247e-12 | 3.212e-12 | 1.0111 | one to one, 0 beyond 0.1, largest 1.44264e-05 | held for RV-3, S1 |
| 272 | 16.965501175831 | T-174 | 8.530e-05 | 0.000e+00 | – | not one to one, 36 beyond 0.1, largest 0.932553 | new arrangement, S3 |
| 292 | 17.590016439231 | T-146 | 1.362e-03 | 1.759e-19 | 7.74e+15 | not one to one, 70 beyond 0.1, largest 0.931284 | continues #1006, S2 |
| 295 | 17.698115018700 | T-146 (T-193) | 6.118e-03 | 1.770e-19 | 3.46e+16 | not one to one, 203 beyond 0.1, largest 1.11945 | new arrangement, S3 |
| 299 | 17.801004434252 | T-277 | 3.527e-12 | 3.404e-12 | 1.0361 | one to one, 0 beyond 0.1, largest 0.00102118 | held for RV-3, S1 |
| 307 | 17.979230960384 | T-279 | 3.478e-12 | 3.419e-12 | 1.0174 | one to one, 0 beyond 0.1, largest 1.41421e-07 | held for RV-3, S1 |

The other reports at these counts: at 262 the certificate is 1.578 × 10⁻³ below
#1007, at 295 also 1.578 × 10⁻³ below #1007, at 292 8.778 × 10⁻⁵ below #1005 and
3.616 × 10⁻⁹ below #1006, and at 299 2.345 × 10⁻¹² below T-280, Kaelan Yim’s held
re-solve of T-277.
The [ledger of 17 November](../../../campaign/issue-intake/upper-bounds-1009-20261117/README.md)
records every claim of #1009 in report order, after #1005, #1006 and #1007.

## Exact Replay

`upper_bound_reports certify` ran 39 jobs, a positive, a duplicate square and a square
moved outside the box at each count, through both maintained exact routes: all as
required, 2,490,354 pair decisions and 599.51 route CPU seconds (7 minutes 34 seconds
of wall on two workers), one receipt a count under [receipts/](receipts/); `check
--replay` admitted all 39 again.
Every certificate clears every wall by exactly 10⁻²⁸, and every pair by at least
2 × 10⁻²⁸, with 1.4449 × 10⁻²⁴ at 180, 1.7763 × 10⁻²⁰ at 295 and 4.2379 × 10⁻¹⁵ at
292, equal on both routes; the issue’s table states the same.

The sharp controls (`receipts/sharp-controls-nNNN.json`) went to exact contact and
10⁻³⁰ past it, as a plan stated before any ran (SHA-256 `49270cac…f97142`, on
think-i38n at 01:59:51Z): every wall and pair margin lies above 10⁻³⁰, so no square
touches, and each enlargement closes its one pair or wall alone.

## Pose by Pose and Padding

- **The refinements.** At 156, 180, 270 and 307 nearest centres pair the certificate one
  to one with its house’s packing and no square moves by 10⁻³; at 299 one square moves
  by 1.02 × 10⁻³. Each gain is 1.01 to 1.07 times the house’s own uniform-contraction
  margin, and the house contracted rounds up at 12 places to the claim’s own print, so
  the gain over the padding lies within the print: RV-3’s class, held as at T-285 and
  T-286.
- **147.** No symmetry pairs the certificate one to one with T-302’s packing, and 8
  squares move beyond a tenth; the gain is 1.16 times T-302’s margin and the side rounds
  up below T-302 contracted, so it is more than the padding.
- **260 and 268.** At 260 the certificate is one to one with T-269’s packing, none
  beyond a tenth and 10 beyond a hundredth, 665 times T-269’s margin; at 268 not one to
  one with T-289’s, 10 beyond a tenth. Further arrangements of each, as the issue says.
- **210, 272, 262, 292 and 295.** New arrangements relative to the record’s packings.
- **Against the earlier reports.** The 262 certificate is one to one with #1007’s
  packing under a box symmetry, 3 squares beyond a tenth; the 292 certificate is one to
  one with #1006’s, 3 beyond a tenth. The issue calls both new and names neither, so the
  register keeps its credit and the owner decides (think-m8ex). The 295 certificate is
  not one to one with #1007’s.

## The L Step

[measure/l-step-scan.json](measure/l-step-scan.json) is `devtools.l_step_scan` with the
13 sides stood in for their ceilings.
It drops main’s sub-print L-step consequences into 262 and 292 and adds one: 295 from
this release’s 262, 5.93 × 10⁻¹⁹ below its own 295 at the same 12-place print.
The 295 side is the 262 side plus 1 and 5.93 × 10⁻¹⁹, but no strip of 33 squares lies
along two sides of its box, so `measure_identity`’s L-base reader refuses it as an L
step on the 262 certificate.

## What Is Not Established

- The source’s verifiers were not run; the issue’s statements about them are its own.
- Whose arrangement the 262 and 292 certificates continue is measured, not stated by
  the source (think-m8ex).
- No local optimality, rigidity, KKT or global optimality is established for any
  certificate.

## Credit and Licence

MIT, copyright (c) 2026 Mykhailo Polkovskyi, by `LICENSE` at the pin, whose grant on
#719 covers the certificates. The key `[Mishapolk issue 1009 2026-11-16]` credits
`Polkovskyi after Ozden, Daniel, Ono, ntumlnoob, Couzo, Levy`: the standing authors of
the packings the refinements re-solve and the improvements continue, and this project,
whose houses they re-solve and whose independent corner checker the author ran.

## Commands

From `packing/`, with the project interpreter:

```bash
P=mishapolk-issue1009-2026-11-16
M=resources/web/$P/measure
python -m devtools.acquire_source $P --checkout CHECKOUT
python -m devtools.acquire_source $P --check
python -m devtools.upper_bound_reports $P check-claims --write
python -m devtools.upper_bound_reports $P certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports $P check --replay
python -m devtools.upper_bound_reports $P sharp-controls
python -m devtools.measure_identity --n 147 "POLK=packet:$P" 'T-302=packet:ono-issue985-2026-11-14' \
  'regularized=witness-center-basis:atlas/known-best/regularized/n-147-regularized.yaml.gz' \
  'house-witness=witness-center-basis:witnesses/known-best/n-147.yaml' --out $M/identity-n147.json
python -m devtools.contraction_margin --n 147 'T-302=packet:ono-issue985-2026-11-14' \
  --against "mishapolk-1009=packet:$P" --out $M/contraction-n147.json
python -m devtools.contraction_margin --n 147 "mishapolk-1009=packet:$P" --out $M/contraction-n147-own.json
python -m devtools.l_step_scan --with 147=... --with 156=... (all 13) --out $M/l-step-scan.json
```

The other counts’ commands differ only in the count and the house’s packet; the
regularized views at 210, 272 and 307 are read by `witness-corners`, and 262 and 295
have none. At 262 the house is T-101’s `evand-cert` certificate at
`resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-262.cert`,
and at 295 T-146’s packet `evand-regularized-2026-10-10`.
#1005’s, #1006’s and #1007’s certificates were read from their pins in scratch
(`center-direction-json` and `witness-corners`); each `--with` names the exact side
`acquisition/claims.json` records.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
