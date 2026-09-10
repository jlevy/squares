---
title: X-022 — segment ownership constraints after the PR 127 review
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-022
  title: Segment Ownership Constraints After the PR 127 Review
  date: '2026-09-08'
  author: GPT-6 Astra mathematical review and synthesis; GPT-5.6 Sol instrument integration
  campaign: packing.squares
  brief: Preserve the local ownership theorems, exact counterexamples and fixed-pattern exclusion derived
    during review, state what they rule out, and select one pointwise full-support pricing test without
    changing the packing bracket.
  sources:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/bc-305-ownership-results.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/outer-middle-capacity-two-proof.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/remaining-eight-segment-capacity-four.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/shared-segment-support-bounds.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/new-outer-constraints-review.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/outer-pair-screen-contract-review.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/outer-pair-corner-counterexample.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/adjacent-corner-two-owner-counterexample.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/fixed-outer-pairs-bottom-corner-incompatibility.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/outer-pair-equal-angle-and-cell-exclusions.md
  proposes:
  - H-135
---
# X-022 — Segment Ownership Constraints

These local theorems and exact counterexamples were developed during the PR 127 handoff
review. They are analytic research results, not outcomes of a preregistered numerical
round. Agenda 031 retains and validates them on the continuation branch.
Their preparation is included in session 110’s usage; session 112 measures integration
and subsequent work from 2026-09-08T23:23:55Z, without charging that preparation twice.

The certified bracket remains unchanged, approximately 3.8100257236 to 3.8770835900;
[SYNOPSIS](../../../SYNOPSIS.md#the-problem) carries the exact source-backed bounds.
The working side is q = 96/25. No local result here decides whether eleven squares fit.

## What the local proofs establish

For the ten horizontal segment labels of H-134 at tolerance `δ = 3/500`:

- Each of the two outer middle-row segments has sharp owner capacity two.
  Every owner contains one of two rational piercing points in its interior, with a
  closed radius-`1/1000` disk about the selected point.
  Two axis-aligned touching squares attain the capacity.
- Each of the other eight segments has sharp owner capacity four.
  Every owner centre is within `1/√2 + 7/125 < 4/5` of the segment midpoint; five such
  centres would put two less than one unit apart.
  Four axis-aligned squares sharing the midpoint as a vertex attain the capacity.
- If `Q₋` and `Q₊` own the same outer segment and are ordered by the lower and upper
  piercing points, any separating unit normal `v` directed from `Q₋` to `Q₊` satisfies
  `v_y ≥ 1/280` and `56v_y ≥ 62|v_x| - 1`. The stronger signed-angle argument excludes
  any pair whose folded half-tangents both lie in `[1997/6000, √2 - 1]`, or both lie in
  its reflected band `[1 - √2, -1997/6000]`, with exact contradiction margin
  `501/1000000`. The reviewed fixed-angle screen enumerates every separating-axis branch
  of the declared necessary relaxation for one supplied rational angle pair.
  A surviving branch remains unresolved geometry.

## What the exact counterexamples prevent us from claiming

Two four-square constructions close two tempting shortcuts:

1. Two owners of one outer segment coexist with distinct owners of the two adjacent
   selected corner marks.
   The corner marks lie strictly in their selected nearest-net `B = 9977/10000` cores.
   Thus outer-pair ownership plus those two distinct corner owners is compatible
   locally.
2. Four diamond squares give two distinct owners for each of two adjacent corner-pair
   mark sets, again with selected nearest-net core containment.
   Thus the corner-pair theorem alone does not reduce those four roles.

Neither four-square construction supplies an eleven-square configuration or checks the
other segment and corner roles.
The review does not decide whether either local pattern can be extended to eleven
squares.

There is one exact partial-pattern exclusion.
Fix the lower left and lower right outer owners as the axis-aligned squares used by the
capacity witness. Two additional squares cannot own the forced bottom-left and
bottom-right marks: both would contain the same point `(48/25, 2336/3175)` in their
interiors. The alternate marks already lie inside the fixed outer squares.
This excludes the specified fixed cross-container pattern, including selected-core
ownership and boundary touching.
It does not extend to arbitrary placements of the outer owners.

## Perturbation Strengthening in Session 112

The
[robust outer-corner proof](../series/series-000-smoke-and-calibration/results/agenda-031/proofs/robust-outer-corner-incompatibility.md)
extends the fixed-pattern exclusion to outer squares containing the specified
`1/1000`-inset rectangles.
Euclidean Hausdorff distance at most `1/1000` from each fixed axis square is a
sufficient condition.
Any additional owner of a forced bottom mark contains the same closed radius-`1/100`
disk in its interior, so the two additional opposite-bottom owners cannot coexist.

This argument was developed after the usage cutoff and belongs to session 112. Its exact
arithmetic and polynomial identities have a retained guarded replay; the geometric proof
uses separating axes and the support-function characterization of convex containment.
The additional-owner assumptions remain essential, and the result does not exclude the
outer squares themselves or change the packing bracket.

## Continuation

The next bounded mechanism test prices the retained BC-232 cutting-state LP once and
compares the first 32 positive rationalised dual rows with the full positive support at
the same full-arm witness.
It asks whether a full-support arrangement exposes a new state-site orbit with exact
depth at most one under the 32-row arm and greater than one under the full arm.
That pointwise test is H-135. It is not a reconstruction of a lost historical dual, a
global certificate, or a claim that the 32-row arm has no other new site.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
