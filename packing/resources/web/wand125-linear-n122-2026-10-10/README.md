# Reported Linear Lower Bound for n = 122, 10 October

A commit of 10 October to wand125/square-packing adds `mixed_n122_L1126`, a linear
certificate reporting $s(122) \ge 563/50 = 11.26$: a measure of point masses, uniform
segments and uniform rectangles of the kind T-080 holds, on T-080’s net, checked by
T-080’s checker. Its mass is below 122, and a packing of more squares contains one of
122, so it reports $s(N) \ge 11.26$ for every $N \ge 122$. That raises the record at n =
122 to 126 and nowhere else.
No issue reports it; the evening watch read of 10 October found it.
Until XXX-DATE the bound was unconfirmed here; its complete replay, the route’s control
and the review [below](#review-and-remaining-work) now put T-144 at V3/C3.

| Item | Value |
| --- | --- |
| Source | [`mixed_n122_L1126`](https://github.com/wand125/square-packing/tree/a9f76c382d023b4095899c4eb7ea7483b8b87ecf/problems/square-lower-bounds/certificates/mixed_n122_L1126) |
| Pinned revision | `a9f76c382d023b4095899c4eb7ea7483b8b87ecf`, committed 2026-10-10T10:41:36Z, unchanged through the head when read, `27ed168`, and through `ea1c454` (2026-10-31) when read again on 18 November |
| Release asset | `certificates__mixed_n122_L1126.tar.gz` in `square-lower-bounds-v1`, 31,784,537 bytes, SHA-256 `6443eae0…5deb` |
| Retrieved | 2026-10-10T17:00:59Z; the documents and the asset again 2026-11-18T05:30Z, for the retention below |
| Measure | 502 point, 1,268 segment and 3 rectangle orbits under D4, mass $12199999/100000$ |
| Net | core $9977/10000$, 201 half-angles of step $83/40000$: `mixed_n101_L1028`’s |
| Checker | `code/unified_linear_verify.cpp`, SHA-256 `0249726a…a06d`, V-wand125-unified-linear-verify-cpp |

The [follow-up facts](reported-n122.json) record every exact value and identity above,
and the [source manifest](source-manifest.json) the size, Git blob and SHA-256 of every
pinned document and archive member.

## What It Would Change

| n | Reported lower bound | Verified lower bound |
| --- | --- | --- |
| 122 | Green, DS7 Theorem 9 with k = 11, 11.22928… | Karakuş strip, 11.04751… |
| 123 to 125 | Green’s, by monotonicity, 11.22928… | Karakuş strip, 11.09481… to 11.18877… |
| 126 | Nagamochi, 11.24695…; since 14 October Hosono’s closed form, 11.31332…, above 11.26 | Karakuş strip, 11.23545… |
| 127 | Nagamochi, 11.29563…, above 11.26 | Karakuş strip, 11.28192…, above 11.26 |

The source compares its side with an exact rational upper bound on Green’s value and
states the margin as more than 0.0307191; the maintained reader confirms that the side
exceeds Green’s bound and Nagamochi’s at n = 122. Green’s proof has not been recovered
here (the n = 122 case record says so), so a certificate-backed bound would replace an
unproved report in the reported lane.
At n = 126 the same source’s closed form of 14 October (T-180), $a(126) = 11.31332\ldots$,
took the reported lane after this packet was written, so there the certificate would
raise the verified lane alone.

## What Is Retained

On 18 November 2026 (think-nd7g)
[`devtools.acquire_source`](../../../devtools/acquire_source.py) wrote the packet’s
pinned-tree part from its [declaration](acquisition/declaration.json), from a blobless,
sparse clone of the source at the pin: the
[acquisition record](acquisition/sources.json) and the
[subtree manifest](acquisition/upstream-subtree.sha256) give the size and SHA-256 of all
19 files in scope, and `--check` re-derives them. Four are retained byte for byte under
[`square-packing/`](square-packing/problems/square-lower-bounds/certificates/mixed_n122_L1126/):
`README.md`, `ASSET.json`, `manifest.json` and `completion-audit.json`, 6,924 bytes. The
other 15 are pinned by digest only: the licence, byte-identical to the FN-1 packet’s,
and all 13 files of `code/` with `requirements.txt`, byte-identical to the reviewed
copies the 2 October linear packet and the 28 September point-and-mixed packet retain.

The same day `devtools.fine_net_followup retain` held the release asset to its pinned
size and SHA-256 again (equal to the release API’s digest, asset 627696187) and copied
its candidate and certificate to [`release/`](release/certificates/mixed_n122_L1126/),
each as deterministic gzip (41,652 and 11,329 bytes), as the MIT notice permits; both
have the SHA-256 the 10 October [source manifest](source-manifest.json) records. The
proof bundle, beyond `OR-18`’s size rule, is pinned by digest only in the
[retention record](acquisition/release-assets.json), which
`devtools.fine_net_followup check-retained` re-derives from the packet.
`devtools.audit_wand125_linear` registers the certificate as `n122`, as it registers
T-179’s `n145`: it reads the four documents here and the two members there, and for a
replay takes the asset from the release, holds it to its pin, and copies out the
bundle, which it holds to the record’s digest before anything runs. Its exact audit of
the retained bytes is [`receipts/linear-audit.json`](receipts/linear-audit.json), and
its pre-replay checks over all 201 angles, which bind the bundle’s 810 files and every
input to the candidate, are [`receipts/n122/fetch.json`](receipts/n122/fetch.json).

## What Was Checked

**Custody.** The asset’s size and SHA-256 equal the release API’s digest and the
source’s `ASSET.json`. The release’s `SHA256SUMS`, as updated at 14:12Z with the n = 30
asset, lists neither this asset’s name nor its digest.
Each of the 18 pinned documents has the Git blob the commit names.
The asset holds three files: `candidate.json`, `certificate.json` and the proof bundle
`n122-L11.26-proof-bundle.tar.gz` (38,912,523 bytes, SHA-256 `3986d902…55d0`), whose
digest is the one the README and `completion-audit.json` state.
Every file of `code/` is byte-identical to a retained, reviewed copy in this repository,
seven in the 2 October linear packet and six in the 28 September point-and-mixed packet,
and `requirements.txt` is the linear packet’s.

**Input premises.** `devtools.fine_net_followup linear-premises` unpacked the asset
beside the pinned documents and ran the T-080 route’s own readers on it, given the files
and their digests in place of a packet’s retained copies
([receipt](receipts/linear-premises.json)):

- `linear_certificate` (1.7 seconds): the stated count, side, core and orbit counts,
  every primitive inside the container, nondegenerate and nonnegative, the exact total
  $122 - 1/100000$, invariance of the 14,184 D4 images, the candidate digest
  `c91a7509…e9ed4` by the source’s rule throughout, the net’s containment, a positive
  centre domain at all 201 angles (least at angle 200), the checker and code identity, a
  replay record at every angle (73,694,735 nodes, at most 2,218,683 at the axis, under
  the manifest’s limit of 3,000,000) and the source audit’s certificate and archive
  digests;
- `bundle_bindings`: the proof bundle’s 810 files, with 202 copies of the pinned checker
  and every angle’s candidate the top-level one;
- `check_inputs` (53.5 seconds): every one of the 201 inputs hashes to its recorded
  digest and encloses, interval by interval, the exact data recomputed from the
  candidate.

Exact premises hold.
None of these readers runs a program of the source, and none decides coverage.

**A diagnostic replay sample.** `devtools.fine_net_followup linear-sample` replayed two
angles as `linear-replay` does: the shipped `code/` assembled from the retained copies,
the driver’s preconditions, each sampled input bound to the candidate, the checker built
by the shipped `compile_verifier`, and the shipped `replay_angle`, two angles at a time
([receipt](receipts/linear-sample-diagnostic.json)). Both returned the certificate’s own
record. A sample decides only the angles it ran, and is not a replay.

| Angle | Nodes | CPU here (s) | Wall (s) | Source (s) |
| --- | --- | --- | --- | --- |
| 37, the fewest nodes | 106,543 | 57.4 | 81.0 | 73.6 |
| 108, near the median | 216,229 | 117.9 | 145.0 | 152.0 |

The host’s load average was 5.1 on four cores, so CPU is the price.
At the sample’s ratio, 0.776, the source’s 51,877 seconds over the net price a complete
replay at about 40,300 CPU seconds; by nodes it is 40,000. The route’s control, the
original and two mutations at angle 37, adds about 170. The total is about 11.2
CPU-hours, or about 5.6 hours of wall at two workers on an idle host, and no complete
replay is shorter than the axis angle, about 1,240 seconds here.
The author’s own replay took 7 hours 41 minutes at three workers, which would be about
23 CPU-hours at full use, so budget between the two.
That is far above the 20 CPU-minute limit for a run inside an intake, so the net was not
replayed.

## Review and Remaining Work

The source reports all 201 angles verified, 51,877 seconds summed over its records, and
a complete replay from the tarball on a fresh machine that ended
`ALL_LINEAR_ANGLES_REPLAYED_MATCHING_CERTIFICATE`; no receipt of that replay is
published. Its audit says the replay re-executes the same implementation and is not an
independent algorithm.

Stage 4 is the T-080 route: register the certificate in `devtools.audit_wand125_linear`,
which needs the five small files of the directory (`candidate.json`, `certificate.json`,
`manifest.json`, `completion-audit.json` and the README) retained in a packet of that
shape, as the MIT notice permits, so that `linear-replay` writes resumable receipts over
all 201 angles; then `linear-control` and a review that reads this certificate, as the 2
October review read T-080’s. That work, with a budget for it, belongs to the import’s
bead, think-nd7g.

That replay ran here XXX-ON-RUN-DATES (think-nd7g), in XXX-RUNS runs of two workers over
the four ranges of `linear-plan n122 --parts 4` (0-76, 77-149, 150-182 and 183-200), the
first resumed after a container restart: `linear-replay n122` replayed all 201 angles,
each returning the certificate’s own record, in XXX-CPU-H CPU-hours, the axis 1,375
CPU-seconds of it, and `linear-merge n122` reports `FULL_REPLAY_MATCHES_SHIPPED`
([merge](receipts/n122/merged.json), with each range’s rows and runs beside it).
`linear-control n122` accepts the original and refuses two mutations at net index
XXX-CONTROL-INDEX, each provably uncovered there in exact arithmetic
([control](receipts/n122/control.json)). With the
[review of XXX-REVIEW-DATE](XXX-REVIEW-PKTLINK) they put T-144 at V3/C3, and the case
records at n = 122 to 126 take $563/50$ in the verified lane, and at 122 to 125 in the
reported lane.

## Sources and Notices

The nearest enclosing source notice, `problems/square-lower-bounds/LICENSE`, is MIT,
Copyright 2026 wand125, byte-identical to the notice the #446 packet records; it covers
the certificate directory, its `code/` included.
Until 18 November the packet retained no upstream byte; it now retains the four
documents and two release members above under that notice, and the asset and its proof
bundle stay with the author, pinned by size and digest.
The sample ran the source’s replay function and checker from this repository’s retained
copies; nothing from the asset or the source tree was executed.

The source credits wand125; the commit is authored by Hiroaki Hosono.
Its README says parts of the work were produced with AI assistance under human
direction, and the commit names Claude Opus 5.5 as co-author.

## Compressed Files

| Stored file | Origin | Git blob (decompressed) | SHA-256 (decompressed) |
| --- | --- | --- | --- |
| `release/certificates/mixed_n122_L1126/candidate.json.gz` | upstream | `50b46ace41f84cbdb49ff0126a795fe0140d2c5e` | `cd427ddb238b69b7d9ba32ac01616a8669f154af2e70abdff827c313a1ea500c` |
| `release/certificates/mixed_n122_L1126/certificate.json.gz` | upstream | `542414fee42cedbd5d62396f154b10deba5f4d17` | `6b57cddadcb75c6f29fbfc3384b521f86dca5deb5d9620df0ee78fbb39dfe709` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
