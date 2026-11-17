# Kaelan Yim’s Certificates in vitamoon/vitamoon: Stage 4 Mathematical Review

**Date:** 2026-11-09. **Subjects:** fifteen exact rational certificates by Kaelan Yim
(GitHub `vitamoon`), published in the watched repository
[vitamoon/vitamoon](https://github.com/vitamoon/vitamoon/tree/ac14112009f5668b464170dcd979334a5537521d)
with no issue:

- `n299.cert` (first committed at `e4209f6`), `n130.cert` (`c10e094`) and `n303.cert`
  (`546928a`), at the pin `ac14112`;
- the first `n303.cert`, committed at `78eb9ea` and replaced at `546928a`;
- eleven certificates beyond the horizon, at n = 553, 599, 600, 601, 602, 604, 645, 647,
  648, 699 and 700, committed at `78eb9ea` and unchanged at `ac14112`.

Bead `think-i5a5`, a child of `think-3guf`.

**Reviewed at:** `main` `ef1af4933`, the record each claim is measured against, and the
pins `ac14112` and `78eb9ea`.

**Reviewer:** Claude (AI review), strong tier (`tbd-strong-max`) at maximum reasoning,
the stage 4 mathematical review lane (L70), separately prompted.
It shared no context with the import lane (L65, bead `think-h96r`), which registers the
same certificates in draft pull request #934. It read the source as data and ran only
programs of its own, kept with their receipts in
[the review directory](../../../packing/resources/web/yim-certificates-2026-11-09/review/review-2026-11-09/README.md).
It is not a human oversight record.

## Summary for the Author

**Verdicts: all fifteen certificates are valid.** At 299, 303 and 130 the gain lies
inside the predecessor’s own padding; the first 303 is not below the standing value; the
eleven beyond the horizon are new rows. No finding is blocking. F4 is major and is the
owner’s RV-3 question; the rest are notes.

| n | Commit | Exact side (floor, 20 places) | Rounded up at 12 | Least pair margin | Standing value | Gap | Verdict |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 299 | `e4209f6` | 17.80100443425411170800… | 17.801004434255 | $1.0 \times 10^{-30}$ | T-277 | $1.18197 \times 10^{-12}$ | valid; inside T-277’s padding (F4) |
| 303 | `546928a` | 17.90178927315319928566… | 17.901789273154 | $5.79 \times 10^{-15}$ | T-278 | $3.29105 \times 10^{-12}$ | valid; inside T-278’s padding (F4) |
| 130 | `c10e094` | 11.90243064598224620420… | 11.902430645983 | $1.82 \times 10^{-14}$ | T-259 | $1.95544 \times 10^{-14}$ | valid; T-259 re-boxed, same print (F5) |
| 303 | `78eb9ea` | 17.90178927329547775570… | 17.901789273296 | $1.82 \times 10^{-16}$ | T-278 | $-1.38987 \times 10^{-10}$ | valid; above T-278 (F6) |
| 553 | `78eb9ea` | 23.96914523866768961365… | 23.969145238668 | $1.51 \times 10^{-15}$ | Couzo | $6.29061 \times 10^{-4}$ | valid; a new row (F7) |
| 599 | `78eb9ea` | 24.93647968124519841831… | 24.936479681246 | $9.54 \times 10^{-16}$ | Couzo | $8.16493 \times 10^{-4}$ | valid; a new row |
| 600 | `78eb9ea` | 24.95109027532072059029… | 24.951090275321 | $6.56 \times 10^{-16}$ | Couzo | $3.24664 \times 10^{-4}$ | valid; a new row |
| 601 | `78eb9ea` | 24.95807047692749947032… | 24.958070476928 | $2.18 \times 10^{-16}$ | Couzo | $3.81786 \times 10^{-4}$ | valid; a new row |
| 602 | `78eb9ea` | 24.98129894963014253637… | 24.981298949631 | $7.07 \times 10^{-15}$ | Couzo | $1.86710 \times 10^{-4}$ | valid; a new row |
| 604 | `78eb9ea` | 24.99588048822511787648… | 24.995880488226 | $2.15 \times 10^{-16}$ | Couzo | $9.47373 \times 10^{-4}$ | valid; a new row |
| 645 | `78eb9ea` | 25.88138553740098334114… | 25.881385537401 | $6.89 \times 10^{-16}$ | Couzo | $1.72369 \times 10^{-3}$ | valid; a new row |
| 647 | `78eb9ea` | 25.89927296878919759109… | 25.899272968790 | $3.82 \times 10^{-15}$ | Couzo | $3.62529 \times 10^{-6}$ | valid; a new row |
| 648 | `78eb9ea` | 25.90880357698094804555… | 25.908803576981 | $5.57 \times 10^{-15}$ | Couzo | $3.31283 \times 10^{-5}$ | valid; a new row |
| 699 | `78eb9ea` | 26.90731111831429741761… | 26.907311118315 | $1.05 \times 10^{-14}$ | Couzo | $2.60750 \times 10^{-4}$ | valid; a new row |
| 700 | `78eb9ea` | 26.90803610271720290961… | 26.908036102718 | $5.00 \times 10^{-15}$ | Couzo | $5.92887 \times 10^{-5}$ | valid; a new row |

- **How the bounds were checked.** A clean-room exact checker, written and frozen for
  this review before any of this repository’s witness or verifier code was read, decided
  every file: every square, every wall and every pair, with no distance filter, by two
  methods that share only the reader. They are separating axes in Python fractions and
  exact clipped areas in GMP rationals.
  They agree on all 2,314,078 pairs and all 7,933 squares.
  Every pair is strictly apart and every square strictly inside: no file has a contact.
- **Controls.** Of 300 controls stated in advance (20 per file), 283 came out as stated.
  The 17 that missed were this review’s own constructions or wording: closing the least
  pair at 130 also closes a pair tied with it, and method B’s containment test presumes
  the unit square it has just refused. An addendum of 45 controls, also stated in
  advance, replaced them: all 45 came out as stated. Reading the rotation the other way breaks
  every file (44 to 247 overlapping pairs).
  Lowering the side by one unit of its own last place breaks none: every far wall clears
  by at least $5 \times 10^{-31}$, far more than $1/q$.
- **Your prints.** Each 12-place side in `PACKINGS.md` is the exact side rounded up, so
  each bounds $s(n)$. The JSON’s exact sides are the headers, its decimals are the exact
  values rounded at 78 places, and its improvements are the exact gaps rounded at 79
  significant digits.
- **299 and 303: real, and inside the padding.** Measured as the 31 October review
  measured padding (think-ruu2), T-277’s and T-278’s own coordinates shrink uniformly,
  with nothing re-solved, by $3.404 \times 10^{-12}$ and $3.402 \times 10^{-12}$. Your
  gains are 0.347 and 0.967 of that, and those contracted predecessors lie
  $2.22 \times 10^{-12}$ and $1.11 \times 10^{-13}$ below your certificates.
  T-259 against T-254 (S1) was 0.92; T-265 against T-257, your 260 (S2), was 9.97.
  Whether such a gain is a new result is the owner’s open RV-3 question.
- **130.** It is T-259’s packing exactly, every centre translated by the same
  $(-9.94 \times 10^{-15}, -9.89 \times 10^{-15})$ and every orientation kept, in a box
  fitted with $10^{-30}$ of padding. It keeps T-259’s print, as you say yourself.
- **The first 303.** It is $1.39 \times 10^{-10}$ above T-278 and keeps all of T-272’s
  ids: a further arrangement of Evan Daniel’s packing, found alongside Özden’s. You
  replaced it at `546928a`.
- **Beyond the horizon.** Each of the eleven pairs one to one with Couzo’s retained
  certificate at its count, keeping every id. 600 and 700 move no square beyond a tenth;
  the other nine move 1 to 22. Each is below Couzo’s current row by $3.6 \times 10^{-6}$
  (647) to $1.7 \times 10^{-3}$ (645), from 16.8 (648) to $1.6 \times 10^{9}$ (553)
  times that certificate’s own padding.
- **Custody and licence.** The commits, trees and digests are as you state. The 299 has
  no licence notice of its own (question 3).
- **Significance.** S1 at 299, 303 and 130 if the owner records them, as T-259 is;
  none for the first 303. Rows beyond the horizon carry no score.

## Scope

**Read.**

- `packing/campaign/result-import.md` (stage 2, the rulings of 23 October and the
  reading of watched repositories) and `epistemics.md` (the ladders, the status table and
  the significance scale).
- The precedents: the 9 November review of Özden’s five certificates (the format here),
  the 5 November review of your 260 (T-265), and the 31 October review of the project’s
  candidates at 130, 293 and 307 (think-ruu2), whose RV-3 is the owner’s question and
  whose contraction is the measure used here.
- `packing/witnesses/witness.schema.yaml`, for the two corner files.
- On `main` `ef1af4933`: the register entries T-254, T-259, T-265, T-272, T-277, T-278
  and T-279; the beyond-horizon rows of `source-coverage.yaml` at the eleven counts; the
  retained certificates of T-277, T-278, T-259, T-254, T-257 (260), T-265 and T-272, and
  Couzo’s eleven; the #763 packet’s README; the known-best packet’s “Retained Factual
  Data”; think-ikku’s notes.
- The source as data, from a bare clone: the fifteen certificates and their text copies,
  `PACKINGS.md`, `README.md`, `SHA256SUMS` and `packing-certificates.json` at both pins,
  and the two licence notices.

**Run.** Programs of my own, importing nothing from this repository or the source
([What I Ran](#what-i-ran)). They decide the fifteen certificates, the three predecessors
and Couzo’s eleven by two methods, run a self-test, 300 controls stated in advance and a
45-control addendum, do the side arithmetic, measure the contraction margins of RV-3,
describe how the coordinates were made, measure each certificate against its
predecessor, check custody, and hold every receipt to the programs’ digests.

**Seen before my findings were written**, disclosed as the runbook asks:

- the coordinator’s brief for this lane, which states the pins, the gaps in round figures, the
  import lane’s draft identifiers (T-280 and T-281, with the question whether one table
  gives T-280 twice), its holds at V0/C0, its credit line, its licence position and
  `reported_at`, and its contraction shares 0.35, 0.97 and 0.09 against the precedents’
  0.92 and 9.97;
- the register entries and rows named above, with their notes;
- the three precedents, which state their own reviewers’ results.

**Not read before my checker was frozen** (2026-11-09T14:05:49Z): any of this
repository’s witness, verifier or review code. The source holds no code.

**Not read before my findings were frozen.** Lane L65’s branch, pull request #934, bead
`think-h96r`, packet and receipts, and its `devtools/contraction_margin.py`.

**Not run here.** Any of the author’s checks (Daniel’s two checkers, the local rational
verifier, the two registry routes) or of the maintained routes.

**Not reviewed.** The author’s numerical search and its audit (the JSON’s cohort and
protocol statements), on which no certificate depends; the adoption; the owner’s answer
to RV-3.

## The Claim and What It Needs

For each certificate the claim is $s(n) \le S$ at its stated side $S$: $n$ closed unit
squares, rotated freely, with pairwise disjoint interiors inside the closed square
$[0, S]^2$. Each 12-place print in `PACKINGS.md` is the side rounded up, so it bounds
$s(n)$ too.

**The format.** Every file is in Evan Daniel’s format, as `packing-certificates.json`
states it (“`n L` header, followed by exactly `n` rows `x y t`; rational
$t = \tan(\theta/2)$”) and the files show: one comment line starting with `#`, the header
`n S`, then $n$ rows of three tokens, each an integer or $p/q$. Row $k$ is the square
$Q_k = \{(x, y) + \alpha u + \beta u^\perp : \lvert\alpha\rvert, \lvert\beta\rvert \le 1/2\}$
with $u = ((1 - t^2)/(1 + t^2), 2t/(1 + t^2))$ and $u^\perp = (-u_y, u_x)$.

The claim needs six hypotheses, each checked separately:

1. **The reading.** UTF-8 with a final newline, no carriage return or tab, comments only
   before the header, single spaces, ASCII data, every token an integer or $p/q$ with
   $q > 0$, and exactly $n$ rows of three tokens.
2. **The side.** The header side is the fraction `packing-certificates.json` states.
3. **Unit squares.** With $p_0, \ldots, p_3$ the corners
   $(x, y) \mp u/2 \mp u^\perp/2$ in counterclockwise order, $e_1 = p_1 - p_0$ and
   $e_2 = p_3 - p_0$: $e_1 \cdot e_1 = 1$, $e_2 = \pm e_1^\perp$ and
   $p_2 = p_0 + e_1 + e_2$ (method A). Four unit edges, four turns of one sign and area
   exactly 1 (method B). For rational $t$ this holds identically; both methods check it
   anyway.
4. **Containment.** A convex polygon lies in $[0, S]^2$ exactly when its corners do
   (method A), and exactly when, clipped to the box, it keeps its area 1 (method B).
5. **Disjoint interiors.** Two convex polygons have disjoint interiors exactly when, on
   one edge normal of either, their projections overlap in at most a point (method A;
   the pair margin is the largest gap over the four normals, a length). Independently,
   $Q_i \cap Q_j$ is convex and has positive area exactly when its interior is nonempty
   (method B, the intersection clipped exactly).
6. **The rotation sense.** Nothing in a file says whether $t$ turns counterclockwise.
   Read the other way, $u = (c, -s)$, every file overlaps (control G6), so the sense the
   record uses for Daniel’s format is the one that holds.

`l70_check.py` decides hypotheses 1 and 2 through the reader and 3 to 5 twice: method A in
`fractions.Fraction`, method B in `gmpy2.mpq`. The two share only the reader, which
returns integers. The 299 and second 303 files carry UTF-8 in their comment line (“Doğa
Özden”), which the reader allows in comments and refuses in data.

## The Certificates Decided

| n | SHA-256 | Squares turned | Pairs | Least wall clearance (wall, squares) | Least pair margin (squares) | Pairs below $10^{-12}$ | Square–wall pairs below $10^{-12}$ |
| ---: | --- | ---: | ---: | --- | --- | ---: | ---: |
| 299 | `7e496437…` | 125 | 44,551 | $2.78 \times 10^{-17}$, all four walls (left 105, 106, 117 …) | $1.0000 \times 10^{-30}$ (246, 254) | 620 | 54 |
| 303 | `14dbc28d…` | 161 | 45,753 | $5 \times 10^{-31}$, top (291) | $5.7891 \times 10^{-15}$ (25, 249; tied with 92, 97 and 292, 296) | 355 | 34 |
| 130 | `3056cb4d…` | 36 | 8,385 | $10^{-30}$ exactly, left (29), bottom (116), top (20) | $1.8230 \times 10^{-14}$ (33, 41; tied with 33, 42 and 41, 42) | 304 | 38 |
| 303, first | `b8318f81…` | 303 | 45,753 | $7.33 \times 10^{-25}$, bottom (299) | $1.8151 \times 10^{-16}$ (32, 198) | 44 | 41 |
| 553 | `78a92b71…` | 356 | 152,628 | $5 \times 10^{-31}$, bottom (21) | $1.5148 \times 10^{-15}$ (262, 263) | 1,528 | 83 |
| 599 | `98cf7076…` | 599 | 179,101 | $5 \times 10^{-31}$, left (442) | $9.5377 \times 10^{-16}$ (34, 119) | 155 | 65 |
| 600 | `10b422dd…` | 436 | 179,700 | $5 \times 10^{-31}$, bottom (585) | $6.5553 \times 10^{-16}$ (420, 482) | 1,649 | 85 |
| 601 | `d8c55d4f…` | 601 | 180,300 | $6.95 \times 10^{-24}$, bottom (191) | $2.1839 \times 10^{-16}$ (135, 153) | 61 | 59 |
| 602 | `8710f13a…` | 293 | 180,901 | $5 \times 10^{-31}$, left (198) | $7.0659 \times 10^{-15}$ (366, 446) | 1,775 | 89 |
| 604 | `ce7ea7da…` | 396 | 182,106 | $5 \times 10^{-31}$, left (122) | $2.1502 \times 10^{-16}$ (87, 101) | 1 | 93 |
| 645 | `b7a129cf…` | 403 | 207,690 | $5 \times 10^{-31}$, bottom (1) | $6.8922 \times 10^{-16}$ (569, 578) | 1 | 28 |
| 647 | `86ef4d3d…` | 456 | 208,981 | $5 \times 10^{-31}$, bottom (454) | $3.8171 \times 10^{-15}$ (325, 446) | 1 | 68 |
| 648 | `31143862…` | 323 | 209,628 | $5 \times 10^{-31}$, top (617) | $5.5671 \times 10^{-15}$ (313, 438) | 1,874 | 90 |
| 699 | `36bc1c18…` | 324 | 243,951 | $5 \times 10^{-31}$, left (17) | $1.0504 \times 10^{-14}$ (632, 634) | 3 | 49 |
| 700 | `6ef241dd…` | 531 | 244,650 | $5 \times 10^{-31}$, bottom (20) | $4.9977 \times 10^{-15}$ (586, 588) | 1 | 60 |

- **Reading.** Every file reads strictly: one comment line, the header, $n$ rows of
  three tokens, every token in lowest terms, a final newline. Each text copy is its
  certificate byte for byte.
- **Squares.** Every square is a unit square by both methods, listed counterclockwise.
- **Walls.** Every square lies strictly inside its box by both methods; no file has a
  wall contact. The values “$5 \times 10^{-31}$” are $5.000000 \times 10^{-31}$ to seven
  digits, not exactly; 130’s are exactly $10^{-30}$, the JSON’s `strict_wall_padding`.
- **Pairs.** All 2,314,078 pairs are separated by both methods, with equal classes; none
  touches.
- **Verdict.** `ACCEPT` at all fifteen. The three predecessors (T-277, T-278, T-259) and
  Couzo’s eleven certificates are accepted the same way, and the predecessors’ least
  margins equal the record’s: $2.0262 \times 10^{-13}$ (179, 194),
  $2.0128 \times 10^{-13}$ (269, 286) and $1.823 \times 10^{-14}$ (33, 41).

The margins are exact fractions in the receipts; the prints here truncate them.

`l70_selftest.py` holds both methods to known answers and passes 32 cases:

- edge, corner and 3-4-5 vertex–edge contacts, the last in both senses, and their
  $10^{-30}$ overlaps of area $10^{-30}$, $10^{-60}$ and $\tfrac{25}{24} \cdot 10^{-60}$;
- a duplicate (area 1, margin $-1$), and a square against its own rotation by
  $(3/5, 4/5)$ and $(4/5, 3/5)$ (area $5/6$, margin $-6/5$);
- walls at contact and $10^{-30}$ past;
- six shapes both methods must refuse, and a clockwise listing they must accept;
- 600 random rational pairs, each taken exactly to contact along its centre line by a
  third computation (the half-width formula) and $10^{-30}$ either side;
- 400 random squares taken to a wall and past it;
- 27 malformed certificates and 8 malformed corner files the readers must refuse, each
  for its own reason.

## Controls

`controls-plan.json` states 20 controls per certificate and the expected outcome of
each, from the check receipts and a facts program. It was written and hashed (`3b990b46…`,
14:21:32Z) before `l70_controls.py` existed. “Contact” is a margin of exactly 0 by method
A and an intersection of area exactly 0 by method B; “past” is $10^{-30}$ beyond it.
Whole-file controls decide every square, wall and pair by both methods. Wall-level
controls decide every square’s shape, containment and wall contacts by both methods: a
change of side or a common translation changes no pair, and the pairs were decided in
the check. Pair-level and square-level controls decide the pair or the square alone.

| Control | Level | Stated | Outcome at all fifteen |
| --- | --- | --- | --- |
| G1. The last square replaced by a copy of the first | whole file | refused: exactly the pair (1, n) overlapping, margin −1, area 1 | as stated |
| G2. Square 1 translated by $(S, 0)$ | whole file | refused: exactly square 1 outside, no pair overlapping | as stated |
| G3. The last row deleted | reader | refused, $n - 1$ rows | as stated |
| G4. The header count raised by one | reader | refused, $n + 1$ squares | as stated |
| G5. Row 1’s $t$ replaced by `1.5` | reader | refused, not a rational token | as stated |
| G6. The rotation read the other way ($t \to -t$) | whole file | refused, overlapping pairs, equal sets by both methods | as stated: 44 (130) to 247 (599) pairs |
| S1a. The side lowered by $1/q$, one unit of its own last place | wall | **accepted**: every far wall clears by more than $1/q$ | as stated |
| S1b. The side lowered by its least far-wall clearance $c$ | wall | accepted, exactly the far-wall squares at $c$ touching | as stated |
| S1c. The side lowered by $c + 10^{-30}$ | wall | refused, exactly the squares within $10^{-30}$ of $c$ outside | as stated |
| S1d. The side set to its 12-place ceiling (the print) | wall | accepted | as stated |
| S1e. The side set to its 12-place floor | wall | refused, exactly the squares within the shortfall outside | as stated |
| S3a, S3c. Every square moved left (down) by the least left (bottom) clearance | wall | accepted, exactly those squares touching | as stated |
| S3b, S3d. The same, $10^{-30}$ further | wall | refused, exactly those squares outside | as stated |
| S4c. The least-margin pair closed along its centre line to contact | whole file | accepted, exactly that pair touching | as stated at 14; **missed at 130** |
| S4p. The same, past | whole file | refused, exactly that pair overlapping | as stated at 14; **missed at 130** |
| S5. Every pair below $10^{-12}$ closed the same way | pair | touching at contact, overlapping past, by both | 8,372 of 8,372 |
| S6. Every square moved to its nearest wall by its clearance | square | inside with that contact at contact, outside past, by both | 7,933 of 7,933 |
| S7. A square of the least pair, as corners, enlarged by $1 + 10^{-30}$ | whole file | refused for shape by both, nothing outside, no overlap | **missed at all fifteen** |

So 283 of the 300 stated outcomes came out as stated, among them every reader, wall,
side, reversed-sense, near-pair and square control. The 17 misses are this review’s
errors, not the certificates’ or the checker’s verdicts:

- **S4c and S4p at 130.** Pairs (33, 41), (33, 42) and (41, 42) share the least margin,
  $1.823 \times 10^{-14}$, exactly; T-259’s dilation left them so. Moving square 41
  toward 33 closes (41, 42) by the same amount along the same axis, so two pairs touch,
  then overlap, where the plan said one. Both methods saw both pairs.
- **S7 at all fifteen.** Both methods refused the enlarged square for its shape, as
  stated. The plan also expected them to agree that it is inside. Method B decides
  containment by “clipped area exactly 1”, which a square of area $(1 + 10^{-30})^2$
  cannot keep, so B called it outside and A did not. B’s containment test presumes the
  unit-square test it runs first; on every square of every certificate that test passed,
  so no verdict depends on it.

Both first runs are kept. `controls-plan-addendum.json` (`9a4630e9…`, 14:50:42Z) was then
stated before any of its controls ran. It closes the same pairs and enlarges the same
squares, with the touching and overlapping sets computed exactly by the centre
half-width formula for every pair of the moved square, and with each method’s
containment stated separately.

| Addendum control | Stated | Outcome |
| --- | --- | --- |
| S4′c. The least pair closed along its centre line to contact | accepted; touching exactly the pairs the formula puts at 0 (at 130, (33, 41) and (41, 42); elsewhere the least pair alone) | as stated at all fifteen |
| S4′p. The same, past | refused; overlapping exactly the pairs the formula puts below 0 | as stated at all fifteen |
| S7′. The enlarged square, as S7 | refused for shape by both; A: inside; B: outside; no overlap | as stated at all fifteen |

So every near pair of every file was taken to exact contact and $10^{-30}$ past it, every
square to its wall and past it, and every side to the far-wall contact and past it, by
both methods.

## The Sides and the Prints

`l70_sides.py` does the arithmetic exactly.

| n | Digits of $q$ | Side to 40 places (floor) | `PACKINGS.md` | Rounded up at 16 |
| ---: | ---: | --- | --- | --- |
| 299 | 97 | 17.8010044342541117080027897886608557495537 | 17.801004434255, the ceiling | 17.8010044342541118 |
| 303 | 86 | 17.9017892731531992856633983391691014163256 | 17.901789273154, the ceiling | 17.9017892731531993 |
| 130 | 61 | 11.9024306459822462042030375294435824141858 | 11.902430645983, the ceiling | 11.9024306459822463 |
| 303, first | 44 | 17.9017892732954777557097258977771009317293 | 17.901789273296 at `78eb9ea`, the ceiling | 17.9017892732954778 |

- **The claims.** Each side is a fraction in lowest terms. Each `PACKINGS.md` print, at
  all fifteen counts, is the 12-place ceiling, so each bounds $s(n)$. The JSON’s
  `side_exact` is the header exactly and its `side_decimal` the exact value rounded to
  nearest at 78 places; the prose prints of 130, 299 and 303 (“11.90243064598224620420…”
  and so on) are truncations, and “upward to 16 places: 11.9024306459822463” is the
  16-place ceiling.
- **The first 303’s side terminates**: $q = 2^{46} \cdot 10^{30}$, and the numerator is
  $1259726429694979 \cdot (10^{30} + 1)$, so the side is a binary64-sized fraction
  dilated by $1 + 10^{-30}$. 601’s side has the same shape.
- **The predecessors.** The JSON’s `source_exact_side` at 299, 303 and 130 is the side
  of T-277’s, T-278’s and T-259’s retained certificate exactly, and its
  `exact_side_improvement_decimal` is the exact gap rounded at 79 significant digits.

| n | Against | Gap (exact, 14 digits) | Relative | 12th-place units | binary64 spacings | Same 12-place print |
| ---: | --- | --- | --- | ---: | ---: | --- |
| 299 | T-277, 17.80100443425529367352… | $1.1819655270744 \times 10^{-12}$ | $6.64 \times 10^{-14}$ | 1.18 | 333 | no (…255 against …256) |
| 303 | T-278, 17.90178927315649033135… | $3.2910456934182 \times 10^{-12}$ | $1.84 \times 10^{-13}$ | 3.29 | 926 | no (…154 against …157) |
| 130 | T-259, 11.90243064598226575861… | $1.9554409882111 \times 10^{-14}$ | $1.64 \times 10^{-15}$ | 0.02 | 11 | **yes** (…983) |
| 303, first | T-278 | $-1.3898742435291 \times 10^{-10}$ | $-7.76 \times 10^{-12}$ | −139 | −39,121 | no (…296 against …157) |

Beyond the horizon the standing value at each count is Couzo’s current row on `main`
(source `couzo-issue763-2026-10-23`, and `couzo-43f666c-2026-10-24` at 604). Each row’s
printed value is the 12-place ceiling of the certificate the record retains for it, so
the exact gaps below are to those certificates.

| n | Couzo’s side (floor, 20 places) | Row print | Gap (exact) | Relative |
| ---: | --- | --- | --- | --- |
| 553 | 23.96977429970356456569… | 23.969774299704 | $6.29061 \times 10^{-4}$ | $2.62 \times 10^{-5}$ |
| 599 | 24.93729617435207380697… | 24.937296174353 | $8.16493 \times 10^{-4}$ | $3.27 \times 10^{-5}$ |
| 600 | 24.95141493945678186057… | 24.951414939457 | $3.24664 \times 10^{-4}$ | $1.30 \times 10^{-5}$ |
| 601 | 24.95845226251721011481… | 24.958452262518 | $3.81786 \times 10^{-4}$ | $1.53 \times 10^{-5}$ |
| 602 | 24.98148566004813480939… | 24.981485660049 | $1.86710 \times 10^{-4}$ | $7.47 \times 10^{-6}$ |
| 604 | 24.99682786169435683707… | 24.996827861695 | $9.47373 \times 10^{-4}$ | $3.79 \times 10^{-5}$ |
| 645 | 25.88310922594354083044… | 25.883109225944 | $1.72369 \times 10^{-3}$ | $6.66 \times 10^{-5}$ |
| 647 | 25.89927659408099715571… | 25.899276594081 | $3.62529 \times 10^{-6}$ | $1.40 \times 10^{-7}$ |
| 648 | 25.90883670532565714627… | 25.908836705326 | $3.31283 \times 10^{-5}$ | $1.28 \times 10^{-6}$ |
| 699 | 26.90757186800514306900… | 26.907571868006 | $2.60750 \times 10^{-4}$ | $9.69 \times 10^{-6}$ |
| 700 | 26.90809539146696435047… | 26.908095391467 | $5.92887 \times 10^{-5}$ | $2.20 \times 10^{-6}$ |

Every beyond-horizon gap is positive, and each of your sides is below its row’s print as
well as its certificate.

## Is the Improvement Real? The Contraction Margin

The owner’s RV-3 question asks whether a gain inside the predecessor’s padding is a new
result. `l70_contract.py` measures the padding from its definition, as the 31 October
review of the project’s candidates did (think-ruu2): keep every orientation, scale every
centre by one factor $\lambda$, and fit the least box around the result.

- **The factor.** For a pair with $d = c_j - c_i$, all four edge normals see the two
  unit squares at the same total half-width
  $T = (1 + \lvert u_i \cdot u_j\rvert + \lvert u_i \cdot u_j^\perp\rvert)/2$, so the
  interiors stay disjoint exactly when $\lambda \max_w \lvert w \cdot d\rvert \ge T$. The
  least factor is $\lambda^* = \max_{\text{pairs}} T / \max_w \lvert w \cdot d\rvert$,
  rational, and the pair attaining it then touches.
- **The box.** Each square’s half-extent on either axis is
  $h = (\lvert\cos\theta\rvert + \lvert\sin\theta\rvert)/2$, so the contracted side is the
  larger of $\max(\lambda^* x_i + h_i) - \min(\lambda^* x_i - h_i)$ and its $y$ twin.
- **The margin.** The certificate’s side less the contracted side: how far the
  certificate shrinks uniformly with nothing re-solved. It splits into the envelope (the
  box re-fitted at $\lambda = 1$) and the scaling.
- **Checked, not assumed.** Each contracted packing is written out exactly and decided by
  the frozen checker: accepted at the contracted side with the binding pair touching,
  refused $10^{-30}$ below it, and refused at the factor $\lambda^*(1 - 10^{-30})$ with
  that pair overlapping. Every one of the ten measured certificates came out so.

| Predecessor | $1 - \lambda^*$ | Binding pair | Envelope | Scaling | Margin | Contracted side, rounded up at 12 |
| --- | --- | --- | --- | --- | --- | --- |
| T-277 (299) | $2.0262 \times 10^{-13}$ | 179, 194 | 0 | $3.4040 \times 10^{-12}$ | $3.403992 \times 10^{-12}$ | 17.801004434252 |
| T-278 (303) | $2.0128 \times 10^{-13}$ | 269, 286 | 0 | $3.4020 \times 10^{-12}$ | $3.402014 \times 10^{-12}$ | 17.901789273154 |
| T-259 (130) | $1.8230 \times 10^{-14}$ | 33, 41 (and 33, 42; 41, 42) | $1.9554 \times 10^{-14}$ | $1.9875 \times 10^{-13}$ | $2.183057 \times 10^{-13}$ | 11.902430645983 |
| T-254 (130, precedent) | $2.0762 \times 10^{-13}$ | 105, 128 | $2.0 \times 10^{-15}$ | $2.2636 \times 10^{-12}$ | $2.265559 \times 10^{-12}$ | 11.902430645983 |
| T-257 (260, precedent) | $1.2016 \times 10^{-12}$ | 28, 34 | $1.2048 \times 10^{-12}$ | $1.8786 \times 10^{-11}$ | $1.999110 \times 10^{-11}$ | 16.633982502102 |

**Calibration.** The contracted T-257 is $16.633982502101892884666\ldots$, which is the
31 October review’s $16.633982502101892884\ldots$ in every digit it printed, and the
contracted T-259 is its $11.902430645982047452\ldots$. So the measure here is that
review’s.

| Certificate | Against | Gain | Share of the predecessor’s margin | Certificate less the contracted predecessor |
| --- | --- | --- | ---: | --- |
| 299 (`e4209f6`) | T-277 | $1.181966 \times 10^{-12}$ | 0.3472 | $+2.222 \times 10^{-12}$ |
| 303 (`546928a`) | T-278 | $3.291046 \times 10^{-12}$ | 0.9674 | $+1.110 \times 10^{-13}$ |
| 130 (`c10e094`) | T-259 | $1.955441 \times 10^{-14}$ | 0.0896 | $+1.988 \times 10^{-13}$ |
| 303 (`78eb9ea`) | T-278 | $-1.389874 \times 10^{-10}$ | $-40.85$ | $+1.424 \times 10^{-10}$ |
| T-259, precedent | T-254 | $2.082800 \times 10^{-12}$ | 0.9193 | $+1.828 \times 10^{-13}$ |
| T-265, precedent | T-257 | $1.992698 \times 10^{-10}$ | 9.9679 | $-1.793 \times 10^{-10}$ |

**What the shares say.**

- **Every one of the three held gains is inside the padding.** The predecessor’s own
  coordinates, scaled uniformly with nothing re-solved, give a smaller side than the new
  certificate: by $2.22 \times 10^{-12}$ at 299, $1.11 \times 10^{-13}$ at 303 and
  $1.99 \times 10^{-13}$ at 130.
  T-259 against T-254 (S1) is the same kind, at 0.92; T-265 against T-257 (S2) is the
  other kind, its certificate $1.79 \times 10^{-10}$ below the contracted T-257.
- **The new certificates measured the same way.** Uniform contraction of your 299 stops
  at once, at its pair (246, 254) apart by $10^{-30}$, after $5.55 \times 10^{-17}$ of
  envelope; your 303 contracts by $1.007 \times 10^{-13}$. Neither number is the padding
  your files keep, since 606 of the 299’s pairs are still $1$ to
  $2 \times 10^{-13}$ apart: uniform contraction is blocked by the closest pair, and
  yours are uneven. So this review compares each new side with the predecessor’s
  contraction, which is what RV-3 asks, and not contraction with contraction.
- **130 is the envelope alone.** Its contracted side equals T-259’s exactly, as one
  packing translated must, and its gain is T-259’s envelope slack less the
  $2 \times 10^{-30}$ it adds back.
- **The prints.** The contracted T-277 rounds up to 17.801004434252, three units of the
  12th place below your 299’s print; the contracted T-278 has your 303’s print,
  17.901789273154. A rule that reads the print alone (RV-3’s option (b)) would record
  your 299 and 303 and, on the same terms, the predecessors’ own contractions, which no
  one has reported.

**Beyond the horizon** the same measure, without the exact check of each contraction,
puts Couzo’s certificates’ margins at $3.96 \times 10^{-13}$ (553) to
$5.69 \times 10^{-12}$ (699), and higher where his packings are loose:
$4.71 \times 10^{-9}$ at 700, $1.97 \times 10^{-6}$ at 648 and $4.71 \times 10^{-8}$ at
604. Your gains are 16.8 (648), $1.26 \times 10^{4}$ (700), $2.01 \times 10^{4}$ (604),
$7.0 \times 10^{5}$ (647) and $3.7 \times 10^{7}$ to $1.6 \times 10^{9}$ (the other seven)
times those margins, so every one is a gain under any answer to RV-3.

This is the measurement RV-3 asks for. It decides nothing about the owner’s question; it
says that all three held gains fall where the question applies, and that the eleven rows
do not.

## How the Certificates Were Made

`l70_construct.py` measures what the coordinates are; it decides nothing.

| n | Exactly upright | Turned below $10^{-9}$ rad | $10^{-9}$ rad to 0.5° | Beyond 0.5° | Pairs below $10^{-9}$ by size |
| ---: | ---: | ---: | ---: | ---: | --- |
| 299 | 174 (T-277: 43) | 7 (138) | 24 (24) | 94 (94) | 1 at $10^{-30}$, 7 in $[10^{-14}, 10^{-13})$, 606 in $[1, 2) \times 10^{-13}$, 6 above; T-277: 612 in $[2, 3) \times 10^{-13}$ |
| 303 | 142 (T-278: 14) | 11 (139) | 39 (39) | 111 (111) | 135 in $[10^{-15}, 10^{-14})$, 220 in $[10^{-14}, 10^{-13})$; T-278: 355 in $[2, 3) \times 10^{-13}$ |
| 130 | 94 (T-259: 94) | 1 (1) | 2 (2) | 33 (33) | 304 in $[10^{-14}, 10^{-13})$, as T-259 |
| 303, first | 0 | 166 | 24 | 113 | 1 below $10^{-15}$, 43 in $[2 \times 10^{-13}, 10^{-12})$, 406 in $[10^{-12}, 10^{-10})$ |
| 553 to 700 | 0 to 375 | 56 to 388 | 0 to 87 | 169 to 252 | 1,230 to 1,874 per file; Couzo’s: 0 to 1,707 |

- **299.** 131 more squares are exactly upright than in T-277, and 119 squares move by
  more than $10^{-6}$ (by up to $4.25 \times 10^{-4}$). Its pairs
  sit mostly $1$ to $2 \times 10^{-13}$ apart, closer than T-277’s promotion left them,
  with one pair (246, 254) at $10^{-30} + 6.9 \times 10^{-44}$ and all four walls at
  $2.7756 \times 10^{-17}$.
- **303.** Every square moves by at most $4.4 \times 10^{-12}$ and turns by at most
  $9.1 \times 10^{-15}$ radian, and 128 more squares are exactly upright than in T-278.
  The 355 pairs below $10^{-12}$ are T-278’s 355, now $5.8 \times 10^{-15}$ to
  $10^{-13}$ apart where T-278 had 2 to $3 \times 10^{-13}$, and the top wall is padded
  by about $5 \times 10^{-31}$.
- **130.** Nothing moves relative to anything else; see the lineage below.
- **Beyond the horizon.** Each file packs far tighter than Couzo’s at its count (for
  example 1,874 pairs below $10^{-9}$ at 648 against none), and most pad one wall by
  about $5 \times 10^{-31}$.
- **The paddings.** Every file keeps its side a little above its extent: lowering the
  side by $1/q$ breaks none (S1a). The bound needs none of this; it is how the
  rationalization left the files (question 2).

## Identity, Lineage and the Predecessors

`l70_identity.py` measures each certificate pose by pose, in binary64, against its
predecessor’s retained certificate under all eight symmetries of the box, by nearest
centres and by SciPy’s optimal assignment. Where the pairing is the identity it also
compares the two exactly.

| n | Against | Best symmetry | One to one by nearest centres | Same id | Moved beyond $10^{-6}$, $10^{-3}$, 0.1 | Largest move | Turned beyond 1° | Largest turn | Near pairs below $10^{-12}$: shared, new, gone |
| ---: | --- | --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| 299 | T-277 | identity | yes | 299 | 119, 0, 0 | $4.25 \times 10^{-4}$ | 0 | 0.0172° | 609, 11, 3 |
| 303 | T-278 | identity | yes | 303 | 0, 0, 0 | $4.4 \times 10^{-12}$ (exact) | 0 | $5.1 \times 10^{-13}$° | 355, 0, 0 |
| 130 | T-259 | identity | yes | 130 | 0, 0, 0 | $1.4 \times 10^{-14}$ (exact; one translation) | 0 | 0 | 304, 0, 0 |
| 303, first | T-278 | identity | yes | 292 | 271, 192, 9 | 0.257 | 3 | 1.44° | — |
| 303, first | T-272 | identity | yes | **303** | 303, 224, 5 | 0.145 | 16 | 19.0° | — |
| 553 | Couzo | identity | yes | 553 | 553, 316, 1 | 0.108 | 10 | 2.22° | 370, 1,158, 4 |
| 599 | Couzo | identity | yes | 599 | 599, 334, 3 | 0.344 | 22 | 9.37° | 0, 155, 1 |
| 600 | Couzo | identity | yes | 600 | 600, 257, 0 | 0.083 | 9 | 2.32° | 1, 1,648, 0 |
| 601 | Couzo | identity | yes | 601 | 601, 406, 11 | 0.565 | 15 | 21.8° | 0, 61, 107 |
| 602 | Couzo | identity | yes | 602 | 602, 199, 9 | 0.237 | 0 | 0.77° | 1, 1,774, 0 |
| 604 | Couzo | identity | yes | 604 | 604, 250, 17 | 0.299 | 40 | 4.20° | 0, 1, 0 |
| 645 | Couzo | identity | yes | 645 | 645, 624, 10 | 0.156 | 16 | 4.11° | 0, 1, 220 |
| 647 | Couzo | identity | yes | 647 | 646, 161, 6 | 0.135 | 1 | 4.20° | 0, 1, 1 |
| 648 | Couzo | identity | yes | 648 | 648, 141, 3 | 0.171 | 5 | 6.18° | 0, 1,874, 0 |
| 699 | Couzo | identity | yes | 699 | 699, 573, 22 | 0.264 | 1 | 6.14° | 0, 3, 358 |
| 700 | Couzo | identity | yes | 700 | 700, 124, 0 | 0.065 | 0 | 0.71° | 0, 1, 0 |

- **130, exactly.** Every centre differs from T-259’s by the same
  $(-4969999999999999/(5 \cdot 10^{29}), -9889999999999997/10^{30})$, the JSON’s
  `translation_x` and `translation_y`, and every tangent is T-259’s. The side is the
  translated packing’s extent plus $2 \times 10^{-30}$. That is the JSON’s operation,
  exactly: “orientations and relative centers unchanged”.
- **303, exactly.** Relative to square 1, 302 centres move, by at most
  $4.34 \times 10^{-12}$. The JSON’s 302 and its largest “relative center change”,
  $3.81 \times 10^{-12}$, are exact: that value is the largest single coordinate change
  relative to square 1 (`l70_relative303.py`). 289 orientations change, each by at most
  $9.1 \times 10^{-15}$ radian.
- **299.** One to one under the identity, every id kept, nothing beyond $10^{-3}$: a
  refinement in the record’s sense, though not a microscopic one. 609 of T-277’s 612 near
  pairs remain near; 11 new pairs come within $10^{-12}$ and 3 leave.
- **The first 303 descends from T-272, not T-278.** It keeps all 303 of T-272’s ids,
  where T-278 renumbers 11. Against T-272 it moves 5 squares beyond a tenth and turns one
  by 19.0°, as T-278 turns its square 85. It is a further arrangement of Daniel’s packing
  found alongside Özden’s, and it lies $1.39 \times 10^{-10}$ above his.
- **Beyond the horizon.** Each certificate keeps every id of Couzo’s retained
  certificate at its count, so each search started from that file or from one numbered
  as it is. By the record’s words, 600 and 700 are refinements (no square beyond a
  tenth) and the other nine further arrangements (1 to 22 squares beyond a tenth); none
  is a new arrangement.

**Credit.** As `PACKINGS.md` and the JSON request:

- 299: Kaelan Yim after Doğa Özden, Evan Daniel and Chris Deotte, the packing T-277’s,
  with Griffin Casson’s SLP (c37, MIT) named in the lineage statement;
- 303: Kaelan Yim after Doğa Özden, Evan Daniel, Chris Deotte and Griffin Casson;
- 130: no credit claimed; the packing is Couzo’s (T-254) as Polkovskyi re-solved it
  (T-259), found from PR #574’s;
- beyond the horizon: Yim after Couzo after Vladislav Lavrentev at ten counts, and after
  alexchilton at 604, as the source’s lineage statements name them.

The measured relation supports every request: each packing continues the one it names.

## What the Checkers Share

- **This review’s checker.** It shares no code with any other checker, and it was
  written and frozen (14:05:49Z) before any of this repository’s witness, verifier or
  review code was read; the source holds no code to read.
  It shares the mathematics above and the format’s meaning: $t = \tan(\theta/2)$
  turning counterclockwise, the box $[0, S]^2$. That meaning comes from the JSON’s
  format line, the files and the precedent reviews’ descriptions, and the reversed-sense
  control shows the sense matters.
  It trusts CPython’s integers and `fractions`, GMP through `gmpy2` 2.3.1, PyYAML’s
  `BaseLoader` for parsing the two corner files only, and the clipping and shoelace
  identities its self-test exercises. Its two methods share the reader and nothing else.
- **The author’s checks.** `PACKINGS.md` and the JSON name five routes that accepted
  every certificate, “sharing some code/ancestry”:
  - Evan Daniel’s `verify_cert.py` and `verify_cert2.py` at `bb4cc78e`, pinned by
    SHA-256 (`3299ca0c…`, `55140a35…`), not read or run here;
  - a local rational verifier, `exact_certificate.verify_certificate`, not published;
  - `registry-main-report.json` and `registry-independent-report.json` at
    `registry_revision` `f30d6405`, which is this repository’s merge of #917
    (2026-11-06T03:59:24Z). Those are the record’s own two maintained routes, and
    `packing/src/sqpack/witness.py`, `verify.py` and
    `packing/devtools/check_rational_witness_independent.py` are unchanged from
    `f30d6405` to `ef1af4933` (compared by `git diff --stat`, not read).
  So a replay on the maintained routes reproduces the author’s own registry checks, as
  at T-265.
- **Authorship.** The author says Hermes Agent was used “for research, numerical search,
  implementation and verification orchestration”, and does not name the model family
  behind it. This review was written by a Claude agent, a system family that also wrote
  this repository’s witness tooling. Whether the producer’s and reviewer’s families
  overlap is unknown (question 5).
- **What is common to all.** An error in the format’s meaning or in the definition of a
  packing would be common to every checker. An error in any one implementation would
  not.

## Custody and Licence

`l70_custody.py` reads the outputs of read-only git plumbing (`ls-tree` at five commits,
`log` of the last eight) on a bare clone made for this review at about 13:52Z on 9
November, and hashes the trees extracted from it.

| Commit | Committed (UTC) | What it adds |
| --- | --- | --- |
| `78eb9ea5da43` | 2026-11-09 07:13:34 | the first `n303.cert` and the eleven beyond-horizon certificates, with `PACKINGS.md`, `SHA256SUMS` and `packing-certificates.json` |
| `e4209f6a5149` | 07:30:26 | `n299.cert` and its text copy |
| `c10e0944b12b` | 08:42:14 | `n130.cert`, its text copy and `n130-source-LICENSE.txt` |
| `546928a8a3d4` | 09:36:10 | the second `n303.cert`, its text copy and `n303-source-LICENSE.md` |
| `576223961cbc` | 09:48:41 | metadata only |
| `ac14112009f5` | 09:49:17 | metadata only (the pin) |

- Every commit is authored and committed by `vitamoon <91440012+vitamoon@users.noreply.github.com>`,
  the account of the earlier #895 (T-265), whose `n260.cert` is still blob `82ecdecc`.
- Every extracted file equals its tree entry’s blob. Every SHA-256 in `SHA256SUMS` (at
  both commits) and in `packing-certificates.json` equals the bytes, and each `.cert.txt`
  is its certificate byte for byte.
- The eleven beyond-horizon blobs are the same at `78eb9ea` and `ac14112`. `n303.cert`
  changes once, from blob `0e28ca53` (SHA-256 `b8318f81…`, the JSON’s
  `prior_certificate_sha256`) to `30147435` (`14dbc28d…`).
- The three predecessors are the files the JSON pins: its `source_sha256` for 299, 303
  and 130 equals the SHA-256 of T-277’s, T-278’s and T-259’s retained certificates
  (`dfb0ccf7…`, `9cbeb7a8…`, `1e00cd74…`), and its `source_exact_side` equals each one’s
  side exactly.
- **Push times.** GitHub’s activity log for the repository was not reachable from this
  session (the API answered that access to the repository is not enabled), so when each
  commit became public is not read here. The times above are when the commits were
  made, not when they were pushed.

Custody holds.

**Licence.** The repository has no licence file. `PACKINGS.md` says the snapshot “makes no
blanket new license assertion for inherited third-party materials”.

- At 303, `n303-source-LICENSE.md` is Özden’s notice (CC BY 4.0 for certificates and
  data, MIT for code), and the JSON says the change notice is retained.
- At 130, `n130-source-LICENSE.txt` is Mykhailo Polkovskyi’s MIT notice, for the source
  T-259’s packet retains.
- At 299 the JSON says Özden’s #929 states CC BY 4.0, but the repository carries no
  notice for that file, though it adapts the same author’s witness under the same
  licence as 303 (question 3).
- The eleven beyond-horizon certificates refine Couzo’s certificates of Kaggle notebook
  packings, which the record retains under its presumption of permission and as factual
  data.

Under the owner’s decision of 9 October (Retained Factual Data, in the known-best
packet’s README), a packet may retain a source’s certificates, digest manifests and
verification records in full when the source publishes no licence, and pins its prose
and programs by digest only. Everything this review read of the source is of that kind or
is prose: no program is in the repository.

## Significance

- **299 and 303: S1, if the owner records them.** Each is a re-solve of the house’s own
  packing whose gain is inside the house certificate’s padding (shares 0.347 and 0.967):
  bookkeeping, as T-259’s re-solve of T-254 at 0.92 is S1. They are not S2: T-265, your
  260, was 9.97 times T-257’s padding and moved 26 squares beyond a tenth.
- **130: S1 at most.** It is T-259’s packing re-boxed, below the print; under the 23
  October ruling’s words a restatement, if the ruling reaches $n \le 324$ (think-ikku
  RV-1).
- **The first 303: none.** It is above the standing value.
- **Beyond the horizon: no score.** Rows are tracked, not scored. By size alone, the
  steps of $3.3 \times 10^{-5}$ to $1.7 \times 10^{-3}$ would sit above the record’s
  S2/S3 line for continued arrangements (between T-198’s $1.15 \times 10^{-5}$ and
  T-226’s $1.88 \times 10^{-5}$), and 647’s $3.6 \times 10^{-6}$ below it.

## Findings

None is blocking.

| Id | Severity | Where | Finding |
| --- | --- | --- | --- |
| F1 | note | all fifteen certificates | each is an exact packing at its side, by both methods, every square, wall and pair; every pair strictly apart and no wall contact |
| F2 | note (this review) | the controls | 283 of 300 as stated; the 17 misses are this review’s constructions (S4 at 130) and method B’s containment test on a shape it refuses (S7); the addendum’s 45 all came out as stated |
| F3 | note | sides and prints | each 12-place print is the exact side’s ceiling; the JSON’s exact sides, decimals and improvements are exact or correctly rounded |
| F4 | **major** (owner decision; records); not blocking | 299, 303, 130 | each gain lies inside its predecessor’s padding (shares 0.347, 0.967 and 0.090 of the uniform-contraction margin), and each contracted predecessor lies below the new side; whether that is a result is RV-3 |
| F5 | note (records) | 130 | T-259’s packing exactly, translated and re-boxed; the same 12-place print; a sub-print re-certification, for which the author claims no credit |
| F6 | note (records) | the first 303 | $1.39 \times 10^{-10}$ above T-278, committed 70 minutes after #930; keeps T-272’s ids; no row |
| F7 | note (records) | the eleven beyond the horizon | each below the current row by $3.6 \times 10^{-6}$ to $1.7 \times 10^{-3}$, 16.8 to $1.6 \times 10^{9}$ times Couzo’s certificate’s padding; refinements at 600 and 700 and further arrangements at nine counts of Couzo’s packings, every id kept |
| F8 | note (author; records) | every file | every side sits a little above its packing’s extent ($5 \times 10^{-31}$ to $2.8 \times 10^{-17}$ at the nearest wall); lowering it by $1/q$ breaks no file |
| F9 | note (author; records) | `n299.cert` | no licence notice for the CC BY 4.0 witness it adapts, where 303 has one |
| F10 | note (records) | the dates | the commit times are read; the push times are not (the activity log was not reachable) |
| F11 | note (records) | the replay evidence still to be registered | the author ran this repository’s two maintained routes at `f30d6405`, whose route files are unchanged at `ef1af4933`, so a replay there reproduces the producer’s check |
| F12 | note (records) | significance | S1 at 299, 303 and 130 if the owner records them; none for the first 303; rows unscored |

**F1. Feasibility.** All fifteen files are exact packings at their sides: 2,314,078
pairs, each decided by both methods with equal classes and strictly apart, and 7,933
squares, each a unit square strictly inside its box by both. Every bound holds.

**F2. Controls.** As [Controls](#controls) gives them. Every control of the reader, the
walls, the side, the reversed sense, every near pair and every square came out as stated.
S4 at 130 missed because three pairs share its least margin and closing one closes a
second; S7 missed everywhere because method B decides containment by “clipped area
exactly 1”, which presumes the unit square it has already refused. Both methods refused
that square’s shape, and no verdict on any certificate depends on B’s containment of a
non-square. The addendum, stated before it ran, takes both into account:
all came out as stated.

**F3. Sides and prints.** As [The Sides and the Prints](#the-sides-and-the-prints) gives
them.

**F4. Inside the padding.** As
[Is the Improvement Real?](#is-the-improvement-real-the-contraction-margin) gives it.

- T-277’s and T-278’s own coordinates, scaled uniformly with nothing re-solved, are
  packings $3.404 \times 10^{-12}$ and $3.402 \times 10^{-12}$ below their sides, checked
  exactly here at contact and $10^{-30}$ past.
- The gains of 299 and 303 are 0.347 and 0.967 of those margins; 130’s is 0.090 of
  T-259’s.
- So each predecessor’s contraction lies below the new certificate, by
  $2.22 \times 10^{-12}$, $1.11 \times 10^{-13}$ and $1.99 \times 10^{-13}$.
- The precedents put T-259 against T-254 at 0.92 (S1) and T-265 against T-257 at 9.97
  (S2).

Under RV-3’s option (a) none of the three is a result; under (b) 299 and 303 cross the
print and 130 does not; under (c) all three are. The holds are right to wait for the
owner (think-ikku). This is a fact about the record’s rule, not a defect of the
certificates.

**F5. 130.** The JSON’s operation is exact: every centre moved by T-259’s near-wall
clearances, every tangent kept, the box the extent plus $2 \times 10^{-30}$. The side is
$1.955 \times 10^{-14}$ below T-259, with the same print, 11.902430645983. Under the 23
October ruling’s words (think-fwa9) that is a restatement, if the ruling reaches
$n \le 324$ (think-ikku RV-1). The author agrees: “not a new packing or numerical search
gain … no Atlas credit is claimed or recommended”.

**F6. The first 303.** Committed at 07:13:34Z on 9 November, 70 minutes after #930 posted
T-278’s certificate, and $1.39 \times 10^{-10}$ above it. It is a further arrangement of
T-272’s packing, keeping every id, and the author replaced it at `546928a` with a
refinement of T-278. It is a report of a side no smaller than the standing one, so it
makes no row; the JSON’s `prior_certificate_commit` and `prior_certificate_sha256` name
it.

**F7. Beyond the horizon.** Eleven valid certificates, each pairing one to one with
Couzo’s retained certificate under the identity and keeping its ids, each below the
current row at its count by an amount no rescaling of Couzo’s coordinates reaches. By the
record’s words, 600 and 700 are refinements (no square beyond a tenth) and the other nine
further arrangements (1 to 22 squares beyond a tenth). Each is a new beyond-horizon row,
superseding Couzo’s, with Göbel’s construction above it since Couzo’s row is below it.

**F8. The paddings.** Every file keeps its side above its extent: by about
$2.78 \times 10^{-17}$ at all four walls at 299, about $5 \times 10^{-31}$ at one wall in
most others, $10^{-30}$ at three walls at 130. 299’s least pair is $10^{-30}$ (plus
$6.9 \times 10^{-44}$) apart. The bound needs none of it, and none of it is wrong; the
record’s 12-place prints are unaffected (question 2).

**F9. Licence at 299.** `n303-source-LICENSE.md` carries Özden’s CC BY 4.0 notice; the
299 adapts the same author’s witness under the same licence, and the repository has no
notice for it. The JSON states the licence in prose. The record retains the certificate
as factual data either way (question 3).

**F10. Dates.** First commits: the eleven and the first 303 at `78eb9ea` (07:13:34Z),
299 at `e4209f6` (07:30:26Z), 130 at `c10e094` (08:42:14Z), the second 303 at `546928a`
(09:36:10Z). GitHub’s activity log was not reachable from this session, so when each
was pushed is not read here; the record dates a watched repository’s report by the push
where the push came later.

**F11. Which confirmation.** The JSON’s `registry-main-report.json` and
`registry-independent-report.json` ran at `f30d6405`, this repository’s merge of #917.
`witness.py`, `verify.py` and `check_rational_witness_independent.py` are unchanged from
there to `ef1af4933`. So a replay on the maintained routes reproduces the producer’s own
check. This review’s run is independently re-implemented, clean room, full coverage of
all fifteen, by a Claude agent, whose system family’s overlap with the producer’s Hermes
Agent is unknown.

**F12. Significance.** As [Significance](#significance) gives it.

## Questions for the Author

There is no issue to post these to; they are informational, for whoever next writes to
the author.

1. **The padding.** T-277’s and T-278’s own coordinates, scaled uniformly with nothing
   re-solved, reach $2.22 \times 10^{-12}$ below your 299 and $1.11 \times 10^{-13}$
   below your 303. Did your continuation start from the promoted coordinates, with their
   pair margins of about $2 \times 10^{-13}$?
2. **The strict margins.** Your 299’s least pair is apart by $10^{-30}$ (plus
   $6.9 \times 10^{-44}$) and its four walls by about $2.7756 \times 10^{-17}$; your 130
   pads three walls by exactly $10^{-30}$; most of the eleven pad one wall by about
   $5 \times 10^{-31}$. Are these the rationalization’s strict padding, as
   `strict_wall_padding` says at 130?
3. **The 299 licence notice.** The 303 carries Özden’s CC BY 4.0 notice
   (`n303-source-LICENSE.md`). Would you add one for the 299?
4. **The first n303.** The file of `78eb9ea` keeps all of T-272’s ids and lies
   $1.39 \times 10^{-10}$ above T-278. Which packing did its search start from?
5. **The AI system.** Which model family does Hermes Agent use? The record notes whether
   producer and reviewer share a system family.

## What I Ran

All with CPython 3.14.7 (`packing/.venv/bin/python3 -I -B`) under `nice -n 19`, at most
two processes, on a shared four-core host.
The programs, the frozen files and the receipts are in
[the review directory](../../../packing/resources/web/yim-certificates-2026-11-09/review/review-2026-11-09/README.md).
Each receipt records the SHA-256 of the programs that wrote it, and `l70_digests.py`
holds every receipt to the kept programs and the checker and plans to their frozen
digests: `ALL_RECEIPTS_MATCH`.

| Program | Receipt | CPU |
| --- | --- | ---: |
| `l70_selftest.py` | `selftest.json`: `PASSED`, 32 cases | 1 s |
| `l70_run_checks.py`, `l70_check.py` per file | `check-*.json`: `ACCEPT` at all 29 (Yim’s 15, the 3 predecessors, Couzo’s 11) | 961 s |
| `l70_plan_data.py`, `l70_plan.py` | `plan-data.json`, `controls-plan.json` (frozen) |  |
| `l70_run_controls.py`, `l70_controls.py` per file | `controls-yim-*.json`: 283 of 300 as stated | 2,991 s |
| `l70_plan_addendum.py`, `l70_controls_addendum.py` per file | `controls-addendum-yim-*.json`: 45 of 45 as stated | 1,458 s |
| `l70_contract.py` | `contract.json`: 32 certificates; the 10 verified contractions all as stated (10) | 610 s |
| `l70_sides.py` | `sides.json` |  |
| `l70_identity.py` | `identity.json` |  |
| `l70_relative303.py` | `relative303.json`: the JSON’s 3.81e-12 is the L-infinity change from square 1 |  |
| `l70_construct.py` | `construct.json` |  |
| `l70_custody.py` | `custody.json`: `CUSTODY_HOLDS` |  |
| `l70_digests.py` | `program-digests.json` |  |

The final runs recorded 6,022 CPU-seconds, 1.67 CPU-hours; the programs that record no CPU (the plan facts, sides, identity, construction, custody and digests) and the development runs bring the review to about two CPU-hours, within the brief’s cap of 40.

What went wrong along the way, and was redone:

- `-I` leaves a script’s own directory off `sys.path`, so each entry program puts its
  own directory first.
- PyYAML’s `BaseConstructor` has no `flatten_mapping`; the corner reader’s
  duplicate-key constructor first called it, and the self-test caught it before the
  freeze.
- The controls’ misses, as [Controls](#controls) gives them, and two program bugs found
  on first runs: the addendum program read S4′p’s pair from its own description, which
  has none, and the identity program first rejected its extra arguments. Neither touched
  a frozen file.
- An early draft compared the contracted new certificates with the contracted
  predecessors. Uniform contraction is blocked by the closest pair, and the new files’
  margins are uneven (299’s single pair at $10^{-30}$), so that comparison was dropped
  before the freeze.

## Verdict

**All fifteen certificates are accepted for finite feasibility.** Each proves
$s(n) \le S$ at its side exactly, and each 12-place print bounds $s(n)$.

- Every hypothesis holds exactly, for every square, wall and pair, by two methods that
  agree everywhere.
- Every control is decided as stated beforehand, but for 17 whose statements were this
  review’s errors, which the addendum replaced as stated.
- No defect of a certificate or of its mathematics is open.

F4 is major: at 299, 303 and 130 the gain is inside the predecessor’s padding, which is
the owner’s RV-3 question, and the review recommends the holds stay until it is answered.
The first 303 makes no row. The eleven beyond the horizon are new rows. The rest are
notes.

Mapped as an adversarial review with verdict `accepted` (finite feasibility), it supports
`V3` and `C3` at any entry the owner’s answer leaves standing, provided `l70_check.py`’s
run is registered as exact-algebraic evidence replayed here with full coverage. That
reads as confirmed, independently re-implemented, clean room, by a Claude agent, a system
family that also wrote this repository’s witness tooling. `V4` and `C4` would need a
second accepted adversarial review by a distinct reviewer and a human oversight record.
The significance is S1 at 299, 303 and 130 if recorded.

## What the Records Lane Needs

To map this review in:

- **The register.** On the entries for 299, 303 and 130 (draft T-280 and T-281): a
  `reviews` item, `kind: adversarial`, `verdict: accepted`, with the scope “finite
  feasibility of the certificates, decided again by a clean-room exact checker, and the
  RV-3 padding shares measured; the result question is the owner’s”. While RV-3 is open,
  the precedent is T-253 and T-260 on think-ikku: `V0/C1`, the review mapped, the replay
  evidence not entered, and the hold named.
- **The measure in the notes.** The shares 0.347, 0.967 and 0.090, the contracted
  predecessors’ sides (17.801004434251889681…, 17.901789273153088317…,
  11.902430645982047452…), and the precedents’ 0.919 and 9.968.
- **The first 303.** No entry; a sentence in the 303 entry’s notes, from F6.
- **The eleven rows.** A beyond-horizon source for `78eb9ea` in `source-coverage.yaml`,
  each row superseding Couzo’s at its count; the review’s `check-yim-nNNN.json` and
  `controls-yim-nNNN.json` as clean-room exact evidence beside the maintained replay.
- **Credit.** 299: Yim after Özden, Daniel, Deotte (with Casson’s SLP); 303: Yim after
  Özden, Daniel, Deotte, Casson; 130: none claimed, the packing Couzo’s (T-254) as
  Polkovskyi re-solved it (T-259); the rows: Yim after Couzo after Lavrentev, and after
  alexchilton at 604.
- **Verifiers.** `l70_check.py` (methods A and B) with this independence record: read
  the mathematics, the certificate format (from the files, the JSON and the precedent
  reviews) and the producer’s output; `clean_room: true`; `shares: []`; written by this
  lane at `tbd-strong-max`, reasoning max; `overlaps_producer: unknown` (question 5).
- **Evidence.** For each registered entry and row, an exact-feasibility entry,
  `independent-implementation`, `coverage: full`, citing this review.
- **Dates.** `first_committed` at the commit times of F10; the push time as unread.
