# Hosono’s Lean Kernel Proof of Valid7, as Merged at 060c1a1

This packet retains version 1 of the Lean kernel proof of Evan Daniel’s finite premise
`Valid7`, which Hiroaki Hosono (wand125) contributed as PR #6 to
[evand/square-packing](https://github.com/evand/square-packing) and Daniel merged at
`060c1a1` on 11 October 2026. `lean/VALID7.md` says the generated `Sqpack/V7/Main.lean`
proves, in namespace `SquarePacking.LemmaELeaf`,

```lean
theorem valid7 : Bentz.Valid7
theorem bentz : ∀ k : ℕ, 6 ≤ k → minSide (k ^ 2 - 3) = k   -- Bentz.bentz_of_valid7 valid7
theorem validTilt7 : Bentz.ValidTilt7
```

with axioms `[propext, Classical.choice, Quot.sound]` and no `sorry` or `native_decide`.
The record holds $s(k^2 - 3) = k$ for every $k \ge 6$ as `T-064`, confirmed on two exact
checkers of `Valid7` and a build here of Daniel’s reduction. It registers this proof,
with [version 2](../wand125-valid7-lean-v2-2026-10-17/README.md), as `T-249`, a
formalization of `T-064`, at `V0`/`C0`, with the bibliography key
**[wand125 Valid7 Lean 2026-10-11]**. Issue
[#537](https://github.com/jlevy/squares/issues/537) tracks it, and bead `think-0ayk` owns
its import. Nothing here has built it, and no review has read it yet.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/evand/square-packing> |
| Revision | `060c1a1052029f81f30c8a97134ee03666b1bb77`, “Merge PR #6 (wand125): ValidTilt7 / Valid7 in the kernel, s(k^2 - 3) = k for all k >= 6” |
| Committed | 2026-10-11T02:36:49Z, by Evan Daniel; the merge names Claude as co-author. Its message says the root modules and `Main` are generated from wand125’s release `data/valid7-lean-certs-v1`, not in the repository, and that the merge was reviewed statically on 10 October and not rebuilt |
| Licence | MIT, copyright (c) 2026 Evan Daniel; `LICENSE` and `CREDITS.md` pinned against the [n299 packet](../evand-n299-2026-10-26/README.md)’s identical copies |
| Retrieved | 2026-10-26, a blobless clone with a sparse checkout of `lean/` at the pin |
| Retained | 68 files, 2,021,491 bytes, under [`square-packing/`](square-packing/) |

## What Is Retained

The whole `lean/` tree at the pin is 2,537 files and 39 MB, almost all of it other proofs’
generated data (`Sqpack/Exact/`, 34 MB). The packet retains what `Valid7` needs:

- **The closure.** `devtools.lean_closure` followed every import from the modules the
  generators import (`Sqpack.V7.Bridge`, `V7.Data`, `LemmaEDec`, `LemmaESplit`, `CapK`,
  `ExTreeX`, `LemmaESplitX`, `LemmaZ` and `ValidSplit7`): 55 modules and the three build
  pins, 1,931,946 bytes, with no kernel-escape token in any
  ([receipts/lean-closure.json](receipts/lean-closure.json)). `Bentz.lean` and
  `ValidSplit7.lean` state `Valid7`, `ValidTilt7` and the reduction; `V7/Bridge.lean`
  proves `box7Cover_eq_mcoverP`.
- **The generators**, under `lean/scripts/`: `gen_main.py` (the glue of the 9,800 roots
  and the three theorems), `emit_v7.py`, `run_v7.py`, `capk.py`, `gen_exact.py`,
  `gen_face.py`, `tree_rebuild.py`, `runB.py` (the build scheduler) and `v7_xroots.txt`,
  the 2,612 roots emitted in X mode.
- **`lean/VALID7.md`**, the build’s account: all 9,800 roots passed on 64-core, 512 GB
  machines; `Face` 9 min (47 GB), `Bridge` 7 min (24 GB), `Main` 2 min 17 s (58 GB);
  roughly $10^4$ CPU-hours in all, which the source later measured at about 6,650.

The run’s leaves file, `certificates/k2m3/qx2_zm/runV3_6294052a_leaves.jsonl.gz`, is the
blob the [1 October evand packet](../evand-square-packing-2026-10-01/README.md) retains for
`T-064`. The release asset `v7cert.tar.zst` (39,117,972 bytes, SHA-256
`be50c2ed65b9214515930f8ab235d036684d571f51a7beecbee7e290c6ed4a75`) was downloaded to
scratch on 26 October 2026 for the audit below and is not retained; no file of either
repository states its digest, so [receipts/root-names.json](receipts/root-names.json) is
where it is pinned.

## The Root Names, Audited Here

`gen_main.py` names root $i$ `Sqpack.V7.R{i:05d}`, numbering the roots in the order of the
run’s leaves file, and asserts that they fill the grid of the D4 root.
`devtools.audit_valid7_roots` checked on 26 October 2026 that the names agree:

- the leaves file has 9,800 roots, which fill a 35 × 35 × 8 grid;
- `v7cert.tar.zst` holds exactly `v7cert/R00000.pkl` to `R09799.pkl`, one per root, and
  `v7cert.sha256`, which lists each once with the SHA-256 of its bytes. The pickles were
  hashed, never loaded;
- [version 2](../wand125-valid7-lean-v2-2026-10-17/README.md)’s
  `generated-sources.sha256` names `Sqpack/V7/R00000.lean` to `R09799.lean`, one per
  root; its other 52,825 files but `Main.lean` lie under the directories of 5,303 of
  those roots, each named for its root;
- `v7_xroots.txt` names 2,612 distinct roots among them.

A name that agrees says which module a root’s certificate becomes, not that the module
checks. `python -m devtools.audit_valid7_roots check` re-derives the leaves and X-mode
parts from the retained files.

## What Is Not Established

- **No build here.** A full build of version 2 is about 798 CPU-hours with 37 GB a leaf
  module and 51 GB for `Main.lean`; a sample of roots is a component check that moves no
  rung. Which to run, if either, is the owner’s decision (`think-qu37`).
- **No review yet.** The stage 4 review stays with `think-0ayk`.
- **PR #7**, merged at `44a105e` on 16 October, derives `validTilt7` from the pose tree
  (`ExTreeTilt.lean`) and drops `Face`, with the root modules unchanged; version 2’s
  library, Daniel’s upstream `3f004b7` with two kernel-speed files, carries it.

## Commands

From `packing/`, with the project interpreter:

```bash
python -m devtools.acquire_source evand-valid7-lean-2026-10-11 --checkout CHECKOUT
python -m devtools.acquire_source evand-valid7-lean-2026-10-11 --check
python -m devtools.lean_closure CHECKOUT --commit 060c1a1052029f81f30c8a97134ee03666b1bb77 --root lean \
  Sqpack.V7.Bridge Sqpack.V7.Data Sqpack.LemmaEDec Sqpack.LemmaESplit Sqpack.CapK Sqpack.ExTreeX \
  Sqpack.LemmaESplitX Sqpack.LemmaZ Sqpack.ValidSplit7 --source-url https://github.com/evand/square-packing \
  --json resources/web/evand-valid7-lean-2026-10-11/receipts/lean-closure.json
python -m devtools.audit_valid7_roots scan --certs V7CERT_TAR_ZST --generated GENERATED_SOURCES_SHA256
python -m devtools.audit_valid7_roots check
```

## Compressed Files

| Stored File | Origin | Git Blob of Original | SHA-256 of Original |
| --- | --- | --- | --- |
| `square-packing/lean/scripts/v7_xroots.txt.gz` | upstream | `0cac447c8301c31c597e0f2e19ea60ce382bdad9` | `447072bf8ec3779e29fff2121a069920afec3d501feea1719a84d8b0606ffbfc` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
