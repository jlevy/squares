# Özden’s Five Certificates of #927 to #931: Stage 4 Mathematical Review

**Date:** 2026-11-09. **Subjects:** five rational corner Witness/v2 certificates by Doğa
Özden, prepared and posted by his AI agent (`kenaznia-doga`):

- `n-232-candidate.yaml` of
  [kenaznia-doga/s232-upper-bound@09e324f](https://github.com/kenaznia-doga/s232-upper-bound/tree/09e324f447d20e10b79de410ad9950a2772c955d),
  issue [#927](https://github.com/jlevy/squares/issues/927);
- `n-268-candidate.yaml` of
  [kenaznia-doga/s268-upper-bound@a40a15d](https://github.com/kenaznia-doga/s268-upper-bound/tree/a40a15d91081be002805b6eea35e099c9a2656db),
  issue [#928](https://github.com/jlevy/squares/issues/928);
- `n-299-candidate.yaml` of
  [kenaznia-doga/s299-upper-bound-17801004@a042eab](https://github.com/kenaznia-doga/s299-upper-bound-17801004/tree/a042eab017caeb07ca5f79afcdc5fbb89103cda2),
  issue [#929](https://github.com/jlevy/squares/issues/929);
- `n-303-candidate.yaml` of
  [kenaznia-doga/s303-upper-bound@b43ca09](https://github.com/kenaznia-doga/s303-upper-bound/tree/b43ca090fc2ff5e750fecc71d8514298fe164514),
  issue [#930](https://github.com/jlevy/squares/issues/930);
- `n-307-candidate.yaml` of
  [kenaznia-doga/s307-upper-bound@dbe8838](https://github.com/kenaznia-doga/s307-upper-bound/tree/dbe8838a7273dc8458fef1f5a16ef4384867ca19),
  issue [#931](https://github.com/jlevy/squares/issues/931).

Bead `think-rd0p`.

**Reviewed at:** `main` `19b354a5c`, the record each claim is measured against, and the
five pins above.

**Reviewer:** Claude (AI review), strong tier (`tbd-strong-max`) at maximum reasoning,
the stage 4 mathematical review lane (L64), separately prompted.
It shared no context with the import lane (L63), which registers the same five issues in
parallel. It read the sources as data and ran only programs of its own, kept with their
receipts in the import packets’ `review/review-2026-11-09/` directories.
It is not a human oversight record.

## Summary for the Author

**Verdicts: accepted with findings at all five counts.** No finding is blocking or
major. F4 is minor; the other findings are notes, F5, F11 and F12 of them for you.

*Changed after the findings were frozen.* The frozen verdict was “accepted at all five”,
with every finding a note.
The [reconciliation](#reconciliation-with-the-import-lane) raises F4 to minor, because
the draft register claims repeat the sentence it is about; both precedents graded a
repeated source account so, with “accepted with findings”.
Every certificate and every bound is accepted without reservation; F4 is about a
sentence. The reconciliation also reassigns F12 and adds F13 and F14, both notes.

| n | Issue | Exact side (floor, 20 places) | Rounded up at 12 | Wall contacts | Least pair gap | Below the house on `main` | Verdict |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 232 | #927 | 15.76140964488172433651… | 15.761409644882 | 3 | $2.0358 \times 10^{-13}$ | T-256 by $2.52115 \times 10^{-4}$ | accept with findings (F4) |
| 268 | #928 | 16.87246989783621245352… | 16.872469897837 | 3 | $2.0122 \times 10^{-13}$ | T-270 by $2.96203 \times 10^{-5}$ | accept with findings (F4) |
| 299 | #929 | 17.80100443425529367352… | 17.801004434256 | 3 | $2.0262 \times 10^{-13}$ | T-263 by $2.34100 \times 10^{-4}$ | accept with findings (F4) |
| 303 | #930 | 17.90178927315649033135… | 17.901789273157 | 3 | $2.0128 \times 10^{-13}$ | T-272 by $4.34777 \times 10^{-5}$ | accept with findings (F4) |
| 307 | #931 | 17.97923096038736272921… | 17.979230960388 | 3 | $2.0174 \times 10^{-13}$ | T-256 by $2.03233 \times 10^{-5}$ | accept with findings (F4) |

- **How the bounds were checked.** A clean-room exact checker, written and frozen for
  this review before any of your code or this repository’s witness code was read,
  decided all five files: every square, every wall and every pair, with no distance
  filter, by two methods that share only the reader.
  They are separating axes in Python fractions and exact clipped areas in GMP rationals.
  They agree on all 199,849 pairs and all 1,409 squares.
  Every pair is strictly apart, and every square is inside.
- **Controls.** Of 95 controls stated in advance (19 per file), every whole-file control
  came out as stated. Two stated outcomes missed through errors in my own constructions,
  and an addendum of 20 controls, also stated in advance, replaced them as stated
  ([Controls](#controls)). Reading the rotation the other way breaks every file (93 to
  122 overlapping pairs).
  Lowering the side by one unit of its own last place pushes out exactly the square
  touching the far wall.
- **Your claims.** Each claim is the side’s 12-place ceiling, so each bounds $s(n)$.
  Each improvement and relative improvement is the exact gap rounded.
  Each `packing-witness verify` print is the certificate’s side, and each sqcheck print
  is its exact 15-place ceiling, so the binary64 print of the 4 November review does not
  recur.
- **How the certificates were made.** The least corner coordinates are exactly 0 and the
  side is exactly the greatest one, so three squares touch the walls exactly (left,
  bottom and one far wall).
  Every pair below $10^{-9}$ is apart by at least $2.012 \times 10^{-13}$, most by less
  than $3 \times 10^{-13}$. Between 111 and 169 squares per file are turned by less than
  $10^{-9}$ radian but not by zero.
  “Squares at the walls touch them exactly” holds for those three; 31 to 61 other
  square–wall pairs sit between $8.7 \times 10^{-33}$ and $10^{-12}$ apart (F4).
- **Against the houses.** Each packing is a further arrangement of its house’s packing:
  the optimal assignment pairs it one to one with the house under the identity, with 4
  to 12 squares beyond a tenth.
  Every count you give in the lineage paragraphs is measured exactly, if “tilted” means
  beyond 0.5 degree (F5). At 299 nearest centres miss one to one by one square, because
  the bottom row slides by up to 0.642 (F6).
- **The gains are real.** Each exceeds its house’s whole scale slack by at least
  $5.7 \times 10^{8}$, so no rescaling of a house reaches the new side.
- **Custody and licence.** The commits, trees and digests are as you state, and
  `LICENSE.md` puts the witnesses under CC BY 4.0.
- **Significance.** S3 at all five, by the record’s own calibration for continued
  arrangements (F8).

## Scope

**Read.**

- `packing/campaign/result-import.md`, stage 4, and `epistemics.md`: the ladders,
  independence, review records, significance and kinds.
- The structural precedents `review-2026-11-04-ozden-893-894-299-204.md` and
  `review-2026-11-05-evand-914-seven.md`.
- `packing/witnesses/witness.schema.yaml`, the Witness/v2 specification.
- Issues #927 to #931 through GitHub (no comments, never edited).
- The five repositories as data: the certificates and JSON twins, `README.md`,
  `LICENSE.md`, and the printed outputs `packing-witness-verify.txt` and
  `sqcheck-output.txt`.
- On `main`: the five house witnesses `n-NNN.yaml`, the five regularized views
  `n-NNN-regularized.yaml.gz`, the register entries named here, the case records’
  upper-bound and rigidity blocks, and the #844 packet’s credit section.

**Run.** Ten programs and five modules of my own, importing nothing from this repository
or the sources ([What I Ran](#what-i-ran)). They decide all five certificates twice, run
a self-test and the controls, do the side arithmetic, decide the five houses and measure
their slack, measure each packing against its house and view, describe how the
coordinates were made, check custody, and hold every receipt to the programs’ digests.

**Seen before my findings were written**, disclosed as the runbook asks:

- the brief (bead `think-rd0p`), which states the five pins, digests, claims and record
  values;
- the register rows of the houses and of the entries cited under
  [Significance](#significance), with their significance rationales;
- the two precedents named above, which state their own reviewers’ results.

**Not read before my checker was frozen** (2026-11-09T07:18:14Z): any producer code, and
any of this repository’s witness, verifier or promotion code.

**Not read before my findings were frozen.** The author’s `verifier/sqcheck.py` and
`verifier/README.md` (hashed only); lane L63’s branch, pull request, notes and packets;
and this repository’s `sqpack` verifier and `packing-witness promote`. *All but the
verifier were read afterwards, in the last three sections.*

**Not run here.** Any of the author’s code or of the maintained routes.

**Not reviewed.** The author’s decimal pose, which is not published, and so the
statement that sqcheck certified it in interval arithmetic before promotion; the
adoption, which follows on the import branch.

## The Claim and What It Needs

For each $n \in \{232, 268, 299, 303, 307\}$ the issue claims $s(n) \le C$, where $C$ is
its 12-place print. The certificate proves $s(n) \le S$ for its side $S$: there are $n$
closed unit squares, rotated freely, with pairwise disjoint interiors inside the closed
square $[0, S]^2$. Since $C \ge S$, the claim follows.
A Witness/v2 corner file gives square $i$ as four rational corners $p_0, \ldots, p_3$
and nothing else: no centre, basis or angle.
The schema leaves the corner order to the file.
The claim needs six hypotheses, each checked separately:

1. **The reading.** The envelope is `packing.squares:Witness/v2`, enforced; the
   representation is `corners`; the scalars are `rational`; the size is `'1'`; the
   origin is `lower-left` and the axes `x-right-y-up`, so the box is $[0, S]^2$. Every
   scalar is an integer or $p/q$ with $q > 0$.
2. **The count.** There are $n$ squares with distinct ids, and the side is the stated
   fraction.
3. **Unit squares.** The corners, in the listed order, are a unit square: with
   $u = p_1 - p_0$ and $f = p_3 - p_0$, $u \cdot u = 1$, $f = \pm u^\perp$ and
   $p_2 = p_0 + u + f$. The rotation is then $u = (\cos\theta, \sin\theta)$ itself,
   exactly rational, which is why every separation along an edge direction below is an
   exact rational length.
   Method B checks the same polygon another way: four edges of length 1, turns of one
   sign and area 1 make a rhombus of side 1 with area 1, which is a unit square.
4. **Containment.** A convex polygon lies in $[0, S]^2$ exactly when its corners do
   (method A), and exactly when, clipped to the box, it keeps its area (method B).
5. **Disjoint interiors.** For convex bodies the interiors meet exactly when
   $0 \in \operatorname{int}(Q_i - Q_j)$, and every facet normal of $Q_i - Q_j$ is an
   edge normal of $Q_i$ or $Q_j$. So the interiors are disjoint exactly when the
   projections on one of the four edge directions $u_i, u_i^\perp, u_j, u_j^\perp$
   overlap in at most a point (method A; the pair margin is the largest gap).
   Independently, $Q_i \cap Q_j$ is convex, and a convex set has positive area exactly
   when its interior is nonempty, so the interiors are disjoint exactly when the clipped
   intersection has area 0 (method B).
6. **The rotation sense.** The corners fix it.
   Reflected in their own horizontal centre lines, which turns $u = (a, b)$ into
   $(a, -b)$, every packing overlaps (control G6), so the sense as written is the one
   that holds.

`l64_check.py` decides hypotheses 1 and 2 through the reader, and 3 to 5 twice: method A
in `fractions.Fraction`, method B in `gmpy2.mpq`. The two share only the reader, which
returns integers. The reader fails closed on any layout it does not expect; the JSON
twin, read with the standard library’s `json`, must hold exactly the same witness.

## The Certificates Decided

| n | SHA-256 | Squares off the axes | Pairs | Wall contacts (square) | Least positive wall clearance | Least pair margin (squares) | Pairs below $10^{-12}$ |
| ---: | --- | ---: | ---: | --- | --- | --- | ---: |
| 232 | `22b3809e…` | 203 | 26,796 | left 210, bottom 62, top 131 | $8.73 \times 10^{-33}$ (140, right) | $2.03581120979 \times 10^{-13}$ (35, 77) | 383 |
| 268 | `74c0e5d4…` | 265 | 35,778 | left 63, bottom 11, top 263 | $2.53 \times 10^{-16}$ (260, top) | $2.01218189216 \times 10^{-13}$ (177, 264) | 499 |
| 299 | `dfb0ccf7…` | 256 | 44,551 | left 107, bottom 113, right 86 | $1.22 \times 10^{-16}$ (106, left) | $2.02624754210 \times 10^{-13}$ (179, 194) | 612 |
| 303 | `9cbeb7a8…` | 289 | 45,753 | left 255, bottom 261, top 303 | $1.05 \times 10^{-16}$ (256, left) | $2.01281301441 \times 10^{-13}$ (269, 286) | 355 |
| 307 | `cb78adf8…` | 283 | 46,971 | left 286, bottom 105, right 131 | $2.62 \times 10^{-17}$ (154, left) | $2.01737379497 \times 10^{-13}$ (69, 215) | 792 |

- **Reading.** Every file reads strictly: ids 1 to $n$ in order, every one of the 11,272
  scalars in lowest terms, and every JSON twin the same witness exactly.
  The twins end without a newline, which the reader records and which decides nothing.
- **Squares.** Every square is a unit square by both methods, listed counterclockwise.
- **Walls.** Every square lies in its box by both methods, with exactly three contacts
  per file.
- **Pairs.** All 199,849 pairs are separated by both methods, with equal classes; none
  touches.
- **Distances.** Of the 40 nearest pairs in each file, the exact distance equals the
  margin for 39, 39, 37, 40 and 33. The others are corner-to-corner, farther apart than
  their margin.
- **Verdict.** `ACCEPT` at all five.

The margins are exact fractions in the receipts; the prints here truncate them.

`l64_selftest.py` holds both methods to known answers and passes:

- edge, corner and 3-4-5 vertex–edge contacts, in both listing senses, and their
  $10^{-30}$ overlaps of area $10^{-30}$, $10^{-60}$ and
  $\tfrac{25}{24} \cdot 10^{-60}$;
- a duplicate (area 1, margin $-1$), and a square against its own rotation by
  $(3/5, 4/5)$ and $(4/5, 3/5)$ (area $5/6$, margin $-6/5$);
- walls at contact and $10^{-30}$ past;
- six shapes both methods must refuse;
- 3,000 random rational pairs, each taken exactly to contact along its centre line and
  $10^{-30}$ either side;
- 1,000 random squares taken to a wall and past it;
- 32 malformed files the reader must refuse, each for its own reason.

## Controls

`controls-plan.json` states 19 controls per certificate and the expected outcome of
each. It was written and hashed (`d5e090ad…`, 07:24:31Z) before `l64_controls.py`
existed. “Contact” is a margin of exactly 0, and “past” is $10^{-30}$ beyond it.
Each control was decided by both methods over the whole file, unless marked pair-level
or square-level.

| Control | Stated | 232 | 268 | 299 | 303 | 307 |
| --- | --- | --- | --- | --- | --- | --- |
| G1. The last square replaced by a copy of the first | refused: margin $-1$, area 1 | as stated | as stated | as stated | as stated | as stated |
| G2. Square 1 translated by $(S, 0)$ | refused, square 1 outside | as stated | as stated | as stated | as stated | as stated |
| G3. The last square’s entry deleted from the YAML | the reader refuses ($n - 1$ squares) | as stated | as stated | as stated | as stated | as stated |
| G4. The last square’s id set to 1 | the reader refuses (repeated id) | as stated | as stated | as stated | as stated | as stated |
| G5. Square 1’s third corner moved $10^{-30}$ in $x$ | refused, not a square | as stated | as stated | as stated | as stated | as stated |
| G6. Every square reflected in its horizontal centre line (the rotation read the other way) | refused, overlapping pairs | 93 pairs | 102 | 122 | 119 | 112 |
| S1a. The side lowered by $1/q$, one unit of its own last place | refused, exactly the far-wall square outside | square 131 | 263 | 86 | 303 | 131 |
| S1b. The side lowered by $10^{-30}$ | the same | squares 131 and 140 (detail missed) | 263 | 86 | 303 | 131 |
| S1c. The side set to its 12-place floor | refused, the far-wall square among those outside | 22 outside | 23 | 29 | 18 | 32 |
| S1d. The side set to its 12-place ceiling, the claim | accepted | as stated | as stated | as stated | as stated | as stated |
| S3a, S3b. Every square moved $10^{-30}$ left, then down | refused, exactly the left (bottom) contact outside | 210, 62 | 63, 11 | 107, 113 | 255, 261 | 286, 105 |
| S4c. The least-margin pair closed along its separating axis | accepted, the pair touching by both | as stated | as stated | as stated | as stated | as stated |
| S4p. The same, past | refused, the pair overlapping by both | as stated | as stated | as stated | as stated | as stated |
| S5. Every pair below $10^{-12}$ closed the same way (pair-level) | touching at contact, overlapping past | missed (construction) | missed | missed | missed | missed |
| S6. Every square moved to its nearest wall by its clearance (square-level) | inside at contact with clearance 0, outside past | 232 of 232 | 268 of 268 | 299 of 299 | 303 of 303 | 307 of 307 |
| S7c. A square of the least-margin pair enlarged to touch its partner | refused for shape, the pair touching | as stated | as stated | as stated | as stated | as stated |
| S7p. The same, past | refused, the pair overlapping | as stated | as stated | as stated | as stated | as stated |
| S8. The far-wall square enlarged by $1 + 10^{-30}$ | refused for shape and wall | as stated | as stated | as stated | as stated | as stated |

Every whole-file control came out as stated, and so did S6 for every square.
Two stated outcomes missed, S1b’s detail at 232 and S5 at every count, and both are this
review’s errors, not the certificates’ or the checker’s:

- **S1b at 232.** Square 140’s right clearance is $8.7 \times 10^{-33}$, below the
  $10^{-30}$ step, so it leaves the box beside the far-wall square 131. The check
  receipt had shown that clearance; the plan overlooked it.
  S1a, a far sharper step ($1/q$ is below $10^{-160}$ at every count), pushes out square
  131 alone, as stated.
- **S5 everywhere.** Closing a pair along its separating axis does not always reach
  contact. For a diagonal near-contact the line along one edge normal passes beside the
  other square, and both methods rightly keep calling the pair separated.
  The least pairs of S4 are not of that kind, which is why S4 held.

Both first runs are kept.
`controls-plan-addendum.json` (`acfd29c1…`, 07:33:36Z) was then stated before any of its
controls ran: the same closings along each pair’s centre line, which always meets the
pair, and a diagnosis of S5.

| Addendum control | Stated | 232 | 268 | 299 | 303 | 307 |
| --- | --- | --- | --- | --- | --- | --- |
| S4′c. The least-margin pair closed along its centre line | accepted, the pair touching by both | as stated | as stated | as stated | as stated | as stated |
| S4′p. The same, past | refused, the pair overlapping by both | as stated | as stated | as stated | as stated | as stated |
| S5′. Every pair below $10^{-12}$ closed along its centre line (pair-level) | touching at contact, overlapping past | 383 of 383 | 499 of 499 | 612 of 612 | 355 of 355 | 792 of 792 |
| S5 diagnosis | S5’s misses are exactly the pairs whose separating-axis line misses the pair | 28 pairs | 91 | 123 | 5 | 238 |

So every near pair of every file was taken to exact contact and $10^{-30}$ past it, and
every square to its wall and past it, by both methods.

## The Sides and the Prints

`l64_sides.py` does the arithmetic exactly.

| n | Digits of $q$ | Side to 40 places (floor) | Claim, the 12-place ceiling | Claim less side |
| ---: | ---: | --- | --- | --- |
| 232 | 221 | 15.7614096448817243365191429188091452493534 | 15.761409644882 | $2.757 \times 10^{-13}$ |
| 268 | 191 | 16.8724698978362124535298641951789205897225 | 16.872469897837 | $7.875 \times 10^{-13}$ |
| 299 | 162 | 17.8010044342552936735298641951785451039999 | 17.801004434256 | $7.063 \times 10^{-13}$ |
| 303 | 161 | 17.9017892731564903313568165555760761864999 | 17.901789273157 | $5.097 \times 10^{-13}$ |
| 307 | 221 | 17.9792309603873627292182246175330942570122 | 17.979230960388 | $6.373 \times 10^{-13}$ |

- **The claims.** Each side is a fraction $p/q$ in lowest terms whose decimal expansion
  does not terminate. Each issue’s claim is its 12-place ceiling, so each claim bounds
  $s(n)$; the 12-place floor of each lies below the side and does not.
- **The extent.** In every file the least corner coordinates are exactly 0 in $x$ and in
  $y$, and the side is exactly the greatest corner coordinate: in $y$ at 232, 268 and
  303, in $x$ at 299 and 307. The other far wall is short of the side by
  $8.7 \times 10^{-33}$ at 232, $6.5 \times 10^{-16}$ at 268, $7.4 \times 10^{-16}$ at
  299, $3.8 \times 10^{-16}$ at 303 and $2.6 \times 10^{-16}$ at 307.
- **The records.** Each house side (the house witness’s `side` on `main`) equals the
  fraction the issue states and appears in its register entry’s claim.
  Each issue’s 16-place print of it (15.7616617594813300 and so on) is its 16-place
  ceiling.
- **The author’s prints.** Each `packing-witness-verify.txt` prints the certificate’s
  side exactly. Each `sqcheck-output.txt` prints, as “exact side rounded up”, the side’s
  exact 15-place ceiling, $2.7$ to $6.7 \times 10^{-16}$ above it.
- **The context values.** Each Kaggle per-puzzle side the issues quote lies above both
  the side and the claim.

| n | House | House side (floor, 20 places) | Gap (12 digits, truncated) | Issue | Relative gap | Issue |
| ---: | --- | --- | --- | --- | --- | --- |
| 232 | T-256 | 15.76166175948132992819 | $2.52114599605 \times 10^{-4}$ | 2.521e-04 | $1.59954 \times 10^{-5}$ | 1.60e-05 |
| 268 | T-270 | 16.87249951813503064607 | $2.96202988181 \times 10^{-5}$ | 2.962e-05 | $1.75553 \times 10^{-6}$ | 1.76e-06 |
| 299 | T-263 | 17.80123853397906211146 | $2.34099723768 \times 10^{-4}$ | 2.341e-04 | $1.31507 \times 10^{-5}$ | 1.32e-05 |
| 303 | T-272 | 17.90183275085404876157 | $4.34776975584 \times 10^{-5}$ | 4.348e-05 | $2.42867 \times 10^{-6}$ | 2.43e-06 |
| 307 | T-256 | 17.97925128368802515800 | $2.03233006624 \times 10^{-5}$ | 2.032e-05 | $1.13037 \times 10^{-6}$ | 1.13e-06 |

Every gap is positive.
Each issue’s improvement and relative improvement are the exact values rounded to four
and three significant digits.
The gaps are $2.0 \times 10^{7}$ to $2.5 \times 10^{8}$ units of the 12th place and
$5.7 \times 10^{9}$ to $1.4 \times 10^{11}$ binary64 spacings at the side, so none is a
print or rounding effect.

## Is the Improvement Real?

`l64_houses.py` writes each house witness on `main` as exact corners and decides it with
the frozen checker at its own side.
All five are accepted, with no pair touching.
It then measures each house’s scale slack exactly.
That is how far its side falls when every centre is scaled about the lower-left corner,
orientations kept, until a pair or a wall binds.

| n | House | Least pair margin | Wall contacts | Scale slack | Gap over slack |
| ---: | --- | --- | ---: | --- | --- |
| 232 | T-256 | $2.12 \times 10^{-13}$ | 0 | $3.15 \times 10^{-14}$ | $8.0 \times 10^{9}$ |
| 268 | T-270 | $1.0 \times 10^{-20}$ | 0 | $1.69 \times 10^{-19}$ | $1.8 \times 10^{14}$ |
| 299 | T-263 | $1.0 \times 10^{-22}$ | 43 | 0 | no slack |
| 303 | T-272 | $1.0 \times 10^{-20}$ | 0 | $1.79 \times 10^{-19}$ | $2.4 \times 10^{14}$ |
| 307 | T-256 | $2.09 \times 10^{-13}$ | 0 | $3.58 \times 10^{-14}$ | $5.7 \times 10^{8}$ |

Every gap exceeds its house’s slack by at least $5.7 \times 10^{8}$; at 299 the house
has none, its left-wall contacts holding the scale at 1. So no rescaling of a house
reaches the new side: squares had to move, and they did
([lineage](#identity-lineage-and-the-houses)). The 299 house’s 43 contacts and its least
margin equal those the 4 November review measured.

## How the Certificates Were Made

The issues and READMEs say the rational corners were made by this repository’s
`packing-witness promote --strategy robust-rational` at `19b354a5`, from a decimal pose
of centres and angles.
Each file’s `certificate` block reads `exact-rational-sat`, `rational_digits: 36`,
`center_dilation: '1'`. `l64_construct.py` measures what that produced; it decides
nothing.

| n | Exactly upright | Turned below $10^{-9}$ rad | $10^{-9}$ rad to 0.5° | Beyond 0.5° | Square–wall pairs below $10^{-12}$ (contacts) | Pairs below $10^{-9}$: in $[2, 2.1)$, in $[2.1, 3)$, above, $\times 10^{-13}$ |
| ---: | ---: | ---: | ---: | ---: | --- | --- |
| 232 | 29 | 111 | 9 | 83 | 45 (3) | 347, 36, 24 |
| 268 | 3 | 152 | 14 | 99 | 43 (3) | 143, 263, 112 |
| 299 | 43 | 138 | 24 | 94 | 54 (3) | 408, 204, 0 |
| 303 | 14 | 139 | 39 | 111 | 34 (3) | 316, 39, 0 |
| 307 | 24 | 169 | 2 | 112 | 64 (3) | 606, 181, 6 |

- **Angles.** Each tilt is a rational half-angle $t = s/(1 + c)$ whose numerator has at
  most 36 digits (denominators 33 to 53), which fits `rational_digits: 36`. The squares
  turned below $10^{-9}$ radian are turned by $1.7 \times 10^{-17}$ (that is, $10^{-15}$
  degree) up to $4.1 \times 10^{-11}$ radian.
  So the decimal pose’s near-upright angles were kept as exact rotations rather than set
  to zero. That is sound, and it is why 203 to 289 squares per file are off the axes
  while 83 to 112 are tilted.
- **Walls.** The packing is placed with its least corner coordinates at exactly 0 and
  the side at its greatest corner coordinate, so exactly one square touches each of
  three walls. The other squares along the walls sit $8.7 \times 10^{-33}$ to $10^{-12}$
  inside: 31 to 61 square–wall pairs per file.
  The houses on `main` have no wall contact at 232, 268, 303 and 307 and 43 at 299.
- **Pairs.** Every pair below $10^{-9}$ is apart by at least $2.012 \times 10^{-13}$;
  most lie in $[2.0, 3.0) \times 10^{-13}$, and the largest such margins are
  $1.6 \times 10^{-10}$ at 232 and $5.0 \times 10^{-11}$ at 268. This fits the issues’
  “pairs are separated by at least about 2e-13”.

The certificates are checked as given; the construction is only how the margins arose
(question 3).

## Identity, Lineage and the Houses

`l64_identity.py` measures each certificate pose by pose, in binary64, against the house
witness on `main` and against the regularized view the issues say the search started
from, under all eight symmetries of the reference’s own box.
It reports nearest-centre pairing and SciPy’s optimal assignment of least summed squared
move.

| n | House | Best symmetry | One to one by nearest centres | Moved beyond $10^{-3}$, 0.05, 0.1 | Within 0.05 | Largest move | Turned beyond 1° | Largest turn | Tilted beyond 0.5° (new, house) | Same id |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | ---: |
| 232 | T-256 | identity | yes | 141, 8, 6 | 224 | 0.500 | 12 | 28.76° | 83, 83 | 206 |
| 268 | T-270 | identity | yes | 122, 11, 4 | 257 | 0.274 | 3 | 2.14° | 99, 99 | 268 |
| 299 | T-263 | identity | no: 298 distinct | 187, 14, 12 | 285 | 0.642 | 5 | 41.32° | 94, 85 | 299 |
| 303 | T-272 | identity | yes | 239, 10, 5 | 293 | 0.227 | 14 | 19.02° | 111, 112 | 292 |
| 307 | T-256 | identity | yes | 45, 7, 5 | 300 | 0.200 | 6 | 25.23° | 112, 108 | 307 |

- **Your lineage statements.** Every count each issue gives (centres beyond $10^{-3}$
  and 0.05, the largest move, the squares re-tilted beyond 1° and the largest re-tilt)
  is the measured one against the house witness, to the digits printed.
  So are the tilted counts, if a square counts as tilted beyond 0.5°. Beyond 1° they are
  80 and 81, 99 and 98, 85 and 85, 111 and 112, and 112 and 107 (F5).
- **The views.** Each regularized view is itself one to one with its house under the
  identity, moving at most 0.373. Measured against the views, the candidates give
  slightly different counts; the issues’ counts are against the houses (F7).
- **What changed.**
  - At 232 a tilt moves between squares: square 44 at $(6.06, 13.00)$ turns from upright
    to $-27.7°$, while two squares near $(1.5, 6)$ and $(2.5, 5.5)$ go from $-28.8°$ to
    upright and $-1.6°$. The largest moves are of two upright squares: 0.500 upward near
    the top wall and 0.472 rightward near the right wall.
  - At 268 two squares of the column at $x = 1.5$ rise by 0.27, and three squares turn
    by 1.3° to 2.1°.
  - At 299 the bottom row from $x \approx 9.7$ to the right wall is pushed right and
    closed up, its squares moving 0.08 to 0.642. The column at $x = 1.5$ rises by 0.26
    to 0.29. Square 71 at $(11.62, 1.47)$ turns from $-26.8°$ to $+14.5°$, reversing its
    tilt (the 41.32°), and square 64 straightens from $-11.9°$ to $-0.3°$.
  - At 303 the upper-right block near $x = 14.4$ to 16.4, $y = 12$ to 17.4 rises by up
    to 0.227, and square 85 at $(11.64, 11.64)$ turns from upright to $-19.0°$.
  - At 307 square 163 at $(4.03, 10.43)$ turns from $-23.7°$ to $+1.5°$, five upright
    squares beside it take the same $1.522°$, and three squares near the top-right
    corner move 0.06 to 0.14.
- **Ids.** At 268, 299 and 307 every square keeps its house id; at 232, 26 squares are
  renumbered, and at 303, 11.

**The reading.** The record keeps “refinement” for a packing that pairs one to one with
another and moves no square beyond a tenth, and “further arrangement” for one that pairs
one to one and moves some (T-239, T-263, T-264, T-265). By that rule all five are
further arrangements of their houses’ packings.
At 299 no symmetry pairs nearest centres one to one.
Under the identity they miss by one square (298 distinct), because the bottom row slides
by more than half a unit, so each of its squares lies nearer its right neighbour’s old
place. The optimal assignment pairs every square with its own id, 285 stay within 0.05,
and the slide is of a row of upright squares along the wall.
I read it as a further arrangement too (F6).

**Credit.** As the issues ask: the improvement to Doğa Özden, the base packings to their
holders as the record lists them (at 232 Alex Chilton’s Kaggle notebook packing as
Francisco Couzo refined it; at 268 and 303 Evan Daniel’s composer packings after Chris
Deotte; at 299 Evan Daniel’s packing as Doğa Özden improved it; at 307 ntumlnoob’s
Kaggle notebook packing as Couzo refined it), and the local optimizer to Evan Daniel.
The measured relation supports that credit: each packing continues its house’s.

## What the Checkers Share

- **This review’s checker.** It shares no code with any other checker, and it was
  written and frozen before any producer code or any of this repository’s witness,
  verifier or promotion code was read.
  It shares the mathematics above and the format’s meaning: corners in cyclic order, the
  lower-left origin, the box $[0, S]^2$. That meaning comes from the schema text and the
  files, and the reflected control shows the orientation matters.
  It trusts CPython’s integers and `fractions`, GMP through `gmpy2` 2.3.1, PyYAML’s
  `BaseLoader` for parsing only, and the clipping and shoelace identities its self-test
  exercises. Its two methods share the reader and nothing else.
- **Where the coordinates came from.** By the issues, the rational corners were made by
  this repository’s `packing-witness promote`, not by code of the author’s. So the code
  that made the exact coordinates is first-party code of this repository.
- **The author’s checks.** By the issues, one is this repository’s
  `packing-witness verify` at `19b354a5`, run unmodified; its printed sides equal the
  certificates’ exactly.
  The other is `verifier/sqcheck.py`, the lab’s own, not read before the freeze and not
  run here; its printed sides are the exact 15-place ceilings.
- **Consequence for the record’s words.** A replay through `sqpack`’s verifier runs the
  author’s own first check again, from the package whose promotion made the coordinates.
  Which maintained route shares what with that code is for the records lane to state
  (F10). This review’s run is independently re-implemented, clean room, with full
  coverage of the five certificates.
- **Authorship.** The issues say AI agents wrote and ran the search and its checks, and
  the lab’s #890 said Claude agents ran its checks.
  This repository’s witness tooling carries commits co-authored by Claude, and this
  review was written by a Claude agent.
  So the reviewer shares a system family with the code that made the coordinates, and
  likely with the producer.
- **What is common to all.** An error in the format’s meaning or in the definition of a
  packing would be common to every checker.
  An error in any one implementation would not.

## Custody and Licence

`l64_custody.py` ran read-only git plumbing (`rev-parse`, `rev-list`, `log`, `ls-tree`,
`cat-file`) on clones of the five repositories made for this review.

| n | Repository | Pin | Committed (UTC) | Tree |
| ---: | --- | --- | --- | --- |
| 232 | `kenaznia-doga/s232-upper-bound` | `09e324f447d2` | 06:02:41 | `c293f408` |
| 268 | `kenaznia-doga/s268-upper-bound` | `a40a15d91081` | 06:02:49 | `fce13dc1` |
| 299 | `kenaznia-doga/s299-upper-bound-17801004` | `a042eab017ca` | 06:02:57 | `1009d5b5` |
| 303 | `kenaznia-doga/s303-upper-bound` | `b43ca090fc2f` | 06:03:05 | `6614d2c8` |
| 307 | `kenaznia-doga/s307-upper-bound` | `dbe8838a7273` | 06:03:13 | `8c1bb02b` |

- Each repository holds one commit, with no parent, at the issue’s pin, authored and
  committed by `kenaznia-doga <doga@doga.kenan.works>`. The issues were opened 32 to 35
  seconds after the last commit and have not been edited.
- Each holds the same nine files: `LICENSE.md`, `README.md`, the certificate, its JSON
  twin, the two printed outputs, `records/n-NNN-candidate-diff.png`,
  `verifier/README.md` and `verifier/sqcheck.py`. The last two and `LICENSE.md` are one
  blob each across all five.
- Every working-tree file equals its committed blob.
- Each certificate’s SHA-256 is the issue’s, and each JSON twin’s is the one its README
  states.
- `verifier/sqcheck.py` is blob `aa4b27ca`; the copy the #893 packet retains is blob
  `29634efa`. The verifier changed between the two passes, as “It now prints the exact
  side rounded up” says.

Custody holds.

`LICENSE.md` (“Copyright © 2026 Doğa Özden”) licenses “certificates, witnesses,
receipts, data and write-ups” under CC BY 4.0, and source code under MIT. So the
witnesses are covered, which answers the 4 November review’s question 5. The base
packings are other holders’: Evan Daniel’s MIT-licensed certificates at 268 and 303, and
through T-258 at 299; at 232 and 307, Couzo’s certificates of Kaggle notebook packings,
which the record retains under its presumption of permission.
Whether coordinates moved this far need an upstream notice remains `think-mdxq`’s
question (F11).

## Significance

**S3 at all five.** If correct, each claim is the smallest side on record at its count,
$2.03 \times 10^{-5}$ to $2.52 \times 10^{-4}$ below the house, by a further arrangement
of the house’s packing.

- The record draws its S2/S3 line by the size of the step.
  T-239’s rationale puts it between T-198’s $1.15 \times 10^{-5}$ (S2) and T-226’s
  $1.88 \times 10^{-5}$, “the low end of S3”.
- Below the line are further arrangements and refinements of a house: T-188
  ($9.29 \times 10^{-6}$), T-239 ($9.89 \times 10^{-6}$), T-264 ($6.48 \times 10^{-6}$),
  T-263 ($1.54 \times 10^{-8}$) and T-265 ($1.99 \times 10^{-10}$), all S2.
- Above it, continuations of an arrangement are S3 as new arrangements are: T-219 (a
  continuation, $4.46 \times 10^{-5}$, “above T-188’s 9.29e-06 (S2)”), T-172 (a
  refinement, $6.66 \times 10^{-5}$), T-189 (a refinement, $1.01 \times 10^{-4}$) and
  T-183 (another arrangement of a design, $2.45 \times 10^{-4}$).
- All five steps lie above the line: 232 and 299 beside T-183 and T-189, 303 just below
  T-219, and 268 and 307 at the low end, above T-226.
- None is S4: no technique is new here.
  The search is basin hopping over Evan Daniel’s published quench, and the promotion is
  this repository’s tool.

## Findings

| Id | Severity | Where | Finding |
| --- | --- | --- | --- |
| F1 | note | all five certificates | each is an exact packing at its side, by both methods, every wall and pair; every pair strictly apart, three wall contacts |
| F2 | note (this review) | the controls | every whole-file control as stated; two stated outcomes missed through this review’s own constructions (S1b at 232, S5), and the addendum is as stated |
| F3 | note | sides and prints | each claim is the 12-place ceiling; each gap and relative gap is as printed; each sqcheck print is the exact 15-place ceiling |
| F4 | minor (author; the record repeats it; raised after the freeze) | each `README.md`:36; each issue’s Certificate paragraph | “squares touching the walls touch them exactly (containment clearance 0)” holds for three squares per file; 31 to 61 other square–wall pairs sit $8.7 \times 10^{-33}$ to $10^{-12}$ apart |
| F5 | note (author; records) | each `README.md`:40; each issue’s Lineage paragraph | “tilted” counts squares beyond 0.5°, which is not stated; beyond 1° the counts differ at four counts |
| F6 | note (records) | the 299 lineage | nearest centres miss one to one by one square; the optimal assignment keeps every id; a further arrangement |
| F7 | note (records) | the lineage of all five | the issues measure against the house witnesses, not the regularized views they started from; all five are one to one with their houses under the identity |
| F8 | note (records) | the significance of all five | S3 by the record’s calibration for continued arrangements |
| F9 | note (records, at adoption) | `n-232.md`, `n-268.md`, `n-299.md`, `n-303.md`, `n-307.md` | the rigidity scopes, credit fields and construction notes describe the retained witness and must be derived again |
| F10 | note (records) | the replay evidence still to be registered | which confirmation each run is, given that this repository’s promotion made the coordinates |
| F11 | note (author; records) | `LICENSE.md` | the witnesses are under CC BY 4.0; the base packings’ notices are `think-mdxq`’s question |
| F12 | note (author; records; reassigned after the freeze) | each certificate’s `source` and `certificate` blocks (lines 2344 to 2352 at 232) | `source.path` and `certificate.replay` name paths under `/tmp` on the author’s machine, which this repository’s `promote` writes from its command line |
| F13 | note (records; added after the freeze) | the five packet READMEs, “What the Source Claims” | the side printed as its 16-place ceiling followed by “…”, which reads as the expansion |
| F14 | note (records; added after the freeze) | the 307 packet’s `measure/identity.json`; the 307 draft entry’s notes | the regularized view at 307 was not measured, its schema path refused by the corner reader; measured here, it is one to one with the certificate under the identity |

**F1. Feasibility.** All five files are exact packings at their sides: 199,849 pairs,
each decided by both methods with equal classes and strictly apart, and 1,409 squares,
each a unit square inside its box by both.
The bounds hold.

**F2. Controls.** As [Controls](#controls) gives them.
Every whole-file control came out as stated in advance, at every count.
The two missed outcomes (S1b’s detail at 232, S5 everywhere) were my constructions’; the
addendum, stated before it ran, takes every near pair to contact and past it along its
centre line and explains every S5 miss.

**F3. Sides and prints.** As [The Sides and the Prints](#the-sides-and-the-prints) gives
them. The 4 November review’s F2 does not recur: sqcheck now prints the exact 15-place
ceiling.

**F4. The wall contacts.** `README.md` line 36 says “every pair is separated by at least
about 2e-13 and squares touching the walls touch them exactly (containment clearance
0)”, and each issue says “squares at the walls touch them exactly”.

- Measured, exactly three squares touch a wall in each file: one each at the left and
  bottom, where the packing is placed at 0, and one at the far wall that sets the side.
- The other squares along the walls are inside by $8.7 \times 10^{-33}$ to $10^{-12}$:
  45, 43, 54, 34 and 64 square–wall pairs below $10^{-12}$, counting the three contacts.
- The bound does not depend on any of this.
  As a description of the certificates the sentence reads as if every wall square
  touched.
- “Exactly one square touches the left, the bottom and one far wall; the others along
  the walls sit within $10^{-12}$” would be exact (question 1).

*Raised to minor after the freeze.* All five draft register claims repeat the sentence,
as the author’s statement: the exact coordinates were made “with pairs separated by at
least about 2e-13 and squares at the walls touching them exactly”.
So do the five packet READMEs.
Both precedents graded a source account the record repeats as minor.
The promotion code, read after the freeze, shows why the sentence overstates: it places
the packing at the corner and the side at its extent, which makes exactly three contacts
([The Promotion](#the-promotion-read-after-the-findings-were-frozen)). The claims could
add the measured account after the author’s sentence.

**F5. What “tilted” counts.** `README.md` line 40 and each issue say the packing has 83,
99, 94, 111 and 112 tilted squares against 83, 99, 85, 112 and 108. Those are the counts
beyond 0.5°, measured exactly.
Beyond 1°, which is also the issues’ re-tilt threshold, they are 80 against 81, 99
against 98, 85 against 85, 111 against 112, and 112 against 107. Beyond $10^{-9}$ radian
they are larger still, since 111 to 169 squares per file are turned by less than that
but not by zero. Naming the threshold would make the counts exact (question 2).

**F6. 299 by nearest centres.** No symmetry pairs the 299 packing one to one with
T-263’s by nearest centres: under the identity 298 houses are nearest, the bottom row
having slid by up to 0.642. The optimal assignment pairs every square with its own id
under the identity, with 12 beyond a tenth and 285 within 0.05. The record’s word for
that is “further arrangement”, as at 232, 268, 303 and 307. The notes should say that
the nearest-centre test fails here only by the slide, so that no reader takes 299 for a
new arrangement.

**F7. Against the views.** The issues say each search started from the regularized
known-best atlas, and their lineage counts are against the house witnesses.
Each view is one to one with its house under the identity, moving at most 0.373, so the
two readings agree on the relation and differ only in counts.
The record’s notes should give the counts against the house and say so.

**F8. Significance.** As [Significance](#significance) gives it: S3 at all five, 268 and
307 at the low end of the band.
*After the freeze:* the import lane drafted S2 at all five; this review changes each to
S3 ([reconciliation](#reconciliation-with-the-import-lane)).

**F9. The case records at adoption.** Each case record’s rigidity scope is of “the
retained witness”, which adoption replaces.
At 232, for example, it names the house’s square 0, which translates 0.022774. The
scopes, `found_by` and `improved_by` (the improvement to Doğa Özden, the base packing to
its holders as listed), and any construction note must be derived again for the new
witnesses, as earlier adoptions did.

**F10. Which confirmation.** The author’s first check is this repository’s
`packing-witness verify`, and the coordinates were made by this repository’s
`packing-witness promote`. When the replay and this review are registered:

- a replay through `sqpack`’s verifier is the author’s first check run again, and shares
  a package with the code that made the coordinates;
- any other maintained route should state what it shares with `sqpack`’s witness code;
- this review’s run is independently re-implemented, clean room, full coverage of the
  five certificates, by a Claude agent, a system family that also wrote this
  repository’s witness tooling.

The result’s level is then independently re-implemented.
*After the freeze:* the draft entries’ notes and evidence limitations already say how
the two routes stand to the author’s check and to the promotion.
One fact could be added: the promotion itself ran `sqpack`’s exact `verify_packing` on
these coordinates before writing them.

**F11. Licence.** `LICENSE.md` licenses the witnesses under CC BY 4.0 and the code under
MIT, with credit to Doğa Özden “with the prior work cited in the README”. The base
packings are Evan Daniel’s MIT-licensed certificates (268, 303, and 299 through T-258)
and Couzo’s certificates of Kaggle packings (232, 307). Whether coordinates moved this
far need an upstream notice is `think-mdxq`’s question; the record’s presumption stands
for the retained copies.

**F12. Local paths in the files.** Each certificate’s `source.path`
(`/tmp/q1108wit/a005-hit-n232-w0.yaml` at 232) and `certificate.replay`
(`uv run --frozen packing-witness verify /tmp/q1108prom/…`) name files on the author’s
machine, which no reader can follow.
The files decide correctly as published, and the record will give its own replay command
(question 5).

*Reassigned after the freeze.* This repository’s `promote_rational` writes `source.path`
and `certificate.replay` from the input and output paths it is given on the command
line. So the paths are what any run from a scratch directory leaves, and the tool, not
only the author, could write a name the reader can follow.

**F13. The packets’ side prints** (added after the freeze).
Each packet README’s “What the Source Claims” states $s(232) \le$ 15.7614096448817244…
“rounded up at 16 places”, and likewise at the other four counts.
That is the 16-place ceiling with an ellipsis after it.
An ellipsis reads as the expansion, whose 16th place is 3 (15.76140964488172433…). The
register claims print the ceiling without one, which is exact.

**F14. The 307 view** (added after the freeze).
The import lane’s identity measurement did not reach the regularized view at 307, a
corner witness whose schema path (`../../../witnesses/witness.schema.yaml`) its corner
reader refuses, so the 307 notes measure against T-256 and the house witness only.
Measured here, the 307 certificate is one to one with the view under the identity: 4
squares beyond a tenth, 18 beyond a hundredth, the largest move 0.255. The view itself
is one to one with the house, with 17 squares moved and one beyond a tenth.
The notes could carry that, and the reader could accept the view’s schema path, which is
valid on `main`.

## Questions for the Author

1. Each README says squares touching the walls touch them exactly.
   In each certificate exactly three squares touch a wall, and 31 to 61 other
   square–wall pairs sit within $10^{-12}$. Were those squares at the walls in your
   decimal pose, and is three contacts what the promotion is meant to leave?
2. Do your tilted counts (83 against 83 at 232, and so on) count squares beyond 0.5°?
3. Are the pair margins of about $2 \times 10^{-13}$ your decimal pose’s, from the
   quench’s tolerance, or the promotion’s? And were the 111 to 169 squares per file
   turned by less than $10^{-9}$ radian meant to be upright?
4. At 299 the bottom row is pushed right by up to 0.642, and square 71 turns from
   $-26.8°$ to $+14.5°$. Did the turn need the room the slide made?
5. Would you replace the `/tmp` paths in each certificate’s `source.path` and
   `certificate.replay` with the repository’s own file names?

*Added after the freeze.* This repository’s promotion code answers part of questions 1
and 3. Three contacts are what it leaves by construction, and with
`center_dilation: '1'` it applied no dilation, so the margins of about
$2 \times 10^{-13}$ are your decimal pose’s, rounded to 36 digits.
What remains is whether the other wall squares touched the walls in your pose, and where
its margins came from.

## What I Ran

All with CPython 3.14.7 (`packing/.venv/bin/python3 -I -B`) under `nice -n 19`, at most
two processes, on a shared four-core host where the import lane used the other two.
The programs, the frozen files and the shared receipts are in
[the 232 packet’s review directory](../../../packing/resources/web/ozden-s232-upper-bound-2026-11-09/review/review-2026-11-09/README.md),
and each other count’s receipts in its own packet’s `review/review-2026-11-09/out/`.
Each receipt records the SHA-256 of the programs that wrote it, and `l64_digests.py`
holds every receipt to the kept bytes and the six checker files to their frozen digests:
`ALL_RECEIPTS_MATCH`.

| Program | Receipt | CPU |
| --- | --- | ---: |
| `l64_selftest.py` | `selftest.json`: `PASSED` | 5 s |
| `l64_check.py`, each count | `check-nNNN.json`: `ACCEPT` at all five | 22 to 43 s each, 167 s in all |
| `l64_controls.py`, each count | `controls-nNNN.json`: every verdict as stated, S1b (232) and S5 missed | 355 to 681 s each, 2,644 s in all |
| `l64_controls_centre.py`, each count | `controls-centre-nNNN.json`: `EVERY_CONTROL_AS_EXPECTED` | 68 to 131 s each, 504 s in all |
| `l64_sides.py` | `sides.json` | 2 s |
| `l64_houses.py` | `houses.json`: five houses `ACCEPT`, slack measured | 58 s |
| `l64_identity.py`, each count | `identity-nNNN.json` | 1 s each |
| `l64_construct.py` | `construct.json` | 140 s |
| `l64_custody.py` | `custody.json`: `CUSTODY_HOLDS` | under 1 s |
| `l64_digests.py` | `program-digests.json`: `ALL_RECEIPTS_MATCH` | under 1 s |

The final runs took 3,524 CPU-seconds, 0.98 CPU-hours; with the development runs, about
one CPU-hour, within the brief’s cap of 40.

What went wrong along the way, and was redone:

- `-I` leaves a script’s own directory off `sys.path`, so each entry program puts its
  own directory first.
- The reader first refused the JSON twins for lacking a final newline.
  A final newline decides nothing, so before the freeze the reader was changed to record
  it.
- The house files on `main` use flow brackets and UTF-8, which the certificate reader
  refuses by design. `l64_house.py` reads them through the same parser.
- The controls’ two missed details, as [Controls](#controls) gives them.

## Verdict

**Accepted with findings at all five counts** (frozen as “accepted”; F4 raised to minor
after the freeze). Each certificate proves $s(n) \le S$ at its side exactly, and each
issue’s 12-place claim bounds $s(n)$.

- Every hypothesis holds exactly, for every square, wall and pair, by two methods that
  agree everywhere.
- Every whole-file control is decided as stated beforehand; two outcomes missed through
  this review’s own constructions, which the addendum replaced as stated.
- No defect of a certificate or of its mathematics is open.

F4 is minor, for the author and for the record that repeats it.
F5, F11 and F12 are notes for both the author and the record; the rest are notes for
this repository’s records.

Mapped as an adversarial review with verdict `accepted` on each of the five entries, it
supports `V3` and `C3` at each, provided `l64_check.py`’s run is registered as
exact-algebraic evidence replayed here with full coverage of the five certificates.
That reads as confirmed, independently re-implemented, clean room, by a Claude agent, a
system family that also wrote this repository’s witness tooling.
`V4` and `C4` would need a second accepted adversarial review by a distinct reviewer and
a human oversight record.
The significance is S3 at all five.

## The Promotion, Read After the Findings Were Frozen

After the freeze I read `promote_rational` and `_promoted_candidate` in
`packing/src/sqpack/witness.py` at `19b354a5c`, the code the issues say made the
coordinates. From a decimal centre-angle witness it:

- rounds every centre to `rational_digits` (36) significant digits, and every angle’s
  half-angle tangent $t = \tan(\theta/2)$ likewise, taking the basis
  $((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$;
- dilates the centres about the box centre by a factor it tries in turn, 1 first and
  then $1 + 10^{-31}$, $1 + 10^{-29}$ and so on;
- translates the corners so that the least $x$ and the least $y$ are 0, and takes the
  side as the greatest corner coordinate;
- keeps the first candidate that its own exact `verify_packing` accepts within the
  allowed side increase, and writes `source.path` and `certificate.replay` from the
  command line.

So everything measured in
[How the Certificates Were Made](#how-the-certificates-were-made) follows.
The 36-digit tangents keep the decimal pose’s near-zero angles.
The three contacts are the translation and the extent.
`center_dilation: '1'` means the first candidate passed, so the margins of about
$2 \times 10^{-13}$ are the decimal pose’s own.
It also means the promotion ran `sqpack`’s exact verifier on these coordinates before
writing them, which F10’s account of the first maintained route should mention.
Nothing here changes a verdict.

## The Author’s Checker, Read After the Findings Were Frozen

After the freeze I read `verifier/README.md` and `verifier/sqcheck.py` (17,654 bytes,
blob `aa4b27ca`, identical in all five repositories).
For a rational corner file, `sqcheck.py`:

- loads YAML with PyYAML’s `safe_load` (`sqcheck.py`:228), which is safe here since
  every scalar is a quoted or `p/q` string; it does not check duplicate keys, ids, the
  origin or the axes, which is immaterial for these files;
- requires $p_1 - p_0$ and $p_3 - p_0$ to be orthonormal and $p_2 = p_0 + e + f$
  (`:283`–290), method A’s unit-square test;
- checks each wall by the half-width $(\lvert u_x\rvert + \lvert u_y\rvert)/2$ about the
  centre, equivalent to method A’s corners;
- skips a pair whose centres are more than $\sqrt 2$ apart, decided exactly (`:333`),
  which is sound;
- decides the rest by separating axes over the four edge normals in `Fraction`,
  reporting an overlap only when all four margins are negative;
- prints `s<=` as the side’s exact 15-place ceiling (`ceil_decimal`, `:365`), which
  fixes the 4 November review’s F2.

So `sqcheck.py` and method A use the same reduction and the same arithmetic.
Method B, exact clipped areas, and the import lane’s second route are what guard against
an error in that reduction.
The README’s statement that it shares no code with this repository’s checkers is the
source’s; nothing in it contradicts that.
Nothing in it changes a finding.

## Reconciliation With the Import Lane

Everything above, except the passages marked as changed or added after the freeze, was
written before I opened anything of lane L63’s, `sqcheck.py`, or this repository’s
verifier and promotion code.
Then I read L63’s bead (`think-463r`) and its branch `claude/bold-ritchie-xo28us-l63` at
`a8e143c6c`, which was not on the remote: the five packets
`ozden-sNNN-upper-bound-2026-11-09`, their receipts and identity measurements, the five
draft register entries with their evidence and bibliography keys, and the ledger’s
listing. The lane and this review were prompted separately and shared no context.

**What agrees, exactly.** `l64_compare_lane.py` holds the lane’s receipts to this
review’s:

- on each positive certificate, both maintained routes’ least pair gap and least
  containment clearance equal this review’s as exact fractions, at all five counts;
- every identity count against the house (moves beyond $10^{-9}$ to 0.1, turns beyond
  $10^{-6}$ radian, nearest-centre one to one or not) equals this review’s;
- the draft entries’ sides, gaps, headlines (“further arrangement … one to one”, and at
  299 “not one to one … by nearest centres under any symmetry”), largest moves and
  turns, and their tilt counts beyond 1° (80 against 81 at 232, and so on) are this
  review’s.

The lane’s 299 reading is F6’s, and its notes already say which confirmation each route
is and that neither is independent of the promotion, as F10 asks.

**What differs, and the dispositions.**

| Here | Lane’s draft | Disposition |
| --- | --- | --- |
| F8: S3 at all five | S2 at all five, “as T-263’s 1.54e-08 … and T-264’s 6.48e-06 … (S2) are”; at 299 “a draft for the review to weigh” | Changed to S3. The draft’s comparators are steps of $10^{-8}$ and $10^{-6}$; the record puts the S2/S3 line between $1.15 \times 10^{-5}$ and $1.88 \times 10^{-5}$ (T-239’s rationale), and every step here is $2.03 \times 10^{-5}$ or more |
| F4: the wall sentence | every claim and packet README repeats it as the author’s | F4 raised to minor; the claims could add the measured account |
| F7: counts against the views | given at 232, 268, 299 and 303, equal to this review’s | Agreed |
| F14 (new): the 307 view | not measured, the corner reader refusing its schema path | Measured here; a note for the notes and the reader |
| F13 (new): “…” after a 16-place ceiling | in all five packet READMEs | A note |
| F12: the `/tmp` paths | not mentioned | Reassigned: the promotion writes them |
| F9: case records at adoption | adoption deferred until this review is mapped | Agreed; F9 applies then |

The draft credit lines (“Ozden after Chilton, Couzo, Daniel, Levy” and so on) add the
project under `builds-on-project` lineage, as `bibliography.yaml`’s rule for such
sources asks, since the searches started from the regularized atlas and the coordinates
were made by the project’s promotion.
That agrees with the issues’ credit request, which names the base holders and Evan
Daniel.

**What only this review has.** The clean-room checker and its second method, the
reversed sense, every near pair taken to contact and past it along its centre line,
every square to its wall, the houses decided and their scale slack, the construction’s
measurements, the 0.5° tilt threshold (F5), and the 307 view.

**What only the lane has.** The maintained routes’ full replays with their gross
controls, the sharp controls on both routes, `acquire_source`’s retention and custody of
the packets, the ledger, the register entries, the requests entries and the contributor
census.

Nothing in the lane’s work, `sqcheck.py` or the promotion code changes a certificate’s
verdict. F4’s grade, and with it the five verdicts’ wording, changed; the significance
proposed here, S3, differs from the draft.

## Frozen Findings

The findings were frozen at 2026-11-09T08:07:30Z, before anything of the import lane’s,
`sqcheck.py` or this repository’s verifier and promotion code was opened, and the time
and digest were recorded in bead `think-rd0p` then.
The frozen text is kept beside the programs as
`frozen/review-2026-11-09-ozden-927-931-five.frozen.md`: 712 lines and 47,124 bytes,
SHA-256 `222929e07ce91629f049581485823ace65c719773f036d21ccb367b975551a2b`. The checker
was frozen earlier, at 07:18:14Z; `frozen/checker-frozen-digests.txt` (SHA-256
`59c3d006…`) holds its six digests.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
