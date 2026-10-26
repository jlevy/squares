# Hosono’s Lean Kernel Proof of Valid7, Version 2, Pinned 2026-10-17

This packet pins, by digest, version 2 of Hiroaki Hosono’s Lean kernel proof of Evan
Daniel’s `Valid7`, at
[wand125/square-packing](https://github.com/wand125/square-packing/tree/649a92042b4b79dda1eca1749c34029aee60990e/lean/valid7)
`lean/valid7/`, which the author named on
[#537](https://github.com/jlevy/squares/issues/537) on 18 October 2026. It re-checks
version 1’s theorem, which the [Valid7 packet](../evand-valid7-lean-2026-10-11/README.md)
retains as merged at evand/square-packing `060c1a1`, from the same 9,800 per-root
certificates. The record registers both as `T-249`, a formalization of `T-064`, at
`V0`/`C0`; this version’s bibliography key is **[wand125 Valid7 Lean v2 2026-10-17]**.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing> (Hiroaki Hosono) |
| Revision | `649a92042b4b79dda1eca1749c34029aee60990e`, “lean/valid7: Valid7 in the Lean kernel, version 2”; `lean/valid7/` is unchanged from it to the head `7a47ab9` read on 26 October 2026 |
| Committed | 2026-10-17T23:45:52Z; the commit names Claude as co-author |
| Licence | None stated for the folder: the root `LICENSE.md` says each top-level project folder keeps the licence it was published under and that a folder with no `LICENSE` takes the nearest enclosing folder’s, and neither `lean/` nor the root carries one. Daniel’s library and statement are MIT |
| Retained | nothing: the twelve files of `lean/valid7/` (6,105,616 bytes) and the root `LICENSE.md` are pinned by SHA-256 in [acquisition/upstream-subtree.sha256](acquisition/upstream-subtree.sha256) |

The folder’s `release-assets.sha256` pins the release `valid7-lean-v2`’s assets, none
downloaded here:

| Asset | SHA-256 |
| --- | --- |
| `v7-sources.tar.zst` (345,491,880 bytes) | `dc1d98887bedfef0175d360e32459cbbea4fa3cf58ff76c1c8a674b4358eabec` |
| `v7r-certs.tar.zst` | `c327ff6389b74969ba2f3c359b05a34b5b2407fb5bf6cad4d61ce4b8f3104ccc` |
| `v7r-logs.tar.zst` (2,874,595 bytes) | `c2cec291dd26406fdfa842cb72750932207c3aba15d526164b360ce49b04c7c0` |

## What the Source Reports

From the folder’s `README.md`, read at the pin:

- **The theorems** `valid7`, `bentz` and `validTilt7`, as `expected/statement.txt` states
  them, with `[propext, Classical.choice, Quot.sound]` (`receipts/axioms.log`,
  `expected/axioms.txt`), no `sorry`, no `native_decide`, every generated module a
  `decide +kernel` check.
- **The library** is Daniel’s at wand125 `c5c7f00` (branch `validtilt9-kernel`, the head
  of evand/square-packing PR #8): upstream `3f004b7` with `RowMinN.lean` (new) and a
  `LemmaEKM.lean` that calls it, for kernel speed and with no statement change.
  `library.sha256` lists its 58 files and the three build pins.
- **What changed from version 1.** The same certificates, every file matching its
  `v7cert.sha256` line; 27,703 leaves re-certified with the rows’ minima sub-bins and
  checked in X mode, 302 kept as published (164 roots) and 55 Lemma-K leaves kept;
  leaves merged into one module up to 800 pair theorems, else row groups of 20.
- **The run.** One Google Cloud c4a-highmem-48 Spot VM (48 Arm vCPUs, 376 GB) for 29.4
  hours, 82,233 tasks returning 0:

| Step | Tasks | CPU-hours | Peak memory |
| --- | ---: | ---: | --- |
| re-certification | 9,800 | 19.4 | 0.4 GB |
| writing sources | 9,806 | 0.3 | 0.2 GB |
| leaf modules | 28,061 | 639.3 | 37.0 GB |
| row groups | 24,765 | 127.3 | 35.3 GB |
| root modules | 9,801 | 11.4 | 7.8 GB |
| `Main.lean` | 1 | 0.01 | 50.6 GB |
| `Axioms7.lean` | 1 | 0.01 | 50.6 GB |

The steps sum to 797.7 CPU-hours, the “798” the author’s comment of 18 October gives;
the note on #537 that the comment’s figures did not sum to it is resolved by this table.
`receipts/main.log` records `Main.lean` in 37.81 s wall at 50,618,440 kB resident, exit 0.

## The Root Names

`generated-sources.sha256` lists 62,626 files: `Main.lean`, the root modules
`Sqpack/V7/R00000.lean` to `R09799.lean`, one per root of the run, and 52,825 leaf and
row-group modules under the directories of 5,303 roots. `devtools.audit_valid7_roots`
read it from a checkout held to the digest this packet pins; its receipt is in the
[Valid7 packet](../evand-valid7-lean-2026-10-11/README.md#the-root-names-audited-here).

## What Is Not Established

Nothing here built a module. A full build is about 798 CPU-hours with 37 GB for a leaf
module and 51 GB for `Main.lean`; a sample of roots moves no rung. The choice is the
owner’s (`think-qu37`).

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source wand125-valid7-lean-v2-2026-10-17 --checkout CHECKOUT
python -m devtools.acquire_source wand125-valid7-lean-v2-2026-10-17 --check
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
