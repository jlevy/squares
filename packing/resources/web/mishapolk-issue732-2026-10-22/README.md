# Mykhailo Polkovskyi’s Issue 732: 77 Certificates at 17cc220

[Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records/tree/17cc220131360ef290750eb845a3544c30ccb389/certificates/0000-0999)
at `17cc220131360ef290750eb845a3544c30ccb389` (committed 2026-10-22T20:15:36Z, “docs: add
MIT License covering all certificates, catalogs, and tools”) holds the release that
[issue #732](https://github.com/jlevy/squares/issues/732) reports: 5,468 exact rational
certificates at 328 to 9913, indexed by `certificates/manifest.json`.
`17cc220` adds only `LICENSE` to `814fbe9` (tag `v1.0.0`), the commit the issue describes,
so it holds the issue’s certificates with their licence.
This packet retains the 77 that the
[ledger of 23 October for issue 732](../../../campaign/issue-intake/upper-bounds-issue732-20261023/README.md)
records as rows (think-0gp6).

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of the pin, from the
declaration in [acquisition/declaration.json](acquisition/declaration.json).
The source was retrieved at 2026-10-23T02:35Z, as a blobless clone of the author’s
repository with its history to `7b6366f`.
Every file is bound to its Git blob at the pin.
[acquisition/sources.json](acquisition/sources.json) is the acquisition record and
[acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest: 400
files, of which 79 are retained under `source/` (9,312,907 bytes), and 321 are pinned by
digest with the reason the declaration gives (52,508,115 bytes).

- **Retained:** the 77 certificates the walk records as rows, `README.md` and `LICENSE`.
- **Pinned by digest:** the other 313 certificates at 325 to 1024, the five indexes, the
  author’s `check_packing.py`, and Evan Daniel’s verifier with its licence against the
  copies the `couzo-issue678-2026-10-18` packet retains.
- **Pinned by the commit alone:** the 126 certificates in the corpus and the 5,078 above
  1024. No blob above 1024 was fetched, and no source file was executed.

**Licence.** `LICENSE` is the MIT licence, copyright Mykhailo Polkovskyi (Mishapolk).
The author’s comment on #719
([issuecomment-6350348588](https://github.com/jlevy/squares/issues/719#issuecomment-6350348588))
says it covers every certificate, catalogue, manifest and tool in the repository.
The indexes are 2.7 to 7.7 MB each and are pinned by digest under OR-18.

**Custody.** The five SHA-256 values the issue states, for `upper_bounds.json`,
`certified_bounds.json`, `certificates/manifest.json`, `certificates/census.json` and
`certificates/SHA256SUMS`, are the digests this packet pins for those files.
[receipts/source-history.json](receipts/source-history.json), written by
`devtools.beyond_horizon_replay source-history` from a blobless clone, holds each of the
390 certificates at 325 to 1024 to the path, SHA-256 and exact bound the manifest states.
It reads only certificate files whose paths name a count in that range, and lists every
side such a file published at those counts with the first commit that held it.
It reads no other file, so two kinds of publication in the repository are not in it:

- **The decimal poses** `certificates/square-343.txt` to `square-360.txt`, there since
  `2b76e6f` (2026-10-09) and still at the pin, are not certificates.
  Every one is above the grid’s 19, as the
  [9 October packet](../mishapolk-decimal-poses-2026-10-09/README.md) records.
- **The indexes** `upper_bounds.json` and `certified_bounds.json`, at `8a488a1`, `3285fac`,
  `814fbe9` and `17cc220`. The history scan reads an index’s `verified` and certified
  bounds, as it does for Couzo’s, and at no commit does either index state one at 325 to
  1024 below the start and every side walked there.
  Only `3285fac`’s `reported` lane does, at 34 counts, where it restates the Kingbird
  catalogue’s 14-place prints of the classical sides the walk holds, 1.95 × 10⁻¹⁶ to
  7.91 × 10⁻¹⁵ below them. The scan reads no index’s `reported` lane.

**Later commits.** `7b6366f` (2026-10-23T01:50:22Z), the head when this packet was written,
removes the certificate at 3426, whose side was above its grid side, and sets 3426 to the
grid in the indexes. It changes nothing at or below 1024.

## Rows Beyond the Corpus

The issue has no table of rows.
[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares it a
release whose packet lists the rows its walk records,
[acquisition/declared-rows.json](acquisition/declared-rows.json), which `declare-rows`
writes from the ledger and the source history.
Each row records its certificate’s header side rounded up at 12 places, the manifest’s
`rounded_up`.

**Report order.** The ledger walks the 390 counts from starts frozen at `main` `fcf2f96a5`
(#730’s merge), each row read at the exact side its source states.
Beside the issue’s claims it walks the author’s own earlier files, since the repository is
watched, and every publication in a watched repository strictly below the start.

- **77 are recorded, each the count’s current row:** 76 first published at `8a488a1`
  (2026-10-22T19:08:59Z) and 539, first published at `1851c2c`.
  539 is one of the ten rows #719’s 06:05Z edit withdrew, which this issue claims again.
- Each is below the standing side by 7.49 × 10⁻¹³ (735) to 7.38 × 10⁻⁴ (752): 7 by less
  than 10⁻¹² (798 by 9.997 × 10⁻¹³), 34 by 10⁻¹² to 10⁻⁹, 17 by 10⁻⁹ to 10⁻⁶, and 19 by
  more.
- They supersede issue #715’s rows at 30 counts, issue #719’s at 29,
  `couzo-index-2026-10-15`’s at 14 and `couzo-verified-bounds-2026-10-14`’s at 4.

[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the record
the source register reads them from, as the source `mishapolk-issue732-2026-10-22`.

**All 77 are verified.** The filtered two-route decision of `devtools.couzo_678_replay`,
reused unchanged, accepts every packing on both routes: 124,464 candidate pairs of
20,950,130, and every corner against every wall.
Every print is the header side rounded up at 12 places.
**All 462 controls are refused by both routes.**
The run took 389 seconds of wall on two workers, the positive decisions 82.0 CPU seconds
([receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json)).
No square touches the box and no pair touches: every wall clears by at least
2.71 × 10⁻²⁰ and every pair by at least 5.42 × 10⁻²⁰.

The maintained all-pairs kernel of `devtools.evand_arrangement_reports`, every pair and no
filter, decided the positives at 645, 752 and 995, the three the author or the triage names as
refinements of #715’s packings or the largest count: 984,581 pairs in 322.5 CPU seconds.
Both routes accept each, and each least pair gap and wall clearance equals, exactly, the
filtered decision’s ([receipts/exhaustive-sample.json](receipts/exhaustive-sample.json)).

Every certificate was first committed at `8a488a1`
([receipts/first-commits.json](receipts/first-commits.json)); the file at 539 holds the side
`1851c2c` first published in another file.
Every side is below Göbel’s classical construction at its count
([receipts/goebel-comparison.json](receipts/goebel-comparison.json)).

## Held Back and Not Recorded

- **499 restates #719’s row.** It is 8.66 × 10⁻¹³ below it, and both round up to
  22.881306218113 at 12 places: by the owner’s answer of 23 October 2026 a
  re-certification below the print restates the report it beats, which stays the row
  (think-fwa9), so the walk does not record it.
- **The author’s own `1851c2c` files at the nine other withdrawn counts** (411, 451, 494,
  495, 540, 583, 587, 632 and 683) are below every earlier report, and the issue’s files are
  below them.
  By the owner’s answer of 23 October 2026 a file its author withdrew from an issue,
  claiming a lower one later, is not a report (think-8m4k): the walk keeps them out of the
  record, a settled disposition, and no verdict rests on them.
- **The other 313 are not recorded.** 131 equal an earlier report, 81 of them #719’s rows
  exactly, 181 lie above one, and 499 restates #719’s row.
  43 of them, 331, 369 and 376 among them, are above Göbel’s construction at their count,
  which the owner counts as an earlier report since 23 October 2026 (think-8krd).
  55 are decided only against publications the walk holds for an owner decision
  (`beyond_horizon_replay.WALKS`):
  - 41 against constructions with no certificate file;
  - 14 against index deletion bounds, 985 among them, equal to Couzo’s `4e4c8ce` bound.
- **What each answer would record.** `beyond_horizon_replay held-dependents` reruns the
  walk without each class of hold. Beside #732’s own claims, each answer also reaches the
  author’s earlier files, which only a release that no walk declares yet could record:
  - leaving deletion bounds out (D6, think-f2io) records #732’s 985, 8 of the author’s
    `1851c2c` files (367, 406, 541, 542, 588, 589, 638 and 847), `8a488a1`’s file at 848,
    and Couzo’s `5a299b4` index at 8 counts;
  - leaving constructions with no certificate file out (D2, think-f2io) records 24 of the
    `1851c2c` files, `8a488a1`’s at 849, and `5a299b4` at 37 counts;
  - the withdrawn files are out of the record already, and leaving them out of the walk
    records nothing of the author’s.
- **The 5,078 above 1024** wait on the owner (D1, think-f2io).
  On 23 October the owner answered that rows above 1024 are tracked; think-llit applies
  the answer.
- **The 126 in the corpus** are not part of the issue, and none is new (the triage, in
  think-0gp6).
- **The saturation argument** is prose and bounds no s(n); the author’s comment of
  2026-10-23T01:52:47Z says no lower bound is claimed at counts that are not squares.

## Credit

The manifest credits every row to “Mishapolk / Mykhailo Polkovskyi (exact certified
macro-layout)”.
His comment on #732
([issuecomment-6355486108](https://github.com/jlevy/squares/issues/732#issuecomment-6355486108))
says that 645, 752 and 931 refine Francisco Couzo’s #715 certificates, credited “Francisco
Couzo (seed topology), refined via continuous SQP by Mishapolk”, that 499 refines his own
#719 packing, and that the rest are new arrangements.
#715’s index credits its 931 after Kevin Fang’s rectangle and gluing and PingYou Ltd’s
squares, so the key’s credit is “Polkovskyi after Couzo, Fang, PingYou Ltd”.
The triage measured 645, 752 and 931 pairing one to one with #715’s files.

Each certificate’s header names a source file in his repository (`src=cert_n-M, layers=k,
del=d`): 26 the same count, 44 another count that is one of his #719 rows (409 from
`cert_n-370`, for example), and 7 another of his own files (372 and 411 from `cert_n-335`).
Every file named is at 335 or above, so none is one of #719’s re-solves of this project’s
house packings at 105 and 204, and #719 states no lineage for its rows beyond the corpus.
The source names this project only as its baseline comparison and as the audience of its
ingestion runbook, so the key’s lineage is `independent`.
The source’s README credits the index’s baselines at N ≤ 308 to Gardner, Erdős, Göbel,
Friedman, Ellsworth and Daniel, and 3,734 classical L-border bounds to Frits Göbel; none of
these is one of the 77.
Per-row credit beyond the corpus is the owner’s open question (D5, think-f2io).
Those statements are the source’s.
The issue states no AI assistance.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source mishapolk-issue732-2026-10-22 --check
python -m devtools.beyond_horizon_replay check --issue 732
python -m devtools.beyond_horizon_replay check --issue 732 --replay --workers 2
python -m devtools.beyond_horizon_replay source-history --issue 732 --clone CLONE
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
