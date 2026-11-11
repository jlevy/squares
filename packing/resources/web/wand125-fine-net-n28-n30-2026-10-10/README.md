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
positives, and an independent review must read each certificate.
That work, with a budget for it, belongs to the import’s bead, think-i85v.

The
[mathematical review of 11 November 2026](../../../../docs/project/reviews/review-2026-11-11-wand125-fine-net-n28-n30.md)
(think-4ul6) accepts both certificates, with no blocking or major finding. Its programs,
README and outputs are in [`review/review-2026-11-11/`](review/review-2026-11-11/README.md):
every exact premise recomputed, direction 0 of each net decided completely, the source’s
logs and controls held to an exact evaluator at every least-bound centre and control
witness, and a seeded search at 33 directions of each net. It also judges T-142’s axis
gap of $2.15 \times 10^{-9}$ under #892’s enclosure rule: the gap is the source sweep’s
own enclosure at that vertex, and the refusal has an exact witness. The census and its
whole-net controls remain.

## Sources and Notices

The nearest enclosing source notice, `problems/square-lower-bounds/LICENSE`, is MIT,
Copyright 2026 wand125, the same blob at both pins and at the head, and byte-identical
to the notice the #446 packet records.
The nested verifier archive carries no notice of its own, so its redistribution is
unresolved. Until 4 November this packet published only authored facts, hash references
and this repository’s own receipts.

On 4 November 2026 (think-i85v, for the review think-4ul6 and the censuses after it) each
asset’s six data members were retained under [`release/`](release/certificates/), at
their paths in the asset, so that the review and the census can read the candidates, by
the owner’s answer of 17 October to retain fine-net candidates where the census reads
them, as the n29, n31, #446 release and 13 October packets do.
`devtools.fine_net_followup retain` held each asset to its pinned size and SHA-256
(627,191 bytes, `7d0f9107…3bf3`; 638,622 bytes, `0d11fe05…61ba`) and copied the
candidate (as deterministic gzip of its 178,089 or 130,050 bytes, SHA-256 `5ef20511…`
and `981a17db…`, the source manifest pins), the check2 receipt, run log, control and
control log, and the pre-publication receipt, each equal to the manifest’s digest.
The nested verifier archive and the sealed inner bundle are pinned by digest only, with
their reasons, in the [retention record](acquisition/release-assets.json), which
`devtools.fine_net_followup check-retained` re-derives from the packet.
No program of the source was run.

The source credits wand125; both commits are authored by Hiroaki Hosono.
Its README says parts of the work were produced with AI assistance under human
direction, and each commit names Claude Opus 5.5 as co-author.

## Compressed Files

| Stored file | Origin | Git blob (decompressed) | SHA-256 (decompressed) |
| --- | --- | --- | --- |
| `release/certificates/mixed_n28_L57425/candidate.json.gz` | upstream | `83973a7165fd67ef82fbf73083fbc27c7e5c690b` | `5ef20511e18a9997dfcc4cef773b65eac83dfe59e6a56fa810f3c789076c0107` |
| `release/certificates/mixed_n30_L58925/candidate.json.gz` | upstream | `6fc73a25e66e7c2e2390c43f767a9fd14c3ef09e` | `981a17db67b24f99d64e176c892655c27fde67f8e99f2875a8f1d55ff3d0677e` |
| `review/review-2026-11-11/outputs/receipts-check.json.gz` | receipt | `86dfc2079d43cf9d100239e73e4f703a961717a8` | `ba49bfbf61129b246a2e8101ab4548085e39aeaaf7f3c0d6f694913c366808db` |
| `review/review-2026-11-11/outputs/direction-sample.json.gz` | receipt | `e4f99940726339b6724ede25d0a2630c436e6761` | `382e4e50a2911d329368d5093f1dc1d821194351b3d7d6e3756143f5a3f0f23f` |

## Original Gzip Files

| Stored file | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `release/certificates/mixed_n28_L57425/check2/control-197_200.jsonl.gz` | upstream | `29be8f524db5174654597ead6ac8d09e8cbf1ffe` | `8fa5261290892b6c7d8e41905bee493320a6954186b2a8ee94342c623de51169` |
| `release/certificates/mixed_n28_L57425/check2/run.jsonl.gz` | upstream | `369a6500730b85aa2810a3fd492945a82f1548e3` | `896c535bb0f26e312ac4349d561a9a006a54c69c9657fbc02e4d068fe7e8bddd` |
| `release/certificates/mixed_n30_L58925/check2/control-197_200.jsonl.gz` | upstream | `c9cc9a7bffba4da5bda5e27c3af079ec6033f918` | `ae1d9957fe143595401cd1c192d56e4851f6a1a3b2a5a4a0673907e19a4d080e` |
| `release/certificates/mixed_n30_L58925/check2/run.jsonl.gz` | upstream | `b3b4e0e43e9fddb869942156ed9306bdc8b4c456` | `a0252ad908786885700a366450fe7ff8654009a3331b93f8065ae74d8e2fea2f` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
