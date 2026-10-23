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
It reads only the files whose paths name a count in that range.
It also lists every side the repository published at those counts with the first commit
that held it.

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
- Each is below the standing side by 7.49 × 10⁻¹³ (735) to 7.38 × 10⁻⁴ (752): 6 by less
  than 10⁻¹², 35 by 10⁻¹² to 10⁻⁹, 17 by 10⁻⁹ to 10⁻⁶, and 19 by more.
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

- **499 is recorded and held.** It is 8.66 × 10⁻¹³ below #719’s row, and both round up to
  22.881306218113 at 12 places: a re-certification below the print, which waits on the
  owner’s answer (think-fwa9).
- **The author’s own `1851c2c` files at the nine other withdrawn counts** (411, 451, 494,
  495, 540, 583, 587, 632 and 683) are below every earlier report, and the issue’s files are
  below them.
  The walk records them and holds them for the owner’s question whether a file its author
  withdrew from an issue is a report (think-8m4k).
  No verdict rests on them.
- **The other 312 are not recorded.** 81 restate #719’s rows exactly, and the rest equal or
  lie above an earlier report.
  129 of these verdicts are decided only against publications the walk holds for an owner
  decision (`beyond_horizon_replay.WALKS`):
  - 43 against publications above Göbel’s construction, 369 and 376 among them, above
    Couzo’s `58a7833` bound; each is above Göbel’s construction itself;
  - 41 against constructions with no certificate file;
  - 31 against re-certifications below the print;
  - 14 against index deletion bounds, 985 among them, equal to Couzo’s `4e4c8ce` bound.
    An answer that leaves deletion bounds out would record 985
    (`beyond_horizon_replay held-dependents`).
- **The 5,078 above 1024** wait on the owner (D1, think-f2io).
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
Couzo (seed topology), refined via continuous SQP by Mishapolk”, and that 499 refines his
own #719 packing.
The triage measured 645, 752 and 931 pairing one to one with #715’s files.
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
