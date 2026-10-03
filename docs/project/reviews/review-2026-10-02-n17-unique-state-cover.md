---
title: n17 Unique-State Capacity-One Cover
date: 2026-10-02
status: planning-review
---
# n17 Unique-State Capacity-One Cover

**Session:** 168, BC-418, lane R1 (independent review).
**Baseline:** `0dabde12`, the commit of `ring-3-voronoi-8-tabbed-unique` and the
`unique_state` check in `packing/devtools/check_n17_capacity_one_cover.py` (module
sha256 `163c19c9…`). **Question:** does that design meet the frozen criterion of
[H-266](../../../packing/campaign/hypotheses/H-266-n17-minimal-capacity-one-cover.md),
which
[exp-246](../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-246-h266-n17-capacity-one-cover.md)
left unresolved on the tabbed design?
It changes no bound, verdict or frontier field; the verdict below is a recommendation to
the coordinator for a recorded run.
Every number comes from five scripts of my own that read only the receipt’s cell list
and the exp-238 certificate, and import nothing from the checker: `wall_lemma_check.py`,
`cells_check.py`, `coverage_check.py`, `d4_burnside.py` and `family_check.py`, with
their outputs. They are retained with a `.txt` suffix under
[exp-247’s `audit/`](../../../packing/campaign/series/series-000-smoke-and-calibration/results/exp-247-n17-unique-state-cover/audit/),
beside the recorded run of this design.

## Summary

- **The criterion is met.** 24 cells, each of proved capacity one; exact coverage of the
  centre box; exact D4 invariance; 346,104 states and 43,593 orbits; the endpoint family
  in one state over the declared slider box, and that state unique, with least seam
  margin $0.002112$ inside and $0.002112$ outside (square 13); controls refused; the
  wall lemma independently reviewed.
  No blocking defect.
- **Capacity is right and has more room than the receipt shows.** The exact maximum of
  the wall bound is $-0.0034802$ for S1 at $(93/100,\,257/375)$ and $-0.0115261$ for the
  $79/100$ corners, inside the checker’s rigorous intervals $[-0.012611,-0.000687]$ and
  $[-0.014000,-0.001719]$. Every interior cell has diameter at most $0.969569$.
- **Coverage holds by a different proof.** Inclusion–exclusion over the cells gives
  union area exactly $844561/62500$, the area of the centre box, and a closed cover with
  no missing area has no missing point.
- **Square 6’s declared box is a superset of what H256 defines,** and the checker proves
  the containment, so “declared rather than derived” is a presentation gap, not a proof
  gap. Over the H256-derived ranges alone the margin is $0.003081$.
- **Two notes, neither blocking:** the design comment says the new tab points meet S1’s
  top corners, but they sit $1/375$ inside them, and the diagonal cells cover the strip;
  and the recipe box $B_W$ is not held (square 13 crosses S1’s top at $z=1/16$), which
  is a mismatch with the local-theorem recipe rather than with H-266.

## 1. Capacity

**Wall and corner cells.** `wall_lemma_check.py` maximises
$G(c,s)=cd+sw-1-\tfrac c2(c+s-1)$ over the closed quarter circle two ways, neither of
which uses the checker’s $\tau$-quartic, Bernstein coefficients or Sturm count.
Method A is exact: $dG/d\theta=0$ with $s^2=1-c^2$ is
$s\,(d-c+\tfrac12)=\tfrac12-c^2+wc$; squaring gives a quartic in $c$ whose real roots
sympy isolates to width $10^{-30}$, $G$ is bounded over each isolating interval by
monotone rational interval arithmetic, roots with a negative unsquared right side are
discarded as spurious, and the endpoints contribute $d-1$ and $w-1$. Method B is a
$40{,}001$-point $\theta$ mesh in mpmath interval arithmetic with the Lipschitz bound
$|G'|\le d+w+3/2$.

| Cell | $(d,w)$ | Exact $\max G$ | at $\theta^\ast$ | Mesh upper bound | Checker interval |
| --- | --- | ---: | ---: | ---: | --- |
| S1, N1, W1, E1 | $(93/100,\,257/375)$ | $-0.0034802$ | $41.65^\circ$ | $-0.003419$ | $[-0.012611,-0.000687]$ |
| Corners | $(79/100,\,79/100)$ | $-0.0115261$ | $57.56^\circ$ | $-0.011466$ | $[-0.014000,-0.001719]$ |
| S0, S2 and images | $(911/1000,\,529/750)$ | $-0.0035253$ | $45.12^\circ$ | $-0.003464$ | $[-0.004663,-0.002578]$ |
| Control | $(4/5,\,4/5)$ | $+0.0022828$ | $57.36^\circ$ | refused | refused |
| Control | $(911/1000,\,3/4)$ | $+0.0290099$ | $48.26^\circ$ | refused | refused |

