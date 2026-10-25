# wand125’s `sqverify_continuous` v4, 12 October

Commit `d4a1981` of wand125/square-packing (12 October 2026) is v4 of
`tools/sqverify_continuous`: this repository’s `sqverify_fast` crate with a
continuous-angle mode, `sqverify-fast --continuous`, which checks a rectangle-density
certificate at every orientation and every centre and concludes $s(n) > L/B$.
v4 adds `--resume` to v3 (`f30cc2c`, the packet
[`wand125-sqverify-continuous-v3-2026-10-12`](../wand125-sqverify-continuous-v3-2026-10-12/README.md));
the search is the same.
It is the source’s first program for T-192 (route A, think-0arj) and a second route for
T-145 and T-157 (think-xzob, jlevy/squares#533).
The [soundness review of 23 October 2026](../../../../docs/project/reviews/review-2026-10-23-wand125-sqverify-continuous-soundness.md)
read it, and its programs and receipts are in [`review/`](review/README.md).

| Item | Value |
| --- | --- |
| Source | [`tools/sqverify_continuous`](https://github.com/wand125/square-packing/tree/d4a19815e2b0cca5faa562f00c7a80b93d3402ef/tools/sqverify_continuous) |
| Pin | `d4a19815e2b0cca5faa562f00c7a80b93d3402ef`, committed 2026-10-12T01:29:29Z by Hiroaki Hosono, “tools/sqverify_continuous: v4, --resume for interrupted runs” |
| The same tree | Git tree `2734b434…` at `8530baf` (the n = 28 certificate’s pin) and at the head `e48de243` read on 2026-10-23; the n = 28 release asset’s `check1/src/sqverify_continuous_v4.tgz` (`72086975…`) unpacks to it byte for byte |
| Retrieved | 2026-10-23T06:52:05Z, a blobless clone of the single public branch, sparsely checked out |
| Version | v4, `source_sha256` `619b3c00bd918b329b4141c24ee30b027af7f88b86bcf2886e3c18855a61c7f5` by `build.rs`’s rule, recomputed here |
| Build here | rustc 1.98.0, `cargo build --release --locked`: binary `31936c4dcfac398b729990f51820fd5a5b70e23a2e809b71de1ca5864e6de618`, the digest the n = 28 import’s build of 15 October recorded |
| Issue | jlevy/squares#533 (review and replay); the replay budget line is on #543 |

## What Is Retained

[`devtools.acquire_source`](../../../devtools/acquire_source.py) wrote the packet from
its [declaration](acquisition/declaration.json); the
[acquisition record](acquisition/sources.json) and the
[subtree manifest](acquisition/upstream-subtree.sha256) give the size and SHA-256 of the
31 files in scope, and `--check` re-derives them.
Twenty-nine are retained byte for byte under
[`square-packing/`](square-packing/tools/sqverify_continuous/): all 28 files of
`tools/sqverify_continuous` (the crate with its sources, tests, lockfile, toolchain pin,
build script and documents, `patches/continuous.diff`, `examples/n40/`, `README.md` and
`PROVENANCE.md`) and `tools/THIRD_PARTY_NOTICES.md`.
Two are pinned by digest only, each byte-identical to a copy the
[closed-form cfcheck packet](../wand125-closed-form-cfcheck-2026-10-14/README.md) retains:
the repository’s licence index `LICENSE.md` and wand125’s MIT `tools/LICENSE`.
No file is compressed.

Not retained: the rest of the repository, which the pin binds, and the n = 28 release
asset, which the [n = 28 packet](../wand125-continuous-n28-2026-10-15/README.md) pins by
size and digest.

## Licence and Credit

`LICENSE.md` says each top-level folder keeps its own licence; `tools/LICENSE` is MIT,
Copyright (c) 2026 wand125. `PROVENANCE.md` gives the crate’s code as MIT, the upstream
code by Joshua Levy and wand125’s changes under the repository’s MIT, and the copied
upstream documentation (`sqverify_fast/README.md`, `SOUNDNESS.md`, `INDEPENDENCE.md`,
`independence-record.yaml`) as CC BY 4.0 to “Joshua Levy, the squares project”;
`tools/THIRD_PARTY_NOTICES.md` states the same. `CONTINUOUS.md`, `PROVENANCE.md`,
`README.md`, `patches/` and `examples/` are wand125’s, MIT.

The commit is authored by Hiroaki Hosono (wand125) and names Claude (Anthropic) as
co-author; `PROVENANCE.md` says the mode’s author read Guzhou0806’s
`verifier/continuous_pose.cpp` while reviewing T-145 (jlevy/squares#485) before writing
it, that it shares no code with that kernel, and that it is “independent code, but not an
independent method”. Its `README.md` names this repository’s `sqverify_fast` as its base
and Guzhou0806/n40-square-packing as the first all-angle n = 40 bound.

## The Review’s Programs and Receipts

The [review](../../../../docs/project/reviews/review-2026-10-23-wand125-sqverify-continuous-soundness.md)
ran only programs it wrote and the verifier built from this packet;
[`review/README.md`](review/README.md) says what each program does, what it read, how to
run it and what it printed. None of them decides a claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
