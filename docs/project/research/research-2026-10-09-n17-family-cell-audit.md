# Restricted N17 Family Cell Audit

**Date:** 2026-10-09\
**Status:** Exact computational deduction for the stated family and slider box

Fix the poses of all unit squares except square 6 to the exact endpoint family, embedded
concentrically in the cover frame with $U=1169/250$. Relative to the endpoint centroid,
square 5 moves by $-a e_x$, square 11 by $-b v$, and square 13 by $+z v$, where

$$
a\in[0,3/25],\qquad b\in[0,3/40],\qquad z\in[-1/20,1/40].
$$

For any non-overlapping completion inside $[0,U]^2$, square 6’s centre must belong to
`side-S2` in the retained exp-247 unique 24-cell cover, at any orientation.
The [maintained audit](../../../packing/devtools/check_n17_family_cell_audit.py) checks
this deduction using the existing
[root verifier](../../../packing/devtools/check_n17_root_certificate.py),
[endpoint geometry](../../../packing/devtools/check_n17_endpoint_feasibility.py), and
[capacity-one cover](../../../packing/devtools/check_n17_capacity_one_cover.py).
These are shared geometry routines; the audit is not an independent implementation.

## Exact Arithmetic and Cell Coverage

The audit replays the exp-237 root certificate and checks that its proven enclosure,
rounded outward to the cover’s $10^{-40}$ lattice, equals the exp-238 endpoint
enclosure. It evaluates the endpoint centres over that interval and the full slider
ranges. The blocker centre intervals, rounded outward to multiples of $1/1000$, are:

| Square | Centre x interval | Centre y interval |
| --- | --- | --- |
| 3 | [0.500, 0.501] | [1.500, 1.501] |
| 9 | [0.704, 0.705] | [2.704, 2.705] |
| 10 | [1.436, 1.437] | [3.388, 3.389] |
| 11 | [1.556, 1.605] | [2.055, 2.114] |
| 12 | [2.288, 2.289] | [2.797, 2.798] |
| 13 | [2.294, 2.343] | [1.370, 1.428] |
| 14 | [3.027, 3.028] | [2.110, 2.111] |
| 16 | [3.245, 3.246] | [3.372, 3.373] |
| 17 | [4.175, 4.176] | [2.613, 2.614] |

Every decimal in the table denotes an exact rational.
For each closed polygon piece, the audit takes the maximum squared distance over its
vertices and all four corners of the blocker centre box:

| Closed cell piece | Blocker | Squared-distance upper bound |
| --- | --- | --- |
| interior-SW | 11 | 58298837/84640000 |
| interior-NW | 10 | 592493086513/673921600000 |
| interior-S | 13 | 11737/12500 |
| interior-SE | 14 | 1294731481/2116000000 |
| interior-NE, $y\le29/10$ | 12 | 409960561/423200000 |
| interior-NE, $y\ge29/10$ | 16 | 151533961/264500000 |
| side-W1, $y\ge21/10$ | 9 | 893101/1000000 |
| side-W1, $y\le21/10$, $x\le1$ | 3 | 61/100 |
| side-W1, $y\le21/10$, $x\ge1$ | 11 | 3420961/9000000 |
| side-E2, $x\le37/10$ | 16 | 3088577/4500000 |
| side-E2, $x\ge37/10$ | 17 | 164821/200000 |

The maximum is $409960561/423200000$, with strict squared-distance margin
$13239439/423200000$ below one.
For fixed centre, squared distance is convex in the candidate point, so its maximum on a
convex polygon is attained at a vertex.
For fixed vertex it is convex in the blocker centre, so the four centre-box corners
bound the whole rectangle.
Thus every point of each piece lies at distance strictly less than one from its blocking
square’s centre, for every permitted slider value.
Each unit square contains its open radius-$1/2$ incircle; this distance forces interior
overlap irrespective of square 6’s orientation.

The cuts form a complete closed cover: for any coordinate $w$ and threshold $q$,
$\{w\le q\}\cup\{w\ge q\}$ contains the entire parent polygon, including $w=q$. Apply
this identity once to interior-NE and side-E2, and twice to side-W1, cutting its lower
part at $x=1$. The other four cells are unsplit.
The eleven pieces therefore cover all seven alternative cells with every seam included.

## The Sixteen Occupied Cells

The audit verifies the following distinct assignments throughout the full slider box:

| Labels | Assigned cells, in label order |
| --- | --- |
| 1, 2, 3, 4, 5 | corner-SW, side-S0, side-W0, corner-NW, corner-SE |
| 7, 8, 9, 10, 11 | side-E0, corner-NE, side-W2, side-N0, interior-W |
| 12, 13, 14, 15, 16, 17 | interior-N, side-S1, interior-E, side-N1, side-N2, side-E1 |

Each centre depends affinely on its slider at a fixed root.
The interval rectangles at slider endpoints enclose those endpoints for every root in
the enclosure.
The audit checks all their corners against the assigned cell’s closed edge
inequalities; convexity then includes every intermediate slider value.
It does not narrow the slider domain to obtain these assignments.

The existing cover checker proves capacity one for every cell, using its diameter or
wall lemma, and verifies closed coverage of $[1/2,U-1/2]^2$ by an exact slab sweep.
The audit replays both checks.
A unit square inside $[0,U]^2$ has its centre in that centre box, at every orientation.
Capacity one excludes the sixteen occupied cells, and incircle overlap excludes the
seven alternatives. The remaining cell is `side-S2`.

## Reproduction and Limits

From `packing/`, with the project’s external scratch environment configured:

```bash
uv run --frozen --all-extras --group dev python -m devtools.check_n17_family_cell_audit
uv run --frozen --all-extras --group dev pytest -q tests/test_n17_family_cell_audit.py
```

The CLI prints a structured result with the exact slider scope, centre boxes, eleven
bounds, occupied assignments, margin, and root verification.
The tests replay the deduction, independently compare polygon vertical-section covers
including closed seams, check centre enclosure across slider values, and reject changed
domains, an invalid bound, a displaced core centre, and an altered cell.

The deduction applies only to the exactly fixed sixteen-square skeleton and the stated
box. It establishes no outer capture, perturbed-core result, wider-slider result, or
global state exclusion.
It does not cover $B_W'$ and does not admit an exclusion object to the global
certificate ledger.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
