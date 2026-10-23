# Hosono’s Hypothesis-Free Lean Proof of the Point-Only s(21) = 5, Pinned 2026-09-29

This packet pins the Lean proof that
[wand125/square-packing-bounds](https://github.com/wand125/square-packing-bounds) added on
29 September 2026 under `point_n21_L5/lean/zero-margin/`:
`theorem SquarePacking.n21pts_eq_5 : minSide 21 = 5`, with no hypothesis.
It removes the one hypothesis of the conditional overlay that the
[28 September packet](../wand125-point-and-mixed-2026-09-28/README.md) retains for
`T-055`, the point-only route to $s(21) = 5$: there the capture bound was an assumption
decided by the source’s rational replay, and here it is checked in Lean’s kernel by a
zero-margin box tree.

Its proposed Frontier key is **[wand125 n21 zero-margin Lean 2026-09-29]**. No issue
asked for it: the triage of wand125/square-packing-bounds at `1a25a5ed` found it, and
bead `think-f2bm` owns its import. The record registers it as `T-234`, a formalization of
`T-055`’s route, at `V0`/`C0`. The claim below is stated as the source states it; nothing
here has built the proof, and no review has read it yet.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing-bounds>, archived on 7 October 2026 at `069f3276`; its content moved to [wand125/square-packing](https://github.com/wand125/square-packing) |
| Revision | `77636c63f45a90d9a829417a1722a3bf9bfef37d`, tree `6da862fd75935a1cd309c7d9c5dd6716561d15b9`, the commit that adds `point_n21_L5/lean/zero-margin/` (“Hypothesis-free Lean proof of the point-only s(21) = 5”) |
| Committed | 2026-09-29T07:16:17Z (16:16:17 by the author’s clock, `+09:00`), authored the same second, by Hiroaki Hosono |
| Licence | MIT, “Copyright (c) 2026 wand125” (root `LICENSE`). `point_n21_L5/UPSTREAM-LICENSE.txt` is Evan Daniel’s MIT licence for the derived support and for the Lean library and generator the build fetches |
| Retrieved | 2026-10-23T06:23Z, a blobless clone of the single branch with a sparse checkout of the pin |
| Pinned subtree | 11 files, 155,710 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 8 files, 58,529 bytes, byte-identical under [`square-packing-bounds/`](square-packing-bounds/) |

None of the eleven files changes from the pin to the archived head `069f3276`
(`git log 77636c63..069f3276` over them is empty). The moved copy at
wand125/square-packing `e48de243`,
`problems/square-lower-bounds/point_n21_L5/lean/zero-margin/`, holds four of the five
files with the same blobs and lacks `data-sha256.txt`, the list the build compares its
generated tree with, so the archived repository is the one that holds the whole proof.

## Credit and AI Assistance, as the Source States Them

The zero-margin README says the proof “follows Evan Daniel’s zero-margin route, which he
used for `s(13) = 4` and `s(32) = 6`”, and that “Only `N21PtsLower.lean`, the axiom
report and the build script are ours. The Lean library and the generator are fetched
from evand/square-packing at the pinned commit `6aa82ba457e9eaeaaa3af0833600f27f91a2fce3`
(MIT …)”. The certificate is Hosono’s re-weighting of Daniel’s `s(21)` support, as the
28 September packet records; the root README at the pin says parts of the work were
produced with AI assistance under human direction, and the `s(21)` write-up that its
code was developed with Codex.

## What Is Retained

Retained byte-identical at their upstream paths:

- **`point_n21_L5/lean/zero-margin/`** whole: `N21PtsLower.lean` (the two theorems),
  `N21PtsAxiomsZ.lean` (the `#print axioms` probe), `build_zero_margin.sh` (the build
  recipe), `data-sha256.txt` (the SHA-256 of the 66 generated files) and `README.md`;
- the three READMEs the commit changed: the root `README.md`, `point_n21_L5/README.md`
  and `point_n21_L5/lean/README.md`.

Pinned by digest only, each retained byte-identical elsewhere:

| Upstream path | Bytes | SHA-256 | Retained in |
| --- | ---: | --- | --- |
| `LICENSE` | 1,064 | `c0dd43e7892932c8…` | [27 September rectangle packet](../wand125-rectangle-certificates-2026-09-27/README.md) |
| `point_n21_L5/UPSTREAM-LICENSE.txt` | 1,068 | `c51886c0f7e6724a…` | [28 September packet](../wand125-point-and-mixed-2026-09-28/README.md) |
| `point_n21_L5/certificates/n21-capture-one.txt` | 95,049 | `9f631fbae420e0376ea636a232b7680e937deebe205dc035cfb9c43a3d74b456` | [28 September packet](../wand125-point-and-mixed-2026-09-28/README.md), as gzip; unchanged since `b97c7963` |

[`acquisition/sources.json`](acquisition/sources.json) records the pin and every file.
From `packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source wand125-n21-zero-margin-lean-2026-09-29 --checkout CHECKOUT`
rebuilds the retained files and both acquisition files from a checkout at the pin, and
`--check` in place of `--checkout CHECKOUT` re-derives the packet without one.

**What the build also needs, from evand/square-packing at `6aa82ba4`.** The build script
clones Daniel’s repository at that commit and checks the SHA-256 of three of its files
and of the certificate. Every file the proof needs from that commit is already retained
here byte for byte, which
[`receipts/evand-library-closure-6aa82ba4.json`](receipts/evand-library-closure-6aa82ba4.json),
written by `devtools.lean_closure`, makes checkable:

- the nine library modules of the closure of `Sqpack.ZMTree`, `BoxTree` and `S32`
  (`Basic`, `Chord`, `ZeroMargin`, `D4`, `Cover`, `S32Data`, `S32`, `BoxTree` and
  `ZMTree`, 690,686 bytes, no `sorry`, `axiom`, `native_decide` or other kernel escape
  in their code) and the three build pins (`leanprover/lean4:v4.33.1`, Mathlib
  `0df444a3`), in the [26 September](../evand-square-packing-2026-09-26/README.md),
  [28 September](../evand-square-packing-2026-09-28/README.md) and
  [3 October](../evand-square-packing-2026-10-03/README.md) evand packets and the
  [7 October packet](../evand-exact-and-local-reports-2026-10-07/README.md);
- the generator `s12/lean/scripts/gen_zmtree.py` (SHA-256 `e6e1d477…`, the
  `GEN_SHA256` the script pins) in the 28 September evand packet, its oracle
  `s12/search/zeromargin.py` (`640fe453…`, `ORACLE_SHA256`) in the
  [1 October evand packet](../evand-square-packing-2026-10-01/README.md), and
  `ZMTree.lean` (`8c23911b…`, `ZMTREE_SHA256`).

The four digests the script pins were recomputed here from the blobs at `6aa82ba4` and
from the retained certificate, and agree.

## The Claim, as the Source States It

`N21PtsLower.lean` proves, in namespace `SquarePacking`,

```lean
theorem n21pts_ge_5 : (5 : ℝ) ≤ minSide 21
theorem n21pts_eq_5 : minSide 21 = 5
-- depends on axioms: [propext, Classical.choice, Quot.sound]   (the README)
```

where `minSide n = sInf {s | Packs n s}` and `Packs n s` says that $n$ closed unit
squares, each translated and rotated, lie in $[0,s]^2$ with pairwise disjoint interiors
(`S32.lean` at `6aa82ba4`, the definitions the kernel build of `T-006`’s $s(13) = 4$
used).

- **The certificate** is `n21-capture-one.txt`, the point-only cover renormalised to
  capture threshold 1: 4,604 entries of $[0,5]^2$ with weights $w/999948000000$ and
  total $20998900000168/999948000000 = 20.9999919997\ldots < 21$, such that every
  closed unit square in $[0,5]^2$ captures weight at least 1. It is not the
  `n21-original.txt` of `T-055`’s replay, at threshold $q = 249987/250000$; the theorem
  is the same.
- **The lower bound** is Daniel’s `BoxTree.le_minSide` applied to a zero-margin box tree
  over the D4 roots, which his `gen_zmtree.py` (untrusted, deterministic) generates as
  `Sqpack/N21PtsZ/`: 59,433 `Z` leaves (22,016 ADM, 13,526 one-chain, 23,891 two-chain),
  5,876 `E` leaves and 5,591 clips, in 2,076 chunks over 64 files. Each chunk is one
  `decide +kernel` of `ZMTree.check`, proved sound once (`ZMTree.sound`). The 66
  generated files, about 88 MB, are not in the tree; `data-sha256.txt` lists their
  SHA-256.
- **The upper bound** is the $5 \times 5$ grid (`packs_grid`), and `n21pts_eq_5` closes
  with `csInf_le` and `le_antisymm`.

**The source’s run.** On an Apple M4 under heavy unrelated load: generation 1,459 s wall
with 6 workers, and the kernel check about 3.5 h wall with 2 parts at a time, peaking
near 6 GB per part. It reports an end-to-end run of `build_zero_margin.sh` from an empty
directory whose regenerated data matched `data-sha256.txt` and which ended
`N21_POINTS_HYPOTHESIS_FREE_VERIFIED`. No build log or axiom output is published.

## The Build Plan, Priced

`sh build_zero_margin.sh WORK 1 2` from the retained directory, with the clone of
`6aa82ba4` it makes replaced by the retained library files (the runbook’s rule for a
script that fetches), then `lake env lean N21PtsAxiomsZ.lean`, accepted only with
`[propext, Classical.choice, Quot.sound]` for `n21pts_eq_5`.

| Item | Estimate |
| --- | --- |
| Toolchain | `leanprover/lean4:v4.33.1` and Mathlib `0df444a3`’s cache, about 2.5 GB and 7 GB on disk; Python 3 with NumPy for the generator |
| Generation | about 2.4 CPU-hours (1,459 s × 6 workers on the M4) |
| Kernel check | about 7 CPU-hours (3.5 h × 2 parts on the M4, under load) |
| Total | 6 to 12 CPU-hours, central 9, from the source’s report; not a receipt |
| Memory | near 6 GB per part: one part at a time fits a 15 GB host; two, about 12 GB, leave little headroom on it |

It is under the owner’s 40 CPU-hour item cap and above the 2 CPU-hour single run this
lane may start, and this host had 5.2 GB of free disk on 23 October, short of the
toolchain and cache. It is held for a lane with the disk, as the import bead records.
What it would add: a `proof-assistant-checked`, `replayed-here` route for `T-234` with its
own axiom receipt, the road to `T-055`’s rung 5 that the
[review of 11 October](../../../../docs/project/reviews/review-2026-10-11-lean-backed-rungs.md)
(LR-9) names.

## Limitations

- **Nothing was built or run here.** The axiom set and the end-to-end run are the
  source’s report.
- **The generated tree is not published.** The proof is the 64 generated parts; a
  rebuild regenerates them with Daniel’s generator, and the kernel checks whatever it
  writes, so the generator is untrusted by design.
- **No review has read it.** The mathematical review of stage 4 starts from this packet.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
