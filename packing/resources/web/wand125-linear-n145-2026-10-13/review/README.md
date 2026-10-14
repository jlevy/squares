# The Mathematical Review’s Programs, 14 October 2026

These are the programs the
[mathematical review](../../../../../docs/project/reviews/review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md)
of wand125’s `mixed_n145_L1224` wrote and ran on 14 October 2026, kept as they ran, with
the output each printed in [`outputs/`](outputs/). The review was the stage-4
mathematical review of the import think-u0av, by an AI agent, Fable, strong tier, max
reasoning, prompted separately from the intake lane and working in a worktree of its
own. Each program ran with the project interpreter (Python 3.14.7, `python3 -I`),
reading the release asset `certificates__mixed_n145_L1224.tar.gz`, unpacked in scratch
space and digested against the packet’s pins, and its proof bundle, as data. No program
imports or executes anything of the source, and the source’s checker was not run here.

## What Its Authors Read

Before writing these programs the lane read the
[2 October review](../../../../../docs/project/reviews/review-2026-10-02-wand125-linear-certificates-and-n76.md)
of the T-080 route, which derived the argument from a linear measure to the bound and
read the checker; the premise readers of `devtools.audit_wand125_linear`; and, as data,
the source’s retained `unified_measure.py` and `unified_linear_verify.py` (for the
orbit order its export writes and the input format) and its receipts. The checker
`unified_linear_verify.cpp` was not re-read. None of these programs is clean-room: the
export order and the digest rule were taken from the producer’s code. None imports or
copies any of it.

The source’s commit names Claude as co-author, and these programs were written by a
Claude agent, prompted separately from the source and from the intake lane.

## The Programs

| Program | What it does | Reads | Output |
| --- | --- | --- | --- |
| [`linear_exact.py`](programs/linear_exact.py) | The module the others import: a candidate read exactly with duplicate keys refused, the eight images in the source’s order, the invariance test under both generators of D4, the direction, Tokoharu’s centre half-width, the rotated core, clipping, the exact capture of points, segments and rectangles, the semantic digest, and rational square-root bounds | (a module) | — |
| [`check_linear_candidate.py`](programs/check_linear_candidate.py) | Every exact premise of the candidate (its SHA-256 against the pin, the schema, the orbit and image counts, containment and nondegeneracy, the exact mass against `total_mass` and $145 - 1/100000$, D4 invariance, the digest, the net’s containment facts, the least centre half-width) and the arithmetic of the scope: Green’s $G_{12}$ bounded from 100-digit integer square roots against the source’s rational upper bound and stated margin, Nagamochi’s and Karakuş’s closed forms, and the case records’ bounds at n = 145 to 150 | the asset’s `candidate.json`; the retained `completion-audit.json`; `packing/frontier/n-145.md` to `n-150.md` | `check_linear_candidate.json` |
| [`check_linear_records.py`](programs/check_linear_records.py) | The 201 records (one per angle, each replayed, distinct input digests, the node total), the certificate’s and the manifest’s net blocks against the facts recomputed here, every digest the three documents state against the files they name (the candidate, the certificate itself, the proof bundle, the retained checker), and the source’s comparison fields | the asset’s `candidate.json`, `certificate.json` and proof bundle; the retained `manifest.json` and `completion-audit.json`; the retained `unified_linear_verify.cpp` of the 2 October packet | `check_linear_records.json` |
| [`check_inputs_sample.py`](programs/check_inputs_sample.py) | At chosen angles, the proof bundle’s `input.txt` and `result.json`: the input’s digest against the record’s, the stored result, its manifest against the facts recomputed here, the six header enclosures with `gamma` exactly one, and every rectangle, point and segment line enclosing the D4 image recomputed here, with the widest enclosure in ulps; every per-angle `verify.cpp` against the retained checker | the unpacked proof bundle; the asset’s `certificate.json` | `check_inputs_sample.json` |
| [`point_checks.py`](programs/point_checks.py) | The exact capture at five centres of the domain at chosen angles: the container’s centre, the far corner, the two edge midpoints and the quadrant’s centre | the asset’s `candidate.json` | `point_checks.json` |

