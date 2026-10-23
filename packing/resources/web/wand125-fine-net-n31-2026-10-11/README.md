# Reported Fine-Net Lower Bound for n = 31, 11 October

One commit of 11 October to wand125/square-packing,
[`23e3186`](https://github.com/wand125/square-packing/tree/23e31862345c532d17ad2c896677a3a8d8821aa4/problems/square-lower-bounds/certificates/mixed_n31_L59775)
(2026-10-11T00:51:18Z), adds the check2 measure certificate `mixed_n31_L59775`,
reporting $s(31) \ge 2391/400 = 5.9775$ on the 2,073-direction net of T-132, T-142 and
T-143 (core $4999/5000$, half-angle step $1/5002$). No issue reports it; the watched
repository read of the 11 October intake pass found it (think-q655), and its import is
think-wop1. The bound is unconfirmed here; no standing bound or rating changes in the
change that adds this packet.

| Item | n = 31 |
| --- | --- |
| Source | [`mixed_n31_L59775`](https://github.com/wand125/square-packing/tree/23e31862345c532d17ad2c896677a3a8d8821aa4/problems/square-lower-bounds/certificates/mixed_n31_L59775) |
| Pinned revision | `23e31862345c532d17ad2c896677a3a8d8821aa4`, committed 2026-10-11T00:51:18Z |
| Release asset | `certificates__mixed_n31_L59775.tar.gz` in `square-lower-bounds-v1` (asset 629390758), 631,670 bytes, SHA-256 `50b1cf3f…0a58` |
| Candidate | 536 positive rectangles in D4 orbits, no point mass, mass $3099999/100000$; SHA-256 `4a7df269…be3b`, candidate digest `2d8d9d59…c6e2` |
| Standing bound | $2381/400 = 5.9525$ in both lower lanes (T-068 reported, T-074 verified); gain $1/40$ |
| Other report | jlevy/squares#446’s unadopted $597/100$ (`mixed_n31_L597`, the same release); gain $3/400$ |
| Upper bound | $6$, the trivial grid; gap $9/400$ |

The directory is the same Git tree, `61226b50`, from the pin through the repository’s
head when read, `e48de24` (2026-10-22T14:15:36Z), whose 130 later commits add other
certificates, problems and site pages and change neither this directory nor its
licence. Retrieved 2026-10-23T06:24Z.

## What Is Retained

Two tools wrote the packet, and each has a check that re-derives it from the packet
alone.

- **The documents.** [`devtools.acquire_source`](../../../devtools/acquire_source.py)
  wrote them from its [declaration](acquisition/declaration.json): the
  [acquisition record](acquisition/sources.json) and the
  [subtree manifest](acquisition/upstream-subtree.sha256) give the size and SHA-256 of
  all 12 files in scope, and `--check` re-derives them.
  Retained byte for byte under
  [`square-packing/`](square-packing/problems/square-lower-bounds/certificates/mixed_n31_L59775/):
  the directory’s `README.md`, `ASSET.json`, `bundle.json` and `files-sha256.json`.
  Pinned by digest only, with their reasons in the record: the licence, the
  `provenance/search-notes.md`, and each `check2/src/` document, all byte-identical to
  copies earlier packets retain or, for `SOUNDNESS.md` and `INDEPENDENCE.md`, this
  repository’s own files of 3 October.
- **The release asset’s data.** The directory’s data is a tarball in release
  `square-lower-bounds-v1`, which its `ASSET.json` names and says unpacks in place
  beside the documents.
  `devtools.fine_net_followup retain` refused the asset unless its size and SHA-256 were
  the pinned ones, unpacked it safely, and copied six of its eight members to
  [`release/`](release/certificates/mixed_n31_L59775/) at their own paths in the asset:
  `candidate.json` (stored as deterministic gzip, by the archive’s rule for data of more
  than 1,000 lines), `check2/receipt.json`, `check2/control.json`, the run log
  `check2/run.jsonl.gz` and the control log `check2/control-197_200.jsonl.gz` (both kept
  as published), and `verification/prepublication-receipt.json`. The
  [retention record](acquisition/release-assets.json) lists every member with its size
  and SHA-256, and `fine_net_followup check-retained` re-derives it.

Two members of the asset are pinned by digest and not copied:

- `check2/src/sqverify-proof-net-fe12e036c.tar.gz`, 69,540 bytes, SHA-256
  `e495f9bf…71e81`: the source’s adaptation of this repository’s `sqverify_fast`, the
  archive the 6, 13 and 16 October packets pin by the same digest.
  It carries no notice of its own, and it is kept out of this tree beside the crate
  whose declared-net change was written apart from it
  ([`sqverify_fast/INDEPENDENCE.md`](../../../sqverify_fast/INDEPENDENCE.md)). It was
  digested and not opened.
- the sealed inner bundle `n31-L5.9775-check2-bundle.tar.gz` (331,092 bytes, SHA-256
  `b88c5003…7b76`), whose payloads repeat this directory’s files; the premises receipt
  inventories its 16 members.

Under
[`OR-18`](../../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)
the retained set is small enough for Git: about 0.25 MB in a checkout, since the logs
are compressed already. The largest file is the run log, 0.17 MB.

## What Was Checked

**Custody.** The asset’s size and SHA-256 equal its `ASSET.json` at the pin, its line of
the release’s `SHA256SUMS` (line 441) and the release API’s digest, downloaded on
2026-10-23. Each retained document has the Git blob its commit names, and each pinned
one the digest of the copy its reason names.

**Input premises.** `devtools.fine_net_followup premises` unpacked the asset beside the
pinned documents and ran the maintained readers on the candidate
([receipt](receipts/premises-n31.json)). It ends `EXACT_PREMISES_HOLD`: lemma N0’s five
premises and its last bin hold on the declared net, with
$B(1 + D) = 25009997/25010000 < 1$ and the last tangent $1036/2501$ past
$\tan(\pi/8)$; the mass is $31 - 1/100000$ over positive rows only; one candidate digest
appears throughout; and the full check2 reader holds every premise.
The sealed bundle holds 16 files and matches its `files-sha256.json`, and the
directory’s README differs from its sealed edition by the pre-publication paragraph.
No program of the source ran.

**Two reported complete runs.** The check2 receipt records the source’s adapted crate
(source digest `ab6e33e1…`, binary `ec04d332…`) verifying all 2,073 directions in
2,161.9 seconds of wall at 12 threads, 21,625 direction CPU-seconds and 787,004,724
nodes. The pre-publication receipt records a second run of the same source on a fresh
Ubuntu 24.04 machine, 7,277 seconds, not the run the check2 receipt embeds.
The control scales every mass by $197/200$ at 32 sampled directions and reports all 32
refused, 31 with an exact capture below the threshold.
These are attributed author outcomes; a sampled control does not replace the whole-net
controls the records lane requires.

**A diagnostic sample of the native capture.** This repository’s `sqverify-fast`, built
from the reviewed crate source `d97758bb…` (binary `567a0fd5…`, the census’s), ran eight
directions of the net, one thread each and two at a time
([receipt](receipts/sample-diagnostic-n31.json)): 0, 296, 592, 888, 1184, 1480, 1776 and
2072\. All eight verified, and each matched the source’s log in node count and least
certified bound. A sample decides only the directions it ran, and is not a replay.

## The Price of a Complete Replay

The census route of the 6 October soundness review: `sqverify-fast` at every direction
of the declared net, then the whole-net controls (the $99/100$ mutant at every
direction, and the original and the near-threshold mutant at the least-bound direction).

| Item | n = 31 |
| --- | --- |
| Sample CPU, here and at the source (s) | 53.24 and 77.24 |
| Ratio | 0.689 |
| Source CPU over the whole net (s) | 21,625 |
| Priced full capture (CPU s) | 14,907 |
| Priced whole-net controls (CPU s) | 14,926 |
| Total | 8.29 CPU-hours; 12.0 at the source’s own CPU |
| Wall at two threads | about 2.1 hours each |

The host’s load average was 1.5 to 1.9 on four cores during the sample.
The tracker’s earlier estimate of about 2 CPU-hours read the pre-publication run’s 7,277
seconds of wall as CPU; the check2 receipt’s direction CPU is the price.
The census reads the candidate from `release/`, and its receipts are to be kept under
`benchmarks/measure-verifier/census-mixed/wand125-fine-net-n31-2026-10-11/`.

## Sources and Notices

The nearest enclosing source notice, `problems/square-lower-bounds/LICENSE`, is MIT,
Copyright 2026 wand125, byte-identical to the notice the FN-1 packet retains.
The `ASSET.json` places its tarball’s data files in the directory it covers.
The nested verifier archive carries no notice of its own and is not retained.

The source credits wand125 (Hiroaki Hosono), with code and formats credited to Evan
Daniel, tokoharu and jlevy/squares; the commit is authored by Hiroaki Hosono.
The repository’s README says parts of the work were produced with AI assistance under
human direction, and the commit names Claude Opus 5.5 as co-author.

## Compressed Files

| Stored file | Origin | Git blob (decompressed) | SHA-256 (decompressed) |
| --- | --- | --- | --- |
| `release/certificates/mixed_n31_L59775/candidate.json.gz` | upstream | `e1a41faa35d58b8d237566d187ef493d0cca2dd7` | `4a7df269037a6449ba2d4bee2b6a76962df097c1515025545d4ca4cfcc39be3b` |

## Original Gzip Files

| Stored file | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `release/certificates/mixed_n31_L59775/check2/control-197_200.jsonl.gz` | upstream | `15fc92d97e05484b925f2d73e6d94c82e4eb76c6` | `0c77648891712846dd6e04992b8bca54a46ad21d8262bab5710c00a0dce3a6ab` |
| `release/certificates/mixed_n31_L59775/check2/run.jsonl.gz` | upstream | `39461644b23663f191b5f65f342d8b02087fb040` | `c23fd1ba7a7ab45c563ad8efd3ef72203e064d0a2c6a947b26fa487bf294b2d3` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
