# De Winter’s Certificate of #996: Stage 4 Mathematical Review

**Date:** 2026-11-15 UTC. **Subject:** a rational center-basis certificate of 90 unit
squares by Joost de Winter (Delft University of Technology), `n90/n90_exact.json`
(SHA-256 `3adcc363…`) and its Witness/v2 twin `n90/n90_witness.yaml` (`3a28f570…`), of
[JoostdeWinter/square-packing@64d5ee7](https://github.com/JoostdeWinter/square-packing/tree/64d5ee762a1159248d375973fb33825d51da637d),
issue [#996](https://github.com/jlevy/squares/issues/996), which claims
$s(90) \le 9.994038857546$.

The full digests are in the packet’s README and `frozen/checker-frozen-digests.txt`.

**Reviewed at:** `main` `91acf2022`, and the pin above.

**Reviewer:** Claude (AI review), strong tier (`tbd-strong`, not the `tbd-strong-max`
tier the runbook names), at the reasoning setting its launcher chose, the stage 4
mathematical review lane (L180), separately prompted.
It read the source as data and ran only programs of its own, kept with their receipts in
[`packing/resources/web/de-winter-996-review-2026-11-15/`](../../../packing/resources/web/de-winter-996-review-2026-11-15/README.md).
Its checker is a clean-room implementation written for this review: it reuses no code
from any earlier review.
It took the review of #989 by lane L169 and the review of #977 and #979 by lane L153 as
the model for method, controls, freeze protocol and layout, read their texts and their
packets’ READMEs, and did not open the programs of either, or of any other review.
It is not a human oversight record.

## Summary for the Author

**Verdict on the bound: accepted.** No finding is blocking or major.

| n | Issue | Squares | Pairs | Wall contacts | Least pair gap | Least positive wall clearance | Verdict |
| ---: | --- | ---: | ---: | --- | --- | --- | --- |
| 90 | #996 | 90 | 4,005 | 18 (9 left, 9 bottom) | $1.06410 \times 10^{-12}$ (2, 40) | $5.0739 \times 10^{-21}$ (15 squares, right and top) | accept |

- **How the bound was checked.** A clean-room exact checker, written and frozen for this
  review before your README, registration, checksums, figures, your two checkers or this
  repository’s witness code (`check_rational_witness_independent` among it) was read,
  decided both files: every square, every wall and every pair, with no distance filter,
  by two methods that share only the reader.
  They are separating axes in plain Python integers, from the JSON file’s centres and
  edge directions, and exact convex clipping in GMP rationals of the twin’s own corners,
  which computes the intersection of each pair, and of each square with the outside of
  each wall. They agree on all 4,005 pairs and all 360 square–wall pairs.
  The reader shows that the twin holds exactly the JSON file’s packing, corner for
  corner.
- **Controls.** All 26 controls stated in advance came out as stated.
  Reading the rotation the other way breaks the file (52 overlapping pairs).
  Turning square 10, which touches the bottom wall, by $10^{-30}$ in $\tan(\phi/2)$
  frees its corner one way and pushes it out the other.
  Lowering the side by one unit of its own last place pushes out exactly the 15 squares
  at the right and top.
  Every one of the 4,005 pairs was closed along its centre line to exact contact and
  $10^{-30}$ past it, and every square was taken to its nearest wall and past it, by
  both methods.
- **The claim’s box.** The same squares in the box of the claimed side, 9.994038857546,
  are accepted by both methods (control S1e), so the certificate proves the claim as
  printed. The 12-place floor, 9.994038857545, is refused (S1f).
- **The side is not the extent.** 18 corners lie exactly on the left and bottom walls,
  and no square touches the right or top: 15 squares clear them by
  $5.07389735200 \times 10^{-21}$. The squares fit the box of side
  $S - 5.07389735200 \times 10^{-21}$ (S1c), and the side is that extent rounded up at
  20 places. Nothing in the bound depends on it.
- **The arrangement.** No square is exactly upright: 50 share one direction, turned
  clockwise by $1.83 \times 10^{-10}$ degrees, and 40 are turned clockwise by 22.90° to
  30.99°. The near pairs form a contact arrangement opened by $1.06 \times 10^{-12}$ to
  $9.20 \times 10^{-12}$: 195 pairs, and then none below $5.8 \times 10^{-6}$. Your
  “smallest gap of 1e-12 between squares” holds.

## Scope

**Read.**

- Issue #996 through GitHub (fetched at about 12:00Z, before any program was written,
  and again at 12:12Z for the copy kept in the packet; no comments, the label `intake`;
  never edited here).
- `n90/n90_exact.json` and `n90/n90_witness.yaml` at the pin, as data; the clone’s
  commit list (hashes, dates and subjects), the file lists of the pin and of the head
  `9cafa33` with blob ids and sizes, and the names of the files that differ between
  them.
- On `main`: `packing/witnesses/witness.schema.yaml`, for the format’s keys and meaning;
  `packing/campaign/result-import.md` stage 4; and, to place this review’s files, the
  Ruff and BasedPyright exclusions of `packing/pyproject.toml`. None of it is witness,
  verifier or promotion code.
- The models: the review of #989 by lane L169,
  `docs/project/reviews/review-2026-11-15-jazivxt-989.md`, its packet’s README and its
  three frozen digest lists; and the review of #977 and #979 by lane L153,
  `docs/project/reviews/review-2026-11-14-de-winter-977-979.md`, its packet’s README and
  the first lines of its checker digest list.
  Not their programs, plans or receipts.
- The bead `think-uhav` and the header of its parent epic.

**Run.** Eleven Python programs and modules of my own, importing nothing from this
repository or the source ([What I Ran](#what-i-ran)). They decide the certificate twice,
run a self-test, compute the facts the controls are stated from, state the controls, run
them, and describe the file.

**Seen before my findings were written**, disclosed as the runbook asks:

- the lane’s brief, which states the pin, the two files, the head `9cafa33d43f6` and
  that the files are unchanged there, the claim and its exact side, that it improves
  T-303 (jazivxt, #989, adopted at 90 on 15 November, 9.998277166926) by 0.00424 by a
  local search from T-303, the public submission at 9.998277166917 as context, that the
  author ran `check_rational_witness_independent`, the contraction margin the #989
  review measured on T-303 ($1.0988 \times 10^{-11}$, wall slack included), and the
  checks to make after the freeze;
- the issue, which states the claim, the exact side, the record at 90, the gain, the
  certificate’s files, the author’s two checkers and what they report (90 squares and
  202 close pairs, pairs with centres closer than $\sqrt 2$), the project checker’s
  “VERIFIED: 90 squares, 4005 pairs”, a schema validation with 0 errors, a numerical
  linear program finding no first-order improvement above $4 \times 10^{-10}$, a
  smallest gap of $10^{-12}$, the lineage (T-303, itself a crop of the author’s 157,
  T-293), that T-303 has 49 leaning squares and the new packing 37, that seven squares
  in the upper left have a new angle and five along the left wall are axis-aligned, and
  the AI assistance (GPT-6.1 Sol Max for the local search, Claude Fable 5.2 for the
  optimization, certificate, checks and figures);
- the model reviews named above.
  The review of #989 describes T-303’s certificate at length: its tilts, near pairs,
  wall clearances and construction.
- the subjects of the author’s three commits of 15 November, among them “Name GPT-6.1
  Sol Max as the model that ran the local search for n = 90”.

**Not read before my checker was frozen** (2026-11-15T12:12:15Z) **or my findings were
frozen**: the author’s `n90/README.md`, `REGISTRATION.md`, `SHA256SUMS`,
`verify_exact.py`, `check_area.py`, `n90_before_after.png` and `n90_record.png` (all
identified only by their blob ids in the tree listing), and the repository’s `README.md`
and `LICENSE`; this repository’s `sqpack` witness, verifier and promotion code, its
devtools that read witnesses (`check_rational_witness_independent` among them), and the
Rust crates; the register entries, case record and house witness at 90, T-303’s
certificate and its import packet; the import lane L181 and its branch; and the model
reviews’ programs.

**Not run here.** Any of the author’s code, `check_rational_witness_independent`, or the
maintained routes.

## The Claim and What It Needs

Issue #996 claims $s(90) \le C = 9.994038857546$, the 12-place print of the
certificate’s side $S = 199880777150913904183/20000000000000000000$, rounded up.
The certificate proves $s(90) \le S$: there are 90 closed unit squares, rotated freely,
with pairwise disjoint interiors inside the closed square $[0, S]^2$. The claim follows
when $C \ge S$, and directly when the same squares are accepted in $[0, C]^2$.

The JSON file is the author’s own format: `n`, `side`, `square_size: "1"`, a `format`
line, and `squares`, each `[center_x, center_y, cos, sin]` as exact rationals, where
`(cos, sin)` is “the unit direction of one edge”.
A square with centre $C$ and edge direction $u = (c, s)$ is read as
$\{C + x u + y v : \lvert x\rvert, \lvert y\rvert \le
1/2\}$ with $v = (-s, c)$. The twin is a Witness/v2 file with `representation: corners`,
`scalar.kind: rational`, `origin: lower-left` and `axes: x-right-y-up`: four rational
corners per square.

The hypotheses are six:

1. **The reading.** The JSON file has exactly the five keys above, `n` an integer, every
   scalar a canonical $p$ or $p/q$ with $q \ge 2$, $\gcd(\lvert p\rvert, q) = 1$, no
   sign on zero and no leading zero; no floats, constants, duplicate keys, tabs or
   carriage returns. The twin is one YAML document with no anchors, aliases, explicit
   tags or duplicate keys, holding only strings, plain decimal integers, mappings and
   sequences; its envelope is `packing.squares:Witness/v2`, its keys lie inside the
   schema’s lists with every required key present, and its squares are `square-1` to
   `square-90` in order, each with four corners of two canonical scalars.
2. **The count and the twin.** 90 squares.
   The twin’s $n$, side and side text are the JSON file’s, and each square’s four
   corners are $C \pm u/2 \pm v/2$ of the JSON pose, listed as a cyclic rotation of them
   in either sense.
3. **Unit squares.** $c^2 + s^2 = 1$ exactly, and the corners form a unit square.
4. **Containment.** Each square lies in $[0, S]^2$. The JSON file does not say where the
   box is; the twin says the origin is the lower-left corner (F7).
5. **Disjoint interiors.** No two squares’ interiors meet.
6. **The rotation sense.** $(c, s)$ is read as an angle counterclockwise from the
   $x$-axis, $x$ to the right and $y$ up; control G6 shows that reading it the other way
   changes the verdict, and controls G5a and G5b that the sense is decided at a single
   square on a wall.

`l180_check.py` decides the first two through the reader, and the next three twice.

- **Method A** (`l180_axes.py`, Python integers) reads the JSON poses and never a
  corner. Each square’s centre is written over one denominator $E$, $C = (X, Y)/E$, and
  its edge direction over one denominator $r$, $u = (a, b)/r$; the square is accepted
  when $r > 0$ and $a^2 + b^2 = r^2$. On a unit normal of either square of a pair,
  square $i$ projects to an interval of half-length $1/2$ and square $j$ to one of
  half-length $(\lvert\cos D\rvert + \lvert\sin D\rvert)/2$, $D$ the angle between them,
  the same on all four normals; the gap is the centre separation along the normal less
  both half-lengths, an exact distance.
  All four gaps of a pair share the denominator $2 E_i E_j r_i r_j$, so the margin,
  their maximum, is decided on integers and kept as an exact fraction: positive is
  apart, zero is contact with disjoint interiors, negative is overlap.
  Two convex polygons with disjoint interiors are weakly separated by a line parallel to
  an edge of one of them, so the three signs are exactly those three classes.
  A wall’s clearance is the signed distance from the square’s extreme corner to it, from
  the half-extent $(\lvert a\rvert + \lvert b\rvert)/(2r)$.
- **Method B** (`l180_clip.py`, `gmpy2.mpq`) is handed corners and nothing else: for the
  certificate, the twin’s own corners; for a modified certificate in the controls, the
  corners the reader derives from the modified poses.
  Four points are a unit square in cyclic order when all four sides have squared length
  1 and both diagonals squared length 2; the sign of the shoelace sum ($\pm 2$) gives
  the listing’s sense, and a clockwise listing is reversed before clipping.
  A pair is decided by clipping one square against the four closed half-planes to the
  left of the other’s counterclockwise edges (Sutherland–Hodgman, keeping boundary
  points), so the result is the intersection exactly; it is clipped both ways round, and
  the two results must agree in class and area.
  Empty is apart; non-empty with zero area is contact, since the interior of an
  intersection of convex sets is the intersection of their interiors; positive area is
  overlap, by that area.
  Each wall is classed the same way, by clipping the square against the closed
  half-plane outside it, and containment is decided separately: a unit square lies in
  the box exactly when its intersection with the box has area exactly 1.

The two share only the reader (`l180_reader.py`), which hands them exact rationals; the
reader is also the one place a pose is turned into corners.
The verdict is `ACCEPT` only when the twin holds exactly the JSON file’s packing, and
both methods accept every square, wall and pair with equal classes everywhere;
`l180_decide.py` runs both over every square, wall and pair.

## The Certificate Decided

| Quantity | 90 |
| --- | --- |
| Scalars read, all canonical | the JSON file’s side and 360 square scalars; the twin’s side and 720 corner coordinates, 18 of them written `'0'` |
| The side | $199880777150913904183/20000000000000000000$, exactly 9.99403885754569520915 |
| The twin | the JSON file’s $n$, side and squares exactly; all 90 squares listed counterclockwise from $C + (u + v)/2$ |
| Squares, unit by both methods | 90 of 90, all listed counterclockwise |
| Pairs decided, apart by both methods | 4,005 of 4,005; none touches |
| Sum of all pair overlap areas (method B) | exactly 0 |
| Least pair margin | $1.06410355706 \times 10^{-12}$, squares 2 and 40 |
| Positive pairs below $10^{-12}$, $10^{-11}$, $10^{-6}$, $10^{-3}$, $10^{-1}$ | 0, 195, 195, 201, 243 |
| Wall contacts | 18: left 57 to 63, 71 and 88; bottom 10, 23, 28, 32, 33, 47, 48, 59 and 75 (square 59 at both) |
| Least positive clearance at each wall | left 0.644 (56); bottom 0.594 (45); right $5.07389735200 \times 10^{-21}$ (11, 31, 34, 35, 47, 49, 55, 83); top the same (82 to 86, 88 to 90) |
| The packing’s width in $x$ and in $y$ | each $S - 5.07389735200 \times 10^{-21}$ |
| Verdict | `ACCEPT` |

- **Reading.** Both files read strictly.
  The JSON file has no integer scalar; the twin writes 18 corner coordinates as the
  quoted string `'0'`, and its envelope is `packing.squares:Witness/v2`, its id
  `W-n90-de-winter`, its claim `coordinate_provenance: reported`,
  `method: exact-algebraic`, with no `certificate` record.
- **The twin.** For every square the twin lists the corners
  $C + (u + v)/2, C + (-u + v)/2, C + (-u - v)/2, C + (u - v)/2$ of the JSON pose, in
  that order, exactly.
- **Squares.** Every square is a unit square by both methods.
- **Walls.** Every square lies in its box by both methods, with area exactly 1 inside,
  and their classes agree on all 360 square–wall pairs.
  18 square–wall pairs touch, each at a single corner written exactly as 0 in the twin:
  nine at the left (57 to 63, 71, 88) and nine at the bottom (10, 23, 28, 32, 33, 47,
  48, 59, 75), square 59 at both by two different corners.
  No square touches the right or top wall.
  Every square at a wall, and every square near the right or top, is one of the 50
  near-upright squares below.
- **Near the right and top.** 16 square–wall pairs, of 15 squares, clear the right or
  top wall by exactly
  $9909955765625015940074994030630443123/1953125000000000000000004987507812500000000000000000000000
  = 5.07389735200 \times 10^{-21}$: squares 11, 31, 34, 35, 47, 49, 55 and 83 at the
  right, and 82 to 86 and 88 to 90 at the top, 83 at both.
  The next clearance is $9.91 \times 10^{-4}$ (square 67, right).
- **The side and the extent.** The left and bottom walls are touched, so the packing’s
  width is $S - 5.07389735200 \times 10^{-21}$ in both directions,
  9.994038857545695209144926102647 to 30 places.
  The side is a multiple of $1/q = 5 \times 10^{-20}$ less than $1/q$ above that width:
  it is the width rounded up at 20 places (F4).
- **Near pairs.** The 195 pairs below $10^{-9}$ lie between
  $1.06410355706 \times 10^{-12}$ and $9.19676800001 \times 10^{-12}$, median
  $6.16 \times 10^{-12}$, in 141 distinct exact values; the commonest is
  $6.00000 \times 10^{-12}$ (16 pairs).
  One normal binds in 58 of them and two in 137. The next pair is
  $5.84765 \times 10^{-6}$ (squares 5 and 18), then $1.16 \times 10^{-5}$ (66, 70): the
  certificate is a contact arrangement opened by about $10^{-12}$ to $10^{-11}$ between
  squares, and closed exactly at the left and bottom walls (F5).
- **Tilts.** No square is exactly upright.
  50 squares share one exact direction,
  $(249999999999999999999999361599, -799000000000000000)/250000000000000000000000638401$,
  the rational direction of $t = \tan(\phi/2) = -799/(5 \times 10^{14})$: a clockwise
  turn of $3.196 \times 10^{-12}$ radians, $1.831 \times 10^{-10}$ degrees.
  The other 40 are turned clockwise by 22.896830° to 30.993239°, in 13 distinct angles
  to six places: 14 at −22.896830°, 7 at −24.051775°, 3 each at −25.220522° and
  −24.341355°, 2 each at −27.799612°, −25.116436°, −23.086558°, −27.393256° and
  −30.993239°, and one each at −23.948575°, −24.532308° and −23.350830°. Squares 21 and
  42 carry −25.116436° under two exact orientations about $5 \times 10^{-16}$ radians
  apart, so there are 14 exact orientations in all (F6).

The least margin and clearances are exact fractions in the receipts; the prints here are
rounded.

`l180_selftest.py` holds both methods, the closed form and the reader to 31,771 checks
and passes:

- edge-to-edge contacts of two parallel squares, upright, turned by $(3/5, 4/5)$ and by
  $(5/13, 12/13)$, across each of the four edges with an offset of 0 and $1/3$ along the
  edge, and corner-to-corner contacts along each of the four diagonals; a 3-4-5 and a
  5-12-13 corner on an upright edge under each quarter turn of the plane; each at a gap
  $\delta$ of $10^{-30}$, 0 and $-10^{-30}$, with both squares under all four equivalent
  edge directions and in both orders.
  The margin is $\delta$ in all of them, by method A and by the closed form, and the
  overlap areas, derived by hand, are $\lvert\delta\rvert(1 - \tau)$ for an offset
  $\tau$, $\delta^2$, $\tfrac{25}{24}\delta^2$ and $\tfrac{169}{120}\delta^2$;
- duplicates at three angles (margin $-1$, area 1), and an upright square against its
  concentric rotation by $(3/5, 4/5)$ and by $(5/13, 12/13)$: margin
  $-(1 + c + s)/2 = -6/5$ and $-15/13$, area $1 - (c + s - 1)^2/(2cs) = 5/6$ and
  $13/15$;
- each wall at $10^{-30}$ inside, at contact and $10^{-30}$ out, for squares at four
  angles under their four edge directions, with B’s containment test;
- the unit test and listing sense at three angles under each quarter turn, both senses,
  and at $t = 10^{-30}$; five directions method A must refuse and seven shapes method B
  must refuse;
- 300 random rational pairs with Pythagorean directions, on which method A’s margin must
  equal the closed form of `l180_geom.py` (corner projections, not half-extents) both
  ways round and method B’s class its sign; 300 more closed along their centre line to
  $10^{-30}$ short of contact, to it and $10^{-30}$ past it, with margins exactly
  $10^{-30}$, 0 and $-10^{-30}$ by both A and the closed form and B’s class to match;
  300 random turned squares taken to a wall, short of it, at it and past it;
- 30 malformed JSON texts and 20 malformed twins the reader must refuse, each for its
  own reason, valid files it must read and write back, and six twin comparisons
  (agreeing, started at another corner, reversed, a corner off by $10^{-30}$, two
  corners swapped, and a different side); and four whole-file decisions: a $2 \times 2$
  grid with six touching pairs and eight wall contacts, a duplicate, a box $10^{-30}$
  too small, and a 3-4-5 square touching all four walls.

Three deliberately broken copies fail it: method A using only square $i$’s two normals
(640 failures), method A counting a zero margin as apart (1,408), and method B clipping
with open half-planes (1,472).

## Controls

`controls-plan.json` states 26 controls and the outcome of each.
It was written and hashed (`31a2b551…`, 2026-11-15T12:15:57Z) before `l180_controls.py`
existed, from the check receipt and from `l180_plan_facts.py`, which computes every
margin, clearance, closing move and turned pose by the closed form of `l180_geom.py`
(corner projections in fractions, a third formulation, apart from both methods) and runs
neither method. That program first recomputed every margin and clearance of the
certificate by the closed form: the SHA-256 of both exact lists equals method A’s.
“Contact” is a margin or clearance of exactly 0, and “past” is $10^{-30}$ beyond it.

Every whole-file control was decided by both methods over every square, wall and pair,
after the modified certificate was written as JSON text and read back through the
reader; G3 and G4 stop at the reader.
The twin controls G7a to G7d write the modified twin as YAML text, read it back and
compare it with the JSON file; G7a, G7c and G7d then decide the JSON poses by method A
and the modified twin’s corners by method B.

| Control | Stated | Outcome |
| --- | --- | --- |
| G1. Square 90 given square 1’s centre and direction | refused: exactly the pair (1, 90) overlapping, margin $-1$, area 1; no other pair touches or overlaps; wall contacts unchanged | as stated |
| G2. Square 1 translated by $(S, 0)$ | refused: square 1 across the right wall by both (clearance $-6.994$, the plan’s exact value), its area inside the box 0; no pair touching or overlapping | as stated |
| G3. Square 90’s entry deleted | the reader refuses: $n$ is 90, 89 entries | as stated |
| G4. The side written as $2p/2q$ | the reader refuses: not in lowest terms | as stated |
| G5a. Square 10, the lowest-numbered square on exactly one wall (bottom), turned about its centre by $t = +10^{-30}$ | accepted, its bottom clearance exactly the plan’s $+1.0 \times 10^{-30}$; that contact gone, no other class changed | as stated |
| G5b. The same with $t = -10^{-30}$ | refused, square 10 across the bottom wall by exactly the plan’s $-1.0 \times 10^{-30}$; no pair changes class | as stated |
| G6. Every $(c, s)$ read as $(c, -s)$ (the rotation read the other way) | refused for exactly the plan’s 52 overlapping pairs, none touching; the exact clearance list unchanged | as stated |
| G7a. The twin’s first corner of square 1 moved by $10^{-30}$ in $x$ | the twin differs at square 1 alone; method B refuses square 1 of the twin as not a unit square | as stated |
| G7b. The twin’s side numerator raised by 4 (…187, still in lowest terms) | the reader reads it, and the twin differs in its side | as stated |
| G7c. Every square of the twin listed clockwise | the twin agrees (each the JSON corners from the fourth, reversed); accepted, margin and clearance lists unchanged, all 90 read clockwise by B | as stated |
| G7d. Every square of the twin listed from its second corner | the twin agrees; accepted, lists unchanged | as stated |
| G8. Every square transposed, $(x, y, c, s) \to (y, x, s, c)$ | accepted, the margin list unchanged, the clearances transposed | as stated |
| G9. Every edge direction replaced by the other, $(-s, c)$ | accepted, margin and clearance lists unchanged | as stated |
| G10. Every edge direction negated | the same | as stated |
| G11. The packing turned a quarter about the box centre, $(x, y, c, s) \to (S - y, x, -s, c)$ | accepted, the margin list unchanged, the clearances turned | as stated |
| G12. Square 1’s $s$ raised by $10^{-30}$ | refused: square 1 not a unit square by either method | as stated |
| S1a. The side lowered by $1/q = 5 \times 10^{-20}$, one unit of its own last place | refused: exactly the 16 right and top clearances of $5.07 \times 10^{-21}$ crossing (15 squares, 83 at both); the left and bottom contacts unchanged | as stated |
| S1b. The side lowered by $10^{-30}$ | accepted, no new contact | as stated |
| S1c. The side lowered by the least right-or-top clearance | accepted, exactly those 16 square–wall pairs touching, with the 18 at the left and bottom | as stated |
| S1d. That, less $10^{-30}$ more | refused, exactly those 16 crossing | as stated |
| S1e. The side set to the claim, 9.994038857546 | accepted; wall contacts only at the left and bottom | as stated |
| S1f. The side set to its 12-place floor, 9.994038857545 | refused: the 16 of S1a crossing | as stated |
| S4c. Square 40 moved toward square 2 along their centre line to exact contact | that pair alone touching by both, margin exactly 0, B area 0; accepted | as stated |
| S4p. The same, $10^{-30}$ past | that pair alone overlapping by both, margin exactly $-10^{-30}$ | as stated |
| S5. Every pair closed along its centre line (pair-level) | touching at contact by both, overlapping past; margins exactly 0 and $-10^{-30}$ by A and the closed form; the closing times’ digest the plan’s | 4,005 of 4,005 |
| S6. Every square moved to its nearest wall by its clearance (square-level) | contact at, crossing past, by both; clearance exactly 0 and $-10^{-30}$; inside by B’s area at contact, not past | 90 of 90 |

All 26 came out as stated: `EVERY_CONTROL_AS_STATED`.

- **G5.** The certificate touches walls, so the rotation sense is tested where it binds.
  The plan took the lowest-numbered square touching exactly one wall whose other
  clearances and margins exceed $10^{-20}$: square 10, on the bottom wall at one corner,
  its least margin $6.0 \times 10^{-12}$. Turning it by $t = +10^{-30}$ lifts that
  corner by $9.99999999997 \times 10^{-31}$, and $t = -10^{-30}$ pushes it out by as
  much.
- **G6.** The least margin of the reflected file is $-2.85 \times 10^{-1}$ (squares 22
  and 56).
- **S1.** The side’s denominator is $2 \times 10^{19}$, so one unit of its last place is
  $5 \times 10^{-20}$, about ten times the right and top clearances.
  S1c finds the box the squares need, $S - 5.07389735200 \times 10^{-21}$; with the left
  and bottom already touched, no translation is needed.
  The claim is $3.0479085 \times 10^{-13}$ above the side and the 12-place floor
  $6.9520915 \times 10^{-13}$ below it.
- **S4.** The plan took the tightest pair whose closing move, $10^{-30}$ past contact,
  is shorter than every other margin and every clearance of the moved square, compared
  exactly through squares of lengths.
  The tightest pair, (2, 40), passes with square 40 moving: its move is
  $1.078 \times 10^{-12}$, its next margin $5.207 \times 10^{-12}$ and its least
  clearance 1.0.
- **S5.** All 4,005 pairs, not only the near ones, were closed along their centre lines.
  The plan moved the higher-numbered square toward the other to the time
  $\max_w (g_w - m^*)/\lvert w \cdot d\rvert$ over the normals with a rate, $g_w$ the
  gap on normal $w$ and $d$ the centre difference, which makes the margin exactly $m^*$
  ($0$ or $-10^{-30}$) whatever the other normals do; the controls’ closing times
  reproduce the plan’s digest.
- **G8 to G11.** The transposed, re-based, negated and turned files’ margins equal the
  original’s exactly (the SHA-256 of the margin list is the same), and G9 and G10 leave
  the exact clearance list unchanged, which holds each method to the symmetries it
  should have.
- **S6.** The nearest walls are the left for 22 squares, the bottom for 23, the right
  for 24 and the top for 21; 17 squares already touch theirs.

## What This Review’s Checker Shares

- **With other checkers.** It shares no code with any other checker, and it was written
  and frozen before the author’s checkers, `check_rational_witness_independent`, or any
  of this repository’s witness, verifier or promotion code was read.
  It reuses nothing of any earlier review’s programs, none of which it opened.
  Its two methods follow the mathematics the models’ texts describe: separating axes in
  integer arithmetic over per-square denominators, with one half-extent for all four
  normals of a pair, and exact clipping of corners with a sides-and-diagonals unit test,
  wall classes by clipping against each wall’s outer half-plane and containment by area.
  It implements them afresh.
  Unlike the models, method B is handed the twin’s own corners rather than corners
  derived from the poses, so the two methods read different files and the reader’s exact
  comparison joins them.
  Its controls follow the models’ list, with G5 a rotation at a square on a wall, G7
  recast as four controls of the twin, G12 the non-unit direction of the model of #977,
  S1 extended to the claim and its floor, and S5 widened to every pair.
  It shares the mathematics above and the format’s meaning (centre and edge direction
  counterclockwise, the lower-left origin, the box $[0, S]^2$), taken from the format
  line, the twin, the schema text and the model reviews.
- **Its trust base.** CPython 3.14.7’s integers and `fractions`, GMP 6.3.0 through
  `gmpy2` 2.3.1, PyYAML 6.0.3 for parsing and composing the twin only, the standard
  `json` module, and the facts its self-test exercises.
  Its two methods share the reader and nothing else.
- **Authorship.** The issue credits GPT-6.1 Sol Max with the local search and Claude
  Fable 5.2 with the local optimization, the rational certificate, the checks and the
  figures, under the author’s direction.
  This review was written by a Claude agent, as were both model reviews; the
  independence claimed here is of code and of what was read.

## Findings

| Id | Severity | Where | Finding |
| --- | --- | --- | --- |
| F1 | note | `n90/n90_exact.json`, `n90/n90_witness.yaml` | an exact packing of 90 squares at its side, by both methods, every wall and pair; every pair strictly apart; 18 wall contacts at single corners, nine at the left and nine at the bottom; the twin holds the JSON file’s packing exactly |
| F2 | note | the controls | all 26 stated controls came out as stated |
| F3 | note | the claim | the squares are accepted in the box of the claimed side, 9.994038857546, the side’s 12-place ceiling, and refused in the box of its floor |
| F4 | note (records) | `n90_exact.json`, `side` | the side is not the packing’s extent: the right and top walls are cleared by $5.07389735200 \times 10^{-21}$ by 15 squares, and the squares fit the box of side $S - 5.07389735200 \times 10^{-21}$ (S1c), not $10^{-30}$ less (S1d); the side is the extent rounded up at 20 places |
| F5 | note (records) | the near pairs | a contact arrangement opened between squares: 195 pairs from $1.06410 \times 10^{-12}$ to $9.19677 \times 10^{-12}$, then $5.85 \times 10^{-6}$; the 18 wall contacts are exact; how this bears on the record’s padding question is measured after the freeze |
| F6 | note (author) | the issue, “Lineage and credit”; the tilts | no square is exactly upright: 50 share one direction turned $1.831 \times 10^{-10}$ degrees clockwise and 40 are turned clockwise by 22.90° to 30.99°; the issue’s counts of 37 leaning squares and of five axis-aligned squares along the left wall do not match these at face value, and are compared with T-303 after the freeze |
| F7 | note (author) | `n90_exact.json`, line 5 (`format`); `n90_witness.yaml` | the JSON `format` line names the scalars but not the box or the sense of the angle; the twin fixes both (`origin: lower-left`, `axes: x-right-y-up`), and G6 shows the sense matters (52 overlapping pairs) |

**F1. Feasibility.** The JSON file is an exact packing at its side: 4,005 pairs, each
decided by both methods with equal classes and strictly apart, and every square a unit
square inside its box by both, 18 of them touching a wall at one corner.
The twin is the same packing, corner for corner, listed counterclockwise from
$C + (u + v)/2$. The bound $s(90) \le S$ holds.

**F2. Controls.** As [Controls](#controls) gives them: 26 of 26 as stated, including the
rotation read the other way, the rotation sense at a square on a wall, four changes to
the twin, the side lowered by $1/q$, every pair closed to exact contact and past it
along its centre line, and every square taken to its wall and past it.

**F3. The claim.** $C = 9.994038857546$ is the ceiling of $S = 9.99403885754569520915$
at 12 places, $3.0479085 \times 10^{-13}$ above it.
Control S1e decides the claim directly: in the box of side $C$ the squares are accepted
by both methods. Control S1f shows that the floor, 9.994038857545, would not do: the 15
squares at the right and top cross it.

**F4. The side and the extent.** The left and bottom walls are touched exactly; the
right and top are cleared by $5.07389735200 \times 10^{-21}$, a tenth of a unit of the
side’s last place. The squares therefore fit the box of side
$S - 5.07389735200 \times 10^{-21} = 9.994038857545695209144926102647\ldots$, accepted
by both methods with contacts at all four walls, and not that box less $10^{-30}$. The
certificate proves a bound $5.1 \times 10^{-21}$ below the side it states; the claim is
the side’s 12-place ceiling either way, and nothing needs correcting.

**F5. Margins of $10^{-12}$.** Of the 195 near pairs, the least is
$1.06410355706 \times 10^{-12}$ at (2, 40) and the greatest
$9.19676800001 \times 10^{-12}$ at (14, 55) and (29, 36); the next pair is
$5.85 \times 10^{-6}$ (squares 5 and 18). The issue’s “smallest gap of 1e-12 between
squares” holds as a lower bound.
Unlike the near pairs, the 18 wall contacts are not opened: each is a corner written
exactly as 0.

**F6. The tilts.** The issue says T-303 has 49 leaning squares and the new packing 37,
and that five squares along the left wall are axis-aligned.
In the file no square is exactly upright: 50 squares, among them all nine at the left
wall, share the direction of $t = -799/(5 \times 10^{14})$, turned clockwise by
$1.831 \times 10^{-10}$ degrees, and 40 are turned clockwise by 22.90° to 30.99°. A
threshold anywhere between those two tilts counts 40 leaning squares, and a smaller one
counts 90; none counts 37. The counts are compared with T-303 after the freeze.

**F7. The box and the rotation sense.** The JSON `format` line says “each square:
[center_x, center_y, cos, sin] as exact rationals; (cos, sin) is the unit direction of
one edge”, and names neither the container nor the sense of the angle.
The twin does: the origin is the lower-left corner and the axes are $x$ to the right and
$y$ up, the reading under which both files are accepted.
G6 shows that the sense matters.
A sentence in the `format` line naming $[0, S]^2$ and the counterclockwise sense would
close the question for a reader of the JSON file alone.

None changes a verdict; all are notes.

## Verdict

**Accepted as an upper bound.** The certificate proves $s(90) \le S$ at its side
exactly, and the issue’s claim $s(90) \le 9.994038857546$ is decided directly by both
methods (S1e).

- Every hypothesis holds exactly, for every square, wall and pair, by two methods that
  agree everywhere, and the twin holds exactly the JSON file’s packing.
- Every control is decided as stated beforehand.
- No defect of the certificate or of its mathematics is open; every finding is a note.

Mapped as an adversarial review with verdict `accepted`, it supports `V3` and `C3` at
90, provided `l180_check.py`’s run is registered as exact-algebraic evidence replayed
here with full coverage of the certificate.
That reads as confirmed, independently re-implemented, clean room, by a Claude agent.
`V4` and `C4` would need a second accepted adversarial review by a distinct reviewer and
a human oversight record.

## What I Ran

All with CPython 3.14.7 (`uv run --frozen --all-extras --group dev python -I -B`, from
`packing/` of a worktree of `main` at `91acf2022`) under `nice -n 19`, one process at a
time. The programs, the frozen files and the receipts are in
[`packing/resources/web/de-winter-996-review-2026-11-15/`](../../../packing/resources/web/de-winter-996-review-2026-11-15/README.md).

| Program | Receipt | CPU |
| --- | --- | ---: |
| `l180_selftest.py` | `out/selftest.json`: `PASSED`, 31,771 checks | 4.8 s |
| `l180_check.py` | `out/check-n90.json`: `ACCEPT` | 0.7 s |
| `l180_plan_facts.py` | `out/plan-facts-n90.json`, kept as written before the plan | 4.9 s |
| `l180_make_plan.py` | `programs/controls-plan.json` | under 1 s |
| `l180_controls.py` | `out/controls-n90.json`: 26 of 26 as stated | 23.3 s |
| `l180_describe.py` | `out/describe-n90.json`: the tilts, gaps and extents; decides nothing | under 1 s |

What went wrong along the way, and was redone before the freeze it precedes:

- The self-test’s first run failed two of its own cases: two JSON mutations (`-0` and
  `0/3`) did not apply to the test text, so the reader was handed a valid file.
  They were corrected, and every JSON and twin mutation is now checked to have applied,
  before the run kept.
- The self-test, the check, the plan facts and the controls each ran once into scratch
  space before the receipts kept here were written by the same code; the plan facts’ two
  receipts are equal but for their CPU seconds.
- One shell line that summarised the scratch self-test also carried a no-op
  `python3 -c "print()"` under the system interpreter, against this repository’s rule;
  it read nothing and decided nothing.
- Two command-line explorations with the project interpreter, which decided and wrote
  nothing, found that squares 21 and 42 share a six-place angle under two exact
  orientations; `l180_describe.py` then gained that count, and the receipt kept is its
  second run.
- The pre-commit hook could not run in this worktree (`lefthook` is not on its `PATH`);
  the commits went through without it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
