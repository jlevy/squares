# Reported Linear Lower Bound for n = 145, 13 October

A commit of 13 October to wand125/square-packing adds `mixed_n145_L1224`, a linear
certificate reporting $s(145) \ge 306/25 = 12.24$: a measure of point masses, uniform
segments and uniform rectangles of the kind T-080 and T-144 hold, on their net, checked
by their checker. Its mass is below 145, and a packing of more squares contains one of
145, so it reports $s(N) \ge 12.24$ for every $N \ge 145$. That raises the record at n =
145 to 149 and nowhere else, and settles no count there.
No issue reports it; the watch survey of 14 October found it (think-fxs7).
The bound remains unconfirmed here; no standing bound or rating changes.

| Item | Value |
| --- | --- |
| Source | [`mixed_n145_L1224`](https://github.com/wand125/square-packing/tree/22f06b31a9295c8185be5d30a1a7b19982b16847/problems/square-lower-bounds/certificates/mixed_n145_L1224) |
| Pinned revision | `22f06b31a9295c8185be5d30a1a7b19982b16847`, committed 2026-10-13T06:18:13Z, the same Git tree through the head when read, `9a28a84` (2026-10-14) |
| Release asset | `certificates__mixed_n145_L1224.tar.gz` in `square-lower-bounds-v1`, 38,598,220 bytes, SHA-256 `6a937dc7…2a49` |
| Retrieved | 2026-10-14T09:22Z |
| Measure | 594 point, 1,541 segment and 9 rectangle orbits under D4, mass $14499999/100000$ |
| Net | core $9977/10000$, 201 half-angles of step $83/40000$: `mixed_n101_L1028`’s |
| Checker | `code/unified_linear_verify.cpp`, SHA-256 `0249726a…a06d`, V-wand125-unified-linear-verify-cpp |

## What It Would Change

| n | Reported lower bound | Verified lower bound | Upper bound |
| --- | --- | --- | --- |
| 145 | Green, DS7 Theorem 9 with k = 12, 12.21386… | Karakuş strip, 12.04339… | 12.53553… |
| 146 to 148 | Green’s, by monotonicity, 12.21386… | Karakuş strip, 12.08663… to 12.17261… | 12.58378… to 12.65685… |
| 149 | Nagamochi, 12.22497… | Karakuş strip, 12.21537… | 12.70710… |
| 150 | Nagamochi, 12.26942…, above 12.24 | Karakuş strip, 12.25797…, above 12.24 | 12.77817… |

The source compares its side with an exact rational upper bound on Green’s value, from
90-digit integer square roots, and states the margin as more than 0.0261330; the
maintained reader confirms that the side exceeds Green’s bound and Nagamochi’s at n =
145\. Green’s proof has not been recovered, and the unavoidable-set argument DS7’s
Figure 34 illustrates leaves a unit square empty at k = 12 (the n = 145 case record, and
jlevy/squares#308), so a certificate-backed bound would replace an unproved report in the
reported lane. Every upper bound stays
above 12.24, so the consequences at 146 to 149 take no entry of their own.

The same source’s closed-form bound $a(N)$ of the same day (`eb0fd19`, whose import
think-tsox owns) prints 12.0561, 12.1125, 12.1669, 12.2277 and 12.2804 at n = 145 to 149 in its
table: below 12.24 at 145 to 148, and above it at 149.

## What Is Retained

[`devtools.acquire_source`](../../../devtools/acquire_source.py) wrote the packet from
its [declaration](acquisition/declaration.json): the
[acquisition record](acquisition/sources.json) and the
[subtree manifest](acquisition/upstream-subtree.sha256) give the size and SHA-256 of all
19 files in scope, and `--check` re-derives them. Four are retained byte for byte under
[`square-packing/`](square-packing/problems/square-lower-bounds/certificates/mixed_n145_L1224/):
`README.md`, `ASSET.json`, `manifest.json` and `completion-audit.json`. The other 15 are
pinned by digest only: the licence, byte-identical to the FN-1 packet’s, and all 13 files
of `code/` with `requirements.txt`, byte-identical to the reviewed copies the 2 October
linear packet (seven files and `requirements.txt`) and the 28 September point-and-mixed
packet (six) retain.

The release asset is not retained: it holds `candidate.json` (516,199 bytes),
`certificate.json` (39,867 bytes, SHA-256 `e3c58aa2…92ca`) and the proof bundle
`n145-L12.24-proof-bundle.tar.gz` (47,407,937 bytes, SHA-256 `4dc4f673…0a0b`, the digest
the README and `completion-audit.json` state). It stays with its author, pinned here by
size and digest.

## What Was Checked

**Custody.** The asset’s size and SHA-256 equal the release API’s digest (asset
636102989), the release’s `SHA256SUMS` (line 445, updated with it at 06:18Z) and the
source’s `ASSET.json`. Each of the 18 pinned documents has the Git blob the commit names.

**Input premises.** `devtools.fine_net_followup linear-premises` unpacked the asset
beside the pinned documents and ran the T-080 route’s own readers on it, given the files
and their digests in place of a packet’s retained copies
([receipt](receipts/linear-premises.json)):

- `linear_certificate` (3.2 seconds): the stated count, side, core and orbit counts,
  every primitive inside the container, nondegenerate and nonnegative, the exact total
  $145 - 1/100000$, invariance of the 17,152 D4 images, the candidate digest
  `31788dc7…ca69` by the source’s rule throughout, the net’s containment, a positive
  centre domain at all 201 angles (least at angle 200), the checker and code identity, a
  replay record at every angle (124,435,707 nodes, at most 3,330,973 at the axis, under
  the manifest’s limit of 12,000,000) and the source audit’s certificate and archive
  digests;
- `bundle_bindings`: the proof bundle’s 810 files, with 202 copies of the pinned checker
  and every angle’s candidate the top-level one;
- `check_inputs` (77.1 seconds): every one of the 201 inputs hashes to its recorded
  digest and encloses, interval by interval, the exact data recomputed from the
  candidate.

Exact premises hold.
None of these readers runs a program of the source, and none decides coverage.

**A diagnostic replay sample.** `devtools.fine_net_followup linear-sample` replayed two
angles as `linear-replay` does: the shipped `code/` assembled from the retained copies,
the driver’s preconditions, each sampled input bound to the candidate, the checker built
by the shipped `compile_verifier`, and the shipped `replay_angle`, one angle at a time
([receipt](receipts/linear-sample-diagnostic.json)). Both returned the certificate’s own
record. A sample decides only the angles it ran, and is not a replay.

| Angle | Nodes | CPU here (s) | Wall (s) | Source (s) | Load before |
| --- | --- | --- | --- | --- | --- |
| 35, the fewest nodes | 168,149 | 163.7 | 286.9 | 138.1 | 9.6 |
| 111, the median | 380,027 | 382.4 | 401.4 | 312.2 | 3.0 |

The host is four cores shared with other work, so CPU is the price.
At the sample’s ratio, 1.213, the source’s 109,342 seconds over the net price a complete
replay at about 132,600 CPU seconds; by nodes it is 124,000. The route’s control, the
original and two mutations at angle 35, adds about 500. The total is about 37 CPU-hours,
or about 18.5 hours of wall at two workers, and no complete replay is shorter than the
axis angle, about 3,400 seconds here.
The ratio is above the 0.776 the n = 122 sample measured, so an idle host may price it
nearer 24 CPU-hours. The author’s own replay took 2 hours 8 minutes at 30 workers, at
most about 64 CPU-hours.
That is far above the 20 CPU-minute limit for a run inside an intake, so the net was not
replayed.

## Review and Remaining Work

The source reports all 201 angles verified, 109,342 seconds summed over its records, and
a complete replay from the tarball on a fresh machine that ended
`ALL_LINEAR_ANGLES_REPLAYED_MATCHING_CERTIFICATE`; no receipt of that replay is
published. Its audit says the replay re-executes the same implementation and is not an
independent algorithm.

Stage 4 is the T-080 route as T-144’s is prepared: register the certificate in
`devtools.audit_wand125_linear`, which reads the retained `README.md`, `manifest.json`
and `completion-audit.json` here and needs `candidate.json` and `certificate.json`
retained beside them, as the MIT notice permits, so that `linear-replay` writes resumable
receipts over all 201 angles; then `linear-control` and a review that reads this
certificate, as the 2 October review read T-080’s. That work, with a budget for it,
belongs to the import’s bead, think-u0av.

## Sources and Notices

The nearest enclosing source notice, `problems/square-lower-bounds/LICENSE`, is MIT,
Copyright 2026 wand125, the same blob (`bbfbff13`) at the pin and at the head, and
byte-identical to the notice the FN-1 packet retains; it covers the certificate
directory, its `code/` included.
The sample ran the source’s replay function and checker from this repository’s retained
copies; nothing from the asset or the source tree was executed.

The source credits wand125 (Hiroaki Hosono), with code and formats credited to Evan
Daniel, tokoharu and jlevy/squares; the commit is authored by Hiroaki Hosono. The
`problems/square-lower-bounds/README.md` says parts of the work were produced with AI
assistance under human direction, and the commit names Claude Opus 5.5 as co-author.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
