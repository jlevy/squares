# Review: Evan Daniel’s s(182) ≤ 13.970916436215 (Issue 806)

- **Date:** 25 October 2026
- **Reviewer:** Claude, strongest tier, maximum reasoning (the stage 4 mathematical
  review lane `c-review-806-math`, for the intake coordinator `coord-intake-1024`; bead
  `think-meci`)
- **Subject:** \#806’s certificate, `search/packer/candidates/s182-1024.cert` at
  [evand/square-packing@d99925d](https://github.com/evand/square-packing/tree/d99925d1298262c4ddb81c95abbb6f45adca8d3d/search/packer/candidates),
  reported on [jlevy/squares#806](https://github.com/jlevy/squares/issues/806). The
  records lane registers it under the next free T-number and retains it in the packet
  `packing/resources/web/evand-n182-2026-10-25/`.
- **Read at:** `main` `bb756e193`
- **Verdict:** accepted, for finite feasibility.
  The bound holds at the exact side stated, and no finding is blocking or major.
  Two findings are minor (M-1 on the credit of the start, M-2 on the commit title), and
  eight are notes.
- **Code:**
  [review/review-2026-10-25/](../../../packing/resources/web/evand-n182-2026-10-25/review/review-2026-10-25/README.md)

## Summary for the Author

Your certificate is valid.
This review decided it again with a clean-room exact checker written for it.
That checker shares no code with your checkers or with this repository’s exact routes.
Every square lies in the box and no two overlap, decided in exact rational arithmetic
over all 182 walls and 16,471 pairs by two methods: separating axes, and exact clipped
areas.
The side is the certificate’s own header side, and the 12-place print rounds it up
correctly.

| Certificate | Exact side | Print, rounded up | Least wall clearance | Least pair gap |
| --- | --- | --- | --- | --- |
| Daniel, 182, `d99925d` | 13970916436214678735385725854133 / 10^30 = 13.970916436214678735385725854133 | 13.970916436215 | 5e-21 exactly | 9.999999999999992e-21 |

Fourteen sharp mutations came out as expected under both methods.
Among them are the box 1e-30 below the packing’s extent, the closest pair 1e-30 past
contact, and a square enlarged 1e-30 past a wall and past its neighbour.

- **Against the house.** The side is 3.174277e-3 below the house (T-174) and below every
  packing reported at 182.
- **A new arrangement.** Against the house’s packing, the optimal assignment moves 44
  squares beyond 0.1, the largest by 0.813. No symmetry pairs the squares one to one.
- **The L-cut holds square for square.** Take T-188’s 211 packing in its own frame.
  The 29 squares whose centres lie within 1.5 of its right and top walls are exactly the
  ones your 182 do not use.
  The other 182 then moved: 17 by more than 0.1 (the largest by 0.464), 156 by more than
  0.01.
- **The start is T-188.** Where T-188 differs from Daniil Ostashev’s own 211 packing
  (T-175), your certificate follows T-188, so the start is Francisco Couzo’s arrangement
  of Ostashev’s design.
  The record should credit both (M-1).
- **Local minimality.** The record states the upper bound only.
  Your local-minimality analysis is numerical and was not replayed here; the record can
  carry it as your report.

The questions at the end ask what only you can answer.
None of them blocks the import.

## The Claim

$s(182) \le 13970916436214678735385725854133/10^{30} = 13.970916436214678735385725854133$
is the bound of `s182-1024.cert` (30,648 bytes, SHA-256
`9e12e0a42b05c4fcd2181c5255a4a19ab1aeb9a9f8c95f9943a20998a415fe97`, blob `a1c01bdf`). It
is printed as 13.970916436215, rounded up at 12 places.
The source describes the packing as a new local minimum found from an L-cut of “the
register’s s(211) packing”.

It is a finite packing, so the claim is an upper bound and nothing more.
The argument from certificate to claim has one step: $n$ closed unit squares with
pairwise disjoint interiors inside $[0, S]^2$ show $s(n) \le S$. A checker must
establish five things:

- the parsed file is the pinned file;
- each line is a unit square;
- the squares lie in the box;
- no two interiors meet;
- the print is at least the side.

## Exact Verification

**Custody.** Each source file this review read was taken from the blob at `d99925d` with
`git show`, and its size and digest match the issue’s table where the issue gives one
([custody](../../../packing/resources/web/evand-n182-2026-10-25/review/review-2026-10-25/out/custody.txt)).

- The commit is dated 2026-10-25T04:11:15Z (22:11:15 −06:00 on the 24th).
- \#806 was opened at 04:16:24Z.
- The push, at 04:16:05Z in `3c335fe..d99925d`, is the stage 1 triage’s reading of
  GitHub’s activity log.
  This session had no API access to the repository to read it again.

**The checker.** `exact_check.py` reads a header `n S` and $n$ lines `x y t` of integers
or integer fractions, refusing anything else.
Each line becomes a square of side 1 with edge directions $u = (c, s)$ and
$v = (-s, c)$, where $c = (1 - t^2)/(1 + t^2)$ and $s = 2t/(1 + t^2)$. So
$c^2 + s^2 = 1$ holds exactly, and the checker asserts it.
The corners are $(x, y) + \alpha u + \beta v$ for
$\alpha, \beta \in \{-\tfrac12, \tfrac12\}$. The checker decides the certificate twice:

- **Separating axes.** A square lies in the box exactly when its four corners do.
  Two convex polygons have disjoint interiors exactly when an edge normal of one of them
  weakly separates their projections.
  So every pair is decided on its four unit edge normals, and its gap is the largest
  projected gap.
- **Clipped areas.** Clipping a square to the box must leave area 1. Clipping one square
  to another must leave area 0. The clipping is Sutherland–Hodgman and the area the
  shoelace formula, in `Fraction`. For closed convex bodies, zero intersection area
  means disjoint interiors.

Both methods run over every wall and every one of the 16,471 pairs, with no distance
filter.

**Results**
([transcript](../../../packing/resources/web/evand-n182-2026-10-25/review/review-2026-10-25/out/check-s182-1024.txt),
[receipt](../../../packing/resources/web/evand-n182-2026-10-25/review/review-2026-10-25/out/check-s182-1024.json)):

|  | \#806, 182 |
| --- | --- |
| SHA-256 as pinned | `9e12e0a4…`, yes |
| Valid, separating axes | yes (182 walls, 16,471 pairs; 3.3 CPU s) |
| Valid, clipped areas | yes (the same; 3.4 CPU s) |
| Tilted squares | 68 |
| Least near-wall clearance | exactly 1/(2 · 10^20), square 0 |
| Least far-wall clearance | 5.00000000063645e-21, square 15 |
| Least pair gap, squares | 9.999999999999992e-21, squares 99–100 |
| Pairs within 1e-15 | 390, with 45 square–wall incidences: 435 contacts, the source’s own count |

Squares are numbered from 0 in file order.
The certificate is a contact packing dilated by $1 + 10^{-20}$ about the corner.
Squares at the near walls sit at $0.5 + 5 \times 10^{-21}$, and the side is the dilated
contact side rounded up at 30 places, which adds $6.36 \times 10^{-31}$. The source’s
`s182-1024.json` (lines 284–285) states `cert_min_wall` 5e-21 and `cert_min_pair`
9.999999999999992e-21, the binary64 values of the same clearances.

**Controls.** Each mutation is decided in full by both methods, with the expected
outcome fixed before the run
([transcript](../../../packing/resources/web/evand-n182-2026-10-25/review/review-2026-10-25/out/controls-s182-1024.txt)).
All fourteen came out as expected, and the two methods agreed on every one.

| Mutation | Expected | Separating axes | Clipped areas |
| --- | --- | --- | --- |
| Box at the packing’s extent $E$ ($S - E = 5.0 \times 10^{-21}$) | accepted | accepted | accepted |
| Box 1e-30 below $E$ | refused | 22 squares at the far walls | 22 squares at the far walls |
| Every square translated onto the near walls | accepted | accepted | accepted |
| The same, 1e-30 further | refused | 16 squares at the near walls | 16 squares at the near walls |
| Closest pair (99, 100), square 100 moved by exactly its gap along the separating axis | accepted | accepted | accepted |
| The same, 1e-30 further | refused | pair (99, 100), gap −1e-30 | pair (99, 100), area 9.5e-31 |
| Square with the least room (153, wall-limited) enlarged to its critical size | accepted | accepted | accepted |
| The same, 1e-30 larger | refused | square 153 | square 153 |
| Least pair-limited square (138, by square 85, room 1.73e-20) enlarged to its size | accepted | accepted | accepted |
| The same, 1e-30 larger | refused | pair (85, 138) | pair (85, 138), area 5.3e-61 |
| Square 0 moved 1e-30 past its wall clearance | refused | square 0 | square 0 |
| Square 0 duplicated | refused | pair (0, 182) | pair (0, 182), area 1 |
| Rotation sense reversed (every frame read as $(c, -s)$) | refused | 80 pairs | 80 pairs |
| Mirror image, $x \mapsto S - x$, $t \mapsto -t$ | accepted | accepted | accepted |

**The source’s regularized certificate.** `s182-1024_regularized.cert` (`f1ec415a…`) is
valid by both methods at the same side, with 478 pairs and 51 wall incidences in
contact, the 529 contacts its JSON states.
It is a display view and proves no further bound.

**Trust boundary.** The checker trusts Python’s `fractions` and integer arithmetic, its
own token reader, and the two geometric facts above.
Its two methods share the reader and the corner construction, and nothing else.
It shares nothing with Daniel’s `verify_cert.py`, `verify_cert2.py` or `exactsolve.py`,
or with this repository’s maintained routes and `devtools.upper_bound_reports`. Its
author read none of them.

It shares with every route the reading of `t` as $\tan(\theta/2)$ turning
counterclockwise, which the certificate’s format line implies but does not state (N-1).
Read the other way, 80 pairs overlap; the mirror image is valid, as it must be.
The certificate’s tilts agree with the binary64 input’s degrees, modulo 90, to
$2.9 \times 10^{-5}$ degrees.

## Sides and Prints

Exact arithmetic over the case record’s fractions and the source’s files
([sides](../../../packing/resources/web/evand-n182-2026-10-25/review/review-2026-10-25/out/sides.txt)):

- **The header side** is the issue’s $S'$ (line 19 of the issue body) and the solver
  report’s `S_cert`, exactly.
  Rounded up at 12 places it is 13.970916436215, the least 12-place decimal at or above
  it. Rounded up at 14 places it is 13.97091643621468, the commit title’s figure.

- **The margins.**
  - 3.174277e-3 below the house, T-174’s exact side, which T-098’s exact side and
    T-056’s printed side also exceed by that amount to seven digits.
  - 1.844911e-3 below Prathamesh Chavan’s side-only 13.9727613470647.
  - 1.592126e-11 below Subramanya N’s side-only 13.9709164362306.

  Neither side-only value comes with a packing, so neither is a report.

- **The padding.** The side lies $1.397092 \times 10^{-19}$ above the source’s KKT side
  $S^* = 13.970916436214678735246016689770\ldots$ (`.exact.txt`, line 1). It is
  $S^*(1 + 10^{-20})$ rounded up by $6.36 \times 10^{-31}$.

## Identity and Lineage

`identity_lineage.py` measures centres in binary64 under each of the box’s eight
symmetries, taking the optimal assignment that minimises the summed centre distance.
Orientations are compared modulo 90°. The program was written and run before this review
read the triage’s identity receipt or any identity code
([transcript](../../../packing/resources/web/evand-n182-2026-10-25/review/review-2026-10-25/out/identity-lineage.txt)).

| First | Second | Best symmetry | Nearest centres one to one | Beyond 0.1 | Beyond 1e-2 | Beyond 1e-3 | Largest move | Largest turn |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| \#806 | The source’s binary64 input | identity | yes | 0 | 0 | 0 (49 beyond 1e-9) | 2.55e-7 | 2.9e-5° |
| \#806 | The source’s 80-digit KKT point | identity | yes | 0 | 0 | 0 | below binary64 | 1.4e-14° |
| \#806 | The source’s regularized view | identity | yes | 5 | 11 | 37 (49 beyond 1e-9) | 0.381 | 0.36° |
| \#806 | T-174, the house (and its witness) | identity | no | 44 | 79 | 166 | 0.8127 | 41.7° |
| \#806 | T-098 | identity | no | 44 | 79 | 166 | 0.8127 | 41.7° |
| \#806 | T-056 | identity | no | 44 | 79 | 166 | 0.8127 | 41.7° |

With the boxes centred, the counts beyond 0.1 are unchanged, and the largest move
against the house is 0.8144. T-174’s certificate and the house witness give identical
figures, as they should: the case record’s witness `W-known-best-n182` is that
certificate.

So \#806’s certificate is the source’s binary64 packing polished: 49 squares move, none
by more than 2.55e-7. It is another arrangement than the one the register holds at 182,
which T-056, T-098 and T-174 hold in common.
The source’s own figures agree:

- 43 squares beyond 0.1 over all squares (`s182-1024_prior.json`), from regularized
  views;
- 38 among load-bearing squares (issue body, line 40).

### The L-Cut from T-188

The issue says the packing came from one L-cut job: “remove an L-shaped strip of 29
squares (a row and a column along two walls) from the s(211) packing, then relax”, then
three explorer moves (issue body, lines 61–64). The program tried every symmetry of the
211 box, with the 211 packing anchored at each corner of the 182 box.
In each placement it assigned the 182 squares optimally to 182 of the 211, and it took
the placement with the least summed distance.

- **The fit.** T-188 fits in its own frame (symmetry 0), with its lower-left corner on
  the 182 box’s, at summed distance 8.43. The next placements give 22.88 and 23.34, and
  no other symmetry gives less than 29.35. In this placement 165 of the 182 squares lie
  within 0.1 of their partners, and 59 of the 68 tilted squares do.

- **The 29 squares cut.** The squares of T-188 left unassigned are exactly the 29 whose
  centres lie within 1.5 of its right and top walls: a column of 15 and a row of 15,
  sharing the corner square.
  26 of them are axis-aligned, one is turned by 0.012°, and two are tilted by about 64°
  where the tilted bands meet the walls.
  Those two have centres 1.27 and 1.28 from the walls, which is why 27 squares lie
  within 1.0 of the walls and 29 within 1.5.

- **What moves.** 17 squares move beyond 0.1, 156 beyond 1e-2 and 173 beyond 1e-3, and 7
  coincide to 1e-9. The largest move is 0.464: square 160, at (1.50, 13.47), from
  T-188’s square 108. Of the 68 tilted squares, 59 lie within 0.1 and 11 within 1e-2,
  and none within 1e-3. The 17 beyond 0.1 lie in three places:
  - seven at the left end of the new top wall ($x$ 0.5 to 3.5, $y$ 11.5 to 13.5);
  - seven at the lower end of the new right wall ($x$ 11.3 to 13.5, $y$ 0.5 to 4.5);
  - three in the left middle (squares 10, 12 and 142).

  The first two are where the cut row and column ended.
  Everywhere else the moves are below 0.1, most above 0.01. That is the scale of 0.0226,
  the amount by which the final side lies below the nominal cut box, $14.99355 - 1$.

**Which 211 packing.** T-188’s claim names three other registered 211 packings of this
design: Ostashev’s T-175 and Couzo’s T-181 and T-182. T-188 differs from each by the
same five squares beyond 0.1, T-188’s 9, 10, 12, 14 and 141. Square 14 is in the cut
column. At the other four:

| T-188 square | \#806’s distance to T-188’s pose | to T-175’s | Follows |
| --- | ---: | ---: | --- |
| 141 (tilted) | 0.015 | 0.442 | T-188 |
| 9 | 0.024 | 0.175 | T-188 |
| 10 | 0.108 | 0.263 | T-188, loosely |
| 12 (tilted) | 0.308 | 0.066 | T-175; one of the 17 moved beyond 0.1 |

T-181 and T-182 agree with T-175 at these squares.
At 1e-9 the certificate coincides with more of T-175’s squares (15) than of T-188’s (7),
and every square that coincides with T-188’s also coincides with T-175’s. The extra
eight are axis-aligned squares stacked tight from the bottom wall up the left wall, plus
squares 144 and 169. Compression produces those grid positions from either start, so
they do not weigh against T-188. The tilted square 141, which follows T-188 to 0.015 and
T-175 only to 0.442, does weigh.

An earlier version of the program anchored the 211 packing only at the cut corner and at
the far corner, and chose by squares within 1e-3. That rule found axis-aligned blocks at
grid positions, which a unit grid matches under any whole shift, and missed this
placement. The kept version chooses by summed distance, the assignment’s own objective.

**What the measurements say.** The start is T-188’s packing, as the issue’s line 55 says
(store side 14.993549626299). The lineage is the L-cut the issue describes: the right
column and top row of 15 cut away, the rest relaxed in place.
“Short” describes the steps, not the motion (N-4): about a tenth of the squares moved
beyond 0.1.

## The KKT Point and Local Minimality

`kkt_consistency.py` read the source’s `s182-1024.exact.txt` at 100 digits, only as far
as it bears on what the record states
([transcript](../../../packing/resources/web/evand-n182-2026-10-25/review/review-2026-10-25/out/kkt-consistency.txt)):

- **The certificate is that point.** Its centres are dilated about the corner by
  $1 + 10^{-20}$ and its half-angle tangents rounded.
  The centres agree within $4.97 \times 10^{-36}$ and the angles within
  $4.85 \times 10^{-34}$ degrees.
- **The point as a packing.** The 80-digit point is a packing at $S^*$ only to its
  precision: pairs overlap by up to $3.5 \times 10^{-69}$, which is why the certificate
  dilates.
- **The contacts.** The point has the certificate’s contact structure: 45 walls and 390
  pairs active below 1e-60. The least inactive gaps are 3.45e-6 at a wall and 1.13e-5
  for a pair, as `s182-1024.json` states.
- **The free squares.** Six squares (121, 135, 142, 155, 163 and 180) touch nothing and
  keep the binary64 input’s values.
  These are the source’s `free_squares`.

**What the record may state.** The record states the upper bound, and only the
certificate’s side proves one.
$S^*$, which the issue calls the “exact side”, is a numerical value of the KKT system’s
solution. No certificate attains it (N-2).

The source’s local-minimality statement (issue body, line 32; `s182-1024.json`, line
193\) reads: “local minimum of S, strict modulo 43 exact flat motions (PD on the rest of
null(J_A)); the configuration is not isolated”.
Its basis is three numerical checks:

- a multiplier bound of 1.66e-5 (`lambda_A_maxmin`);
- a second-order test on a 45-dimensional null space;
- a corner–corner MILP descent test that found none.

It rests on 80-digit computation without interval enclosures, as the issue itself says.
Three gaps separate it from a proof (N-3):

- strictness holds only modulo the 43 flat motions and the six free squares, and a
  minimum along flat directions needs more than second order;
- the 68 corner–corner contacts make the feasible set non-smooth, and the MILP test
  covers their descent directions to first order only;
- nothing encloses an exact KKT point near the 80-digit one.

This review replayed none of it.
If the record carries the statement, it is the source’s report, in the entry’s claim or
notes, as T-098’s claim carries that source’s earlier statement: “not verified here; it
bears on the packings, not on s(n)”. Registered as a rigidity result of its own, it
would stand at `V1` at most, numerically checked by the source at recorded precision,
and `C0`. This review examined the point’s agreement with the certificate and nothing of
the stationarity or second-order computation, so it supplies no `C1` read of that claim.
No rung of the upper bound depends on it.

## Credit Chain

**The packing** is Evan Daniel’s, found by his search (“our explore loop”, issue body,
line 22). The commit `d99925d` carries a Co-Authored-By trailer naming Claude.

**The start** is T-188’s 211 packing.
That is Francisco Couzo’s further arrangement, by his hop search, of Daniil Ostashev’s
issue-575 design (T-175). The register credits it so, and the measurement above supports
it.

**The source’s files:**

- `CREDITS.md` at the pin (lines 1–108, blob `1d7dcb7`) concerns the repository’s
  lower-bound work and says nothing of `search/packer` or this candidate.
  Its “Provenance of this work” states that the repository’s work was “Produced by
  Claude (Anthropic) in a single session under human direction”.
- The commit message names no start.
- The issue names the start as “the register’s s(211) packing (Daniil Ostashev; also in
  Francisco Couzo’s repository)” (line 22), and asks that it be credited “(Daniil
  Ostashev)” (line 61). Its detail block (line 55) gives the store’s sources as “Daniil
  Ostashev (register); Francisco Couzo (watch:franciscouzo/square-packing@43ac7d2);
  Francisco Couzo (watch:franciscouzo/square-packing@487b058)”, side 14.993549626299.

So the chain is *Daniel, from Couzo’s arrangement (T-188) of Ostashev’s design (T-175)*.

## Significance

**S3, confirmed.** \#806’s certificate is a new arrangement at 182, 3.17e-3 below the
house and every packing reported there.

- **Identity.** No symmetry pairs it one to one with the house’s packing by nearest
  centres, and the assignment moves 44 squares beyond 0.1 and 79 beyond 1e-2.
- **Its neighbours.** It is S3 as T-158 (2.95e-3 to 3.44e-3), T-164 (1.75e-3) and T-240
  (4.45e-3 and 2.78e-3) are, and well above T-188’s further arrangement (S2).
- **Its limits.** It proves no lower bound or optimum.
  The cross-count construction is the source’s search method, not a result here, so S4’s
  reusable technique does not apply.

## Findings

No finding is blocking: the certificate decides its bound.
Lines are those of the files at `d99925d` and of issue 806’s body as fetched at 05:44Z
on 25 October (66 lines, SHA-256 `978d648d…`).

### M-1 (minor): The start’s credit names the finder only

**Where.** Issue body, lines 22, 55 and 61.

**What.** The issue asks the record to credit “the register’s s(211) packing (Daniil
Ostashev)” as the start.
The register’s packing at the side the issue gives (14.993549626299, line 55) is T-188.
The register credits T-188 to Francisco Couzo as his further arrangement of Ostashev’s
design (T-175), five squares beyond 0.1 from it.

The measurement places the start at T-188 rather than T-175: squares 141 and 9 follow
T-188 to 0.015 and 0.024 (Identity and Lineage).
The issue’s own line 55 lists Couzo’s repository among the store’s sources.

**Fix.** Credit *Evan Daniel, from an L-cut of Francisco Couzo’s 211 packing (T-188), an
arrangement of Daniil Ostashev’s design (T-175)*. Question 1 asks the author to agree.

### M-2 (minor): The commit title states an equality

**Where.** Commit `d99925d`, message line 1: “candidates: s(182) = 13.97091643621468
(polished and certified; …)”.

**What.** The result is an upper bound.
The issue’s title and table state it so.

**Fix.** The record states $s(182) \le$ and carries no “=”. Later titles can use “≤”.

### N-1 (note): The format line does not fix the rotation sense

`s182-1024.cert`, line 1, gives the frame $(c, s)$ from $t$. It does not give the
corners $(x, y) + \alpha(c, s) + \beta(-s, c)$ or the box $[0, S]^2$, and the sense is
load-bearing: read the other way, 80 pairs overlap.
The record’s readers take this convention already, for T-098 and T-188, and the
certificate is valid only under it.
Question 4 asks for the corner formula in the format line.

### N-2 (note): “Exact side $S^*$” is an 80-digit value, not a bound

Issue body, lines 32 and 44. $S^*$ comes from an 80-digit point that is a packing only
to its precision. The bound is the certificate’s side, $1.397 \times 10^{-19}$ above
$S^*$, and the record states that side.

### N-3 (note): The local-minimality statement is numerical

Issue body, line 32; `s182-1024.json`, line 193. The statement rests on 80-digit
computation without enclosures.
The flat motions, the free squares and the corner–corner contacts keep it short of a
proof (The KKT Point and Local Minimality).
If the record carries it, it does so as the source’s report.

### N-4 (note): “The lineage from the start is short” counts steps, not motion

Issue body, line 61. Measured against T-188 in its own frame, 17 squares move beyond
0.1, 156 beyond 1e-2 and 173 beyond 1e-3, and 7 coincide to 1e-9. The record should
state the measurement.

### N-5 (note): The source compares with T-098, not the house

`s182-1024_prior.json`, line 78, and `s182-1024_vs_prior.json`, field `prior`. Both
compare with T-098’s certificate (store 340). The house since 17 October is T-174,
PingYou Ltd’s refinement of the same packing.
The gap is 3.174277e-3 either way.
The identity counts agree to one square: 44 beyond 0.1 here, and the source’s 43 over
all squares, from regularized views.

### N-6 (note): The source’s credits file omits this candidate

`CREDITS.md`, lines 1–108, at `d99925d`. It covers the repository’s lower-bound work and
has no entry for `search/packer/candidates` or its 211 start.
The lineage and the credit of the start live only in the issue; a line in the file would
keep them with the files.

### N-7 (note): A side-only value lies 1.6e-11 above

Issue body, line 12. Subramanya N’s Kaggle leaderboard side, 13.9709164362306, is
1.592126e-11 above the certificate’s side.
By the issue’s account it was listed on 2026-10-24 at 18:41 UTC, about four hours before
the source’s search found the packing.
It has no packing and is no report, so it moves no bound.
The record’s text should not call \#806’s side the first known at this value.
“The first public packing at that side”, the issue’s own words, is accurate as far as is
known.

### N-8 (note, for the record): The case record’s rigidity statement goes stale on adoption

`packing/frontier/n-182.md`, front matter `rigidity`. The statement describes the
present witness, T-174’s packing, in which square 0 translates 0.357659. If \#806’s
certificate becomes the house, the statement must be derived again with
`devtools.screen_translation_escape`. The source reports six free squares, so “not
rigid” will stay; its scope text changes.

## Questions for the Author

1. **The start’s credit.** May the record credit the start as Francisco Couzo’s 211
   arrangement (T-188) of Daniil Ostashev’s design (T-175)? Where T-188 differs from
   Ostashev’s own 211 packing, your certificate follows T-188 (M-1).
2. **The cut.** Was the L the right column and the top row of the store’s 211 packing in
   its own orientation, 15 and 15 squares sharing the corner, as measured?
   Two of them are tilted, with centres 1.27 and 1.28 from the walls.
   Did the store hold T-188’s certificate poses, or a binary64 copy of them?
3. **Local minimality.** Do you plan an interval or exact enclosure of the KKT point, or
   an argument along the 43 flat motions?
   Until then the record carries the statement as your numerical report (N-3).
4. **The format line.** Would you add the corner formula and the box $[0, S]^2$ to your
   certificates’ format line (N-1)?

## Rungs

**`V3`/`C3`, confirmed, independently re-implemented**, for \#806’s entry once the
records lane’s replay evidence and this review’s are entered and this review is mapped
as accepted. The maintained replay is the records lane’s. This review’s checker is a
clean-room re-implementation by a Claude agent, and the producer’s commit names Claude
as co-author. The full phrase is *independently re-implemented, clean-room, by a Claude
agent, a system family the producer also used*.

By the house rule the entry then holds the smallest validated side at 182, and the
adoption moves the house to it.
No `V4`/`C4` follows, which needs a second accepted adversarial review by a distinct
reviewer and a human oversight record.
No lower bound, optimum, local minimum, rigidity or priority follows.

## Proposed Record Changes

These are for the records lane; this review writes none of them.
[record-changes.md](../../../packing/resources/web/evand-n182-2026-10-25/review/review-2026-10-25/record-changes.md)
gives each in full.

- **`verifiers.yaml`:** register `exact_check.py` as `V-evand-n182-review-check`
  (decides), with its independence record.
  The other programs decide nothing and stay unregistered.
- **`evidence.yaml`:** add `E-evand-n182-review-exact-feasibility`,
  `independent-implementation`, `coverage: full`, or fold it into the records lane’s
  replay entry. Record this document as `external_review` on
  `E-evand-n182-certificate-report`.
- **`results.yaml`:** the entry’s `reviews` gains this document (`kind: adversarial`,
  `reviewer_kind: ai`, `relation: project`, `verdict: accepted`). The significance stays
  S3 with the rationale drafted, `by` naming this review.
  The claim’s credit, lineage and local-minimality sentences follow M-1, N-3 and N-4.
- **`docs/project/document-map.yaml`:** map this document as a retained review.
- **The adoption at 182:** derive the rigidity statement again (N-8).

## Independence and Disclosure

- **Programs.** They were written for this review and are clean-room for what they
  decide. Their author read the mathematics, the certificate’s format line and, to
  compare, the source’s stored outputs: `s182-1024.json`, `_prior.json`,
  `_vs_prior.json`, `_regularized.json`, the issue and the commit message.
  It read none of Daniel’s `verify_cert.py`, `verify_cert2.py`, `exactsolve.py` or
  search code, nor the maintained routes, `devtools.upper_bound_reports` or
  `devtools.measure_identity`.

- **Read before these findings:**
  - the brief and the runbook’s stage 4;
  - epistemics.md’s Verification, Confirmation, Review Records, Scope and Composition,
    Significance and Novelty, Result Kinds and Results by Others;
  - the register entries of T-056, T-098, T-174, T-175, T-181, T-182 and T-188, and the
    significance of the single-count upper-bound entries from T-158 to T-242;
  - the case records at 182 and 211;
  - for format, four verifier entries and one evidence entry of earlier reviews, T-195’s
    `reviews` item and the document map.

  The sources were read as data, at `d99925d`.

- **Seen first.** The brief stated the triage’s result: one positive job accepted on
  both maintained routes, and 44 squares beyond 0.1 against T-174. It also stated the
  suggested S3 and the lineage claim.
  So the identity measurement was not blind to the 44.

- **Not read before these findings,** which were written by 06:19Z on 25 October: the 24
  October review of T-241 and T-242, read for layout at about 06:19Z, and the stage 1
  triage’s files, read from about 06:20Z. After reading them, this review:
  - took that review’s layout and finding labels;
  - added the custody listing;
  - took the record ids from the triage’s import plan;
  - wrote the comparison below.

  No finding and no figure changed.

- **Shared system family.** The reviewer is a Claude agent, and the producer’s commit
  names Claude as co-author.

## Comparison with the Stage 1 Triage

The triage (`c-triage-2lzo-1025`, bead `think-2lzo`) checked the side, decided one
positive job on both maintained routes and measured the identity with
`devtools.measure_identity`. Its files are in the coordinator’s scratch space and not on
`main`.

**Agreements.**

- **The side.** Both read the header side, the print 13.970916436215 and the margin
  3.174277e-3 below T-174. The triage gives $S - S^*$ as 1.40e-19, this review
  $1.397 \times 10^{-19}$.
- **The clearances.** The routes’ 5e-21 and about 1e-20 are this review’s.
- **Identity.** The identity figures match to the digit, from code that shares nothing:
  - against T-174, the house witness and T-098: no symmetry one to one, 44 squares
    beyond 0.1 and 79 beyond 1e-2, the largest move 0.812741 (0.814402 box-centred), 74
    squares turned, the largest turn 41.72°;
  - against the source’s input: one to one, 2.55e-7;
  - against the regularized view: 49 squares moved, 5 beyond 0.1 and the largest 0.381.
    The triage identifies the 49 as the source’s 43 flat-motion squares and six free
    squares; this review did not compare the sets.
- **The significance.** The draft S3 and its comparison with T-240 and T-162 stand.

**Disagreement.**

- **What T-188 is.** The triage’s import plan and ledger draft call T-188 “Daniil
  Ostashev’s packing, Francisco Couzo’s certificate” and “certified by Francisco Couzo
  at 487b058”. The register calls it Couzo’s further arrangement, five squares beyond
  0.1 from T-175. Where the two differ, the certificate follows T-188. The credit line
  should be M-1’s.

**Not in the triage.**

- **The lineage measurement.** The import plan assigned the L-cut measurement to this
  review.
- **The KKT consistency check.**
- **Sharp controls.** The triage ran the positive job only, so all fourteen controls are
  this review’s.

**Carried over, not checked here.** The push time, 04:16:05Z in `3c335fe..d99925d`, is
the triage’s reading of GitHub’s activity log.

## What This Review Does Not Establish

- **Beyond the bound.** No optimality, lower bound, local minimum, rigidity, novelty or
  priority, and no human oversight.
- **Runs it did not make.** No run or reading of the source’s checkers, this
  repository’s maintained routes or `devtools.upper_bound_reports`. No check of the
  stationarity, multiplier, second-order, flat-motion or MILP statements in the source’s
  JSON.
- **The search history.** The relaxation’s side 13.971254466 and the explorer’s moves
  are the source’s account; the lineage rests on the geometry alone.
- **Packings it could not compare.** Side-only leaderboard values come with no packing.
- **Changes it did not make.** No house adoption, case-record change or regularization.

## Files

- [README.md](../../../packing/resources/web/evand-n182-2026-10-25/review/review-2026-10-25/README.md):
  the programs, what each read, how to run them and what they printed.
- `programs/`:
  - `exact_check.py` (decides);
  - `identity_lineage.py`, `kkt_consistency.py`, `sides.py` and `custody.sh`, which
    decide nothing;
  - `run_review.sh`, which reproduces the outputs in `out/` (129 CPU seconds).
- [record-changes.md](../../../packing/resources/web/evand-n182-2026-10-25/review/review-2026-10-25/record-changes.md):
  the drafted `verifiers.yaml` record, evidence entries and register changes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