The checker’s intervals contain the exact maxima; its S1 upper bound is loose by a
factor of five because the Bernstein split stops early, which costs nothing.
The lemma’s hypotheses hold as the cells are listed: every ring cell is an axis-aligned
rectangle touching its wall, with $(d,w)$ measured from the centre-box edge equal to
$(79/100,79/100)$, $(93/100,257/375)$ or $(911/1000,529/750)$ (`cells_check.py`). The
$79/100$ corner is $0.0083$ below the one-wall limit $0.798347$ of the
[lemma review](review-2026-10-02-n17-depth-width-wall-lemma.md); Lemma 3 there would
give $0.29\sqrt2-\tfrac12=-0.0899$ with both walls, so the corners have ample room.

**Interior cells.** All eight listed polygons are strictly convex and inside the centre
box.
Exact squared diameters: $29377/31250$ ($0.969569$) for the four cut and tabbed axis
cells, attained between a tab point such as $(999/500,143/100)$ and the apex
$(1169/500,1169/500)$, and $2502024804841/3369608000000$ ($0.861700$) for the four cut
diagonal cells. All are strictly below one, so the inscribed-disc argument applies.
No cell’s capacity argument is wrong.

## 2. Coverage

`coverage_check.py` proves coverage by area rather than by a sweep.
The cells are closed and lie in the closed box $B$, so $B$ minus their union is
relatively open; if it has zero area it is empty.
The union area is computed by inclusion–exclusion over every subset of cells whose
common intersection has positive area, each intersection an exact rational
Sutherland–Hodgman clip and each area an exact shoelace sum; subsets with zero-area
intersection and their supersets contribute nothing.
The sum of the 24 cell areas is $13.605668$; twenty pairs overlap with positive area and
no triple does; the alternating sum is exactly $844561/62500=13.512976=(U-1)^2$. A
non-proof pass of $2\times10^5$ random rational points found none uncovered.

The overlaps are the four $0.121^2$ squares where two outer side cells meet near a
corner, the eight lens-shaped overlaps of $0.00422$ between an axis cell and a diagonal
cell, and eight slivers of $4.55\times10^{-5}$ where a diagonal cell reaches into a
middle side cell. The slivers are the strips the design comment overlooks: the axis
cell’s tab points $(999/500,143/100)$ and $(1339/500,143/100)$ are $1/375$ inside S1’s
top corners at $x=2993/1500$ and $4021/1500$, and the diagonal cells, not the tabs,
cover the two strips above those corners.
The cover is exact either way; only the comment is inaccurate.

## 3. D4 and Burnside

`d4_burnside.py` applies the eight symmetries about $(U/2,U/2)$ to each cell as a vertex
set and finds every image among the cells, so the cover is D4-invariant, and the induced
permutations close under composition.
Cycle types: identity $1^{24}$; quarter turns $4^6$; half turn $2^{12}$; the four
reflections $1^4\,2^{10}$. Fixed 17-subsets, counted as unions of whole cycles:
$346{,}104$, $0$, $0$, $0$ and $660$ four times; Burnside gives $348{,}744/8=43{,}593$.
A brute-force reduction of all $\binom{24}{17}=346{,}104$ subsets to their least image
also counts $43{,}593$ orbits.
Both are far below the threshold of $135{,}196$.

## 4. The Unique State

**Soundness of `unique_state`.** The check lower-bounds the distance from the family to
each other cell by the largest, over the cell’s edge lines, of the least outward signed
distance over the member rectangles.
Any supporting half-plane of a convex set bounds the distance to that set from below,
and the least value of a linear function over a rectangle is at a corner, so the bound
is sound; it can only under-report, when the nearest feature is a vertex.
The family set is the union of segments between slider endpoints, which lies in the
convex hull of the member rectangles; the cells are convex; so a hull inside one cell by
$\delta$ and at distance $\delta$ from every other is the same state at every point of
the slider box, including the interior of the ranges and the H256 triangle inside the
product box. The claim “one unique state over the box” is therefore the right statement,
and the check proves it.

