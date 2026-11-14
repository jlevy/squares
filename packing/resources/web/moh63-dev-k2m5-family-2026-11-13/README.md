# Khalili and Gharabaghi’s Family for s(k² − 5) = k, Pinned 2026-11-13

This packet pins [moh63-dev/k2m5-family](https://github.com/moh63-dev/k2m5-family) at
its one commit, of 13 November 2026, for one registration request:
[jlevy/squares#973](https://github.com/jlevy/squares/issues/973), opened by Mohsen
Khalili and Sara Gharabaghi (`moh63-dev`) at 2026-11-14T01:33:59Z, which reports
$s(k^2 - 5) = k$ for every integer $k \ge 7$. The upper halves are the $k \times k$
grids; the claim is the lower bound $s(k^2 - 5) \ge k$. For $k = 7, 8, 9$ it rests on
certificates the record already holds, T-252, T-066 and T-184; for every $k \ge 10$ it
rests on one family of measures reduced to an $11 \times 11$ board.

When it was retrieved the record held $s(95) = 10$ as proved (Greff, T-191) and the
other counts of the family that it holds, $n = 116, 139, 164, 191, 220, 251, 284, 319$
($k = 11$ to $18$), open, each with Hiroaki Hosono’s closed form (T-180) as the reported
lower bound and Karakuş’s strip bound as the verified one.
Its import follows Evan Daniel’s families for $k^2 - 3$ (T-064) and $k^2 - 4$ (T-081).
Its Frontier key is **[Khalili Gharabaghi k2m5 family 2026-11-13]**, and the register
entry is T-298. The claim below is stated as the source states it; what was checked here
is in [Checks Made Here](#checks-made-here).

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/moh63-dev/k2m5-family> |
| Revision | `2c0b1b9979bcb67d92eb215366dc5ee19286c1d8`, branch `main`, tree `27a438512f52e61337f974792cb8d71fb4db6472`: the repository’s one commit and its head when retrieved |
| Committed | 2026-11-13T23:50:51Z, by Mohsen Khalili, 1 hour 43 minutes before the issue |
| Licence | MIT, “Copyright (c) 2026 Mohsen Khalili and Sara Gharabaghi” (`LICENSE`); the README adds “Text and data: CC BY 4.0. (See `LICENSE`.)”, though `LICENSE` carries the MIT text alone. Both permit retention |
| Retrieved | 2026-11-14T02:00Z: a full clone of `main` |
| Pinned subtree | Everything but `.gitignore`: 466 files, 17,169,459 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256). The release’s own `SHA256SUMS_ALL` lists every file but itself, and every line holds at the pin |
| Retained here | 465 files, 8,475,699 bytes, byte-identical at their upstream paths under [`k2m5-family/`](k2m5-family/); ten data files of more than 1,000 lines are stored as deterministic gzip ([Compressed Files](#compressed-files)) |
| Pinned by digest only | `tight_tile/cov.tar.xz`, 8,693,760 bytes, SHA-256 `9d57475533d054ad73b75273defc716f88c271cf22fca67f06962a1c62fce535`: the `zmx2` dumps of every uncertified box in the 75 tight-tile roots, over the 5 MiB per-blob ceiling of OR-18. The replay here read it from the pinned commit after checking that digest. A hosted data release is owed before a full replay cites receipts compared with it (`think-0h7r`) |
| Board | `certificate/sol_exact_box11.txt`, SHA-256 `d259fed5c9d5eb02c6fed85f5d1070e86d48f5717305f9e056c9a88adbd12099`, the issue’s and `certificate/SHA256SUMS`’s |
| The issue | [#973](https://github.com/jlevy/squares/issues/973), labelled `intake`; no comment when read |

Evan Daniel’s checkers are not in the tree.
`verification/verify.sh --full` clones evand/square-packing at
`659ee62e4a9d39542a1146e8b011cc3ab6407ede`, applies `verification/zmx2_print_all.patch`
and builds `verify2/`. At that commit `verify2/src/bin/zmx2.rs` is `e2bb84e9…`, which
the [4 October evand packet](../evand-square-packing-2026-10-04/README.md) retains, and
`search/qx2_zm.py` is `6294052a…`, which the
[3 October evand packet](../evand-square-packing-2026-10-03/README.md) retains.
The `zeromargin.py` it imports there, `3cb95fb7…`, was not retained anywhere; the
[24 October evand packet](../evand-square-packing-2026-10-24/README.md) now retains it
and pins the other checker files at that commit to the earlier copies.

## Credit and AI Assistance, as the Source States Them

The README and the paper name Mohsen Khalili and Sara Gharabaghi, independent
researchers, as the authors, “with AI assistance (see the paper’s acknowledgments)”, and
call the work computer-assisted and not yet peer reviewed.
The paper’s acknowledgments: “The search, the certificate, the Tight-Tile checker and
its proof, and the verification runs were produced with Claude (Anthropic) under the
authors’ direction; the authors reviewed the method, the checks and the text.
We thank Evan Daniel for the open-source linear program, checkers, format and Lean
reductions this work builds on; Hiroaki Hosono and B. Greff for their public
certificates; and the Squares Project for its records.”

The paper credits the method’s lineage to Friedman’s survey, Nagamochi, Kearney and
Shiu, Bentz and Daniel, Daniel’s families for $k^2 - 3$ and $k^2 - 4$ and their
corner-plus-periodic-wall form, and his quadrant linear program `qx2_lp.py`. It names
two things as new: the family’s parameters (corner size 4, wall depth 4, pitch $1/10$, a
Lebesgue interior), which push the saving per corner from about $1.25$, the limit Daniel
found at pitch $1/5$, to $D \approx 1.3406 > 5/4$; and the Tight-Tile Lemma, which
closes the wall tiles of mass exactly one where box subdivision stalls.
`search/` documents the authors’ patches to Daniel’s LP and projection tools, which are
not part of the proof.
The source cites this project’s register for $k = 7, 8, 9, 10$ (T-252, T-066, T-184,
T-191) and thanks it for its records; it names no debt to the project’s methods, so its
lineage is `independent`.

## The Claim, as the Source States It

| Part | What it states | How the source decides it |
| --- | --- | --- |
| $k = 7, 8, 9$ | $s(44) = 7$, $s(59) = 8$, $s(76) = 9$ | The certificates T-252 (theirs), T-066 (Hosono) and T-184 (Greff), each V3/C3 here |
| Mass (Lemma 6) | $\mu_k$ has total $k^2 - 4D$, $D = 1340566927759/10^{12} > 5/4$, so below $k^2 - 5$ | `sanity_k2m5.py`; boards $k = 10, 11, 12, 13, 20$ summed; the Lean `famCover_total5` for every $k \ge 9$ |
| Locality (Lemma 7) | Every unit square in $[0,k]^2$ has the mass of a unit square in $[0,11]^2$, so validity of $\mu_{11}$ gives every $k \ge 10$ | A proof by hand; the Lean `k2m5_of_valid11 : Valid11 → ∀ k ≥ 10, minSide (k² − 5) = k`; `locality_check.py` on $k = 10, 12, 13, 20$ |
| Valid11, $\theta = 0$ | Every axis-parallel unit square has mass at least one | Daniel’s Lemma Z at 10,000 limit corners, an exact axis check at 7,717 corners, `zmx2 cert0` on 2,500 roots |
| Valid11, general position | 12,024 of the 12,100 D4 roots certified | `zmx2 cert --d4 --first-order --depth 40 --node-cap 20000000`, 55 columns, 45,366 CPU-seconds recorded |
| Valid11, root 9632 | The 6,850 boxes `zmx2` leaves lie in one `qx2_zm.py` root, which leaves 83 boxes, none meeting them | `qx2_zm.py` at depth 18 on a cover cropped to the root’s neighbourhood, 1,652 CPU-seconds; `check_9632.py` |
| Valid11, the 75 tight-tile roots | The Tight-Tile Lemma (paper section 6): every pose within $u_0$ of tilt and $\delta_{\max}$ of a tight wall tile has mass at least one, and every one of the 1,255,023 boxes `zmx2` leaves there lies in that region | `ttbox` in 308 jobs at $u_0 = 1/4000$, 15 at $1/2000$ and 3 reruns, about 2.75 million cells, 1,007,447 CPU-seconds recorded; `cov_check.py` |

The source reports controls (`docs/CHECKING.md`): `zmx2` refuses the board with every
segment mass scaled by $999/1000$ and by $993/1000$ at root $(15, 36)$, which it
certifies for the real board; `qx2_zm.py` at root 9632 with masses scaled by $999/1000$
leaves 87 boxes, three meeting `zmx2`’s, so `check_9632.py` says NOT-CLOSED; the
Tight-Tile checker refuses masses scaled by $0.99$, the line $x = 2$ lowered by 1%, and
one segment moved so that the $\theta = 0$ limits are unchanged and the first-order
growth is smaller, a true violation of mass $1 - 1.34 \cdot 10^{-7}$; and
`locality_check.py` refuses a one-weight mutation of $\mu_{12}$. It reports one
adversarial review of the Tight-Tile proof and code by a separate AI agent, which found
two bookkeeping gaps in the coverage step, since fixed, and no review by outside
mathematicians.

## Checks Made Here

On 14 November 2026, on a four-core x86-64 Linux container, Python 3.14.7 and rustc
1.97.0, at most two jobs at `nice -n 19`. Every run went through
[`devtools.replay_k2m5_family`](../../../devtools/replay_k2m5_family.py), which stages
the retained tree with each file held to the manifest and `cov.tar.xz` to its pinned
digest, and runs the source’s own programs under `devtools.replay_receipt`; each receipt
is in [`receipts/`](receipts/), and
[`receipts/compare.json.gz`](receipts/compare.json.gz) sets each run beside the source’s
record of it.
Python ran with `-I`, the script’s directory appended to `sys.path` so that
the source’s sibling imports resolve and nothing it ships can shadow a standard module.

- **Custody.** `devtools.acquire_source --check` re-derives the packet from its
  manifest; the board’s SHA-256 is the issue’s; every line of `SHA256SUMS_ALL` holds at
  the pin.
- **The fast `verify.sh`, unmodified**
  ([`receipts/verify_fast.log`](receipts/verify_fast.log)), passed in 37 CPU-seconds:
  the certificate hashes; `SANITY-OK` (13,244 segments, total
  $28909433072241/250000000000 = 121 - 4D$ exactly, $D > 5/4$, D4-invariant, the family
  file agreeing); `LOCALITY OK` on the built boards $k = 10, 12, 13, 20$;
  `ZMX2-AUDIT-OK` (55 columns, 12,100 roots, one settings hash, uncertified boxes in
  exactly the 75 tight-tile roots and root 9632); `ROOT-9632-CLOSED` on the recorded
  outputs; `jobs
  ALL-OK 308`; and `COVERAGE-OK`, 1,255,023 boxes inside the certified region.
  It reads the recorded runs and recomputes no tilted box: a diagnostic of the records.
- **The checkers at the pin.** evand/square-packing `659ee62` was fetched; its
  `verify2/src/bin/zmx2.rs` is `e2bb84e9…` and its `Cargo.toml` and `Cargo.lock` are the
  retained copies, so `devtools.replay_evand_zmx2 build --checker e2bb84e9` builds it
  from retained bytes, to binary
  `d68a2e3540344a0e5ad8af33847e3c473b099cf922b150afd184cc715e038787`, the 31 October
  build’s ([`receipts/zmx2_build.log`](receipts/zmx2_build.log)).
  `verification/zmx2_print_all.patch` touches `zmx2.rs` alone and replaces one line, the
  `.take(40)` of the uncertified-box listing, with two that take every box when
  `ZMX2_PRINT_ALL` is set; it changes output only.
  The patched copy built to
  `32cf67df0081e6ebf2e26c5173f2929d007833ae2de49b40d23105b6b28ed615`
  ([`receipts/zmx2_print_all_build.log`](receipts/zmx2_print_all_build.log)).
- **`zmx2`, a sample of the sweep** ([`receipts/zmx2/`](receipts/zmx2/)). `cert0` on all
  2,500 roots: VERIFIED-D4 at $\theta = 0$, as recorded.
  Columns 0 to 22, 26 to 31 and 43 of the first-order sweep, with `verify.sh --full`’s
  flags: 30 columns, 6,600 of the 12,100 roots, 4,545 CPU-seconds here against the
  source’s 3,977 for the same columns, 8.8% of the sweep’s recorded 45,366. Every
  column’s census (roots, boxes, certified, empty, uncertified, deepest level) and every
  uncertified box it lists equal the source’s record; column 15 leaves 2,753 boxes in
  its tight-tile roots and column 43 405, among them root 9632’s, which reaches `zmx2`’s
  default cap of 200 uncertified boxes and stops at 226, as the source’s sweep did.
- **Root 9632, whole.** The patched `zmx2` on that root alone, with `--uncert-cap
  100000000` as `tight_tile/run_cov.sh` passes for the 75 dumps
  ([`receipts/r9632/dump.log.gz`](receipts/r9632/dump.log.gz)), 229 CPU-seconds: 168,563
  boxes, 77,432 certified, 6,850 uncertified, every box the source’s `dump.out` lists.
  Without the cap, at `zmx2`’s default of 200, the root stops at 226 boxes
  ([`receipts/r9632/dump_cap200.log`](receipts/r9632/dump_cap200.log)), so the dump
  needs the flag, which neither its header nor the release records.
  `qx2_zm.py` (`6294052a…`, with `zm_mixed.py`, `mixed_cover.py` and `zeromargin.py`
  `3cb95fb7…` staged by digest from the evand packets) on the source’s cropped cover
  with the source’s arguments, `--nproc 1`
  ([`receipts/r9632/zm.log`](receipts/r9632/zm.log)), 1,274 CPU-seconds: 2,357 boxes to
  depth 18, 83 uncertified, the leaf census equal to the source’s and the list of 83
  byte for byte its `zm_unc.txt`. The source’s `check_9632.py` on these two outputs
  ([`receipts/r9632/check_9632.log`](receipts/r9632/check_9632.log)): all 6,850 `zmx2`
  boxes inside the window, one `qx2_zm.py` root meeting it, none of its 83 boxes meeting
  a `zmx2` box, `ROOT-9632-CLOSED`. Each of the cropped cover’s 632 segments is a
  segment of the board with its mass, and its header and Lebesgue square are the
  board’s, so it is the board with segments removed; `crop_cover.py`, which made it, is
  not in the release.
- **The Tight-Tile checker, a sample** ([`receipts/tight/`](receipts/tight/)). 26 of the
  323 jobs, 22 strips and 4 lines across $d_0 = 3/2, 5/2, 7/2$ and both tilt signs, all
  among the cheapest, run with the retained `run_tt.py` as `run_all2.sh` runs them: 252
  CPU-seconds here against the source’s recorded 687, under 0.1% of the jobs’ recorded
  1,007,447. Every job ends ALL-OK, and every chart line and verdict, 144 lines in all,
  equals the recorded output’s (cells, certified cells, refused cells, worst margin).
  The retained `run_tt.py` prints one field, `"K": "4"`, that the recorded outputs in
  `out/` and `out_u2000/` lack and only `out_u2000_fix/` has, so those outputs were
  written by an earlier version of the script (question 9); the comparison leaves that
  field out.
- **Controls** ([`receipts/controls/`](receipts/controls/)), each held by
  `tests/test_replay_k2m5_family.py`:
  - `zmx2` at root $(15, 36)$, depth 24, node cap $2 \cdot 10^6$: the real board REGION
    CLEAN (55,283 boxes); every segment mass times $999/1000$, NOT VERIFIED with 209
    uncertified boxes; times $993/1000$, NOT VERIFIED with 217. Each census is the
    source’s.
  - `qx2_zm.py` on the root-9632 window of the cropped cover with every segment mass
    times $999/1000$
    ([`receipts/controls/qx2-scale0999-r9632.log`](receipts/controls/qx2-scale0999-r9632.log)),
    1,704 CPU-seconds: 2,405 boxes and 87 uncertified, the leaf census and the list of
    87 byte for byte the source’s; 3 of the 87 meet a `zmx2` box, and `check_9632.py` on
    it says ROOT-9632-NOT-CLOSED.
  - `locality_check.py` on the one-weight mutation of $\mu_{12}$: LOCALITY FAILED, 176
    of 11,025 windows without an integer translate in $\mu_{11}$, as the source reports.
  - `ctl_rise.py`, the Tight-Tile control: on the real board the control’s chart region
    certifies in 155 cells with none refused; on `ctl_rise.txt`, one segment moved by
    $1/10$, it refuses 443 cells within 2,000, 6 of them at the face point $(1, 1)$,
    every one shown a failed bound.
    The run is capped at 2,000 cells of the script’s default 20,000; a first run at the
    default was stopped after 1,400 cells with 248 refused
    ([`receipts/controls/tight-ctl-rise-stopped.log`](receipts/controls/tight-ctl-rise-stopped.log)).
    The source’s other two Tight-Tile controls are not in the release.

So root 9632 and `zmx2`’s part of the axis face are decided here in full; the rest is a
sample, a diagnostic and not a replay.
In all, the runs here took about 2.5 CPU-hours.

## What Is Not Checked Here

- **Most of the `zmx2` sweep’s cost.** Twenty-five of the 55 columns, 23 to 25, 32 to 42
  and 44 to 54, were not run: 41,389 of the 45,366 CPU-seconds the source recorded, the
  heaviest among them (columns 34 and 35, 17,558 CPU-seconds); nor were the 75 coverage
  dumps (`tight_tile/run_cov.sh`, about 18.3 CPU-hours at the source), which the fast
  mode reads from `cov.tar.xz` and `verify.sh
  --full` does not regenerate.
- **The Tight-Tile jobs.** Only the sample above re-ran; the 323 jobs and 3 reruns
  recorded 1,007,447 CPU-seconds at the source.
  The fast mode’s `summarize_tt.py` and `cov_check.py` read the recorded outputs and the
  dumps; they recompute no cell.
- **The Lean reduction.** Not built: the toolchain `leanprover/lean4:v4.33.1` and its
  Mathlib cache need about 10 GB of disk, and the source reports about 6 GB of memory
  for each kernel-check module.
  Daniel’s `lean/` at `659ee62`, whose `minSide`, `sq`, `box` and mixed-cover measure
  the statement uses, is not retained here.
  The statement of `k2m5_of_valid11` and of `Valid11` was read (`lean/K2m5/Inst.lean`),
  and the axiom list is the source’s report.
- **The axis face beyond `zmx2 cert0`.** Daniel’s Lemma Z run at 10,000 limit corners
  and the authors’ exact axis check at 7,717 corners are named in the paper and
  `docs/CHECKING.md`, but neither their programs nor their outputs are in the release;
  only `cert0`’s record is, and it re-ran here.
- **The mathematics.** The mass lemma, the locality lemma (Lemma 7), the D4 reduction,
  the Tight-Tile Lemma’s charts, cell certificate and corner zones, and `zmx2`’s
  first-order mode and area density, which Daniel’s own notes count among his
  least-reviewed lemmas, are the stage 4 review’s (`think-h10k`). No review here has
  read `zmx2`’s first-order path before; the reviews of 28 September, 2 October and 31
  October read its other modes.
- **The search.** `search/` is not part of the proof and was read, not run.

## The Price of a Full Replay

The fast mode is the 37 CPU-seconds above.
`verify.sh --full` re-runs the `zmx2` sweep and the Tight-Tile jobs and checks coverage
against the shipped dumps; it regenerates neither the 75 coverage dumps nor root 9632’s
runs, and builds no Lean.
A full replay needs all of them.
Each part’s price is its recorded CPU at the source, scaled by this host’s speed
measured on the same programs here:

| Part | Recorded at the source | Here, at the measured speed | Run here |
| --- | --- | --- | --- |
| `zmx2` sweep: `cert0` and 55 columns | 45,366 CPU-s (12.6 CPU-h) | about 14.4 CPU-h, at 1.14 times the source’s CPU over the 30 sampled columns | `cert0` and 30 columns, 4,545 CPU-s |
| The 75 coverage dumps (`tight_tile/run_cov.sh`) | 65,802 CPU-s (18.3 CPU-h) | about 20.9 CPU-h, at the same factor | none |
| Root 9632: the dump and `qx2_zm.py` | 1,834 CPU-s | 0.4 CPU-h | all, 1,507 CPU-s |
| Tight-Tile jobs: 308 and 15, with 3 reruns | 1,007,447 CPU-s (279.8 CPU-h) | about 102 CPU-h at 0.37 times, the factor of the 26 jobs sampled here, all among the cheapest; up to 280 at the source’s own speed, since the largest jobs (up to 66,225 CPU-s) were not sampled | 26 jobs, 252 CPU-s |
| The source’s controls | 3,193 CPU-s for the two whose CPU is recorded | about 0.7 CPU-h | all four, 2,433 CPU-s |
| The Lean build of `lean/K2m5` | not recorded | a few CPU-hours, an estimate; about 10 GB of disk for the toolchain and Mathlib cache, and about 6 GB of memory for each kernel-check module by the source | none |
| **All** | about 313 CPU-h with the Lean build | **about 140 CPU-h, up to about 320** | about 2.5 CPU-h |

`verify.sh --full` alone is about 117 CPU-hours here at these factors, up to about 295.
The full replay is above this lane’s box and the owner’s 40 CPU-hour item cap; it is
held for the owner on `think-0h7r`, which lists subsets under the cap: the Lean build,
and the `zmx2` sweep with the coverage dumps, about 35 CPU-hours.
The tight-tile jobs are nearly all of the rest.

## Questions for the Authors

These hold no rung; they are for the reply on #973.

1. **The dump’s command.** The root-9632 dump lists 6,850 uncertified boxes only when
   `zmx2` runs with a large `--uncert-cap`, as `tight_tile/run_cov.sh` passes for the 75
   dumps (`100000000`); with the default cap of 200 the same root stops at 226 boxes,
   which is what the main sweep’s own records show.
   `zmx2`’s header prints no cap, and the release records no command for
   `verification/r9632/dump.out`. Could it record the command line, and could
   `verify.sh --full` regenerate that dump, the `qx2_zm.py` run on root 9632 and the 75
   coverage dumps, which it now reads from the release rather than recomputing?
2. **The cropped cover.** `verification/r9632/c9632.txt` and its control are made by
   `crop_cover.py`, which is not in the release.
   Every segment of the cropped cover is a segment of the board with its mass, and the
   header and the Lebesgue square are the board’s, as checked here.
   Could the release include the script?
3. **The axis face.** The paper and `docs/CHECKING.md` cite Lemma Z at 10,000 limit
   corners and an exact axis check at 7,717 corners for $\theta = 0$, besides
   `zmx2 cert0`. Neither program nor output is in the release.
   Could they be added?
4. **The Tight-Tile controls.** `docs/CHECKING.md` lists three refused mutations, masses
   times 0.99, the line $x = 2$ lowered by 1%, and one moved segment; only the last,
   `ctl_rise.txt`, is in the release.
   Could the other two be added, with their commands and outputs?
5. **The licence.** `LICENSE` holds the MIT text and names `search/cover_loop.py` and
   `search/tilesep.py`, which are not in this release; the README adds CC BY 4.0 for
   text and data. Could `LICENSE` state the CC BY 4.0 grant and name the files it covers?
6. **The patch step.** `verify.sh --full` applies `zmx2_print_all.patch` with `|| true`,
   so a patch that fails to apply goes unnoticed.
   The sweep does not need the patch, but the dumps do.
   Could the script stop when the patch fails?
7. **The Lean build.** `lean/build.log` keeps the last lines only.
   Could the release keep the whole log with each module’s time and memory, so that a
   rebuild can be priced?
8. **The Zenodo record.** The issue says a DOI will follow; the record will cite it.
9. **The Tight-Tile outputs.** The recorded outputs in `tight_tile/out/` and
   `out_u2000/` lack the `"K"` field the shipped `run_tt.py` prints, so an earlier
   version wrote them. The 26 jobs re-run here agree with them line for line.
   Could the release say which version of `ttbox` and `run_tt.py` ran each job, and
   whether anything but the output changed?

## Compressed Files

Data files of more than 1,000 lines are stored as deterministic gzip made by `gzip -9n`,
with no file name or timestamp in the header.
The table gives the Git blob and SHA-256 of the decompressed bytes, and
`python -m devtools.retained_data check PACKET` re-derives every row.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `k2m5-family/certificate/sol_exact_box11.txt.gz` | upstream | `23821edf4a53e7d712b5048b955e14622c2b83bd` | `d259fed5c9d5eb02c6fed85f5d1070e86d48f5717305f9e056c9a88adbd12099` |
| `k2m5-family/certificate/sol_exact_family.txt.gz` | upstream | `d469a48863ffea129b481e410bcd10fb625fbbe4` | `643c17343574c8aa73a79d9af37b117001be590f99f1e27730019cf3c028cd3a` |
| `k2m5-family/tight_tile/ctl_rise.txt.gz` | upstream | `244560634eb19935ec3309ae5a6fd5730ad3fe1c` | `e41ca6ea2f277b1d9f2610cc953f04fb46402ebdeb9d61869b8f1b351df3c8b9` |
| `k2m5-family/verification/boards/box10.txt.gz` | upstream | `76def5f854b3126756b6c81515bb4ff857b26195` | `c314ab680f4e88671331c3e2d75e1a94bda8ce195bf82910579e7bb675b90901` |
| `k2m5-family/verification/boards/box12.txt.gz` | upstream | `5fab92877ff2d2f9bc7795551f75578203970725` | `1073218ace14f649417f8916035dc2a1aecb0a7c549d71f6ea07720829a22e7d` |
| `k2m5-family/verification/boards/box13.txt.gz` | upstream | `05653fa3383c591b86c1d6f8ab85871bdec2171f` | `4f3d4fef14b2eb933c390924af532323b37bdc1cfda4fe62295c295d25497823` |
| `k2m5-family/verification/boards/box20.txt.gz` | upstream | `fa2fd247dfb963a8239c02a8fd58a4d26e49a1ee` | `30a2715322aedd58487c23c64a723699c42e363efc5436896e7646809e165e19` |
| `k2m5-family/verification/controls/box12_onemutation.txt.gz` | upstream | `ce545eda70ce0511f2cfca9928ca1f9527c9f0d4` | `24a71da62e0ec718aeb64027e8750596d375affbbc2ef2b314a32e8d2083afcf` |
| `k2m5-family/verification/controls/scale0993_box11.txt.gz` | upstream | `2a6aef05118101fbaa5aa7419bc2c1173d4a4d5a` | `e1a3658ae3d555735af4fd4644ae247f864c0a77af8190e25ca30f452ca6b021` |
| `k2m5-family/verification/controls/scale0999_box11.txt.gz` | upstream | `364bca861883b4180b395243a03ab77b24206184` | `f75c36e4f653a4eea4461411cd796e5c2fbc9e07320e895a119dba79309db591` |
| `receipts/compare.json.gz` | receipt | `a663991527843056414ac8a6a391680bc55d7aed` | `303091215fd7850b94b756318c4150c11ec91a3b5751b44eada58b1d8cf48078` |
| `receipts/r9632/dump.log.gz` | receipt | `48dab02e6bb20fdfe88b0b14a4aa2a78a73bfffe` | `d8ba5f205e3376e7fcf7e46e1823b907c4316402191d4c356a2d68b5916cd0cb` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
