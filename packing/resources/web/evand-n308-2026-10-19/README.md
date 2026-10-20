# Evan Daniel’s s(308) Certificate

[Issue #689](https://github.com/jlevy/squares/issues/689) reports an exact rational
packing of 308 unit squares, in
[evand/square-packing](https://github.com/evand/square-packing/tree/bc0708fc75c84cffd241e1901c71fbdd120542a3/search/packer/candidates).
The packet pins the commit the issue names,
`bc0708fc75c84cffd241e1901c71fbdd120542a3` (tree
`e5c826d0c667fef3abbff3820d5c91b800c25d7a`, committed 2026-10-19T22:41:02Z), which adds
the eight n = 308 files.
The issue was filed at 2026-10-19T22:44:19Z, 197 seconds later.
The sources were retrieved on 20 October 2026, when the branch head was `1d2bb82`; the
two later commits leave the eight files unchanged.

| n | Exact side of the certificate | The issue prints, rounded up | Rounded up at 16 places |
| --- | --- | --- | --- |
| 308 | `3599429824254181747030632150463/200000000000000000000000000000` | 17.997149121271 | 17.9971491212709088 |

The certificate, `s308_d308.cert`, gives 308 unit squares, each a rational centre and a
rational $t = \tan(\theta/2)$, in an open square of the stated side, in the format of
issues #489, #552, #659, #664, #669 and #680.
The commit also holds the 80-digit KKT point it was certified from
(`s308_d308.exact.txt`), the binary64 packing that point was solved from, the solver’s
report, a summary of the record the author compared against (`s308_d308_prior.json`), a
regularized view of the same packing at the same side (`s308_d308_regularized.cert`, 29
angle groups from 34) with its report, and the source’s comparison with #489’s packing
(`s308_d308_vs_prior.json`). The claim rests on `s308_d308.cert`.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of a blobless clone at
the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
20 files, 906,877 bytes, of which 13 files and 309,168 bytes are retained.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `search/packer/candidates/s308_d308.cert` | `a8781bd8a09c24a8fd2b9823a31bd5f0bc511ed1` | 47184 | `6a9c03318ee5a703313b5dcab02febbe6b520133ffea0a21ea2ecf0741c42a91` |
| `search/packer/candidates/s308_d308_regularized.cert` | `745dbc4864a9dde1b6c64d4a4f076cbdd276e132` | 50250 | `5e5af5a4833656743ae84c66dcaa6b2cd3d65d9e8308ff1323240f33520c2f03` |

Both digests are the ones the issue prints.
Beside the two certificates the packet retains the KKT point, the binary64 input, the
solver’s and the regularizer’s reports, the prior-record summary and the comparison with
#489 (stored compressed, below), with `LICENSE`, `CREDITS.md`, the root `README.md`, and
the format and packer READMEs.
The source’s two checkers, `search/exact/verify_cert.py` and `verify_cert2.py`, the exact
solver `search/exact/exactsolve.py` and the basin explorer `search/packer/explore.py` are
pinned by digest only. They are byte-identical to the copies the
[n183 packet](../evand-n183-subgrid-2026-10-19/README.md) retains, and were not run.
The packer’s working log (`search/packer/PACKER.md`), the chained explorer
(`search/packer/chain.py`) and the morph walk (`search/packer/landscape/morph.py`) are
pinned by digest only.
The issue also names `search/packer/dgen.py` as the fingerprint that chose the six
restarts; no file of that name is in the tree at the pin or at the head `1d2bb82`.

The regularized view’s report, `s308_d308_regularized.json`, says `"by": []`, unlike the
n155, n236 and n271 views’ reports, which said `"by": ["Francisco Couzo"]`.

## Exact Replay

The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, as the #659 to #674 imports did: `sqpack`’s exact
witness verifier and the independent rational corner checker
(`devtools.check_rational_witness_independent`), each deciding every wall and every pair
over $\mathbb{Q}$ after an exact half-angle conversion.
The count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on two workers.

The positive passes both routes, and both routes refuse both controls: the duplicate
square as an overlap of squares 0 and 1, and the translated square as outside the
container.
Every positive clears every wall by at least $5.00 \times 10^{-21}$ and every pair by at
least $9.99 \times 10^{-21}$.
The 3 jobs made 283,668 pair decisions in 35.66 route CPU seconds and 36.22 job wall
seconds, summed; the longest job took 12.41 seconds.
`certify --workers 2` took 25 seconds of wall time on 20 October 2026, on a four-core
host shared with other lanes at a load average of about 1, and `check --replay` decided
the receipt again in 37 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code. No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record at `main` `d588ad987` (20 October 2026), and `check-claims` rebuilds it, each
side from its own retained packet:

| Report at 308 | Holder | This certificate is below it by |
| --- | --- | --- |
| `T-174` (PR #574), the case ceiling | Evan Daniel, improved by PingYou Ltd | $1.12 \times 10^{-3}$ |
| `T-141` (#489) | Evan Daniel, on Kevin Fang’s two-wedge construction | $1.12 \times 10^{-3}$ |
| `T-135` (#484) | Kevin Fang | $2.16 \times 10^{-3}$ |
| #593 | Mykhailo Polkovskyi (Mishapolk) | $1.12 \times 10^{-3}$ |

The margin below the case ceiling is exactly the difference `claims.json` records,
$0.00112075825534714005\ldots$.
The certificate is below every report the record holds or has pending at 308, and no
other open report through #698 states a bound at 308.

## Lineage

The issue says the packing came from Nate Chaoweeraprasit’s (itsnaka’s) s(307) packing
of #481, the register’s witness at 307: on 14 October the author’s chained explorer
inserted one square into it and five rounds of basin-explorer moves reached a non-record
308, and five further moves gave a stored packing at 17.998946. On 19 October he
restarted the explorer from six stored 308 packings chosen to be far apart by a
configuration fingerprint, that one among them, and symmetric kicks, a mirror move and
re-polishing reached 17.9971491213 in 710 seconds; twelve 40-minute runs from it stayed
at that side, and `exactsolve.py` certified the point.
It asks that #481’s s(307) packing be credited as the ultimate start, and says the
packing is not a refinement of #489 and does not descend from #489 or from Kevin Fang’s
#484: matched square by square over the eight symmetries of the box, 295 load-bearing
squares move by more than $10^{-4}$ (at most 0.706), and no tilt angle is shared.
That is the source’s statement; the import measured no identity or lineage.
The stage 4 review measured it pose by pose
([review of 20 October](../../../../docs/project/reviews/review-2026-10-20-upper-bound-imports-689-694.md#credit-and-lineage)):
under a quarter turn the best assignment against #489’s packing moves 15 squares beyond a
tenth, at most 0.708, and keeps 293 within one, and 263 of #481’s 307 squares lie within
a tenth of this packing, so it is another arrangement of the two-wedge design, not a
refinement, found from #481’s 307 by the source’s account.

## What Is Not Established

The certificate establishes a finite upper bound at its exact side, nothing more.
The source states that its KKT point is a local minimum of the side, strict modulo 47
exact flat motions, with 242 corner-to-corner contacts, no corner-to-corner MILP descent,
5 rattlers and 102 tilted squares, in the family of #484 and #489. Those are numerical
evidence at 80 digits, as the source says, not interval proofs, and were not replayed
here. Novelty, local or global optimality and rigidity are not established.
The regularized view has the same exact side; it is the source’s display view, not a
separate claim, and was not replayed.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`, which states that the work was done with Claude (Anthropic) under human
direction and without peer review. The pinned commit names Claude Opus 5.5 as co-author
and says the commit and push were approved by Evan Daniel.
The issue asks for the credit name “Evan Daniel (GitHub @evand)” and that
Chaoweeraprasit’s #481 s(307) packing be credited as the ultimate start.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-n308-2026-10-19 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n308-2026-10-19 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n308-2026-10-19 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n308-2026-10-19 check --replay
```

`check` admits the receipt structurally against the retained certificate; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs; the records
pull request of 20 October registers it as `T-221`, at V0/C0 until the stage 4 review.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/search/packer/candidates/s308_d308_vs_prior.json.gz` | upstream | `414d1f2aabc2a07b1a866c597828495e1fe6ca47` | `26801cac86717dde5c432ec06bcc2b457c2066ae05a94cbc655932e646574230` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