**Independent numbers.** `family_check.py` evaluates the H256 centres with the exp-238
`_layout` in mpmath interval arithmetic at 60 digits over the root box, rounds outward,
embeds by $(U-S)/2$, and computes exact distances: the least inward edge distance of the
hull inside its cell, box-boundary edges excluded since they are walls and not seams,
and the exact Euclidean distance between the hull and every other cell (vertex–segment
minima both ways, zero if they meet).

| Square | Cell | Inside margin | Nearest other cell | Distance |
| --- | --- | ---: | --- | ---: |
| 13 | side-S1 | $0.002112$ | interior-S | $0.002112$ |
| 11 | interior-W | $0.050903$ | interior-SW | $0.045697$ |
| 9 | side-W2 | $0.023770$ | side-W1 | $0.023770$ |
| 16 | side-N2 | $0.107729$ | side-E2 | $0.019691$ |

Every square lies in exactly one cell, the seventeen cells are distinct, and the
checker’s floor-rounded $0.002111$, $0.050902$ and $0.045696$ are lower bounds of these.
Square 13’s two numbers coincide because S1’s top and interior-S’s bottom lie on the one
line $y=143/100$, where the edge-line bound is exact.
The margin is thin but real: it exceeds the whole container slack $U-S=0.00047$, so a
translation of the packing within the cap would still leave square 13 at least $0.0016$
from the seam, and it is ten times the recipe radius $1/5000$.

## 5. Scope: Square 6

H256 (`_layout`) defines square 6 as an axis-aligned square on the bottom wall with
centre $(\lambda_6,\tfrac12)$, and square 13 by $\lambda_{13}$ along $v$; its slider
domain is the triangle $a\le R$, $z\le H$, $z+sa\ge L_0$ in
$(a,z)=(\lambda_6,\lambda_{13})$, so $\lambda_6\in[R-T/s,\,R]$ and
$\lambda_{13}\in[H-T,\,H]$, jointly.
Squares 5 and 11 do not move in H256. The criterion’s “whole H256 endpoint family,
sliders included” therefore requires exactly those two ranges on that triangle, and
nothing about square 6’s height or rotation.

The checker’s declared box for square 6, $[R-\tfrac15,R]\times[\tfrac12,\tfrac34]$
before embedding, contains the H256 range because $T/s\le0.111240047<\tfrac15$, which
the receipt proves in `domain_containment` (“square 6: T/s <= 1/5”), and the other
ranges contain the H256 ranges likewise ($2T/3\le0.047476\le\tfrac1{20}$,
$T/3\le0.023738\le\tfrac1{40}$). A family in one state over a superset is in one state
over the H256 family.
The box is adequate; what Session 167 called “declared rather than derived” is that the
derivation lives in a containment check rather than in the box’s definition.
Run on the H256-derived ranges alone, with squares 5 and 11 fixed, the state is the same
and square 13’s margin rises to $0.003081$. The extra motions in the declared domain,
square 5 by $-ae_x$, square 11 by $-bv$ and square 6’s height for a turn, are the route
review’s physical slider domain, beyond H256, and only strengthen the result.

## 6. Verdict

**H-266’s frozen criterion is met** by `ring-3-voronoi-8-tabbed-unique`: $N=24\le25$,
$43{,}593\le135{,}196$ orbits, every item exact or by outward bounds, the family in one
unique state with margin $\ge10^{-3}$ over the H256 slider domain, the synthetic
controls refused, and the wall lemma independently reviewed.
The hypothesis’ outcome should move from unresolved to confirmed on a recorded run of
this design, as exp-246 run-002 or a new experiment.

**Blocking defects:** none.

**Notes for the record, in priority order:**

1. Record the run and update exp-246 and H-266; retain the five scripts above.
2. Correct the design comment: the tab points sit $1/375$ inside S1’s top corners and
   the diagonal cells cover the strips.
3. The recipe box $B_W=[0,\tfrac14]\times[0,\tfrac1{12}]\times[-\tfrac18,\tfrac1{16}]$
   is not held in one state (square 13 is unassignable), so the local-theorem lane must
   use a $z$ range inside $[-\tfrac1{20},\tfrac1{40}]$ or accept a second state.
4. State in the receipt that square 6’s box is a proved superset of the H256 range, so
   the next reader does not repeat this question.
5. The Bernstein depth could be raised so the reported S1 bound approaches the exact
   $-0.003480$; cosmetic.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
