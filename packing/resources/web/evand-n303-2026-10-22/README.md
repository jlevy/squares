# Evan Daniel’s s(303) Certificate

[Issue #728](https://github.com/jlevy/squares/issues/728) reports an exact rational
packing of 303 unit squares, in
[evand/square-packing](https://github.com/evand/square-packing/tree/f06521f4bde9e379a91c1ea88053f3e43df8ede5/search/packer/candidates).
The packet pins the commit the issue names,
`f06521f4bde9e379a91c1ea88053f3e43df8ede5` (tree
`b1cd5bd9088267fb8b77e560f9583d08d0e03a7c`, authored 2026-10-22T17:09:55Z, committed
2026-10-22T17:14:52Z), which adds the three n = 303 files and nothing else.
No earlier commit on any branch names them.
The issue was filed at 2026-10-22T17:17:20Z, 148 seconds later.
The sources were retrieved on 22 October 2026, when the branch head was `7982d7a`; that
commit changes only Lean files, and its certificate is the same blob.

| n | Exact side of the certificate | The issue prints, rounded up | Rounded up at 16 places |
| --- | --- | --- | --- |
| 303 | `447744305431858194305431410441/25000000000000000000000000000` | 17.909772217275 | 17.9097722172743278 |

The side is exactly 17.90977221727432777221725641764.
The certificate, `s303_r303w0.cert`, gives 303 unit squares, each a rational centre and a
rational $t = \tan(\theta/2)$, in an open square of the stated side, in the format of
issues #489, #552, #659, #664, #669, #674, #680 and #689.
It is a dilation certificate, made by `search/packer/dilate_cert.py` as the n229
certificate of #674 was: the binary64 packing in `s303_r303w0.input.txt` (side
17.909772217256418) has its centres and box scaled by $1 + 10^{-12}$, its coordinates
rounded to rationals and each angle rounded to a rational half-angle tangent, so every
square is exactly unit.
The commit also holds the pipeline’s report, `s303_r303w0.json`. The claim rests on
`s303_r303w0.cert`.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of a blobless clone at
the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
17 files, 292,316 bytes, of which 8 files and 107,752 bytes are retained.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `search/packer/candidates/s303_r303w0.cert` | `c4bda0b40aebde7fc2d83354bc71f1f0429e6bb2` | 42160 | `929c2acf72ee54a1850183fc149f06dbf35bffa2f7ee68c8f833d888400e8080` |
| `search/packer/candidates/s303_r303w0.input.txt` | `d1a5b152e7e7f2c512c23a6d055047a6a6c39d89` | 15084 | `8167bcb37498ded1029f8fea6b13665f59806cfb0a2beb750388852452f107b7` |
| `search/packer/candidates/s303_r303w0.json` | `4b618f400113eaf4bd612aeadbad111ff4b1bf8d` | 2743 | `36d033db66991743d92f3dc2a370fe018d5ad328ffa6b67315621c58c5bdf910` |

The first two digests are the ones the issue prints; it prints none for the report.
Beside the three files the packet retains `LICENSE`, `CREDITS.md`, the root `README.md`,
and the format and packer READMEs.

Pinned by digest only:

- **The source’s two checkers and the dilation producer.**
  `search/exact/verify_cert.py`, `verify_cert2.py` and `search/packer/dilate_cert.py` are
  byte-identical to the copies the
  [n229 packet](../evand-n229-dilation-2026-10-17/README.md) retains, and were not run.
- **The exact solver.** `search/exact/exactsolve.py`, whose not-jammed verdict and
  corner-to-corner MILP the issue reports, is byte-identical to the copy the
  [n183 packet](../evand-n183-subgrid-2026-10-19/README.md) retains.
- **The discovery code the issue names.** The basin explorer `search/packer/explore.py`
  (not the copy the n183 packet keeps; it has changed since), the near-record sweep
  `search/packer/dgen.py` and the band flip `search/packer/bandflip.py`.
- **The report’s producer and the distance.** `search/packer/candidate.py`, which wrote
  `s303_r303w0.json`, and `search/packer/pk/crossing.py`, which defines the matching
  distance the issue prints.

## Exact Replay

The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, as the #659 to #689 imports did: `sqpack`’s exact
witness verifier and the independent rational corner checker
(`devtools.check_rational_witness_independent`), each deciding every wall and every pair
over $\mathbb{Q}$ after an exact half-angle conversion.
The count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on two workers.

The positive passes both routes, and both routes refuse both controls: the duplicate
square as an overlap of squares 0 and 1, and the translated square as outside the
container.
Every wall is cleared by at least `60480000000010479/10^29`
($6.048 \times 10^{-13}$) and every pair by at least $1.2045 \times 10^{-12}$, on both
routes, as a $10^{-12}$ dilation gives.
The 3 jobs made 274,518 pair decisions, 45,753 a route a job, in 33.54 route CPU seconds
and 69.15 job wall seconds, summed; the longest job took 29.02 seconds.
`certify --workers 2` took 44 seconds of wall time on 22 October 2026, under `nice` on a
four-core host shared with other lanes at a load average of about 8, and `check --replay`
decided the receipt again in 61 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code. No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record at `main` `cacdafc1f` (22 October 2026), and `check-claims` rebuilds it, each
side from its own retained packet:

| Report at 303 | Holder | This certificate is below it by |
| --- | --- | --- |
| `T-186`, the case ceiling and house best packing | Mykhailo Polkovskyi, after PingYou Ltd, of Daniil Ostashev’s packing | $1.8607 \times 10^{-4}$ |
| `T-174` (PR #574) | PingYou Ltd, of Daniil Ostashev’s packing | $1.8607 \times 10^{-4}$ |
| `T-162` (#562) | Daniil Ostashev | $1.8607 \times 10^{-4}$ |
| #593 | Mykhailo Polkovskyi (Mishapolk) | $1.8607 \times 10^{-4}$ |
| `T-146`, `T-136` (#481) | Evan Daniel’s regularization of Nate Chaoweeraprasit’s packing; Chaoweeraprasit | $3.29 \times 10^{-3}$ |
| #573 | Mykhailo Polkovskyi (Mishapolk) | $3.29 \times 10^{-3}$ |
| `T-134` (#476), #488 | Francisco Couzo | $7.67 \times 10^{-3}$, $7.59 \times 10^{-3}$ |
| `T-138` (#470), `T-113` (#401) | Mishapolk; Nate Chaoweeraprasit | $1.05 \times 10^{-2}$ |
| `T-098` (#375), `T-092`, `T-056` | Evan Daniel; Francisco Couzo | $1.46 \times 10^{-2}$ |

The margin below the case ceiling is exactly the difference `claims.json` records,
$0.00018607379558020919938508084803700\ldots$.
The certificate is below every report the record holds or has pending at 303, and no
other open report through #727 states a bound at 303.

## Pose by Pose

[measure/identity.py](measure/identity.py) measures the packing against the three
certificates of Ostashev’s packing the record holds, with the measures of the
[evand-regularized-2026-10-20](../evand-regularized-2026-10-20/README.md) packet’s
identity program, and writes [measure/identity.json](measure/identity.json). It repeats
the stage 1 triage’s measurement from the retained files; the stage 4 review’s own
measurement, below, agrees. A measurement, which decides nothing:

- **No symmetry pairs it one to one** by nearest centres with T-186’s packing, T-174’s or
  T-162’s.
- **The best assignment**, under the identity, moves 64 squares by more than a tenth
  against T-186 (at most 0.910), 100 beyond $10^{-2}$ and 123 beyond $10^{-3}$, and turns
  one by up to 44.39 degrees. Against T-162 the counts are 62, 99 and 122.
- **The tilts.** This packing has 91 squares tilted by 22.83 to 26.12 degrees, all one way,
  and two near upright, at $-0.062$ and $-0.080$ degrees. Thirteen more are turned by
  less than $2 \times 10^{-11}$ degrees, which the rounding of their half-angle tangents
  leaves, so 106 have $c \cdot s \ne 0$. T-186’s packing has 92 tilted squares, 46 each
  way.
- **The band flip.** Under the assignment, 45 of the 91 tilted squares stay within a tenth
  of a square tilted the same way, and 44 pair, beyond a tenth, with squares tilted the
  other way. No tilt angle is shared within $10^{-4}$ degrees.

The record keeps the word refinement for a pairing in which no square moves beyond a
tenth, so this is not a refinement of Ostashev’s packing, as the issue says. It is
another arrangement of his two-band design with one tilted band reflected; that it was
found from his packing is the source’s account, which the measurement does not
contradict.
The issue’s matching distance of 0.266, the root-mean-square corner displacement that
`pk/crossing.py` defines, was not recomputed here; the triage measured 0.273 against
T-186 and 0.263 against T-162 with its own program, which is not retained.

## Lineage

The issue says the packing was found from Daniil Ostashev’s packing, by a hunt through
non-record packings:

1. On 17 October the author’s basin explorer started from Ostashev’s packing and stored
   14 generations of non-record descendants, the last at 17.917896.
2. On 20 October a near-record sweep (`dgen.py sweep`) started from it, among others, and
   a crossover gave 17.913464.
3. On 21 and 22 October a second sweep, with a graded reward and junction and band moves,
   gave 17.910030 by a crossover.
4. On 22 October a focused run made seven moves from 17.910030. The last was a band flip,
   which reflects one of the two tilted bands along its wall, so that its tilt sign flips
   and its ends swap; re-polished, it reached 17.909772.
5. `exactsolve.py` found the packing not first-order jammed, and the binary64 packing was
   dilated into this certificate.

The report’s `prior` block names the start as the author’s store’s copy of Ostashev’s
packing, citing #501, #575 and `dostashev/square-packing@b909e1b`. Its exact side is
T-186’s and its certificate side T-162’s.

## What Is Not Established

The certificate establishes a finite upper bound at its exact side, nothing more.
The source leaves local optimality unresolved: its exact solver finds no equilibrium with
smooth contacts, and its corner-to-corner MILP predicts a further first-order descent of
about $4.75 \times 10^{-7}$ (`vv_milp_dS` in the report) that its descent step did not
realise. Those are the source’s numerical statements and were not replayed here.
Novelty, local or global optimality and rigidity are not established.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`, which states that the work was done with Claude (Anthropic) under human
direction and without peer review. The pinned commit names Claude Opus 5.5 as co-author
and says the record claim was approved by Evan Daniel in chat on 22 October 2026.
The issue asks for the credit name “Evan Daniel (GitHub @evand)” and names Daniil
Ostashev’s packing (#562) as the search’s start.
The source’s root README lists the Squares Project among the 2026 work it builds on or
runs beside, so the bibliography credit reads `Daniel after Ostashev, Levy`, as for the
n155 packing of #669, which was also found from Ostashev’s packing.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-n303-2026-10-22 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n303-2026-10-22 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n303-2026-10-22 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n303-2026-10-22 check --replay
uv run --frozen --all-extras --group dev python resources/web/evand-n303-2026-10-22/measure/identity.py --out resources/web/evand-n303-2026-10-22/measure/identity.json
```

`check` admits the receipt structurally against the retained certificate; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs. The records
pull request of 22 October registers it as `T-230`, and the stage 4 review below raises
it to V3/C3.

## Stage 4 Review

The [review of 22 October 2026](../../../../docs/project/reviews/review-2026-10-22-daniel-728.md)
accepted the certificate for finite feasibility, with seven findings, none blocking.
Its programs and outputs are kept in
[review/review-2026-10-22/](review/review-2026-10-22/README.md); the fetched copies of
the source’s files it read are not, since this packet keeps them.

- **Its own checker.** `review_728_check.py` decides the certificate on two exact routes
  that share only a reader of its own: integers alone (route Z) and `Fraction` with the
  exact clipped area of every pair (route C). Both accept it, with the least wall
  clearance and the least pair gap above, and agree with both maintained routes at every
  number they share. Its author read neither maintained route nor the source’s checkers
  before it decided, so it is a clean-room re-implementation
  (`E-evand-728-n303-review-exact-feasibility`).
- **Sharp controls.** Eight mutants, at exact contact and $10^{-30}$ past it at a wall
  and at the least-gap pair, are accepted and refused as expected by all four deciders,
  and so is the kernel’s `run_sharp`. The receipt’s own two controls are gross (RF-2).
- **The adapter** (RF-1). The maintained routes read the certificate through
  `devtools.evand_exact_certificates`, whose line filter and corner construction are the
  source’s checkers’ expressions transcribed; its module statement and registry note now
  say so, and the replay entry records `producer-code` among what its authors read.
- **Identity** (RF-3). The review measured the packing against the house’s and T-146’s:
  64 squares beyond a tenth of the house’s, 8 beyond half a unit, 180 within $10^{-3}$
  and 24 tilts reversed. It is another arrangement, and the closest to Ostashev’s of
  those compared. The issue’s matching distance of 0.266 is not defined there, and no
  definition the review tried reproduced it.
- **The issue’s citation** (RF-4). The issue cites #501 beside #562 for the earlier
  bound; #501 makes no claim at 303.
- **The exact side** (RF-5). `verify_cert2.py`’s VALID line prints the side as a
  binary64, $9.95 \times 10^{-16}$ below it; the record quotes the exact side or its
  12-place ceiling, never that print.
- **Local optimality** (RF-7) is unresolved by the source’s own account, and the record
  states no local-minimum, KKT or rigidity claim.
- **Significance** S3, as T-197 at 155 is.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
