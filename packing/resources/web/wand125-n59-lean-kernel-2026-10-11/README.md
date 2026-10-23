# Hosono’s Lean Kernel Proof of s(59) = 8, Pinned 2026-10-11

This packet pins the Lean proof that
[wand125/square-packing](https://github.com/wand125/square-packing) added on 11 October
2026 under `problems/square-lower-bounds/certificates/k2m5_n59_L8/lean/`:
`theorem SquarePacking.s59_eq_8 : minSide 59 = 8`, with no hypothesis, from Hiroaki
Hosono’s mixed cover of 1 October on Evan Daniel’s mixed-measure checker in Lean. The
record holds $s(59) = 8$ as `T-066`, on a complete replay here of Daniel’s `zmx2` over
the same cover, and its claim says the cover “has no Lean statement”. This is a
proof-assistant route to the lower half.

Its proposed Frontier key is **[wand125 n59 Lean kernel 2026-10-11]**. No issue asked
for it: the intake read of 11 October found it (`think-q655`), and bead `think-xk3f`
owns its import; it is tracked on GitHub by
[jlevy/squares#536](https://github.com/jlevy/squares/issues/536) and
[#544](https://github.com/jlevy/squares/issues/544). It is new evidence for `T-066`, not
a new result. The claim below is stated as the source states it; nothing here has built
the proof, and no review has read it yet.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing>, which took in wand125/square-packing-bounds and the author’s other repositories on 7 October |
| Revision | `f9a77b7d38fd60144b78fe290c94f841ab626156`, tree `cda8dd92993281faea93fa69fdc17e297924b630`, the commit that adds `lean/` (“k2m5_n59_L8: add Lean kernel proof of s(59) = 8”) |
| Committed | 2026-10-11T01:42:37Z (10:42:37 by the author’s clock, `+09:00`), by Hiroaki Hosono; the commit names Claude as co-author |
| Licence | MIT, “Copyright (c) 2026 wand125” (`problems/square-lower-bounds/LICENSE`; the root `LICENSE.md` says each folder keeps the licence it was published under). Daniel’s Lean library is MIT |
| Retrieved | 2026-10-23T06:23Z, a blobless clone of the single branch, head `e48de243`, with a sparse checkout of the pin |
| Pinned subtree | 21 files, 6,988,274 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | 13 files, 2,618,860 bytes, byte-identical under [`square-packing/`](square-packing/), one of them an upstream gzip kept as published ([Original Gzip Files](#original-gzip-files)) |

The cover is not in the tree at the pin: the directory’s `ASSET.json` names it as a
release asset (`square-lower-bounds-v1`), as the repository’s README says of all
certificate data. The [1 October packet](../wand125-point-and-mixed-2026-10-01/README.md)
retains `n59_mixed_cover_8.txt` from wand125/square-packing-bounds `1a25a5ed`, and its
decompressed SHA-256 is `6f4d2b64f9a88ae49546f05fa28752382f9ebfa8b7f8b6e6c6f1a8e693177e19`,
the digest the Lean README and `Pts.lean` state.

## Credit and AI Assistance, as the Source States Them

`lean/README.md`: “The Lean side is Evan Daniel’s mixed-measure checker in
evand/square-packing (MIT licence), used unchanged at commit
`1718a580e5de2fac7e1a5535e98f11ba447d312e` … Nothing in the Lean library was added or
changed; this folder only adds generated data and the scripts that generate it.” Its
generator is “Evan Daniel’s `gen_zmmtree.py` with a batch mode and a point sublist per
chunk”. The certificate’s README credits the method to Daniel, as `T-066` records. The
commit message names Claude as co-author.

## What Is Retained

Retained byte-identical at their upstream paths, under
`square-packing/problems/square-lower-bounds/certificates/k2m5_n59_L8/`:

- **`lean/Sqpack/S59Lower.lean`**, the two theorems, and **`lean/Axioms59.lean`**, the
  `#print axioms` probe;
- **`lean/Sqpack/S59T/Pts.lean`** (1,841,594 bytes), the cover as Lean data with its D4
  invariance and total, and **`lean/Sqpack/S59T/Cov.lean`**, the gluing of the 6,400
  root theorems, both as built;
- **`lean/scripts/`**: `gen_zmmtree_s59.py`, `run_s59.py` and `mk_s59_cov.py`, the
  generator, its driver and the gluing generator; **`lean/batches.json`**, the 290
  batches; **`lean/README.md`**;
- **`lean/receipts/kernel_tasks.jsonl.gz`**, the source’s per-task run record, as
  published;
- **`README.md`**, **`ASSET.json`** and **`SHA256SUMS`**, which the commit changed.

Pinned by digest only:

| Upstream path | Bytes | Why not retained |
| --- | ---: | --- |
| `lean/SOURCES.sha256` | 4,108,305 | The SHA-256 of the 43,444 generated files the source does not store; needed only to compare a rebuild’s generated tree file by file, and fetched at the pin for that |
| `INDEX.json` | 244,978 | The repository’s index; this commit adds `lean/README.md` to the entry’s documents, as the retained `ASSET.json` does |
| `check_records.py`, `verify.sh` | 4,441 and 5,936 | Byte-identical in the [4 October record-updates packet](../wand125-record-updates-2026-10-04/README.md) |
| `zm_mixed_d4/manifest.json`, `zm_mixed_root/manifest.json` | 1,977 and 2,110 | Byte-identical in the 1 October packet |
| `LICENSE.md`, `problems/square-lower-bounds/LICENSE` | 603 and 1,064 | Byte-identical in the [14 October closed-form packet](../wand125-closed-form-2026-10-14/README.md) and the [7 October FN1 packet](../wand125-fn1-input-bindings-2026-10-07/README.md) |

[`acquisition/sources.json`](acquisition/sources.json) records the pin and every file,
and from `packing/`,
`uv run --frozen --all-extras --group dev python -m devtools.acquire_source wand125-n59-lean-kernel-2026-10-11 --checkout CHECKOUT`
rebuilds the packet from a checkout at the pin; `--check` re-derives it without one.

**Daniel’s library at `1718a580` is already retained.**
[`receipts/evand-library-closure-1718a580.json`](receipts/evand-library-closure-1718a580.json),
written by `devtools.lean_closure`, lists the closure of `Sqpack.Attain`, `ZMTreeX` and
`CovM` at that commit: 19 modules, 936,052 bytes, Mathlib only outside them, and no
`sorry`, `axiom`, `native_decide` or other kernel escape in their code. All 19 and the
three build pins (`leanprover/lean4:v4.33.1`, Mathlib `0df444a3`) have the same Git blobs
as the copies the [7 October packet](../evand-exact-and-local-reports-2026-10-07/README.md)
retains from `f58a0177`, so no further evand packet is needed for this proof. Daniel’s
own `lean/scripts/gen_zmmtree.py` at `1718a580` is not retained; the generator this
proof used is Hosono’s retained variant.
[`receipts/source-tree-closure.json`](receipts/source-tree-closure.json) is the same read
of the source’s own `lean/` tree: `S59Lower` and `Cov` are present, and the 290
`B<k>/Roots` modules and `Sqpack.Attain` are not, as the README says.

## The Claim, as the Source States It

`S59Lower.lean` proves, in namespace `SquarePacking`,

```lean
theorem s59_ge_8 : (8 : ℝ) ≤ minSide 59
theorem s59_eq_8 : minSide 59 = 8
-- 'SquarePacking.s59_eq_8' depends on axioms: [propext, Classical.choice, Quot.sound]  (README)
```

with “no `sorry`, no `native_decide`, no new axioms”, where `minSide` and `Packs` are
`S32.lean`’s at `1718a580`: closed unit squares, translated and rotated, in $[0,s]^2$ with
pairwise disjoint interiors.

- **The certificate** is the mixed cover `n59_mixed_cover_8.txt`: 26,308 points and
  5,240 segments of $[0,8]^2$, masses $w/10^8$, total $1474762899/25000000 = 58.99051596
  < 59$ by `T-066`’s claim. `Pts.lean` holds it as search trees and lists, with
  `pts_nodup`, `pts_d4`, `segs_d4` and `wsum_lt` checked by `decide +kernel`.
- **The covering statement** is a box tree over the D4 fundamental region
  $[0,4]^2 \times (0, 1/2]$, cut into $80 \times 80$ root cells; each root cell’s tree is
  generated by `gen_zmmtree_s59.py`, and every chunk is one `decide +kernel` of
  `ZMTreeM.checkM`, proved sound once (`ZMTreeM.soundM`). The 6,400 cells form 290
  batches; batch $k$ is `Sqpack/S59T/B<k>/Part<i>.lean`, about 50 leaves each, 43,154
  files in all, and `B<k>/Roots.lean`, one theorem per root cell. None of these 43,444
  files is stored; `SOURCES.sha256` lists their SHA-256.
- **The bound** is Daniel’s `le_minSide_mixed` on the cover, which `CovM.lean` defines at
  `1718a580` (the README places it in `Attain.lean`), and the $8 \times 8$ grid
  (`packs_grid`) gives the equality.

**The source’s run**, as `lean/README.md` states it: Lean `v4.33.1` on Arm64 Linux
machines; generation 94 CPU-hours; the Part files 768 CPU-hours, at most 9.8 GB resident
per `lean`; the `Roots` files 0.5 CPU-hours; `Cov.lean` 13 s and `S59Lower.lean` 8 s at
35 GB resident each, mostly mapped imports. The retained receipt agrees with the first
three: 290 generation tasks (94.04 hours, at most 7.5 GiB), 43,154 Part tasks (767.87
hours, at most 9.8 GiB) and 290 Roots tasks (0.48 hours), 43,734 lines of task, seconds
and peak resident memory. It records no exit status, though the README says every task
returned 0, and it does not cover `Cov.lean`, `S59Lower.lean` or the axiom run. The
README’s `receipts/final_build.log`, “the last two builds and the axioms”, is not in
the tree at the pin, so no axiom output is published.

## The Build Plan, Priced

The README’s three steps from a checkout of evand/square-packing at `1718a580`, staged
from the retained library: build `Sqpack.S59T.Pts` and `Sqpack.Attain`; generate and
check the 290 batches with `run_s59.py`, comparing the generated files with
`SOURCES.sha256`; glue with `mk_s59_cov.py`, build `Cov` and `S59Lower`, and run
`Axioms59.lean`, accepted only with the three standard axioms.

| Item | Estimate |
| --- | --- |
| Toolchain | `leanprover/lean4:v4.33.1` and Mathlib `0df444a3`’s cache, about 10 GB of disk with the toolchain; Python 3 for the generator |
| CPU | about 862 CPU-hours: 94 generation, 768 Part files, 0.5 `Roots`, by the retained receipt |
| Memory | 9.8 GB per Part process, and 35 GB for `Cov` and `S59Lower`, above this host’s 15 GB |
| Subset under the cap | `lake build Sqpack.S59T.Pts` alone decides the data facts (no duplicate atoms, D4 invariance, total below 59) in Lean, priced at under an hour; it decides no covering and moves no rung |

The complete build is held: it is above the owner’s 40 CPU-hour item cap and this host’s
memory. What it would add: a `proof-assistant-checked`, `replayed-here` route to
`T-066`’s lower half, a second machine method beside `zmx2` that shares Daniel’s
authorship and architecture but is checked by Lean’s kernel.

## Limitations

- **Nothing was built or run here.** The axiom set and the runs are the source’s report,
  and the axiom output it names is not published.
- **The proof’s bulk is generated and not published.** A rebuild regenerates it; the
  kernel checks what the generator writes, so the generator is untrusted by design.
- **No review has read it.** The mathematical review of stage 4 starts from this packet.

## Original Gzip Files

The upstream file whose own name ends in `.gz` is retained as published, never
recompressed. The table binds its compressed bytes: the Git blob is its blob at the
pinned commit.

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `square-packing/problems/square-lower-bounds/certificates/k2m5_n59_L8/lean/receipts/kernel_tasks.jsonl.gz` | upstream | `4f5fc25382ca9266fda9ee084d94e8ad37ac81df` | `e2758f5d46d7625f3bac305a60417095db67f4b8f98193b219aa8046d18e76d0` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
