---
title: n17 Whole-Square Envelope Transfer from n11
date: 2026-10-07
status: proposed
---
# n17 Whole-Square Envelope Transfer from n11

A closed occupancy assignment is impossible if eleven of its whole unit squares are
forced into a square of side $31/8$. The accepted n11 lower bound rules this out, with
arbitrary independent square orientations and boundary contact allowed.
The proposed test proves whole-square containment using conservative envelopes of the
original capacity-one cells.
It evaluates at most 576 candidate windows per assignment.

This makes the existing X048 route R9 executable; it is not a new n11 theorem or a claim
that the proposed windows succeed.
The transfer and exhaustive-window argument below are sole-Astra hand derivations, not
independently mathematically reviewed or formalized.
The original contract preceded every selected-state envelope or window evaluation.
The actual H312/exp304 result and separately selected H314/exp306 representation test
are recorded below; no target for the latter has been evaluated.

## Accepted Theorem and Exact Constants

Freeze

$$
U=\frac{1169}{250},\qquad
r=\frac{707107}{1000000},\qquad
H=\frac{31}{8},\qquad
B_{11}=\frac{3875000000}{999999999}.
$$

The finite scalar requirements are

$$
2r^2\ge1,\qquad
B_{11}-H=\frac{31}{7999999992}>0.
$$

[T-061](../../../packing/frontier/RESULTS.md) establishes $s(11)>B_{11}$. Its
unrestricted scope and replay record are retained in the
[n11 case](../../../packing/frontier/n-011.md) and
[Wang–Li review](../reviews/review-2026-09-30-issue-247-wang-li-n11.md).
T-060 supersedes that bound but does not invalidate it.
The weaker rational window size $H$ avoids a new algebraic-root comparison or replay of
the n11 optimality proof.

The consumer inherits T-061 as an accepted theorem.
It checks the exact registered claim, n11 scope, V3/C3 status and named source/native
evidence, together with the retained small full-replay receipt.
These joins do not themselves re-prove the n11 theorem.
The new finite arithmetic concerns the n17 envelopes and window containments.

## Whole-Square Envelopes

Every point of a unit square is at Euclidean distance at most $\sqrt2/2\le r$ from its
centre, regardless of orientation.
Consequently each coordinate differs from that of the centre by at most $r$.

Let the exact axis-aligned bounding box of original cell $i$ be

$$
C_i=[a_i,b_i]\times[c_i,d_i].
$$

If a physical unit square has its centre in that cell and is contained in $[0,U]^2$, the
entire closed square is contained in

$$
R_i=
[\max(0,a_i-r),\min(U,b_i+r)]
\times
[\max(0,c_i-r),\min(U,d_i+r)].
$$

Both ingredients are necessary: the radius bound supplies the expanded rectangle, and
physical containment supplies its intersection with the original container.
A centre inside a proposed window is insufficient.
The consumer must contain every point of $R_i$ in the window.
Equality on a window boundary is allowed.

The original cells are exact closed convex polygons in the original $U$ frame.
Their coordinate extrema occur at vertices.
Reconstruct them through `check_n17_capacity_one_cover.build_cover` and its exact D4
permutations; do not use the selector’s floating-point polygon adapter.
The accepted closed capacity-one cover makes the assignment to occupied cells injective,
so eleven distinct occupied cells designate eleven distinct squares.

## Complete Enumeration of This Envelope Criterion

Write $\ell_i$ and $b_i'$ for the left and bottom endpoints of $R_i$. For every ordered
pair of cell indices $(a,b)$ among the 24 original cells, construct

$$
W_{ab}=[\ell_a,\ell_a+H]\times[b_b',b_b'+H].
$$

Keep all $24^2=576$ anchor pairs, including aliases with the same geometric window.
Do not clamp the start to $U-H$. A window may extend beyond the original container: it
is still a square of side $H$, and the complete unit squares placed within it still
contradict the n11 theorem.

Suppose eleven envelope rectangles fit in any axis-aligned square
$[x,x+H]\times[y,y+H]$. Let $\ell$ be the least left endpoint among those rectangles,
and $b'$ the least bottom endpoint.
Then $\ell\ge x$, while their greatest right endpoint is at most $x+H\le\ell+H$. Thus
every rectangle fits horizontally in $[\ell,\ell+H]$; the same reasoning applies
vertically. Some selected rectangle supplies $\ell$ and some supplies $b'$, so the
enumeration contains that window.

Therefore the 576 anchors exhaust the existence of an axis-aligned $H$-square containing
eleven of these conservative envelopes.
A complete miss is not a proof that no eleven actual squares could be confined to a
smaller region by stronger, pose-dependent reasoning.
It does not test rotated windows or sharper orientation-dependent envelopes.

## What a Positive Certificate Proves

