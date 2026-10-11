# Reported Fine-Net Lower Bounds for n = 28 and n = 30, 10 October

Two commits of 10 October to wand125/square-packing add check2 measure certificates on
the 2,073-direction net of the n = 29 follow-up: `mixed_n28_L57425`, reporting
$s(28) \ge 2297/400 = 5.7425$, and `mixed_n30_L58925`, reporting
$s(30) \ge 2357/400 = 5.8925$. No issue reports either; the evening watch read of 10
October found them. Both bounds remain unconfirmed here; no standing bound or rating
changes.

| Item | n = 28 | n = 30 |
| --- | --- | --- |
| Source | [`mixed_n28_L57425`](https://github.com/wand125/square-packing/tree/36b85b9f37efa7cc5d4464805cfb0f2d21576267/problems/square-lower-bounds/certificates/mixed_n28_L57425) | [`mixed_n30_L58925`](https://github.com/wand125/square-packing/tree/ff9f2692afe7d1e65a51bb079b61b3710b97fc82/problems/square-lower-bounds/certificates/mixed_n30_L58925) |
| Pinned revision | `36b85b9f37efa7cc5d4464805cfb0f2d21576267`, committed 2026-10-10T11:47:30Z | `ff9f2692afe7d1e65a51bb079b61b3710b97fc82`, committed 2026-10-10T14:12:31Z |
| Release asset | `certificates__mixed_n28_L57425.tar.gz`, 627,191 bytes, SHA-256 `7d0f9107…3bf3` | `certificates__mixed_n30_L58925.tar.gz`, 638,622 bytes, SHA-256 `0d11fe05…61ba` |
| Candidate | 631 positive rectangles, mass $2799999/100000$ | 463 positive rectangles, mass $2999999/100000$ |
| Standing bound | T-107’s $1147/200$, both lanes; $+3/400$ | T-109’s $11767/2000$, both lanes; $+9/1000$ |
| Other report | #446’s unadopted $287/50$ (`mixed_n28_L574`); $+1/400$ | none |

Both declare core $4999/5000$ and the net `{"step": "1/5002", "last": 2072}`, and both
use release `square-lower-bounds-v1`. The repository’s head when read, `27ed168`, is
five commits past `ff9f269`; they change README tables only, and neither certificate
directory nor the licence.
Retrieved 2026-10-10T17:00:59Z.

The follow-up facts for [n = 28](reported-n28-followup.json) and
[n = 30](reported-n30-followup.json) record every exact value and identity above, and
the [source manifest](source-manifest.json) the size, Git blob and SHA-256 of every
pinned document and every archive member.
The two share a packet because their revisions share a date and a net; the n = 29 packet
stays as it was.

## What Was Checked

**Custody.** Each asset’s size and SHA-256 equal the release API’s digest, the release’s
`SHA256SUMS` (lines 439 and 440) and the source’s `ASSET.json`. Each of the 11 pinned
documents of each directory has the Git blob its commit names.
Each sealed inner bundle holds 16 files and matches all 15 entries of its own
`files-sha256.json`; six of its payloads repeat the outer asset’s byte for byte.
The adapted verifier’s source archive is `e495f9bf…71e81` in both, the archive the n =
29 and #446 packets inventory.
Both README editions differ from the sealed ones by the pre-publication paragraph.

**Input premises.** `devtools.fine_net_followup premises` unpacked each asset beside its
pinned documents and ran the maintained readers on the candidate
([n = 28](receipts/premises-n28.json), [n = 30](receipts/premises-n30.json)). For both,
Lemma N0’s five premises hold on the declared net, with $B(1 + D) = 25009997/25010000$,
the mass is $n - 1/100000$ over positive rows only, and one candidate digest appears
throughout. The three narrow readers took under 0.01 seconds each.

- **n = 28.** The full check2 reader (`audit_check2`) holds every premise: exact
  premises hold.
- **n = 30.** The full check2 reader holds every premise too: exact premises hold.
  The pre-publication receipt has a newer shape, `fine-net-check2-receipt/v1`, with
  `verifier` where the earlier shape has `build` and a control given as tries.
  The first run of `premises` stopped there with `KeyError: 'build'`, a reader gap and
  not a defect found in the certificate.
  Commit `d34d0084a` closed it: the reader takes the build from `verifier` and requires
  the control’s one try to have refused at 197/200, the factor of the check2 control.
  A second run on the same asset and documents gave the receipt kept here, which differs
  from the first only in the check2 audit, the status and the two walls; every custody
  fact is unchanged.

**One reported run each.** The n = 30 pre-publication receipt is the very record the
check2 receipt embeds: the same start, 12:01:39Z, 1,790.3 seconds, 12 threads and binary
`ec04d332…`. The n = 28 one, in the older shape, states 772 seconds against the check2
run’s 771.6 and the same control outcome.
So each certificate carries one reported complete run, where n = 29 carried two (1,058
and 4,306 seconds).

**A diagnostic sample of the native capture.** This repository’s `sqverify-fast`, built
from the reviewed crate source `d97758bb…`, ran eight directions of each net, one thread
each and two at a time ([n = 28](receipts/sample-diagnostic-n28.json),
[n = 30](receipts/sample-diagnostic-n30.json)): 0, 296, 592, 888, 1184, 1480, 1776 and
2072\. All sixteen verified, and each matched the source’s log in node count and least
certified bound. A sample decides only the directions it ran, and is not a replay.

|  | n = 28 | n = 30 |
| --- | --- | --- |
| Sample CPU, here and at the source (s) | 21.19 and 33.05 | 29.65 and 52.60 |
| Ratio | 0.641 | 0.564 |
| Source CPU over the whole net (s) | 9,204 | 14,335 |
| Priced full capture (CPU s) | 5,903 | 8,080 |
| Priced whole-net controls (CPU s) | 5,911 | 8,092 |
| Total | 3.28 CPU-hours | 4.49 CPU-hours |
| Wall at two workers, idle host | about 1.6 hours | about 2.2 hours |

The host’s load average was 4.3 and 4.1 on four cores during the samples, so CPU is the
price. The controls are those of the 6 October review: the 99/100 mutant at every
direction, and the original and the near-threshold mutant at the least-bound direction.
Both certificates together come to about 7.8 CPU-hours, above the 20 CPU-minute limit
for a run inside an intake, so neither full net was run.

## Review and Remaining Work

The source reports all 2,073 directions verified by its adaptation of this repository’s
crate (build `ab6e33e1…`, 12 threads): in 771.6 seconds of wall for n = 28 and 1,790.1
for n = 30. Its control scales every mass by 197/200 at 32 sampled directions and
reports all 32 refused, 31 with an exact capture below the threshold, for each.
These are attributed author outcomes; a sampled control does not replace the whole-net
controls the records lane requires.

A maintained replay must retain the complete direction outcomes of a census run, from a
candidate retained where the census reads it, with the whole-net controls and restored
positives, and must be followed by an independent review that reads each certificate.
That work, with a budget for it, belongs to the import’s bead, think-i85v; the
[run plan of 11 October](../../../../docs/project/specs/active/plan-2026-10-11-wand125-confirmations.md)
gives its commands.

## Retained for the Replay

On 11 October the two candidates alone were retained, so that the census can read them:
[`mixed_n28_L57425/candidate.json.gz`](square-packing-bounds/certificates/mixed_n28_L57425/candidate.json.gz)
and
[`mixed_n30_L58925/candidate.json.gz`](square-packing-bounds/certificates/mixed_n30_L58925/candidate.json.gz)
under `square-packing-bounds/certificates/`, each asset’s `candidate.json` (178,089 and
130,050 bytes, SHA-256 `5ef20511…0107` and `981a17db…677e`, the digests the source
manifest pins for those members) stored as deterministic gzip.
`devtools.retain_wand125_release` wrote them from the pinned assets, refusing an asset
unless its size and SHA-256 were the manifest’s and a member unless its digest was.
`square-packing-bounds/` is the directory the census reads under every wand125 mixed
packet; here it stands for `problems/square-lower-bounds/` of wand125/square-packing.

The census runs `sqverify-fast` on a candidate retained in its packet
(`MIXED_PACKETS` in `devtools/sqverify_fast_census.py`), and item (b)4 of the
[declared-net soundness review](../../../../docs/project/reviews/review-2026-10-06-sqverify-fast-declared-net-soundness.md#for-the-records-lane)
holds a census row to the retained `.gz` file’s digest, with
`devtools.retained_data check` passing on its packet.
The [6 October check2 packet](../wand125-mixed-bounds-check2-2026-10-06/README.md)
retained its ten candidates the same way, and this one follows it.
The candidates sit under the MIT notice below.
The redistribution question this packet records is the nested verifier archive’s, and
that archive stays unretained, with the run and control logs, the sealed bundles and the
pre-publication receipts.

## Sources and Notices

The nearest enclosing source notice, `problems/square-lower-bounds/LICENSE`, is MIT,
Copyright 2026 wand125, the same blob at both pins and at the head, and byte-identical
to the notice the #446 packet records and to the copy the
[27 September rectangle packet](../wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE)
retains (Git blob `bbfbff13…`).
The nested verifier archive carries no notice of its own, so its redistribution is
unresolved. This packet publishes authored facts, hash references, this repository’s own
receipts and, since 11 October, the two candidates alone, under that MIT notice.
The assets stay with their author, pinned here by size and digest, and no copy of either
is hosted here. No program of the source was run.

The source credits wand125; both commits are authored by Hiroaki Hosono.
Its README says parts of the work were produced with AI assistance under human
direction, and each commit names Claude Opus 5.5 as co-author.

## Compressed Files

The retained candidates have more than 1,000 lines each, so they are stored as
deterministic gzip made by `gzip -9n`, with no file name or timestamp in the header.
The table gives the Git blob and SHA-256 of the decompressed bytes, which are the asset
members’ as the [source manifest](source-manifest.json) pins them.
The repository’s readers decompress through
`devtools.retained_data.read_retained_bytes`, and
`python -m devtools.retained_data check PACKET` re-derives every row.

| Stored file | Origin | Git blob | SHA-256, decompressed |
| --- | --- | --- | --- |
| `square-packing-bounds/certificates/mixed_n28_L57425/candidate.json.gz` | upstream | `83973a7165fd67ef82fbf73083fbc27c7e5c690b` | `5ef20511e18a9997dfcc4cef773b65eac83dfe59e6a56fa810f3c789076c0107` |
| `square-packing-bounds/certificates/mixed_n30_L58925/candidate.json.gz` | upstream | `6fc73a25e66e7c2e2390c43f767a9fd14c3ef09e` | `981a17db67b24f99d64e176c892655c27fde67f8e99f2875a8f1d55ff3d0677e` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
