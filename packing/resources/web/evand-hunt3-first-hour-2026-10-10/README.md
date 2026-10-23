# Evan Daniel’s Hunt 3 First Hour: the 343 Certificate at f7a2325

[evand/square-packing](https://github.com/evand/square-packing/tree/f7a2325df1e396f46ee373c6d00a880795b749b7/search/packer/candidates) at `f7a2325df1e396f46ee373c6d00a880795b749b7` (committed 2026-10-10T09:15:50Z, “packer: Hunt 3 first hour”) publishes `search/packer/candidates/hunt3_n343.dil.cert`, a dilated rational certificate at 343, five hours before the Hunt 3 certificates the [76a529bc packet](../evand-record-hunt3-2026-10-10/README.md) retains. No issue reports it. The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) records it as a report with a row; this packet retains it with the repository’s MIT licence.

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json); every file is bound to its Git blob at the pin. [acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest: 3 files, 60,699 bytes, of which 2 are retained (54,424 bytes) under `source/` and the rest pinned by digest with the reason the declaration gives.

MIT License, Copyright (c) 2026 Evan Daniel (LICENSE, retained). The certificate is retained under it.

## Rows Beyond the Corpus

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares this publication a release with no issue, `evand/square-packing@f7a2325`, and reads the rows the history walk records from [acquisition/watched-release.json](acquisition/watched-release.json), which `declare-rows` writes from the walk.

Each certificate was first committed at the commit itself ([receipts/first-commits.json](receipts/first-commits.json)).

**It is verified.** The filtered two-route decision of `devtools.couzo_678_replay`, reused unchanged, accepts every packing on both routes (821 candidate pairs of 58,653, and every corner against every wall), and every side is its header side rounded up at 12 places. **All six controls are refused by both routes.** The positive decisions took 0.6 CPU seconds ([receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json)). No square touches the box and no pair touches: every wall clears by at least $6.02 \times 10^{-13}$ and every pair by at least $1.21 \times 10^{-12}$. Every side is below Göbel’s classical construction at its count ([receipts/goebel-comparison.json](receipts/goebel-comparison.json)).

The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) walks every count from 325 to 1024 in report order from starts frozen at `main` `a97b712b9` and records it. **It is superseded on entry**, by Evan Daniel’s Hunt 3 (76a529bc). It supersedes first the row of Kevin Fang’s two-wedge certificates of 10 October (fang-two-wedge-certificates-2026-10-10).

[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the record the source register reads them from, as the source `evand-hunt3-first-hour-2026-10-10`.

## Held Back

Nothing else of the commit is held at 325 to 1024.

## Credit

Evan Daniel’s Hunt 3, grown from Kevin Fang’s two-wedge packings of #484, as the 76a529bc packet records; the source discloses Claude assistance.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source evand-hunt3-first-hour-2026-10-10 --check
python -m devtools.beyond_horizon_replay check --issue evand/square-packing@f7a2325
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
