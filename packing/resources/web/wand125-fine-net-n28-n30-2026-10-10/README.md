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
- **n = 30.** The full check2 reader refuses at its last but one step, with
  `KeyError: 'build'`. The pre-publication receipt has a new shape,
  `fine-net-check2-receipt/v1`, with `verifier` where the reader reads `build` and a
  control given as tries.
  Every earlier step of the reader passed, since it reached this one, and the
  inventories in the receipt show the step after it would pass too: every file
  `files-sha256.json` lists, its README apart, has the directory’s digest.
  This is a reader gap, not a defect found in the certificate; the reader needs to read
  the new shape before the exact premises can be said to hold.

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
That work, with a budget for it, belongs to the import’s bead, think-i85v.

## Sources and Notices

The nearest enclosing source notice, `problems/square-lower-bounds/LICENSE`, is MIT,
Copyright 2026 wand125, the same blob at both pins and at the head, and byte-identical
to the notice the #446 packet records.
The nested verifier archive carries no notice of its own, so its redistribution is
unresolved. This packet publishes authored facts, hash references and this repository’s
own receipts. No upstream byte is retained in Git: the assets stay with their author,
pinned here by size and digest, and no copy is hosted here.
No program of the source was run.

The source credits wand125; both commits are authored by Hiroaki Hosono.
Its README says parts of the work were produced with AI assistance under human
direction, and each commit names Claude Opus 5.5 as co-author.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
