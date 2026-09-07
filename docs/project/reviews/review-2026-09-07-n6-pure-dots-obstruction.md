# Five-Dot Obstruction for the Six-Square Problem

**Date:** 2026-09-07. **Status:** mathematical derivation independently reviewed; not a
registered campaign theorem.
**Scope:** five unweighted points required to hit every individual square.
The argument does not exclude weighted measures, multiple points charged to each square,
or geometric restrictions involving several packed squares.
Coordinator bead: `think-7u4s`.

## Source Search and the Boundary Convention

[Stromquist’s Memo I](../../../packing/resources/papers/stromquist-1984-packing-unit-squares-inside-squares-i-six-unit-squares.md)
gives a proof of `s(6) = 3` using a geometric restriction on adjacent isolated points
before its final point cover.
It does not state a theorem that every pure dots proof fails.
The three archived memoranda were read in full, including all 47 scanned pages.
Searches on 2026-09-07 for Stromquist with “dots,” “square packing” with “five points,”
and “unit squares” with “unavoidable” and “five” found no primary proof of the
five-point obstruction.
This is a bounded negative source search.

[Bašić–Slivková, *On optimal piercing of a square*](../../../packing/resources/papers/basic-slivkova-2018-optimal-piercing-square.pdf),
Theorem 1, proves `pi(U_3) = 9` for **open unit squares at container side exactly 3**.
The nine disjoint open cells of the ordinary `3 × 3` tiling already require nine points.
That fact alone says nothing about open squares of side strictly greater than 1 in the
same container. Stromquist uses this latter convention to prove a lower bound on the
unit-square packing side.

## A Five-Point Obstruction Without Symmetry

The following derivation supplies a precise version of the unweighted obstruction.
Its only packing objects are individual square placements; they need not coexist.

**Proposition.** For every set P of at most five points in `S = [0,3]^2`, some closed
square of side strictly greater than 1 lies in S and is disjoint from P.

Add points if necessary so that there are five.
If a closed axis-aligned unit square Q in S misses P, the positive distance from the
finite set P to Q allows Q to be enlarged slightly inside S while still missing P. At a
container wall, enlarge away from that wall.
Therefore it suffices to treat the case in which P hits every closed axis-aligned unit
square in S.

The four closed corner unit squares are pairwise disjoint.
Choose one point in each:

```text
A in [0,1] × [0,1]       B in [2,3] × [0,1]
D in [0,1] × [2,3]       C in [2,3] × [2,3].
```

Call the remaining point R. Along a boundary strip, the possible unit squares are
parameterized by the intervals `[t,t+1]`, `0 ≤ t ≤ 2`. We use one elementary fact: if
all eligible projected sites lie in `[0,1]` or `[2,3]`, hitting every such closed
interval forces the rightmost site of the first group to be 1 and the leftmost site of
the second group to be 2. Otherwise the gap between the two groups is greater than 1 and
contains a closed interval of length 1. In particular, if there is exactly one eligible
site in each group, their projected coordinates are exactly 1 and 2.

There are three cases up to a symmetry of S. These cases include the cell boundaries:
the corner cells are closed; an edge-middle cell has its coordinate along the edge
strictly between 1 and 2; the central cell is `(1,2)^2`.

1. **R is in the central cell.** Each boundary strip has just its two corner sites.
   Applying the interval fact on all four sides forces `A=(1,1)`, `B=(2,1)`, `C=(2,2)`,
   and `D=(1,2)`.
2. **R is in an edge-middle cell**, say `(1,2) × [0,1]`. The left and right strips force
   `A.y=B.y=1` and `D.y=C.y=2`. The top strip forces `D.x=1` and `C.x=2`. Thus D and C
   are the two inner top corners, and all other sites have `y ≤ 1`.
3. **R is in a corner cell**, say `[0,1]^2`. The right strip forces `B.y=1` and `C.y=2`;
   the top strip forces `D.x=1` and `C.x=2`. In the bottom strip the left projected
   group consists of A and R, while the right group contains B, so the interval fact
   forces `B.x=2`. In the left strip the lower projected group consists of A and R,
   while the upper group contains D, so it forces `D.y=2`. Again D and C are the two
   inner top corners, and all other sites have `y ≤ 1`.

Now consider the open top diamond with vertices

```text
(3/2,3), (3/4,9/4), (3/2,3/2), (9/4,9/4).
```

It is a square of side squared `9/8 > 1`. Its interior has `y > 3/2`, while `D=(1,2)`
and `C=(2,2)` lie on its boundary.
It therefore misses P in cases 2 and 3. In case 1, use this diamond and its three
quarter-turn rotations.
Their interiors lie in the four disjoint sectors formed by the diagonals of S. The four
corner sites lie on those diagonals, and R can belong to at most one sector.
At least three diamonds therefore miss P.

In each case, shrink an avoiding diamond concentrically by a factor `19/20`. Its closed
version lies strictly inside the original open diamond, misses P, and has side squared

