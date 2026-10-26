# ValidTilt9 in the Lean kernel: s(k² − 4) = k for every k ≥ 8

`Sqpack/V9/Main.lean` (generated) proves, in namespace `SquarePacking.LemmaELeaf`,

```lean
theorem validTilt9 : Bentz4.ValidTilt9
theorem valid9 : Bentz4.Valid9
theorem bentz4 : ∀ k : ℕ, 8 ≤ k → minSide (k ^ 2 - 4) = k
```

with (`Axioms9.lean`, output in `receipts/main.log`)

```
'SquarePacking.LemmaELeaf.validTilt9' depends on axioms: [propext, Classical.choice, Quot.sound]
'SquarePacking.LemmaELeaf.valid9' depends on axioms: [propext, Classical.choice, Quot.sound]
'SquarePacking.LemmaELeaf.bentz4' depends on axioms: [propext, Classical.choice, Quot.sound]
```

No `sorry`, no `native_decide`, no new axioms.

This folder records the run as it was done. It describes what was run, on which machines, with which
versions, how long it took and what came out. Nothing was re-run or re-checked for this record.

## What is proved and where the statement comes from

`Bentz4.ValidTilt9`, `Bentz4.Valid9` and the reduction `bentz4_of_validTilt9` are Evan Daniel's, in
[evand/square-packing](https://github.com/evand/square-packing) (MIT licence): `lean/Sqpack/ValidSplit9.lean`,
`Bentz4.lean`, `Bentz4Data.lean`. The certificate is his k2m4 run `qxzm_full`
(`certificates/k2m4/qx2_zm/run_k4x_k008_leaves.jsonl.gz`) with the box cover `K4_k008_box9.txt`. These
input files are byte-identical to upstream `main` (44a105e).

### The Lean library used

The run used the library at evand/square-packing `060c1a1` (the merge of PR #6) with two files changed.
`library/library.sha256` lists all 56 files in the import closure of `Main.lean`, plus `lakefile.toml`,
`lake-manifest.json` and `lean-toolchain`.

- 51 files are byte-identical to upstream from `060c1a1` to `main` (`44a105e`), including
  `ValidSplit9.lean`, `Bentz4.lean` and `Bentz4Data.lean`. `lake-manifest.json` is identical to `060c1a1`.
- `library/Sqpack/RowMinN.lean` (new, 199 lines) holds `rmChk`, the row-minimum check of `RowMinK.rmLoop`
  computed on natural-number digits, and `rmChk_sound : rmChk … = true → rmLoop … = true`.
- `library/Sqpack/LemmaEKM.lean` (diff in `library/LemmaEKM.diff`, 4 lines) calls `rmChk` where upstream
  calls `rmLoop`, and adds `rmChk_sound` as one step of its proof. No statement changes.
- The purpose was kernel speed. On 2026-10-10, heavy row modules ran 3 to 5 times faster.
- The three files under `Sqpack/V9/` other than `Main.lean` are new: `Data.lean` (the cover data),
  `Bridge.lean` (the cover equals `box9Cover`) and `Tilt.lean` (`validTilt_of_tree`).

## How the proof is organised

- The D4 root `[0, 9/2]² × (0, 1/2]` is cut into the 45 × 45 × 8 = 16,200 root cells of `qxzm_full`.
  Root `N` is `Sqpack/V9/RNNNNN.lean` (theorem `root_NNNNN : CovT …`).
- The leaves of a root are in `Sqpack/V9/RNNNNN/` as one module per leaf with its data (`…lK`) and one
  module per row group (`…lK_gJ`). Each is a `decide +kernel` check.
- `Main.lean` (from `scripts_manual/gen_main9.py`, run without `V7_SGK`) glues the 16,200 root theorems with `CovT.splitX`, `splitY` and
  `splitU`. It then applies `validTilt_of_tree`, `box9Cover_eq_mcoverP`, `valid9_of_tilt` and
  `bentz4_of_validTilt9`.
- The generated sources are not stored. `SOURCES.sha256` (a Release asset, 1,275,911 files, paths
  relative to `lean/`) lists the sha256 of every generated file. Its own sha256 is given below.

## The recorded run

All dates are UTC.

### Machines and versions

There were two Google Cloud c4a-highmem-48 Spot VMs (48 Arm vCPUs, 376 GB), called machine A and
machine B. Both ran Ubuntu 24.04, Lean v4.33.1 and Python 3.12.3. Details are in `ENVIRONMENT.md`.

### Generating and checking the roots

The driver is `driver/run9.py`. Machine A took the even roots and machine B the odd roots. For each root,
the driver ran these steps in order:

1. the certificate (`run_v7.py`, a pickle), retried with stronger options when it failed;
2. the Lean sources (`emit_v7.py --chunk 20`);
3. `lean -o` of every leaf module, then every row group, then the root module.

The driver admitted jobs by free memory. Restarts resumed from per-task markers.

- When machine B had finished its own roots, it took 744 of machine A's highest even roots. Those were
  moved to A through a storage bucket, with md5 checked.
- The roots were checked from 2026-10-10 to 10-15.

### Certificates installed by hand (9 roots)

In 9 roots the automatic certificate step failed. For each of them, certificates were made by hand in trial
directories and the one that closed was put in place with its marker. The Lean side (emit, leaves, groups,
root) then ran through the driver as for every other root.

Five roots used the run's own generator (`scripts/`) with options it already had. The options that closed
each root were later added to the automatic retries.

| root | options | trial | logged in `tasks.jsonl` |
|---|---|---|---|
| 2270 | `V7_MIXED_CH=1` | `try2270/E`, 10 s | no `manual` line (the cert marker was written by hand) |
| 4262 | `V7_SUBM=1 V7_MIXED_CH=1 V7_MAXDEPTH=12` | `try4262/C` | `"manual"` |
| 11715 | `V7_SUBM=1 V7_MIXED_CH=1 V7_MAXDEPTH=14 V7_SPLIT=6` | `tryb/11715A` | `"manual"` |
| 11827 | `V7_MAXDEPTH=16 V7_SPLIT=8` (with `SUBM`, `MIXED_CH`) | `tryb/11827D` | `"manual": "tryb/11827D"` |
| 11397 | `V7_MAXDEPTH=18 V7_SPLIT=10 V7_RSHIFT=3` (with `SUBM`, `MIXED_CH`) | `tryb/11397E` | `"manual": "tryb/11397E"` |

The options of 11827 and 11397 are taken from the run notes, because their `tasks.jsonl` lines give only
the trial directory.

Four roots did not close with any existing option: 8917, 11424, 11768 and 12100. They were rebuilt with two
new generator options, using the copy in `scripts_manual/`. The other files there are identical to
`scripts/`, and the defaults reproduce the old behaviour. The Lean library is unchanged.

| root | options | certificate | modules | root theorem |
|---|---|---|---|---|
| 12100 | `V7_TOUCH=1e-9` | 0 failures, 55 s | 185 | rc 0 |
| 11424 | `V7_SGK=8 V7_SPLIT=10` | 0 failures, 3,065 s | 3,847 | rc 0 |
| 11768 | `V7_SGK=8 V7_SPLIT=18` | 0 failures, 2,699 s | 3,962 | rc 0 |
| 8917 | `V7_SGK=8 V7_SPLIT=18` | 0 failures, 9,627 s | 8,322 | rc 0 |

- 12100: one segment touches the square's corner at u = 0 and lies outside it for u > 0. With the
  default 1e-12 threshold the generator counted it as meeting the square, and its case split failed a
  zero-margin vertex check. `V7_TOUCH` is the chord length above which a segment counts as meeting the
  square at a sample point; at 1e-9 the segment is dropped (contribution 0).
- The other three failed in the first u-interval at box corners. Splitting stopped at the 1/640 centre
  grid. `V7_SGK=8` makes the grid 8 times finer. The root theorem is built on the fine grid and brought
  back by the existing `CovT.scaleS (k := 8)`.
- Trials that did not close are in the logs asset, with every trial directory of the 9 roots:
  - 11768 at `V7_SPLIT=10`: failed, 2,393 s.
  - 8917 at `V7_SPLIT=10`: stopped by hand.
  - 11424 at `V7_SPLIT=18`: closed, 3,057 s, not used.

### Assembly

- Machine A had its disk enlarged to 550 GB and received all 1.27 M oleans (340 GB).
- `lean -o Main.olean Main.lean` took 584 s with 230 GB resident, mostly mapped olean files.
- `lean Axioms9.lean` took 222 s.

The first attempt (`receipts/main_try1.log`) failed after 128 s. The error was
`failed to read file '…/R12076/r12076l42.olean'` on an intact file. The cause was
`vm.max_map_count = 1048576`, which is below the number of oleans. It was raised to 4194304 on machine A
with `sysctl -w`, without a reboot, and the second attempt passed. Nothing else changed.

### CPU time

These figures are summed from `tasks.jsonl` of both machines.

| step | tasks (rc 0) | CPU hours | peak resident |
|---|---|---|---|
| certificates (`run_v7.py`, all attempts) | 16,195 | 177 (135 for the passing attempt) | 2.2 GB |
| Lean sources (`emit_v7.py`) | 16,196 | 0.9 | 1.7 GB |
| leaf modules (`def`) | 140,466 | 2,694 | 22.3 GB |
| row groups (`grp`) | 1,129,519 | 4,665 | 19.6 GB |
| root modules | 16,309 | 31 | 32.5 GB |
| `Main.lean` + `Axioms9.lean` | 1 + 1 | 0.2 | 230 GB |

The kernel checks total about 7,390 CPU hours.

- The four rebuilt certificates took another 4.3 CPU hours, or 5.8 with the failed and unused trials. One
  trial was stopped by hand and its time was not logged. Their emit and kernel checks are in `tasks.jsonl`.
- 102 leaf tasks were killed by the memory guard and re-run.
- 10,483 tasks passed twice, either after a Spot preemption or on both machines for the moved roots.

## Rebuilding

From a checkout of evand/square-packing at `060c1a1`, in `lean/`:

1. Put this folder's `library/Sqpack/RowMinN.lean` and `LemmaEKM.lean` into `Sqpack/`.
2. Put `Sqpack/V9/{Data,Bridge,Tilt}.lean` into `Sqpack/V9/` and `scripts/*.py` into `scripts/`.
3. Build `Sqpack.V9.Tilt`, `Sqpack.V9.Bridge`, `Sqpack.CapK`, `Sqpack.ExTreeX`, `Sqpack.LemmaEDec`,
   `Sqpack.LemmaESplit` and `Sqpack.LemmaESplitX`.
4. Run `driver/run9.py` (one `lean -o` per module; the even/odd split and the memory guard are in its
   header). To skip the certificate step, unpack the Release asset `v9-certs.tar.zst`, put all 16,200
   `certs/auto/*.pkl` and `certs/manual/*.pkl` into the driver's certificate directory, and write the
   `cert:N` markers; the driver then starts at the Lean sources. These are the certificates the run used. For roots 8917, 11424, 11768 and 12100, use `scripts_manual/` with the options of the table.
   Optionally compare the generated files with `SOURCES.sha256`.
5. Run `python3 scripts_manual/gen_main9.py` without `V7_SGK` (this is how `Main.lean` was made; it reads
   the grid as `SG0 = 128`). Then run
   `lean -o .lake/build/lib/lean/Sqpack/V9/Main.olean Sqpack/V9/Main.lean` and `lean Axioms9.lean`.
   Raise `vm.max_map_count` above the number of oleans first.

The files `Sqpack/V9/Main.lean` and `Axioms9.lean` here are the ones that were built.

| file | sha256 |
|---|---|
| `Sqpack/V9/Main.lean` | `39f42605c45e3c084f5de66e900c2b3e862356bee756db5d730ef5e3dc0904f9` |
| `Axioms9.lean` | `9bfeda3634d91245b417a1fdc6f6c5f7d03b4c70d6b5bf2b1c27456863faae0d` |
| `Main.olean` (as built) | `4a60a684ec935f3a16fd033e57f671926c0051e9501a64a6a64d4575eed6e442` |
| `SOURCES.sha256` (Release) | `5bce91b1232261b356fa0d16d94acdd51b05c275327f8b4c8a268d09e53270db` |

## Files

- `ENVIRONMENT.md`: the machines, versions, OS settings and the machine history.
- `scripts/`: the generator and emitter as used for every root except the four rebuilt ones.
- `scripts_manual/`: the four files that differ, as used for the four rebuilt roots.
- `driver/run9.py`: the final driver. Earlier versions are in the logs asset.
- `library/`: the two changed library files, the diff and the sha256 of the import closure.
- `receipts/`: `main.log`, `main_try1.log`, `manual.log` of each machine and `sha256_final.txt`.
- `receipts/ASSETS.sha256`: the sha256 of the three Release assets.
- `receipts/CERTS.sha256`: the sha256 of each of the 16,200 certificates in `v9-certs.tar.zst`.
  `receipts/MANUAL.tsv`: the 9 roots whose certificate was made by hand, with the options used.
- Release assets, in [`validtilt9-lean-v1`](https://github.com/wand125/square-packing/releases/tag/validtilt9-lean-v1):
  - `v9-certs.tar.zst` (109 MB, sha256
    `c40eed8bc57aca82824bcb9a00d8b8d37773b6258bc6e86aa171cd8a01774593`): the per-root certificates as used
    (pickles from `run_v7.py`, unchanged). It holds 16,191 in `certs/auto/` and the 9 hand-made ones in
    `certs/manual/`, plus `CERTS.sha256` and `MANUAL.tsv`. 748 roots had a copy on both machines; each pair
    was byte-identical.
  - `SOURCES.sha256.zst`;
  - the logs: `tasks.jsonl` of both machines, every driver version, the hand-built certificates' logs and
    the Main logs.

### Changes made for publication

The published logs and receipts were scanned for home-directory paths, machine names and Japanese text.
Only one substitution was needed: the home directory path was replaced by `~`, in two lines of
`main_try1.log`. No machine names and no Japanese text were found. `receipts/SANITIZE.sha256` gives the
file's sha256 before and after. Nothing else was changed.

The machines were Google Cloud VMs. This bundle is built from the outputs of that run.
