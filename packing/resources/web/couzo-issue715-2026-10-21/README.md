# Francisco Couzo’s Upper Bounds at 6b7391de (Issue #715)

[Issue #715](https://github.com/jlevy/squares/issues/715), filed 2026-10-21T20:55:57Z as
a follow-up to [#678](https://github.com/jlevy/squares/issues/678), reports 1285 upper
bounds for n = 328 to 9913 from
[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/6b7391de820fd01f3ff6984e4a081e8c86845588)
at `6b7391de820fd01f3ff6984e4a081e8c86845588`: 173 at or below 1024 and 1112 above.
This packet decides the 173 at or below 1024. It retains the 139 certificates that reached
this repository first through the issue, records their exact replay, and compares every
claim with the record and the earlier reports in report order.
All 173 counts lie beyond the n ≤ 324 case corpus, so the issue takes no register entry.
The 109 that are the issue’s own new reports are dated beyond-horizon rows of the
`couzo-issue715-2026-10-21` source in
[source-coverage.yaml](../../../frontier/source-coverage.yaml), read from
[acquisition/beyond-horizon-claims.json](acquisition/beyond-horizon-claims.json).
The 1112 rows above 1024 are not recorded: whether the record tracks counts above 1024,
and rows the source states only as constructions, waits on the owner (think-f2io).

## Source and Dates

| Field | Value |
| --- | --- |
| Source | [franciscouzo/square-packing](https://github.com/franciscouzo/square-packing) |
| Pin | `6b7391de820fd01f3ff6984e4a081e8c86845588`, tree `1716ce7919230164598ee4c7e9465d3f02f77698`, the head of `master` when retrieved |
| Committed | 2026-10-21T20:48:49Z, “Land verified packing improvements and retain only strict record claims” |
| Parents | `5a299b4` (2026-10-20T22:35:41Z), then `d09edd7` (2026-10-19T14:33:31Z), whose parent is `7b6c87e`, the pin of #678 |
| Published | 2026-10-21T22:56:37Z, when the three commits were pushed together (the repository’s `pushed_at`); `master` had stood at `7b6c87e` since GitHub recorded that push at 2026-10-18T23:23:42Z |
| Issue filed | 2026-10-21T20:55:57Z, seven minutes after the commit and two hours before it was public |
| Retrieved | 2026-10-22T00:13Z, a blobless clone of the full history and a checkout at the pin |
| Licence | none for the data or prose; the checker is MIT-licensed (below) |
| Custody | [declaration](acquisition/declaration.json), [acquisition record](acquisition/sources.json), [manifest](acquisition/upstream-subtree.sha256), [the issue as read](acquisition/issue.json) |

The issue had no comment when this packet was written, at 01:00Z on 22 October.
Couzo said on [#678](https://github.com/jlevy/squares/issues/678) at 23:26Z on 21
October that `6b7391de` does not carry the source correction #678 asked for; that ask
stays with #678.

## Which Counts Are New

Every certificate reachable from `7b6c87e` was public before the issue, and every other
one reached this repository first through it. At each of the 173 counts at or below 1024
the pin holds an explicit certificate, `certificates/nN.cert`, of n squares whose header
side is the claim’s exact side: the issue’s print is that side rounded up at 12 places,
and it equals the bound the source’s index, `certified_bounds.json`, states.
`devtools.couzo_715_replay publications` read the source’s history and held each pin
certificate to every certificate file of the same count in every commit reachable from
`7b6c87e` (1,567 distinct files, under any directory and name) and to the bound the
public index at `7b6c87e` states there, exactly
([receipts/earlier-publications.json](receipts/earlier-publications.json)).
Each count falls in one of three sets:

- **109 recorded.** The certificate was first committed at `5a299b4` (19) or the pin
  (90), and its side is below every earlier public side by at least 2.90e-07 (at 931,
  against a `c6da0fc` certificate), so the print alone decides it. These are the issue’s
  own reports.
- **30 held.** The certificate was first committed at `5a299b4`, and its side is below
  the `4e4c8ce` certificate of the same count, published on 15 October, by 2.37e-23 to
  3.18e-23: both round up to the issue’s print. Each is one of the index’s L-border
  constructions, written out in full. Whether such a re-certification of the author’s
  own earlier publication is a
  new report depends on reading below the print, and it is left to a decision
  (think-fwa9); nothing is recorded for these counts.
- **34 restated.** The side equals that of a certificate first published at `02f9690`
  (6), `a7067d7` (1), `f311f08` (1) or `4e4c8ce` (26, two of them the index’s deletion
  bounds), 32 of them byte for byte. Each is an earlier report, owned by its own import,
  and the issue restates it.

The triage of 21 October read the 64 restated and held counts as one set of byte-for-byte
earlier certificates, from `7b6c87e`’s files; at the pin, 30 of those files were
replaced by the re-certifications above.

## Retained Here

`devtools.acquire_source` wrote the packet from the declaration; every file is bound to
its Git blob at the pin. The scope is 359 files, 52,289,925 bytes:

- **retained**, 139 files, 13,737,718 bytes: the explicit certificates of the 109 recorded
  counts (10,857,469 bytes) and the 30 held counts (2,880,249 bytes), under
  [source/certificates/](source/certificates/);
- **pinned by digest only**, 220 files: the 34 restated certificates, eight of them
  against the identical copies the
  [9 October](../couzo-exact-certificates-2026-10-09/README.md),
  [11 October](../couzo-certificates-2026-10-11/README.md) and
  [12 October](../couzo-certificates-2026-10-12/README.md) packets retain; the credit
  record `certificates/nN.json` of each of the 173 counts; the four indexes the issue
  links (`upper_bounds.json`, `certified_bounds.json`, `certificates/best/manifest.json`
  and `public_bounds.json`); the provenance review and `record_provenance.json`; the three
  READMEs and `certificates/best/SHA256SUMS`; the construction checker
  `certificate_constructions.py`; and the source’s exact checker
  `verify_bound_certificate.py` with its licence, both byte-identical to the
  [18 October packet](../couzo-issue678-2026-10-18/README.md)’s retained copies and pinned
  against them.

The 13.7 MB of certificates are 4.42 MB as zlib stores them, which is how
[OR-18](../../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)
counts them, so they are kept in Git as #678’s 2.86 MB were.
The 857 witnesses under `certificates/best/`, `certificates/parents/`,
`certificates/extended/`, the drawings, the search programs and the Rust and CUDA sources
are pinned by the commit alone; none was retained or run.

The repository states no licence for its data or prose. The certificates are retained as
factual data under the owner decision of 2026-10-09
([Retained Factual Data](../known-best-packings/README.md#retained-factual-data)).
`verify_bound_certificate.py` names itself Evan Daniel’s MIT-licensed verifier with
modifications by Francisco Couzo with Codex, under the MIT licence in
`BOUND_VERIFIER_LICENSE.txt` (Copyright (c) 2026 Evan Daniel).

## The Claims

A certificate is `n S` and then `n` rows `x y t`: a unit square’s centre and
`t = tan(theta/2)`. The issue prints each side rounded up at 12 places and makes the
header authoritative.
The source’s index calls 59 of the 139 retained counts L-border constructions of another
count’s certificate (four of them less a square or two) and 9 deletions; the explicit
file writes each out in full. With the pinned checkout, the replay read each count’s
index entry and parent certificate, held each to its digest, and found every file to be
what the index says: an L-border file is its parent’s poses followed by axis-aligned unit
squares (`t = 0`) at the parent’s side plus the layers, and a deletion file is its
parent’s first n poses at the parent’s side. The replay decides the files themselves, so
nothing rests on the construction lemmas.

## Exact Replay

[`devtools.couzo_715_replay`](../../../devtools/couzo_715_replay.py) reads every
retained certificate from this packet once `acquire_source --check` holds it, and decides
each with the filtered two-route decision and the six controls of
[`devtools.couzo_678_replay`](../../../devtools/couzo_678_replay.py), reused unchanged:
route `sqpack` through `sqpack.witness` and `sqpack.verify`’s exact predicates, route
`independent` through `devtools.check_rational_witness_independent`’s, over every corner
against every wall and every pair whose centres are closer than √2 by exact comparison.
A unit square’s interior lies in the open disc of radius √2/2 about its centre, so no
other pair can overlap; both routes check that every square is a unit square whose corner
mean is that centre, which the lemma needs. The
[18 October packet](../couzo-issue678-2026-10-18/README.md#exact-replay) states the six
controls, and the
[review of 20 October 2026](../../../../docs/project/reviews/review-2026-10-20-upper-bound-imports-678.md)
accepted the route as a complete replay for #678.

### Results

**All 139 certificates are verified.** Every printed side is its header side rounded up at
12 places, and both routes accept every packing: 227,018 candidate pairs of 38,193,642,
and every corner against every wall.

- **The 109 recorded.** The least wall clearance is exactly 0 at 77 and `10^-15` at 32.
  The least pair gap is exactly 0 at the 29 L-border constructions, 2,785 touching pairs
  in all, and elsewhere between 3.55e-13 (at 554) and 3.98e-10.
- **The 30 held.** Every one touches a wall and has touching pairs, 5,066 in all, as an
  exact L-border does.

**All 834 controls are refused by both routes**, each on the overlap, wall or shape it
was built to break. The positive decisions took 115.8 CPU seconds; with the controls, two
workers took 570.0 seconds of wall from 00:40:42Z on 22 October, 1,134 seconds summed
over the rows, at `nice` on a four-core machine shared with another lane.
[receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json) keeps every
row’s side, both routes’ counts, least clearance, least gap and failures, the controls,
and, from the pinned index and manifest, each row’s index entry, its parent relation and
the manifest’s credits.

**The all-pairs kernel**, `devtools.evand_arrangement_reports`’s two routes with no
filter, decided every pair at 343 and 996: 554,163 pairs in 96.2 CPU seconds. Both
routes accept both, and their least pair gaps and wall clearances equal the filtered
decision’s exactly. Receipt: [receipts/exhaustive-sample.json](receipts/exhaustive-sample.json).
At that rate, about 0.17 milliseconds a pair for both routes, the all-pairs positives of
all 139 certificates would be about 1.8 CPU-hours; it is not run here.

**Göbel’s classical constructions.** Every replayed side is below Göbel’s side at its
count (squares, strips and corner-touching strips, with deletion), by 2.17e-02 at 860 or
more, decided exactly by the 15 October packet’s
[goebel_beyond_horizon.py](../couzo-verified-bounds-2026-10-14/review/goebel_beyond_horizon.py),
read from its retained path. Receipt:
[receipts/goebel-comparison.json](receipts/goebel-comparison.json).

**The source’s own checker** was not run here: the two maintained routes decide every
packing in full, and the checker is the same file #678’s packet ran on 85 rows.

## Against the Record, in Report Order

The [22 October ledger](../../../campaign/issue-intake/upper-bounds-20261022/README.md)
walks every report at the 173 counts in report order. Its start is the record on `main`
at `d588ad987bd8de53361d087b8961a7f2bf157c41`, the 20 October ledger’s read and the last
`main` before #678’s rows; every row `main` has gained at these counts since is #678’s,
#686’s or #702’s, and each is walked as a report. It walks the publications at
`02f9690`, `f311f08` and `4e4c8ce` at the counts the issue restates or re-certifies,
issues #666, #670, #672 and #675, not yet recorded, then #678, #686, #702 and #715, with
exact sides where a certificate gives one.

**Each of the 109 is recorded**: below every number the standing side and every earlier
report at its count may be. Each supersedes the row that stood at its count: 50 of
Darius Muglich’s #686 rows, by 3.85e-09 (at 496) to 7.45e-03, 29 of Couzo’s
`487b058` rows, 26 of #678’s and #702’s at 343; 509, 860 and 931 held no row.
**At 343** the reports arrived #678, #702, #715, each below the one before: #715’s side,
`3993049794861220561760624561/210408851936750000000000000`, is 1.0736e-04 below Evan
Daniel’s #702 side. The manifest credits that packing to Daniel, with Kevin Fang’s
two-wedge design, before Couzo’s refinement.
**At the 64 other counts** the ledger records the earlier publications and not the issue:
at the 34 restated counts #715 ties them (at 338 the start is the identical certificate,
which the ledger reads only by its print and so leaves undecided), at 335 both are
1.78e-11 or more above the 8 October decimal report the record holds, and at the 30 held
counts the issue’s print cannot be ordered against the `4e4c8ce` certificate, so the
ledger leaves them undecided and names what would decide them.
The ledger orders reports and verifies no certificate; recording is stage 3’s.

Since 22 October the
[backlog ledger](../../../campaign/issue-intake/upper-bounds-backlog-20261022/README.md)
has recorded the rows of #666, #670, #672 and #675, which come before #715 in report
order. At ten counts one of them is the row this packet’s row now supersedes: de Winter’s
#666 row at 509, #670’s at 866 and 925, #672’s at 750, and #675’s at 547, 807, 809, 864,
923 and 931. At eight of those (547, 750, 807, 809, 864, 866, 923 and 925) the `487b058`
row the table names now names the backlog report that beat it first, so each count is one
chain in report order and 21 of the 29 still name #715. Only 860 still holds this
packet’s row alone.
The table below keeps the rows that stood on `main` when this packet was written.

### The 109 Recorded Rows

Each row’s print, its exact side rounded up at 16 places, what the index calls it (`own`,
an L-border of a parent, or a deletion), the row it superseded and the ledger’s margin
below the standing side, the least pair gap the filtered decision found, its pairs, and
the earlier credit the manifest names before Couzo’s.

| n | Printed, up | Exact side, up at 16 | Index | Row superseded | Below the standing side by | Least pair gap | Pairs decided / all | Manifest’s earlier credit |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 328 | 18.614368938513 | 18.6143689385120729 | own | #686 | 7.95e-06 | 1.21e-12 | 706 / 53,628 | Muglich |
| 343 | 18.977575126267 | 18.9775751262667989 | own | #702 | 1.07e-04 | 1.20e-12 | 792 / 58,653 | Daniel after Fang |
| 365 | 19.614368938513 | 19.6143689385120729 | 328 + 1 L | #686 | 7.95e-06 | 0 | 809 / 66,430 | Muglich |
| 404 | 20.614368938513 | 20.6143689385120729 | 328 + 2 L | #686 | 7.95e-06 | 0 | 883 / 81,406 | Muglich |
| 417 | 20.933672777441 | 20.9336727774402606 | own | #686 | 9.99e-04 | 1.60e-12 | 911 / 86,736 | - |
| 455 | 21.848427413955 | 21.8484274139541061 | own | #678 | 3.38e-02 | 4.07e-12 | 1,040 / 103,285 | - |
| 456 | 21.881307463869 | 21.8813074638687389 | own | #678 | 8.76e-04 | 1.25e-12 | 1,106 / 103,740 | - |
| 458 | 21.903616797192 | 21.9036167971915195 | own | #678 | 1.62e-04 | 7.84e-11 | 1,081 / 104,653 | - |
| 459 | 21.937022304151 | 21.9370223041501789 | own | #686 | 2.06e-04 | 1.20e-12 | 1,030 / 105,111 | - |
| 461 | 21.964134608334 | 21.9641346083339922 | own | #686 | 2.06e-03 | 1.60e-12 | 1,023 / 106,030 | Muglich |
| 463 | 21.971254044975 | 21.9712540449745445 | own | #686 | 2.42e-03 | 8.94e-11 | 1,072 / 106,953 | - |
| 496 | 22.822875655559 | 22.8228756555586237 | own | #686 | 3.85e-09 | 1.20e-12 | 1,064 / 122,760 | - |
| 497 | 22.823102656285 | 22.8231026562840826 | own | #678 | 1.37e-06 | 1.12e-12 | 1,041 / 123,256 | - |
| 499 | 22.881306218323 | 22.8813062183220752 | own | #678 | 8.77e-04 | 4.43e-12 | 1,207 / 124,251 | - |
| 500 | 22.887841512273 | 22.8878415122724073 | 501 less 1 | 487b058 | at least 1.17e-02 | 1.18e-12 | 1,145 / 124,750 | - |
| 501 | 22.887841512273 | 22.8878415122724073 | own | #678 | 1.59e-02 | 1.18e-12 | 1,148 / 125,250 | - |
| 502 | 22.933269925480 | 22.9332699254794991 | own | #686 | 1.18e-03 | 1.44e-12 | 1,219 / 125,751 | - |
| 503 | 22.943933771540 | 22.9439337715399617 | own | #686 | 7.34e-04 | 1.18e-12 | 1,191 / 126,253 | Muglich |
| 504 | 22.961828398888 | 22.9618283988872938 | own | #686 | 2.91e-04 | 8.82e-12 | 1,193 / 126,756 | - |
| 505 | 22.964182800913 | 22.9641828009120983 | own | #686 | 7.09e-05 | 1.18e-12 | 1,252 / 127,260 | - |
| 506 | 22.971254044975 | 22.9712540449745445 | 463 + 1 L | #686 | 8.91e-04 | 0 | 1,194 / 127,765 | - |
| 509 | 22.993588501431 | 22.9935885014300704 | own | grid | at least 7.40e-04 | 1.49e-12 | 1,198 / 129,286 | - |
| 545 | 23.883414761903 | 23.8834147619022157 | own | #678 | 5.60e-03 | 8.06e-11 | 1,205 / 148,240 | - |
| 546 | 23.887841512273 | 23.8878415122724073 | 501 + 1 L | #678 | 1.17e-03 | 0 | 1,277 / 148,785 | - |
| 547 | 23.898819144794 | 23.8988191447939965 | own | 487b058 | at least 7.55e-03 | 1.20e-12 | 1,253 / 149,331 | - |
| 548 | 23.943933771540 | 23.9439337715399617 | 503 + 1 L | #686 | 7.34e-04 | 0 | 1,319 / 149,878 | Muglich |
| 549 | 23.955501804754 | 23.9555018047539789 | own | #678 | 8.43e-04 | 1.19e-12 | 1,258 / 150,426 | - |
| 550 | 23.960681444798 | 23.9606814447975880 | own | #686 | 3.77e-04 | 1.20e-12 | 1,241 / 150,975 | - |
| 553 | 23.979452392567 | 23.9794523925668811 | own | #686 | 3.34e-04 | 3.92e-12 | 1,366 / 152,628 | Muglich |
| 554 | 23.986307325908 | 23.9863073259072518 | own | #686 | 7.73e-06 | 3.55e-13 | 1,343 / 153,181 | Muglich |
| 592 | 24.883414761903 | 24.8834147619022157 | 545 + 1 L | #678 | 5.57e-03 | 0 | 1,338 / 174,936 | - |
| 593 | 24.887841512273 | 24.8878415122724073 | 501 + 2 L | #678 | 1.15e-03 | 0 | 1,367 / 175,528 | - |
| 594 | 24.898819144794 | 24.8988191447939965 | 547 + 1 L | 487b058 | at least 6.76e-04 | 0 | 1,387 / 176,121 | - |
| 595 | 24.943933771540 | 24.9439337715399617 | 503 + 2 L | #686 | 7.34e-04 | 0 | 1,409 / 176,715 | Muglich |
| 597 | 24.950690418637 | 24.9506904186364534 | own | #686 | 7.45e-03 | 1.40e-12 | 1,443 / 177,906 | - |
| 598 | 24.954250129268 | 24.9542501292674733 | own | #686 | 3.97e-03 | 1.60e-12 | 1,339 / 178,503 | - |
| 599 | 24.959619887409 | 24.9596198874082448 | own | #686 | 3.21e-03 | 1.35e-12 | 1,399 / 179,101 | Muglich |
| 600 | 24.978172747238 | 24.9781727472371350 | own | #686 | 1.61e-03 | 1.17e-12 | 1,439 / 179,700 | - |
| 601 | 24.986189080604 | 24.9861890806035131 | own | #686 | 1.26e-04 | 1.20e-12 | 1,423 / 180,300 | - |
| 602 | 24.988237878425 | 24.9882378784241400 | own | #686 | 2.12e-03 | 5.04e-12 | 1,444 / 180,901 | Muglich |
| 643 | 25.898819144794 | 25.8988191447939965 | 547 + 2 L | 487b058 | at least 6.76e-04 | 0 | 1,481 / 206,403 | - |
| 645 | 25.946937290069 | 25.9469372900683251 | 647 less 2 | 487b058 | at least 2.81e-03 | 2.18e-10 | 1,434 / 207,690 | - |
| 646 | 25.946937290069 | 25.9469372900683251 | 647 less 1 | 487b058 | at least 2.81e-03 | 2.18e-10 | 1,436 / 208,335 | - |
| 647 | 25.946937290069 | 25.9469372900683251 | own | #686 | 2.96e-03 | 2.18e-10 | 1,440 / 208,981 | - |
| 648 | 25.959619886978 | 25.9596198869773024 | own | #686 | 1.43e-03 | 1.21e-12 | 1,534 / 209,628 | Muglich |
| 651 | 25.981928099991 | 25.9819280999907479 | own | #686 | 9.51e-04 | 1.19e-12 | 1,695 / 211,575 | Muglich |
| 652 | 25.990044325432 | 25.9900443254312957 | own | #686 | 3.11e-04 | 1.38e-12 | 1,557 / 212,226 | Muglich |
| 653 | 25.992652721826 | 25.9926527218252415 | own | #678 | 1.76e-03 | 7.82e-11 | 1,518 / 212,878 | - |
| 654 | 25.994801642508 | 25.9948016425074131 | own | #686 | 6.57e-05 | 1.54e-12 | 1,616 / 213,531 | Muglich |
| 694 | 26.898819144794 | 26.8988191447939965 | 547 + 3 L | 487b058 | at least 6.76e-04 | 0 | 1,579 / 240,471 | - |
| 696 | 26.946937290069 | 26.9469372900683251 | 647 + 1 L less 2 | 487b058 | at least 2.81e-03 | 0 | 1,578 / 241,860 | - |
| 697 | 26.946937290069 | 26.9469372900683251 | 647 + 1 L less 1 | 487b058 | at least 2.81e-03 | 0 | 1,581 / 242,556 | - |
| 698 | 26.946937290069 | 26.9469372900683251 | 647 + 1 L | 487b058 | at least 2.81e-03 | 0 | 1,584 / 243,253 | - |
| 700 | 26.963723854128 | 26.9637238541272675 | own | #686 | 6.30e-06 | 1.14e-12 | 1,603 / 244,650 | Muglich |
| 702 | 26.976012028499 | 26.9760120284988631 | own | #686 | 6.81e-04 | 1.20e-12 | 1,733 / 246,051 | - |
| 705 | 26.990419622637 | 26.9904196226365133 | own | #686 | 5.38e-05 | 2.94e-11 | 1,671 / 248,160 | Muglich |
| 747 | 27.884019388658 | 27.8840193886574204 | 749 less 2 | 487b058 | at least 1.55e-02 | 1.15e-12 | 1,615 / 278,631 | - |
| 748 | 27.884019388658 | 27.8840193886574204 | 749 less 1 | 487b058 | at least 1.55e-02 | 1.15e-12 | 1,617 / 279,378 | - |
| 749 | 27.884019388658 | 27.8840193886574204 | own | #678 | 2.72e-02 | 1.15e-12 | 1,620 / 280,126 | - |
| 750 | 27.911200800711 | 27.9112008007105991 | own | 487b058 | at least 1.67e-02 | 8.82e-11 | 1,787 / 280,875 | - |
| 751 | 27.914175785603 | 27.9141757856025849 | own | #678 | 1.83e-02 | 1.20e-12 | 1,668 / 281,625 | - |
| 752 | 27.932396768486 | 27.9323967684851698 | own | #678 | 5.31e-05 | 4.66e-11 | 1,987 / 282,376 | - |
| 756 | 27.976782251658 | 27.9767822516578175 | own | #686 | 1.32e-04 | 1.20e-12 | 1,883 / 285,390 | Muglich |
| 758 | 27.983731022945 | 27.9837310229448515 | own | #686 | 5.53e-04 | 2.46e-11 | 2,012 / 286,903 | Muglich |
| 801 | 28.825777528963 | 28.8257775289621208 | own | 487b058 | at least 2.65e-03 | 3.52e-11 | 1,821 / 320,400 | - |
| 802 | 28.827439471389 | 28.8274394713880746 | own | 487b058 | at least 9.88e-04 | 8.18e-11 | 1,762 / 321,201 | - |
| 803 | 28.827585222385 | 28.8275852223840695 | own | 487b058 | at least 7.19e-02 | 1.15e-12 | 1,745 / 322,003 | - |
| 804 | 28.884019388658 | 28.8840193886574204 | 749 + 1 L | #678 | 2.52e-02 | 0 | 1,777 / 322,806 | - |
| 805 | 28.902673974184 | 28.9026739741833862 | 806 less 1 | #678 | 6.99e-03 | 1.59e-12 | 2,013 / 323,610 | - |
| 806 | 28.902673974184 | 28.9026739741833862 | own | #678 | 1.71e-02 | 1.59e-12 | 2,015 / 324,415 | - |
| 807 | 28.924694876402 | 28.9246948764016085 | own | 487b058 | at least 8.03e-06 | 3.98e-10 | 1,885 / 325,221 | - |
| 808 | 28.931498747933 | 28.9314987479323120 | own | #678 | 9.51e-04 | 1.20e-12 | 1,970 / 326,028 | - |
| 809 | 28.933954694456 | 28.9339546944556193 | own | 487b058 | at least 3.47e-03 | 1.15e-11 | 1,895 / 326,836 | - |
| 813 | 28.979120019579 | 28.9791200195783958 | own | #686 | 2.47e-03 | 2.37e-12 | 1,909 / 330,078 | Muglich |
| 814 | 28.981388189193 | 28.9813881891929735 | own | #686 | 2.06e-04 | 5.91e-11 | 1,904 / 330,891 | Muglich |
| 815 | 28.992261716554 | 28.9922617165532824 | own | #686 | 6.62e-04 | 1.11e-12 | 1,897 / 331,705 | - |
| 858 | 29.825571500168 | 29.8255715001673948 | 859 less 1 | 487b058 | at least 2.86e-03 | 3.74e-13 | 1,831 / 367,653 | - |
| 859 | 29.825571500168 | 29.8255715001673948 | own | 487b058 | at least 2.86e-03 | 3.74e-13 | 1,834 / 368,511 | - |
| 860 | 29.827585222385 | 29.8275852223840695 | 803 + 1 L | grid | 1.72e-01 | 0 | 1,909 / 369,370 | - |
| 863 | 29.902673974184 | 29.9026739741833862 | 806 + 1 L | #678 | 1.37e-02 | 0 | 2,179 / 371,953 | - |
| 864 | 29.924694876402 | 29.9246948764016085 | 807 + 1 L | 487b058 | at least 8.03e-06 | 0 | 2,047 / 372,816 | - |
| 865 | 29.931498747933 | 29.9314987479323120 | 808 + 1 L | #678 | 9.51e-04 | 0 | 2,134 / 373,680 | - |
| 866 | 29.933954694456 | 29.9339546944556193 | 809 + 1 L | 487b058 | at least 1.81e-03 | 0 | 2,059 / 374,545 | - |
| 867 | 29.942070418091 | 29.9420704180901865 | own | #678 | 7.62e-03 | 1.11e-12 | 2,036 / 375,411 | - |
| 868 | 29.974553547719 | 29.9745535477188754 | own | #686 | 8.89e-06 | 1.22e-12 | 2,199 / 376,278 | Muglich |
| 869 | 29.974935743865 | 29.9749357438648642 | own | #686 | 1.09e-06 | 1.20e-12 | 2,173 / 377,146 | Muglich |
| 870 | 29.979120019579 | 29.9791200195783958 | 813 + 1 L | #686 | 2.47e-03 | 0 | 2,068 / 378,015 | Muglich |
| 871 | 29.981295638373 | 29.9812956383721795 | own | #686 | 2.99e-04 | 1.20e-12 | 2,075 / 378,885 | Muglich |
| 872 | 29.992261716554 | 29.9922617165532824 | 815 + 1 L | #686 | 3.61e-04 | 0 | 2,059 / 379,756 | - |
| 873 | 29.992265777039 | 29.9922657770385690 | own | #686 | 3.57e-04 | 1.17e-12 | 2,079 / 380,628 | - |
| 917 | 30.825571499902 | 30.8255714999011878 | 918 less 1 | 487b058 | at least 2.86e-03 | 1.22e-12 | 1,946 / 419,986 | - |
| 918 | 30.825571499902 | 30.8255714999011878 | own | 487b058 | at least 2.86e-03 | 1.22e-12 | 1,949 / 420,903 | - |
| 919 | 30.827585222385 | 30.8275852223840695 | 803 + 2 L | #678 | 1.73e-02 | 0 | 2,023 / 421,821 | - |
| 923 | 30.924694876402 | 30.9246948764016085 | 807 + 2 L | 487b058 | at least 8.03e-06 | 0 | 2,161 / 425,503 | - |
| 924 | 30.931498747933 | 30.9314987479323120 | 808 + 2 L | #678 | 9.51e-04 | 0 | 2,248 / 426,426 | - |
| 925 | 30.933954694456 | 30.9339546944556193 | 809 + 2 L | 487b058 | at least 1.81e-03 | 0 | 2,173 / 427,350 | - |
| 926 | 30.942070418091 | 30.9420704180901865 | 867 + 1 L | #678 | 3.54e-03 | 0 | 2,205 / 428,275 | - |
| 927 | 30.969443226806 | 30.9694432268050400 | own | #686 | 5.36e-04 | 8.84e-11 | 2,203 / 429,201 | Muglich |
| 928 | 30.974935654060 | 30.9749356540592345 | own | #686 | 1.18e-06 | 1.13e-11 | 2,332 / 430,128 | Muglich |
| 931 | 30.989934444611 | 30.9899344446101474 | own | grid | at least 2.90e-07 | 1.86e-12 | 2,132 / 432,915 | Fang, PingYou Ltd |
| 932 | 30.992265777039 | 30.9922657770385690 | 873 + 1 L | #686 | 3.57e-04 | 0 | 2,245 / 433,846 | - |
| 978 | 31.825090165859 | 31.8250901658584109 | 979 less 1 | 487b058 | at least 3.34e-03 | 1.59e-12 | 2,006 / 477,753 | - |
| 979 | 31.825090165859 | 31.8250901658584109 | own | 487b058 | at least 3.34e-03 | 1.59e-12 | 2,009 / 478,731 | - |
| 980 | 31.827585222385 | 31.8275852223840695 | 803 + 3 L | 487b058 | at least 8.42e-04 | 0 | 2,141 / 479,710 | - |
| 987 | 31.941797078452 | 31.9417970784518649 | own | #678 | 2.87e-03 | 2.06e-12 | 2,301 / 486,591 | - |
| 989 | 31.974181306003 | 31.9741813060027712 | own | #686 | 7.56e-04 | 1.21e-12 | 2,294 / 488,566 | - |
| 994 | 31.992271544010 | 31.9922715440099804 | own | #686 | 6.12e-04 | 6.84e-11 | 2,375 / 493,521 | - |
| 995 | 31.993696413074 | 31.9936964130735590 | own | #686 | 4.78e-04 | 1.14e-12 | 2,335 / 494,515 | - |
| 996 | 31.994135336337 | 31.9941353363364388 | own | #686 | 3.87e-05 | 1.20e-12 | 2,397 / 495,510 | Muglich |

### The 30 Held Re-certifications

Each row’s print, the `4e4c8ce` certificate’s side rounded up at 16 places, how far below
it the pin’s certificate is, and what the index calls it. Both routes accept each, with
every control refused; the ledger leaves each undecided against the `4e4c8ce`
publication. Recording them would add 30 rows to the claims record, superseding the
`487b058` rows that stand at those counts, and `4e4c8ce`’s rows when that import
(think-yfoo) lands.

| n | Printed, up | 4e4c8ce side, up at 16 | This certificate below it by | Index |
| ---: | --- | --- | --- | --- |
| 535 | 23.656854249519 | 23.6568542495185541 | 2.37e-23 | 490 + 1 L |
| 582 | 24.656854249519 | 24.6568542495185541 | 2.47e-23 | 490 + 2 L |
| 591 | 24.828427124775 | 24.8284271247741273 | 2.48e-23 | 544 + 1 L |
| 631 | 25.656854249519 | 25.6568542495185541 | 2.57e-23 | 490 + 3 L |
| 633 | 25.677669529693 | 25.6776695296922677 | 2.57e-23 | 584 + 1 L |
| 640 | 25.828427124775 | 25.8284271247741273 | 2.58e-23 | 544 + 2 L |
| 682 | 26.656854249519 | 26.6568542495185541 | 2.67e-23 | 490 + 4 L |
| 684 | 26.677669529693 | 26.6776695296922677 | 2.67e-23 | 584 + 2 L |
| 691 | 26.828427124775 | 26.8284271247741273 | 2.68e-23 | 544 + 3 L |
| 695 | 26.899494936642 | 26.8994949366417450 | 2.69e-23 | 644 + 1 L |
| 735 | 27.656854249519 | 27.6568542495185541 | 2.77e-23 | 490 + 5 L |
| 737 | 27.677669529693 | 27.6776695296922677 | 2.77e-23 | 584 + 3 L |
| 742 | 27.778174593084 | 27.7781745930831558 | 2.78e-23 | 689 + 1 L |
| 745 | 27.828427124777 | 27.8284271247760159 | 2.78e-23 | 692 + 1 L |
| 790 | 28.656854249519 | 28.6568542495185541 | 2.87e-23 | 490 + 6 L |
| 791 | 28.656854249525 | 28.6568542495246164 | 2.87e-23 | 736 + 1 L |
| 797 | 28.778174593084 | 28.7781745930831558 | 2.88e-23 | 689 + 2 L |
| 798 | 28.798989873256 | 28.7989898732557379 | 2.88e-23 | 744 + 1 L less 1 |
| 799 | 28.798989873256 | 28.7989898732557379 | 2.88e-23 | 744 + 1 L |
| 854 | 29.778174593084 | 29.7781745930831558 | 2.98e-23 | 689 + 3 L |
| 855 | 29.798989873256 | 29.7989898732557379 | 2.98e-23 | 744 + 2 L less 1 |
| 856 | 29.798989873256 | 29.7989898732557379 | 2.98e-23 | 744 + 2 L |
| 857 | 29.798989873257 | 29.7989898732569475 | 2.98e-23 | 800 + 1 L |
| 909 | 30.656854249528 | 30.6568542495270285 | 3.07e-23 | 850 + 1 L |
| 913 | 30.778174593084 | 30.7781745930831558 | 3.08e-23 | 689 + 4 L |
| 915 | 30.798989873256 | 30.7989898732557379 | 3.08e-23 | 744 + 3 L |
| 916 | 30.798989873257 | 30.7989898732569475 | 3.08e-23 | 800 + 2 L |
| 970 | 31.656854249528 | 31.6568542495270285 | 3.17e-23 | 850 + 2 L |
| 975 | 31.778174593089 | 31.7781745930880724 | 3.18e-23 | 914 + 1 L |
| 977 | 31.798989873257 | 31.7989898732569475 | 3.18e-23 | 800 + 3 L |

### The 34 Restated Certificates

Each is an earlier report, owned by its import: `02f9690`’s by think-a4wq (with
think-1545), `f311f08`’s by think-om5l, `4e4c8ce`’s by think-yfoo, and `a7067d7`’s at 338
already the row the record holds (`couzo-certificates-2026-10-12`). At 335 the
certificate is 1.78e-11 or more above the 8 October decimal report the record holds, so
neither it nor the issue is recorded there.

| n | Printed | First published | Earlier certificate | Here |
| ---: | --- | --- | --- | --- |
| 335 | 18.822875655562 | `02f9690`, 2026-10-09 | `certificates/n335.cert` | pinned; the same bytes as [couzo-exact-certificates-2026-10-09](../couzo-exact-certificates-2026-10-09/README.md)'s copy |
| 336 | 18.825571499862 | `02f9690`, 2026-10-09 | `certificates/n336.cert` | pinned; the same bytes as [couzo-exact-certificates-2026-10-09](../couzo-exact-certificates-2026-10-09/README.md)'s copy |
| 337 | 18.858391767637 | `02f9690`, 2026-10-09 | `certificates/n337.cert` | pinned; the same bytes as [couzo-exact-certificates-2026-10-09](../couzo-exact-certificates-2026-10-09/README.md)'s copy |
| 338 | 18.906332809853 | `a7067d7`, 2026-10-12 | `certificates/n338.cert` | pinned; the same bytes as [couzo-certificates-2026-10-12](../couzo-certificates-2026-10-12/README.md)'s copy |
| 340 | 18.939649632892 | `f311f08`, 2026-10-11 | `certificates/n340.cert` | pinned; the same bytes as [couzo-certificates-2026-10-11](../couzo-certificates-2026-10-11/README.md)'s copy |
| 341 | 18.951882408720 | `02f9690`, 2026-10-09 | `certificates/n341.cert` | pinned; the same bytes as [couzo-exact-certificates-2026-10-09](../couzo-exact-certificates-2026-10-09/README.md)'s copy |
| 373 | 19.823062082838 | `02f9690`, 2026-10-09 | `certificates/n373.cert` | pinned; the same bytes as [couzo-exact-certificates-2026-10-09](../couzo-exact-certificates-2026-10-09/README.md)'s copy |
| 374 | 19.832356217033 | `02f9690`, 2026-10-09 | `certificates/n374.cert` | pinned; the same bytes as [couzo-exact-certificates-2026-10-09](../couzo-exact-certificates-2026-10-09/README.md)'s copy |
| 410 | 20.778174593076 | `4e4c8ce`, 2026-10-15 | `certificates/best/n410.cert` | pinned by digest |
| 413 | 20.831663365378 | `4e4c8ce`, 2026-10-15 | `certificates/best/n413.cert` | pinned by digest |
| 454 | 21.828427124844 | `4e4c8ce`, 2026-10-15 | `certificates/best/n454.cert` | pinned by digest |
| 490 | 22.656854249519 | `4e4c8ce`, 2026-10-15 | `certificates/best/n490.cert` | pinned by digest |
| 498 | 22.828427124827 | `4e4c8ce`, 2026-10-15 | `certificates/best/n498.cert` | pinned by digest |
| 544 | 23.828427124775 | `4e4c8ce`, 2026-10-15 | `certificates/best/n544.cert` | pinned by digest |
| 584 | 24.677669529693 | `4e4c8ce`, 2026-10-15 | `certificates/best/n584.cert` | pinned by digest |
| 596 | 24.949747468335 | `4e4c8ce`, 2026-10-15 | `certificates/best/n596.cert` | pinned by digest |
| 637 | 25.778174593082 | `4e4c8ce`, 2026-10-15 | `certificates/best/n637.cert` | pinned by digest |
| 644 | 25.899494936642 | `4e4c8ce`, 2026-10-15 | `certificates/best/n644.cert` | pinned by digest |
| 689 | 26.778174593084 | `4e4c8ce`, 2026-10-15 | `certificates/best/n689.cert` | pinned by digest |
| 692 | 26.828427124777 | `4e4c8ce`, 2026-10-15 | `certificates/best/n692.cert` | pinned by digest |
| 699 | 26.949747468415 | `4e4c8ce`, 2026-10-15 | `certificates/best/n699.cert` | pinned by digest |
| 736 | 27.656854249525 | `4e4c8ce`, 2026-10-15 | `certificates/best/n736.cert` | pinned by digest |
| 743 | 27.798989873256 | `4e4c8ce`, 2026-10-15 | `certificates/best/n744.cert less 1` | pinned by digest |
| 744 | 27.798989873256 | `4e4c8ce`, 2026-10-15 | `certificates/best/n744.cert` | pinned by digest |
| 746 | 27.828427124795 | `4e4c8ce`, 2026-10-15 | `certificates/best/n746.cert` | pinned by digest |
| 792 | 28.656854249526 | `4e4c8ce`, 2026-10-15 | `certificates/best/n792.cert` | pinned by digest |
| 800 | 28.798989873257 | `4e4c8ce`, 2026-10-15 | `certificates/best/n800.cert` | pinned by digest |
| 850 | 29.656854249528 | `4e4c8ce`, 2026-10-15 | `certificates/best/n850.cert` | pinned by digest |
| 862 | 29.899494936647 | `4e4c8ce`, 2026-10-15 | `certificates/best/n862.cert` | pinned by digest |
| 914 | 30.778174593089 | `4e4c8ce`, 2026-10-15 | `certificates/best/n914.cert` | pinned by digest |
| 976 | 31.778174593090 | `4e4c8ce`, 2026-10-15 | `certificates/best/n976.cert` | pinned by digest |
| 985 | 31.920310216821 | `4e4c8ce`, 2026-10-15 | `certificates/best/n986.cert less 1` | pinned by digest |
| 986 | 31.920310216821 | `4e4c8ce`, 2026-10-15 | `certificates/best/n986.cert` | pinned by digest |
| 988 | 31.949747468406 | `4e4c8ce`, 2026-10-15 | `certificates/best/n988.cert` | pinned by digest |

## Above 1024

The issue’s 1112 rows from 1033 to 9913 are not recorded or replayed here. The index
states them through 98 distinct certificates under `certificates/best/`, 51,161,736
bytes and 9.1 MB as zlib stores them: 85 rows are a certificate’s own count, 171 its
deletions, and 856 L-border constructions, 621 of them with deletion. The pin writes out
an explicit certificate at only 90 of the 1112 counts. Whether the record tracks counts
above 1024 at all (D1), whether a construction without its own file becomes a row (D2),
and where the certificates are hosted (D4) are the owner’s decisions (think-f2io); every
file is pinned by the commit until then. Joost de Winter’s #666 claims above 1024 wait on
the same answer.

## What Is Not Established

The certificates establish finite upper bounds at their exact sides, nothing more.
Novelty, local or global optimality and rigidity are not decided, and neither are the
source’s credit and lineage statements: the manifest’s seed, construction and parent
records are the author’s. The issue says both maintained exact routes accept the source
witnesses and that no compared construction matches or beats a listed bound; those runs
are the author’s. The filtered route is a first-party program; its two routes share the
certificate parser, the half-angle conversion, the pair filter and Python’s rational
arithmetic, so it is two implementations of the unit-shape, pair and wall predicates, not
two independent replays (RF-1 of the 20 October review). The all-pairs kernel has run only
at 343 and 996. No stage 4 review is owed for a beyond-horizon row, and none is recorded.

## Credit and Licence

Francisco Couzo wrote the source, which states no licence for its data; the certificates
are kept as factual data and nothing of the source is relicensed.
The manifest credits Couzo at every row and keeps earlier credits beside it: at 28 of the
109 recorded counts the packing refines Darius Muglich’s #686 packing (or is an L-border
of one), at 343 Evan Daniel’s #702 packing in Kevin Fang’s two-wedge family, and at 931
Fang’s rectangle and gluing with PingYou Ltd’s squares. Per-row credit beyond the horizon
is the owner’s open question from #686.
The checker is Evan Daniel’s, modified by Couzo with Codex. The issue states nothing
about AI assistance; the checker’s header names Codex, and the author’s issues of 13 and
14 October disclose OpenAI Codex and Claude Code assistance.

## Commands

From `packing/`:

```sh
uv run --frozen --all-extras --group dev python -m devtools.acquire_source couzo-issue715-2026-10-21 --check
uv run --frozen --all-extras --group dev python -m devtools.couzo_715_replay check
uv run --frozen --all-extras --group dev python -m devtools.couzo_715_replay check --replay
uv run --frozen --all-extras --group dev python -m devtools.couzo_715_replay publications --history CLONE
uv run --frozen --all-extras --group dev python -m devtools.couzo_715_replay filtered --pinned CHECKOUT --workers 2
uv run --frozen --all-extras --group dev python -m devtools.couzo_715_replay exhaustive --n 343 996
uv run --frozen --all-extras --group dev python -m devtools.couzo_715_replay goebel
uv run --frozen --all-extras --group dev python -m devtools.couzo_715_replay claims-record
```

`check` reads the four receipts and the beyond-horizon claims record against the issue
and the packet; `check --replay` decides every row and control again (about 19 CPU
minutes). `publications` needs a clone of the source’s history (blobless is enough) and
the network for the blobs it lacks; `filtered --pinned` reads the index, the manifest and
each construction’s parent from a checkout at the pin, held to their digests.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