```text
(9/8)(19/20)² = 3249/3200 > 1.
```

This proves the proposition.
The axis-aligned branch’s enlargement is chosen from the positive clearance to the
supplied P; it has no asserted uniform numerical size.

## What This Says About a Pure Dots Proof

The proposition excludes one fixed set of five points that would hit every enlarged open
square in S. Compactness also excludes a sequence of five-point covers working for
enlargement factors tending down to 1.

To see this, suppose such covers `P_k` existed for sides `1+epsilon_k`, with
`epsilon_k → 0+`. Order each set arbitrarily, repeat points if needed, and pass to a
convergent subsequence in the compact space `S^5`. Let its limit be P. The proposition
gives a closed square Q of side `1+delta > 1`, disjoint from P. Its distance from P is
positive, so Q misses every `P_k` sufficiently far along the subsequence.
For large k, `epsilon_k < delta`; a concentric open square of side `1+epsilon_k` inside
Q contradicts the claimed cover.

Thus some positive enlargement interval admits no five-point cover, although this
argument by itself gives no explicit endpoint.
Rescaling converts this to a neighborhood of container sides below 3 in which five
unweighted dots cannot prove impossibility by requiring one dot in each individual unit
square. The argument establishes no analogous obstruction for fractional weights or
conditional covers.

The subsequent
[quantitative derivation](review-2026-09-07-n6-quantitative-piercing-bound.md) makes the
neighborhood explicit.
Every set of at most five sites in S misses a closed square of side at least `101/100`.
Its rational construction tests axis-aligned squares of that side, then four diamonds of
L1 radius `143/200` with side squared `20449/20000`, exceeding `(101/100)^2` by
`47/20000`. The linked review supplies the modified corner-coordinate bounds and the
stronger algebraic endpoint.

## A Shorter Symmetric Control

The fully dihedral case has a direct witness independent of the site coordinates.
The dihedral group D4 of the container has orbit sizes 1, 4, and 8. Its only fixed point
is the center. A noncentral point is fixed by at most one reflection, since two distinct
symmetry axes intersect only at the center.
A set invariant under D4 with at most five points therefore consists of the center and
at most one orbit of size 4. That orbit lies either on the two container diagonals or on
the two midlines.

- For the diagonal family, the open square with vertices `(3/2,0)`, `(9/4,3/4)`,
  `(3/2,3/2)`, `(3/4,3/4)` has side squared `9/8`. Its interior satisfies `x-y > 0` and
  `x+y < 3`, so it avoids both diagonals.
- For the midline family, the open square `(0,3/2)^2` has side squared `9/4`. Its
  interior avoids the lines `x=3/2` and `y=3/2`.

Both interiors are contained in the interior of S. Contact with the container boundary
and with a dot at a witness vertex is allowed because the witnesses are open.
The coordinate checks belong in the reusable exact control.
The independent review also checks the orbit classification and the arbitrary-site case
split.

## Exact Reusable Control

[`five_point_obstruction.py`](../../../packing/cases/stromquist/five_point_obstruction.py)
constructs a closed escaping square for a supplied set of at most five rational sites.
It partitions the translation domain of axis-aligned side-`101/100` squares at all
coordinate events, testing both the event faces and each open interval between them.
Site membership is constant on every resulting product stratum, so an unsuccessful axis
search establishes that every closed axis-aligned square of that side is hit for that
input. The constructor then tries the four fixed diamonds of L1 radius `143/200`.

Every returned witness is checked using exact `Fraction` arithmetic: equal side lengths,
orthogonal adjacent edges, counterclockwise orientation, containment, side squared at
least `(101/100)^2`, and a strictly separating edge for every supplied site.
The public entry points reject malformed points and non-`Fraction` coordinates; the
command line parses fractions and decimal strings exactly.

Run from `packing/` using the project interpreter:

```bash
.venv/bin/python3 -m cases.stromquist.five_point_obstruction
.venv/bin/python3 -m cases.stromquist.five_point_obstruction --point 1,1 --point 1,2 --point 2,1 --point 2,2 --point 3/2,3/2
.venv/bin/python3 -m cases.stromquist.five_point_obstruction --svg cases/stromquist/five-point-obstruction.svg
```

The default output replays the retained
[`five-point-obstruction.json`](../../../packing/cases/stromquist/five-point-obstruction.json)
controls; `--output PATH` retains the same JSON. The
[tests](../../../packing/tests/test_stromquist_five_point_obstruction.py) check
witnesses with an independent projection predicate, include all five-point subsets of a
nine-site grid, exercise wall and closed-boundary cases, and reject corrupted squares
and inputs outside the proposition.
The finite tests verify the implementation; the real-coordinate case split and
compactness argument above establish the continuum claim.
The [independent review](review-2026-09-07-stromquist-incorporation.md) records the
proof audit.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