For a selected 17-cell assignment, intersect its occupied-cell mask with each window’s
full-envelope containment mask.
If the count is at least eleven, retain the first lexicographic anchor pair and first
eleven occupied contained cells in the frozen cell order.
The fresh checker independently verifies their distinctness, occupancy and all four
closed containment inequalities for every envelope.

Any physical packing in that assignment would then contain eleven independently rotated
unit squares with disjoint interiors, all contained in a square of side $H<B_{11}$. That
contradicts T-061. This is an ordinary physical assignment obstruction and does not
depend on fixed-orientation normalization, a rank condition, an endpoint guard or a
chosen SAT branch.

In fact, the eleven named cells alone form a forbidden subpattern at $U$. The same
certificate excludes every larger assignment containing that subpattern, and D4
transports both the cell assignment and its window.
Any broader survivor-count effect must be measured separately.
Ordinary ledger admission requires its own reviewed consumer; a finite positive receipt
must not silently change the standing census.

## First Selected Roster and Controls

Use the same complete selected stratum as the proposed normalized-rank discriminator:
all 95 distance-two D4 orbits in the accepted current partition.
Freeze the exact named representatives and D4 identities before constructing target
windows. Check the full 4,683-entry partition’s named masks, orbit sizes and distances
before selecting the 95; the ordinary residue remains 36,768 assignments after sixty
admissions.

Unlike the normalized-rank filter, this method cannot exclude a state containing the
known feasible endpoint packing.
Any actual endpoint-state positive would be a calibration failure requiring
investigation. The selected 95 states differ by one cell replacement from a D4 image of
the endpoint state. A window with ten contained endpoint envelopes could cross the
eleven-envelope threshold after such a replacement.
That is a possible mechanism for this roster choice, not an observed count or success
prediction.

The primary criterion is at least one fresh verified assignment obstruction with all 95
states and all 576 windows per state accounted.
Report every complete negative as a miss of this envelope criterion.
Resource incompleteness supplies neither a complete-stratum negative nor a reason to
alter the window size or radius after seeing counts.

Synthetic controls must cover:

- a centre-only false positive rejected by full-envelope containment;
- closed boundary containment, degenerate rectangles and aliases;
- anchor completeness, including a valid window extending outside $U$;
- eleven distinct occupied cells, with duplicate and nonoccupied selections refused;
- a complete positive and complete negative window roster with fresh reconstruction;
- exact radius and n11-bound arithmetic, theorem-entry and generated-receipt tampering;
- named cells, D4 actions, full partition distances and changed input identities.

## Input Custody and Resource Contract

The four named roles are the accepted partition, accepted cover, T-061 registry source
and small n11 full-replay receipt.
Generated receipts retain their byte identities.
The curated `packing/frontier/results.yaml` source is identified through Git provenance
and its inspected exact T-061 tuple, not a new source-file checksum lock.
A declared source revision identifies the theorem text being read; it is not a
requirement that current code or a mathematical verdict equal a particular Git commit.

The small replay is
`packing/resources/web/wang-li-n11-2026-09-29/receipts/authors/fresh-full-replay/RESULT.json`.
Its accepted status is `PASS_FRESH_TWO_IMPLEMENTATION_FULL_REPLAY`, with 12,028 rows,
histogram `{1000047559: 12028}`, surplus 428,125 and the stated improved-certificate
identity. The much larger native replay need not be decompressed or rerun: its accepted
theorem role remains explicit in T-061’s evidence.

Proposed ceilings are 60 seconds construction plus 60 seconds fresh checking, one
worker, sampled 4 GiB current RSS per live process and owned-group cleanup.
These are allocations, not runtime predictions.
Geometry uses exact rationals with a 4,096-bit ceiling; descriptor/input receipts are at
most 10 MiB and output at most 64 MiB. The finite work is fixed: 24 envelopes, 576
window masks and 54,720 state-window counts.
Neither a numerical solver nor a new n11 proof replay is part of this consumer.

The result distinguishes `t061_proof_inherited` from `t061_proof_replayed`, and actual
ordinary assignment obstructions from ledger admission, global optimality and a new n17
side bound. A complete miss stops this fixed envelope rule.
It does not justify an unbounded search over subcontainers or reinterpret the
lower-dimensional theorem as an n17 conclusion without the whole-square containment
proved here.

## Actual First Result

Exp304 completed all 54,720 state-window counts with matching fresh reconstruction and
no eleven-envelope witness.
The largest count is six in 47 selected orbits and seven in the other 48. The supervised
pair completed normally in 2.044 seconds.
These are complete misses of the fixed envelope rule, not feasible packings or ordinary
exclusions. Its endpoint mask was used to validate the distance-two roster; the first
consumer did not evaluate a separate endpoint window control.

