# Evan Daniel’s s(270) Sweep Certificate

[Issue #703](https://github.com/jlevy/squares/issues/703) reports an exact rational
packing of 270 unit squares, in
[evand/square-packing](https://github.com/evand/square-packing/tree/88385abc95ab25d520302282d1946cbb07bc9cf3/search/packer/candidates).
The packet pins the commit the issue names,
`88385abc95ab25d520302282d1946cbb07bc9cf3` (tree
`34fd62e00173b6b9abf84d8368a9edf83e4b6a97`, committed 2026-10-20T21:47:03Z), which adds
the eight n = 270 files, and the eight n = 343 files of
[#702](https://github.com/jlevy/squares/issues/702), which this packet does not retain.
The issue was filed at 2026-10-20T22:09:32Z, 22 minutes later.
The sources were retrieved on 21 October 2026, when the pin was the branch head.

| n | Exact side of the certificate | The issue prints, rounded up | Rounded up at 16 places |
| --- | --- | --- | --- |
| 270 | `16928162252196750114897964982713/1000000000000000000000000000000` | 16.928162252197 | 16.9281622521967502 |

The side is $16.928162252196750114897964982713$ exactly, the decimal the issue prints.
The certificate, `s270_sw.cert`, gives 270 unit squares, each a rational centre and a
rational $t = \tan(\theta/2)$, in an open square of the stated side, in the format of
issues #489, #552, #659, #664, #669, #680, #689 and #694.
The commit also holds the 80-digit KKT point it was certified from
(`s270_sw.exact.txt`), the binary64 packing that point was solved from, the solver’s
report, a summary of the record the author compared against (`s270_sw_prior.json`), a
regularized view of the same packing at the same side (`s270_sw_regularized.cert`, 21
angle groups from 22) with its report, and the source’s comparison with the register’s
packing (`s270_sw_vs_prior.json`). The claim rests on `s270_sw.cert`.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of a blobless clone at
the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
20 files, 885,255 bytes, of which 14 files and 264,708 bytes are retained.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `search/packer/candidates/s270_sw.cert` | `b6453e8fa04e9f1064ba238bb080e0d90a0ddf05` | 39318 | `a01114af338f092232c0b7de07bfd164a636ef6355e15259c7fcb5812aa6034f` |
| `search/packer/candidates/s270_sw_regularized.cert` | `113380183f70b0a85ef8a8993216a8dd0554887d` | 41070 | `776433d8e89b43727dc9da72096fb581b8f4ec4c619732c637bc0d14be8bad30` |

Both digests are the ones the issue prints.
Beside the two certificates the packet retains the KKT point, the binary64 input, the
solver’s and the regularizer’s reports, the prior-record summary and the comparison with
the register’s packing, with `LICENSE`, `CREDITS.md`, the root `README.md`, the format
and packer READMEs, and the source’s submission guide, `search/packer/SUBMITTING.md`,
which defines the words the issue uses for the packing’s relation to earlier ones.
No retained file is long enough to be stored compressed.
The source’s two checkers, `search/exact/verify_cert.py` and `verify_cert2.py`, the exact
solver `search/exact/exactsolve.py` and the basin explorer `search/packer/explore.py` are
pinned by digest only. They are byte-identical to the copies the
[n183 packet](../evand-n183-subgrid-2026-10-19/README.md) retains, and were not run.
The packer’s working log (`search/packer/PACKER.md`) and the near-record sweep the issue
names (`search/packer/dgen.py`, added in `a435c97`, the pin’s parent) are pinned by
digest only.

The regularized view’s report, `s270_sw_regularized.json`, says `"by": ["Evan Daniel"]`
and places the view at level 1, “differs from the source only in rattlers”. The pin’s
parent, `a435c97`, says the author’s `candidate.py` now writes that field as the
packing’s own finder; the n154, n155, n236 and n271 views’ reports, written before it,
said `"by": ["Francisco Couzo"]`, which the question put to the author on #669 asked
about.

## Exact Replay

The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, as the #659 to #694 imports did: `sqpack`’s exact
witness verifier and the independent rational corner checker
(`devtools.check_rational_witness_independent`), each deciding every wall and every pair
over $\mathbb{Q}$ after an exact half-angle conversion.
The count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on two workers.

The positive passes both routes, and both routes refuse both controls: the duplicate
square as an overlap of squares 0 and 1, and the translated square as outside the
container.
The positive clears every wall by at least $5.00 \times 10^{-21}$ and every pair by at
least $9.99 \times 10^{-21}$ on both routes.
The 3 jobs made 217,890 pair decisions in 26.65 route CPU seconds and 30.40 job wall
seconds, summed; the longest job took 10.99 seconds.
`certify --workers 2` took 21 seconds of wall time on 21 October 2026, on a four-core
host shared with other lanes at a load average of about 4.5, and `check --replay` decided
the receipt again in 28 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code. No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record at `main` `4851d8193` (21 October 2026), and `check-claims` rebuilds it, each
side from its own retained packet or, for T-056, from its binary64 print:

| Report at 270 | Holder | This certificate is below it by |
| --- | --- | --- |
| `T-174` (PR #574), the case ceiling | Nate Chaoweeraprasit, improved by PingYou Ltd | $3.47 \times 10^{-5}$ |
| `T-151` (#500) | Nate Chaoweeraprasit | $3.47 \times 10^{-5}$ |
| Mishapolk’s `70a033f` certificate | Mykhailo Polkovskyi (Mishapolk) | $3.47 \times 10^{-5}$ |
| #593 | Mykhailo Polkovskyi (Mishapolk) | $3.47 \times 10^{-5}$ |
| #573 | Mykhailo Polkovskyi (Mishapolk) | $1.61 \times 10^{-3}$ |
| `T-140` (#488) | Francisco Couzo | $1.61 \times 10^{-3}$ |
| `T-136` (#481) | Nate Chaoweeraprasit | $1.62 \times 10^{-3}$ |
| `T-134` (#476) | Francisco Couzo | $8.56 \times 10^{-3}$ |
| `T-130` (#460) | Francisco Couzo | $8.56 \times 10^{-3}$ |
| `T-138` (#470) | Mykhailo Polkovskyi (Mishapolk) | $8.56 \times 10^{-3}$ |
| `T-119` (#399) | Evan Daniel | $9.64 \times 10^{-3}$ |
| `T-098` (#375) | Evan Daniel, at Francisco Couzo’s packing | $9.65 \times 10^{-3}$ |
| `T-056` | Francisco Couzo | $9.65 \times 10^{-3}$ |

The margin below the case ceiling is exactly the difference `claims.json` records,
$0.0000347411322664733798710171\ldots$.
The certificate is below every report the record holds or has pending at 270, and no
other open report through #703 states a bound at 270. The issue also compares against
Francisco Couzo’s `4e4c8ce` and `58a7833` at the register’s side; the record’s read of
that repository at `58a7833` found its files inside the corpus, but for 237, to be
copies of certificates the record holds, or larger ones.

## Lineage

The issue says the packing came from Nate Chaoweeraprasit’s #500 packing, the register’s
s(270) packing as PingYou Ltd improved it in PR #574: on 17 October the author’s basin
explorer started from #500’s packing in a test run and stored eight generations of
non-record descendants, the last $9.2 \times 10^{-3}$ above the record.
On 20 October a near-record sweep (`dgen.py sweep`, over 42 counts) chose 24 starts from
the 1,069 distinct stored 270s, far apart by a configuration fingerprint and
$10^{-3}$ to $10^{-2}$ above the best known side, and ran four 40-minute explorer runs on
one core each, which stored 1,357 new non-record 270s. This packing came 38 minutes into
one run, five moves from its start: a kick, a row slide, an L-kick and two crossovers
with other packings of the same run, each re-polished; `exactsolve.py` certified it
directly, with no descent needed.
It asks that #500’s packing be credited as the ultimate start.
It calls the packing a new packing, a different local minimum from the register’s: the
exact sides differ by $3.47 \times 10^{-5}$; matched over the eight symmetries of the box,
the contact graphs share 514 pairs, with 49 only in each, and share neither packing’s one
rattler; no load-bearing tilt angle is shared; and matched square by square on the
regularized views’ load-bearing squares, the largest move is 0.391, with 17 squares moving
by more than 0.1 and 59 by more than 0.01.
That is the source’s statement; no identity or lineage is measured here.

## What Is Not Established

The certificate establishes a finite upper bound at its exact side, nothing more.
The source states that its KKT point is a local minimum of the side, strict modulo 23
exact flat motions and not isolated, with 113 wall and 1,524 square-to-square contact
equations, 263 corner-to-corner contacts, no corner-to-corner MILP descent, 1 rattler
and 67 tilted squares, all load-bearing. Those are numerical evidence at 80 digits, as
the source says, not interval proofs, and were not replayed here.
Novelty, local or global optimality and rigidity are not established.
The regularized view has the same exact side; it is the source’s display view, not a
separate claim, and was not replayed.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`, which states that the work was done with Claude (Anthropic) under human
direction and without peer review. The pinned commit names Claude Opus 5.5 as co-author
and says the commit and push were approved by Evan Daniel.
The issue asks for the credit name “Evan Daniel (GitHub @evand)” and that
Chaoweeraprasit’s #500 packing be credited as the ultimate start.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-n270-sweep-2026-10-20 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n270-sweep-2026-10-20 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n270-sweep-2026-10-20 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n270-sweep-2026-10-20 check --replay
```

`check` admits the receipt structurally against the retained certificate; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs; the records
pull request of 21 October registers it as `T-224`, at V0/C0 until the stage 4 review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
