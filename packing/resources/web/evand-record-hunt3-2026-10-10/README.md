# Evan Daniel’s Hunt 3 Certificates: 132, 308, 343 and 344

[Issue #489](https://github.com/jlevy/squares/issues/489) reports four exact rational
packings from Evan Daniel’s record hunt Hunt 3, in
[evand/square-packing](https://github.com/evand/square-packing/tree/76a529bc6f36ed05827cae3d1412d6acb5be00fc/search/packer/candidates).
The issue names commit `c013f43` (2026-10-10T13:46:56Z). The packet pins the branch head
when the sources were retrieved, `76a529bc6f36ed05827cae3d1412d6acb5be00fc` (tree
`c1f6626649091961088c28114403b2bbd7bd76c2`, committed 2026-10-10T14:48:25Z), whose
parent is `c013f43`. That commit changes only the packer log and
`search/packer/pk/pending.yaml`, so every retained byte is the same at both.
The issue was filed at 2026-10-10T14:47Z.

| n | Exact side of the certificate | The issue prints | Rounded up at 16 places |
| --- | --- | --- | --- |
| 132 | `5992840099422904405761115982051/500000000000000000000000000000` | 11.985680198845808811522231964102 | 11.9856801988458089 |
| 308 | `17998269879526255875387992744507/1000000000000000000000000000000` | 17.998269879526255875387992744507 | 17.9982698795262559 |
| 343 | `18978232523635611279730512106023/1000000000000000000000000000000` | 18.978232523635611279730512106023 | 18.9782325236356113 |
| 344 | `148394144642792199383704185913/7812500000000000000000000000` | 18.994450514277401521114135796864 | 18.9944505142774016 |

Each certificate gives `n` unit squares, each a rational centre and a rational
$t = \tan(\theta/2)$, in an open square of the stated side, in the format of issues
#375, #399 and #465. Every side terminates within 30 places, and the issue prints each
one exactly. The pin holds a fifth Hunt 3 certificate, at 305, which the issue does not
name. The message of `c013f43` prints its side rounded up as 17.951139772207, and the
packer log at the pin drops it (see below).
The certificates at 132 and 344 were first committed in `f7a2325`
(2026-10-10T09:15:50Z). `c013f43` replaced those at 305 and 308 and added the one at
343\. The sources were retrieved at 2026-10-10T17:08Z.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout at the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json); every file
is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
26 files, 782,804 bytes.

| Upstream path | Git blob | Bytes | SHA-256 |
| --- | --- | --- | --- |
| `search/packer/candidates/hunt3_n132.cert` | `d31dbcba2d3c219ad4aa78090eaccb8da6c6be3a` | 21420 | `a0def8c4e0bd5425c96f68054eb44fd0766cbd433bb3c324f366f1a19d70baa2` |
| `search/packer/candidates/hunt3_n305.cert` | `e0cddd54c99ca48f70215625ea25040f7169b514` | 46106 | `baa52f50c527472810f24dbbdeee9b21cdacbdece2e9fb9c1bfcf134f414449c` |
| `search/packer/candidates/hunt3_n308.cert` | `d79ff11875868224a14d60b5e6cc8f79cbfc5336` | 52119 | `41961a5e096afa5f7763419d81b2958c54f37aae5e54e51a0c54ca23946da734` |
| `search/packer/candidates/hunt3_n343.cert` | `670f643ca74410cb9063aaef100d2923d047a830` | 57308 | `bf05962c580d46bbeef5ad66fee5d3ca45dab7002d726c424126d9b9259f4332` |
| `search/packer/candidates/hunt3_n344.cert` | `461c4d2dda6ca743c169ee490d00451638bf2bc3` | 57344 | `54bb6b6696b96ccf6a30db313ee4e62240fe17c070624fd916b59b483f7b20cc` |

For each count the packet retains four files: the `.cert` certificate, the 80-digit KKT
point it was rounded from (`.exact.txt`), the binary64 packing that point was solved
from (`.input.txt`), and the solver’s report (`.json`) with multipliers, the reduced
Hessian and the corner-to-corner jamming check.
It also retains `LICENSE`, `CREDITS.md` and `search/exact/README.md`, 23 files and
652,501 bytes in all.
The source’s two checkers, `search/exact/verify_cert.py` and `verify_cert2.py`, are
pinned by digest only.
They are byte-identical to the copies the
[issue-399 packet](../evand-new-arrangements-2026-10-07/README.md) retains, and were not
run. The packer’s working log, `search/packer/PACKER.md` (123,801 bytes), is pinned by
digest only.

## Exact Replay

Only the five certificates enter geometry decisions.
They go through the maintained two-route kernel of `devtools.evand_arrangement_reports`,
which the issue-399 and issue-465 imports also used.
The two routes are `sqpack`’s exact witness verifier and the independent rational corner
checker. Each decides every wall and every pair over $\mathbb{Q}$ after an exact
half-angle conversion.
Each count runs a positive job, a duplicate-square control and an outside-container
control, each in its own child process.

All five positives pass both routes.
Both routes refuse all ten controls, each on the overlap or the wall it was built to
break. In every positive the two routes find the same least wall clearance, exactly
`1/200000000000000000000` ($5 \times 10^{-21}$), and the same least pair gap, just under
$10^{-20}$, as the issue states.
The 15 jobs made 1,319,598 pair decisions in 308.35 route CPU seconds and 409.47 job
wall seconds, summed.
The longest job, the positive at 343, took 43.27 seconds, and the two-worker run took 3
minutes 33 seconds of wall time.
Other lanes held the four-core machine at a load average of about 7 during the run, so
the walls overstate the work and the route CPU seconds do not.
A fresh serial `check --replay` decided all 15 jobs again, equal to the retained rows
apart from timing, in 5 minutes 33 seconds.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. The register entry and its beyond-horizon rows would cite the four requested
certificates. Each was also decided by the third exact route,
`devtools.check_half_angle_area decide-imports`, which reads the certificate with its
own parser and decides containment by each square’s half-extent and overlap by exact
clipping. That route accepts all four and reaches the required outcome on all 24 of its
controls. It finds the same least wall clearances as both maintained routes and a least
Euclidean distance between squares of $1.00 \times 10^{-20}$ at every count.
Run as `decide-imports --imports '#488' '#489'` with `--upstream` for both packets,
which also holds each retained certificate to its bytes fetched at the pin, it found no
disagreement across the ten certificates of the two imports, in 19 seconds on two
workers. The third route does not read the certificate at 305, which no entry cites.
No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes each certificate against the
record as it stood when the issue was read (`main` at `af17208c0`, 10 October 2026).
`check-claims` rebuilds it, the case ceilings and the issue-476 and T-131 sides from
their own retained packets:

| n | Case ceiling, holder | Below it by | Other pending reports at the count | Smallest |
| --- | --- | --- | --- | --- |
| 132 | 11.9913278876915015, Evan Daniel’s exact optimum of Francisco Couzo’s packing (T-098) | $5.65 \times 10^{-3}$ | #488 prints 11.986953587255, above by $1.27 \times 10^{-3}$; #476 above by $1.27 \times 10^{-3}$; #470 prints 11.986956226066, above by $1.28 \times 10^{-3}$; T-131 (#465) above by $1.42 \times 10^{-3}$ | this certificate |
| 308 | 18, the grid, in both lanes | $1.73 \times 10^{-3}$ | #484 prints 17.999309855162748, above by $1.04 \times 10^{-3}$ | this certificate |
| 343 | none: beyond the horizon; the grid’s 19 | $2.18 \times 10^{-2}$ | #484 prints 18.994903529220497, above by $1.67 \times 10^{-2}$; #470 prints 19.000000000007, above the grid | this certificate |
| 344 | none: beyond the horizon; the grid’s 19 | $5.55 \times 10^{-3}$ | #484 prints 18.995489275430816, above by $1.04 \times 10^{-3}$; #470 prints 19.002369297056, above the grid | this certificate |

A side a report prints, and does not retain here, is compared at its printed places.
Where the report says it rounded up, the side may be up to one unit in the last place
below the print. Where it does not say, the side may be one unit either way.
Issue #488’s six sides and issue #484’s three are retained in their own packets, the
[issue-488 packet](../couzo-certificates-2026-10-10/README.md) and the
[issue-484 packet](../fang-two-wedge-certificates-2026-10-10/README.md), and the frozen
comparisons read their prints.
At 132 the certificate is below every report the record holds or has pending, by
$1.27 \times 10^{-3}$ or more.
None of #481, #483, T-128 and T-130 reports any of the four counts.

The certificate at 305, which the issue does not name, is an import of its own
(`result-import.md`, stage 1), compared here and registered by no entry of this import.
It is below the case ceiling, 17.9529594590155280 (T-098), by $1.82 \times 10^{-3}$, and
below issue #481’s printed 17.951196144147385 by $5.64 \times 10^{-5}$. Its exact side,
`8975569886103498772971256586313/500000000000000000000000000000`, is the side of
Francisco Couzo’s issue #488 certificate at 305. The frozen comparison reads #488’s
12-place print, which cannot decide between them, so it names neither as the smaller.
The two are the same arrangement up to a quarter turn of the box.
Matched square by square by the third route’s `arrangement_gap`, 271 of the 305 lie
within $10^{-9}$ of their counterparts and the other 34 within $1.77 \times 10^{-2}$;
the Hunt 3 solver report lists 3 free squares and 44 exact flat motions at that point.
The `c013f43` timestamp is five minutes earlier than Couzo’s commit, 13:52:27Z. The
packer log at the pin says that #488 was filed before this commit was pushed.
It also says that both packings descend from SQUISH’s through `fq`, and it drops 305 as
Couzo’s. The issue does not report it.

The record keeps 343 and 344 as dated beyond-horizon rows, the form Kevin Fang’s
issue-484 sides take: one row each in `beyond_horizon_claims` of `source-coverage.yaml`,
keyed on the count and this source, with the side the issue prints,
`assurance: reported` and `disposition: tracked-outside-case-corpus`, and no case
record, register row, selected bound or atlas entry.
A row there must equal its source’s reparsed claim byte for byte, so
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the two claims alone, and the source’s coverage entry names it as its `claims_record`.
Both are smaller than the issue-484 rows at those counts, which these supersede once
both are registered.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
The source makes three statements about each exact point.
First, it is a KKT point with positive multipliers on its load-bearing contacts, the
smallest at least $1.8 \times 10^{-7}$. Second, its reduced Hessian is positive
semidefinite modulo exact flat motions: 31 at 132, 52 at 308, 19 at 343 and 71 at 344.
Third, a first-order MILP finds it jammed in every corner-to-corner branch.
Those are numerical evidence, as the source itself says, and were not replayed here.
So are its matching distances from the packings each started from.
Novelty, local or global optimality and rigidity are not established, and no review of
the replay has been made.
The source expects further improvement at 343.

## Credit and Licence

Evan Daniel wrote the source under the MIT licence (`LICENSE`), with credits in
`CREDITS.md`. Its commits disclose Claude (Anthropic) as co-author, and the issue states
that the search code and the request were written with Claude under his direction.
The packings at 308, 343 and 344 build on Kevin Fang’s packings from
[issue #484](https://github.com/jlevy/squares/issues/484), in the two-wedge family of
Arslanov, Mustafin and Shangitbayev.
The issue asks that the construction be credited to him:

- 344 is his packing, polished and moved by a corner-to-corner descent to a nearby exact
  local minimum;
- 308 is his packing, polished and then moved by seven explorer steps;
- 343 started from his 344 less one square, in a different basin from his 343.

The packing at 132 is the author’s own lineage from issue #465, eight explorer moves
from a packing below 12 out of his earlier 132 runs.
The search was the quality-diversity basin explorer of #465 with a two-parent crossover
move added.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source evand-record-hunt3-2026-10-10 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-record-hunt3-2026-10-10 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-record-hunt3-2026-10-10 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports evand-record-hunt3-2026-10-10 check --replay
uv run --frozen --all-extras --group dev python -m devtools.check_half_angle_area decide-imports --workers 2 --imports '#488' '#489'
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 2` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
