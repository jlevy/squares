# Francisco Couzo’s Index of 15 October: 253 Certificates at 4e4c8ce

[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/4e4c8ce23cb5e87f033021687010992c40575480/certificates/best) at `4e4c8ce23cb5e87f033021687010992c40575480` (committed 2026-10-15T00:31:53Z, “Update all verified bounds for n < 1024”) rewrites Francisco Couzo’s index for every count below 1024: `certificates/best/nN.cert` at every count the grid does not hold, `manifest.json` naming each count’s credit and the author’s two checker outcomes, `upper_bounds.json` and `certified_bounds.json`. No issue reports it. It is a publication in a watched repository, a report from its commit (the owner, 14 October 2026), and the [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) records 253 of its certificates beyond the n ≤ 324 corpus as reports with a row. This packet retains those 253 (think-yfoo).

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json); every file is bound to its Git blob at the pin. [acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest: 304 files, 56,851,346 bytes, of which 253 are retained (42,694,658 bytes) under `source/` and the rest pinned by digest with the reason the declaration gives.

The repository states no licence for its data or prose: the tree has no LICENSE, and no README states reuse terms. The 253 certificates are retained as factual data under the owner decision of 2026-10-09 recorded in resources/web/known-best-packings/README.md (Retained Factual Data). verify_bound_certificate.py states that it is Evan Daniel’s MIT-licensed verifier with modifications by Francisco Couzo with Codex, under the MIT licence in BOUND_VERIFIER_LICENSE.txt (Copyright (c) 2026 Evan Daniel); both are pinned against the byte-identical copies the couzo-issue678-2026-10-18 packet retains. Prose, the indexes and the manifest are hash-pinned and not copied.

## Rows Beyond the Corpus

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares this publication a release with no issue, `franciscouzo/square-packing@4e4c8ce`, and reads the rows the history walk records from [acquisition/watched-release.json](acquisition/watched-release.json), which `declare-rows` writes from the walk.

Each certificate was first committed at the commit itself ([receipts/first-commits.json](receipts/first-commits.json)).

**All 253 are verified.** The filtered two-route decision of `devtools.couzo_678_replay`, reused unchanged, accepts every packing on both routes (364,009 candidate pairs of 60,910,803, and every corner against every wall), and every side is its header side rounded up at 12 places. **All 1518 controls are refused by both routes.** The positive decisions took 333.2 CPU seconds ([receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json)). No square touches the box and no pair touches: every wall clears by at least $5.00 \times 10^{-25}$ and every pair by at least $1.00 \times 10^{-24}$. Every side is below Göbel’s classical construction at its count ([receipts/goebel-comparison.json](receipts/goebel-comparison.json)).

The maintained all-pairs kernel of `devtools.evand_arrangement_reports`, every pair and no filter, decided the positives at 366, the row with the release’s least pair gap, $10^{-24}$, and 703, a glued composite with a binary-fraction side: 313,548 pairs in 117.7 CPU seconds, both routes accepting each, and each least pair gap and wall clearance equal, exactly, to the filtered decision’s ([receipts/exhaustive-sample.json](receipts/exhaustive-sample.json)).

The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) walks every count from 325 to 1024 in report order from starts frozen at `main` `a97b712b9` and records all 253. **91 are current**. **162 are superseded on entry**, by Couzo’s #670 (55), Mykhailo Polkovskyi’s #719 (38), Couzo’s #715 (20), Darius Muglich’s #686 (16), Couzo’s 5a299b4 (10), Couzo’s #678 (9), Couzo’s #672 (5), Couzo’s #675 (4), Couzo’s 23aff0c (4) and Joost de Winter’s #666 (1). The rows supersede first Couzo’s 487b058 (199), Couzo’s #607 (43ac7d2) (7), Kevin Fang’s bef5c42 (2), Couzo’s b85dee2 (1), Couzo’s 8 October decimal row (1), Evan Daniel’s 622cd2e composition (1) and Kevin Fang’s 078789a4 theorem (1); at 41 counts no row stood before them.

[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the record the source register reads them from, as the source `couzo-index-2026-10-15`.

## Held Back

The walk records the commit’s 39 bounds `upper_bounds.json` states by deleting squares from the next count’s certificate, with no certificate file at their own count, 743 and 985 among them, which #715 restates. By the owner’s answer of 23 October 2026 on D6 (think-f2io) each is an earlier report, so a later side equal to it is not recorded, and the index covers it with no row of its own; whether an issue’s claim at 743 or 985 gives one a row is think-kzme. By the owner’s answers of 23 October 2026 it does not record the commit’s publications at 50 more counts: 47 certificates above Göbel’s classical construction at their count, an earlier report (#613, think-8krd), pinned by digest here, and 3 re-certifications below the side they beat by less than 10⁻¹² with the same 12-place print, at 327, 332 and 542, which restate those reports (think-fwa9).

## Credit

`manifest.json`, pinned by digest, credits each count. Of the 253 rows it credits Francisco Couzo at 200 (local search, the ct105 campaign and constructions from his own certificates), PingYou Ltd’s pieces at 40 (constructions from PingYou Ltd’s certificates), Kevin Fang’s rectangles and gluing at 8 (with PingYou Ltd’s square input at 7 and Couzo’s at 1) and Evan Daniel at 5. Those statements are the source’s; this packet establishes none. The source discloses OpenAI Codex assistance.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-index-2026-10-15 --check
python -m devtools.beyond_horizon_replay check --issue franciscouzo/square-packing@4e4c8ce
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
