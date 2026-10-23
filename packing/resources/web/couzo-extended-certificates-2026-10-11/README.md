# Francisco Couzo’s Four Certificates at f311f08

[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/f311f08901c24b2a6c5f720710a45adec23e926a/certificates) at `f311f08901c24b2a6c5f720710a45adec23e926a` (committed 2026-10-11T03:39:54Z), the parent of issue #506’s pin `337078c`, rewrites certificates beyond the corpus that no issue reports. The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) records four of them as reports with a row: 340, 378, 379 and 380. This packet retains them (think-om5l). `certificates/n340.cert` is byte for byte the copy the [11 October packet](../couzo-certificates-2026-10-11/README.md) retains from `337078c`, which #506 did not name.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json); every file is bound to its Git blob at the pin. [acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest: 6 files, 292,581 bytes, of which 4 are retained (223,855 bytes) under `source/` and the rest pinned by digest with the reason the declaration gives.

The repository states no licence for its data or prose: the tree has no LICENSE, and no README states reuse terms. The four certificates are retained as factual data under the owner decision of 2026-10-09 recorded in resources/web/known-best-packings/README.md (Retained Factual Data). Prose is hash-pinned and not copied.

## Rows Beyond the Corpus

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares this publication a release with no issue, `franciscouzo/square-packing@f311f08`, and reads the rows the history walk records from [acquisition/watched-release.json](acquisition/watched-release.json), which `declare-rows` writes from the walk.

Each certificate was first committed at the commit itself ([receipts/first-commits.json](receipts/first-commits.json)).

**All four are verified.** The filtered two-route decision of `devtools.couzo_678_replay`, reused unchanged, accepts every packing on both routes (3,369 candidate pairs of 272,524, and every corner against every wall), and every side is its header side rounded up at 12 places. **All 24 controls are refused by both routes.** The positive decisions took 2.1 CPU seconds ([receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json)). No square touches the box and no pair touches: every wall clears by at least $5.00 \times 10^{-21}$ and every pair by at least $1.00 \times 10^{-20}$. Every side is below Göbel’s classical construction at its count ([receipts/goebel-comparison.json](receipts/goebel-comparison.json)).

The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) walks every count from 325 to 1024 in report order from starts frozen at `main` `a97b712b9` and records all four. **One is current**, at 340. **Three are superseded on entry**, by Couzo’s #506 (337078c). The rows supersede first Couzo’s 02f9690 (2) and Couzo’s 3ef7634 (1); at one count no row stood before them.

[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the record the source register reads them from, as the source `couzo-extended-certificates-2026-10-11`.

## Held Back

The walk records the commit’s 376 too and holds it back from a row: it is above Göbel’s construction at 376 (#613, think-8krd), pinned by digest here.

## Credit

The commit names no per-count credit; the certificates are Francisco Couzo’s own constructions and searches.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-extended-certificates-2026-10-11 --check
python -m devtools.beyond_horizon_replay check --issue franciscouzo/square-packing@f311f08
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
