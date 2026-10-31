# Khalili and Gharabaghi’s Certificate for s(44) = 7, Pinned 2026-10-29

This packet pins the whole of
[moh63-dev/s44-equals-7](https://github.com/moh63-dev/s44-equals-7) at its head of 29
October 2026, tag v1.1, for one registration request:
[jlevy/squares#842](https://github.com/jlevy/squares/issues/842), opened by Mohsen
Khalili and Sara Gharabaghi (`moh63-dev`) at 2026-10-26T23:46:23Z, which reports
$s(44) = 7$. The upper half is the $7 \times 7$ grid; the new claim is the lower bound
$s(44) \ge 7$, by a closed mixed cover in Evan Daniel’s format decided by his checker
`zmx2`. When it was retrieved the record held $s(44)$ open at
$2789/400 = 6.9725 \le s(44) \le 7$ (Hosono, T-090,
[`n-044.md`](../../../frontier/n-044.md)).

It is the case $k = 7$ of $s(k^2 - 5) = k$, after T-066 ($k = 8$), T-184 ($k = 9$) and
T-191 ($k = 10$), and its import follows T-066’s, whose cover `zmx2` also decides whole
in both modes. Its Frontier key is **[Khalili Gharabaghi s44 cover 2026-10-29]**. The
claim below is stated as the source states it; what was checked here is in
[Checks Made Here](#checks-made-here), and the stage 4 review is
[review-2026-10-31-khalili-gharabaghi-s44-mixed-cover.md](../../../../docs/project/reviews/review-2026-10-31-khalili-gharabaghi-s44-mixed-cover.md).

## Source and Pin

| Field | Value |
| --- | --- |
| Source | <https://github.com/moh63-dev/s44-equals-7> |
| Revision | `b5b1bc9d7354a8f62efcb6b7abeb30d1eb576aaf`, tag v1.1, branch `main`, tree `6a63c99e7b103bffd649a5ca618820aba8cac7d3`: the head when retrieved, and the revision the issue’s comment of 2026-10-29T15:58:14Z names |
| Committed | 2026-10-29T15:20:35Z |
| History | Two commits by Mohsen Khalili. `063c4d656212a7cf7cc0d104f2846f05b6b043c9` (tag v1.0, 2026-10-26T23:30:49Z), the commit the issue body names, adds the certificate, the logs, the paper and the scripts; `b5b1bc9` adds `verification/zm_mixed_check.py` (a two-stage driver and an audit of the recorded logs), edits `README.md` and `verification/verify.sh`, adds `.gitignore` and deletes `.DS_Store`. The certificate is byte for byte the same at both |
| Licence | MIT, “Copyright (c) 2026 Mohsen Khalili and Sara Gharabaghi” (`LICENSE`), for the scripts; the README releases the certificate into the public domain (CC0) |
| Retrieved | 2026-10-31T04:58Z: a full clone of `main` |
| Pinned subtree | `LICENSE`, `README.md`, `certificate/`, `paper/`, `search/` and `verification/`: 212 files, 9,083,065 bytes, each by SHA-256 in [`acquisition/upstream-subtree.sha256`](acquisition/upstream-subtree.sha256) |
| Retained here | All 212, byte-identical at their upstream paths under [`s44-equals-7/`](s44-equals-7/); three of more than 1,000 lines are stored as deterministic gzip ([Compressed Files](#compressed-files)). `.gitignore` is not retained |
| Certificate | `certificate/s44_cover_7.txt`, SHA-256 `c9fde0f1e7013f3f61f4a8d673b6bcaf9c5e54c914b6462164d7326ba254cae0`, the issue’s and `certificate/SHA256SUMS`’s |
| The issue | [#842](https://github.com/jlevy/squares/issues/842), labelled `intake`, and its one comment, announcing v1.1 and the paper at <https://doi.org/10.5281/zenodo.23769766> |

The checker is not in the tree. `verify.sh` clones evand/square-packing at
`659ee62e4a9d39542a1146e8b011cc3ab6407ede` and builds `verify2/`; this repository
retains the inputs of that build byte for byte: `verify2/src/bin/zmx2.rs`
(`e2bb84e9e05938db416940ad608d2583ca9a0c248d59820937c4ce59d607ead7`) in the
[evand-square-packing-2026-10-04 packet](../evand-square-packing-2026-10-04/README.md),
and `Cargo.toml` and `Cargo.lock` in that packet and the 26 September one. At `659ee62`
`verify2/src/main.rs` differs from the retained copy; it builds the separate `zmcheck`
binary and nothing of it is in `zmx2`. The second checker’s files, `zm_mixed.py`
`1fd20346…` and `mixed_cover.py` `bb89de15…`, are retained in the evand packets of 1
October and 28 September; its `zeromargin.py` at `659ee62`, `3cb95fb7…`, is not
retained, and nothing here ran it.

## Credit and AI Assistance, as the Source States Them

The README and the paper name Mohsen Khalili and Sara Gharabaghi, independent
researchers, as the authors. Their lineage section credits:

- the unavoidable-set method to Göbel, Stromquist and Friedman, and weighted points,
  segments and areas to Nagamochi;
- weights found by linear programming and checked in exact rational arithmetic to Sam
  Burns and Gustavo Massaccesi;
- closed mixed covers, the mixed format, the checkers `zmx2` and `zm_mixed.py`, the
  `line_cover` model and the $s(45) = 7$ cover used as the starting point to Evan
  Daniel;
- public mixed-cover certificates, including $s(59) = 8$, to Hiroaki Hosono.

What the source calls new: the certificate, and a separation step, `search/tilesep.py`,
for low-mass valleys of nearly axis-parallel squares on a wall beside a corner at tilts
of 0.01° to 3°.

AI assistance, `README.md`: “The search, the certificate, the new valley-separation tool
and the verification runs were produced with Claude (Anthropic) under our direction; we
reviewed the method, the checks and this write-up.”

The source mentions this project only to cite its case page for the standing bound and
T-066 for $s(59) = 8$, and its paper thanks “the Squares Project for its records”; it
names no debt to the project’s methods, so its lineage is `independent`.

## The Claim, as the Source States It

| Claim | Certificate | Total | Checks the source reports |
| --- | --- | --- | --- |
| $s(44) \ge 7$, so $s(44) = 7$ with the grid | 15,525 weighted points and 3,912 uniformly weighted pieces of the grid lines $x, y \in \{1, \ldots, 6\}$ of $[0,7]^2$ in Daniel’s mixed format v1, coordinates $X/1000$, weights $w/10^8$, D4-invariant | $2199755099/50000000 = 43.99510198 < 44$ | `zmx2 cert --d4`: VERIFIED-D4, every root, 0 uncertified, 191 s on one thread; `zmx2 cert --full`: VERIFIED, 39,200 roots, 134,880,184 boxes, 0 uncertified, 27.6 min; `zm_mixed.py cert --d4 --depth 24 --disj --chain-from 0` over 9,800 roots, 1,265 boxes uncertified in 27 roots, each re-swept whole at `--depth 30` with none, about 143 CPU-hours; `sanity.py` (exact) and `stress.py` (float, least mass 1.0031) |

The source says no Lean formalization and no independent review exist.

## Checks Made Here

On 31 October 2026, on a shared four-core x86-64 Linux container with four other lanes
running, Python 3.14.7 and rustc 1.97.0, two threads. Each checker run has its receipt in
[`receipts/`](receipts/), written by `devtools.replay_receipt`.

- **Custody.** `devtools.acquire_source --check` re-derives the packet from its manifest;
  the certificate’s SHA-256 is the issue’s.
- **Data facts.** `devtools.audit_evand_mixed_covers cover --case 44`: total
  $2199755099/50000000$ as stated, 15,525 points and 3,912 segments as stated, all of
  length $1/50$ on $x, y \in \{1, \ldots, 6\}$, none on a wall, D4-invariant entry by entry
  and as a measure, no point on a loaded line.
- **The `zmx2` build.** `devtools.replay_evand_zmx2 build --checker e2bb84e9` assembled
  `verify2/` from the retained `zmx2.rs` `e2bb84e9…` and crate files, digests checked,
  and built binary `d68a2e3540344a0e5ad8af33847e3c473b099cf922b150afd184cc715e038787`
  ([`receipts/n44_zmx2_build.log`](receipts/n44_zmx2_build.log)).
- **`zmx2 cert --d4`.** `devtools.replay_evand_zmx2 run --case 44 --mode d4`: VERIFIED-D4,
  4,900 roots, 16,792,446 boxes, 8,321,795 certified and 76,878 empty leaves, 0
  uncertified, none capped, maximum depth 39; 131 s wall, 222 CPU-s, 05:08:25Z to
  05:10:36Z ([`receipts/n44_zmx2_d4.log`](receipts/n44_zmx2_d4.log)). Every root’s census
  equals the source’s `verification/logs/zmx2_d4.log`, headers identical.
- **`zmx2 cert --full`.** The same with `--mode full`: VERIFIED, 39,200 roots (two
  passes, the cover and its reflection $y \mapsto 7 - y$), 134,880,184 boxes,
  66,848,724 certified and 610,968 empty leaves, 0 uncertified, none capped, maximum
  depth 39. The run started at 05:10:36Z and was stopped by a container restart at about
  05:27Z with 29,812 roots in its root log
  ([`receipts/n44_zmx2_full.log.gz`](receipts/n44_zmx2_full.log.gz), no footer); the same
  command resumed it from that log at 05:30:34Z and finished the other 9,388 at 05:35:45Z
  (311 s wall, 430 CPU-s,
  [`receipts/n44_zmx2_full_resume1.log`](receipts/n44_zmx2_full_resume1.log)). `zmx2`
  appended to the one root log under its one header, and its summary counts 2,601
  CPU-s over all roots. Every root’s census equals the source’s
  `verification/logs/zmx2_full.log`, headers identical, and the totals are the source’s.
- **Controls.** `devtools.replay_evand_zmx2 control --case 44`, each mutation removing
  one $D_4$ orbit so that `--d4` still applies, in
  [`receipts/controls/`](receipts/controls/), held by
  `tests/test_replay_controls.py`. Each region was found by sweeping the mutant over the
  roots around its removed orbit (the point mutant over $x$ 11–25, $y$ 17–31: 32,355
  uncertified boxes; the segment mutant over $x, y$ 0–19: 48,952) and keeping one refused
  root cell; the published cover certifies both cells.
  - `drop-heaviest-point`: the eight points at the images of $(1.812, 2.430)$, $0.00998176$
    each, $0.0798541$ in all; mutated cover `85678ee6…`; `zmx2 cert --d4` on the cell
    $x$ 23, $y$ 17: NOT VERIFIED, 435 uncertified boxes.
  - `drop-heaviest-segment`: the eight segments at the images of $(0.98, 1)$–$(1, 1)$,
    $0.09198265$ each, $0.7358612$ in all; mutated cover `eca3c3f3…`; the cell $x$ 8, $y$
    9: NOT VERIFIED, 235 uncertified boxes.

  The review’s own program finds each mutant capturing less than 1 exactly at a pose
  where the published cover captures more ([`review/`](review/README.md)).
- **The source’s `zm_mixed.py` records**, read by the review’s own program (not run):
  every one of the 9,800 roots once at depth 24, and each of the 27 roots left with
  uncertified boxes certified whole at depth 30, under the pinned digests; 495,545
  CPU-s recorded ([`review/outputs/zm-records-n44.json`](review/outputs/zm-records-n44.json)).

`devtools.audit_evand_mixed_covers check` re-derives the cover audit, both source logs’
audits, both replays’ audits and the root-for-root comparisons from the retained files.

## What Is Not Checked Here

- `zm_mixed.py` was not run: its complete pass is about 138 CPU-hours by the source’s
  records, over the pass’s 40 CPU-hour cap (`think-qvp6`). It is a second machine method
  by the producer and would raise no rung.
- The source’s `sanity.py`, `stress.py`, `tilesep.py`, `cover_loop.py` and
  `zm_mixed_check.py` were read and not run.
- No Lean statement exists for this cover; the reduction’s Lean proofs in Daniel’s
  library were not read or built.
- `zmx2` is trusted as the reviews of 28 September and 2 October derived it, with the
  host’s IEEE-754 arithmetic; its acceptances are exact integer tests on binary64
  enclosures widened outward.

## Review Programs

The stage 4 review’s programs and outputs are in [`review/`](review/README.md).

## Compressed Files

Data files of more than 1,000 lines are stored as deterministic gzip made by `gzip -9n`,
with no file name or timestamp in the header. The table gives the Git blob and SHA-256
of the decompressed bytes, and `python -m devtools.retained_data check PACKET`
re-derives every row.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `s44-equals-7/certificate/s44_cover_7.txt.gz` | upstream | `6dc71a7c3bdfd309bc6f963e6fcd494c2c0d9dfb` | `c9fde0f1e7013f3f61f4a8d673b6bcaf9c5e54c914b6462164d7326ba254cae0` |
| `s44-equals-7/verification/logs/zmx2_d4.log.gz` | upstream | `29d39778f676769e6a24525e8565414f59289df0` | `16d05e12bf0b7785633463a444734818ab4e36a5b4d5eccf2efe2abfb4640965` |
| `s44-equals-7/verification/logs/zmx2_full.log.gz` | upstream | `1fe693ad9c80eb78198a63bf4405d68f33cbb20a` | `c48f7f30f2232ff87f732aac28ac81c9e344719d177a23cd12866b6a63c21ae1` |
| `receipts/n44_zmx2_d4_roots.log.gz` | receipt | `7d7acd70cf53757d5fe193abf1aab56feddeb97f` | `cbcf1dbc693ad0537ff03741f640df71513838c15dae363d5c8452559534ab32` |
| `receipts/n44_zmx2_full_roots.log.gz` | receipt | `51cbb7c28e853eaf0b81befc1ce171b795990882` | `48cf17905103926f2a0b48fe75cfd640a73f0e67969febffe703ac9598c030af` |
| `receipts/n44_zmx2_full.log.gz` | receipt | `067db4168e2878189559bd4c55674797b3aafd1d` | `9d8d507fc04fb6ba5d894f32dd79721bad3469b721fc4ef8ec422c5e87dda078` |
| `review/outputs/zmx2/n44_zmx2_6b7f0f79_d4_roots.log.gz` | receipt | `4dfca2877a49c0e2e4e8151a0b11dba0e2b8de45` | `eb659564d71bdf198e30ed5672ec12e98ff6edc9f9902f945a479afd88772633` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
