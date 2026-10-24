# Mykhailo Polkovskyi’s f1ceee4 for Issue 732: 138 Certificates at 328 to 989

[Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records/tree/f1ceee4c1dd69f97d8e50e6ddaf1a14084dceda7/certificates/0000-0999)
at `f1ceee4c1dd69f97d8e50e6ddaf1a14084dceda7` (committed 2026-10-23T20:34:13Z, pushed at
20:34:22Z, “Add 138 newly certified world records (N <= 1024) with exact open-container
Weierstrass SAT verification”) holds the release the author’s
[comment of 20:35:12Z on issue #732](https://github.com/jlevy/squares/issues/732#issuecomment-6374211504)
reports: 138 rewritten exact rational certificates at 328 to 989, indexed by
`certified_bounds.json`.
This packet retains all 138, which the
[ledger of 24 October for f1ceee4](../../../campaign/issue-intake/upper-bounds-issue732-f1ceee4-20261024/README.md)
records as rows (think-e3im).
It is #732’s second release; the first, at `17cc220`, is the
[22 October packet](../mishapolk-issue732-2026-10-22/README.md).

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json).
The source was retrieved at 2026-10-24T01:31Z, as a blobless clone of the author’s
repository with its history to the head, `7e82c64`.
Every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest: 401
files, of which 140 are retained under `source/` (18,869,805 bytes), and 261 are pinned by
digest with the reason the declaration gives (43,938,773 bytes).

- **Retained:** the 138 certificates the walk records as rows, `README.md` and `LICENSE`.
- **Pinned by digest:** the other 252 certificates at 325 to 1024, unchanged since
  `17cc220` (30 of them byte-identical to the 22 October packet’s retained copies), the five
  indexes, `.gitignore`, the author’s `check_packing.py`, and Evan Daniel’s verifier with its
  licence against the copies the `couzo-issue678-2026-10-18` packet retains.
- **Pinned by the commit alone:** the certificates in the corpus and above 1024. No blob
  above 1024 was fetched, and no source file was executed.

