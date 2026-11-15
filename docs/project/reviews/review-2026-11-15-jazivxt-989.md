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

*Added after the findings were frozen*, from the checks the lane’s brief orders after
the freeze ([After the Freeze](#after-the-freeze)):

- **Your arithmetic holds.** The side is the claim exactly, and its gain on 10 is
  exactly 0.001722833074, relative $1.72 \times 10^{-4}$. Your README’s least
  separating-axis clearance, $1.19448 \times 10^{-12}$, is this review’s least margin,
  and its box and rotation sense are the ones this review read (F14).
- **Nothing in the record conflicts.** No family, theorem or register entry claims
  $s(90) = 10$. At $k = 10$ the families of $s(k^2 - c) = k$ have deficits 1 to 5 and
  stop at 95, where $s(95) = 10$ is proved (T-191); $90 = 10^2 - 10$ is outside all of
  them. The lower bounds at 90 are 9.73, verified (T-091), and 9.78, reported (T-212),
  both below your side.
  What the claim does refute is the case’s listed conjectured optimum, the integer 10
  (F8, F9).
- **None of it is padding.** The house at 90 is the grid, whose contraction margin is 0:
  its squares 1 and 2 touch, and every full row of ten spans the side.
  RV-3 does not apply (F10).
- **Your construction reproduces.** From de Winter’s 157, the crop to the top of his
  square 103 is 9.3533845 high; a copy shifted by one unit clears it at pitch
  9.019403129; and a side-10 window across the two copies holds 90 squares.
  Your certificate pairs one to one with those 90 under the identity: no square moves
  more than 0.146 and none turns more than 4.02° (F11). The README does not say where
  the window sat: the box at the placement that fits your certificate holds 91 centres.
- **A new arrangement**, relative to the grid, the only packing the record holds at 90.
  No $s(m) + j$ lies within $10^{-3}$ of the side, and no L step from it moves another
  count.
- **Custody holds.** The certificate’s blob is unchanged across both publishing commits,
  every digest in `SHA256SUMS` holds, the CSV equals the certificate to
  $8.2 \times 10^{-16}$, and the issue was opened 11 seconds after the pin’s commit.
  The repository states no licence of its own; its only licence file is de Winter’s MIT
  notice (F12). The commit before the pin credited “Codex Astra Ultra” (F13).
- **Significance.** S3. 90 is $10^2 - 10$: the smallest $n$ with $s(n^2 - n) < n$ falls
  from 11 (Cantrell’s 110, 2025) to 10, which answers the first target of Evan Daniel’s
  atlas, “s(90) < 10”. The record scored the earlier firsts below the grid at 211, 183,
  157 and 308 S3.

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

## After the Freeze

Everything in this section was written after the findings were frozen at
2026-11-15T03:28:11Z and pushed as `d20230eb6`. It follows the lane’s brief, which puts
the claim’s arithmetic, the record at 90 and the families that reach $k = 10$, the
contraction margins and RV-3, identity and lineage, the closed-form question, the
licence, dating and custody, and the significance after the freeze.

**The record.** `main` was at `a4f36ae70` throughout; nothing at 90 moved while this
review ran.

**Read after the freeze.**

- The author’s `README.md`, `SHA256SUMS`, `DONOR-LICENSE.txt`, `n90.csv` and `n90.png`.
- Couzo’s `verify_bound_certificate.py`, as the `couzo-issue678-2026-10-18` packet
  retains it, byte-identical to `712c6a6`’s by the `couzo-issue843-2026-10-28` packet’s
  acquisition record: read, not run.
- On `main`: `n-090.md`, and the front matter of every case record (through
  `l169_record.py`); the register entries T-007, T-057, T-058, T-064, T-081, T-091,
  T-135, T-212, T-220, T-293 and T-298, and the rungs of T-191; the significance scale
  in `epistemics.md`; the T-293 packet’s README and acquisition declaration, and de
  Winter’s `n157_exact.json` as it retains it; the house witness at 90, through the
  devtools; the help texts of `devtools.contraction_margin` and
  `devtools.measure_identity`.
- The §1 and §7 rows of the review of Evan Daniel’s atlas (5 October), and the atlas’s
  `WISHLIST.md` and problems page as the `evand-square-packing-2026-10-04` packet
  retains them.
- Kingbird’s catalogue as captured on 30 September 2026, from 88 to 132; Friedman’s DS7
  survey (2009) and Packing Center page, at Table 1, the $s(n^2 - n)$ passage and
  Conjecture 1.

Still unread: the import lane L170 and its branch; this repository’s verifier and
promotion code; the reviews of T-191 and T-293.

### The Record at 90

`l169_record.py` (`out/record-n90.json`) reads the front matter of every case record.

| Lane | At 90 | Source |
| --- | --- | --- |
| Reported upper bound | 10, the trivial grid (`construction_method: trivial-grid`) | the Kingbird catalogue; witness `W-known-best-n090` |
| Verified upper bound | 10 | `E-basic-grid-upper` |
| Reported and verified lower bound | $973/100 = 9.73$ | T-091 (Hosono, 4 October), which replaced T-082’s $389/40$ on 5 October |
| A claim held outside the reported lane | $489/50 = 9.78$ | T-212, `V0`/`C0`, not yet replayed |
| Conjectured optimum | `integer` | the case |

- **The lower bound.** The brief’s $389/40$ (T-082) is no longer the record’s lower
  bound at 90: T-091’s $973/100$ replaced it in both lanes on 5 and 6 October.
  T-212’s $489/50$ stays outside the reported lane until a complete replay, by its own
  rationale. All three lie below the claim; the gap from the verified lower bound to the
  claim is $0.268277166926$.
- **The families at $k = 10$.** $s(k^2 - 1) = k$ and $s(k^2 - 2) = k$ give $s(99)$ and
  $s(98)$. T-064, $s(k^2 - 3) = k$ for $k \ge 6$, proves $s(97) = 10$ (`V3`/`C3`).
  T-081, $s(k^2 - 4) = k$ for $k \ge 5$, reports $s(96) = 10$ (`V0`/`C1`). T-191,
  Greff’s mixed cover, proves $s(95) = 10$ and with it $s(96)$ (`V3`/`C3`). T-298,
  $s(k^2 - 5) = k$ for $k \ge 7$, reaches $s(95) = 10$ by a second, reported route
  (`V0`/`C1`).
- **None reaches 90.** Their deficits are 1 to 5, and $90 + c$ is a square for no
  $c \le 5$; 90 is $10^2 - 10$. No family, theorem or register entry claims
  $s(90) = 10$. The entries whose scope includes 90 are lower bounds (T-007, T-069,
  T-082, T-083, T-091, T-212), a correction (T-085) and a method limit (T-058). The
  claim contradicts none of them, and the proved values at $k = 10$, $s(n) = 10$ for
  $95 \le n \le 100$, sit above it as monotonicity requires.
- **What it does contradict** is the case’s `conjectured_optimum: integer` and its
  prose: “no arrangement has ever been found that beats the trivial
  $\lceil\sqrt{90}\rceil = 10$ grid” (F9).
- **The method limit.** T-058 bounds what a rectangle-density certificate on the
  standard net can prove by $\alpha U$, with $U$ the side of any packing of $n$ squares
  and $\alpha = 399908091/400000000$. With $U$ the new side, that ceiling at 90 falls
  from 9.99770 to 9.99598, still above every lower bound at 90.
- **Friedman’s Conjecture 1**, “if $s(n^2 - k) = n$, then $s((n+1)^2 - k) = n + 1$”,
  read backwards at deficit 10, makes $s(90) < 10$ require $s(71) < 9$, which the record
  holds (8.944072). On best known values the staircase $c^*(k)$, the largest deficit at
  the grid, was 9, 10, 10, 11 at $k = 9$ to 12; with the claim it is 9, 9, 10, 11, still
  non-decreasing.

### The Sides and the Prints

| Quantity | Value |
| --- | --- |
| The side $S$ | $4999138583463/500000000000$, exactly 9.998277166926 |
| The claim | 9.998277166926, equal to $S$ |
| The record improved | 10, reported and verified |
| Gain, exact; relative | $861416537/500000000000 = 0.001722833074$; $1.722833074 \times 10^{-4}$ |
| The issue’s and README’s print of the gain | 0.001722833074, exact |
| The side the squares fit, translated (S1e) | 9.9982771669257601771669167619, $2.398228330832381 \times 10^{-13}$ below $S$ |
| The README’s least separating-axis clearance, “approximately $1.19448 \times 10^{-12}$” | this review’s $1.194484972 \times 10^{-12}$ at (79, 81) |

Every print in the issue and the README holds exactly; there is no rounding to check.

### Is the Improvement Real?

`devtools.contraction_margin`, run read-only with its receipts written to this review’s
packet, contracts a certificate uniformly about the origin to its first contact and
decides the contracted certificate on both maintained exact routes.
It read the certificate through the `evand-cert` adapter, CRLF line ends and all, and
the house witness through `witness-corners`.

| Certificate | First contact, $1 - \lambda^*$, pair | Side margin | Against the claim |
| --- | --- | --- | --- |
| The house at 90, the grid (`W-known-best-n090`) | 0; squares 1 and 2 already touch | 0 | gain $1.723 \times 10^{-3}$, `within_margin: false` |
| #989 | $1.194485 \times 10^{-12}$, (79, 81) | $1.0988 \times 10^{-11}$ | — |

- **RV-3**, the owner’s open question whether a gain inside a certificate’s padding
  counts, does not apply: the grid has no padding.
  The house is nine full rows of ten in $[0, 10] \times [0, 9]$, so its side is its
  extent in $x$, which every row spans edge to edge.
  The slack the brief notes is real but of another kind: the top row is empty, so ten
  squares can slide up by 1 (the case’s rigidity field), which frees nothing in $x$.
- **The certificate’s own padding.** Contracted, it is accepted by both routes at a side
  $1.0988 \times 10^{-11}$ below its own, and it carries the separate wall slack of
  $2.398 \times 10^{-13}$ (F4). RV-3 bears only on sides like those, about $10^8$ times
  smaller than the gain, and this review registers nothing.
- **The maintained routes on the certificate itself** accept it as given; their least
  wall clearance, $21000000001021/10^{28}$, and least gap are this review’s exact
  values.

### Identity

`devtools.measure_identity` (`out/identity-n90.json`) measured the certificate against
the house and against the seed rebuilt below.

| Reference | Nearest centres one to one | Optimal assignment: beyond $10^{-3}$, $10^{-2}$, $10^{-1}$; largest move | Tilted squares |
| --- | --- | --- | --- |
| The house, the grid | under no symmetry | 90, 54, 52; 1.332 | all 44 paired with upright squares |
| The issue’s seed from de Winter’s 157 | under the identity | 90, 49, 2; 0.1457 | all 44 paired with tilted squares of the same sign |

A new arrangement relative to the only packing the record holds at 90, and the first at
90 with turned squares.

### Lineage

`l169_lineage.py` (`out/lineage-n90.json`) rebuilds the README’s construction in
binary64 from de Winter’s `n157_exact.json` as the T-293 packet retains it (SHA-256
`b6c28446…`, the bytes of `a491dad`, unchanged at `6617869`). The issue and README pin
`c70defa`, a later commit.
The GitHub API read of that file was refused for this session (“GitHub access to this
repository is not enabled”), and it was not retried another way, so the two copies were
not compared.

| Step | The README | Reproduced here |
| --- | --- | --- |
| The symmetry | none stated | the identity: one translation, binned to 0.1, carries 37 of de Winter’s turned squares onto the certificate’s; his pinwheel reads alike under its four rotations, and no mirror matches, his tilts being −24.02° to −27.54° |
| The motif | a crop “about 12.993303 units wide and 9.353384 units high” | the full width, from his bottom wall to the top of his square 103 (turned −24.65°) at 9.3533845, holding 107 squares wholly, 51 of them turned |
| The pitch | copies “offset horizontally by one unit … at a vertical pitch of 9.019403 units” | the least pitch at which the crop and a copy shifted by +1 have disjoint interiors is 9.019403129; shifted by 0 or −1 it is the crop’s height, 9.353384 |
| The window | “A square window across two copies supplied 90 pieces” | at the placement that fits the certificate, copy A at $(-2.99624, 0.00183)$ and copy B at A + (1, 9.019403), the box holds 91 centres, 82 and 9; the extra, a turned square of copy A, has its centre 0.112 inside the left wall and crosses it by 0.548. A side-10 window with its left edge 0.113 to 0.503 to the right holds exactly the other 90 |
| The fit | “Fitting their centers and orientations” | the certificate pairs one to one with those 90 under the identity: 49 squares move beyond $10^{-2}$ and 2 beyond $10^{-1}$ (largest 0.1457, square 58); 38 turn beyond 1°, at most 4.02°; the 44 turned squares, at −24.02° to −27.54° in the seed, end at −22.61° to −31.56° |

- **The seed is nearly a packing.** One pair overlaps by $1.2 \times 10^{-7}$, the pitch
  printed at six places being just below the least 9.019403129. Ten squares cross a
  wall: copy B’s nine across the top by 0.023, which the fit lowers from 9.5212 to
  9.4983, and one of copy A’s by 0.041; the fit brings every square inside the box of
  side $S$.
- **The certificate’s top row is copy B** (squares 82 to 90), the bottom row of de
  Winter’s 157 one unit to the right, and the rest is copy A.
- **So the construction holds as stated** (F11), with one detail the README leaves out,
  where the window sat.
  Whether the record has used a shifted periodic stack of a crop before was not searched
  here.

### Closed Forms

`l169_record.py` computes $S - (s(m) + j)$ for every reported $s(m)$ with $m < 90$ and
every integer $j \ge 0$.

- **No closed form.** None lies within $10^{-3}$ of the side.
- **The L step from the new side.** Widths 1 to 8 carry 90 to 109, 130, 153, 178, 205,
  234, 265 and 298, at sides 0.049 to 0.220 above the record there: the certificate
  moves no other count.
- **Monotonicity.** No reported $s(m)$ with $m < 90$ lies above $S$, so nothing below 90
  moves.

### Custody and Licence

`l169_custody.py` (`out/custody.json`) ran read-only plumbing (`rev-parse`, `log`,
`ls-tree`, `show`, `diff`, `status`) on the clone made for this review.
It records author names and times, not addresses.

- **Commits.** Three, all under one author name, within 46 seconds on 15 November: the
  initial commit (02:59:56Z, a README of 160 bytes); `e5c2ecc` (03:00:02Z), which adds
  five files and rewrites the README, with the credit “jazivxt and Codex Astra Ultra”;
  and the pin `179fcba` (03:00:42Z), which changes only `README.md` and `SHA256SUMS`,
  the credit now “jazivxt and GPT-6 Astra Ultra” (F13). The certificate’s blob,
  `9a07072`, is the same in both.
  The pin is the head, and the clone’s working tree equals it.
- **Dates.** Issue #989 was opened at 03:00:53Z, 11 seconds after the pin was committed,
  and labelled `intake`; it had no comments when fetched at 03:41Z. Git dates are the
  author’s own, and push times were not checked.
- **Digests.** `SHA256SUMS` lists all five files, and every digest holds.
- **The CSV** lists the 90 squares in certificate order, with centres within
  $8.2 \times 10^{-16}$ of the certificate’s and angles equal to $2\arctan t$ in degrees
  as printed.
- **Licence.** `DONOR-LICENSE.txt` is Joost de Winter’s MIT licence, byte-identical to
  the `LICENSE` this repository retains from his repository (SHA-256 `324f918c…`); the
  MIT terms ask copies of substantial portions to carry it.
  The repository states no licence for its own files, the certificate, CSV, figure and
  README (F12). The record has retained data from a repository that states no licence
  before, at Couzo’s issue #843.

Custody holds.

### The Author’s Checks

No checker is published at the pin.
Couzo’s `verify_bound_certificate.py`, the one the issue names, was read after the
freeze and not run.

- **Strict mode** accepts when the least wall margin is positive and every tested pair’s
  separation is positive, the open-container, disjoint-closed-squares contract of Evan
  Daniel’s verifier. Every decision is in `fractions`.
- **Its prefilter** skips pairs whose centres are more than $\sqrt 2$ apart, which is
  sound: their circumscribed discs are disjoint.
- **Its reader** splits lines, so CRLF is no obstacle, and skips blank and `#` lines.
- **The certificate’s shape is what strict mode needs:** no wall contact, a least
  clearance of $2.1 \times 10^{-15}$, every pair at least $1.19 \times 10^{-12}$ apart.
  That accounts for F4 and F5.

This review’s checker shares none of its code, and decides every pair without a filter.

### Significance

**S3**, a substantive case result.

- **The anchor.** A count whose best known packing was the trivial grid now has one
  below it, by $1.72 \times 10^{-3}$. The record has scored such firsts before, each S3:
  T-057 at 211 ($15^2 - 14$), T-220 at 183 ($14^2 - 13$), T-293 at 157 ($13^2 - 12$) and
  T-135 at 308 ($18^2 - 16$).
- **The conjecture it bounds.** Friedman’s survey reports the conjecture that
  $s(n^2 - n) = n$ “whenever $n$ is small”, with Cleemann’s $n = 17$ then its smallest
  counterexample. The record’s reported $s(n^2 - n)$ is $n$ for $n = 2$ to 10 and below
  $n$ for $n = 11$ to 18, and Kingbird credits Cantrell’s 2025 packing of 110 with
  bounding “the $s(n^2-n)=n$ conjecture to $n \lt 11$”. This packing bounds it to
  $n < 10$: the last $n$ with $s(n^2 - n) = n$ is at most 9.
- **The atlas’s target.** It answers the first target of Evan Daniel’s atlas, WISHLIST
  P1 “s(90) < 10”, which says it would show “The last k with s(k²−k) = k is ≤ 9 (now: in
  [3, 10] …)”. As T-057 moved the smallest $k$ with $s(k^2 - k + 1) < k$ from 16 to 15,
  scored S3, this moves the smallest $n$ with $s(n^2 - n) < n$ from 11 to 10.
- **At deficit 10** it is the first packing below $k$ for any $k \ge 10$: the record
  holds the grid at $n = k^2 - 10$ for $k = 10$ to 18. The staircase $c^*(10)$, on best
  known values, falls from 10 to 9.
- **Not S4.** One count, no technique shown to carry (no L step from it moves a count),
  no bound family and no disputed value resolved; whether $s(n^2 - n) = n$ for
  $4 \le n \le 9$ stays open.
  Not S5: no lower bound or optimum.
- **The catalogues at 90.** Friedman’s DS7 Table 1 (2009) and his Packing Center page
  list 90 to 97 at 10. Kingbird’s catalogue, captured on 30 September 2026, has no entry
  between 89 ($5 + \tfrac72\sqrt 2$, Stenlund 1980) and “98, 99”. Neither lists a
  packing below 10 at 90, and the case’s `catalogue_pictured` is false.

### Findings Added After the Freeze

| Id | Severity | Where | Finding |
| --- | --- | --- | --- |
| F8 | note (records) | `n-090.md`; the families | the record at 90 conflicts with nothing: reported and verified upper bound 10, lower bound 9.73 (T-091), T-212’s 9.78 held outside the lane; no family, theorem or entry claims $s(90) = 10$, since the $k = 10$ families have deficits 1 to 5; the gain is 0.001722833074 on both upper lanes |
| F9 | note (records, at adoption) | `n-090.md` | `conjectured_optimum: integer` is refuted, as the catalogue’s values at 260 and 299 were before it, where the field was set to null (the review of #984 and #985, F12); its prose (“no arrangement has ever been found that beats the trivial … grid”, “The record catalogue does not picture $n = 90$”) needs rewriting; the brief’s T-082 lower bound is stale, the case’s being T-091’s 973/100 |
| F10 | note (records) | the contraction | the house has no contraction margin (squares 1 and 2 touch), so RV-3 does not apply; the certificate contracts by $1.0988 \times 10^{-11}$ in side and has a further $2.398 \times 10^{-13}$ of wall slack, sides only RV-3 could register |
| F11 | note (records) | identity and lineage | a new arrangement relative to the grid; a refinement of the README’s seed, one to one under the identity, no square beyond 0.146; crop height, pitch and count reproduce from the T-293 bytes, and where the side-10 window sat is not stated; `c70defa`’s copy was not compared (API read refused) |
| F12 | note (author) | the repository | no licence for the author’s own files; `DONOR-LICENSE.txt` is de Winter’s MIT licence, byte-identical to the record’s copy |
| F13 | note (author) | `e5c2ecc` and the pin, `README.md` | the commit 40 seconds before the pin credits “Codex Astra Ultra”, the pin “GPT-6 Astra Ultra”; the record should credit as the issue asks, jazivxt and GPT-6 Astra Ultra |
| F14 | note (author) | `README.md`, “Coordinates and verification” | answers F6: “The origin is the lower left corner and positive θ rotates counterclockwise”, the reading this review used |

None changes a verdict.
F12 to F14 bear on the author’s words, and F8 to F11 on the record’s.

### Questions for the Author

1. Would you state a licence for the certificate, the CSV, the figure and the README
   (F12)?
2. The commit before the pin credits Codex Astra Ultra and the pin GPT-6 Astra Ultra.
   Is the issue’s credit, jazivxt and GPT-6 Astra Ultra, the one to record (F13)?
3. Where did the side-10 window sit?
   At the placement that fits your certificate the box holds 91 centres; a window 0.113
   to 0.503 to the right holds the 90 (F11).
4. Was de Winter’s `n157_exact.json` at `c70defa` the same file as at `a491dad` (SHA-256
   `b6c28446…`), the copy the record retains?
5. Were the $2.1 \times 10^{-15}$ wall offset and the $2.377 \times 10^{-13}$ slack at
   the right and top chosen for strict mode?
   The squares fit a box $2.398 \times 10^{-13}$ smaller (F4).
6. Would you publish the fitting step (its objective, optimiser and the conversion to
   rationals), and say whether the Kaggle leaderboard at 90 shows any side below yours?

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

*Added after the freeze*, none of them a decider of the certificate, run from `packing/`
of this review’s worktree (`main` at `a4f36ae70`), one at a time; the README lists the
commands. The devtools were run with `python -B` (not `-I`, which leaves `packing/` off
the module path); they are this repository’s own, run read-only, writing only to this
review’s packet.

| Program | Receipt | CPU |
| --- | --- | ---: |
| `l169_lineage.py` | `out/lineage-n90.json`, the seed in `out/lineage/seed-n90.cert` | under 1 s |
| `devtools.contraction_margin`, the certificate alone | `out/contraction-new-n90.json`: $1 - \lambda^* = 1.194485 \times 10^{-12}$ | 2 s |
| the same, the house against the certificate | `out/contraction-house-n90.json`: margin 0, `within_margin: false` | 1 s |
| `devtools.measure_identity`, against the house and the seed | `out/identity-n90.json` | under 5 s |
| `l169_record.py` | `out/record-n90.json` | under 5 s |
| `l169_custody.py` | `out/custody.json`, with `programs/issue-989.json` | under 1 s |
| `l169_digests.py` | `out/program-digests.json`: `ALL_FROZEN_DIGESTS_HOLD` (26 digests), `RERUN_REPRODUCES_EVERY_RECEIPT` | 17 s |

The frozen chain (self-test, check, plan facts, plan, controls, description), rerun into
scratch space after the freeze with the controls reading the kept plan, reproduced every
kept receipt in everything but its CPU seconds and the plan’s time of statement.

What went wrong after the freeze, and was redone:

- `l169_lineage.py` was written three times.
  The first version searched for two translations under the eight symmetries, and found
  one copy and a second only modulo the unit lattice of the upright squares.
  The second cut the band by centres, which gave 90 squares only by cutting it at the
  wrong height. The kept version builds the README’s construction literally, and found
  the crop’s height at the top of de Winter’s square 103. The first two wrote to the
  kept receipt paths and were overwritten.
  Between them, five short explorations from the command line (a tilted-only histogram,
  a listing of each square’s nearest image, two crop readings and the tops near
  9.353384) decided nothing and wrote nothing.
- The GitHub API read of de Winter’s `n157_exact.json` at `c70defa` was refused for this
  session; it was not retried another way.
- One `grep` for the Kingbird capture ran in the primary checkout after a `cd` to a
  wrong path failed; it read files and wrote nothing.
- `packing-validate --edit --jobs 2` (405 s wall) failed two steps and passed the rest.
  The browser floor failed because `npm ci` was not run in this worktree; no JavaScript
  changed here. The documentation check names this review an unmapped durable document:
  the document map is the import lane’s to update, as it was for the model review, and
  this lane makes no records edits.

## Relation to Earlier Reviews

- **The models**, L163’s review of #984 and #985 and L159’s review of #983, concern
  rational certificates by other authors.
  L163’s text, README and frozen digest lists, and the first 140 lines of L159’s text,
  were read before any program here was written; their programs, plans and receipts were
  not opened. This review follows their layout, their two methods’ ideas and their list
  of controls, adapted to a certificate that touches no wall: G5 first moves a turned
  square to its wall, G7 tests the text form in place of a twin, S1 finds the box the
  squares need, and S5 closes every pair, not only the near ones.
- **No earlier review of this certificate exists**, and the import lane’s work (L170)
  was not read. The reviews of T-191 and T-293, whose entries this review cites, were not
  read.

## Frozen Findings

The checker was frozen at 2026-11-15T03:19:25Z: `frozen/checker-frozen-digests.txt`
(list SHA-256 `998ff4ca…`) holds the source certificate’s digest, the seven checker
files’ and the two receipts they had written, pushed as `caaeeacf5`. The controls plan
was stated at 03:21:48Z: `frozen/controls-plan-digest.txt` (list SHA-256 `3782b4b4…`,
plan `71bee737…`), pushed as `9f874f2d0`. The findings were frozen at 03:28:11Z, before
the author’s README, checksums, CSV, figure or licence file, Couzo’s checker, the case
record, register entries, family entries and house witness at 90, de Winter’s 157, any
import lane’s work or this repository’s verifier, promotion, identity and contraction
code was opened: `frozen/findings-frozen-digest.txt` (list SHA-256 `23fdb0bd…`). The
frozen text is kept beside the programs as
`frozen/review-2026-11-15-jazivxt-989.frozen.md`: 481 lines and 33,903 bytes, SHA-256
`475fad339b0360c3db2b4747a333a5e42e1b1480a7ce8dc4599e108204c031d6`, committed and pushed
as `d20230eb6` before anything after it was written.
That text is everything here but the passages marked as added after the freeze, the
sections After the Freeze, Relation to Earlier Reviews and Frozen Findings, and the
closing comment.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
