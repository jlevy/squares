# Greff: The Second Route for s(76) = 9, zm_mixed Alone, Pinned 2026-10-31

This packet retains the one commit of
[bengreff/s76-certificate](https://github.com/bengreff/s76-certificate) past the
[`bengreff-s76-certificate-2026-10-14`](../bengreff-s76-certificate-2026-10-14/README.md)
packet’s pin `1cb924f`, the source T-184 registers.
That commit, `0699398`, adds the second route that issue #594’s comment of 14 October
described: Evan Daniel’s exact-rational checker `zm_mixed.py` alone over all 129,600 D4
roots of the cover, without `zmx2`, with its per-root records.
The cover, the composite’s records and the Lean wrapper are unchanged.

It is new evidence for T-184, the author’s own run and not a replay here.
Bead `think-osvq` imports it.
Nothing in the packet changes a rung (below).

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/bengreff/s76-certificate> |
| Revision | [`06993982e83dba37ca12121bd876396a15571fcb`](https://github.com/bengreff/s76-certificate/tree/06993982e83dba37ca12121bd876396a15571fcb), “Add the second route: zm_mixed alone over the whole region, with R rerun at depth 34” |
| Committed | 2026-10-14T08:16:10Z (03:16:10 in the commit’s −05:00), author and committer Benjamin Greff; the commit carries the trailer “Co-Authored-By: Claude Opus 5.5” |
| Parent | `1cb924f`, the earlier packet’s pin |
| Retrieved | 2026-10-31T05:07Z, a full clone; `main` pointed at this commit, its fifth |
| Licence | MIT, copyright 2026 Benjamin Greff (`LICENSE`, unchanged, retained by the earlier packet) |
| Request | [Issue #594](https://github.com/jlevy/squares/issues/594) |
| Bibliography key | **[bengreff s76 certificate 2026-10-14]**, the key of the earlier packet |

## What Is Retained

[`devtools.acquire_source`](../../../devtools/acquire_source.py) wrote the packet from
its [declaration](acquisition/declaration.json); the
[acquisition record](acquisition/sources.json) and the
[subtree manifest](acquisition/upstream-subtree.sha256) give the size and SHA-256 of the
twelve files the commit changes, and `--check` re-derives them.
All twelve are retained under [`s76-certificate/`](s76-certificate/): `README.md`,
`SHA256SUMS`, `verify.sh`, `records/toolchain.txt`, `tools/check_full.py` and the seven
files of [`records/zm_full/`](s76-certificate/records/zm_full/).
The two upstream `.gz` files are kept as published
([Original Gzip Files](#original-gzip-files)); their SHA-256 are the ones the tree’s
`SHA256SUMS` lists.
Every other file of the tree is byte-identical to the earlier packet’s copy at `1cb924f`.

## What the Commit Reports

| Run | What it reports |
| --- | --- |
| Full pass | `zm_mixed.py cert --d4 --cert-mode --disj --chain-from 0 --pitch 1/20 --ubins 16 --depth 24 --nproc 24` over the whole region: 129,600 roots of 1/20 × 1/20 × 1/32, 2,227,114 boxes, 6 uncertified, all in one root, so the pass’s own verdict is `NOT VERIFIED` (`records/zm_full/manifest.json`, `full.log.gz`) |
| Rerun of R | The one root R = [27/20, 7/5] × [13/10, 27/20] × [1/4, 9/32] alone at depth 34: 13,767 boxes, maximum depth 26, none uncertified, `VERIFIED-D4 (PARTIAL)` (`rerun_R_depth34.log`, `.jsonl`, `.sh`; `rerun.txt` lists it) |
| Records | `roots.jsonl.gz`: a header and one record per root, 129,601 lines. Its header and the rerun’s name `zm_mixed.py` `ee3e2915…`, `mixed_cover.py` `bb89de15…`, `zeromargin.py` `640fe453…` and the cover `b6a1214b…`, the digests the earlier packet and `verify.sh` pin |
| Cost | 651,314 CPU-s (181 CPU-hours) over 27,729 s of wall on 24 processes, 2026-10-13 19:31 to 2026-10-14 03:13 CDT; the rerun 2,661 CPU-s (`records/toolchain.txt`) |
| Checker of the records | `tools/check_full.py`: every root has a record, each header names this cover and the pinned checker files, and each root is certified by the full run or a rerun. `verify.sh` applies it to the shipped records by default and, with `--full-zm`, repeats the pass and the reruns |

The source’s `README.md` adds that R lies in a corner taken unchanged from wand125’s
s(59) cover, whose full `zm_mixed` run also left 6 boxes there and certified it alone at
depth 34 with 13,767 boxes. It concludes that the covering statement holds by
`zm_mixed`’s exact arithmetic alone, as well as by the composite.

**Checked here, from the retained bytes only.** The two `.gz` files’ SHA-256 equal the
tree’s `SHA256SUMS`, and `roots.jsonl.gz` decompresses to 129,601 lines.
Nothing here ran `check_full.py`, `zm_mixed.py` or `verify.sh`, or read the records
beyond that line count and the headers quoted above.

## What It Changes in the Record

T-184 holds the composite replay (`E-bengreff-594-cover-replay`).
This second route is the author’s execution, so it raises no rung.
It makes the records-only audit cheap: `check_full.py` and an exact reader of
`roots.jsonl.gz` take minutes, and the rerun of R is 2,661 CPU-s.
The full pass here stays priced at about 155 to 181 CPU-hours, above the owner’s 40
CPU-hour item cap, and owned by `think-osvq`.

## Original Gzip Files

The two upstream files whose own names end in `.gz` are retained as published, never
recompressed. The table binds their compressed bytes: the Git blob and SHA-256 of each
stored file, which are its blob at the pinned commit and the digest the source’s
`SHA256SUMS` lists.

| Stored path | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `s76-certificate/records/zm_full/full.log.gz` | upstream | `fffa79d53489409220f43f0f76b0e4a695c7c72b` | `5ae17cf0583683d7d251cfcabe854472649141f99fa196879270f5f48f63e538` |
| `s76-certificate/records/zm_full/roots.jsonl.gz` | upstream | `6e483932623ba97b76e74aa3a3ce067451fbf09e` | `cfea95f9b23eb1836c3a2531b516bd2d0d42f42f7bcff34e5164877e6bb657f1` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
