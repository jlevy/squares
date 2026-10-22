# Francisco Couzo’s Issue 670: 73 Certificates at 23aff0c6

Francisco Couzo’s [issue #670](https://github.com/jlevy/squares/issues/670), opened
2026-10-17T18:05:06Z, asks to register 73 upper bounds for n = 204 and 330 to 993, each
the exact rational side of a certificate in
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/23aff0c6f992271e1ad13a148d44f392c4b386c0)
at `23aff0c6f992271e1ad13a148d44f392c4b386c0` (committed 2026-10-17T18:00:09Z) rounded up
at 12 places.
This packet retains the one row in the n ≤ 324 case corpus, s(204), registered as T-226.
Since 22 October it also retains the issue’s 72 rows beyond the corpus, recorded as
dated beyond-horizon rows ([Beyond the Corpus](#beyond-the-corpus)).

| n | Exact side of the certificate | Issue’s print, rounded up | SHA-256 |
| --- | --- | --- | --- |
| 204 | `45044217780850246618141/3041751595240000000000` | 14.808644417690 | `f317d0c0b04b947b9199ed47c998ff221d05e4d01849b942545364a173bc73dc` |

The certificate gives 204 unit squares, each a rational centre and a rational
$t = \tan(\theta/2)$, in Evan Daniel’s certificate format, which the header names.
Its per-count JSON, `certificates/n204.json`, names its digest and exact side and credits
the seed to Mykhailo Polkovskyi (Mishapolk), search job 105412 (`hop`).

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of a blobless clone at
the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json);
every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest.
Retained: every certificate the issue links, `source/certificates/nN.cert` at its 73
counts, each with its per-count JSON `nN.json`, 146 files, 7,453,248 bytes (2.65 MB as
Git’s zlib stores them): the 204 pair at 01:24Z on 22 October for T-226, and the 72
beyond the corpus from the same pin at 04:41Z. On 22 October at 19:10Z the 21
certificates the pin publishes beyond the corpus and the issue does not claim were added
from the same pin, 8 under `certificates/best/` and 13 at the root with their per-count
JSON ([The Pin’s Unclaimed Certificates](#the-pins-unclaimed-certificates)): 180 files,
13,835,156 bytes in all.
The repository states no licence for its data or prose, so the certificates and their
JSON are retained as factual data under the owner decision of 9 October 2026 recorded in
[known-best-packings/README.md](../known-best-packings/README.md).
Pinned by digest only: the root `README.md` and `upper_bounds.json`, the certificate
directory’s `README.md`, `manifest.json` and `SHA256SUMS`, and the source’s exact checker
`verify_bound_certificate.py` with its MIT licence `BOUND_VERIFIER_LICENSE.txt`, which are
byte-identical to the copies the [issue-678 packet](../couzo-issue678-2026-10-18/README.md)
retains and were not run.
The rest of the tree is pinned by the commit alone.

## Exact Replay

The certificate goes through the maintained two-route kernel of
`devtools.evand_arrangement_reports`, by the declaration-driven importer
`devtools.upper_bound_reports` ([acquisition/report.json](acquisition/report.json)):
`sqpack`’s exact witness verifier and the independent rational corner checker, each
deciding every wall and every pair over $\mathbb{Q}$ after an exact half-angle conversion.
Each count ran a positive job, a duplicate-square control and an outside-container
control, each in its own child process.
The positive passes both routes, and both routes refuse both controls. In the positive a square touches the box, a least wall clearance of exactly 0, which the closed box allows, and every pair clears by at least $5.47 \times 10^{-11}$. The 3 jobs made 124,236 pair decisions in 10.22 route CPU seconds, on one worker on 22 October 2026.
[receipts/exact-certification.json.xz](receipts/exact-certification.json.xz) keeps every
deciding input and both routes’ complete outputs.
The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method. No source program ran here, and the entry
awaits a stage 4 review (think-0nse).

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes the certificate against the
record on `main` at `d7923b8d`, 22 October 2026: above the case’s house best packing,
Couzo’s own #678 certificate (T-223), by $1.58 \times 10^{-6}$; above Evan Daniel’s view
of that packing (T-225) by the same; above Couzo’s #675 by $5.05 \times 10^{-8}$; below
Mykhailo Polkovskyi’s refinement T-186, which held the case when #670 was reported, by
$1.88 \times 10^{-5}$.
The [18 October ledger](../../../campaign/issue-intake/upper-bounds-20261018/README.md)
recorded it in report order, after T-186 and before #675; #678 and T-225 came later, each
smaller. So T-226 enters superseded.
Measured pose by pose in the
[issue-672 packet’s measurement](../couzo-issue672-2026-10-17/measure/identity.json),
#675’s packing is this one under the identity (5 squares beyond a tenth, at most 0.143),
Couzo’s own sequence; no regularization is recorded.

## Beyond the Corpus

The issue’s 72 rows from 330 to 993 read root `certificates/nN.cert`, each first committed
at the pin, five minutes before the issue
([receipts/first-commits.json](receipts/first-commits.json)).

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) reads every
certificate a row beyond the corpus names from this packet once `acquire_source --check`
holds it, and decides it with the filtered two-route decision and the six controls of
[`devtools.couzo_678_replay`](../../../devtools/couzo_678_replay.py), reused unchanged:
route `sqpack` through `sqpack.witness` and `sqpack.verify`’s exact predicates, route
`independent` through `devtools.check_rational_witness_independent`’s, over every corner
against every wall and every pair whose centres are closer than √2 by exact comparison.
A unit square’s interior lies in the open disc of radius √2/2 about its centre, so no
other pair can overlap; both routes check that every square is a unit square whose corner
mean is that centre. The [18 October packet](../couzo-issue678-2026-10-18/README.md#exact-replay)
states the six controls.

**All 72 are verified.** Every printed side is its header side rounded up at 12 places,
and both routes accept every packing: 118,501 candidate pairs of 17,911,878, and every
corner against every wall. 60 touch the box and 10 have touching pairs, 604 in all, which
the closed contract allows; elsewhere the least pair gap is between 1.0e-20 (at 382) and
7.8e-11. **All 432 controls are refused by both routes.** The positive decisions took 76.6
CPU seconds; [receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json)
keeps every row’s side, both routes’ counts, least clearance, least gap and failures, the
controls, and the per-count JSON’s seed credit. The maintained all-pairs kernel,
`devtools.evand_arrangement_reports`’s two routes with no filter, decided every pair at
922, the row that becomes current there: 424,581 pairs in 107.0 CPU seconds; both routes
accept it, and their least pair gap and wall clearance equal the filtered decision’s
exactly ([receipts/exhaustive-sample.json](receipts/exhaustive-sample.json)). The
all-pairs replay of every row, about 4 CPU-hours for the three Couzo packets at that rate,
is not run; the filtered route is the replay of record, as for #678 and #715. Every side
is below Göbel’s classical construction at its count, by 5.47e-03 at 330 or more
([receipts/goebel-comparison.json](receipts/goebel-comparison.json), the 15 October
packet’s retained program).

The [backlog ledger of 22 October](../../../campaign/issue-intake/upper-bounds-backlog-20261022/README.md)
walks every report at these counts from the 18 October ledger’s starts, frozen at `main`
`804eff369`, and records all 72. **Eight are current**, at 364, 370, 382, 403, 444, 452,
536 and 922: each supersedes the row that stood there, six of Couzo’s own 487b058 rows
(`couzo-verified-bounds-2026-10-14`), his 14 October certificate at 382
(`couzo-certificates-2026-10-14`) and Evan Daniel’s composition at 364
(`evand-compositions-2026-10-13`), by 2.74e-10 (at 382) to 5.07e-05. **64 are superseded
on entry** by the next report the walk records at their count: Couzo’s #675 (25), #672
(19), #678 (9) and #715 (2), and Darius Muglich’s #686 (9).
At 57 counts besides the eight, #670 is the first report the walk records and its row is
superseded in turn; the start there, 50 of `couzo-verified-bounds-2026-10-14`’s rows, six
of `couzo-certificates-2026-10-14`’s and `evand-fresh-compositions-2026-10-14`’s at 460,
now names #670 as its successor instead of the #678, #686 or #715 row that had superseded
it on `main`, so each count is one chain in report order.
Since 22 October Mykhailo Polkovskyi’s #719 rows
([`mishapolk-issue719-2026-10-22`](../mishapolk-issue719-2026-10-22/README.md)),
recorded by the [ledger of 22 October for issue
719](../../../campaign/issue-intake/upper-bounds-issue719-20261022/README.md), supersede
three of the eight, at 370, 452 and 536, by 2.88e-12 to 1.27e-11; five remain current.
[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the record
the source register reads them from.

## The Pin’s Unclaimed Certificates

Issue #670 claims 72 of the pin’s certificates beyond the corpus. The pin publishes 21 more at 325 to 1024 that the issue does not claim, at 547, 554, 602, 652, 653, 704, 705, 759, 814, 815, 816, 872, 873, 874, 932, 933, 934, 994, 995, 996 and 997: 8 under `certificates/best/` and 13 at the root. A publication in a watched repository is a report from its first commit (the owner, 14 October 2026), so since 22 October 2026 they are rows of their own, as the source `couzo-23aff0c-2026-10-17`, which the [history walk of Couzo’s watched publications](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) records in report order (think-tmwt).

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares this publication a release with no issue, `franciscouzo/square-packing@23aff0c`, and reads the rows the history walk records from [acquisition/watched-release-23aff0c.json](acquisition/watched-release-23aff0c.json), which `declare-rows` writes from the walk.

Each certificate was first committed at the commit itself ([receipts/23aff0c/first-commits.json](receipts/23aff0c/first-commits.json)).

**All 21 are verified.** The filtered two-route decision of `devtools.couzo_678_replay`, reused unchanged, accepts every packing on both routes (40,608 candidate pairs of 7,113,182, and every corner against every wall), and every side is its header side rounded up at 12 places. **All 126 controls are refused by both routes.** The positive decisions took 138.9 CPU seconds ([receipts/23aff0c/filtered-exact-replay.json](receipts/23aff0c/filtered-exact-replay.json)). 13 touch the box and 12 have touching pairs, which the closed contract allows. Every side is below Göbel’s classical construction at its count ([receipts/23aff0c/goebel-comparison.json](receipts/23aff0c/goebel-comparison.json)).

The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) walks every count from 325 to 1024 in report order from starts frozen at `main` `a97b712b9` and records all 21. **All 21 are superseded on entry**, by Couzo’s #672 (16) and Couzo’s #675 (5). The rows supersede first Couzo’s 4e4c8ce (4); at 17 counts no row stood before them.

[acquisition/beyond-horizon-rows-23aff0c.json](acquisition/beyond-horizon-rows-23aff0c.json) is the record the source register reads them from, as the source `couzo-23aff0c-2026-10-17`.

The walk records the pin’s publications at 71 more counts and holds each back from a row for its decision: 10 re-certifications below the side they beat by less than 10⁻¹² with the same 12-place print, at 325, 333, 362, 401, 442, 456, 485, 499, 530 and 577 (think-fwa9); 15 bounds `upper_bounds.json` states by deleting squares from the next count’s certificate, with no certificate file at their own count, 447 among them (D6, proposed on think-f2io); and 46 L-border, tiling or composite bounds of the index with no certificate file of their own (D2, think-f2io).

## Credit

Francisco Couzo, whose issue keeps every seed, construction and certificate credit in
the source’s manifest; the per-count JSON credits the seed to Mykhailo Polkovskyi.
The source discloses OpenAI Codex assistance with its checker.
Beyond the corpus the per-count JSON credits Couzo’s seeds at most counts, Evan Daniel’s
at 364 and his seed or construction at 403 and 444, Kevin Fang’s at 382, and Fang’s
rectangle and gluing with PingYou Ltd’s square input at 703, 757, 813 and 931, and names
no seed credit at 21 counts; those statements are the source’s, and per-row credit beyond the
horizon is the owner’s open question from #686.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-issue670-2026-10-17 --check
python -m devtools.upper_bound_reports couzo-issue670-2026-10-17 check-claims
python -m devtools.upper_bound_reports couzo-issue670-2026-10-17 certify --jobs-dir "$TMPDIR/jobs" --workers 1
python -m devtools.upper_bound_reports couzo-issue670-2026-10-17 check --replay
python -m devtools.upper_bound_reports couzo-issue670-2026-10-17 register-plan
python -m devtools.beyond_horizon_replay check --issue 670
python -m devtools.beyond_horizon_replay check --issue 670 --replay --workers 2
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
