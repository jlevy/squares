# Evan Daniel’s s(343) Sweep Certificate

[Issue #702](https://github.com/jlevy/squares/issues/702) reports an exact rational
packing of 343 unit squares, in
[evand/square-packing](https://github.com/evand/square-packing/tree/88385abc95ab25d520302282d1946cbb07bc9cf3/search/packer/candidates).
The packet pins the commit the issue names,
`88385abc95ab25d520302282d1946cbb07bc9cf3` (tree
`34fd62e00173b6b9abf84d8368a9edf83e4b6a97`, committed 2026-10-20T21:47:03Z), which adds
the nine n = 343 files, and the eight n = 270 files of
[#703](https://github.com/jlevy/squares/issues/703), which the
[n270 packet](../evand-n270-sweep-2026-10-20/README.md) retains and this one does not.
The issue was filed at 2026-10-20T22:09:31Z, 22 minutes later.
The sources were retrieved on 21 October 2026, when the pin was the branch head.

| n | Exact side of the certificate | The issue prints, rounded up | Rounded up at 16 places |
| --- | --- | --- | --- |
| 343 | `18977682482404124568634475670459/1000000000000000000000000000000` | 18.977682482405 | 18.9776824824041246 |

The side is $18.977682482404124568634475670459$ exactly, which rounded up at 12 places
is the $18.977682482405$ the issue prints.
343 is beyond the record’s $n \le 324$ case corpus, so the side is a beyond-horizon row
of the source register, not a register entry, as the author’s 343 of
[#489](https://github.com/jlevy/squares/issues/489) is.
The certificate, `s343_sw.cert`, gives 343 unit squares, each a rational centre and a
rational $t = \tan(\theta/2)$, in an open square of the stated side, in the format of
issues #489, #552, #659, #664, #669, #680, #689, #694 and #703.
The commit also holds the 80-digit KKT point it was certified from
(`s343_sw.exact.txt`), the binary64 packing that point was solved from, the point before
the corner-slip descent (`s343_sw.predescent.txt`), the solver’s report, a summary of the
record the author compared against (`s343_sw_prior.json`), a regularized view of the same
packing at the same side (`s343_sw_regularized.cert`, 31 angle groups from 41) with its
report, and the source’s comparison with Francisco Couzo’s #678 packing
(`s343_sw_vs_prior.json`). The claim rests on `s343_sw.cert`.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of a blobless clone at
the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
22 files, 1,006,244 bytes, of which 15 files and 382,667 bytes are retained.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `search/packer/candidates/s343_sw.cert` | `2fdd87c5f1d539430a75f916e43d941ef9ffa354` | 57008 | `18415455772cb1b9cdfd3b7384695ea202fb6a02291e2ede2db777e93d207dfa` |
| `search/packer/candidates/s343_sw_regularized.cert` | `b8d2a9ecb5b76d455795dc7262a64ba6baa3886b` | 56116 | `f9a147750b51bfb3d24fa5469e93aeab903bad472f8d294b15250f2c3473e2b8` |

Both digests are the ones the issue prints.
Beside the two certificates the packet retains the KKT point, the binary64 input, the
pre-descent point, the solver’s and the regularizer’s reports, the prior-record summary
and the comparison with #678’s packing, with `LICENSE`, `CREDITS.md`, the root
`README.md`, the format and packer READMEs, and the source’s submission guide,
`search/packer/SUBMITTING.md`, which defines the words the issue uses for the packing’s
relation to earlier ones. The comparison, 2,420 lines, is stored compressed by the
archive’s rule (Compressed Files, below).
The source’s two checkers, `search/exact/verify_cert.py` and `verify_cert2.py`, the exact
solver `search/exact/exactsolve.py` and the basin explorer `search/packer/explore.py` are
pinned by digest only. They are byte-identical to the copies the
[n183 packet](../evand-n183-subgrid-2026-10-19/README.md) retains, and were not run.
The packer’s working log (`search/packer/PACKER.md`), the near-record sweep the issue
names (`search/packer/dgen.py`, added in `a435c97`, the pin’s parent) and the corner-slip
descent it names (`search/exact/descend.py`) are pinned by digest only.

The regularized view’s report, `s343_sw_regularized.json`, says `"by": ["Evan Daniel"]`
and places the view at level 2, “same packing: traversable without expansion (angle moves
path-checked; slides by construction)”.
The prior-record summary names the packing it compared against as
“pending:#678 (Francisco Couzo (franciscouzo))”, as watched in
`franciscouzo/square-packing@7b6c87e`, the commit the
[#678 packet](../couzo-issue678-2026-10-18/README.md) pins.

## Exact Replay

The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, as the #659 to #703 imports did: `sqpack`’s exact
witness verifier and the independent rational corner checker
(`devtools.check_rational_witness_independent`), each deciding every wall and every pair
over $\mathbb{Q}$ after an exact half-angle conversion.
The count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process, on two workers.

The positive passes both routes, and both routes refuse both controls: the duplicate
square as an overlap of squares 0 and 1, and the translated square as outside the
container.
The positive clears every wall by at least $5.00 \times 10^{-21}$, exactly
$1/(2 \cdot 10^{20})$, and every pair by at least $9.99 \times 10^{-21}$ on both routes.
The 3 jobs made 351,918 pair decisions in 51.74 route CPU seconds and 53.62 job wall
seconds, summed; the longest job took 18.25 seconds.
The triage priced the replay at about 45 route CPU seconds, from #689’s receipt at 308
scaled by $(343/308)^2$.
`certify --workers 2` took 37 seconds of wall time on 21 October 2026, on a four-core
host shared with other lanes at a load average of about 2.5, and `check --replay`
decided the receipt again in 53 seconds of wall time.

[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. Neither is the author’s code. No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record at `main` `d640ad8fb` (21 October 2026), and `check-claims` rebuilds it, each
earlier side from its own retained packet where the record holds one exactly and from
its print otherwise.
343 has no case record; the grid’s side there is 19.
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) is the
record `check_source_coverage` reads the beyond-horizon row against.

| Row at 343 | Holder | Disposition on `main` | This certificate is below it by |
| --- | --- | --- | --- |
| `couzo-issue678-2026-10-18` (#678), its print 18.978232204823 | Francisco Couzo | current, reported | $5.497224 \times 10^{-4}$ |
| `evand-record-hunt3-2026-10-10` (#489) | Evan Daniel | superseded by #678’s | $5.500412 \times 10^{-4}$ |
| `fang-two-wedge-certificates-2026-10-10` (#484) | Kevin Fang | superseded by #489’s | $1.722105 \times 10^{-2}$ |
| The grid, side 19 | | | $2.231752 \times 10^{-2}$ |

The margin below #678’s print is exactly the difference `claims.json` records,
$0.000549722418875431365524329541$, and holds however that print was rounded; the
certificate the #678 packet retains has the exact side
$41733573967670534550712079/2199023255552 \cdot 10^{-12} = 18.9782322048224771\ldots$,
which is $5.497224 \times 10^{-4}$ above this one.
The margin below #489’s row is exact, $0.000550041231486711096036435564$.

The certificate is below every row the source register holds at 343, and no other open
report through #703 states a bound at 343.
Francisco Couzo’s #678 reached this repository on 18 October, before #702, and each is
below the row before it, so the owner’s rule of 14 October records both, in report order
([result-import.md, Several Reports at One Count](../../../campaign/result-import.md#several-reports-at-one-count)).

## Lineage

The issue gives the packing’s lineage in three steps.
On 10 October, in the author’s Hunt 3 (#489), Kevin Fang’s #484 packing of 344 less one
square went through the author’s basin explorer at 343
(`search/packer/explore.py`), which besides #489’s record stored many non-record 343s.
On 20 October a near-record sweep (`dgen.py sweep`, over 42 counts) chose 24 starts from
the 1,552 distinct stored 343s, far apart by a configuration fingerprint and $10^{-3}$ to
$10^{-2}$ above the best known side, and ran four 40-minute explorer runs on one core
each, which stored 2,131 new non-record 343s. This packing came 28 minutes into one run,
seven moves from its start, one of the Hunt 3 packings $7.4 \times 10^{-3}$ above the
record: a kick, a band move and five symmetric kicks, each re-polished.
A corner-slip descent (`search/exact/descend.py`) then lowered it from 18.9776923 to
18.9776825, and `exactsolve.py` certified it.
The issue places it in Fang’s two-wedge family (#484), the design of #678 and of #489’s
343, and credits that family as the construction, as #489 did.
It calls the packing a new packing, a different local minimum from #678’s: the exact
sides differ by $5.497 \times 10^{-4}$; matched over the eight symmetries of the box, the
contact graphs share 602 pairs, with 100 only in this packing and 109 only in #678’s, and
5 of this packing’s 11 rattlers; no load-bearing tilt angle is shared; and matched square
by square on the regularized views’ load-bearing squares, the largest move is 0.242, with
12 squares moving by more than 0.1 and 107 by more than 0.01.
It reports the same relation to its nearest stored packing, a non-record 343 at
18.985669223699.
That is the source’s statement; no identity or lineage is measured here.

## What Is Not Established

The certificate establishes a finite upper bound at its exact side, nothing more.
The source states that its KKT point is a local minimum of the side, strict modulo 82
exact flat motions and not isolated, with 111 wall and 1,683 square-to-square contact
equations, 203 corner-to-corner contacts, no corner-to-corner MILP descent and 11
rattlers, and 106 tilted squares in the regularized view, 103 of them load-bearing.
Those are numerical evidence at 80 digits, as the source says, not interval proofs, and
were not replayed here.
Novelty, local or global optimality and rigidity are not established.
The regularized view has the same exact side; it is the source’s display view, not a
separate claim, and was not replayed.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`, which states that the work was done with Claude (Anthropic) under human
direction and without peer review. The pinned commit names Claude Opus 5.5 as co-author
and says the commit and push were approved by Evan Daniel.
The issue asks for the credit name “Evan Daniel (GitHub @evand)” and credits Kevin Fang’s
two-wedge family (#484) as the construction, as in #489.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-n343-sweep-2026-10-20 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n343-sweep-2026-10-20 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n343-sweep-2026-10-20 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-n343-sweep-2026-10-20 check --replay
```

`check` admits the receipt structurally against the retained certificate; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs; the records
pull request of 21 October records 343 as a beyond-horizon row of the source register,
`evand-n343-sweep-2026-10-20`, and registers no result.

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `source/search/packer/candidates/s343_sw_vs_prior.json.gz` | upstream | `483327990340fbb4a5e87f63e761cc78a958c81d` | `5c02d42aa6cb4da5bcdee27718099ab611a33504a76c8ad139461076cdd3cb48` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