## How to Run Them

From this directory, with `$ASSET` the directory the asset unpacks to, `$BUNDLE` the
directory its proof bundle unpacks to, `$PY` the project interpreter and `$CHECKER` the
retained
`wand125-linear-certificates-2026-10-02/square-packing-bounds/certificates/mixed_n101_L1028/code/unified_linear_verify.cpp`:

```sh
$PY -I programs/check_linear_candidate.py $ASSET/candidate.json 3cd54c43…360 \
    ../square-packing/problems/square-lower-bounds/certificates/mixed_n145_L1224/completion-audit.json \
    ../../../frontier
$PY -I programs/check_linear_records.py $ASSET/candidate.json $ASSET/certificate.json \
    ../square-packing/problems/square-lower-bounds/certificates/mixed_n145_L1224/manifest.json \
    ../square-packing/problems/square-lower-bounds/certificates/mixed_n145_L1224/completion-audit.json \
    $ASSET/n145-L12.24-proof-bundle.tar.gz $CHECKER
$PY -I programs/check_inputs_sample.py $BUNDLE 3cd54c43…360 $ASSET/certificate.json $CHECKER \
    0 1 35 100 111 200
$PY -I programs/point_checks.py $ASSET/candidate.json 0 100 200
```

## What They Printed

- **`check_linear_candidate`.** 594 point, 1,541 segment and 9 rectangle orbits, all of
  positive mass, expanding to 4,752, 12,328 and 72 images; the mass
  $14499999/100000$, equal to `total_mass` and to $145 - 1/100000$; the weighted images
  invariant under the diagonal swap and under $x \mapsto L - x$; the digest
  `31788dc7…` by the source’s rule; $B(1 + D) = 399908091/400000000$, the endpoint check
  $89/40000$, the last tangent $83/200$; the centre half-width positive everywhere,
  least $5077628753/937780000 \approx 5.4145$ at angle 200; the nearest primitive
  0.0998 from a wall. $G_{12}$ lies in $[12.21386694778915\ldots, \ldots]$ to 100
  digits, the README’s and the case records’ forms of it agree, the source’s rational
  upper bound exceeds it by $4.05 \times 10^{-91}$, and the stated margin
  $0.026133052\ldots$ is exact and above $0.0261330$. At every n from 145 to 149 the side
  exceeds Nagamochi’s, Karakuş’s and Green’s values and every record bound in the lower
  lanes, and both record upper bounds exceed it; at 150 Nagamochi’s $1 + \sqrt{127}$ and
  Karakuş’s value exceed the side.
- **`check_linear_records`.** 201 records at indices 0 to 200 once, each
  `LINEAR_ANGLE_REPLAYED` with a distinct input digest, 124,435,707 nodes in all, most
  3,330,973 at angle 0 and fewest 168,149 at angle 35, under the manifest’s limit of
  12,000,000; every claim field and net block the candidate’s; the certificate’s SHA-256
  `e3c58aa2…`, the bundle’s `4dc4f673…` and the checker’s `0249726a…` as the completion
  audit states them, the checker byte-identical to the retained copy; the side less the
  source’s comparison value equal to its stated margin.
- **`check_inputs_sample`.** At angles 0, 1, 35, 100, 111 and 200: the input hashes to
  the record’s digest, the stored result is `ANGLE_VERIFIED` with an empty frontier, no
  witness and the record’s node count, its manifest states this certificate’s facts,
  `gamma` is exactly one, and all 17,152 image lines and the six header lines enclose
  the exact values with no enclosure wider than one ulp; all 201 per-angle `verify.cpp`
  copies are the retained checker (the bundle’s root copy, hashed in scratch, too).
- **`point_checks`.** Fifteen captures, all at least one; least 1.00206 at the
  container’s centre at angle 200.

## What Decides What

`linear_exact.capture` decides the capture at the fifteen centres it evaluated, which is
no evidence of the claim: the claim is over every centre, and a capture of at least
one at a centre decides nothing about the others. Everything else checks premises. No
program here replays an angle, and none is cited by an evidence entry yet; the review
proposes the registry entries. The computation totalled about five CPU seconds.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
