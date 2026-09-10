# BC-305 Ownership Results

BC-305 retains and validates analytic ownership results developed and reviewed during
the PR 127 handoff preparation.
They are not prospective numerical discoveries on the continuation branch.
At `q = 96/25` and ownership tolerance `delta = 3/500`, they establish the following
local facts.

## Retained results

- Each outer middle-row segment has sharp owner capacity two.
  Every owner contains one of two rational piercing points in its interior, together
  with a closed radius-`1/1000` disk about that point.
  Two axis-aligned owners attain the bound.
  See [the capacity-two proof](proofs/outer-middle-capacity-two-proof.md) and its
  [independent review](proofs/new-outer-constraints-review.md).
- Each of the other eight segments has sharp owner capacity four.
  Its owners’ centers lie within `1/sqrt(2) + 7/125 < 4/5` of the segment midpoint, so
  five centers would force two squares’ interiors to overlap.
  Four axis-aligned squares sharing the midpoint as a vertex attain the bound.
  See [the capacity-four proof](proofs/remaining-eight-segment-capacity-four.md).
- For two owners of one outer segment, ordered by the lower and upper piercing points,
  every weak unit separating normal directed between them obeys `v_y >= 1/280` and
  `56v_y >= 62|v_x| - 1`. The general shared-support slab also bounds the excess
  projected center gap by `ell|v_x| + 2delta`, and that upper gap is sharp.
  See [the support proof](proofs/shared-segment-support-bounds.md) and the
  [outer-constraint review](proofs/new-outer-constraints-review.md).
- The coarse orientation corollary excludes a pair when both owners have absolute folded
  half-tangent at least `49/125`, including equality.
  The stronger signed result excludes any pair whose half-tangents both lie in
  `[1997/6000, sqrt(2)-1]`, or both lie in the reflected band `[1-sqrt(2), -1997/6000]`;
  its exact contradiction margin is `501/1000000`. See
  [the broad-band proof](proofs/outer-pair-equal-angle-and-cell-exclusions.md).
- The guarded fixed-angle reader enumerates every separating-axis branch of the declared
  necessary relaxation for one supplied rational angle pair.
  Rejection of every branch excludes that pair.
  A surviving branch proves only feasibility of its relaxation.
  It is not an existence certificate.
  See [the screen contract](proofs/outer-pair-screen-contract-review.md).

## Exact limits on ownership shortcuts

Two exact four-square counterexamples keep the local counts from being overread.

1. Two owners of the left outer segment coexist with distinct bottom-left and top-left
   corner owners, with the selected marks strictly inside their canonical nearest-net
   `B = 9977/10000` cores.
   See [the outer-pair counterexample](proofs/outer-pair-corner-counterexample.md).
2. Two adjacent corner-pair mark sets can each have two distinct diamond-square owners,
   again with the selected marks strictly inside their canonical nearest-net cores.
   See
   [the adjacent-corner counterexample](adjacent-corner-two-owner-counterexample.md).

One fixed cross-container pattern is nevertheless impossible.
Fix the lower left and lower right outer owners to the axis-aligned squares used in the
capacity witness. Any two additional squares containing the forced bottom-left and
bottom-right marks would both contain `(48/25,2336/3175)` in their interiors.
The alternate bottom marks already lie inside the fixed outer squares, including their
selected cores, so the mark choice is forced for additional owners.
This excludes the specified fixed pattern, with boundary touching allowed; it does not
exclude arbitrary placements of the outer owners.
See
[the fixed-pattern proof](proofs/fixed-outer-pairs-bottom-corner-incompatibility.md).

## Independent reader receipts

The integrated control suite passed all 60 tests in 13.52 seconds under project Python
3.14.7; its [raw output](bc-305-focused-tests.txt) is retained.
The two exact CLI readers were then replayed from the continuation checkout:

- [Adjacent-corner fixture](corner_ownership_audit-reference.json): verified, with
  [overlap](corner-overlap-control.json),
  [containment](corner-containment-control.json), and
  [core-ownership](corner-core-ownership-control.json) mutations rejected by their
  intended checks.
- [Outer-pair corner fixture](outer_pair_corner_audit-reference.json): verified, with
  [overlap](outer-corner-overlap-control.json),
  [broken-mark](outer-corner-broken-mark-control.json), and
  [changed-target](outer-corner-changed-target-control.json) controls passing.
- Fixed-angle screen: the known [axis](pair-screen-axis-control.json) and
  [quarter-half-tangent](pair-screen-quarters-control.json) controls remain unresolved;
  the known [third-half-tangent](pair-screen-thirds-control.json) case is excluded.
  These replays validate known examples, not a new search over angle pairs.

## Perturbation Supplement

The [robust extension](proofs/robust-outer-corner-incompatibility.md) covers outer
squares containing the fixed owners’ `1/1000`-inset rectangles; Euclidean Hausdorff
distance at most `1/1000` is sufficient.
Every additional owner of a forced bottom mark then contains the closed radius-`1/100`
disk about the common point in its interior.
Two additional opposite-bottom owners therefore overlap.

This is a new analytic continuation result from session 112, with 23 rational
inequalities and two polynomial identities replayed in the
[arithmetic receipt](robust-outer-corner-arithmetic.json).
The reader checks the arithmetic and algebra; the geometric proof is written separately.
The expanded instrument suite passed
[64 tests in 2.46 seconds](continuation-instrument-tests.txt).

## Scope

These capacity, support, angle, counterexample, and fixed-pattern results do not compose
into a global exclusion at `q = 96/25`. Capacity is a local ownership count, and a
surviving fixed-angle screen branch is an unresolved relaxation branch.
The certified packing bracket remains unchanged; its canonical values and provenance
remain in [SYNOPSIS](../../../../../../SYNOPSIS.md).
As approximate orientation only, its endpoints are about `3.81003` and `3.87708`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
