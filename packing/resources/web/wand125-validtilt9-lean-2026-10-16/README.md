# Hosono’s Lean Kernel Proof of ValidTilt9, Pinned 2026-10-16

This packet retains the Lean proof that
[wand125/square-packing](https://github.com/wand125/square-packing) added on 16 October
2026 under `problems/square-lower-bounds/certificates/k2m4_n77_L9/lean/`. In namespace
`SquarePacking.LemmaELeaf`, the generated `Sqpack/V9/Main.lean` proves

```lean
theorem validTilt9 : Bentz4.ValidTilt9
theorem valid9 : Bentz4.Valid9 := Bentz4.valid9_of_tilt validTilt9
theorem bentz4 : ∀ k : ℕ, 8 ≤ k → minSide (k ^ 2 - 4) = k := Bentz4.bentz4_of_validTilt9 validTilt9
```

`ValidTilt9` is Evan Daniel’s finite premise for $s(k^2 - 4) = k$, which the record holds
as `T-081`, reported, on two reported runs of it and a build here of Daniel’s reduction.
The record registers this proof as `T-251`, a formalization of `T-081` at $k \ge 8$, at
`V0`/`C0`, with the bibliography key **[wand125 ValidTilt9 Lean 2026-10-16]**. Issue
[#643](https://github.com/jlevy/squares/issues/643), which the project opened, tracks it,
and bead `think-jh0n` owns its import. The claims below are the source’s; nothing here
has built the proof, and no review has read it yet.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/wand125/square-packing> (Hiroaki Hosono) |
| Revision | `319a779efcc78db2f92bffc87844446f8723b01d`, the head the 16 October triage read; `2c75edc` (03:25:10Z) adds `lean/` and `e99f5e3` (03:25:35Z) its four receipt logs, and nothing under `lean/` changes after them to the pin |
| Committed | 2026-10-16T04:47:29Z; both commits name Claude as co-author |
| Licence | MIT, “Copyright (c) 2026 wand125” (`problems/square-lower-bounds/LICENSE`; the root `LICENSE.md` says each folder keeps the licence it was published under). The statement, the reduction and the certificate are Evan Daniel’s, MIT |
| Retrieved | 2026-10-26, a blobless clone of the single branch with a sparse checkout of the pin |
| Retained | the 56 files of `lean/`, 2,908,328 bytes, byte-identical under [`square-packing/`](square-packing/); the two licences pinned against the copies the [14 October closed-form packet](../wand125-closed-form-2026-10-14/README.md) and the [7 October FN1 packet](../wand125-fn1-input-bindings-2026-10-07/README.md) retain |

The release `validtilt9-lean-v1` holds what is not in Git. The retained
`lean/receipts/ASSETS.sha256` pins its three assets, none downloaded here:

| Asset | SHA-256 | What it is |
| --- | --- | --- |
| `v9-certs.tar.zst` | `c40eed8bc57aca82824bcb9a00d8b8d37773b6258bc6e86aa171cd8a01774593` | the 16,200 per-root certificates, Python pickles (109 MB) |
| `SOURCES.sha256.zst` | `0367b0e78b60e654273442d27f92f4509e7d0bb5a3ea940f1a39aab6d70739fd` | the SHA-256 of each of the 1,275,911 generated Lean files |
| `v9-logs.tar.zst` | `c3c856968207fd1482712efb5c0b1229572ca70fcb2088da695932fdaf0d29ab` | the run’s logs |

## What the Source Reports

- **Axioms.** `receipts/main.log`: Lean 4.33.1 (aarch64, commit `819816b`) built
  `Main.lean` in 584 s at 230,597,216 kB resident, and `Axioms9.lean` printed
  `[propext, Classical.choice, Quot.sound]` for all three theorems. `lean/README.md` says
  there is no `sorry`, no `native_decide` and no new axiom, that each leaf and row group
  is `decide +kernel`, and that the run is recorded as it was done, with nothing re-run.
- **Cost.** About 7,390 CPU-hours of kernel checks (leaf modules 2,694, row groups 4,665,
  roots 31), 177 CPU-hours of certificate generation, peaks of 22 to 32 GB a module and
  230 GB for `Main.lean` over 1.27 million oleans, as the 16 October triage read the
  receipts (`think-jh0n`).
- **What is new in the library.** `library/Sqpack/RowMinN.lean` (new: `rmChk` and
  `rmChk_sound`) and `library/Sqpack/LemmaEKM.lean`, changed by the four hunks of
  `library/LemmaEKM.diff`, for kernel speed; `Sqpack/V9/Bridge.lean`
  (`box9Cover_eq_mcoverP`), `Tilt.lean` (`validTilt_of_tree`) and `Data.lean`.

## The Statement Binding, Checked Here

`lean/library/library.sha256` lists the 59 files of the import closure: 56 modules,
`lakefile.toml`, `lake-manifest.json` and `lean-toolchain`. Checked on 26 October 2026
with `sha256sum --check` against the retained copies, every one is in the record:

- 53 are byte-identical to the
  [Valid7 packet](../evand-valid7-lean-2026-10-11/README.md)’s copies at
  evand/square-packing `060c1a1`;
- `ValidSplit9.lean`, where `ValidTilt9` and `Valid9` are defined, is byte-identical to
  the [3 October evand packet](../evand-square-packing-2026-10-03/README.md)’s, as are
  `Basic.lean`, `S32.lean` (where `minSide` is `sInf {s | Packs n s}`), `Bentz4.lean` and
  `Bentz4Data.lean` and the three build pins, 19 files in all, the files of the record’s
  3 October build of the reduction;
- `LemmaEKM.lean`, `RowMinN.lean` and the three `V9` modules are the source’s own and are
  retained here. The 16 October triage read `RowMinN.lean` (199 lines, no `sorry`,
  `axiom`, `native_decide`, `implemented_by`, `extern` or `unsafe`) and found
  `LemmaEKM.lean` to differ from `060c1a1`’s by exactly the diff’s four hunks, with no
  statement change.

So every definition the three theorems’ statements use is the one the record’s own build
of the reduction used. That `Bridge.lean` and `Tilt.lean` say what the statement needs is
the stage 4 review’s to read.

## What Is Not Established

- **No build here.** The replay is held above the owner’s 40 CPU-hour item cap and far
  beyond this host (`think-rw3i`).
- **No review yet.** The stage 4 mathematical review stays with `think-jh0n`.
- **The rectangle theorem** at `746b0c0`, `lean/rectangle-k2m4/`, a second Lean route to
  `T-081`’s lower half over the same premise, is its own import, `think-d5m3`.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source wand125-validtilt9-lean-2026-10-16 --checkout CHECKOUT
python -m devtools.acquire_source wand125-validtilt9-lean-2026-10-16 --check
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
