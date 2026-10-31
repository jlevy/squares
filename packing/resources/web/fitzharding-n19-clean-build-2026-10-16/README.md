# Fitzharding: The Author’s Clean Rebuild of the s(19) Lean Proof, Pinned 2026-10-31

This packet retains the one commit of
[ofitzharding/sq19](https://github.com/ofitzharding/sq19) past the
[`fitzharding-n19-lean-2026-10-16`](../fitzharding-n19-lean-2026-10-16/README.md)
packet’s pin `34fb2b7` (tag `v1.0.0`), the proof T-194 registers.
That commit, `c86a991`, adds the author’s receipt and log of a clean rebuild of `v1.0.0`
from source and a paragraph on it in `README.md`. The proof itself is unchanged.

It is the source build that issue #640 said had not been run.
It is new evidence for T-194, the author’s own execution and not a replay here.
Bead `think-a4x3` imports it.
Nothing in the packet changes a rung: admitting a producer’s build is the source-build
audit that [epistemics.md](../../../../epistemics.md#reported-formal-proofs-and-source-builds)
describes, and it has not been done (below).

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/ofitzharding/sq19> |
| Revision | [`c86a991ea1379d1598739182f5f26619c9b7126a`](https://github.com/ofitzharding/sq19/tree/c86a991ea1379d1598739182f5f26619c9b7126a), tree `b20bedf1`, “Add clean source rebuild receipt and log” |
| Committed | 2026-10-16T14:28:55Z (10:28:55 in the commit’s −04:00), author and committer Oscar Fitzharding; the commit carries the trailer “Co-Authored-By: Claude Opus 5.5” |
| Parent | `34fb2b7`, the earlier packet’s pin and `v1.0.0` |
| Retrieved | 2026-10-31T05:07Z, a full clone; `main` pointed at this commit, its seventh |
| Licence | MIT: `LICENSE` (unchanged, retained by the earlier packet), “Copyright (c) 2026 Oscar Fitzharding”; `README.md`, “MIT License.” |
| Request | [Issue #640](https://github.com/jlevy/squares/issues/640) |
| Bibliography key | **[Fitzharding n19 Lean 2026]**, the key of the earlier packet |

## What Is Retained

[`devtools.acquire_source`](../../../devtools/acquire_source.py) wrote the packet from
its [declaration](acquisition/declaration.json); the
[acquisition record](acquisition/sources.json) and the
[subtree manifest](acquisition/upstream-subtree.sha256) give the size and SHA-256 of the
three files the commit changes, and `--check` re-derives them.
All three are retained under [`sq19/`](sq19/): `README.md`,
[`verification/clean-build-receipt.json`](sq19/verification/clean-build-receipt.json)
and `verification/clean-build.log`, stored as deterministic gzip (26,639 lines).
Every other file of the tree is byte-identical to the earlier packet’s copy at `34fb2b7`.

## What the Commit Reports

The receipt says a fresh clone of `v1.0.0` was built with `bash scripts/fetch.sh`, which
downloads the release’s certificate sources and checks their digests, and then
`python3 scripts/verify.py --kernel-replay`. It says no precompiled project objects were
used, only the pinned Mathlib build cache.

| Field | Receipt |
| --- | --- |
| Commit built | `34fb2b7bc39465db368c45cb48d4db58829d3051` |
| Run | 2026-10-16T07:23:41Z to 12:42:15Z, 19,114 s of wall |
| Machine | Ubuntu 24.04, Linux x86-64, 64 vCPUs, 512 GB, Lean 4.34.1 |
| Built from source | 2,400 modules |
| Statement | `Sq19.square19_optimality : ∀ (L : ℝ), Sq19.Feasible19 L ↔ 3 + 4 * √2 / 3 ≤ L` |
| Axioms | `Classical.choice`, `Quot.sound`, `propext` and 4,320 `native_decide` checks |
| Kernel replay | 13,143 modules, 0 failures |
| Against the research build | 2,399 modules compared: 2,177 byte-identical and 222 different; every generated certificate module identical, the differing ones hand-written modules that this route builds with Lake |
| Result | `VERIFIED` |

The statement and the axiom list are the ones T-194 records.
At 64 vCPUs for 5 h 18 min the run is at most about 340 CPU-hours.

**Checked here, from the retained bytes only.** The log’s SHA-256,
`9ad3ac1e4853aa633ceb231330fab145bc3db257c649a982c6971be86e194dfb`, is the
`log_sha256` the receipt states. The log’s timestamps run from 07:24:48 (`lake exe cache
get`) through the build of the hand-written base modules and checker C code (07:27:56),
the native checker library (07:31:07) and the numbered build steps to `[2119/2119]
Sq19Lean.Assembly.FinalReport` at 12:11:29, then the final theorem’s statement and
axioms, `kernel replay: 13143 modules, 0 failures` and `VERIFIED`.
Nothing here built a module, ran the source’s scripts or compared any build product.

## What It Changes in the Record

It answers the triage’s question whether a source rebuild ran. The answer is the
author’s own execution, so it raises no C rung. An admitted producer build can earn V3,
but only through a source-build evidence entry with a retained `build_receipt`, an
`axioms_receipt`, full coverage and a dated audit of the build’s pins, completeness,
statement fidelity and trust boundary.
That audit is owed to `think-a4x3`, and the from-source build here stays held on the
machine (`think-nqnl`), now priceable against this run.

## Compressed Files

| Stored file | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `sq19/verification/clean-build.log.gz` | upstream | `ffd91b3b5180218530ce18d6b3156d510cedd2df` | `9ad3ac1e4853aa633ceb231330fab145bc3db257c649a982c6971be86e194dfb` |

`gunzip -k sq19/verification/clean-build.log.gz` restores the upstream bytes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
