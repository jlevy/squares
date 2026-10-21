# Evan Daniel’s s(154) Sweep Certificate

[Issue #694](https://github.com/jlevy/squares/issues/694) reports an exact rational
packing of 154 unit squares, in
[evand/square-packing](https://github.com/evand/square-packing/tree/1d2bb82035af4b7eb4658488543e46b67d1099ca/search/packer/candidates).
The packet pins the commit the issue names,
`1d2bb82035af4b7eb4658488543e46b67d1099ca` (tree
`0eeb61451d9bece767cac0962118d25513b740bf`, committed 2026-10-20T03:54:48Z), which adds
the eight n = 154 files and the comparison program `search/packer/analysis/cmp154.py`.
The issue was filed at 2026-10-20T03:56:43Z, 115 seconds later.
The sources were retrieved on 20 October 2026, when the pin was the branch head.
The commit is dated 19 October in the author’s time zone (UTC−6) and 20 October in UTC;
the record dates it by UTC.
The author’s earlier s(154) packet, from #552, is
[evand-n154-2026-10-12](../evand-n154-2026-10-12/README.md).

| n | Exact side of the certificate | The issue prints, rounded up | Rounded up at 16 places |
| --- | --- | --- | --- |
| 154 | `1615137617595210068732072760947/125000000000000000000000000000` | 12.921100940762 | 12.9211009407616806 |

The side is $12.921100940761680549856582087576$ exactly, the decimal the issue prints.
The certificate, `s154_sw.cert`, gives 154 unit squares, each a rational centre and a
rational $t = \tan(\theta/2)$, in an open square of the stated side, in the format of
issues #489, #552, #659, #664, #669, #680 and #689.
The commit also holds the 80-digit KKT point it was certified from
(`s154_sw.exact.txt`), the binary64 packing that point was solved from, the solver’s
report, a summary of the record the author compared against (`s154_sw_prior.json`), a
regularized view of the same packing at the same side (`s154_sw_regularized.cert`, 10
angle groups from 19) with its report, and the source’s comparison with #586’s packing
(`s154_sw_vs_prior.json`). The claim rests on `s154_sw.cert`.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of a blobless clone at
the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
21 files, 766,052 bytes, of which 13 files and 164,990 bytes are retained.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `search/packer/candidates/s154_sw.cert` | `2ac12453c6cb54c8247d096d82326ab62602e1af` | 24302 | `c2242dcda1ae3d4c9d580af14ed9adf425780320d94846c3c96f5c3ee486d78d` |
| `search/packer/candidates/s154_sw_regularized.cert` | `73174fe992d5bc7eb3c2ec9522643d8002c8cdaf` | 23743 | `7fb7f288a864e9d3190e7b1b01f2491e7ce97f5e2e9e7de9b1dae3768580d2bd` |

Both digests are the ones the issue prints.
Beside the two certificates the packet retains the KKT point, the binary64 input, the
solver’s and the regularizer’s reports, the prior-record summary and the comparison with
#586, with `LICENSE`, `CREDITS.md`, the root `README.md`, and the format and packer
READMEs. No retained file is long enough to be stored compressed.
The source’s two checkers, `search/exact/verify_cert.py` and `verify_cert2.py`, the exact
solver `search/exact/exactsolve.py` and the basin explorer `search/packer/explore.py` are
pinned by digest only. They are byte-identical to the copies the
[n183 packet](../evand-n183-subgrid-2026-10-19/README.md) retains, and were not run.
The packer’s working log (`search/packer/PACKER.md`), the chained explorer
(`search/packer/chain.py`), the morph walk (`search/packer/landscape/morph.py`) and the
comparison program (`search/packer/analysis/cmp154.py`) are pinned by digest only.
The issue and the commit message name `search/packer/dgen.py`, the fingerprint sweep that
chose the restarts; no file of that name is in the tree at the pin.

The regularized view’s report, `s154_sw_regularized.json`, says
`"by": ["Francisco Couzo"]`, as the n155, n236 and n271 views’ reports do; the issue
credits Couzo’s #586 arrangement as a start, and the field is retained as the source
wrote it. The author answered the question put to him on #669 about that field in
[his comment of 20 October](https://github.com/jlevy/squares/issues/669#issuecomment-6302893217):
it was a bug in his tooling, which took the field from the record holder at that count
in his 5 October batch instead of from the packing drawn, fixed in
`search/packer/candidate.py` at `a435c97`, after this pin. He names `s154_sw` among the
affected views and asks that the field there be read as no credit at all, the issue’s
credit line being what he asks for.

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
The 3 jobs made 70,686 pair decisions in 8.9 route CPU seconds and 9.03 job wall seconds,
summed; the longest job took 3.14 seconds.
`certify --workers 2` took 8 seconds of wall time on 20 October 2026, on a four-core host
shared with other lanes at a load average of about 1, and `check --replay` decided the
receipt again in 9 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code. No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record at `main` `d588ad987` (20 October 2026), and `check-claims` rebuilds it, each
side from its own retained packet:

| Report at 154 | Holder | This certificate is below it by |
| --- | --- | --- |
| `T-186` (Mishapolk’s 70a033f), the case ceiling | Evan Daniel, improved by Francisco Couzo and Mishapolk | $1.06 \times 10^{-4}$ |
| `T-182` (#586) | Francisco Couzo | $1.06 \times 10^{-4}$ |
| `T-172` (#583) | Francisco Couzo | $1.40 \times 10^{-3}$ |
| `T-160` (#552) | Evan Daniel | $1.47 \times 10^{-3}$ |
| #593 | Mykhailo Polkovskyi (Mishapolk) | $1.40 \times 10^{-3}$ |

The margin below the case ceiling is exactly the difference `claims.json` records,
$0.000105636370950500085\ldots$.
The certificate is below every report the record holds or has pending at 154, and no
other open report through #698 states a bound at 154.

## Lineage

The issue says the packing came from the register’s s(156) packing, Daniil Ostashev’s:
on 14 October the author’s chained explorer removed two squares from it and, over five
basin-explorer moves at 154, three of them crossovers with descendants of close relatives
of #586’s packing, reached a stored non-record 154 at 12.928447. On 19 October he
restarted the explorer from stored 154 packings $10^{-3}$ to $10^{-2}$ above the record,
chosen to be far apart by a configuration fingerprint, that one among them, and symmetric
kicks, a kick, row slides and a band move reached 12.9211009408 in 771 seconds; twelve
40-minute runs from it stayed at that side, and `exactsolve.py` certified the point.
It asks that Francisco Couzo’s #586 arrangement, itself continued from the author’s #552,
and Ostashev’s s(156) packing be credited as its starts.
It calls the packing a different KKT point from #586’s, in its family: matched over the
eight symmetries of the box, the contact graphs share 232 pairs, with 61 only here and
64 only in #586’s, and a feasible-step morph walk finds no path between the two up to
$10^{-2}$ above #586’s side, which the issue calls a heuristic. It keeps #586’s band of
ten squares near 26.53° and its 38° to 44° group.
That is the source’s statement; the import measured no identity or lineage.
The stage 4 review measured it pose by pose
([review of 20 October](../../../../docs/project/reviews/review-2026-10-20-upper-bound-imports-689-694.md#credit-and-lineage)):
against #586’s packing the pairing is one to one under a quarter turn and moves three
squares beyond a tenth, at most 0.204, so it is #586’s arrangement continued, while
Ostashev’s s(156) packing lies within a tenth of it at only 94 of its 156 squares, so
that start is the source’s account of the search.

## What Is Not Established

The certificate establishes a finite upper bound at its exact side, nothing more.
The source states a KKT point that it has not shown to be a strict local minimum: its
second-order test finds one negative-curvature direction, blocked only to first order by
weakly active contacts, and calls the status inconclusive. It reports 58
corner-to-corner contacts, no corner-to-corner MILP descent, 51 exact flat motions, 9
rattlers and 38 tilted squares. Those are numerical evidence at 80 digits, as the source
says, not interval proofs, and were not replayed here.
Novelty, local or global optimality and rigidity are not established.
The regularized view has the same exact side; it is the source’s display view, not a
separate claim, and was not replayed.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`, which states that the work was done with Claude (Anthropic) under human
direction and without peer review. The pinned commit names Claude Opus 5.5 as co-author
and says the commit, push and post were approved by Evan Daniel.
The issue asks for the credit name “Evan Daniel (GitHub @evand)” and that Couzo’s #586
arrangement and Ostashev’s s(156) packing be credited as its starts.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-n154-sweep-2026-10-20 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n154-sweep-2026-10-20 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n154-sweep-2026-10-20 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n154-sweep-2026-10-20 check --replay
```

`check` admits the receipt structurally against the retained certificate; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs; the records
pull request of 20 October registers it as `T-222`, at V0/C0 until the stage 4 review.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