The retained evidence is in
`packing/campaign/series/series-000-smoke-and-calibration/results/exp-304-n11-envelope-windows/`.
The gap to eleven motivates one final representation test, rather than an unrestricted
window search.

## Selected Two-Sided Representation Test

H314/exp306 is reserved for a separately registered, disjoint consumer.
Keep the same $U,r,H$, theorem and complete 95-orbit roster.
For a cell AABB $[a,b]\times[c,d]$, first verify that both coordinate intervals lie in
$[1/2,U-1/2]$. Define

$$
M_x=\min(U/2,b,U-a),\qquad M_y=\min(U/2,d,U-c),
\qquad R_x=\min(r,M_y),\quad R_y=\min(r,M_x).
$$

A rotated unit square has the same half-extent in the x and y directions,
$h=(|\cos\theta|+|\sin\theta|)/2$. If its centre is $(x,y)$ and the square lies in
$[0,U]^2$, then

$$
h\le\min(r,x,U-x,y,U-y).
$$

Consequently every square point lies in the following *upper envelope*:

$$
U_i^x=[\max(0,2a-U,a-R_x),\ \min(U,2b,b+R_x)],
$$

$$
U_i^y=[\max(0,2c-U,c-R_y),\ \min(U,2d,d+R_y)].
$$

For example, $x+h$ is bounded above by $U$, $2b$, $b+r$ and $b+M_y$; the other three
coordinate bounds follow by the same inequalities.
This proof uses the shared coordinate half-extent and all four wall constraints.
The upper envelope is contained in the first test’s expanded-and-clipped envelope.

There is also a useful *lower envelope*:

$$
L_i=[a-1/2,b+1/2]\times[c-1/2,d+1/2].
$$

Every centre in the original cell supports an axis-aligned unit square inside $[0,U]^2$.
The coordinate extrema $a,b,c,d$ are attained in that cell.
Any axis-aligned box that encloses every independently allowed single-square pose in the
entire cell must therefore contain $L_i$. This does not assert that those different
extremal poses occur in one seventeen-square packing.
Nor does $L_i$ enclose arbitrary rotated squares.

The finite checker must verify the sandwich

$$
L_i\subseteq U_i\subseteq R_i
$$

for every cell. Enumerate all 576 anchor windows separately for the upper and lower
envelopes, retaining aliases and the same catalogue-index tie convention.
The anchor completeness proof applies to either rectangle family.

An upper-envelope witness gives the ordinary eleven-square contradiction already proved
above. In contrast, if no window contains eleven occupied lower envelopes, then **no
independent whole-cell AABB-enclosure method can produce an eleven-square window
contradiction for that assignment at side $H$**: any admissible enclosing boxes would
contain the lower envelopes, so a successful window for them would also be a successful
lower-envelope window.

This is a representation limitation for the fixed original $U$, entire independent cell
domains, axis-aligned enclosing boxes and fixed window side $H$. It does not cover
smaller centered-container domains, coupled poses, subdivided cells, rotated windows or
other subcontainer bounds.
A lower-positive window only leaves the representation possible; it proves neither an
exclusion nor a physical packing.

The frozen primary criterion is an upper-envelope obstruction for at least one selected
state, or lower-envelope failure for all 95 states, establishing the stated limitation
on the whole selected roster.
Both complete 95-by-576 rosters are required in either case.
A mixed result with lower-positive states but no upper obstruction is a primary miss;
retain any individual lower-negative certificates as secondary limitations.
The maximum lower count must be at least the maximum upper count in every state.
Contradictory summaries are refused.

The new consumer also evaluates all 576 upper windows on the accepted endpoint
representative and requires a maximum count at most ten.
An endpoint positive is a calibration refusal.
Lower endpoint counts may reach eleven and are diagnostic only.

Use three top-level roles: the accepted exp304 descriptor, construction receipt and
fresh receipt. Check their complete mathematical-payload agreement and inherit the old
finite proof. Reuse the old bounded intake once for the exact cells, complete roster and
theorem joins; do not recompute the old windows.
The generated-artifact custody and curated Git-source conventions remain unchanged.
A fresh process reconstructs both new rectangle families, both complete window rosters,
the endpoint control and all new claims.

Keep 60 seconds per phase, 120 seconds combined, one worker and sampled 4 GiB current
RSS per live process.
Retain the existing 4,096-bit, 10 MiB input and 64 MiB output limits.
The declared new work is 24 upper/lower rectangle pairs, two 576-window rosters, 109,440
selected-state counts and 576 endpoint upper-window counts.
No new n11 proof, rank search, ordinary census admission or global side-bound claim is
part of this test. A complete architecture kill ends this independent-envelope route on
the selected roster; do not respond with an unchanged grid or contact atlas.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
