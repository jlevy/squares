# Joost de Winter’s Packings beyond 324 (Issue #666)

Joost de Winter’s [issue #666](https://github.com/jlevy/squares/issues/666), opened
2026-10-17T07:06:07Z, reports nineteen packings of n unit squares beyond the n ≤ 324 case
corpus, each the exact rational side of a certificate rounded up at 12 places: 464, and
from 509 to 1568 one count below each integer side ⌈√n⌉ that the record held there.
This packet retains all nineteen certificates. The 11 at or below 1024 are recorded as
dated beyond-horizon rows of the `de-winter-issue666-2026-10-17` source; the 8 above
1024 wait on the owner’s decision whether the record tracks counts that high
(think-f2io), and are retained here only because the issue’s pin is on no branch.

## Source and Dates

| Field | Value |
| --- | --- |
| Repository | [JoostdeWinter/joostdewinter.github.io](https://github.com/JoostdeWinter/joostdewinter.github.io), folder `square-packing-above-324/` |
| Issue pin | `b3152f526f23bc3ae450e51b6e906841233086d1`, committed 2026-10-17T07:03:15Z; on no branch since the site’s history was rewritten to drop an unrelated PDF |
| Reachable equivalent | `b9cdc16bc20fedfbd4f5aa142dd7039b22f757f2`, the same time and message; its folder tree `83563a8b35cb65bcf034f7fdd6d4483dcca05841` is the pin’s |
| Retained revision | `643dc9ad4d3dbd71a9a05558c7f6116b809ba930`, committed 2026-10-17T14:27:33Z: adds the folder’s MIT `LICENSE` and a README paragraph releasing every file under it, and changes none of the 41 certificate, pose and checker blobs |
| Head on 22 October | `206c7fc63b9105cf9b4009d8c6ea3fa160c495ad`, which adds an unrelated paper only ([intake-watch.yaml](../../../campaign/intake-watch.yaml)) |
| Licence | MIT, copyright 2026 Joost de Winter ([LICENSE](source/square-packing-above-324/LICENSE)) |
| Custody | [declaration](acquisition/declaration.json), [acquisition record](acquisition/sources.json), [manifest](acquisition/upstream-subtree.sha256), [the issue as read](acquisition/issue.json) |

[receipts/first-commits.json](receipts/first-commits.json) reads the retained commit’s
history from a blobless clone and finds each certificate’s blob first at `b9cdc16b`,
three minutes before the issue: every row reached this repository through the issue.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of
`square-packing-above-324/` at `643dc9a`; every file is bound to its Git blob there.
Retained, under the MIT licence: the 19 certificates `nNNNN.cert`, the exact checker
`check.py` (read, not run), `records.txt`, the folder’s `README.md` and `LICENSE`,
23 files, 6,564,793 bytes (1.37 MB as Git’s zlib stores the
certificates). Pinned by digest only: the 19 decimal-pose files `nNNNN.json` and the
10.6 MB figure `before_after.svg`; no claim rests on either.

Each certificate is `n S`, one comment line, then n rows `x y t`, a rational centre and
$t = \tan(\theta/2)$, in Evan Daniel’s certificate format; the header side is
authoritative. The sides carry large rationals (numerators of up to 110 digits).

| n | Issue’s print, rounded up | Record the issue names | Disposition |
| --- | --- | --- | --- |
| 464 | 21.988813022694 | 21.989992144499 (Couzo) | recorded; superseded on entry by Couzo’s #675 |
| 509 | 22.994328036438 | 23 | recorded; superseded on entry by Couzo’s #715 |
| 555 | 23.993653790591 | 24 | recorded; superseded on entry by Couzo’s #678 |
| 603 | 24.995268064197 | 25 | recorded; superseded on entry by Couzo’s #675 |
| 654 | 25.996103908965 | 26 | recorded; superseded on entry by Couzo’s #675 |
| 706 | 26.998712100405 | 27 | recorded; superseded on entry by Couzo’s #675 |
| 760 | 27.995949340329 | 28 | recorded; superseded on entry by Couzo’s #675 |
| 817 | 28.998488480775 | 29 | recorded; superseded on entry by Couzo’s #672 |
| 875 | 29.998783733108 | 30 | recorded; superseded on entry by Muglich’s #686 |
| 935 | 30.995955854834 | 31 | recorded; superseded on entry by Couzo’s #672 |
| 998 | 31.998349747355 | 32 | recorded; superseded on entry by Couzo’s #675 |
| 1061 | 32.996048342114 | 33 | retained; waits on the owner (think-f2io) |
| 1128 | 33.998294117981 | 34 | retained; waits on the owner (think-f2io) |
| 1196 | 34.998294118334 | 35 | retained; waits on the owner (think-f2io) |
| 1266 | 35.996046404219 | 36 | retained; waits on the owner (think-f2io) |
| 1339 | 36.997865207179 | 37 | retained; waits on the owner (think-f2io) |
| 1413 | 37.999463832123 | 38 | retained; waits on the owner (think-f2io) |
| 1489 | 38.997600184483 | 39 | retained; waits on the owner (think-f2io) |
| 1568 | 39.999336626159 | 40 | retained; waits on the owner (think-f2io) |

## Exact Replay

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) reads every
certificate a decided row names from this packet once `acquire_source --check` holds it,
and decides it with the filtered two-route decision and the six controls of
[`devtools.couzo_678_replay`](../../../devtools/couzo_678_replay.py), reused unchanged:
route `sqpack` through `sqpack.witness` and `sqpack.verify`’s exact predicates, route
`independent` through `devtools.check_rational_witness_independent`’s, over every corner
against every wall and every pair whose centres are closer than √2 by exact comparison.
A unit square’s interior lies in the open disc of radius √2/2 about its centre, so no
other pair can overlap; both routes check that every square is a unit square whose corner
mean is that centre, which the lemma needs. The
[18 October packet](../couzo-issue678-2026-10-18/README.md#exact-replay) states the six
controls.

**All 11 are verified.** Every printed side is its header side rounded up at 12 places,
and both routes accept every packing: 18,530 candidate pairs of 2,972,615, and every
corner against every wall. No square touches the box or another: the least wall clearance
is between 1.0e-35 and 2.8e-09 and the least pair gap between 1.0e-35 (at 509) and
2.2e-11, the range the issue states. **All 66 controls are refused by both routes**, the
near-contact pair `10^-30` of its centre distance past contact among them. The positive
decisions took 57.1 CPU seconds, about four times Couzo’s per pair since the rationals are
long; with the controls the rows took 496 seconds of wall, summed, on two workers at
`nice`. [receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json) keeps
every row’s side, both routes’ counts, least clearance, least gap and failures, and the
controls.

**The all-pairs kernel**, `devtools.evand_arrangement_reports`’s two routes with no
filter, decided every pair at 464: 107,416 pairs in 215.7 CPU seconds. Both routes accept
it, and their least pair gap and wall clearance equal the filtered decision’s exactly.
Receipt: [receipts/exhaustive-sample.json](receipts/exhaustive-sample.json). At that rate,
about 2 milliseconds a pair for both routes, the all-pairs positives of the 11 would take
about 1.7 CPU-hours; they are not run here, and the filtered route is the replay of
record, as for #678 and #715.

**Göbel’s classical constructions.** Every side is below Göbel’s side at its count
(squares, strips and corner-touching strips, with deletion), by 0.143 at 875 or more,
decided exactly by the 15 October packet’s retained
[goebel_beyond_horizon.py](../couzo-verified-bounds-2026-10-14/review/goebel_beyond_horizon.py).
Receipt: [receipts/goebel-comparison.json](receipts/goebel-comparison.json).

## Against the Record, in Report Order

The [backlog ledger of 22 October](../../../campaign/issue-intake/upper-bounds-backlog-20261022/README.md)
walks every report at each count these rows claim, from starts frozen at the 18 October
ledger’s `main` (`804eff369`), through issues #666, #670, #672, #675, #678 and #686 and
Couzo’s #715. Each of the 11 is recorded: at 464 below Francisco Couzo’s certificate of
14 October, elsewhere below the grid. Each is superseded on entry by a later report at
its count, which the source register names as the row’s successor: Couzo’s #675 at six
counts, his #672 at two, and his #678, Darius Muglich’s #686 and Couzo’s #715 at one each.

## Above 1024

The rows at 1061, 1128, 1196, 1266, 1339, 1413, 1489 and 1568 are retained and not
replayed or recorded. Whether the record tracks counts above 1024 (D1, think-f2io) is the
owner’s decision, and Couzo’s #715 raises it too; at six of these counts #715 reports a
smaller side, and at 1128 and 1196 de Winter’s are the only reports. The certificates are
retained now because the issue’s pin is on no branch.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
Novelty, local or global optimality and rigidity are not decided. The issue says its
`check.py` accepts all nineteen and that the printed poses pass at 80 digits, with least
clearances between 10⁻³⁵ and 2 × 10⁻¹¹; those runs are the author’s, and `check.py`, which
pre-filters pairs in binary floating point, was not run here. The filtered route is a
first-party program; its two routes share the certificate parser, the half-angle
conversion, the pair filter and Python’s rational arithmetic, so it is two
implementations of the unit-shape, pair and wall predicates, not two independent replays.
No stage 4 review is owed for a beyond-horizon row, and none is recorded.

## Credit and Licence

Joost de Winter wrote the source and released the folder under the MIT licence. The issue
credits the staircase-rectangle and four-block method of Arslanov, Mustafin and
Shangitbayev (Electronic Journal of Combinatorics 28(4), P4.22, 2021) and, at 464, a
six-square patch from his own n = 422 construction. It discloses GPT-6 Astra for the
numerical search and refinement and Claude (Anthropic) for the certificates and checks,
under his direction.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source de-winter-issue666-2026-10-17 --check
uv run --frozen --all-extras --group dev python -m devtools.beyond_horizon_replay check --issue 666
uv run --frozen --all-extras --group dev python -m devtools.beyond_horizon_replay check --issue 666 --replay
uv run --frozen --all-extras --group dev python -m devtools.beyond_horizon_replay filtered --issue 666 --workers 2
uv run --frozen --all-extras --group dev python -m devtools.beyond_horizon_replay first-commits --issue 666 --clone CLONE
uv run --frozen --all-extras --group dev python -m devtools.beyond_horizon_replay exhaustive --issue 666 --n 464
uv run --frozen --all-extras --group dev python -m devtools.beyond_horizon_replay goebel
uv run --frozen --all-extras --group dev python -m devtools.beyond_horizon_replay claims-record
```

`check` reads the receipts and the beyond-horizon record against the issue and the
packet, and the source register’s rows against the ledger; `check --replay` decides every
row and control again. `first-commits` needs a clone of the site’s history (blobless is
enough).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
