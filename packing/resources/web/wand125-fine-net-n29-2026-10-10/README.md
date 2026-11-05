# Reported Fine-Net Lower Bound for n = 29, 10 October

Wand125’s
[comment of 10 October on issue #446](https://github.com/jlevy/squares/issues/446#issuecomment-6092965941),
at 02:47 UTC, reports $s(29) \ge 291/50 = 5.82$ by the measure certificate
`mixed_n29_L582` on a declared net of 2,073 directions.
It supersedes the issue’s earlier n = 29 report, $1163/200 = 5.815$, which the
[seven-case packet](../wand125-fine-net-lower-bounds-2026-10-08/README.md) keeps, by
$1/200$. The certificate’s own README compares it instead with `mixed_n29_L58175`
($2327/400$, at `dd6a7cc`), which no issue reported, and which it exceeds by $1/400$.
Since 4 November 2026 a complete replay here, its whole-net controls and a stage 4
review confirm it (T-132, V3/C3; [Review and Replay](#review-and-replay)), and both
lower lanes at n = 29 hold it.

| Item | Value |
| --- | --- |
| Source | [wand125/square-packing](https://github.com/wand125/square-packing/tree/22a23c8a99aa4e9616d596bc2f28555bacbee3dd/problems/square-lower-bounds/certificates/mixed_n29_L582) |
| Pinned revision | `22a23c8a99aa4e9616d596bc2f28555bacbee3dd`, committed 2026-10-10T02:47:21Z, the repository’s head when read |
| Release asset | `certificates__mixed_n29_L582.tar.gz` in `square-lower-bounds-v1`, 651,878 bytes, SHA-256 `6203a9b4…3274` |
| Retrieved | 2026-10-10T10:27:25Z |
| Candidate | 650 positive rectangles, mass $2899999/100000$, core $4999/5000$ |
| Declared net | `{"step": "1/5002", "last": 2072}`, 2,073 directions |

The [follow-up facts](reported-n29-followup.json) record every exact value and identity
above, and the [source manifest](source-manifest.json) the size, Git blob and SHA-256 of
every pinned document and every archive member.

This is a packet of its own rather than a third file in the seven-case packet: the
revision is dated 10 October, and a later revision is a new packet whose name and
bibliography key carry its own date.
The 8 October n = 27 follow-up shared that packet’s revision date, so joining it kept
both true.

## What Was Checked

**Custody.** The asset’s size and SHA-256 equal the release API’s digest, the release’s
`SHA256SUMS` and the source’s `ASSET.json`. Each of the 11 pinned documents of the
certificate directory has the Git blob the commit names.
The sealed inner bundle holds 16 files and matches all 15 entries of its own
`files-sha256.json`; six of its payloads repeat the outer asset’s byte for byte.
The adapted verifier’s source archive, `e495f9bf…71e81`, is the one the seven-case
packet inventories. Both README editions are recorded; the published one adds the
pre-publication paragraph.

**Input premises.** `devtools.fine_net_followup premises` unpacked the asset beside the
pinned documents and ran the maintained readers on the candidate
([receipt](receipts/premises.json)). Lemma N0’s five premises hold on the declared net,
with $B(1 + D) = 25009997/25010000$, and the last bin holds an orientation.
The mass is $n - 1/100000$ over 650 positive rows, and one candidate digest,
`377bcd7b…0777`, appears throughout.
The three narrow readers of the n = 27 follow-up (`measure`, `declared_net`,
`semantic_digest`) took 0.013 seconds.
The full check2 reader (`audit_check2`) took 0.018 seconds; it also binds the source’s
receipt, control and pre-publication run to these bytes.
This checks input premises; it decides no coverage.

**A diagnostic sample of the native capture.** This repository’s `sqverify-fast`, built
from the reviewed crate source `d97758bb…`, ran at eight directions spread over the net,
one thread each and two at a time ([receipt](receipts/sample-diagnostic.json)): 0, 296,
592, 888, 1184, 1480, 1776 and 2072. Each verified, and each matched the source’s log in
node count and least certified bound.
A sample decides only the directions it ran, and is not a replay.

| Direction | Nodes | Process CPU (s) | Wall (s) | Source CPU (s) |
| --- | --- | --- | --- | --- |
| 0 (axis sweep) | — | 0.84 | 2.19 | 1.09 |
| 296 | 212,287 | 1.94 | 5.76 | 2.90 |
| 592 | 224,345 | 2.37 | 6.36 | 4.12 |
| 888 | 295,777 | 3.35 | 8.30 | 5.97 |
| 1184 | 351,783 | 4.02 | 11.38 | 7.31 |
| 1480 | 367,297 | 4.30 | 14.81 | 7.83 |
| 1776 | 414,019 | 4.88 | 17.08 | 7.83 |
| 2072 | 472,383 | 5.65 | 13.54 | 7.51 |

The host’s load average was 12.5 on four cores, so the walls are inflated; CPU is the
price. The sample took 0.613 of the source’s CPU on the same directions.
Applied to the source’s 12,616 CPU seconds over the net, that prices a complete capture
at about 7,740 CPU seconds; the sample’s mean gives 7,080. The whole-net controls of the
6 October review, the 99/100 mutant at every direction plus the original and the
near-threshold mutant at the least-bound direction, add about one more sweep.
The total is about 4.3 CPU-hours, or about 2.2 hours of wall at two workers on an idle
host. That is above the 20 CPU-minute limit for a run inside an intake, so the full net
was not run.

## Review and Replay

The source reports all 2,073 directions verified by its adaptation of this repository’s
crate (build `ab6e33e1…`, 12 threads, 1,058 seconds of wall), and a second run on a
fresh machine in 4,306 seconds.
Its control scales every mass by 197/200 at 32 sampled directions and reports all 32
refused, 31 with an exact capture below the threshold.
These are attributed author outcomes; a sampled control does not replace the whole-net
controls the records lane requires.

**The review.** The
[stage 4 mathematical review of 4 November](../../../../docs/project/reviews/review-2026-11-04-wand125-fine-net-n29.md)
(think-1lri) read this certificate and accepted it with findings, none blocking or
major. It re-derived the argument, recomputed every exact premise apart from the crate
and the tools, read the source’s run log, receipts and control against the candidate,
and decided direction 0 and nine oblique directions over their whole per-bin domains by
code that shares nothing with the crate. Its programs and receipts are in
[`review/`](review/README.md).

**The replay.** On 4 November 2026 (think-r333) the census ran `sqverify-fast`, built
from the reviewed crate source `d97758bb…`, on the candidate retained in
[`release/`](release/certificates/mixed_n29_L582/): every one of the 2,073 directions
verified, 649,871,818 nodes and least certified bound 1.0000000000046825 at direction
1947, in 9,296.0 CPU-seconds at two threads, against the 7,740 priced above.
`devtools.fine_net_followup capture-agreement` finds every direction equal to the
source’s check2 log ([receipt](receipts/capture-agreement-n29.json)).
Its whole-net control the same day ended `CONTROLS_REFUSED`: the original verified again
at 1947, the 99/100 mutant was refused at all 2,073 directions and the near-threshold
mutant was refused. At the axis direction the mutant’s exact capture lies in the
enclosure the vertex sweep held at its least vertex, recomputed apart from the crate,
whose lower end is the crate’s bound to the bit, as #892’s rule requires; the gap of
5.2e-10 that the review’s F-8 measured sits near the middle of an enclosure 1.05e-9
wide.
The receipts are in the
[census folder](../../../benchmarks/measure-verifier/census-mixed/wand125-fine-net-n29-2026-10-10/README.md),
and with the review they put T-132 at V3/C3: n29’s lower lanes hold $291/50$.

## Sources and Notices

The nearest enclosing source notice, `problems/square-lower-bounds/LICENSE`, is MIT,
Copyright 2026 wand125, byte-identical to the notice the seven-case packet records.
The nested verifier archive carries no notice of its own, so its redistribution is
unresolved. Until 2 November this packet published only authored facts, hash references
and this repository’s own receipts.

On 2 November 2026 (T-132’s census, think-r333) the asset’s six data members were
retained under [`release/`](release/certificates/mixed_n29_L582/), at their paths in the
asset, so that the census can read the candidate, by the owner’s answer of 17 October to
retain fine-net candidates where the census reads them, as the n31, #446 release and 13
October packets do. `devtools.fine_net_followup retain` held the asset to its pinned
651,878 bytes and SHA-256 and copied the candidate (as deterministic gzip of the 182,193
bytes, SHA-256 `c9171c92…`, the source manifest pins), the check2 receipt, run log,
control and control log, and the pre-publication receipt, each equal to the manifest’s
size and digest. The nested verifier archive and the sealed inner bundle are pinned by
digest only, with their reasons, in the [retention record](acquisition/release-assets.json),
which `devtools.fine_net_followup check-retained` re-derives from the packet.
No program of the source was run.

The source credits wand125; the commit is authored by Hiroaki Hosono.
Its README says parts of the work were produced with AI assistance under human
direction, and the commit names Claude Opus 5.5 as co-author.

## Compressed Files

| Stored file | Origin | Git blob (decompressed) | SHA-256 (decompressed) |
| --- | --- | --- | --- |
| `release/certificates/mixed_n29_L582/candidate.json.gz` | upstream | `ac6f7f2d2219ca1fbddd7bc5f1de7c803cccca72` | `c9171c9278271b6b4ca5fb9f925ea42a15a88e9aca7701d6542e29e38979722b` |

## Original Gzip Files

| Stored file | Origin | Git blob | SHA-256 |
| --- | --- | --- | --- |
| `release/certificates/mixed_n29_L582/check2/control-197_200.jsonl.gz` | upstream | `6b370a13e8dae232c2938efb39f2be83db99079b` | `6ceca1e90beafc30dac48a3b3a29109798412980995c741e5d9e845b968e1eaf` |
| `release/certificates/mixed_n29_L582/check2/run.jsonl.gz` | upstream | `4d0c335c9d510e0b50201a72a6f4803f455f190e` | `6bce9a2ae9aa2616bfdc5f91704a19091765d70c23513651bcc8e345e550f171` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
