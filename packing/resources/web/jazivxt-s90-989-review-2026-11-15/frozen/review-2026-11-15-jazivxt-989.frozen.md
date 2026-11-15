# The Certificate of #989 by jazivxt: Stage 4 Mathematical Review

**Date:** 2026-11-15 UTC. **Subject:** an exact rational certificate of 90 unit squares,
`n90.cert` of
[dpre4ai/n90-square-packing@179fcba](https://github.com/dpre4ai/n90-square-packing/tree/179fcba7f0e91e2c3d3e92525e0738b6da0f8dd5),
SHA-256 `88c93b2f1d1f3061d1e6815f790d13f3d8f174dd3431f50d8d4d9d4383b3d466`, issue
[#989](https://github.com/jlevy/squares/issues/989), opened by dpre4ai, which claims
$s(90) \le 9.998277166926$ and credits jazivxt and GPT-6 Astra Ultra.

**Reviewed at:** `main` `a4f36ae70`, and the pin above.

**Reviewer:** Claude (AI review), strong tier (`tbd-strong`, not the `tbd-strong-max`
tier the runbook names), at the reasoning setting its launcher chose, the stage 4
mathematical review lane (L169), separately prompted.
It read the source as data and ran only programs of its own, kept with their receipts in
[`packing/resources/web/jazivxt-s90-989-review-2026-11-15/`](../../../packing/resources/web/jazivxt-s90-989-review-2026-11-15/README.md).
Its checker is a clean-room implementation written for this review: it reuses no code
from any earlier review.
It took the reviews of #984 and #985 by lane L163 and of #983 by lane L159 as the model
for method, controls, freeze protocol and layout, read their texts and the L163 packet’s
README and frozen digest lists, and did not open the programs of either, or of any other
review. It is not a human oversight record.

## Summary for the Author

**Verdict on the bound: accepted.** No finding is blocking or major.

| n | Issue | Squares | Pairs | Wall contacts | Least pair gap | Least wall clearance | Verdict |
| ---: | --- | ---: | ---: | --- | --- | --- | --- |
| 90 | #989 | 90 | 4,005 | none | $1.19448 \times 10^{-12}$ (79, 81) | $2.1 \times 10^{-15}$ (squares 28, 33, 75 bottom; 61, 62, 71 left) | accept |

- **How the bound was checked.** A clean-room exact checker, written and frozen for this
  review before your README, your checksum file, the decimal CSV, the diagram, Francisco
  Couzo’s checker or this repository’s witness code was read, decided the file: every
  square, every wall and every pair, with no distance filter, by two methods that share
  only the reader. They are separating axes in plain Python integers, from the centres
  and half-angles, and exact convex clipping of the squares’ corners in GMP rationals,
  which computes the intersection of each pair, and of each square with the outside of
  each wall. They agree on all 4,005 pairs and all 360 square–wall pairs.
  Every pair is strictly apart, and every square is strictly inside $[0, S]^2$.
- **Controls.** All 23 controls stated in advance came out as stated.
  Reading the rotation the other way breaks the file (66 overlapping pairs).
  Moving square 60 to the left wall and turning it by $10^{-30}$ in $t$ pushes its
  corner across one way and frees it the other.
  Lowering the side by one unit of its own last place pushes out exactly the 13 squares
  nearest the right and top walls.
  Every one of the 4,005 pairs was closed along its centre line to exact contact and
  $10^{-30}$ past it, and every square was taken to its nearest wall and past it, by
  both methods.
- **The claim is the side.** The certificate’s side 4999138583463/500000000000 is
  exactly 9.998277166926, the number the issue claims, so the certificate decides the
  claim as printed.
- **No square touches a wall.** The packing clears the left and bottom walls by
  $2.1 \times 10^{-15}$ and the right and top by $2.377 \times 10^{-13}$. Its width in
  each direction is $S - 2.398228330832381 \times 10^{-13}$, and both methods accept it,
  translated, in the box of that side (control S1e). Nothing in the bound depends on it.
- **The arrangement.** 41 squares are upright, 44 are turned clockwise by 22.6° to
  31.6°, and five lie within 0.07° of upright.
  The near pairs form a contact arrangement opened by about $1.2 \times 10^{-12}$: 174
  pairs between $1.19448 \times 10^{-12}$ and $8.16 \times 10^{-12}$, and then none
  below $2.05 \times 10^{-4}$. Your “minimum pair separation … exceeded
  $1.19 \times 10^{-12}$” holds.

## Scope

**Read.**

- Issue #989 through GitHub (fetched before any program was written; never edited here).
- `n90.cert` at the pin, as data, and the clone’s file list with blob ids and sizes.
- On `main`: `packing/campaign/result-import.md` stage 4; and, to place this review’s
  files, the Ruff and BasedPyright sections of `packing/pyproject.toml`,
  `.flowmarkignore`, `lefthook.yml` and `biome.json`. None of it is witness, verifier or
  promotion code.
- The models: the review of #984 and #985 by lane L163,
  `docs/project/reviews/review-2026-11-14-ono-984-985.md`, its packet’s README and its
  three frozen digest lists; and the first 140 lines of the review of #983 by lane L159,
  `docs/project/reviews/review-2026-11-14-ozden-983.md` (its header, summary and scope).
  Not their programs, plans or receipts.
- The bead `think-176a` and the header of its parent epic.
- To see how the model review landed: the commit log of the L163 review file, and the
  names (not the contents) of the record files that mention it.

**Run.** Eleven Python programs and modules of my own, importing nothing from this
repository or the source ([What I Ran](#what-i-ran)). They decide the certificate twice,
run a self-test, compute the facts the controls are stated from, state the controls, run
them, and describe the file.

**Seen before my findings were written**, disclosed as the runbook asks:

- the lane’s brief, which states the pin, the certificate’s SHA-256 and exact side, the
  claim, the record’s side 10 at 90, the lineage (a crop of Joost de Winter’s packing of
  157, the record’s T-293, with successive copies shifted by one unit), that the issue
  reports Couzo’s checker accepting the file in strict mode, the record’s lower bound
  $s(90) \ge 389/40$ (T-082), the family statements to check after the freeze (T-081 and
  T-064 at $k = 10$, T-298 at 95), that 90 is $10^2 - 10$, and that the $10 \times 10$
  grid less ten squares has slack; and its framing of the significance to propose, that
  this would be the first packing below $k$ at $n = k^2 - 10$ for $k = 10$, with
  Kingbird’s and Friedman’s listings at 90 to find;
- the issue, which states the claim, the improvement 0.001722833074 on 10, the credit,
  the construction (successive copies of a crop of the 157 packing shifted horizontally
  by one unit, the vertical spacing reduced from about 9.353384 to 9.019403, a square
  window spanning two copies holding 90 tiles, then tightened and converted to exact
  rationals), the certificate’s digest, that Couzo’s checker accepted it in strict mode,
  that a separate exact check tested all four walls per square and all 4,005 pairs, and
  that the least pair separation on a certifying axis exceeded $1.19 \times 10^{-12}$;
- the model reviews named above.

**Not read before my checker was frozen** (2026-11-15T03:19:25Z) **or my findings were
frozen**: the author’s `README.md`, `SHA256SUMS`, `DONOR-LICENSE.txt`, `n90.csv` and
`n90.png` (all identified only by their blob ids in the tree listing); Couzo’s
`verify_bound_certificate.py`; this repository’s `sqpack` witness, verifier and
promotion code, its devtools that read witnesses, and the Rust crates; the register
entries, case record and house witness at 90, and the family entries; de Winter’s
`n157_exact.json`; the import lane L170 and its branch; and the model reviews’ programs.

**Not run here.** Any of the author’s code (none is published at the pin), Couzo’s
checker, or the maintained routes.

## The Claim and What It Needs

Issue #989 claims $s(90) \le C = 9.998277166926$. The certificate proves $s(90) \le S$:
there are 90 closed unit squares, rotated freely, with pairwise disjoint interiors
inside the closed square $[0, S]^2$. The claim follows when $C \ge S$; here $C = S$
exactly.

The format is the `.cert` text of Evan Daniel’s convention: a header `n S`, then `x y t`
per square, every scalar an exact rational, $(x, y)$ the centre and
$t = \tan(\theta/2)$. Then
$$\cos\theta = \frac{1 - t^2}{1 + t^2}, \qquad \sin\theta = \frac{2t}{1 + t^2}$$ are
rational, and with $u = (\cos\theta, \sin\theta)$ and $v = (-\sin\theta, \cos\theta)$
the square is $\{C + x u + y v : \lvert x\rvert, \lvert y\rvert \le 1/2\}$. The file has
no comment line; its 91 lines end in CRLF.

The hypotheses are six:

1. **The reading.** The header is `n S` with $n$ a positive integer and $S > 0$, and
   there are exactly $n$ further lines of three tokens.
   Every scalar is canonical: an integer as `[-]D`, anything else as `[-]P/Q` with
   $Q \ge 2$, no leading zeros, no sign on zero and $\gcd(\lvert P\rvert, Q) = 1$.
   Single spaces, one line terminator throughout (CRLF or LF), the last line terminated,
   nothing else: no blank line, comment, trailing space, tab or byte outside printable
   ASCII.
2. **The count.** 90 squares, numbered 1 to 90 in the file’s order.
3. **Unit squares.** Any finite rational $t$ gives a rational unit vector $u$, since
   $(1 - t^2)^2 + (2t)^2 = (1 + t^2)^2$; this format cannot state a square that is not
   unit, and both methods check it anyway.
4. **Containment.** Each square lies in $[0, S]^2$. The file does not say where the box
   is; it is accepted under the convention’s reading, centres in $[0, S]^2$ (F6).
5. **Disjoint interiors.** No two squares’ interiors meet.
6. **The rotation sense.** $\theta$ is read counterclockwise from the $x$-axis, $x$ to
   the right and $y$ up; control G6 shows that reading it the other way changes the
   verdict, and controls G5a and G5b that the sense is decided at a single square.

`l169_check.py` decides the first two through the reader, and the next three twice.

- **Method A** (`l169_sat.py`, Python integers).
  Each square’s centre is written over one denominator $E$, $C = (X, Y)/E$, and from
  $t = p/q$ its edge direction is $u = (a, b)/r$ with $a = q^2 - p^2$, $b = 2pq$,
  $r = p^2 + q^2$. The square is accepted when $r > 0$ and $a^2 + b^2 = r^2$. On a unit
  normal of square $i$, square $i$ projects to an interval of half-length $1/2$ and
  square $j$ to one of half-length $(\lvert\cos D\rvert + \lvert\sin D\rvert)/2$, $D$
  the angle between them, the same on both of $i$’s normals; the gap is the centre
  separation along the normal less both half-lengths, an exact distance.
  All four gaps of a pair share the denominator $2 E_i E_j r_i r_j$, so the margin,
  their maximum, is decided on integers and kept as an exact fraction: positive is
  apart, zero is contact with disjoint interiors, negative is overlap.
  Two convex polygons with disjoint interiors are weakly separated by a line parallel to
  an edge of one of them, so the three signs are exactly those three classes.
  A wall’s clearance is the signed distance from the square’s extreme corner to it, from
  the half-extent $(\lvert a\rvert + \lvert b\rvert)/(2r)$.
- **Method B** (`l169_clip.py`, `gmpy2.mpq`). Each square is turned into its four
  corners $C \pm u/2 \pm v/2$ in cyclic order, with $\cos\theta$ and $\sin\theta$
  computed from $t$ in GMP rationals, and from then on only the corners are used.
  Four points are a unit square in cyclic order when all four sides have squared length
  1 and both diagonals squared length 2. The listing must be counterclockwise (twice the
  shoelace sum is $+2$). A pair is decided by clipping one square against the four
  closed half-planes to the left of the other’s directed edges (Sutherland–Hodgman,
  keeping boundary points), so the result is the intersection exactly; it is clipped
  both ways round, and the two results must agree in class and area.
  Empty is apart; non-empty with zero area is contact, since the interior of an
  intersection of convex sets is the intersection of their interiors; positive area is
  overlap, by that area.
  Each wall is classed the same way, by clipping the square against the closed
  half-plane outside it.
  Containment is decided separately: a unit square lies in the box exactly when its
  intersection with the box has area exactly 1.

The two share only the reader (`l169_reader.py`), which hands them integers.
The verdict is `ACCEPT` only when both methods accept every square, wall and pair and
their classes agree everywhere; `l169_decide.py` runs both over every square, wall and
pair.

## The Certificate Decided

| Quantity | 90 |
| --- | --- |
| Scalars read, all canonical | 272 (the header’s two and 270 in 90 rows); 41 $t$ written as a bare `0` |
| The side | 4999138583463/500000000000, exactly 9.998277166926 |
| Squares, unit by both methods, listed counterclockwise | 90 of 90 |
| Pairs decided, apart by both methods | 4,005 of 4,005; none touches |
| Sum of all pair overlap areas (method B) | exactly 0 |
| Least pair margin | $1.194484972 \times 10^{-12}$, squares 79 and 81 |
| Positive pairs below $10^{-12}$, $10^{-10}$, $10^{-6}$, $10^{-3}$ | 0, 174, 174, 184 |
| Wall contacts | none |
| Least clearance at each wall | left $2.1 \times 10^{-15}$ (61, 62, 71); bottom $2.1 \times 10^{-15}$ (28, 33, 75); right $2.3772283 \times 10^{-13}$ (11 and seven more); top the same (82 and five more) |
| Positive clearances below $10^{-15}$, $10^{-12}$, $10^{-3}$ | 0, 27, 30 |
| The packing’s width in $x$ and in $y$ | each $S - 2.398228330832381 \times 10^{-13}$ |
| Verdict | `ACCEPT` |

- **Reading.** The file reads strictly: every scalar canonical, the header’s count equal
  to the rows, one terminator (CRLF) throughout.
- **Squares.** Every square is a unit square by both methods, listed counterclockwise.
- **Walls.** Every square lies in its box by both methods, with area exactly 1 inside,
  and their classes agree on all 360 square–wall pairs.
  No square touches a wall.
- **Near the walls.** 27 positive clearances lie below $10^{-12}$, in five exact values:
  at the left, squares 61, 62 and 71 at $2.1000000001021 \times 10^{-15}$, 59 at
  $3.0 \times 10^{-15}$ and 60 at $1.8997392 \times 10^{-13}$; at the bottom, 28, 33 and
  75 at $2.1000000001021 \times 10^{-15}$, 10, 23, 32 and 48 at $3.0 \times 10^{-15}$,
  and 47 at $4.8 \times 10^{-15}$; at the right, 11, 31, 34, 35, 47, 49, 55 and 83, and
  at the top, 82, 83, 84, 85, 88 and 90, all at
  $928604816731/3906250000000000000000000 = 2.3772283 \times 10^{-13}$. The next
  clearance is $1.51 \times 10^{-4}$ (square 63, left).
- **The side and the extent.** The least left and bottom clearances are equal, and so
  are the least right and top ones, so the packing’s width is the same in both
  directions, $S - 2.398228330832381 \times 10^{-13}$: the side is not the packing’s
  extent in either direction (F4).
- **Near pairs.** The 174 pairs below $10^{-10}$ lie between $1.19448 \times 10^{-12}$
  and $8.15536 \times 10^{-12}$, median $1.20662 \times 10^{-12}$, in 126 distinct exact
  values; 139 lie below $1.22 \times 10^{-12}$, 173 below $1.5 \times 10^{-12}$, and the
  last is (25, 41). The commonest values are $1.206 \times 10^{-12}$ (13 pairs) and
  $1.204 \times 10^{-12}$ (9). Of the 174, one normal binds in 60, two in 112 and four
  in 2. The next pair is $2.05262 \times 10^{-4}$ (squares 26 and 70): the certificate
  is a contact arrangement opened by about $1.2 \times 10^{-12}$ (F5).
- **Tilts.** 41 squares are exactly upright; one more, at $t = -10^{-14}$, lies within
  $10^{-11}$ degrees of upright, and four more lie within 0.07° (0.0029°, 0.0200°,
  −0.0212° and −0.0625°). 44 are turned beyond 0.5°, all clockwise, from −22.61° to
  −31.56°: 25 of them at −22.914477° to six places, under seven distinct values of $t$
  spanning $1.24 \times 10^{-12}$, six of them within $10^{-13}$ of one another; four at
  −22.61°, three at −23.11°, two each at −24.09°, −24.95°, −27.61° and −31.56°, and one
  each at −22.75°, −22.93°, −22.94° and −23.14°. There are 25 distinct values of $t$ in
  all (F7).

The least margin and clearances are exact fractions in the receipts; the prints here are
rounded.

`l169_selftest.py` holds both methods and the reader to 6,166 cases and passes:

- edge-to-edge contacts in four directions for upright squares and for squares turned by
  $(3/5, 4/5)$ and $(5/13, 12/13)$, along each of their four edge directions, with an
  offset of 0 and $1/3$ along the edge; corner-to-corner contacts in four directions at
  each of those angles; a $(3/5, 4/5)$ and a $(4/5, 3/5)$ corner on an upright edge
  under each quarter turn of the plane; each at a gap $\delta$ of $10^{-30}$, 0 and
  $-10^{-30}$, with each square under every equivalent half-angle $t$,
  $(t + 1)/(1 - t)$, $-1/t$ and $(t - 1)/(1 + t)$ where defined, and in both orders.
  The margin is $\delta$ in all of them, by method A and by the closed form, and the
  overlap areas, derived by hand, are $\lvert\delta\rvert$,
  $\tfrac23\lvert\delta\rvert$, $\delta^2$ and $\tfrac{25}{24}\delta^2$;
- duplicates at four angles (margin $-1$, area 1), and an upright square against its
  concentric rotation by $(3/5, 4/5)$ and by $(4/5, 3/5)$ (margin $-6/5$, area $5/6$,
  from four corner triangles with legs $1/4$ and $1/3$);
- each wall at $10^{-30}$ inside, at contact and $10^{-30}$ out, for squares at seven
  angles, two of them the certificate’s own $t$, with B’s containment test;
- the unit test and listing sense at six angles, among them $t = 10^{-30}$; seven shapes
  method B must refuse as unit squares listed counterclockwise, and three triples method
  A must refuse;
- 300 random rational pairs with Pythagorean rotations, on which method A’s margin must
  equal the closed form of `l169_geom.py` (corner projections, not half-extents) and
  method B’s class its sign, both ways round; 300 more closed along their centre line to
  $10^{-30}$ short of contact, to it and $10^{-30}$ past it, with margins exactly
  $10^{-30}$, 0 and $-10^{-30}$ by both A and the closed form and B’s class to match;
  300 random turned squares taken to a wall, short of it, at it and past it;
- 30 malformed texts the reader must refuse, a valid text it must read the same with
  CRLF and LF and write back byte for byte, and four whole-file decisions: a duplicate,
  a square $10^{-30}$ outside, an edge contact, and a turned square touching two walls.

Three deliberately broken copies fail it: method A using only square $i$’s two normals
(288 failures), method A counting a zero margin as apart (1,476), and method B clipping
with open half-planes (1,584).

## Controls

`controls-plan.json` states 23 controls and the outcome of each.
It was written and hashed (`71bee737…`, 2026-11-15T03:21:48Z) before `l169_controls.py`
existed, from the check receipt and from `l169_plan_facts.py`, which computes every
margin, clearance and closing move by the closed form of `l169_geom.py` (corner
projections in fractions, a third formulation, apart from both methods) and decides no
modified file. That program first recomputed every margin and clearance of the
certificate by the closed form: the SHA-256 of both exact lists equals method A’s.
“Contact” is a margin or clearance of exactly 0, and “past” is $10^{-30}$ beyond it.

Every whole-file control was decided by both methods over every square, wall and pair,
after the modified certificate was written as text and read back through the reader; G3,
G4 and G7b stop at the reader.

| Control | Stated | Outcome |
| --- | --- | --- |
| G1. Square 90 given square 1’s centre and $t$ | refused: exactly the pair (1, 90) overlapping, margin $-1$, area 1; no other pair or wall changes class | as stated |
| G2. Square 1 translated by $(S, 0)$ | refused: square 1 across the right wall by both (its right clearance $-6.998$, the plan’s exact value), not inside by B’s area; no pair overlapping or touching | as stated |
| G3. Square 90’s row deleted | the reader refuses: the header says 90, the file has 89 rows | as stated |
| G4. The side written as $2p/2q$ | the reader refuses: not in lowest terms | as stated |
| G5a. Square 60, the turned square nearest a wall, moved to the left wall by its clearance $1.8997 \times 10^{-13}$, then $t + 10^{-30}$ | accepted, its left clearance exactly $+5.1075 \times 10^{-31}$; no pair or other wall changes class | as stated |
| G5b. The same with $t - 10^{-30}$ | refused, exactly $-5.1075 \times 10^{-31}$, square 60 not inside by B’s area; no pair changes class | as stated |
| G6. Every $t$ negated (the rotation read the other way) | refused for exactly the plan’s 66 overlapping pairs, none touching; the clearance list unchanged | as stated |
| G7a. The text with LF line ends | accepted; margin and clearance lists unchanged | as stated |
| G7b. The header’s count written as 91 | the reader refuses: the header says 91, the file has 90 rows | as stated |
| G8. Every square transposed, $(x, y, t) \to (y, x, -t)$ | accepted, the margin list unchanged, the clearance list transposed | as stated |
| G9. Every $t$ replaced by $(t + 1)/(1 - t)$, the angle plus 90° | accepted; margin and clearance lists unchanged | as stated |
| G10. Every $t$ replaced by $(t - 1)/(1 + t)$, the angle less 90° | the same | as stated |
| G11. The packing turned a quarter about the box centre, $(x, y, t) \to (S - y, x, t)$ | accepted, the margin list unchanged, the clearance list turned | as stated |
| S1a. The side lowered by $1/q = 2 \times 10^{-12}$, one unit of its own last place | refused: exactly the 14 right and top clearances of $2.377 \times 10^{-13}$ crossing (13 squares; 83 at both) | as stated |
| S1b. The side lowered by $10^{-30}$ | accepted, no contact: no positive right or top clearance is below $10^{-30}$ | as stated |
| S1c. The side lowered by the least right-or-top clearance | accepted, exactly those 14 square–wall pairs touching | as stated |
| S1d. That, less $10^{-30}$ more | refused, exactly those 14 crossing | as stated |
| S1e. The packing translated by minus the least left and bottom clearances, in the box of side $S - 2.398228330832381 \times 10^{-13}$ | accepted, the margin list unchanged, contacts exactly at 61, 62, 71 left, 28, 33, 75 bottom and the 14 at the right and top | as stated |
| S1f. The same box less $10^{-30}$ | refused: the 14 at the right and top crossing, the six at the left and bottom still touching | as stated |
| S4c. Square 79 moved toward 81 along their centre line to exact contact | that pair alone touching by both, margin exactly 0, B area 0; accepted | as stated |
| S4p. The same, $10^{-30}$ past | that pair alone overlapping by both, margin exactly $-10^{-30}$ | as stated |
| S5. Every pair closed along its centre line (pair-level) | touching at contact by both, overlapping past; margins exactly 0 and $-10^{-30}$; the closing times’ digest the plan’s | 4,005 of 4,005 |
| S6. Every square moved to its nearest wall by its clearance (square-level) | contact at, crossing past, by both; clearance exactly 0 and $-10^{-30}$; inside by B’s area at contact, not past | 90 of 90 |

All 23 came out as stated: `EVERY_CONTROL_AS_STATED`.

- **G5.** No square touches a wall, so the rotation sense is tested at a square first
  moved to one. The plan took the turned square with the least clearance at any wall:
  square 60, $t = -2026751922729/10^{13}$ (−22.91°), $1.8997 \times 10^{-13}$ from the
  left wall, whose next pair margin at contact is $1.278 \times 10^{-12}$. Turning it a
  further $10^{-30}$ in $t$ toward upright frees its corner by $5.1075 \times 10^{-31}$,
  and turning it the other way pushes the corner out by as much: the sense is decided at
  one square, with every pair and every other wall unchanged.
- **S1.** The side’s denominator is $5 \times 10^{11}$, so one unit of its last place is
  $2 \times 10^{-12}$, about eight times the right and top clearances.
  S1c to S1f find the box the squares actually need: the side less
  $2.398228330832381 \times 10^{-13}$, exactly, and not $10^{-30}$ less.
- **S4.** The plan took the tightest pair whose closing move, $10^{-30}$ past contact,
  is shorter than every other margin and every clearance of the moved square, compared
  exactly through squares of lengths.
  The tightest pair, (79, 81), passes with square 79 moving: its move is
  $1.2050 \times 10^{-12}$ and its next margin $1.2142 \times 10^{-12}$.
- **S5.** All 4,005 pairs, not only the near ones, were closed along their centre lines.
  The plan moved square $j$ toward square $i$ to the time
  $\max_n (g_n - m^*)/\lvert n \cdot d\rvert$ over the normals with a rate, $g_n$ the
  gap on normal $n$ and $d$ the centre difference, which makes the margin exactly $m^*$
  ($0$ or $-10^{-30}$) whatever the other normals do; the controls’ closing times
  reproduce the plan’s digest.
- **G6.** The least margin of the reflected file is $-2.91 \times 10^{-1}$ (squares 21
  and 54).
- **G8 to G11.** The transposed, re-based and turned files’ margins equal the original’s
  exactly (the SHA-256 of the margin list is the same), and G9 and G10 leave the exact
  clearance list unchanged, which holds each method to the symmetries it should have.
- **S6.** The nearest walls are the left for 21 squares, the right for 21, the bottom
  for 25 and the top for 23.

## What This Review’s Checker Shares

- **With other checkers.** It shares no code with any other checker, and it was written
  and frozen before Couzo’s checker or any of this repository’s witness, verifier or
  promotion code was read; the author publishes no checker at the pin.
  It reuses nothing of any earlier review’s programs, none of which it opened.
  Its two methods follow the mathematics the models’ texts describe: separating axes in
  integer arithmetic over per-square denominators, from centres and half-angles as
  Pythagorean triples with one half-extent for both normals of a square, and exact
  clipping of corners with a sides-and-diagonals unit test, wall classes by clipping
  against each wall’s outer half-plane and containment by area.
  It implements them afresh; method B also clips each pair both ways round.
  Its controls follow the models’ list, with G5 recast for a file in which no square
  touches a wall, G7 recast for a format with no twin, S1 extended to find the box the
  squares need, and S5 widened from the near pairs to every pair.
  It shares the mathematics above and the format’s meaning (centre and
  $t = \tan(\theta/2)$ counterclockwise, the box $[0, S]^2$), taken from the issue, the
  model reviews and the file.
- **Its trust base.** CPython 3.14.7’s integers and `fractions`, GMP 6.3.0 through
  `gmpy2` 2.3.1, and the facts its self-test exercises.
  Its two methods share the reader and nothing else.
- **Authorship.** The issue credits GPT-6 Astra Ultra as the AI collaborator on the
  search and verification.
  This review was written by a Claude agent, as were both model reviews; the
  independence claimed here is of code and of what was read.

## Findings

| Id | Severity | Where | Finding |
| --- | --- | --- | --- |
| F1 | note | `n90.cert` | an exact packing of 90 squares at its side, by both methods, every wall and pair; every pair strictly apart; no square touches a wall |
| F2 | note | the controls | all 23 stated controls came out as stated |
| F3 | note | the claim | the side 4999138583463/500000000000 is exactly 9.998277166926, the claim, so the certificate decides the claim as printed |
| F4 | note (records) | `n90.cert`, the side | the side is not the packing’s extent: the least clearances are $2.1 \times 10^{-15}$ at the left and bottom and $2.3772283 \times 10^{-13}$ at the right and top, so the squares fit, translated, a box $2.398228330832381 \times 10^{-13}$ smaller (S1e), and not $10^{-30}$ less (S1f) |
| F5 | note (records) | `n90.cert`, the near pairs | a contact arrangement opened by about $1.2 \times 10^{-12}$: 174 pairs from $1.19448 \times 10^{-12}$ to $8.16 \times 10^{-12}$, then $2.05 \times 10^{-4}$; how this bears on the record’s padding question is measured after the freeze |
| F6 | note (author) | `n90.cert`, the format | the file states neither the box nor the sense of $\theta$, and has no comment line; read as $[0, S]^2$ with $\theta$ counterclockwise and $y$ up it is accepted, and read clockwise 66 pairs overlap (G6) |
| F7 | note (records) | `n90.cert`, the tilts | 41 upright, 44 turned clockwise by 22.6° to 31.6°, five within 0.07°; 25 squares share −22.914477° under seven values of $t$ spanning $1.24 \times 10^{-12}$, consistent with the issue’s “tightened … and converted the result to exact rational coordinates” |

**F1. Feasibility.** The file is an exact packing at its side: 4,005 pairs, each decided
by both methods with equal classes and strictly apart, and every square a unit square
strictly inside its box by both.
The bound $s(90) \le S$ holds.

**F2. Controls.** As [Controls](#controls) gives them: 23 of 23 as stated, including the
rotation read the other way, the rotation sense at a single square, the side lowered by
$1/q$, every pair closed to exact contact and past it along its centre line, and every
square taken to its wall and past it.

**F3. The claim.** $4999138583463/500000000000 = 9.998277166926$ exactly, so $C = S$ and
nothing is rounded.

**F4. The side and the extent.** No square touches a wall.
The left and bottom are cleared by $2.1 \times 10^{-15}$ and the right and top by
$2.377 \times 10^{-13}$, by squares 61, 62 and 71, 28, 33 and 75, and fourteen
square–wall pairs at the right and top.
Translated by minus the least left and bottom clearances, the squares fit the box of
side $S - 2.398228330832381 \times 10^{-13} = 9.9982771669257601771669167619$, accepted
by both methods with contacts at all four walls, and not that box less $10^{-30}$. The
certificate therefore proves a bound $2.4 \times 10^{-13}$ below the side it states.
The margin is about $7 \times 10^{9}$ times smaller than the step of 0.001722833074 the
issue states on 10, and nothing needs correcting; the record registers the claim as
stated, or that side, as it chooses.

**F5. Margins of $1.2 \times 10^{-12}$.** Of the 174 near pairs, 139 lie below
$1.22 \times 10^{-12}$ and 173 below $1.5 \times 10^{-12}$; the last is
$8.16 \times 10^{-12}$ (squares 25 and 41), and the next pair is $2.05 \times 10^{-4}$:
a contact arrangement opened uniformly.
The issue’s “exceeded $1.19 \times 10^{-12}$” holds: the least margin is
$1.194484972 \times 10^{-12}$ at (79, 81).

**F6. The box and the rotation sense.** The file is bare: `n S` and 90 rows, with no
comment naming the box or the sense of $\theta$. Read with the convention the issue
names, centres in $[0, S]^2$ and $\theta$ counterclockwise, it is accepted, and G6 shows
the sense matters. A comment line, or the README, saying “$[0, S]^2$, $\theta$
counterclockwise with $y$ up” would close the question for a reader without this review.
The CRLF line ends do not matter to this reader (G7a).

**F7. The tilts.** 44 squares are turned clockwise, by 22.61° to 31.56°, and the angle
−22.914477° is carried by seven values of $t$ spanning $1.24 \times 10^{-12}$. The
values are not one closed form repeated; that bears on the lineage, which is checked
after the freeze.

None changes a verdict; all are notes.

## Verdict

**Accepted as an upper bound.** The certificate proves $s(90) \le S$ at its side
exactly, and its side is the issue’s claim $s(90) \le 9.998277166926$.

- Every hypothesis holds exactly, for every square, wall and pair, by two methods that
  agree everywhere.
- Every control is decided as stated beforehand.
- No defect of the certificate or of its mathematics is open; every finding is a note.

Mapped as an adversarial review with verdict `accepted`, it supports `V3` and `C3` at
90, provided `l169_check.py`’s run is registered as exact-algebraic evidence replayed
here with full coverage of the certificate.
That reads as confirmed, independently re-implemented, clean room, by a Claude agent.
`V4` and `C4` would need a second accepted adversarial review by a distinct reviewer and
a human oversight record.

## What I Ran

All with CPython 3.14.7 (`uv run --frozen --all-extras --group dev python -I -B`, from
`packing/` of a worktree of `main` at `a4f36ae70`) under `nice -n 19`, one process at a
time. The programs, the frozen files and the receipts are in
[`packing/resources/web/jazivxt-s90-989-review-2026-11-15/`](../../../packing/resources/web/jazivxt-s90-989-review-2026-11-15/README.md).

| Program | Receipt | CPU |
| --- | --- | ---: |
| `l169_selftest.py` | `out/selftest.json`: `PASSED`, 6,166 cases | 1.3 s |
| `l169_check.py` | `out/check-n90.json`: `ACCEPT` | 0.4 s |
| `l169_plan_facts.py` | `out/plan-facts-n90.json`, kept as written before the plan | 4.0 s |
| `l169_make_plan.py` | `programs/controls-plan.json` | under 1 s |
| `l169_controls.py` | `out/controls-n90.json`: 23 of 23 as stated | 10.4 s |
| `l169_describe.py` | `out/describe-n90.json`: the tilts, gaps and extents; decides nothing | under 1 s |

What went wrong along the way, and was redone before the freeze it precedes:

- The first run of the self-test stopped on import: `python -I` leaves the script’s
  directory off the module path.
  Each entry point now puts its own directory first; nothing else changed.
- The self-test and the check then ran once each into scratch space, for timing, before
  the receipts kept here were written by the same code.
- The scratch check receipt was summarised once with the system `python3`, against this
  repository’s rule; it printed a JSON file and decided nothing.
- The pre-commit hook could not run in this worktree (`lefthook` is not on its `PATH`);
  the commits went through without it.
