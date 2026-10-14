# Reported Fine-Net Lower Bounds for n = 37, 39 and 44, 13 October

Three commits of 13 October to wand125/square-packing add check2 measure certificates on
the 2,073-direction net of T-132, T-142 and T-143: `mixed_n39_L66625`, reporting
$s(39) \ge 533/80 = 6.6625$; `mixed_n44_L69975`, reporting $s(44) \ge 2799/400 = 6.9975$;
and `mixed_n37_L64975`, reporting $s(37) \ge 2599/400 = 6.4975$. No issue reports them;
the watch survey of 14 October found them (think-fxs7). All three bounds remain
unconfirmed here; no standing bound or rating changes.

| Item | n = 37 | n = 39 | n = 44 |
| --- | --- | --- | --- |
| Source | [`mixed_n37_L64975`](https://github.com/wand125/square-packing/tree/7a42c16eacaab112b537ab09e89d3485f6f4c75f/problems/square-lower-bounds/certificates/mixed_n37_L64975) | [`mixed_n39_L66625`](https://github.com/wand125/square-packing/tree/dfb2cf85fdf9ee5f95c5ec2c67fd49210854f146/problems/square-lower-bounds/certificates/mixed_n39_L66625) | [`mixed_n44_L69975`](https://github.com/wand125/square-packing/tree/9f24185c602c8c0b83cf6a88b11a69ea8d668673/problems/square-lower-bounds/certificates/mixed_n44_L69975) |
| Added by | `7a42c16`, 2026-10-13T03:18:05Z | `dfb2cf8`, 2026-10-13T03:01:37Z | `9f24185`, 2026-10-13T03:01:53Z |
| Release asset | `certificates__mixed_n37_L64975.tar.gz`, 630,375 bytes, SHA-256 `8aa78cc4…1965` | `certificates__mixed_n39_L66625.tar.gz`, 639,558 bytes, SHA-256 `8e88ca06…851f` | `certificates__mixed_n44_L69975.tar.gz`, 631,497 bytes, SHA-256 `b4cf96d5…3eb4` |
| Candidate | 612 positive rectangles, mass $3699999/100000$ | 687 positive rectangles, mass $3899999/100000$ | 606 positive rectangles, mass $4399999/100000$ |
| Candidate digest | `23387d7d…4495` | `3b464f3f…9cfc` | `02f4933f…24ef` |
| Standing bound | T-069’s $161/25$, both lanes; $+23/400$ | T-110’s $133/20$, both lanes; $+1/80$ | T-090’s $2789/400$, both lanes; $+1/40$ |
| Upper bound | 6.59861… | 6.81072… | 7 |

All three declare core $4999/5000$ and the net `{"step": "1/5002", "last": 2072}`, and
all use release `square-lower-bounds-v1`. No count is settled: the least gap to an upper
bound is n = 44’s $1/400$.

The packet is pinned at `7a42c16eacaab112b537ab09e89d3485f6f4c75f`, the last of the
three commits, which holds all three directories. Each directory is the same Git tree from
the commit that adds it through the repository’s head when read, `9a28a84` (2026-10-14),
whose later commits add the n = 145 certificate of the
[companion packet](../wand125-linear-n145-2026-10-13/README.md) and change the
closed-form problem, the right isosceles triangle and the site, and not these directories
or their licence. Retrieved 2026-10-14T09:22Z.

## What Is Retained

[`devtools.acquire_source`](../../../devtools/acquire_source.py) wrote the packet from
its [declaration](acquisition/declaration.json): the
[acquisition record](acquisition/sources.json) and the
[subtree manifest](acquisition/upstream-subtree.sha256) give the size and SHA-256 of all
34 files in scope, and `--check` re-derives them. Twelve are retained byte for byte under
[`square-packing/`](square-packing/problems/square-lower-bounds/certificates/): each
directory’s `README.md`, `ASSET.json`, `bundle.json` and `files-sha256.json`.
The other 22 are pinned by digest only, each with its reason in the record:

- the licence, and each directory’s `SPEC.md`, `REPRODUCE.md`, `UPSTREAM_COMMIT`,
  `fine_net_check.sh` and `provenance/search-notes.md`, which are byte-identical to
  copies the FN-1 and 6 October check2 packets retain;
- each directory’s `check2/src/SOUNDNESS.md` and `INDEPENDENCE.md`, which are this
  repository’s own `packing/sqverify_fast/` notes as of `e020eb1e2` (Git blobs
  `cadf59b6` and `9b60b4af`), the edition before `f007d7afd` added lemma N0 for declared
  nets.

The release assets are not retained: each holds the candidate, the check2 receipt, run
log and control, the sealed inner bundle, the pre-publication receipt and the nested
verifier archive `sqverify-proof-net-fe12e036c.tar.gz`. They stay with their author,
pinned here by size and digest, and the receipts below inventory every member.

## What Was Checked

**Custody.** Each asset’s size and SHA-256 equal the release API’s digest (asset ids
635741442, 635702665 and 635703292), the release’s `SHA256SUMS` (lines 444, 442 and 443)
and the source’s `ASSET.json`. Each of the 11 documents of each directory has the Git
blob its commit names. Each sealed inner bundle holds 16 files and matches all 15 entries
of its own `files-sha256.json`; six of its payloads repeat the outer asset’s byte for
byte. The verifier archive is `e495f9bf…71e81` in all three, the archive the n = 28 to 30
packets inventory. Each README edition differs from its sealed one by the pre-publication
paragraph.

**Input premises.** `devtools.fine_net_followup premises` unpacked each asset beside its
pinned documents and ran the maintained readers on the candidate
([n = 37](receipts/premises-n37.json), [n = 39](receipts/premises-n39.json),
[n = 44](receipts/premises-n44.json)). For all three, Lemma N0’s five premises and its
last bin hold on the declared net, with $B(1 + D) = 25009997/25010000$; the mass is
$n - 1/100000$ over positive rows only; one candidate digest appears throughout; and the
full check2 reader (`audit_check2`) holds every premise. Exact premises hold. The readers
took under 0.03 seconds each, and no program of the source ran.

**Two reported complete runs each.** Each check2 receipt records the source’s adapted
crate (build `ab6e33e1…`, binary `ec04d332…`) verifying all 2,073 directions, and each
pre-publication receipt a second run of the same source on a fresh Ubuntu 24.04 machine
that is not the run the check2 receipt embeds:

|  | n = 37 | n = 39 | n = 44 |
| --- | --- | --- | --- |
| check2 run: wall (s), threads | 1,146.4, 16 | 1,682.7, 12 | 2,785.4, 16 |
| check2 run: direction CPU (s) | 13,474 | 13,502 | 35,894 |
| check2 run: nodes | 864,953,550 | 881,271,470 | 1,166,443,954 |
| Pre-publication run: wall (s) | 619 | 697 | 1,654 |

Each control scales every mass by 197/200 at 32 sampled directions and reports all 32
refused, 31 with an exact capture below the threshold. These are attributed author
outcomes; a sampled control does not replace the whole-net controls the records lane
requires.

**A diagnostic sample of the native capture.** This repository’s `sqverify-fast`, built
from the reviewed crate source `d97758bb…` (binary `567a0fd5…`, the n = 28 to 30
samples’ binary), ran eight directions of each net, one thread each and one at a time
([n = 37](receipts/sample-diagnostic-n37.json),
[n = 39](receipts/sample-diagnostic-n39.json),
[n = 44](receipts/sample-diagnostic-n44.json)): 0, 296, 592, 888, 1184, 1480, 1776 and
2072\. All 24 verified, and each matched the source’s log in node count and least
certified bound. A sample decides only the directions it ran, and is not a replay.

**The whole-net control’s mutant at two directions.** The control the census runs, every
mass scaled by 99/100 at every direction (FC-1), counts only if every refusal is a
coverage refusal at a pose in the centre domain whose capture, evaluated again apart from
the crate, is below 1. `fine_net_followup control-sample` runs that mutant at chosen
directions and judges each refusal with the census’s own `refusal_record` and
`refusal_held` ([n = 37](receipts/control-sample-n37.json),
[n = 39](receipts/control-sample-n39.json),
[n = 44](receipts/control-sample-n44.json)). It is the command of `fc3199fc0` on the
unmerged branch `claude/wand125-confirmations-2026-10-11` (file blob `614d2be3` at
`44eb6a017`), run with this tree’s census and `check_sqverify_fast`, which that commit
does not change. It ran direction 0 and the oblique direction of least certified bound in
the source’s log (1919, 1804 and 622), in under 3 CPU seconds each:

| n | Axis: exact capture minus the sweep’s certified bound | Axis refusal counts | Oblique refusal counts |
| --- | --- | --- | --- |
| 37 | $6.9 \times 10^{-11}$ | yes | yes |
| 39 | $1.26 \times 10^{-9}$ | **no** | yes |
| 44 | $1.3 \times 10^{-10}$ | yes | yes |

At n = 39 the axis refusal is sound (an exact capture below 1 at a centre inside the
domain), but the gap is above the census’s `AXIS_ROUNDING` of $10^{-9}$, so the whole-net
control would end `CONTROL_FAILED`. It is the defect T-142’s control is held for
(2.15e-9 there), so the owner’s answer to that question on jlevy/squares#543 decides
n = 39’s control too.
These are diagnostics of the directions they ran and are no control receipts.

## The Price of a Complete Replay

|  | n = 37 | n = 39 | n = 44 |
| --- | --- | --- | --- |
| Sample CPU, here and at the source (s) | 43.08 and 49.45 | 48.06 and 50.86 | 107.87 and 126.98 |
| Ratio | 0.871 | 0.945 | 0.850 |
| Host load average, before and after | 0.8 and 0.9 | 0.9 and 4.6 | 4.6 and 9.3 |
| Priced full capture (CPU s) | 11,739 | 12,758 | 30,492 |
| Priced whole-net controls (CPU s) | 11,759 | 12,781 | 30,533 |
| Total | 6.53 CPU-hours | 7.09 CPU-hours | 16.95 CPU-hours |
| At the source’s own CPU, twice over the net | 7.49 CPU-hours | 7.50 CPU-hours | 19.94 CPU-hours |

The controls are those of the 6 October review: the 99/100 mutant at every direction, and
the original and the near-threshold mutant at the least-bound direction. The three come to
about 30.6 CPU-hours at the sample’s ratios, and 34.9 if this host is no faster than the
source’s, or about 15 to 17.5 hours of wall at two workers on an idle host.
That is far above the 20 CPU-minute limit for a run inside an intake, so no full net was
run.

## Review and Remaining Work

A maintained replay must retain the complete direction outcomes of a census run from
reviewed source, from a candidate retained where the census reads it, with the whole-net
controls and restored positives, and must be followed by a review that reads each
certificate, by the checklist of the 6 October declared-net soundness review. The census
reads candidates from packets, which retaining these candidates in Git would need: the
owner’s question on jlevy/squares#543 for T-132, T-142 and T-143 applies here as well. The
n = 39 control needs the `AXIS_ROUNDING` decision first. That work, with a budget for it,
belongs to the import’s bead, think-u0av.

## Sources and Notices

The nearest enclosing source notice, `problems/square-lower-bounds/LICENSE`, is MIT,
Copyright 2026 wand125, the same blob (`bbfbff13`) at the pin and at the head, and
byte-identical to the notice the FN-1 packet retains.
The nested verifier archive carries no notice of its own, so its redistribution is
unresolved, and it is not retained.
No program of the source was run.

The source credits wand125 (Hiroaki Hosono), with code and formats credited to Evan
Daniel, tokoharu and jlevy/squares; all three commits are authored by Hiroaki Hosono. The
`problems/square-lower-bounds/README.md` says parts of the work were produced with AI
assistance under human direction, and each commit names Claude Opus 5.5 as co-author.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