**Licence.** `LICENSE` is the MIT licence, copyright Mykhailo Polkovskyi (Mishapolk), added
at `17cc220` and unchanged here.
The author’s comment on #719
([issuecomment-6350348588](https://github.com/jlevy/squares/issues/719#issuecomment-6350348588))
says it covers every certificate, catalogue, manifest and tool in the repository.

**Custody.** `f1ceee4` rewrites the 138 certificates, `certified_bounds.json` and
`upper_bounds.json`, and adds `.gitignore`.
It does not rewrite `certificates/manifest.json`, `census.json` or `SHA256SUMS`, which still
name the earlier files at the 138 counts, so the release is held to `certified_bounds.json`,
the index it keeps current.
[receipts/source-history.json](receipts/source-history.json), written by
`devtools.beyond_horizon_replay source-history` from the clone, holds each of the 390
certificates at 325 to 1024 to the path, SHA-256 and exact bound that index states.
It dates every side the repository published at those counts with the first commit that held
it. The 138 are the certificates whose blobs `f1ceee4` first holds, and each side is new
there.

**The prints.** Each row records its certificate’s exact header side rounded up at 12
places. The index’s own `rounded_up` field rounds to the nearest place instead, and at 70 of
the 138 counts it prints one unit below the side, as at 365 (`19.614368938495` for a side
the row records as `19.614368938496`).
No row reads it.

## Rows Beyond the Corpus

The comment has no table of rows.
[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares the
release `#732 comment 6374211504`, dated by the comment, whose packet lists the rows its walk
records, [acquisition/declared-rows.json](acquisition/declared-rows.json).
[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the record the
source register reads them from, as the source `mishapolk-issue732-f1ceee4-2026-10-23`.

**Report order.** The ledger walks the 138 counts from starts frozen at `main` `0bbb0a2c4`
(#754’s merge), each row read at the exact side its source states, and Göbel’s construction
beside it, since the walk was read on 24 October.
Beside the comment’s claims it walks the author’s own earlier files, every publication in a
watched repository strictly below the start, and #715’s re-certifications.

- **All 138 are recorded, each the count’s current row**, below the standing side by
  8.09 × 10⁻¹³ (924) to 8.59 × 10⁻⁴ (747): 1 by less than 10⁻¹², whose 12-place print
  differs from the row’s, so it restates nothing; 109 by 10⁻¹² to 10⁻⁹, 17 by 10⁻⁹ to
  10⁻⁶, and 11 by more.
- They supersede #715’s rows at 59 counts, #732’s own `17cc220` rows at 47, #719’s at 21,
  `couzo-index-2026-10-15`’s at 9, `couzo-verified-bounds-2026-10-14`’s at 1, and Couzo’s
  8 October row at 335.
- At 985 the walk records Couzo’s `4e4c8ce` deletion bound first, an earlier report by the
  owner’s answer of 23 October on D6 (think-f2io) with no row of its own, and `f1ceee4`’s
  side below it; the chain passes over the bound.
- At 909, 970 and 975 #715’s re-certifications restate the rows they beat (think-fwa9), and
  `8a488a1`’s file at 985 ties the deletion bound.

**All 138 are verified.** The filtered two-route decision of `devtools.couzo_678_replay`,
reused unchanged, accepts every packing on both routes: 216,573 candidate pairs of
36,623,826, and every corner against every wall.
Every print is the header side rounded up at 12 places.
**All 828 controls are refused by both routes.**
The run took 1,326 seconds of wall on two workers at `nice` on a shared host, the positive
decisions 125.6 CPU seconds ([receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json)).
No square touches the box: every wall clears by at least 10⁻¹⁶, the clearance the comment
states.
No pair the filter decides touches: each clears by at least 7.38 × 10⁻¹⁵ (919).
That claim rests on the filtered pairs, whose centres are closer than √2; a pair at exactly √2
could still touch corner to corner.
[Review A of #769](https://github.com/jlevy/squares/pull/769#issuecomment-6380362746) scanned
exactly every pair with centres closer than √2.01 in all 138: none touches, and outside the
filter the least gap is 1.64 × 10⁻¹³ (554).
At 582, 691, 798 and 924 the least gap overall lies outside the filter, below the receipt’s
per-row `least_pair_gap` (at 924, 8.597 × 10⁻¹³ at squares 191 and 211 against the
receipt’s 8.695 × 10⁻¹³).
That scan is the review’s, not a receipt of this packet.

The maintained all-pairs kernel of `devtools.evand_arrangement_reports`, every pair and no
filter, decided the positives at 335, 747 and 989, the count whose 8 October row the release
supersedes, its largest margin and its largest count: 823,142 pairs in 157.5 CPU seconds.
Both routes accept each, and each least pair gap and wall clearance equals, exactly, the
filtered decision’s ([receipts/exhaustive-sample.json](receipts/exhaustive-sample.json)).

Every certificate was first committed at `f1ceee4`
([receipts/first-commits.json](receipts/first-commits.json)), and every side is below Göbel’s
classical construction at its count ([receipts/goebel-comparison.json](receipts/goebel-comparison.json)).

## Couzo’s 8 October Row at 335

The record held Couzo’s 8 October decimal report at 335, `18.822875655543559`, with no exact
side, and asked whether its poses pack at their printed side (D3 of think-f2io, think-rx26).
Couzo answered on #715 at 22:16:52Z on 23 October
([issuecomment-6375833547](https://github.com/jlevy/squares/issues/715#issuecomment-6375833547)):
his 9 October certificate is that report’s packing in exact form, its centres dilated by
exactly 1 + 10⁻¹² about (½, ½) and the three near-axis angles (4.73 × 10⁻¹¹, 9.02 × 10⁻¹² and
1.10 × 10⁻¹² radians) set to 0; the print read literally overshoots a wall by up to
7.8 × 10⁻¹⁶; and “the bound we stand behind is the certificate’s”.
The owner answered on 24 October that the existing process decides it: “we should have clear
defined process for this already, why are you asking? if it is replaced by another one, we
could indicate that too”.
[`devtools.couzo_decimal_decisions`](../../../devtools/couzo_decimal_decisions.py) decides it,
and think-rx26’s five other counts (336, 337, 341, 373 and 374), in
[receipts/couzo-8-october-decisions.json](receipts/couzo-8-october-decisions.json), in 4.6
CPU seconds:

- **Read literally**, every printed centre and every angle in radians, the poses are not a
  packing at 335: 21 squares cross a wall, the worst, square 2, by 7.77 × 10⁻¹⁶, its angle
  −1.55 × 10⁻¹⁵ radians; no pair overlaps.
  Outward-rounded interval arithmetic, with the wall and pair formulas of
  `devtools.decimal_pose_margins` read in radians, proves each such wall negative.
- **With the 196 angles below 10⁻¹⁰ read as 0**, the poses pack exactly at the printed side:
  every wall and pair is proved nonnegative, and the least pair separation is
  5.86 × 10⁻¹⁴.
  These are the angles his 9 October certificate sets to 0: 193 binary64 roundings of zero,
  none above 3.1 × 10⁻¹⁵, and three near-axis angles, 1.1 × 10⁻¹², 9.0 × 10⁻¹² and
  4.7 × 10⁻¹¹.
  The certificate sets to 0 exactly these and the 88 printed zeros, 284 rotations in all, and
  keeps the next angle, 2.40 × 10⁻¹⁰.
- **The printed centres with the 9 October certificate’s rational rotations** pack at the
  printed side on both exact routes of `devtools.couzo_678_replay`.
- **The 9 October certificate** is that packing, 1.78 × 10⁻¹¹ larger, and packs at its own
  side on both routes.

So the row reports a packing that exists at its print when it is read as its own
certificate reads it, which is how Couzo’s answer reads it too.
Read literally it does not: square 2 crosses the left wall by 7.77 × 10⁻¹⁶ and square 308 the
right wall by 6.88 × 10⁻¹⁶, so the literal poses need a side of at least the print plus
1.465 × 10⁻¹⁵, outside the span of one unit either side of the print that the walk’s start
reads at 335.
The verdict does not depend on the reading: `f1ceee4`’s 335, `18.822875655542`, is
1.607 × 10⁻¹² below the print and 1.94 × 10⁻¹¹ below the certificate, and supersedes the row
on either reading.
The row stays listed as Couzo printed it.

At 336 and 337 neither reading packs at the printed side: one wall fails by 4.0 × 10⁻¹⁶ and
three by 1.0 × 10⁻¹⁶ with the near-axis angles at 0.
At 341, 373 and 374 the poses pack with the angles below 10⁻¹⁰ read as 0, which is this
decision’s reading and not a certificate’s: Couzo’s 9 October certificates at the five are
other packings, below the prints, and their rows already supersede the 8 October ones.

## The Later Commits

Three commits followed, which no issue reports, so each is a report from the push that made
it public, as the repository’s activity log dates it.
[receipts/later-commits.json](receipts/later-commits.json) reads every certificate file and
index bound each one changes at a count to 1024 (`later-commits`).
Each changes only counts in the corpus, and the walk records none of them:

- `34e59f3` (pushed 21:28:42Z) restates T-229’s two sides in the indexes: 105 ties T-229,
  and 204 is above T-231.
- `c0bf150` (pushed with it) rewrites or adds 51 certificates at 17 to 301, centred in an open
  container. Each is above the case’s reported lane (31 counts), a register entry pending
  adoption (14), PR #574’s row (5) or T-126 (1).
  At seven of them a print alone cannot order the certificate: the reported lanes at 17, 28,
  39, 69, 87 and 205, and T-123 at 177.
  The walk’s
  [undecided-resolved.json](../../../campaign/issue-intake/upper-bounds-issue732-f1ceee4-20261024/undecided-resolved.json)
  decides each exactly against the algebraic side, which the certificate lies 3.9 × 10⁻²⁵ to
  1.4 × 10⁻²⁴ above (`decide-later`, through `devtools.decide_undecided_comparisons`).
- `7e82c64` (pushed 21:42:38Z) rewrites 303, 9.89 × 10⁻⁶ above Amund Kristiansen’s #755
  (11:12:48Z), which was reported first.

## Credit

The index credits 127 of the 138 to “Mishapolk (continuous SLP quench refinement of Couzo
topology)”, and the other 11 to “Mishapolk (major structural quench refinement of Couzo
topology)”. The comment says the candidates were Couzo’s base topologies, re-quenched, and
that the author verified them with this project’s `sqpack.verify` in his testbench.
Unlike `17cc220`’s, the certificates’ headers name no source file.

Couzo’s own manifests credit the topologies at some of these counts to earlier work, and by
[attribution.md](../../../../attribution.md)’s chain rule a chain through an intermediate
author keeps every supported link:

- **His #715 manifest at `6b7391d`** (SHA-256 `5b56aebd…`, pinned in the
  [`couzo-issue715-2026-10-21` packet](../couzo-issue715-2026-10-21/README.md)) credits
  Darius Muglich at 15 of the 138, as its own credit or its prior source credit: 328, 365,
  404, 548, 554, 599, 602, 648, 651, 654, 700, 756, 813, 814 and 871.
  It credits 343 to Evan Daniel with Kevin Fang’s two-wedge construction, and names Muglich,
  Fang and PingYou Ltd in its provenance at 813.
- **His `4e4c8ce` manifest** (SHA-256 `08f257e7…`, pinned in the
  [`couzo-index-2026-10-15` packet](../couzo-index-2026-10-15/README.md)) credits PingYou Ltd at
  328, Evan Daniel at 365, 404 and 455 and after Kevin Fang at 343, “refinement of Kevin
  Fang’s packing” at 651, and Fang’s rectangle and gluing with PingYou Ltd’s square input at
  813.

The key’s credit is therefore “Polkovskyi after Couzo, Muglich, Daniel, Fang, PingYou Ltd,
Levy”, with Levy for the checker.

The source’s `README.md`, rewritten at `7b6366f` and retained here, says “Credit &
Maintainer: Mishapolk / Mykhailo Polkovskyi”.
It credits the index’s baselines at N ≤ 308 to Gardner, Erdős, Göbel, Friedman, Ellsworth
and Daniel, and 3,734 classical L-border bounds to Frits Göbel; none of these is one of the
138. Those statements are the source’s.

The comment asks that 11 counts be credited to Mishapolk alone: 463, 645, 646, 651, 696, 702,
747, 756, 809, 813 and 989, at margins of 2.5 × 10⁻⁶ to 8.59 × 10⁻⁴, with joint credit at the
other 127.
[receipts/pose-identity.json](receipts/pose-identity.json) measures each of the 11, square by
square and in binary64, under each of the box’s eight symmetries (`pose-identity`).
Each is measured against the retained certificate of the row it supersedes (#715’s at 463 and
747, #732’s own at the other nine) and against #715’s at the count:

- every one pairs one to one with Couzo’s #715 certificate under the box’s identity, every
  square within 0.23 of its counterpart, the largest distance running from 1.2 × 10⁻² (813)
  to 0.225 (696);
- between 85 (463) and 558 (989) squares moved by more than 10⁻³, and rotations changed by up
  to 9.0 degrees (646);
- against the row it supersedes each pairs the same way, but at 696, where one square
  moves 0.96 from #732’s.

The measurement decides nothing.
Per-row credit beyond the corpus is the owner’s open question (D5, think-f2io), so the record
keeps the request beside the index’s own word.
Neither the comment nor the source’s README states AI assistance.

## The Comment’s Theorems

The comment states two theorems, and neither is registered.
Theorem 1 says that a chain of edge-to-edge contacts across opposite corners at angles 0 and
π/4 fixes the side in Q(√2) with no first-order descent, with a corollary that 33 diagonal
counts (10, 11, 14, 18, 23, 27, 32, …) have no continuous slack.
Theorem 2 says that solver outputs at general angles admit a descent direction and an exact
dilation.

- No proof is given, and neither bounds any s(n).
- The corollary’s own examples contradict its hypothesis: the record’s best packings at 11
  and 18 tilt squares by about 40.18 and 24.3 degrees, angles neither 0 nor π/4.
- Theorem 2 describes the author’s method.

## A Later Report at Overlapping Counts

Francisco Couzo’s issue #763 (2026-10-23T23:35:51Z) claims upper bounds at many of these
counts. His commits `efef7d1` and `fa6237e` were committed at 18:16Z and 18:59Z, before
`f1ceee4` (20:34:13Z), but reached GitHub only in his push of 23:38:42Z, from `6b7391d` to
`964ee2b`, as GitHub’s activity API for his repository records it.
By their headers `fa6237e`’s sides lie below `f1ceee4`’s at 131 of the 138 counts.
They follow `f1ceee4` in report order only by the push rule, which dates a commit by the push
that made it public, not by its commit time (`beyond_horizon_replay.PUSHED_LATER`, which now
holds that push, so the next import dates them by it).
This walk does not read them; the next import walks them from a `main` that holds these rows
(think-cnn7).

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source mishapolk-issue732-f1ceee4-2026-10-23 --check
python -m devtools.beyond_horizon_replay check --issue "#732 comment 6374211504"
python -m devtools.beyond_horizon_replay check --issue "#732 comment 6374211504" --replay --workers 2
python -m devtools.beyond_horizon_replay source-history --issue "#732 comment 6374211504" --clone CLONE
python -m devtools.beyond_horizon_replay later-commits --issue "#732 comment 6374211504" --clone CLONE
python -m devtools.beyond_horizon_replay decide-later --issue "#732 comment 6374211504"
python -m devtools.beyond_horizon_replay pose-identity --issue "#732 comment 6374211504"
python -m devtools.couzo_decimal_decisions check
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
