# Release Members of Four #446 Fine-Net Certificates, 8 October

This packet retains the data of the four certificates of
[jlevy/squares#446](https://github.com/jlevy/squares/issues/446) that T-233 registers:
the candidates, receipts and logs of their release assets, beside the directories’
documents, so that a review can read each certificate and the census can replay it.
The [authored-facts packet of 8 October](../wand125-fine-net-lower-bounds-2026-10-08/README.md)
holds the issue’s seven claims at `61e37d5`, with its reported catalogue, the n = 27
follow-up facts and its source manifest, and is unchanged; this packet adds the bytes it
pinned and did not keep. Each bound remains unconfirmed here.

| n | Certificate | Claim | First in the source | Release asset (bytes, SHA-256) | Positive rows | Candidate SHA-256, digest |
| ---: | --- | --- | --- | --- | ---: | --- |
| 19 | [`mixed_n19_L48275`](https://github.com/wand125/square-packing/tree/bf85d6b537a7e854ac2f885c871474ea46db65ac/problems/square-lower-bounds/certificates/mixed_n19_L48275) | $s(19) \ge 1931/400$ | `7400660`, 2026-10-07T08:56:31Z | 597,835, `9d1aea51…8ccb` | 347 | `20dcda35…fe90`, `7a292c49…e070` |
| 20 | [`mixed_n20_L49125`](https://github.com/wand125/square-packing/tree/bf85d6b537a7e854ac2f885c871474ea46db65ac/problems/square-lower-bounds/certificates/mixed_n20_L49125) | $s(20) \ge 393/80$ | `61e37d5`, 2026-10-08T09:10:50Z | 614,741, `0ccc62a0…fb76` | 471 | `dc6321dd…7187`, `9cf12db0…8d11` |
| 26 | [`mixed_n26_L5555`](https://github.com/wand125/square-packing/tree/bf85d6b537a7e854ac2f885c871474ea46db65ac/problems/square-lower-bounds/certificates/mixed_n26_L5555) | $s(26) \ge 1111/200$ | `7400660`, 2026-10-07T08:56:31Z | 635,440, `ae4dc5e8…1074` | 615 | `a3a3d93b…a9a3`, `5cd188ae…511f` |
| 27 | [`mixed_n27_L5655`](https://github.com/wand125/square-packing/tree/bf85d6b537a7e854ac2f885c871474ea46db65ac/problems/square-lower-bounds/certificates/mixed_n27_L5655) | $s(27) \ge 1131/200$ | `bf85d6b`, 2026-10-08T16:53:25Z | 642,635, `4f1b449a…59cf` | 714 | `97198893…6ec8`, `3bd905d3…e566` |

All four declare core $4999/5000$ and the net `{"step": "1/5002", "last": 2072}` of
2,073 half-angle directions, the net of T-132, T-142, T-143 and T-232, and each has mass
$n - 1/100000$. The issue’s n = 27 value, $2261/400$ (`mixed_n27_L56525`), is
superseded by the follow-up in the same release and is not retained here; nor are its n
= 28, 29 and 31 certificates, which later certificates of the release supersede (T-142,
T-132, T-232).

The packet is pinned at `bf85d6b537a7e854ac2f885c871474ea46db65ac` (2026-10-08T16:53:25Z),
the follow-up’s commit, two commits after `61e37d5`. The n19, n20 and n26 directories
are the same Git trees (`415619d8`, `8e1d48bb`, `16d306b7`) at `61e37d5`, at the pin
and at the head when read, `e48de24`; the n27 directory is `f109c1de` at the pin and the
head; the licence is blob `bbfbff13` at all three. Retrieved 2026-10-23T07:00Z.

## What Is Retained

Two tools wrote the packet, and each has a check that re-derives it from the packet
alone.

- **The documents.** [`devtools.acquire_source`](../../../devtools/acquire_source.py)
  wrote them from its [declaration](acquisition/declaration.json): the
  [acquisition record](acquisition/sources.json) and the
  [subtree manifest](acquisition/upstream-subtree.sha256) give the size and SHA-256 of
  all 45 files in scope, and `--check` re-derives them.
  Retained byte for byte under
  [`square-packing/`](square-packing/problems/square-lower-bounds/certificates/): each
  directory’s `README.md`, `ASSET.json`, `bundle.json` and `files-sha256.json`.
  Pinned by digest only, with their reasons in the record: the licence, each
  `provenance/search-notes.md`, and each `check2/src/` document, all byte-identical to
  copies earlier packets retain or, for `SOUNDNESS.md` and `INDEPENDENCE.md`, this
  repository’s own files of 3 October.
- **The release assets’ data.** `devtools.fine_net_followup retain` refused each asset
  unless its size and SHA-256 were the pinned ones, unpacked it safely, and copied six of
  its eight members to [`release/`](release/certificates/) at their own paths in the
  asset: `candidate.json` (stored as deterministic gzip), `check2/receipt.json`,
  `check2/control.json`, the run log `check2/run.jsonl.gz` and the control log
  `check2/control-197_200.jsonl.gz` (both kept as published), and
  `verification/prepublication-receipt.json`. The
  [retention record](acquisition/release-assets.json) lists every member of every asset
  with its size and SHA-256, and `fine_net_followup check-retained` re-derives it.

Two members of each asset are pinned by digest and not copied: the nested verifier
archive `check2/src/sqverify-proof-net-fe12e036c.tar.gz` (69,540 bytes, `e495f9bf…71e81`
in all four), the source’s adaptation of this repository’s `sqverify_fast`, which carries
no notice of its own and was digested and not opened; and the sealed inner bundle
(313,813 to 336,026 bytes), whose payloads repeat the directory’s files and whose 16
members each premises receipt inventories.

Under
[`OR-18`](../../../../operating-rules.md#or-18-keep-bulk-data-out-of-git-and-never-bind-code-or-verdicts-to-a-git-commit-or-blob)
the retained set is small enough for Git: 0.9 MB of release members and 0.04 MB of
documents, the logs compressed already.

## What Was Checked

**Custody.** Each asset’s size and SHA-256 equal its `ASSET.json` at the pin, its line
of the release’s `SHA256SUMS` (lines 19, 435, 22 and 436) and the release API’s digest,
downloaded on 2026-10-23, and the stored size and SHA-256 the 8 October packet recorded.
Each candidate’s SHA-256 is the one that packet records. Each retained document has the
Git blob its commit names.

**Input premises.** `devtools.fine_net_followup premises` unpacked each asset beside the
pinned documents and ran the maintained readers on the candidate
([n = 19](receipts/premises-n19.json), [n = 20](receipts/premises-n20.json),
[n = 26](receipts/premises-n26.json), [n = 27](receipts/premises-n27.json)). All four end
`EXACT_PREMISES_HOLD`: lemma N0’s five premises and its last bin hold on the declared
net, with $B(1 + D) = 25009997/25010000 < 1$; the mass is $n - 1/100000$ over positive
rows only; one candidate digest appears throughout; and the full check2 reader holds
every premise. Each sealed bundle holds 16 files and matches its `files-sha256.json`,
and each directory’s README differs from its sealed edition.
No program of the source ran.

**Two reported complete runs each.** Each check2 receipt records the source’s adapted
crate (source digest `ab6e33e1…`) verifying every direction, and each pre-publication
receipt a second run of the same source on a fresh Ubuntu 24.04 machine, not the run the
check2 receipt embeds. Each control scales every mass by $197/200$ at 32 sampled
directions and reports all 32 refused, 31 with an exact capture below the threshold.
These are attributed author outcomes; a sampled control does not replace the whole-net
controls the records lane requires.

| n | check2 run: wall (s), threads | Direction CPU (s) | Nodes | Pre-publication run (s) |
| ---: | --- | ---: | ---: | ---: |
| 19 | 671.1, 6 | 3,584 | 377,472,588 | 1,259 |
| 20 | 699.6, 12 | 8,353 | 410,012,470 | 2,823 |
| 26 | 709.1, 12 | 8,158 | 663,387,112 | 2,794 |
| 27 | 1,061.8, 12 | 12,676 | 648,972,154 | 4,380 |

## The Stage 4 Review

The [mathematical review of 23 October](../../../../docs/project/reviews/review-2026-10-23-wand125-446-fine-net.md)
accepts all four certificates, with no blocking or major finding. Its programs, README
and receipts are in [`review/review-2026-10-23/`](review/review-2026-10-23/README.md):
every exact premise recomputed apart from the crate, each axis direction decided
completely, the source’s logs read exactly and 32 sampled directions per count evaluated
exactly. It decides no other direction; coverage there rests on the source’s runs until
the census.

**Control-log filename (F-6).** Each directory’s `README.md` lists
`check2/control.jsonl.gz`; the asset holds `check2/control-197_200.jsonl.gz`, which
`release/` retains. This affects discovery only, and the archived README and its digest
are unchanged; the correction was asked of the author for the 16 October bundles on 19
October, and the same note goes to the author for these four.

## The Price of a Complete Replay

The census route of the 6 October soundness review is a capture at every direction and
the whole-net controls. The review prices the four at 10.5 to 19.2 CPU-hours: 1.4 to
2.7 at n = 19, 2.3 to 4.6 at n = 20, 3.1 to 4.8 at n = 26 and 3.7 to 7.0 at n = 27.
Each capture is priced by the ratio of 0.689 to the source that the n31 sample measured
on this host on 23 October
([`wand125-fine-net-n31-2026-10-11`](../wand125-fine-net-n31-2026-10-11/README.md)) and
by node count at that sample’s 18.6 microseconds per node, since the source’s n = 19 run
used 6 threads and the others 12; the controls at 10 to 40 percent of the capture, as at
n = 84, 85 and 68. The census reads each candidate from `release/`; the replays are
owned by think-ndvg.

## Sources and Notices

The nearest enclosing source notice, `problems/square-lower-bounds/LICENSE`, is MIT,
Copyright 2026 wand125, byte-identical to the notice the FN-1 packet retains.
Each `ASSET.json` places its tarball’s data files in the directory it covers.
The nested verifier archive carries no notice of its own and is not retained.

The source credits wand125 (Hiroaki Hosono), with code and formats credited to Evan
Daniel, tokoharu and jlevy/squares; the commits are authored by Hiroaki Hosono.
The repository’s README says parts of the work were produced with AI assistance under
human direction.

## Compressed Files

| Stored file | Origin | Git blob (decompressed) | SHA-256 (decompressed) |
| --- | --- | --- | --- |
| `release/certificates/mixed_n19_L48275/candidate.json.gz` | upstream | `4bd83b58be52ab40695d0a5fc1737d6920d05559` | `20dcda3541e139f79a9aec6e3bd469bb5dc8ccbb2c837aa18d49a0e708e5fe90` |
| `release/certificates/mixed_n20_L49125/candidate.json.gz` | upstream | `02481fad6550115b2faae73d8f340ee4ace18f48` | `dc6321dd0478625ef0a164749754657331c73ecfdf7212523edb3d0f2dfd7187` |
| `release/certificates/mixed_n26_L5555/candidate.json.gz` | upstream | `fb784458acca421cb66cfa7419586369b32503aa` | `a3a3d93b81e201a4fdc8c454a929ad3d20eb10875eab46611302a796256ea9a3` |
| `release/certificates/mixed_n27_L5655/candidate.json.gz` | upstream | `4e5797c604d46e3b62dddc3285485b36c3ab1677` | `971988936fe73cf62ffbd8645f9aad5006b7bb297d3a5bfa5d9226d75bec6ec8` |

## Original Gzip Files

| Stored file | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `release/certificates/mixed_n19_L48275/check2/control-197_200.jsonl.gz` | upstream | `d27475a2d027dcb850feec939fa2a48be82ab15d` | `8671cc5101ce11bd71bb4b2a2b3a4f99e5f3b715b6c8d7448dba845c1232b118` |
| `release/certificates/mixed_n19_L48275/check2/run.jsonl.gz` | upstream | `8319bd660b84871acc7b73fd7a3b67d1a65c3501` | `d497fe7b8d667ff318afb9c871cdcc0c3942fa218bc09754944201914c597b7d` |
| `release/certificates/mixed_n20_L49125/check2/control-197_200.jsonl.gz` | upstream | `93ad0777bc5b1d7619a2ab3ab8c74b903fc8f2d9` | `52331a5cf510cda5ba6f0730322593d8e0084cfd1b239a66f28b0ac27a0a83e4` |
| `release/certificates/mixed_n20_L49125/check2/run.jsonl.gz` | upstream | `ceaf742fadf0843793520b76b9f611c7c1fc37ef` | `0fcf0bec91ef550fe489b179ab621e0cb135f24c55be80729aa182973cf03fe1` |
| `release/certificates/mixed_n26_L5555/check2/control-197_200.jsonl.gz` | upstream | `b08833e64bfb4d225ea5b354b30a403c6ef286f8` | `1c743f78bdfcce3fbd734b8acced662dcd82312bb2f83e7a57d2099e2993834f` |
| `release/certificates/mixed_n26_L5555/check2/run.jsonl.gz` | upstream | `5c9281587a138c431ffd9556069a8ab3febc8cfe` | `43f9be3f55ed5eabfb225e0ea7eaeb9d62aef44ddc9b5ebee483b477301bfb1d` |
| `release/certificates/mixed_n27_L5655/check2/control-197_200.jsonl.gz` | upstream | `8623b2818801e3ca7a5e4998625e3ddcb50da77b` | `5b555d496c761b7eda2da72cab40001b993b5d59830390b3f8c53a37da630d56` |
| `release/certificates/mixed_n27_L5655/check2/run.jsonl.gz` | upstream | `70c90bd9bf7adf937d657587e74685e80dbd07ce` | `2fbeb42ceda20e813df3534ea7535bef034d60ffa630148b6e213c6b5f09a429` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
