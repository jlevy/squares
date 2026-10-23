# Francisco Couzo’s Registration Witnesses at 43ac7d2

[Issue #607](https://github.com/jlevy/squares/issues/607), filed 2026-10-14T23:18:36Z,
reports 23 exact rational packings from
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/43ac7d29cfeb7b71ea1eb09939cb30b9f71850f2/submissions/2026-10-14)
at `43ac7d29cfeb7b71ea1eb09939cb30b9f71850f2` (tree
`17312eac943e63fbf9abc196c81a3e9343c4a76f`, committed 2026-10-14T19:15:09Z, parent
`487b058`), the head of `master` when retrieved, under
`submissions/2026-10-14/certificates/`. The issue had no comments or edits when read, at
2026-10-14T23:30Z.

It asks for 21 finite upper bounds and lists two precision refinements apart from them:

- **Fourteen campaign improvements**, Couzo’s own: one inside the case corpus, at 237,
  where it continues Mykhailo Polkovskyi’s #593 certificate, and 13 beyond it.
- **Seven of Kevin Fang’s composites**, from the Section 5 table of
  [TheSnakeFang/squarepack-certs](https://github.com/TheSnakeFang/squarepack-certs/blob/078789a4cfd36f915f1bfbe76d742413d79b2965/composites/TABLE.md),
  which the author replayed in support of
  [#603](https://github.com/jlevy/squares/issues/603) and credits to Fang as their
  construction author.
- **Two precision refinements**, at 342 and 542, of the author’s own certificates.

| n | Exact side, rounded up at 16 places | The issue prints | Group |
| --- | --- | --- | --- |
| 237 | 15.9026036382835755 | 15.902603638284 | Campaign |
| 339 | 18.9158185554690925 | 18.915818555470 | Campaign |
| 342 | 18.9647067231724058 | 18.964706723173 | Precision refinement |
| 382 | 19.9876211542404763 | 19.987621154241 | Campaign |
| 409 | 20.7674283499656930 | 20.767428349966 | Campaign |
| 419 | 20.9599975820781481 | 20.959997582079 | Campaign |
| 450 | 21.7674283505864604 | 21.767428350587 | Campaign |
| 461 | 21.9731837533740979 | 21.973183753375 | Campaign |
| 542 | 23.8284271247738502 | 23.828427124774 | Precision refinement |
| 552 | 23.9680348455028245 | 23.968034845503 | Campaign |
| 599 | 24.9680348461267911 | 24.968034846127 | Campaign |
| 648 | 25.9680348463277911 | 25.968034846328 | Campaign |
| 649 | 25.9769740884020804 | 25.976974088403 | Campaign |
| 651 | 25.9845150682787440 | 25.984515068279 | Campaign |
| 703 | 26.9992563084462490 | 26.999256308447 | Fang composite |
| 757 | 27.9910008659939410 | 27.991000865994 | Campaign |
| 804 | 28.9203987475766181 | 28.920398747577 | Campaign |
| 812 | 28.9882872368506546 | 28.988287236851 | Fang composite |
| 930 | 30.9882872368506546 | 30.988287236851 | Fang composite |
| 931 | 30.9940486550319320 | 30.994048655032 | Fang composite |
| 992 | 31.9972203617828275 | 31.997220361783 | Fang composite |
| 993 | 31.9913278876915015 | 31.991327887692 | Fang composite |
| 994 | 31.9992563084462490 | 31.999256308447 | Fang composite |

Each certificate gives `n` unit squares, each a rational centre in $[0, S]^2$ and a
rational $t = \tan(\theta/2)$, in a square of the stated side, in Evan Daniel’s format.
Each exact side rounds up, at the 12 places the issue prints, to the side printed, and
[acquisition/claims.json](acquisition/claims.json) holds each exact side.
The submission’s `manifest.json` states each certificate’s full SHA-256 and exact side,
and its `SHA256SUMS` lists all 49 other files of the directory; both agree with the
bytes at the pin.

## What the Commit Changes

`43ac7d2` adds `submissions/2026-10-14/` (50 files) and nothing else.
Its parent, `487b058` (2026-10-14T17:45:39Z, “Land verified bounds through n=1024”),
holds the index `upper_bounds.json` whose values the issue prints as “previous verified
bound”; the index’s blob is the same at both commits.
Against the [issue-586 packet’s](../couzo-certificates-2026-10-13/README.md) pin
`b85dee2`, `487b058` adds 290 certificates under `certificates/`, at 370 and at 403 to
991, changes seven, at 211, 339 and 378 to 382, and deletes 22. No issue reports those
certificates, and this packet does not retain them.
At the 17 counts where `487b058` holds a certificate and the issue reports another (339,
342, 382, 409, 419, 450, 461, 542, 552, 599, 648, 649, 651, 757, 804, 812 and 930), the
comparison below reads the index’s side, rounded up at 12 places.
The header of each of those 17 files at `487b058` states exactly the index’s rational
bound. Its 342 is the certificate the
[issue-476 packet](../couzo-exact-certificates-2026-10-09/README.md) retains, unchanged
since `02f9690`; the other 16 were first committed in `487b058`.

## Retained Here

`devtools.acquire_source` wrote the packet from a blobless clone with a sparse checkout
at the pin, from the declaration in
[acquisition/declaration.json](acquisition/declaration.json); every file is bound to its
Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest:
the root `README.md`, `upper_bounds.json` and the 50 files of `submissions/2026-10-14/`,
52 files, 3,823,642 bytes.

The repository states no licence: its tree has no licence file, and neither `README.md`
nor `submissions/2026-10-14/README.md` states reuse terms.
The 23 certificates under `source/submissions/2026-10-14/certificates/` (3,048,022
bytes) are retained as factual data under the owner decision of 2026-10-09
([Retained Factual Data](../known-best-packings/README.md#retained-factual-data)); the
seven composites are also released under CC0 1.0 by the repository that first published
them. The two READMEs, `upper_bounds.json`, `manifest.json`, `SHA256SUMS`,
`verification-receipts.json` and the 23 checker logs under `verification/` are pinned by
digest only. No prose or program is copied.

## Kevin Fang’s Seven Composites

The seven composite certificates are Fang’s, byte for byte.
Each has the SHA-256 that `composites/table.csv` lists for its row, in the copy the
[excess-theorem packet](../fang-excess-theorem-2026-10-13/README.md) retains from
`078789a`, where the table is unchanged since it was first committed in `bef5c42`
(2026-10-12T19:13:41Z). Each row is Fang’s smallest at its count:

| n | Fang’s row | Status in his table | SHA-256, first 16 hex digits |
| --- | --- | --- | --- |
| 703 | `L1_n27_703_r17x16_n0257+n-110` | shipped as `composites/n027_j1_703.cert` | `0ba5cd285b5dd1a8` |
| 812 | `L1_n29_812_r21x20_n0401+n-71` | table only | `90b2464abbf3befd` |
| 930 | `L1_n31_930_r21x20_n0401+n-109` | table only | `a0ff666efa634762` |
| 931 | `L1_n31_931_r19x18_n0325+n-156` | table only | `503efbc15a94dc93` |
| 992 | `L1_n32_992_r22x21_n0442+n-109` | table only | `65c89b14a05e6be8` |
| 993 | `L1_n32_993_r21x20_n0401+n-132` | table only | `c30e494d7136f11a` |
| 994 | `L1_n32_994_r17x16_n0257+n-241` | shipped as `composites/n032_j2_994.cert` | `aef770c71d1d8884` |

At 703 and 994 the certificate is also the file Fang shipped, whose digest the
excess-theorem packet pins without retaining it.
The other five rows Fang lists but does not ship; the issue says the author regenerated
them with Fang’s retained `tools/glue.py`, and the bytes it publishes have the digests
Fang’s table names, so they are Fang’s certificates, not re-derived ones.
At 931 Fang also ships `composites/n031_j1_931.cert`, 30.9992563084462490, which this
table-only row is $5.21 \times 10^{-3}$ below.

Bead `think-rn2y` holds Fang’s composites: 81 counts from 420 to 4035, the smallest
report a shipped certificate at 28 counts and a table-only row at 53, with the replay of
the 38 shipped held at about 122 CPU-hours.
These seven cover two of the 28 shipped counts, 703 and 994, and five of the 53
table-only counts, 812, 930, 931, 992 and 993, and the replay below decides all seven.

## Exact Replay

Only the retained certificates enter geometry decisions.
They go through the maintained two-route kernel of `devtools.evand_arrangement_reports`,
which the earlier Couzo imports also used: `sqpack`’s exact witness verifier and the
independent rational corner checker, each deciding every wall and every pair over
$\mathbb{Q}$ after an exact half-angle conversion.
The replay covers all 23 certificates, the seven composites among them.
Each count runs a positive job, a duplicate-square control and an outside-container
control, each in its own child process.

All 23 positives pass both routes.
Both routes refuse all 46 controls, each on the overlap or the wall it was built to
break. In every positive the two routes find the same least wall clearance and the same
least pair gap:

- **The 16 campaign and precision certificates** clear every wall by exactly
  `1/1000000000000000` ($10^{-15}$) and every pair by between $9.76 \times 10^{-13}$ (at
  419\) and $1.60 \times 10^{-12}$ (at 339).
- **The seven composites** clear every wall by exactly `1/36893488147419103232`
  ($2^{-65}$, $2.71 \times 10^{-20}$) and every pair by exactly `1/18446744073709551616`
  ($2^{-64}$, $5.42 \times 10^{-20}$), the margins the author’s logs of Evan Daniel’s
  checker print.

The 69 jobs made 31,386,744 pair decisions in 12,425.76 route CPU seconds (3.45
CPU-hours) and 14,795.58 job wall seconds, summed; the longest job, the
outside-container control at 994, took 632.89 seconds.
The run used one worker on a machine shared with other import lanes, at a load average
between 2 and 11 on four cores.
Each job was decided by the same `decide-job` command `certify` runs, one at a time,
from 23:41Z on 14 October to 03:55Z on 15 October, by a runner that skips finished
outputs: the session’s two-hour limit on a background command stopped it once, during
the duplicate-square control at 812, and it was started again from there.
`certify --workers 1 --finished` then assembled and admitted the receipt from all 69 job
outputs, as it admits any; it is kept as one shard per count,
`receipts/exact-certification-nNNN.json.xz`, since the whole would exceed the kernel’s
ceiling on uncompressed evidence, and each keeps every deciding input and both routes’
complete outputs.
A fresh serial `check --replay` decided all 69 jobs again, equal to the
retained rows apart from timing, in four runs over the counts (`--n` 237 to 651, then
703 to 812, 930 to 992, and 993 and 994) from 04:04Z to 08:09Z on 15 October, each
within the two-hour limit: 4 hours 4 minutes of wall and 3 hours 39 minutes of CPU in
all.

The two routes share certificate parsing, the half-angle conversion, Python’s rational
arithmetic and the separating-axis method, so they are two implementations of one
method. The third exact route, `devtools.check_half_angle_area`, is a separate review
lane and did not run here.
No source program ran here.

## Against the Record

[acquisition/claims.json](acquisition/claims.json) freezes every certificate against the
record as `main` stood at `22a67ce4a`, after #614 adopted T-183 as the house at 237; the
frozen record first read `9b32da04d`, when the issue arrived, then `6964362b5` and
`c4c690a3e` (after #612 registered T-185 to T-187), and every relation is the same at
all four.
That lane added T-056’s printed side at 237, which the declaration had left out (above
by $8.59 \times 10^{-3}$), and labels the reports without commit ids: `487b058`’s
certificates by the source row that records them, `couzo-verified-bounds-2026-10-14`, and
Fang’s by their table rows and file names.
`check-claims` rebuilds it, each exact side from its holder’s own retained packet.

**At 237**, inside the corpus, the case ceiling is Nate Chaoweeraprasit’s packing as
improved by Couzo and by Mykhailo Polkovskyi, his #593 certificate (T-183),
15.9027050578663668, and the certificate is below it by $1.01 \times 10^{-4}$. Every
other register entry and open report at 237 is above it: Couzo’s #561 (T-161) and
PingYou Ltd’s PR #574 (T-174) by $3.44 \times 10^{-4}$; Couzo’s #488 (T-140, the house
until #614) and Polkovskyi’s #573 by $3.46 \times 10^{-4}$; and T-098, T-115, T-127,
T-134, T-136, Robert Barnett’s #505 and Polkovskyi’s #470 by $3.86 \times 10^{-4}$ or
more.
[review/compare_lineage-output.txt](review/compare_lineage-output.txt) measures it
against #593’s and #488’s packings with
`mishapolk-kkt-refinements-2026-10-14/review/compare_lineage.py`: under a reflection of
the box, 195 of its 237 squares are within $10^{-3}$ of #593’s and all within 0.034, and
T-189 lists it as a regularization of T-183.
Mishapolk’s `70a033f`, read by another lane the same evening, holds no 237.

**Beyond the corpus** there is no case record.
Each side is compared with the grid, with the row the source register tracks as current
at its count, and with every other report there.
Fang’s composite rows are read at the 15 places, rounded up, his table prints, and the
theorem certificates of his `078789a` at their exact sides $n - 1/20000$.

| n | Current row on `main` | Below it by | Other reports | Smallest |
| --- | --- | --- | --- | --- |
| 339 | Couzo’s #586, 18.925319360704 | $9.50 \times 10^{-3}$ | Couzo’s `487b058`, above by $2.29 \times 10^{-4}$; Evan Daniel’s #584, above by $1.11 \times 10^{-2}$; #583, #506 and #476, above by $1.16 \times 10^{-2}$ or more | this certificate |
| 342 | Couzo’s 8 October report, 18.964706723440020 | $2.68 \times 10^{-10}$ | #476, the same certificate as `487b058`’s, above by $2.86 \times 10^{-10}$; Fang’s composite, above by $3.28 \times 10^{-2}$ | this certificate |
| 382 | Couzo’s #586, 19.987713157610 | $9.20 \times 10^{-5}$ | `487b058`, above by $1.34 \times 10^{-7}$; #583, above by $9.79 \times 10^{-4}$; Fang’s direct `c284cd0`, above by $1.86 \times 10^{-3}$; Fang’s theorem certificate, above by $1.23 \times 10^{-2}$ | this certificate |
| 409 | none: the grid, 21 | $2.33 \times 10^{-1}$ | `487b058`, above by $5.07 \times 10^{-5}$ | this certificate |
| 419 | none: the grid, 21 | $4.00 \times 10^{-2}$ | `487b058`, above by $1.50 \times 10^{-3}$ | this certificate |
| 450 | none: the grid, 22 | $2.33 \times 10^{-1}$ | `487b058`, above by $5.07 \times 10^{-5}$ | this certificate |
| 461 | none: the grid, 22 | $2.68 \times 10^{-2}$ | `487b058`, above by $1.29 \times 10^{-3}$ | this certificate |
| 542 | none: the grid, 24 | $1.72 \times 10^{-1}$ | `487b058`, above by $1.02 \times 10^{-9}$ | this certificate |
| 552 | none: the grid, 24 | $3.20 \times 10^{-2}$ | `487b058`, above by $5.73 \times 10^{-3}$; Fang’s composite, above by $2.03 \times 10^{-2}$ | this certificate |
| 599 | none: the grid, 25 | $3.20 \times 10^{-2}$ | `487b058`, above by $5.55 \times 10^{-3}$ | this certificate |
| 648 | none: the grid, 26 | $3.20 \times 10^{-2}$ | `487b058`, above by $5.55 \times 10^{-3}$ | this certificate |
| 649 | none: the grid, 26 | $2.30 \times 10^{-2}$ | `487b058`, above by $8.12 \times 10^{-4}$ | this certificate |
| 651 | Fang’s direct `e646c47`, 25.991547815274380 | $7.03 \times 10^{-3}$ | `487b058`, above by $3.79 \times 10^{-4}$; Fang’s theorem certificate, above by $1.54 \times 10^{-2}$ | this certificate |
| 757 | none: the grid, 28 | $9.00 \times 10^{-3}$ | `487b058`, above by $1.47 \times 10^{-3}$; Fang’s composites, above by $6.55 \times 10^{-3}$ (table only) and $8.26 \times 10^{-3}$ (shipped); Fang’s theorem certificate, above by $8.95 \times 10^{-3}$ | this certificate |
| 804 | none: the grid, 29 | $7.96 \times 10^{-2}$ | `487b058`, above by $6.78 \times 10^{-3}$ | this certificate |
| 703 | none: the grid, 27 | $7.44 \times 10^{-4}$ | Fang’s composite, the same file; Fang’s theorem certificate, above by $6.94 \times 10^{-4}$ | Fang’s composite |
| 812 | none: the grid, 29 | $1.17 \times 10^{-2}$ | Fang’s composite, the same file; `487b058`, above by $4.18 \times 10^{-3}$ | Fang’s composite |
| 930 | none: the grid, 31 | $1.17 \times 10^{-2}$ | Fang’s composite, the same file; `487b058`, above by $1.28 \times 10^{-3}$ | Fang’s composite |
| 931 | none: the grid, 31 | $5.95 \times 10^{-3}$ | Fang’s table-only composite, the same file; his shipped one, above by $5.21 \times 10^{-3}$ | Fang’s composite |
| 992 | none: the grid, 32 | $2.78 \times 10^{-3}$ | Fang’s composite, the same file | Fang’s composite |
| 993 | none: the grid, 32 | $8.67 \times 10^{-3}$ | Fang’s composite, the same file | Fang’s composite |
| 994 | none: the grid, 32 | $7.44 \times 10^{-4}$ | Fang’s composite, the same file; Fang’s theorem certificate, above by $6.94 \times 10^{-4}$ | Fang’s composite |

At the seven composite counts the claim record leaves the certificate and Fang’s row
undecided, since his table prints 15 places and the two sides differ by less than one
unit there; the digests decide it, as the certificate is the file his row names.
The declaration’s `requested` roster is the 16 counts the per-count rule records as the
author’s: the seven composites stay in the claim record as replayed certificates, and
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json) holds
the 15 recorded counts beyond 324, each a row of the source register.

## In Report Order

#607 reports the 23 certificates, filed at 2026-10-14T23:18:36Z; the issue is what
times a claim ([stage 1](../../../campaign/result-import.md#several-reports-at-one-count)).
They were first committed at `43ac7d2`, 19:15:09Z the same day, in a watched repository.
No report at any of the 16 counts it records falls between the two times (`487b058`, at 17:45:39Z,
precedes both, and `4e4c8ce`, at 00:31:53Z the next day, follows both), so the order is
the same either way; which time a certificate committed before its issue takes is the
owner’s question.
Under the owner’s rule of 14 October, a report is recorded at a count only where it is
below every report that reached the record before it:

- **Recorded, 16 counts.** At 237 the certificate is below T-140, T-183 and every
  earlier report; the issue calls it a refinement of Polkovskyi’s #593 certificate, so
  it is credited to Couzo after Polkovskyi’s packing.
  At 339, 342, 382, 409, 419, 450, 461, 542, 552, 599, 648, 649, 651, 757 and 804 it is
  below every earlier report, among them Couzo’s own `487b058`, 90 minutes earlier, and
  at 339, 342 and 382 the source register’s current rows.
  At 342 and 542 it refines the author’s own packing.
- **Not recorded, 7 counts.** At 703, 812, 930, 931, 992, 993 and 994 the certificate is
  Fang’s composite, published at `bef5c42` two days earlier: the same file, so a tie,
  and the earlier holder keeps it.
  The issue asks for exactly that credit.
  These certificates and their replay here are evidence for Fang’s rows, which
  `think-rn2y` registers.

`487b058`’s own certificates are reports at their first commit, before this one, and an
import of their own (T-188’s source).
At 14 of the 15 recorded counts beyond 324 its row is recorded and then superseded by
this packet’s; at 812 and 930 it is above Fang’s composites and not recorded.

The records lane of 15 October registered the 237 side as T-189 and the 15 rows, each
superseding the row it beats: `487b058`’s at 14 counts and Couzo’s 8 October report at
342. Couzo’s later `4e4c8ce` certificate at 237 is T-190.
The `4e4c8ce` index, not yet recorded (think-yfoo), is smaller in turn at 7 of the 15
rows, at 339, 382, 450, 552, 599, 648 and 757, by $2.88 \times 10^{-11}$ to
$1.13 \times 10^{-3}$ (its exact sides are in
[couzo-verified-bounds-2026-10-14’s review/goebel-beyond-horizon.json](../couzo-verified-bounds-2026-10-14/review/goebel-beyond-horizon.json)).
The [history walk of Couzo’s watched publications](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md)
records it (couzo-index-2026-10-15), and those 7 rows name it as their successor; the row
at 409 names Couzo’s `5a299b4` of 20 October, public on 21 October
(couzo-reconcile-2026-10-20).

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
The issue says every certificate passes this repository’s `sqpack.verify` at `37e6757`
and Evan Daniel’s `verify_cert.py` at `622cd2e`, and the 16 campaign and precision
certificates the campaign’s Rust rational checker; those runs are the author’s, and no
program of the source ran here.
Novelty, local or global optimality and rigidity are not established, and the replay of
seven composites says nothing of Fang’s other composites or his theorem.

## Credit and Licence

Francisco Couzo wrote the source, which states no licence; the certificates are kept as
factual data and nothing of the source is relicensed.
The issue asks that the constructions each continues be credited.
At 237 it is Mykhailo Polkovskyi’s #593 certificate, whose construction credit the
author asks to keep.
339 continues the author’s L-border construction of #506, refined in #583 and #586; Evan
Daniel’s 339 is a comparison, not its seed.
382 and 651 continue Kevin Fang’s published arrangements, and the 649 search descends
from 651 by elimination.
409 and 450 continue the L-border lineage, whose 409 start includes Evan Daniel’s 298;
450 adds one L-border layer to the new 409. 419, 461 and 804 continue campaign
refinements and L-border or elimination constructions, from starts that include the
project’s refinements of Fang’s 380 and 381. 552, 599 and 648 continue the campaign’s
552, the latter two with one and two L-border layers, and 757 a seed obtained by
elimination from 758. The seven composites are Kevin Fang’s, using the input
certificates and gluing named in his table; the author regenerated five and replayed all
seven, and claims no construction credit.
Fang’s repository credits Evan Daniel with the input pieces and the checker, and Couzo
with the 342 seed of the 21 × 20 and 22 × 21 rectangles.
The browser submissions carry the public credit `franciscouzo`; Evan Daniel’s optimizer
and verifier, David Ellsworth’s refinement ideas and this repository’s exact verifier
were used. The issue states that OpenAI Codex was used for search and verification
orchestration, source review, certificate packaging and the issue, that earlier search
work used Claude Code, and that the author directed the work.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source couzo-certificates-2026-10-14 --check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-14 check-claims
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-14 check
uv run --frozen --all-extras --group dev python -m devtools.upper_bound_reports couzo-certificates-2026-10-14 check --replay
uv run --frozen --all-extras --group dev python resources/web/mishapolk-kkt-refinements-2026-10-14/review/compare_lineage.py couzo-certificates-2026-10-14 237 mishapolk-records-2026-10-14 couzo-certificates-2026-10-10
```

`check` admits the receipt structurally against the retained certificates; only
`--replay` decides the geometry again.
`certify --jobs-dir SCRATCH --workers 1` writes a new receipt from a fresh job
directory, and `register-plan` prints the record entries the import needs.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
