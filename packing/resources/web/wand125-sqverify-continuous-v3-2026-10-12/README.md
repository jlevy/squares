# wand125’s `sqverify_continuous` v3, 12 October

Commit `f30cc2c` of wand125/square-packing (12 October 2026) is v3 of
`tools/sqverify_continuous`, the first published version of the continuous-angle mode
`sqverify-fast --continuous`, and the version the source’s n = 40 examples ran: its
`README.md` reports $s(40) > 1340000/199529$ (T-145’s density) and $s(40) > 3359/500$
(T-157’s) `VERIFIED` at all 86 root ranges, and their controls `REFUSED`, with no run
output published. Its child `d4a1981`, 29 minutes later, is v4, retained in full as the
packet [`wand125-sqverify-continuous-v4-2026-10-12`](../wand125-sqverify-continuous-v4-2026-10-12/README.md);
the [soundness review of 23 October 2026](../../../../docs/project/reviews/review-2026-10-23-wand125-sqverify-continuous-soundness.md)
read both (think-xzob, jlevy/squares#533).

| Item | Value |
| --- | --- |
| Source | [`tools/sqverify_continuous`](https://github.com/wand125/square-packing/tree/f30cc2cf345a3a3f6af778925f354d9ec979868b/tools/sqverify_continuous) |
| Pin | `f30cc2cf345a3a3f6af778925f354d9ec979868b`, committed 2026-10-12T01:00:19Z by Hiroaki Hosono, “tools: sqverify_continuous, sqverify_fast with a continuous-angle mode (v3)” |
| Retrieved | 2026-10-23T06:52:05Z, the same clone as the v4 packet’s, sparsely checked out at this commit |
| Version | v3, `source_sha256` `1266a8b90f9a355d74772e211a7b9a52d0236b0d33cc4113d2f897d8a1044f33` by `build.rs`’s rule, recomputed here from this packet and the v4 packet’s identical files |
| Issue | jlevy/squares#533 |

## What Is Retained

[`devtools.acquire_source`](../../../devtools/acquire_source.py) wrote the packet from
its [declaration](acquisition/declaration.json); the
[acquisition record](acquisition/sources.json) and the
[subtree manifest](acquisition/upstream-subtree.sha256) give the size and SHA-256 of the
31 files in scope, and `--check` re-derives them.
The seven files that v4 changes are retained byte for byte under
[`square-packing/`](square-packing/tools/sqverify_continuous/): `README.md`,
`PROVENANCE.md`, `patches/continuous.diff`, and the crate’s `CONTINUOUS.md`,
`src/main.rs`, `src/slab.rs` and `src/slab_tests.rs`.
The other 24 are pinned by digest only, each byte-identical to a copy another packet
retains: 22 to the v4 packet’s (every other file of the directory and
`tools/THIRD_PARTY_NOTICES.md`), and `LICENSE.md` and `tools/LICENSE` to the
[closed-form cfcheck packet](../wand125-closed-form-cfcheck-2026-10-14/README.md)’s.
No file is compressed.

What v4 changes, measured by the review’s
[custody receipt](../wand125-sqverify-continuous-v4-2026-10-12/review/receipts/custody.json):
in `slab.rs`, only `Params` and `run` (output written as each root ends, a `run_key`
on every line, and `--resume`); `run_root` and every function it calls are the same
text, so the two versions accept and refuse the same inputs without `--resume`. Run here,
v4 reproduces the v3 README’s three control rows node for node.

## Licence and Credit

As the v4 packet’s: `tools/LICENSE` is MIT, Copyright (c) 2026 wand125, for the code, and
the copied documentation of this repository’s `sqverify_fast` is CC BY 4.0 to “Joshua
Levy, the squares project”. The commit is authored by Hiroaki Hosono (wand125) and names
Claude (Anthropic) as co-author; `PROVENANCE.md` says the mode is independent code but not
an independent method, its author having read Guzhou0806’s kernel before writing it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
