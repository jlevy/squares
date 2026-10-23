# Francisco Couzo’s Intermediate Certificates at 93570ef

[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/93570ef79474fd8c35d1293addf095f9eee6a658/certificates) at `93570ef79474fd8c35d1293addf095f9eee6a658` (committed 2026-10-12T21:31:43Z, “Track search implementation and retain only current certificates”) publishes certificates at 344 and 378 between the `0fa0e0d` and `4596670` certificates. No issue reports them. The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) records both as reports with a row; this packet retains them.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json); every file is bound to its Git blob at the pin. [acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest: 4 files, 178,901 bytes, of which 2 are retained (110,843 bytes) under `source/` and the rest pinned by digest with the reason the declaration gives.

The repository states no licence for its data or prose: the tree has no LICENSE, and no README states reuse terms. The certificates are retained as factual data under the owner decision of 2026-10-09 recorded in resources/web/known-best-packings/README.md (Retained Factual Data). Prose is hash-pinned and not copied.

## Rows Beyond the Corpus

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares this publication a release with no issue, `franciscouzo/square-packing@93570ef`, and reads the rows the history walk records from [acquisition/watched-release.json](acquisition/watched-release.json), which `declare-rows` writes from the walk.

Each certificate was first committed at the commit itself ([receipts/first-commits.json](receipts/first-commits.json)).

**Both are verified.** The filtered two-route decision of `devtools.couzo_678_replay`, reused unchanged, accepts every packing on both routes (1,639 candidate pairs of 130,249, and every corner against every wall), and every side is its header side rounded up at 12 places. **All 12 controls are refused by both routes.** The positive decisions took 1.0 CPU seconds ([receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json)). No square touches the box and no pair touches: every wall clears by at least $5.00 \times 10^{-21}$ and every pair by at least $1.00 \times 10^{-20}$. Every side is below Göbel’s classical construction at its count ([receipts/goebel-comparison.json](receipts/goebel-comparison.json)).

The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) walks every count from 325 to 1024 in report order from starts frozen at `main` `a97b712b9` and records both. **Both are superseded on entry**, by Couzo’s b85dee2 (1) and Couzo’s 4596670 (1). The rows supersede first Couzo’s 0fa0e0d (2).

[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the record the source register reads them from, as the source `couzo-retained-certificates-2026-10-12`.

## Held Back

The walk records the commit’s 375 too and holds it back from a row: it is above Göbel’s construction (#613, think-8krd), pinned by digest here.

## Credit

The per-count JSON names a hop search from Francisco Couzo’s own L-border and deletion construction at each count.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-retained-certificates-2026-10-12 --check
python -m devtools.beyond_horizon_replay check --issue franciscouzo/square-packing@93570ef
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
