# Stage 4 Review R1 of De Winter’s Integer Octagon Lower-Bound Certificates

**Verdict.** Partially verified.
The review re-derived the method under its stated implementation hypotheses and found no
gap in the checked portions.
It checked the exact premises for all 77 standalone certificates and independently
decided 155 of 18,989 bins.
No complete independent certificate sample has a retained receipt.
The evidence supports the scope below and leaves full independent verification open.

R1 covers the 34 standalone certificates of
[issue #1041](https://github.com/jlevy/squares/issues/1041) and the 43 of
[issue #1042](https://github.com/jlevy/squares/issues/1042) at
[JoostdeWinter/square-packing 21d944c4](https://github.com/JoostdeWinter/square-packing/tree/21d944c43098e2261ab7d713cd10f02a5eb13f3d/lower_bounds_2026_11_19).
It examines the casewise integer octagon and Gram bounds behind the Hosono-style
exclusion, and the original lane kept its checker independent of the producer programs.
The
[frozen findings](../../../packing/resources/web/de-winter-lower-r1-review-2026-11-20/frozen/review-2026-11-20-de-winter-lower-r1-octagon.frozen.md)
give the re-derived lemmas, hypotheses, controls and receipts in full.

## Retained Checks

| Check | Retained result |
| --- | --- |
| Synthetic self-test | 5,933 checks passed and the three deliberately broken variants were caught |
| Exact premises | All 77 certificates met the checked premises. Five rejected controls behaved as planned |
| Exact pose search | 462 checked poses yielded no capture below 1. The least was approximately 1.0005828505087886 |
| Independent bins | Two bins per certificate and one additional pricing bin give 155 distinct accepted bins |
| Pose-search control S1 | 69 of 77 returned a capture below 1. Eight outcomes differed from the expectation |
| Decider controls | 24 of 36 outcomes met the predeclared expectation. The retained controls have 16 exact refusals, nine undecided outcomes and 11 decided outcomes |
| Complete certificates | The nine-certificate sample has no committed receipt or checkpoint |

The
[programs and receipts](../../../packing/resources/web/de-winter-lower-r1-review-2026-11-20/README.md)
retain each calculation at its original freeze.
The accepted bins belong to an independent exact implementation.
An unexpectedly accepted mutated control requires checking the mutated condition.
Twelve decider-control outcomes differed from their predeclared expectation.
None of those outcomes demonstrates an unsound acceptance.

## Interruption and Post-Freeze Source Check

The first review agent froze the plan and checker on 20 November 2026 UTC. It stopped
around 20:40 UTC, and the host restarted at 20:53. The first whole-certificate sample
left no receipt.
A second agent resumed at 21:04 and froze the findings at 21:20:28 while
a later sample attempt was running.
The
[amendment record](../../../packing/resources/web/de-winter-lower-r1-review-2026-11-20/frozen/checker-amendments.txt)
retains these events and the orchestration changes.
The saved branch has no subsequent sample output.

A separate Codex agent continued the F-2 source audit.
It checked the frozen findings’ digest before opening the producer’s programs.
It performed no certificate computation and left the two freezes unchanged.

- At the source pin,
  [octagon.cpp](https://github.com/JoostdeWinter/square-packing/blob/21d944c43098e2261ab7d713cd10f02a5eb13f3d/lower_bounds_2026_11_19/proof/octagon.cpp#L111-L115)
  skips a rectangle with any nonpositive corner mass before adding any of its four
  affine contributions.
- [gram.cpp](https://github.com/JoostdeWinter/square-packing/blob/21d944c43098e2261ab7d713cd10f02a5eb13f3d/lower_bounds_2026_11_19/proof/gram.cpp#L100-L105)
  skips a rectangle’s matrix contribution when any of the triangle’s three corner masses
  is zero. The
  [cover decision](https://github.com/JoostdeWinter/square-packing/blob/21d944c43098e2261ab7d713cd10f02a5eb13f3d/lower_bounds_2026_11_19/proof/gram.cpp#L143-L154)
  requires both triangles in a covering pair to pass.

The necessary F-2 condition holds per interpolation cell, conditional on correct
corner-mass bounds and arithmetic.
Other implementation obligations remain open, including the domain, angular errors,
rounding, overflow, dual bounds, completeness, and authentication of executed binaries
and receipts.

## Remaining Sample

The frozen sample’s nine certificates have 1,800 bins.
Their order is `1042/n136`, `1041/n114`, `1042/n129`, `1042/n132`, `1042/n115`,
`1041/n115`, `1041/n107`, `1042/n135`, and `1041/n111`. The frozen plan calls for
threshold 1, true certificate masses, at most 1,000,000 nodes per bin, minimum width
1,024 lattice units and at most two ternary splits.

The
[resumed sample driver](../../../packing/resources/web/de-winter-lower-r1-review-2026-11-20/programs/rr1_sample_resumed.py)
can finalize an existing checkpoint as a partial receipt.
A normal invocation starts with an empty checkpoint.
The driver’s time check is between batches, so an external supervisor needs to enforce
the 1,800-second per-certificate cap.
The sample allowance is 24 cumulative CPU-hours within a 40 CPU-hour lane allowance.
The freeze estimates about six CPU-hours spent, including roughly five from the
interrupted run. Later expenditure remains unrecorded.
The remaining sample awaits surviving host evidence or a new controlled run with
external scratch.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
