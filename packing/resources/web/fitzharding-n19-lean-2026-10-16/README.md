# Fitzharding: A Lean Proof That s(19) = 3 + 4√2/3, Pinned 2026-10-16

This packet retains [ofitzharding/sq19](https://github.com/ofitzharding/sq19) at the
head of `main` and tag `v1.0.0` on 16 October 2026: a Lean 4 proof that Robert
Wainwright’s 1979 packing of nineteen unit squares is optimal. Its theorem is

```lean
Sq19.square19_optimality (L : ℝ) :
  Feasible19 L ↔ 3 + 4 * Real.sqrt 2 / 3 ≤ L
```

The side is $3 + 4\sqrt{2}/3 \approx 4.8856180831641267$. The source trusts Lean’s
compiler and native evaluator for 4,320 `native_decide` facts. It reports a kernel replay
of the theorem’s 13,143-module import closure with no failure, and says it has not yet
run a complete rebuild from source.

The author, Oscar Fitzharding, announced it on X as
[@ofitzharding](https://x.com/ofitzharding/status/2110935681597874374) at
2026-10-16T03:27:40Z. He asked for its registration on this repository in
[issue #640](https://github.com/jlevy/squares/issues/640), opened at 2026-10-16T03:41:08Z.
Bead `think-a4x3` imports it, and its triage is in that bead and in the issue’s entry in
`packing/campaign/result-requests.yaml`. On 16 October the owner asked for the
announcement to be recorded and the repository watched (`think-xik9`); this packet’s
acquisition record is what makes the intake sweep watch it. Nothing in the packet is a
register entry, and nothing here built the proof or ran the source’s scripts.

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/ofitzharding/sq19> |
| Revision | [`34fb2b7bc39465db368c45cb48d4db58829d3051`](https://github.com/ofitzharding/sq19/tree/34fb2b7bc39465db368c45cb48d4db58829d3051), tree `f5192ae5`, “README: shorten”, the last of six commits |
| Committed | 2026-10-16T03:20:12Z (23:20:12 on 15 October in the commit’s −04:00), author and committer Oscar Fitzharding |
| History | `0ffc604` 02:15:45Z, “s(19) optimality: Lean proof sources, verification script and records”, holds the proof; `22023ba`, `a1e09e9`, `c1411f0` and `9c2686b` (03:03Z to 03:09Z) and the pin change only `README.md`, `scripts/verify.py` and `verification/kernel-replay.json`. Every commit carries the trailer “Co-Authored-By: Claude Opus 5.5” |
| Release | `v1.0.0`, published 2026-10-16T02:38:08Z; five archives and `SHA256SUMS` (below). The tag now points at this commit, which was made 42 minutes after publication, so it was moved to `34fb2b7` afterwards (GitHub keeps no tag history this session could read, so the commit it first named is not recorded). The pins still hold: the commits after `0ffc604` change only `README.md`, `scripts/verify.py` and `verification/kernel-replay.json` (History, above), so no file the archives or `fetch.sh`'s digest check depend on, `expected/generated-sources.sha256` included, changed in between |
| Retrieved | 2026-10-16T04:12Z, a full clone; `main` and `v1.0.0` pointed at this commit |
| Licence | MIT: `LICENSE`, “Copyright (c) 2026 Oscar Fitzharding”; `README.md`, “MIT License.” |
| Announcement | @ofitzharding (display name “Oscar”, account 2097726704118603776, the account that announced the s(17) proof), 2026-10-16T03:27:40Z, retained as [`receipts/announcement/tweet-2110935681597874374.json`](receipts/announcement/tweet-2110935681597874374.json), the post as X’s syndication endpoint returned it at 2026-10-16T04:58:12Z (2,278 bytes, SHA-256 `1af584d9777af2ed54c0f64e98bfe209911d7dfdb63217cfb77a9646cd65b3b5`) |
| Request | [Issue #640](https://github.com/jlevy/squares/issues/640), “Complete Lean proof of s(19) optimality: registration request”, opened by ofitzharding at 2026-10-16T03:41:08Z |
| Bibliography key | **[Fitzharding n19 Lean 2026]**, defined in `bibliography.yaml` by the change that registers the result |

## Credit and AI Assistance

`CITATION.cff` names one author, given name Oscar and family name Fitzharding, version
1.0.0, released 2026-10-16, and asks: “If you use this formal proof or its verification
software, please cite this release.” `LICENSE` carries the same name.

`README.md`, section Credits, reads in full:

> Builds on the [s(17) formalization](https://github.com/ofitzharding/sq17-lean).
> Thanks to everyone involved with the [Squares Project](https://github.com/jlevy/squares),
> especially Manasseh Ahmed ([@Queuingtheorydotcom](https://github.com/Queuingtheorydotcom)).
> Developed with substantial assistance from Claude and Codex.

Issue #640 adds: “Robert Wainwright supplied the 1979 construction. The proof extends
the method and checker code of the s(17) Lean proof (#565).” It credits Oscar
Fitzharding and says “Development used Claude and Codex assistance.” The s(17) proof is
[`[Fitzharding n17 Lean 2026]`](../fitzharding-n17-lean-2026-10-13/README.md), T-154.

The announcement reads, in full: “lol here’s a lean proof of the optimal packing for 19
squares”. It links this repository and an image.

**AI assistance, in the source’s own terms.** `README.md`: “Developed with substantial
assistance from Claude and Codex.” The issue: “Development used Claude and Codex
assistance.” Every commit names Claude Opus 5.5 as co-author.

## What the Source Claims

- **The statement.** `Feasible19 L` (`Sq19Lean/Assembly/PlainPacking.lean`) says there
  are 19 sets, each `IsUnitSquare`, the closed square `sq cx cy ux uy` with
  $u_x^2 + u_y^2 = 1$ (`Sq19Lean/SquareBase.lean`, copied from sq17-lean v1.0.0), each
  inside $[0, L]^2$, with pairwise disjoint interiors. Rotations are arbitrary and
  boundary contact is allowed. `side19 = 3 + 4 * Real.sqrt 2 / 3` (`Sq19Lean/Basic.lean`).
  Existence at the endpoint is `endpoint_packing` (`Sq19Lean/EndpointPacking.lean`), and
  that file uses no `native_decide`. `expected/statement.txt` is the statement the
  source’s script compares the build with.
- **The trust boundary.** `verification/Square19Optimality.log` and
  `expected/axioms.txt` list `propext`, `Classical.choice`, `Quot.sound` and 4,320
  `native_decide` facts, and no `sorryAx`. `scripts/verify.py` compiles six checker
  modules to C and links them into the library that `native_decide` runs, so the C
  toolchain is trusted as well.
- **The kernel replay.** `verification/kernel-replay.json`: `LeanChecker.replayFromImports`
  over every module of the import closure of `Sq19Lean.Assembly.FinalReport`, 13,144
  modules, the theorem module’s closure of 13,143 plus the report module. There were 0
  failures: 2,400 project modules in 12m57s and 10,744 Mathlib and standard-library
  modules in 24m04s, on 64 cores. It ran on the compiled objects of the research build of
  15 October, and was repeated by `scripts/verify.py --kernel-replay` on 16 October. A
  kernel replay takes the `native_decide` facts as axioms.
- **What it has not done.** Issue #640: “A complete from-scratch rebuild with the
  published script takes several hours on 64 cores and has not yet been run, so
  independent reproduction is very welcome.”

The build pins are Lean `v4.34.1` (`lean-toolchain`), Mathlib `v4.34.1` at `d13f23b7`, and
sq17-lean at `0a7167efa8dcae7fa73855890630fb7e2de550ed` (`lake-manifest.json`), whose
`Sq17Lean` modules `lakefile.toml` compiles in place as the half-plane checker. That
commit is sq17-lean’s `v1.0.0`, the revision T-154 cites. The
[s(17) packet](../fitzharding-n17-lean-2026-10-13/README.md) pins `e6ee548`, whose tree
differs from it only by `CITATION.cff`, and its `manifest.json` gives every module’s
SHA-256.

## The Release Archives

The 2,112 generated certificate modules are not in the Git tree.
`scripts/fetch.sh` downloads the five archives of release `v1.0.0`, checks each against
`SHA256SUMS`, extracts them, and checks every extracted file against
`expected/generated-sources.sha256`, which this packet retains.

| Archive | Bytes | SHA-256 |
| --- | --- | --- |
| `sq19-generated-census.tar.xz` | 296,168,032 | `507ac0953372631d7202e0ed01fda46166f59ef2e5e8c9f0bd6ad6aa6f55b542` |
| `sq19-generated-S3435.tar.xz` | 520,505,480 | `9c919f688d5fe5029162e82f1705b8f3309e129340d70ab18fafce65dbc457a3` |
| `sq19-generated-S3438.tar.xz` | 73,115,752 | `ec7692082475aa37a32cbc2445ff973d1e54dabcd78e2d57f5204df8326a5d57` |
| `sq19-generated-S3442.tar.xz` | 113,206,288 | `641a76a81fa1acbd0aad79ddeca870d7a166f1dd45b0cbe8b19db7ac05f6d91b` |
| `sq19-generated-survivors.tar.xz` | 107,592,684 | `0c134b5953675f39c81ffc2469703ebdeaddf87f73f83a741525523ba2f5a5f4` |

Together they are 1,110,588,236 bytes. `SHA256SUMS` (475 bytes, SHA-256
`218f59d01bf21cbb850574cdf077ce632caf05a6bc7e12f8daa15a20f5fc2751`) was downloaded here
on 16 October 2026, and its five digests equal the ones GitHub reports for the assets. The
archives were not downloaded, and their bytes are not retained (`OR-18`); they are
pinned here by name, size and SHA-256.

## What Is Retained

Every tracked file of the pin, 243 files and 3,360,904 bytes, is in the manifest
([`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256)) and is
retained under [`sq19/`](sq19/), byte-identical, two of them as deterministic gzip (below).
That is the root files and build pins, the 89 hand-written modules under `Sq19Lean/`,
the 137 certificate modules under `s19/certificates/` (the endgame shards and assembly
blocks), the scripts, `expected/` and `verification/`. A mathematical review
(`think-o40t`) needs all of it. The packet retains `sq19/.gitignore`, which names only
the paths of generated modules and build outputs. Nothing in the tree is pinned by digest
only. **Not retained:** the five release archives above.
[`devtools.acquire_source`](../../../devtools/acquire_source.py) `--check` re-derives the
packet from its manifest.

## Receipts

- [`receipts/announcement/tweet-2110935681597874374.json`](receipts/announcement/tweet-2110935681597874374.json)
  is the announcement as X’s syndication endpoint returned it.
- `sq19/verification/` is the source’s own receipt, retained as published. Nothing here
  built a module, ran `#print axioms`, or ran `fetch.sh` or `verify.py`. The full build
  is priced in `think-nqnl`, above the intake’s 40 CPU-hour cap.

## Compressed Files

| Stored file | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `sq19/expected/axioms.txt.gz` | upstream | `9848add16d4ee6dbc46f014dc23e486906eb2bb5` | `84367f34dae85905be43339f1155e019fe8ba8864d5c34c4696fa9fdfba0fd8e` |
| `sq19/verification/Square19Optimality.log.gz` | upstream | `721cfaf7572795f2f00fe615ad383b9a9b94e5e3` | `bfe8c69fd7ddcecaeed52e95b31cf8a8a6a913eda5b631b53b4a1c28c0ef9b37` |

`gunzip -k sq19/expected/axioms.txt.gz sq19/verification/Square19Optimality.log.gz`
restores the upstream bytes.

## Commands

From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.acquire_source \
  fitzharding-n19-lean-2026-10-16 --check
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
