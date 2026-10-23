# Francisco Couzo’s Reconciliation of 20 October: 20 Certificates at 5a299b4

[franciscouzo/square-packing](https://github.com/franciscouzo/square-packing/tree/5a299b4708ab1ae4870d0fc1ab155738144f6ab8/certificates) at `5a299b4708ab1ae4870d0fc1ab155738144f6ab8` (committed 2026-10-20T22:35:41Z, “Reconcile packing bounds through 10000 and current record claims”) reconciles Francisco Couzo’s bounds through n = 10000. It reached GitHub in the push of 2026-10-21T22:56:37Z with `d09edd7` and `6b7391d`, after issue #715, and is dated by that push (`PUSHED_LATER`). No issue reports it. The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) records 20 of its root certificates beyond the n ≤ 324 corpus at or below 1024 as reports with a row; this packet retains them (think-tmwt).

## Retained Here

`devtools.acquire_source` wrote the packet from a sparse checkout of the pin, from the declaration in [acquisition/declaration.json](acquisition/declaration.json); every file is bound to its Git blob at the pin. [acquisition/sources.json](acquisition/sources.json) is the acquisition record and [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) the manifest: 69 files, 29,807,378 bytes, of which 20 are retained (2,538,321 bytes) under `source/` and the rest pinned by digest with the reason the declaration gives.

The repository states no licence for its data or prose: the tree has no LICENSE, and no README states reuse terms. The 20 certificates are retained as factual data under the owner decision of 2026-10-09 recorded in resources/web/known-best-packings/README.md (Retained Factual Data). verify_bound_certificate.py and BOUND_VERIFIER_LICENSE.txt are pinned against the byte-identical copies the couzo-issue678-2026-10-18 packet retains under the MIT licence. Prose, the indexes and the manifest are hash-pinned and not copied.

## Rows Beyond the Corpus

[`devtools.beyond_horizon_replay`](../../../devtools/beyond_horizon_replay.py) declares this publication a release with no issue, `franciscouzo/square-packing@5a299b4`, and reads the rows the history walk records from [acquisition/watched-release.json](acquisition/watched-release.json), which `declare-rows` writes from the walk.

Each certificate was first committed at the commit itself ([receipts/first-commits.json](receipts/first-commits.json)).

**All 20 are verified.** The filtered two-route decision of `devtools.couzo_678_replay`, reused unchanged, accepts every packing on both routes (33,207 candidate pairs of 5,694,934, and every corner against every wall), and every side is its header side rounded up at 12 places. **All 120 controls are refused by both routes.** The positive decisions took 26.3 CPU seconds ([receipts/filtered-exact-replay.json](receipts/filtered-exact-replay.json)). 17 touch the box and 17 have touching pairs, which the closed contract allows. Every side is below Göbel’s classical construction at its count ([receipts/goebel-comparison.json](receipts/goebel-comparison.json)).

The maintained all-pairs kernel of `devtools.evand_arrangement_reports`, every pair and no filter, decided the positive at 903, a current row whose squares touch the box and each other: 407,253 pairs in 76.1 CPU seconds, both routes accepting it, and its least pair gap and wall clearance, both zero, equal, exactly, to the filtered decision’s ([receipts/exhaustive-sample.json](receipts/exhaustive-sample.json)).

The [history walk of 22 October](../../../campaign/issue-intake/upper-bounds-couzo-history-20261022/README.md) walks every count from 325 to 1024 in report order from starts frozen at `main` `a97b712b9` and records all 20. **Nine are current**, at 487, 532, 579, 628, 679, 732, 787, 844, 903. **11 are superseded on entry**, by Mykhailo Polkovskyi’s #719. The rows supersede first Couzo’s 4e4c8ce (10), Darius Muglich’s #686 (9) and Couzo’s #607 (43ac7d2) (1).

[acquisition/beyond-horizon-rows.json](acquisition/beyond-horizon-rows.json) is the record the source register reads them from, as the source `couzo-reconcile-2026-10-20`.

## Held Back

The walk records the commit’s publications at 32 more counts and holds each back from a row: 31 re-certifications below the side they beat by less than 10⁻¹² with the same 12-place print (think-fwa9), 11 certificate files, pinned by digest here, and 20 L-border bounds of its index; and 331, above Göbel’s construction (think-8krd). Issue #715’s 30 re-certifications, whose files the commit also holds, are #715’s, which reported them two hours earlier; they are pinned here against the couzo-issue715-2026-10-21 packet’s identical copies. The index’s bounds above 1024 wait on the owner (D1, think-f2io).

## Credit

The per-count JSON beside each certificate, pinned by the commit, credits Darius Muglich’s packings at 453, 649, 810, 812, 933, 934, 990, 991 and 997, with his original seed and construction credits, Couzo with Evan Daniel’s seed or construction at the nine current counts (487, 532, 579, 628, 679, 732, 787, 844 and 903), and Couzo alone at 409 and 450. Those statements are the source’s. The source discloses OpenAI Codex assistance.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source couzo-reconcile-2026-10-20 --check
python -m devtools.beyond_horizon_replay check --issue franciscouzo/square-packing@5a299b4
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
