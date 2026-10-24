# Francisco Couzo’s Intermediate Certificate at a7067d7

[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/a7067d7b92b1e0208499b26d93e898648f0e8667/certificates) at `a7067d7b92b1e0208499b26d93e898648f0e8667` (committed 2026-10-12T17:55:52Z, “results: n = 156, 176, 237, 271 improved; n > 324 updates”) publishes a certificate at 344 half an hour before the `0fa0e0d` certificates of the [12 October packet](../couzo-certificates-2026-10-12/README.md). No issue reports it. The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) records it as a report with a row; this packet retains it. Three of the commit’s other sides are the 12 October source’s rows, which the walk dates from this commit.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json); every file is bound to its Git blob at the pin. [acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest: 3 files, 127,682 bytes, of which 1 are retained (43,282 bytes) under `source/` and the rest pinned by digest with the reason the declaration gives.

The repository states no licence for its data or prose: the tree has no LICENSE, and no README states reuse terms. The certificates are retained as factual data under the owner decision of 2026-10-09 recorded in resources/web/known-best-packings/README.md (Retained Factual Data). Prose is hash-pinned and not copied.

## Rows Beyond the Corpus

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares this publication a release with no issue, `franciscouzo/square-packing@a7067d7`, and reads the rows the history walk records from [acquisition/watched-release.json](acquisition/watched-release.json), which `declare-rows` writes from the walk.

Each certificate was first committed at the commit itself ([receipts/first-commits.json](receipts/first-commits.json)).

**It is verified.** The filtered two-route decision of `devtools.couzo_678_replay`, reused unchanged, accepts every packing on both routes (814 candidate pairs of 58,996, and every corner against every wall), and every side is its header side rounded up at 12 places. **All six controls are refused by both routes.** The positive decisions took 0.5 CPU seconds ([receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json)). No square touches the box and no pair touches: every wall clears by at least $1.00 \times 10^{-15}$ and every pair by at least $1.20 \times 10^{-12}$. Every side is below Göbel’s classical construction at its count ([receipts/goebel-comparison.json](receipts/goebel-comparison.json)).

The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) walks every count from 325 to 1024 in report order from starts frozen at `main` `a97b712b9` and records it. **It is superseded on entry**, by Couzo’s 0fa0e0d. It supersedes first the row of Couzo’s #506 (337078c).

[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the record the source register reads them from, as the source `couzo-updates-2026-10-12`.

## Held Back

The commit’s 375 is above Göbel’s construction there, an earlier report by the owner’s answer of 23 October 2026 (#613, think-8krd), so the walk does not record it; it is pinned by digest here.

## Credit

The commit names no per-count credit for 344; it is Francisco Couzo’s own certificate.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-updates-2026-10-12 --check
python -m devtools.beyond_horizon_replay check --issue franciscouzo/square-packing@a7067d7
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
