# Evan Daniel’s s(182) Certificate at d99925d

This packet retains the certificate Evan Daniel’s
[evand/square-packing](https://github.com/evand/square-packing/tree/d99925d1298262c4ddb81c95abbb6f45adca8d3d/search/packer/candidates)
adds at `d99925d1298262c4ddb81c95abbb6f45adca8d3d` (authored and committed
2026-10-25T04:11:15Z), which GitHub’s activity log records pushed at 04:16:05Z in the
push `3c335fe..d99925d`. Issue [#806](https://github.com/jlevy/squares/issues/806),
opened 19 seconds later at 04:16:24Z, reports it:

- **182, recorded as T-243:** `s182-1024.cert`,
  $s(182) \le 13970916436214678735385725854133/10^{30} =
  13.970916436214678735385725854133$, which the issue prints rounded up at 12 places as
  13.970916436215: 3.17e-3 below T-174, the case’s house, and below every report at 182.

T-243 registers it at `V3`/`C3` since the
[stage 4 review of 25 October](#stage-4-review), which accepted it with no blocking or
major finding. It is the smallest validated side at 182, so the case adopts it under the
house rule, with the regularization of the new house by both strong generators in the
same pull request.

The source was read on 25 October 2026 from a blobless clone fetched at 05:22Z, whose head
was `d99925d`, as it still was when this packet was written.

## What the Author Claims

The commit’s title gives the certificate’s side rounded up at 14 places, 13.97091643621468,
as an equality, and calls the packing “polished and certified” and a “distinct minimum
from the register’s 13.974090713”. The result is an upper bound, as the issue’s title and
table state it, and the record states it so (M-2 of the review).

Issue #806 claims one new upper bound, the certificate’s exact rational side rounded up at
12 places, and prints the SHA-256 of `s182-1024.cert` and of
`s182-1024_regularized.cert`, “the same packing at the same side, regularized for
display”. It says:

- **Checking.** The source’s `search/exact/verify_cert.py` (separating axes) and
  `verify_cert2.py` (polygon intersection) both print VALID; they share an author and
  the certificate format.
- **Local optimality**, as numerical evidence at 80 digits and not interval proofs: the
  exact side $S^* = 13.970916436214678735246\ldots$ is a KKT point and a local minimum of
  the side, strict modulo 43 exact flat motions, with no corner–corner MILP descent, 68
  corner–corner contacts and 6 rattlers. Three later jobs at 182 in the same run found
  nothing lower.
- **Relationship.** “A new packing (a different local minimum from the register’s
  13.974090713)”: matched against the previous record’s regularized view, its largest
  move is 0.814, 38 squares move beyond 0.1 and 69 beyond 0.01, and no tilt angle is
  shared.
- **How it was found.** One L-cut job of a targeted search: “remove an L-shaped strip of
  29 squares (a row and a column along two walls) from the s(211) packing, then relax”,
  giving 182 squares at 13.971254466, then a local search to 13.970916436. “Please
  credit the register’s s(211) packing (Daniil Ostashev) as the start.” Its table names
  that start as “Daniil Ostashev (register); Francisco Couzo (43ac7d2); Francisco Couzo
  (487b058)”, side 14.993549626299.
- **Side-only claims.** Two Kaggle per-puzzle leaderboard entries list a side with no
  packing: 13.9727613470647 for Prathamesh Chavan (23 October, 08:32 UTC) and
  13.9709164362306 for Subramanya N (24 October, 18:41 UTC), “the same local minimum,
  very likely”, listed about four hours before the source’s search found it.

The certificate’s JSON report (`s182-1024.json`) states `S_input` 13.970916436217552,
the side of the binary64 packing it was solved from, and `S_exact`, the side of a
Newton-converged KKT point at 80 digits, with 885 active contacts, 176 load-bearing
squares, 6 free squares and 43 frozen variables. The certificate’s side exceeds `S_exact`
by about 1.40e-19, a relative padding of 1e-20 (computed here; the JSON states the sides,
not the gap).

These statements are the author’s. No source program ran here.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is 12 files of 182,986 bytes: 10 retained under
[source/](source/) (176,484 bytes) and 2 pinned by digest.

| Retained under `source/search/packer/candidates/` | What it is |
| --- | --- |
| `s182-1024.cert` | the certificate, SHA-256 `9e12e0a42b05c4fc…`, as the issue prints |
| `s182-1024.exact.txt` | the 80-digit KKT point |
| `s182-1024.input.txt` | the binary64 packing it was solved from |
| `s182-1024.json` | the solver’s report |
| `s182-1024_prior.json`, `s182-1024_vs_prior.json` | the comparison with the source store’s prior best at 182 |
| `s182-1024_regularized.cert`, `s182-1024_regularized.json` | the display view at the same side, SHA-256 `f1ec415a194b9c0d…`, as the issue prints |

The eight files are the whole `s182-1024` set the commit adds, 167,915 bytes upstream.
The licence and `CREDITS.md` are retained beside them. Pinned by digest: the two exact
checkers the certificate’s header names, `search/exact/verify_cert.py` and
`verify_cert2.py`, against the identical copies the
[n183 packet](../evand-n183-subgrid-2026-10-19/README.md) retains.
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) is the full
manifest, and [acquisition/sources.json](acquisition/sources.json) the record.
The packet is about 0.2 MB, so it is kept in Git.

## Report Order

The [ledger of 25 October for this import](../../../campaign/issue-intake/upper-bounds-issue806-20261025/README.md)
walks #806 from the starts frozen at `main` `bb756e19`, where T-174 holds 182 in both
lanes and no register bound is pending adoption: recorded, 3.17e-3 below, a new packing.
The push of `d99925d` 19 seconds before the issue is the same author’s publication of the
same file, and nothing reached 182 between them, so no verdict depends on which dates it.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `bb756e19` on 25 October
2026). The certificate is below the case’s house, T-174 (PingYou Ltd’s certificate of
Francisco Couzo’s packing as Evan Daniel improved it), and below T-098 (#375), Couzo’s
certificate of #476 and #593’s, all by 3.17e-03, and below T-056’s print by 3.17e-03. It
is the smallest report at 182.

Neither Kaggle entry the issue quotes is a report, since neither states a packing.
Subramanya N’s side is 1.59e-11 above this certificate’s, and Prathamesh Chavan’s 1.84e-3
above.

## Pose by Pose

`devtools.measure_identity` measured the certificate against each packing the record holds
at 182 and against the source’s own files, and wrote
[measure/identity.json](measure/identity.json). A measurement for credit; it decides
nothing.

- **Against T-174**, the house: no symmetry of the box pairs the two one to one by nearest
  centres. The optimal assignment, best under the identity, moves 44 of 182 squares beyond
  0.1 and 79 beyond 0.01 (largest 0.813) and turns 74. It pairs 16 tilted squares with
  squares tilted the other way and shares no tilt angle within 1e-4 degrees. The
  certificate has 68 tilted squares, all turned one way; T-174 has 59. The house witness
  and T-098’s packing, the same packing at 182, measure the same. So it is another
  arrangement, as the issue says.
- **Against the source’s binary64 input:** one to one under the identity, none beyond
  1e-6 (largest 2.55e-7).
- **Against the regularized view:** one to one under the identity at the same side. It
  moves 49 squares, 5 beyond 0.1 (largest 0.381). The view proves no other bound and is
  not registered. The adoption’s regularization may offer it to the selection as a
  candidate drawing.

## Exact Replay

`devtools.upper_bound_reports certify` decided the certificate and its duplicate-square
and outside-container controls on both maintained routes, each job in its own child
process: 3 jobs, 98,826 pair decisions, 11.53 route CPU seconds, the longest job 4.15
seconds ([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)).
The certificate clears every wall by exactly 5e-21 and every pair by at least 9.99e-21.

Those margins are below the binary64 spacing of the coordinates, so the gross controls
cannot tell an exact route from one that rounds.
`devtools.upper_bound_reports sharp-controls` took the certificate to exact contact and
1e-30 past it ([receipts/sharp-controls.json](receipts/sharp-controls.json)). It lowered
the side by the least far-wall clearance, closed the least-gap pair by its gap, and moved
every square toward the nearer near wall by its least clearance. Both routes accepted all
three at contact with margin 0 and refused all three past it with margin −1e-30. It also
enlarged one square to its pair and one to its wall: both routes refused each at contact
for its shape alone, and 1e-30 past it for the overlap or the wall as well. Both refused a
duplicated square. The run took about 45 CPU seconds.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read the certificate through the `evand-cert` reader,
whose line filter and corner construction are transcribed from Daniel’s checkers. The
source’s checkers were not run.

## What Is Not Established

A finite packing certifies an upper bound and nothing more.
No KKT, local-minimum, rigidity or optimality statement is replayed: the source’s
`S_exact`, free squares, flat motions and second-order report are its own numerical
report at 80 digits, with no interval enclosure (N-2 and N-3 of the review). The search
history, the relaxation’s side 13.971254466 and the explorer’s moves, is the source’s
account; the lineage rests on the review’s geometry alone. Whether Subramanya N
published a packing at the Kaggle side is for the author or Subramanya N to say, and the
record does not call this side the first known at its value (N-7).

## Credit and Licence

- **The packing:** Evan Daniel’s, a new arrangement found by his explore loop.
- **The start:** the register’s s(211) packing, as the issue asks, which is T-188’s:
  Francisco Couzo’s 211 packing, an arrangement of Daniil Ostashev’s design (T-175). The
  issue’s own account gives the start T-188’s side, 14.993549626299, and where T-188
  differs from Ostashev’s own 211 packing the certificate follows T-188 (M-1 of the
  review). So the credit is *Evan Daniel, from an L-cut of Francisco Couzo’s 211 packing
  (T-188), an arrangement of Daniil Ostashev’s design (T-175)*.
- **Licence and assistance:** MIT, copyright (c) 2026 Evan Daniel ([LICENSE](source/LICENSE)).
  [CREDITS.md](source/CREDITS.md) says the repository’s work was “Produced by Claude
  (Anthropic) in a single session under human direction”, the commit carries a
  Co-Authored-By trailer naming Claude, and the issue discloses Claude assistance.

The bibliography key is **[Daniel n182 2026-10-25]**, credited *Daniel after Couzo,
Ostashev, Levy*. Its lineage is `builds-on-project`: the issue names this project’s
register as where its start came from, as Daniel’s issue-728 key does for his 303.

## Stage 4 Review

The [review of 25 October 2026](../../../../docs/project/reviews/review-2026-10-25-evand-n182.md)
accepted the certificate for finite feasibility, with no blocking or major finding, two
minor findings and eight notes. Its programs and outputs are kept here in
[review/review-2026-10-25/](review/review-2026-10-25/README.md).

- **Its own checker.** `exact_check.py` decides the certificate in `Fraction` over all 182
  walls and 16,471 pairs, by separating axes and again by exact clipped areas, with
  fourteen controls sharp at $10^{-30}$, all as expected under both methods. Its least
  wall clearance, exactly 5e-21, and least pair gap, about 9.999999999999992e-21 (squares
  99 and 100), are the replay’s. Its author read neither maintained route nor any checker
  of Daniel’s, so it is a clean-room re-implementation
  (`E-evand-n182-review-exact-feasibility`, `V-evand-n182-review-check`).
- **The maintained replay** reads the certificate through the `evand-cert` reader, whose
  line filter and corner construction are transcribed from Daniel’s `verify_cert.py` and
  `verify_cert2.py`, so it is `shared-components` (`E-evand-n182-exact-feasibility`), and
  T-243’s independent re-implementation rests on the review’s checker.
- **The lineage.** Measured square for square, T-188’s 211 packing fits in its own frame,
  and the 29 squares the 182 do not use are exactly its right column and top row of 15,
  sharing the corner square. Of the other 182, 17 move beyond 0.1 (largest 0.464), 156
  beyond 1e-2 and 173 beyond 1e-3 (N-4). At T-188’s tilted square 141 the certificate lies
  0.015 from T-188’s pose and 0.442 from T-175’s, which places the start at T-188 (M-1).
- **The KKT point.** The certificate is the source’s 80-digit point dilated about the
  corner by $1 + 10^{-20}$, its centres within $4.97 \times 10^{-36}$; the point is a
  packing at $S^*$ only to its precision (N-2). The local-minimality statement is the
  source’s numerical report (N-3).
- **The rest.** M-1, M-2, N-2, N-3, N-4 and N-7 are applied above and in the register;
  S3 is confirmed. N-8, the case record’s rigidity statement, is derived again on the new
  witness at the adoption. The author’s four questions (the start’s credit, the cut, an
  enclosure of the KKT point, the format line’s corner formula) are drafted for the
  acknowledgement in think-2lzo and hold nothing open: the issue’s own start side and the
  review’s measurement settle the start, and the others change nothing the record asserts.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source evand-n182-2026-10-25 --checkout CHECKOUT
python -m devtools.acquire_source evand-n182-2026-10-25 --check
python -m devtools.upper_bound_reports evand-n182-2026-10-25 check-claims --write
python -m devtools.upper_bound_reports evand-n182-2026-10-25 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports evand-n182-2026-10-25 check --replay
python -m devtools.upper_bound_reports evand-n182-2026-10-25 sharp-controls
python -m devtools.measure_identity --n 182 '#806=packet:evand-n182-2026-10-25' \
  'T-174=packet:pingyou-pr574-certificates-2026-10-13' \
  'house-witness=witness-center-basis:witnesses/known-best/n-182.yaml' \
  'T-098=evand-cert:resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-182.cert' \
  'input=binary64-xyd:resources/web/evand-n182-2026-10-25/source/search/packer/candidates/s182-1024.input.txt' \
  'regularized=evand-cert:resources/web/evand-n182-2026-10-25/source/search/packer/candidates/s182-1024_regularized.cert' \
  --out resources/web/evand-n182-2026-10-25/measure/identity.json
```

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/search/packer/candidates/s182-1024_vs_prior.json.gz` | upstream | `54f6986306daef6ade15e9c0ef83f1f40535456e` | `37b0b50b4a9e3112e68f3be00a43ed8c9ff201d0894687876f0fdff7dcf4f44e` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
