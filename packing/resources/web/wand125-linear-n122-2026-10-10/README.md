# Reported Linear Lower Bound for n = 122, 10 October

A commit of 10 October to wand125/square-packing adds `mixed_n122_L1126`, a linear
certificate reporting $s(122) \ge 563/50 = 11.26$: a measure of point masses, uniform
segments and uniform rectangles of the kind T-080 holds, on T-080’s net, checked by
T-080’s checker. Its mass is below 122, and a packing of more squares contains one of
122, so it reports $s(N) \ge 11.26$ for every $N \ge 122$. That raises the record at n =
122 to 126 and nowhere else.
No issue reports it; the evening watch read of 10 October found it.
The bound remains unconfirmed here; no standing bound or rating changes.

| Item | Value |
| --- | --- |
| Source | [`mixed_n122_L1126`](https://github.com/wand125/square-packing/tree/a9f76c382d023b4095899c4eb7ea7483b8b87ecf/problems/square-lower-bounds/certificates/mixed_n122_L1126) |
| Pinned revision | `a9f76c382d023b4095899c4eb7ea7483b8b87ecf`, committed 2026-10-10T10:41:36Z, unchanged through the head when read, `27ed168` |
| Release asset | `certificates__mixed_n122_L1126.tar.gz` in `square-lower-bounds-v1`, 31,784,537 bytes, SHA-256 `6443eae0…5deb` |
| Retrieved | 2026-10-10T17:00:59Z |
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
| 126 | Nagamochi, 11.24695… | Karakuş strip, 11.23545… |
| 127 | Nagamochi, 11.29563…, above 11.26 | Karakuş strip, 11.28192…, above 11.26 |

The source compares its side with an exact rational upper bound on Green’s value and
states the margin as more than 0.0307191; the maintained reader confirms that the side
exceeds Green’s bound and Nagamochi’s at n = 122. Green’s proof has not been recovered
here (the n = 122 case record says so), so a certificate-backed bound would replace an
unproved report in the reported lane.

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

## Sources and Notices

The nearest enclosing source notice, `problems/square-lower-bounds/LICENSE`, is MIT,
Copyright 2026 wand125, byte-identical to the notice the #446 packet records; it covers
the certificate directory, its `code/` included.
This packet nonetheless retains no upstream byte: it publishes authored facts, hash
references and this repository’s own receipts, and the asset stays with its author,
pinned by size and digest.
The sample ran the source’s replay function and checker from this repository’s retained
copies; nothing from the asset or the source tree was executed.

The source credits wand125; the commit is authored by Hiroaki Hosono.
Its README says parts of the work were produced with AI assistance under human
direction, and the commit names Claude Opus 5.5 as co-author.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
