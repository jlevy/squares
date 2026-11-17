# Evan Daniel’s Certificates at 175, 204, 260, 268, 293, 303 and 304 at bb4cc78

This packet retains the seven certificate sets Evan Daniel’s
[evand/square-packing](https://github.com/evand/square-packing/tree/bb4cc78e5b35103c1f177db55e9cf08974e66563/search/packer/candidates)
adds at `bb4cc78e5b35103c1f177db55e9cf08974e66563` (committed 2026-11-05T18:29:13Z, tree
`341f5ffb`), the repository’s head when it was read on 5 November 2026 and the first
commit to hold any of the seven. Issue [#914](https://github.com/jlevy/squares/issues/914),
opened 38 minutes 37 seconds after the commit, reports them.
The six regularized views the commit also adds are decided on both routes through the
[views packet](../evand-issue914-views-2026-11-05/README.md), which pins them against the
copies retained here.

## What the Source Claims

Each certificate gives `n` unit squares, each a rational centre and a rational
$t = \tan(\theta/2)$, in an open square of the stated side, in the source’s certificate
format. #914 claims each side rounded up at 12 places, and global optimality at none.

| n | Certificate | Exact side (header) | #914 prints | The issue says |
| ---: | --- | --- | --- | --- |
| 175 | `s175_1105.cert` | `13764050051543175143919941166751/10^30` | 13.764050051544 | exact KKT point; positive semidefinite with 83 zero modes; regularized view at the same side |
| 204 | `s204_trig1.cert` | `7402180691825929362760144937013/(5*10^29)` | 14.804361383652 | exact KKT point; a local minimum strict modulo 57 flat motions; regularized view |
| 260 | `s260_ks_1105.cert` | `8316760475444266760475435949833/(5*10^29)` | 16.633520950889 | dilation of its binary64 input by the factor 1 + 1e-12, side 1.66e-11 above the input's (the issue's 8.8e-12 is the excess over the pre-descent input's, F3 of the review); the exact solver did not converge |
| 268 | `s268_1105.cert` | `2109062439766878830759866953431/(1.25*10^29)` | 16.872499518136 | exact KKT point; local minimality inconclusive; regularized view |
| 293 | `s293_1105.cert` | `17623065212060701770633564247069/10^30` | 17.623065212061 | exact KKT point; a local minimum strict modulo 17 flat motions; regularized view |
| 303 | `s303_1105.cert` | `17901832750854048761575294038467/10^30` | 17.901832750855 | exact KKT point, not shown to be a local minimum (a first-order MILP descent, dS −2.2e-4, not realised); regularized view after the regularizer fix of `39fb4f0` |
| 304 | `s304_1105.cert` | `17920944093340242061198022152503/10^30` | 17.920944093341 | exact KKT point; a local minimum strict modulo 103 flat motions; regularized view |

The local-optimality statements are numerical evidence at 80 digits, not interval proofs,
and the issue says so. It calls all seven new packings, not refinements, and gives matched
moves and contact-pair counts against the register’s packings at 175, 204, 268 and 303.
It says all seven were built by the author’s fault-line composer, his independent
implementation of Chris Deotte’s multi-gadget fault DP from Deotte’s Kaggle notebooks, and
asks that Deotte be credited for the method. It credits the register’s s(175) packing
(Mishapolk’s, after Daniil Ostashev et al.) as the start at 175; the author’s own s(233)
and s(370) as the gadgets at 204; the tilted island of his #845 260, from Kirill
Tymchishin’s Kaggle s(260), at 260; and says the gadget donors at 268, 293, 303 and 304
were not recorded. It says the source’s two exact checkers, `search/exact/verify_cert.py`
(separating axes) and `verify_cert2.py` (polygon intersection), report VALID on all
thirteen files, and that they share an author and the format. It quotes Kaggle
per-puzzle leaderboard sides at all seven counts, below these at five, with no
coordinates. Those statements are the author’s; no source program ran here.

The thirteen SHA-256 digests the issue prints are the retained files’
([acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256)).

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin. The scope is 60 files of 1,364,428 bytes: 58 retained under
[source/](source/) (1,357,926 bytes) and 2 pinned by digest.

| Retained under `source/search/packer/candidates/` | What it is | Counts |
| --- | --- | --- |
| `<set>.cert` | the certificate | all seven |
| `<set>.input.txt` | the binary64 packing it was solved or dilated from | all seven |
| `<set>.json` | the run summary | all seven |
| `<set>_prior.json` | the source store’s prior facts at the count | all seven |
| `<set>.predescent.txt` | the binary64 packing before the exact descent | all but 268 |
| `<set>.exact.txt` | the 80-digit KKT point | all but 260 |
| `<set>_regularized.cert`, `<set>_regularized.json` | the regularized display view at the same side, and its report | all but 260 |
| `<set>_vs_prior.json` | the comparison with the store’s prior packing | 175, 204, 268, 303 |

The sets are `s175_1105`, `s204_trig1`, `s260_ks_1105`, `s268_1105`, `s293_1105`,
`s303_1105` and `s304_1105`: the 56 files the commit adds, retained as #845’s packet
retained its companions. The licence and `CREDITS.md` are retained beside them. Pinned by
digest: the two exact checkers the certificates name, against the identical copies the
[n183 packet](../evand-n183-subgrid-2026-10-19/README.md) retains.
[acquisition/sources.json](acquisition/sources.json) is the record. The packet is about
1.6 MB with its receipts, so it is kept in Git.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) is the frozen comparison
(`devtools.upper_bound_reports check-claims`, read from `main` `249bb82e7` on 5 November
2026). Each certificate is admitted at the side #914 prints, its exact side rounding up to
it at 12 places, and each is the smallest report at its count:

| n | The house it is below | By |
| ---: | --- | --- |
| 175 | T-186, Daniil Ostashev’s packing as PingYou Ltd and Mykhailo Polkovskyi refined it | 1.24e-4 |
| 204 | T-264, Evan Daniel’s #845 packing as Doğa Özden improved it | 3.26e-3 |
| 260 | T-265, Evan Daniel’s #845 packing as Kaelan Yim improved it | 4.62e-4 |
| 268 | T-242, Vladislav Lavrentev’s packing as Evan Daniel improved it | 1.86e-3 |
| 293 | T-257, Evan Daniel’s #845 packing | 1.09e-2 |
| 303 | T-240, Vladislav Lavrentev’s packing as Francisco Couzo improved it | 5.15e-3 |
| 304 | T-242, Kirill Tymchishin’s packing as Evan Daniel improved it | 5.95e-3 |

No register bound is pending adoption below these houses, and no other report reached
these counts before the issue. None of the Kaggle sides the issue quotes is a report,
since none states a packing.

## Report Order

The [ledger of 5 November for this import](../../../campaign/issue-intake/upper-bounds-914-20261105/README.md)
walks #914 from the starts frozen at `main` `249bb82e7` and records all seven, each a new
packing by the source’s word.

## Pose by Pose

`devtools.measure_identity` measured each certificate against the packing the house holds,
the house witness, the certificate’s binary64 input and, at six counts, its regularized
view, and wrote the receipts under [measure/](measure/). A measurement for credit; it
decides nothing.

| n | Against the house | Optimal assignment against it | Tilted beyond 1° (this, house) |
| ---: | --- | --- | --- |
| 175 | T-186: no symmetry one to one | symmetry 2: 60 beyond 0.1, 83 beyond 0.01, largest 0.774 | 48, 50 |
| 204 | T-264: no symmetry one to one | symmetry 5: 66 beyond 0.1, 126 beyond 0.01, largest 1.032 | 63, 76 |
| 260 | T-265: no symmetry one to one | identity: 42 beyond 0.1, 165 beyond 0.01, largest 0.602 | 103, 105 |
| 268 | T-242: no symmetry one to one | symmetry 2: 80 beyond 0.1, 139 beyond 0.01, largest 1.072 | 98, 81 |
| 293 | T-257: no symmetry one to one | symmetry 5: 193 beyond 0.1, 249 beyond 0.01, largest 0.995 | 54, 104 |
| 303 | T-240: no symmetry one to one | symmetry 5: 124 beyond 0.1, 144 beyond 0.01, largest 1.104 | 112, 102 |
| 304 | T-242: no symmetry one to one | identity: 66 beyond 0.1, 157 beyond 0.01, largest 0.867 | 110, 99 |

Each house witness measures as its house’s packet does. At 260 the certificate is also
one to one with T-257’s packing, whose tilted island the issue says it recomposes, under no
symmetry: the optimal assignment, under the identity, moves 33 squares beyond 0.1 and 160
beyond 0.01 (largest 0.633). So each is another arrangement than the house’s, as the
issue says. Each certificate pairs one to one under the identity with its binary64 input,
largest move 2.28e-11 at 260 (the dilation) and at most 1.42e-4 elsewhere. Each regularized view pairs with its certificate by the optimal assignment with
3 to 8 squares beyond 0.1 (largest 0.332 to 0.623), one to one by nearest centres at five
counts and not at 293.

## Exact Replay

`devtools.upper_bound_reports certify` decided every certificate of the packet and its
duplicate-square and outside-container controls on both maintained routes, each job in
its own child process: 21 jobs, 1,439,796 pair decisions, 200.09 route CPU seconds, the
longest job 13.97 seconds ([receipts/exact-certification.json.xz](receipts/exact-certification.json.xz)).
Every positive passed and every control was refused on both routes, and `check --replay`
decided all 21 again. The KKT certificates clear every wall by exactly 5e-21 and every
pair by at least 9.99e-21, the source’s dilation by $1 + 10^{-20}$ about the corner; the
260 certificate clears every wall by at least 4.98e-13 and every pair by at least
9.98e-13.

`devtools.upper_bound_reports sharp-controls` took each certificate to exact contact and
1e-30 past it (`receipts/sharp-controls-nNNN.json`, one per count). It lowered the side by
the least far-wall clearance, closed the least-gap pair by its gap, and moved every square
toward the nearer near wall by its least clearance: both routes accepted each at contact
with margin 0 and refused each past it. It enlarged one square to its pair and one to its
wall: both routes refused each at contact for its shape alone and 1e-30 past it for the
overlap or the wall as well. Both refused a duplicated square.

The [views packet](../evand-issue914-views-2026-11-05/README.md) decided the six
regularized views the same way, with their own gross and sharp controls.

The two routes, the `sqpack` rational witness verifier and the independent rational
corner checker, share certificate parsing, half-angle conversion, `Fraction` arithmetic
and the separating-axis method, and read each certificate through the `evand-cert`
reader. The source’s checkers were not run.

## Stage 4 Review

The [review of 5 November 2026](../../../../docs/project/reviews/review-2026-11-05-evand-914-seven.md),
by a strong-tier lane prompted separately from this one, accepted all seven certificates,
at 260 with findings, none blocking or major, and confirmed the significance S3 at each.
Its programs, receipts and frozen findings are in
[review/review-2026-11-05/](review/review-2026-11-05/README.md); `out/program-digests.txt`
lists each program’s digest, and `frozen-findings.sha256` the digest its findings were
frozen under before it read the earlier reviews.

- **Its own checker.** `decide_feasibility.py` decides all thirteen files, every wall and
  every pair with no distance filter, by two methods that share only its reader:
  separating axes in `Fraction` and exact clipped areas in GMP rationals. They agree pair
  by pair, 239,966 certificate pairs and 206,296 view pairs, every pair strictly apart and
  every square strictly inside. Its 182 sharp and gross controls, fourteen a file, are
  decided as stated beforehand, and under the reversed rotation sense every file overlaps
  (`E-evand-914-review-exact-feasibility`, `V-evand-1105-review-check`). It shares no
  code with either maintained route or the source, so each bound is confirmed,
  independently re-implemented, clean room; the replay above shares the `evand-cert`
  reader with the producer (`E-evand-914-exact-feasibility`, shared components).
- **The gains.** Each is at least $6.2 \times 10^{8}$ times all of its house’s side
  slack (F9), so no rescaling of a house reaches the new side.
- **New arrangements.** No symmetry pairs any certificate one to one with its house’s
  packing (F7). At 260 the 97 squares tilted beyond 10 degrees are T-257’s island within
  0.042 only after a half turn about the box centre and a shift of one unit upward, and
  the frame around it is rebuilt: a new arrangement built on that island, not a further
  arrangement (F8).
- **The record’s findings.** F3 corrected the 260 dilation above: $1 + 10^{-12}$, the
  side $1.66 \times 10^{-11}$ above the binary64 input’s. F13 gave each lineage its own
  key (below), and F14 names Mykhailo Polkovskyi by his surname. F15 records the replay
  as shared components and the review as an independent re-implementation. F11 finds that
  the 175 start needs no regularization or improvement credit.
- **For the author.** F4 (the 260 $S'$ print is the side’s binary64 value, and the input
  read exactly overlaps by up to $3.9 \times 10^{-16}$), F10 (custody holds; the issue
  was edited after it was opened) and five questions, none holding a rung.

## Adoption

The cases adopted the seven certificates as their house best packings under the house
rule: 175, 204, 268, 293, 303 and 304 in the pass of 5 November 2026, and 260 in the pass
of 6 November 2026, since the pass of 5 November had already moved 260 to T-265 and a
day’s prior-state archive holds one record a count. Each replaced house keeps its
certificate as history: T-186 at 175, T-264 at 204, T-265 at 260, T-242 at 268 and 304,
T-257 at 293 and T-240 at 303. Evan Daniel is each packing’s finder, and no improver is
credited ([n-175.md](../../../frontier/n-175.md) to
[n-304.md](../../../frontier/n-304.md)).

Both strong generators ran on the seven new witnesses
([think-lrj4-2026-11-05](../../../cases/regularized_drawings/think-lrj4-2026-11-05/README.md)).
Evan Daniel’s regularizer’s views are drawn at 175, 204 and 268, and grid-slack’s at 260
(0.5 degrees) and 303 (5 degrees). At 293 and 304 no view improves on the axis tool’s, so
the counts are decided no better. At 175 the drawn view is this release’s own
`s175_1105_regularized.cert`, every square within $10^{-9}$, and at 268 it is the same but
for one square moved $7.3 \times 10^{-4}$; at 204 it is the release’s view after a half
turn, with 33 squares moved beyond a hundredth. The rigidity blocks were derived again on
the new witnesses, and each stays not rigid. The posters’ print-credit hold no longer holds
Doğa Özden’s name at 204 or Kaelan Yim’s at 260, whom the case records there no longer
credit; it holds Özden’s at 299 (think-tj4o, think-hgpg).

## What Is Not Established

- **A second review.** One AI review is retained; V4 and C4 would need a second accepted
  adversarial review by a distinct reviewer.
- **Human oversight.** No human oversight record is retained.
- **Optimality** of any kind: a finite certificate proves an upper bound and nothing more.
  The KKT and local-minimum statements are the author’s numerical evidence.
- **The lineage** the source states, beyond what the measurements above show; at 268,
  293, 303 and 304 the source did not record it.

## Credit and Licence

MIT, copyright (c) 2026 Evan Daniel. `CREDITS.md` says the repository’s work was
“Produced by Claude (Anthropic) in a single session under human direction”, and the
commit carries a Co-Authored-By trailer naming Claude. The packings are Daniel’s, built by
his composer after Chris Deotte’s method, with the starts the issue credits: the register’s
s(175) packing (Ostashev’s, as PingYou Ltd and Mykhailo Polkovskyi refined it) at 175, and Kirill
Tymchishin’s Kaggle s(260), through Daniel’s #845 island, at 260. Each lineage has its
own bibliography key (the review’s F13): **[Daniel issue 914 2026-11-05]**, “Daniel after
Deotte”, at 204, 268, 293, 303 and 304; **[Daniel issue 914 n175 2026-11-05]**, “Daniel
after Deotte, Ostashev, PingYou Ltd, Polkovskyi”, at 175; and **[Daniel issue 914 n260
2026-11-05]**, “Daniel after Deotte, Tymchishin”, at 260. The views packet has its own,
**[Daniel issue 914 views 2026-11-05]**. The register records one entry per count, T-267
to T-273.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source evand-issue914-2026-11-05 --checkout CHECKOUT
python -m devtools.acquire_source evand-issue914-2026-11-05 --check
python -m devtools.upper_bound_reports evand-issue914-2026-11-05 check-claims --write
python -m devtools.upper_bound_reports evand-issue914-2026-11-05 certify --jobs-dir "$TMPDIR/jobs" --workers 2
python -m devtools.upper_bound_reports evand-issue914-2026-11-05 check --replay
python -m devtools.upper_bound_reports evand-issue914-2026-11-05 sharp-controls
python -m devtools.measure_identity --n 175 '#914=packet:evand-issue914-2026-11-05' \
  'T-186=packet:mishapolk-kkt-refinements-2026-10-14' \
  'regularized=packet:evand-issue914-views-2026-11-05' \
  'house-witness=witness-center-basis:witnesses/known-best/n-175.yaml' \
  'input=binary64-xyd:resources/web/evand-issue914-2026-11-05/source/search/packer/candidates/s175_1105.input.txt' \
  --out resources/web/evand-issue914-2026-11-05/measure/identity-n175.json
```

The other counts’ measurements name their houses’ packets in the same way: T-264
`ozden-s204-upper-bound-2026-11-03`, T-265 `yim-s260-upper-bound-2026-11-05` (with T-257
`evand-issue845-2026-10-29` and no view at 260), T-242
`evand-kaggle-descents-2026-10-24` at 268 and 304, T-257 `evand-issue845-2026-10-29` at
293, and T-240 `couzo-issue763-2026-10-23` at 303.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/search/packer/candidates/s204_trig1_vs_prior.json.gz` | upstream | `21ef14b88ed717d2f584cb0b75a4c0e5d716cf8b` | `145c0ffb8b7dd5052920b687a0d706e26451d4b1de6fb8f04c6bfbbae6a79200` |
| `source/search/packer/candidates/s268_1105_vs_prior.json.gz` | upstream | `c85a9d1a0921bca092b0b330219b4329ea56054e` | `450e6f322debe9b523cc5a861b28aed7ace2c4069145cfbdb9fb06c96c856150` |
| `source/search/packer/candidates/s303_1105_vs_prior.json.gz` | upstream | `c620962695bbae1ddb43d2257c9bcd2ae8d68d70` | `875ed8655f4f50a49912d4efa2725b50f6594eef4d878ec7d417b4e561fb1822` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
