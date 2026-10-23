# Kevin Fang’s Composites at bef5c42: 703 and 994

[TheSnakeFang/squarepack-certs](https://github.com/TheSnakeFang/squarepack-certs/tree/bef5c42d58257fe38ed010a5d1ff9b8fc608df57/composites) at `bef5c42d58257fe38ed010a5d1ff9b8fc608df57` (committed 2026-10-12T19:13:41Z, “Composites: best j per n for 27 ≤ n ≤ 64”) publishes composite certificates at 703 and 994 and `composites/table.csv`, the side of every composite it lists rounded up at 15 places. No issue reports them. The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) records the two certificates as reports with a row; this packet retains them. The [14 October packet](../couzo-certificates-2026-10-14/README.md) retains byte-identical copies under `submissions/2026-10-14/certificates/`, where issue #607 reported them two days later.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json); every file is bound to its Git blob at the pin. [acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest: 6 files, 429,873 bytes, of which 4 are retained (379,958 bytes) under `source/` and the rest pinned by digest with the reason the declaration gives.

MIT License, Copyright (c) 2026 Kevin Fang (LICENSE, retained), for verify.py and the tools; ATTRIBUTION.md (retained) releases the certificates, text files and drawings in the nNNNN folders under CC0 1.0 and does not name composites/. The two composite certificates are retained as factual data under the owner decision of 2026-10-09 recorded in resources/web/known-best-packings/README.md (Retained Factual Data); the copies the couzo-certificates-2026-10-14 packet retains under submissions/2026-10-14/certificates/ are byte-identical. The source discloses that the search, the verifier and the bundle were written and run with Claude (Anthropic), directed and reviewed by Kevin Fang.

## Rows Beyond the Corpus

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares this publication a release with no issue, `TheSnakeFang/squarepack-certs@bef5c42`, and reads the rows the history walk records from [acquisition/watched-release.json](acquisition/watched-release.json), which `declare-rows` writes from the walk.

Each certificate was first committed at the commit itself ([receipts/first-commits.json](receipts/first-commits.json)).

**Both are verified.** The filtered two-route decision of `devtools.couzo_678_replay`, reused unchanged, accepts every packing on both routes (3,762 candidate pairs of 740,274, and every corner against every wall), and every side is its header side rounded up at 12 places. **All 12 controls are refused by both routes.** The positive decisions took 3.0 CPU seconds ([receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json)). No square touches the box and no pair touches: every wall clears by at least $2.71 \times 10^{-20}$ and every pair by at least $5.42 \times 10^{-20}$. Every side is below Göbel’s classical construction at its count ([receipts/goebel-comparison.json](receipts/goebel-comparison.json)).

The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) walks every count from 325 to 1024 in report order from starts frozen at `main` `a97b712b9` and records both. **Both are superseded on entry**, by Couzo’s 4e4c8ce. 

[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the record the source register reads them from, as the source `fang-composites-2026-10-12`.

## Held Back

The walk records 17 rows of `composites/table.csv` with no certificate file of their own and holds each back from a row, as a composite bound with no certificate file of its own (D2, think-f2io); the table is pinned by digest here.

## Credit

Kevin Fang’s composites of the two-wedge family of Arslanov, Mustafin and Shangitbayev, as `ATTRIBUTION.md` says; the source discloses Claude assistance.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source fang-composites-2026-10-12 --check
python -m devtools.beyond_horizon_replay check --issue TheSnakeFang/squarepack-certs@bef5c42
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
