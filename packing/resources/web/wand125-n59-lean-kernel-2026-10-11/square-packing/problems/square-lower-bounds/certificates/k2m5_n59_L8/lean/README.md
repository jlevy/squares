# s(59) = 8 in the Lean kernel

`Sqpack/S59Lower.lean` (generated) proves

```lean
theorem s59_ge_8 : (8 : ℝ) ≤ minSide 59
theorem s59_eq_8 : minSide 59 = 8
```

in namespace `SquarePacking`, with

```
'SquarePacking.s59_eq_8' depends on axioms: [propext, Classical.choice, Quot.sound]
'SquarePacking.s59_ge_8' depends on axioms: [propext, Classical.choice, Quot.sound]
```

No `sorry`, no `native_decide`, no new axioms.

The certificate is the mixed cover `n59_mixed_cover_8.txt` of this directory's parent
(SHA256 `6f4d2b64f9a88ae49546f05fa28752382f9ebfa8b7f8b6e6c6f1a8e693177e19`). The Lean side is Evan
Daniel's mixed-measure checker in [evand/square-packing](https://github.com/evand/square-packing)
(MIT licence), used unchanged at commit `1718a580e5de2fac7e1a5535e98f11ba447d312e`: the box tree
`ZMTreeM` (`checkM`, proved sound once, `ZMTreeM.soundM`), `CovM`, and `le_minSide_mixed`
(`Attain.lean`), exactly as in his `s(13)` lower bound. Nothing in the Lean library was added or
changed; this folder only adds generated data and the scripts that generate it.

## How the proof is organised

- `Sqpack/S59T/Pts.lean`: the cover (26,308 points, 5,240 segments, masses `w/10^8`) as search trees
  and lists, with its D4 invariance and total mass `< 59` checked by `decide +kernel`.
- The D4 fundamental region `[0,4]^2 x (0, 1/2]` is cut into 80 x 80 root cells; each root cell gets a
  box tree from `scripts/gen_zmmtree_s59.py` (Evan Daniel's `gen_zmmtree.py` with a batch mode and a
  point sublist per chunk). Every chunk of a tree is one `decide +kernel` of `ZMTreeM.checkM`.
- The 6,400 root cells are grouped into 290 batches (`batches.json`). Batch `k` is
  `Sqpack/S59T/B<k>/Part<i>.lean` (about 50 leaves each, 43,154 files in all) and
  `Sqpack/S59T/B<k>/Roots.lean` (one theorem `r_<i>_<j>` per root cell).
- `Sqpack/S59T/Cov.lean` (from `scripts/mk_s59_cov.py`) glues the 6,400 root theorems into the cover
  of the fundamental region; `Sqpack/S59Lower.lean` applies `le_minSide_mixed` and the 8 x 8 grid.

The batch sources are not stored: the generator is deterministic, and `SOURCES.sha256` lists the
SHA256 of every generated file (43,444 files, paths relative to `lean/`), so a rebuild can be
compared file by file.

## Rebuilding

From a checkout of evand/square-packing at `1718a58`, in `lean/`:

1. Copy this folder's `scripts/*.py` into `lean/scripts/` and `Sqpack/S59T/Pts.lean` into
   `lean/Sqpack/S59T/`; then `lake build Sqpack.S59T.Pts Sqpack.Attain`.
2. Generate and check the batches:
   `python3 scripts/run_s59.py . COVER batches.json WORK [--slots N] [--share I/K]`
   (`COVER` is `n59_mixed_cover_8.txt`; `WORK` holds markers and logs; the run restarts where it
   stopped). Optionally compare the generated files with `SOURCES.sha256`.
3. `python3 scripts/mk_s59_cov.py batches.json .`, then
   `lake env lean -o .lake/build/lib/lean/Sqpack/S59T/Cov.olean Sqpack/S59T/Cov.lean`,
   `lake env lean -o .lake/build/lib/lean/Sqpack/S59Lower.olean Sqpack/S59Lower.lean`, and
   `lake env lean Axioms59.lean` (this folder's `Axioms59.lean`).

The files `Sqpack/S59T/Cov.lean` and `Sqpack/S59Lower.lean` here are the ones that were built.

## The recorded run

- Lean `v4.33.1` and the Mathlib of the repository's `lake-manifest.json`, on Arm64 Linux machines.
- Generation 94 CPU-hours; the 43,154 Part files 768 CPU-hours (at most 9.8 GB resident per `lean`,
  shared imports included); the 290 `Roots` files 0.5 CPU-hours; `Cov.lean` 13 s and
  `S59Lower.lean` 8 s (35 GB resident each, mostly the mapped imports).
- `receipts/kernel_tasks.jsonl.gz`: one line per task (generation, Part, Roots) with its CPU seconds
  and peak resident memory; every task returned 0. `receipts/final_build.log`: the last two builds and
  the axioms.
- The data definitions are `noncomputable def` (kernel checks only, no compiled code), which keeps
  each Part `.olean` near 0.5 MB.
