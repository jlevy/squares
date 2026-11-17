# De Winter’s Thirty-Seven Upper Bounds of #941 and #942: Stage 4 Mathematical Review

**Date:** 2026-11-11. **Subjects:** 37 exact rational `.cert` certificates by Joost de
Winter (Delft University of Technology), produced with Claude (Anthropic) under his
direction, each claiming $s(n) \le L$ for a count beyond the case corpus:

- issue [#941](https://github.com/jlevy/squares/issues/941), opened
  2026-11-10T13:30:51Z, fifteen counts from 413 to 910: folder `above324/` of
  [JoostdeWinter/square-packing@71da0d56](https://github.com/JoostdeWinter/square-packing/tree/71da0d56fd91b7061addca2a728ee72ec9728b0b/above324);
- issue [#942](https://github.com/jlevy/squares/issues/942), opened 14:41:18Z, sixteen
  counts from 632 to 989: folder `above324_refined/` of
  [JoostdeWinter/square-packing@a9486ede](https://github.com/JoostdeWinter/square-packing/tree/a9486ede74cd75996f488605f27d7fce32a73b3a/above324_refined);
- the addendum
  [comment 6772308414 on #942](https://github.com/jlevy/squares/issues/942#issuecomment-6772308414),
  posted 16:02:47Z, six counts (597, 754, 864, 865, 869, 991): the same folder at
  [a0c4fc80](https://github.com/JoostdeWinter/square-packing/tree/a0c4fc80db67e9806026921654dce49a155ac31b/above324_refined).

**Reviewed at:** `main` `591644a9e`, the record each claim is measured against; the
certificates as the import branch `claude/bold-ritchie-xo28us-l90` retains them at
`2fb1156eb` (draft pull request #952).

**Reviewer:** Claude (AI review), strong tier (`tbd-strong`), the stage 4 mathematical
review lane (L96), separately prompted.
It shared no context with the import lane (L90), which registers the same reports in
#952. It read the sources as data and ran only programs of its own, kept with their
receipts in the three import packets’ `review/review-2026-11-11/` directories.
It is not a human oversight record.

## Summary for the Author

**Verdicts: accepted at all 37 counts.** No finding is blocking or major.
Three are minor, all about this repository’s records (licence, attribution and the words
the record uses); the rest are notes.

| n | Report | Claim (10-place ceiling) | Exact side (floor, 20 places) | Least pair gap | Least wall gap | Below `main`’s current row by |
| ---: | --- | --- | --- | --- | --- | --- |
| 413 | #941 | 20.8239520077 | 20.82395200761974992883 | $1.0 \times 10^{-45}$ | $5.0 \times 10^{-46}$ | $8.12 \times 10^{-4}$ |
| 494 | #941 | 22.7365988643 | 22.73659886424820000000 | $2.01 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $9.34 \times 10^{-4}$ |
| 539 | #941 | 23.7365988643 | 23.73659886424820000000 | $2.01 \times 10^{-10}$ | 0 (47 contacts) | $7.08 \times 10^{-5}$ |
| 543 | #941 | 23.8024287170 | 23.80242871693299980406 | $1.0 \times 10^{-45}$ | $5.0 \times 10^{-46}$ | $6.25 \times 10^{-4}$ |
| 547 | #941 | 23.8787301198 | 23.87873011972126200421 | $1.0 \times 10^{-45}$ | $5.0 \times 10^{-46}$ | $3.98 \times 10^{-4}$ |
| 590 | #941 | 24.8024287170 | 24.80242871693299980406 | $1.0 \times 10^{-45}$ | 0 (49 contacts) | $9.84 \times 10^{-5}$ |
| 597 | addendum | 24.8969258585 | 24.89692585849740000000 | $2.00 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $4.22 \times 10^{-3}$ |
| 632 | #942 | 25.6456954277 | 25.64569542762600000000 | $2.00 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $1.12 \times 10^{-2}$ |
| 637 | #942 | 25.7447388658 | 25.74473886576590000000 | $3.79 \times 10^{-10}$ | $1.79 \times 10^{-10}$ | $2.46 \times 10^{-2}$ |
| 655 | #942 | 25.9996711101 | 25.99967111005710000000 | $2.00 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | no row; 26 is the grid |
| 684 | #942 | 26.6456964776 | 26.64569647751560000000 | $3.65 \times 10^{-10}$ | $1.55 \times 10^{-10}$ | $1.12 \times 10^{-2}$ |
| 685 | #942 | 26.6870020013 | 26.68700200121560000000 | $2.00 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $5.39 \times 10^{-3}$ |
| 738 | #941 | 27.6912062515 | 27.69120625143270000000 | $8.89 \times 10^{-10}$ | $4.19 \times 10^{-10}$ | $7.74 \times 10^{-5}$ |
| 739 | #941 | 27.6912835939 | 27.69128359386520000000 | $2.00 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $1.67 \times 10^{-4}$ |
| 744 | #942 | 27.7601633593 | 27.76016335925450000000 | $2.00 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $2.66 \times 10^{-2}$ |
| 750 | #942 | 27.8595204745 | 27.85952047445040000000 | $2.02 \times 10^{-10}$ | $1.01 \times 10^{-10}$ | $1.51 \times 10^{-2}$ |
| 753 | #941 | 27.9026514302 | 27.90265143012240000000 | $2.01 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $5.33 \times 10^{-3}$ |
| 754 | addendum | 27.9075316299 | 27.90753162984960000000 | $2.77 \times 10^{-10}$ | $1.29 \times 10^{-10}$ | $1.29 \times 10^{-2}$ |
| 756 | #942 | 27.9245802503 | 27.92458025022390000000 | $2.00 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $2.50 \times 10^{-2}$ |
| 794 | #941 | 28.6912835939 | 28.69128359386520000000 | $2.00 \times 10^{-10}$ | 0 (57 contacts) | $1.65 \times 10^{-4}$ |
| 805 | #942 | 28.8450303356 | 28.84503033550360000000 | $1.41 \times 10^{-9}$ | $5.33 \times 10^{-10}$ | $1.32 \times 10^{-2}$ |
| 809 | #941 | 28.9079170470 | 28.90791704691430000000 | $2.86 \times 10^{-10}$ | $1.27 \times 10^{-10}$ | $1.19 \times 10^{-4}$ |
| 810 | #941 | 28.9079170470 | 28.90791704691430000000 | $2.86 \times 10^{-10}$ | $1.27 \times 10^{-10}$ | $2.53 \times 10^{-3}$ |
| 814 | #942 | 28.9549571055 | 28.95495710545360000000 | $2.00 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $6.48 \times 10^{-3}$ |
| 851 | #941 | 29.6912835939 | 29.69128359386520000000 | $2.00 \times 10^{-10}$ | 0 (61 contacts) | $1.65 \times 10^{-4}$ |
| 864 | addendum | 29.8530288378 | 29.85302883770570000000 | $2.00 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $2.08 \times 10^{-2}$ |
| 865 | addendum | 29.8693054513 | 29.86930545120230000000 | $2.00 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $1.45 \times 10^{-2}$ |
| 867 | #941 | 29.9079170470 | 29.90791704691430000000 | $2.86 \times 10^{-10}$ | 0 (59 contacts) | $1.19 \times 10^{-4}$ |
| 869 | addendum | 29.9122235088 | 29.91222350879550000000 | $2.01 \times 10^{-10}$ | $1.01 \times 10^{-10}$ | $1.02 \times 10^{-3}$ |
| 910 | #941 | 30.6912835939 | 30.69128359386520000000 | $2.00 \times 10^{-10}$ | 0 (65 contacts) | $1.65 \times 10^{-4}$ |
| 918 | #942 | 30.7867372035 | 30.78673720347770000000 | $2.04 \times 10^{-10}$ | $1.02 \times 10^{-10}$ | $9.32 \times 10^{-3}$ |
| 921 | #942 | 30.8271449853 | 30.82714498520890000000 | $2.01 \times 10^{-10}$ | $1.01 \times 10^{-10}$ | $1.25 \times 10^{-2}$ |
| 924 | #942 | 30.8553857463 | 30.85538574620720000000 | $2.00 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $1.54 \times 10^{-2}$ |
| 935 | #942 | 30.9800571865 | 30.98005718640180000000 | $2.00 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $1.41 \times 10^{-2}$ |
| 970 | #942 | 31.6389903231 | 31.63899032305240000000 | $2.02 \times 10^{-10}$ | $1.01 \times 10^{-10}$ | $1.79 \times 10^{-2}$ |
| 989 | #942 | 31.8889473785 | 31.88894737841510000000 | $2.01 \times 10^{-10}$ | $1.01 \times 10^{-10}$ | $2.07 \times 10^{-2}$ |
| 991 | addendum | 31.9019684133 | 31.90196841326170000000 | $2.01 \times 10^{-10}$ | $1.00 \times 10^{-10}$ | $3.26 \times 10^{-2}$ |

The least pair gap is the exact separating-axis margin of the nearest pair, the least
wall gap the least positive clearance; both are exact fractions in the receipts and
truncated here.

- **How the bounds were checked.** A clean-room exact checker, written and frozen for
  this review before any of your code or this repository’s verifier code was read,
  decided all 37 files: every one of the 28,156 squares, every wall, and every one of
  the 11,093,138 pairs.
  It uses two methods that share only the reader: separating axes in Python fractions,
  and exact clipped areas in GMP rationals.
  They agree on every pair’s class and on every one of the 112,624 square–wall
  clearances, exactly.
  No pair overlaps, and every square is inside.
- **Controls.** All 333 controls stated in advance (nine per file) came out as stated.
  Reading the rotation the other way breaks every file (69 to 592 overlapping pairs).
  The 64,223 pairs nearer than $10^{-9}$, and every touching pair, were closed along
  their centre line to exact contact and $10^{-30}$ past it by both methods.
  All 28,156 squares were taken to their nearest wall and past it.
- **Your claims.** Each printed side is the exact side’s 10-place ceiling, so each
  bounds $s(n)$. Each “best recorded value” and “register value” is `main`’s current row
  at that count, and each improvement and gain is the exact difference, rounded as
  printed.
- **Your construction statements hold exactly.** 539, 590, 794, 851, 867 and 910 are
  their parents (494, 543, 739, 794, 810, 851) square for square, plus an L of 45 to 59
  axis-aligned squares along the top and right, at side plus 1 exactly.
  809 is 810 with its last square removed, at the same side.
- **Against the record.** Every count lies beyond the case corpus (1 to 324). At 36
  counts each side lies below `main`’s current beyond-horizon row and below every
  current row at a larger count.
  At 655 `main` has no row; the 26 you cite is the 26 × 26 grid.
- **Custody and licence.** Every retained file equals the SHA256SUMS kept beside it, and
  the 16 files of #942 are unchanged at `a0c4fc80`. The three packets keep no `LICENSE`.
  The root README at each pin releases all files under MIT, and this repository already
  holds your MIT notice from the same repository (F8).

## Scope

**Read.**

- The runbook’s stage 4
  ([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)) and
  its triage rules on reports beyond 324.
- The structural precedents
  [review-2026-11-11-ozden-943-947.md](review-2026-11-11-ozden-943-947.md) (its text and
  its packet README) and the first twelve lines of
  [review-2026-11-11-de-winter-939-946.md](review-2026-11-11-de-winter-939-946.md), to
  confirm that it reviews other reports (#939 and #946), not these.
- Issues #941 and #942 and the comment on #942, through GitHub’s REST API, kept as
  `programs/issues-941-942.json`.
- From the three packets on the import branch, as data: the 37 certificates, the
  `README.md` and `SHA256SUMS` of each retained folder, and each `source/README.md` (the
  upstream root README at each pin).
  The 941 packet’s `verify_cert.py` was hashed and not read.
- On `main` at `591644a9e`: `packing/frontier/source-coverage.yaml` (its
  `beyond_horizon_claims`), `results.yaml` (scope only) and the two earlier de Winter
  packets’ `LICENSE` files and pin lines.

**Run.** Twelve Python programs and modules of my own, importing nothing from this
repository or the source ([What I Ran](#what-i-ran)).

**Seen before my findings were written**, disclosed as the runbook asks: the brief,
which names the reports, the pins, the comment time, lane L90’s branch and head, and
asks for judgments on the issue-versus-commit provenance, the licence, and the horizon.
Also the import branch’s file list (`git diff --stat`), which names the lane’s
`acquisition/`, `measure/contraction-*` and `measure/identity-*` files; none was opened.

**Not read before my findings were frozen.** The packets’ root `README.md` files (the
lane’s notes), everything under `acquisition/`, `measure/` and `receipts/`, lane L90’s
register rows, evidence, ledger and notes, `verify_cert.py`, and this repository’s
`sqpack`, `devtools` and crate code.

**Not run here.** Any of the author’s code or of the maintained routes.

**Not reviewed.** The statements of local optimality (“less than 1e-43 above the local
optimum” at 413, 543 and 547, “about 5e-9 above the numerical optimum” elsewhere); the
sub-window lineage from Francisco Couzo’s packings at 544, 539, 590, 696, 851 and 868,
and 753 from 810; that #942’s arrangements are those of the Kaggle merge file
`Samanyu-dev/squares_in_squares@53551d7`, which is not retained; and the upstream blobs
and commit times at the three pins, which this session could not reach (F12).

## The Claim and What It Needs

For each $n$ the report claims $s(n) \le C$, where $C$ is its 10-place print.
The certificate proves $s(n) \le L$ for its side $L$: there are $n$ closed unit squares,
rotated freely, with pairwise disjoint interiors inside the closed square $[0, L]^2$.
Since $C \ge L$, the claim follows.

The format, from each file’s first comment line and the README: comment lines, then
`n L`, then one line `x y t` per square, where $(x, y)$ is the centre and
$t = \tan(\theta/2)$. Every scalar is an integer or $p/q$. A square is then
$$u = \left(\tfrac{1 - t^2}{1 + t^2}, \tfrac{2t}{1 + t^2}\right), \quad v = u^\perp, \quad
\text{corners } (x, y) \pm \tfrac{u}{2} \pm \tfrac{v}{2},$$ and since $|u| = 1$ exactly
for every rational $t$, the parametrization makes every square a unit square.
The hypotheses are: the reading, the count, unit squares, containment and disjoint
interiors. The rotation sense does not affect soundness: the claim is existential, so a
packing accepted under the reading the checker uses proves the bound.
Control C1 shows the reading is the one the files intend, since the opposite sense
breaks every file.

`l96_check.py` decides the first two through the reader and the rest twice.

- **The reader** (`l96_read.py`) fails closed on any byte it does not expect: non-ASCII,
  a carriage return or tab, a missing final newline, a comment after the header, a blank
  or padded line, a decimal point, a sign other than a leading minus, a leading zero, a
  zero denominator, `-0`, or a line count other than $n$. It hands both methods integer
  pairs. All 84,505 scalars in the 37 files are in lowest terms.
- **Method A** (`l96_sat.py`, `fractions.Fraction`). Containment uses the exact
  half-extent $h = (|\cos\theta| + |\sin\theta|)/2$, giving the four clearances $x - h$,
  $y - h$, $L - x - h$ and $L - y - h$. A pair’s margin is the largest gap over the four
  edge normals $a$ of $|a \cdot d| - h_i(a) - h_j(a)$, with
  $h_k(a) = (|a \cdot u_k| + |a \cdot v_k|)/2$: positive is apart, zero is contact,
  negative is overlap.
  A pair whose exact bounding boxes are strictly apart along $x$ or $y$ is decided apart
  by that axis-aligned line, through a sweep over the boxes sorted by left edge, and
  every other pair gets the full margin.
- **Method B** (`l96_clip.py`, `gmpy2.mpq`). Each square is built as four corners and
  accepted when its edges have squared length 1, every turn has cross product $+1$, and
  its shoelace area is 1. Containment is the corners’ least distance to each wall.
  A pair is clipped by the other square’s four closed half-planes: empty is apart, a
  non-empty result of area 0 is contact, positive area is overlap.
  Pairs whose centres are more than $\sqrt 2$ apart ($d^2 > 2$, exactly) are decided
  apart without clipping, since each square lies in the disc of radius $\sqrt 2 / 2$
  about its centre. Pairs are enumerated by integer cells $\lfloor x \rfloor$,
  $\lfloor y \rfloor$, taken by exact integer division; pairs whose cells differ by 3 or
  more have centres more than 2 apart.

The two methods share only the reader and the format’s formula above.
They prune by different lemmas (axis-aligned lines for A, the circumscribed disc for B),
so a pair one method decides without its full test is decided in full by the other
wherever their prunes differ.
The verdict is `ACCEPT` only when both methods accept every square, wall and pair, their
four clearances per square are equal as exact rationals, and their contact and overlap
sets are equal.

## The Certificates Decided

| Group | Files | Squares | Pairs | A: by axis line | A: by margin | B: not enumerated | B: by disc | B: clipped |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| all 37 | 37 | 28,156 | 11,093,138 | 11,060,613 | 32,525 | 10,797,233 | 226,008 | 69,897 |

- **Reading.** All 37 files read strictly: two comment lines each, $n$ square lines, no
  scalar outside lowest terms.
- **Squares.** Every square is a unit square by both methods.
- **Walls.** Every square lies in its box by both methods, with equal clearances.
  338 square–wall contacts, all in the six bordered files; every other certificate keeps
  every square off every wall.
- **Pairs.** No pair overlaps by either method, and the classes agree everywhere.
  The 964 touching pairs all involve a border square: the re-optimized cores touch
  nothing. The nearest pair decided by an axis-aligned line is $5 \times 10^{-46}$ apart,
  at 413, 543, 547 and 590.
- **Verdict.** `ACCEPT` at all 37.

`l96_selftest.py` holds both methods and the reader to 72 cases and passes:

- edge, corner and 3-4-5 vertex–edge contacts ($t = 1/3$), each also swapped and
  transposed; their $10^{-30}$ overlaps of area $10^{-30}$, $10^{-60}$ and
  $\tfrac{25}{24} \cdot 10^{-60}$; the same pairs $10^{-30}$ apart;
- a duplicate (margin $-1$, area 1), $t = 1$ read as a quarter turn, and a square
  against its own 3-4-5 rotation (margin $-6/5$, area $5/6$, derived by hand);
- walls at contact and $10^{-30}$ past, in both rotation senses;
- 23 malformed files the reader must refuse, each for its own reason, and two it must
  accept;
- 300 random rational pairs closed along their centre line to exact contact and
  $10^{-30}$ either side;
- both methods’ pruned decisions against brute force over every pair of 25 random dense
  sets of 30 squares.

## Controls

`frozen/controls-plan.json` states the outcome of nine controls for each file.
`l96_controls.py plan` wrote it from exact facts of the unmodified files (clearances,
margins, each near pair’s closing move), deciding no modified file, and its digest
(`c815af9a…`) was recorded at 15:11:17Z before `run` decided any.
“Contact” is a margin or clearance of exactly 0, and “past” is $10^{-30}$ beyond it.

| Control | Stated | Result |
| --- | --- | --- |
| C1. Every $t$ negated (the rotation read the other way) | refused for overlapping pairs, equal by both methods; every square still inside with the same contacts | as stated at all 37: 69 to 592 overlapping pairs |
| C2. The side lowered by $1/q$, one unit of its own last place | refused for exactly the far-wall contact squares, or accepted where none touches | as stated: 45, 47, 55, 57, 57 and 59 squares outside in the bordered files, accepted elsewhere |
| C3. The side set to its 10-place floor | outside exactly the squares whose right or top clearance is below the drop | as stated: 21 to 59 outside at 413, 543, 547 and the six bordered files; accepted at the other 28, whose wall gaps exceed the drop (F6) |
| C4. The side set to its 10-place ceiling, the claim | accepted, contacts at the left and bottom walls only | as stated at all 37 |
| C5. The last square given square 1’s $(x, y, t)$ | refused: exactly the pair $(1, n)$ overlapping, margin $-1$, area 1 | as stated at all 37 |
| C6. Square 1 translated by $(L, 0)$ | refused: square 1 outside the right wall only, no pair overlapping | as stated at all 37 |
| C7. Every pair with margin below $10^{-9}$, or touching, closed along its centre line | contact at the closing move, overlap $10^{-30}$ past, by both methods | as stated: 64,223 pairs (none at 805, whose nearest pair is $1.41 \times 10^{-9}$ apart) |
| C8. Every square moved to its nearest wall by its clearance | contact there, outside $10^{-30}$ past, by both methods | as stated: 28,156 squares |
| C9. Every square transposed, $(x, y, t) \mapsto (y, x, -t)$ | accepted; contacts transposed; every margin decided both times exactly equal; clearances transposed | as stated at all 37 |

Every control came out as stated at every file: `EVERY_CONTROL_AS_STATED`.

- **C7.** The closing move is exact: moving square $j$ by $-\lambda d$ along the centre
  line, the margin is $\max_a (|a \cdot d|(1 - \lambda) - h_i(a) - h_j(a))$, a maximum
  of decreasing lines, so contact comes first at
  $\lambda^\ast = \max_a \bigl(1 - (h_i(a) + h_j(a)) / |a \cdot d|\bigr)$. Method B,
  which shares none of that algebra, finds contact at $\lambda^\ast$ and overlap past it
  for all 64,223 pairs.
- **C9.** The transposed files’ margins equal the originals’ exactly wherever method A
  decided the pair by margin both times (134 to 2,116 pairs per file), which holds A to
  the symmetry it should have; method B’s classes agree as before.

## The Sides and the Prints

`l96_claims.py` parses the three tables and holds every printed number to the exact side
and to `main`’s rows (`out/claims.json`, all 37 rows as printed).

- **The claims.** Every printed new side is the exact side’s ceiling at 10 places.
- **The record values.** Each “best recorded value” (#941) and “register value” (#942
  and the addendum) is `main`’s current beyond-horizon row at that count, rounded to 10
  places. At 809 the row, 28.908036098650, is exactly half way, and the print
  28.9080360986 rounds it down.
  At 655 the print is 26.0000000000, and `main` has no row.
- **The differences.** Each #941 “improvement” is the row minus the exact side, rounded
  to six places. Each #942 and addendum “gain over best public” is the printed public
  value minus the exact side, to two significant figures.
  The public values themselves are not checked here.
- **The READMEs.** Each folder’s README table equals the report’s table row for row: 15
  rows in `above324/README.md`, 16 in `above324_refined/README.md` at `a9486ede`, and 22
  at `a0c4fc80`, the six addendum rows included.

## The Construction Statements

`l96_construct.py` holds #941’s statements to the files exactly (`out/construct.json`,
`AS_STATED`).

| Child | Parent | Stated | Parent’s squares in child, unchanged | Added, all $t = 0$ | Right column, top row | Side |
| ---: | ---: | --- | --- | ---: | --- | --- |
| 539 | 494 | border of 45 | yes, as a prefix | 45 | 22, 23 | parent + 1 |
| 590 | 543 | border of 47 | yes, as a prefix | 47 | 23, 24 | parent + 1 |
| 794 | 739 | border of 55 | yes, as a prefix | 55 | 27, 28 | parent + 1 |
| 851 | 794 | border of 57 | yes, as a prefix | 57 | 28, 29 | parent + 1 |
| 867 | 810 | border of 57 | yes, as a prefix | 57 | 28, 29 | parent + 1 |
| 910 | 851 | border of 59 | yes, as a prefix | 59 | 29, 30 | parent + 1 |

Each border is $\lfloor L \rfloor + \lfloor L + 1 \rfloor$ squares for the parent side
$L$, the capacity of an L-strip of width 1. 809 is 810 without square 810, centred at
about (28.408, 23.408) with $t \approx -7.6 \times 10^{-12}$, at the same side.

`l96_extent.py` measures each packing’s exact extent, the least box it fits after a
translation (`out/extent.json`).

- At 413, 543 and 547 every wall gap is $5 \times 10^{-46}$ and the nearest pairs are
  $10^{-45}$ apart, which agrees with a side placed $10^{-45}$ beyond a tight
  arrangement. The 1e-43 statement itself is not reviewed.
- The bordered files touch all four walls, so their extent is their side.
- The other 28 files leave $1.00$ to $5.3 \times 10^{-10}$ at every wall and about
  $2.0 \times 10^{-10}$ between their nearest pairs.
  Their extents lie $2.0 \times
  10^{-10}$ to $1.19 \times 10^{-9}$ below their sides, so each 10-place ceiling of the
  extent is two to twelve units below the claim (F6).

## Against the Record

`l96_record_rows.py` reads `main`’s `source-coverage.yaml` and `results.yaml` at
`591644a9e` (`out/record-rows.json`).

- **The horizon.** `case_corpus` is 1 to 324. No count here lies inside it, and no
  register entry at `main` has any of the 37 counts in its scope.
- **Existing rows.** 36 counts carry a current `beyond_horizon_claims` row
  (`tracked-outside-case-corpus`), from Francisco Couzo’s `43f666c`, `964ee2b` and #763
  releases (with its recipes), Tymchishin’s `22-3662` and `reclosure-v3`. Each claim
  lies below its row by $7.08 \times 10^{-5}$ (539) to $3.26 \times 10^{-2}$ (991). At
  935 the superseded rows include your own #666 report, 30.995955854834.
- **Monotonicity.** Each side also lies below the least current row at any count at or
  above $n$; at every count but 655 that row is the count’s own.
- **655.** No row. The least current row at a larger count is 26.535533905933 at 677. The
  “register value” 26 is the trivial bound from the $26 \times 26$ grid at 676. This
  review did not compute Göbel’s classical construction at 655, which the record takes
  as an earlier report beyond 324. Whether 25.9996711101 lies below it decides whether
  655 is recorded, and the import lane’s start holds it.
- **Within the reports.** The 37 sides increase with $n$, so no claim is beaten by
  another at a larger count, except that 809 ties 810 (F5).

## Provenance

- **#941** names `71da0d56`, folder `above324`, and its fifteen rows equal that folder’s
  README. **#942** names `a9486ede`, folder `above324_refined`, and its sixteen rows
  equal that README. **The addendum**, comment 6772308414 at 2026-11-10T16:02:47Z, names
  `a0c4fc80` for six further rows of the same folder.
  Its `updated_at` equals its `created_at`, so it was never edited.
- **The six addendum counts date from the comment**, not from #942’s opening at
  14:41:18Z, and their pin is `a0c4fc80`, not `a9486ede`. The 16 files of #942 have the
  same digests in `a0c4fc80`’s SHA256SUMS as in `a9486ede`’s, so either pin carries
  them.
- **The upstream root READMEs agree with the order:** fifteen packings at `71da0d56`,
  then sixteen refined packings added at `a9486ede`, then twenty-two at `a0c4fc80`.
- **What changed in the refined README** between `a9486ede` and `a0c4fc80`: “Sixteen
  packings still had one.
  Following the descent to convergence gave the values in the table” became “Following
  the descent to convergence improved twenty-two packings by at least 1e-6”. #942’s text
  still says sixteen, and the addendum says “the same procedure” (F7).
- **Both issues’ `updated_at`** is the owner’s `intake` labelling at 04:56:33Z and
  04:56:35Z on 11 November; their edit history could not be read here (F12).
- **Not checked here:** the commit times of the three pins, and the upstream blobs.

## What the Checkers Share

- **This review’s checker** shares no code with any other checker.
  It was written and frozen before `verify_cert.py` or any of this repository’s verifier
  code was read. It shares the mathematics above and the format’s meaning, taken from the
  files’ own comment line and the README. It trusts CPython 3.14.7’s integers and
  `fractions`, GMP through `gmpy2` 2.3.1, and the clipping, shoelace and disc identities
  its self-test exercises.
- **The author’s checks.** `verify_cert.py` (SHA-256 `df2bbc33…`, one blob at all three
  pins) runs separating axes in `fractions.Fraction` on pairs with centres closer than
  $\sqrt 2$, by the issues.
  It was not read or run here.
  The issues say a second script of the author’s checked the same packings before the
  files were written, and that the two share one author, the separating-axis test and
  `Fraction`. This review’s method A shares the separating-axis mathematics with them
  (not code), and method B shares neither.
- **Consequence for the record’s words.** This review’s run is independently
  re-implemented, clean room, with full coverage of all 37 certificates.
- **Authorship.** The issues say Claude (Anthropic) produced the search, the
  certificates and the author’s checks under his direction, and this review was written
  by a Claude agent: a shared system family.

## Custody and Licence

`l96_custody.py` digests every retained file and holds it to the SHA256SUMS beside it
(`out/custody.json`).

- **941 packet** (`above324/` at `71da0d56`): the fifteen certificates and
  `verify_cert.py` equal their SHA256SUMS lines.
- **942 packet** (`above324_refined/` at `a9486ede`): the sixteen certificates equal
  theirs. `verify_cert.py` is listed with the 941 copy’s digest and not kept here.
- **Addendum packet** (`above324_refined/` at `a0c4fc80`): the six new certificates
  equal theirs. The other sixteen and `verify_cert.py` are listed with the same digests
  as at `a9486ede` and not kept again.
- **Upstream.** The GitHub API refused `JoostdeWinter/square-packing` in this session,
  so no retained file was held to an upstream blob, and no commit time was read (F12).

**Licence.** Each pin’s root README (`source/README.md`) ends “All files are released
under the MIT licence (see `LICENSE`)”. None of the three packets retains that
`LICENSE`. `main` holds this repository’s MIT notice, “Copyright (c) 2026 Joost de
Winter” (blob `17e795f2`), in `de-winter-upper-bounds-227-229-260-2026-10-17/source/`,
retained from `9bf5d9be`, the 17 October commit that added it.
The same bytes are in the #666 packet from his site repository.
Whether the blob is unchanged at the three new pins is not checked here (F8).

#942’s starting packings are not his: they come from a merge of public Kaggle notebooks
and datasets. The licence terms of those notebooks and of the merge file
`Samanyu-dev/squares_in_squares@53551d7` are stated nowhere in the source and are not
retained (F8).

## Findings

| Id | Severity | Where | Finding |
| --- | --- | --- | --- |
| F1 | note | all 37 certificates | each is an exact packing at its side by both methods, every square, wall and pair; no pair overlaps; every contact (338 with walls, 964 between pairs) involves a border square |
| F2 | note (this review) | the controls | all 333 stated controls came out as stated |
| F3 | note | the three tables | each printed side is the 10-place ceiling; each record value is `main`’s current row, 809’s rounded down at a half-way tie; each improvement and gain is the exact difference as printed |
| F4 | note (records) | horizon and rows | all 37 counts are beyond the case corpus; 36 improve a current beyond-horizon row and lie below every current row at a larger count; 655 has no row, and its standing against Göbel’s construction is the import lane’s to decide |
| F5 | note (records) | #941, 809 and the bordered counts | 809 is 810 less its last square, at 810’s side: a deletion bound claimed in the same issue, which is think-kzme’s open question (whether an issue claiming a deletion count gives it a row); 539, 590, 794, 851, 867 and 910 are exact L-border extensions of 494, 543, 739, 794, 810 and 851, so their bounds follow from their parents’ by the border consequence #941 itself cites, though each certificate stands on its own |
| F6 | note (author) | the re-optimized certificates; each README’s margin sentence | the 28 files outside 413, 543, 547 and the borders leave $1.0$ to $5.3 \times 10^{-10}$ at every wall and about $2 \times 10^{-10}$ between nearest pairs; their extents are $2.0 \times 10^{-10}$ to $1.19 \times 10^{-9}$ below their sides, so the claims are conservative by two to twelve units in the 10th place; the visible margin is not the “about 5e-9” the issues state, which this review cannot measure (it is the side’s distance to a numerical optimum) |
| F7 | note (author; records) | #942 Lineage paragraph; `above324_refined/README.md`:34 at `a0c4fc80` | #942 says sixteen of the 1000 packings still had a descent direction; the README at `a0c4fc80` says the descent improved twenty-two by at least 1e-6, and the addendum calls its six “the same procedure”; the record should quote the README of the pin it cites |
| F8 | minor (records) | the three packets; `source/README.md` at each pin | no `LICENSE` retained, though each pin’s README releases all files under MIT “(see LICENSE)”; `main` holds the same repository’s notice (blob `17e795f2`, from `9bf5d9be`), whose blob at the new pins was not checked here; the licences of #942’s Kaggle starting packings and of the merge file are not stated or retained |
| F9 | minor (records) | #942 Claim and Lineage; #941 Not done | #942’s arrangements are other people’s public packings, not credited individually, and its steps over the best public packing are $1.8 \times 10^{-7}$ to $3.8 \times 10^{-4}$, while its steps over the record are $1.0 \times 10^{-3}$ to $3.3 \times 10^{-2}$; #941 says public Kaggle submissions hold smaller packings at 14 of its 15 counts (all but 543); the record’s words should call these bounds below the record, not the best known packings, and credit the arrangements’ origin |
| F10 | minor (records) | provenance | the six addendum counts are reports of comment 6772308414 at 2026-11-10T16:02:47Z, pinned at `a0c4fc80`, not of #942 at 14:41:18Z or `a9486ede`; the record should date and pin them so |
| F11 | note (records) | the 942 and addendum packets | `verify_cert.py` is kept only in the 941 packet, and the addendum packet keeps only its six new certificates; custody of the other copies rests on identical SHA256SUMS lines |
| F12 | note (this review) | process | the runbook asks for the `tbd-strong-max` tier at maximum reasoning, and this review ran as `tbd-strong`; the GitHub API refused the upstream repository and GraphQL, so upstream blobs, commit times and the issues’ edit history were not checked |
| F13 | note (this review) | `check-nNNNN.json`, `positive_margins_below` | it counts only the pairs method A decided by margin; near pairs decided by an axis-aligned line (down to $5 \times 10^{-46}$ apart) are not in it; the plan’s census (C7: 64,223 pairs below $10^{-9}$) counts every pair within centre distance 2 |

## Questions for the Author

1. #942 says sixteen packings still had a descent direction, and the README at
   `a0c4fc80` says twenty-two improved by at least 1e-6. Were the six addendum counts
   below the 1e-6 threshold at first, or found by a later run?
2. Under what licence did the Kaggle notebooks and datasets publish the starting
   packings, and does the merge file state one?
3. Can the individual authors of the 22 refined arrangements be identified, for example
   by the notebook each came from?
4. What does “a margin of about 5e-9 above the numerical optimum” measure?
   The certificates leave about $10^{-10}$ at each wall and $2 \times 10^{-10}$ between
   nearest pairs.
5. Is 809 meant as its own claim, or as the deletion bound from 810?

## What I Ran

All with CPython 3.14.7 through `uv run --frozen --all-extras --group dev python -I -B`
from `packing/`, under `nice -n 19`, at most two processes, on a host shared with the
import lane. The programs, the frozen files and the shared receipts are in
[the 941 packet’s review directory](../../../packing/resources/web/de-winter-issue941-2026-11-10/review/review-2026-11-11/README.md).
Each count’s receipts are in its own packet’s `review/review-2026-11-11/out/`.
`l96_digests.py` holds every receipt that names programs to the kept bytes, and the
checker and plan to their frozen digests: `ALL_RECEIPTS_MATCH` over 80 receipts.

| Program | Receipt | CPU |
| --- | --- | ---: |
| `l96_selftest.py` | `selftest.json`: `PASSED`, 72 cases | 1 s |
| `l96_check.py`, all 37 | `check-nNNNN.json`: `ACCEPT` at all 37 | 24 s |
| `l96_record_rows.py` | `record-rows.json` | a few seconds |
| `l96_claims.py` | `claims.json`: 37 rows, none not as printed | under 1 s |
| `l96_controls.py plan` | `frozen/controls-plan.json` | 17 s |
| `l96_controls.py run`, all 37 | `controls-nNNNN.json`: `EVERY_CONTROL_AS_STATED` at all 37 | about 9 min |
| `l96_construct.py` | `construct.json`: `AS_STATED` | under 1 s |
| `l96_custody.py` | `custody.json` | under 1 s |
| `l96_extent.py` | `extent.json` | a few seconds |
| `l96_digests.py` | `program-digests.json`: `ALL_RECEIPTS_MATCH` | under 1 s |

What went wrong along the way, and was redone before any receipt was kept: method B
first took cells through `gmpy2.floor`, which rounds through `mpfr` and is not exact for
these rationals. It was replaced by integer floor division before the first run.
`l96_claims.py` first counted a print that matched the rounded row but not the cut one
as a failure; it now records which rule matched.
No checker file changed after the freeze.

## Verdict

**Accepted at all 37 counts.** Each certificate proves $s(n) \le L$ at its side exactly,
and each report’s 10-place claim bounds $s(n)$.

- Every hypothesis holds exactly, for every square, wall and pair, by two methods that
  agree everywhere.
- Every control is decided as stated beforehand.
- No defect of a certificate or of its mathematics is open.
  The three minor findings (F8, F9, F10) are about the record’s licence, credit and
  dating of these reports.

Mapped as an adversarial review with verdict `accepted`, it supports each beyond-horizon
row at assurance verified, provided `l96_check.py`’s run is registered as exact evidence
replayed with full coverage of all 37 certificates.
That reads as confirmed, independently re-implemented, clean room, by a Claude agent, a
system family that also produced the certificates and the author’s checks.
Whether 655 is recorded turns on Göbel’s construction there, which this review did not
compute.

## Frozen Findings

The checker was frozen at 2026-11-11T15:10:54Z: `frozen/checker-frozen-digests.txt`
(SHA-256 `3d65e3ebf69621acc4d6fd253d49f4c3ffd0d5cc2f14a3f2339faad35b71a8c0`) holds the
five checker files’ digests:

| File | SHA-256 |
| --- | --- |
| `l96_read.py` | `45ae2270ac50e7edd8c6cf49b0cae55d298a3931bc4db933e6349bd8f90e1f29` |
| `l96_sat.py` | `c09e123ab57545907ffc388d3f34f831919b509a55a1202987dec5273b41b9a1` |
| `l96_clip.py` | `8b0e5e21a0b01b3faa81b8059b2d973d31b9891eccde60cb301489fcc24ac728` |
| `l96_check.py` | `88bca816c37b02a16df53f400ce3c2272d860def44c5f7b78b2919687aff8131` |
| `l96_selftest.py` | `fe187127e14fe25bc90fe3b7c19189cc1bb191a84b13187dce170f418adae4ef` |

The controls plan was stated at 15:11:17Z: `frozen/controls-plan.json` SHA-256
`c815af9ac5213905150530133f5ea90186b5f835c96c8790037e1d231b10cfb5`, with
`l96_controls.py` at `205969366bf308792fa2eb017676d1f0f8c6aa9a99a88727680228c97b951e7a`.
The findings above were frozen before anything of the import lane’s was opened; the
frozen text is kept as
`frozen/review-2026-11-11-dewinter-941-942-upper-bounds.frozen.md`, and its SHA-256 is
recorded below with the reconciliation.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
