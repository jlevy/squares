# Polkovskyi’s Thirteen Certificates of #1009: Stage 4 Mathematical Review

**Date:** 2026-11-17 UTC. **Subject:** thirteen exact rational certificates by Mykhailo
Polkovskyi ([@Mishapolk](https://github.com/Mishapolk)), each published in two forms, a
`.cert` file of centres and half-angle tangents (`certificates/0000-0999/nN.cert`) and a
Witness/v2 file of rational corners (`witnesses/2026-11-16/n-N.yaml`), in
[Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records/tree/b637e6cf59c23781c813e8442bfdccb5aa5f3954)
at the commit the issue pins, issue
[#1009](https://github.com/jlevy/squares/issues/1009). The issue claims seven lowered
upper bounds (its Part A), $s(210) \le 14.971214601589$, $s(260) \le 16.633520939840$,
$s(262) \le 16.698115018700$, $s(268) \le 16.871868135103$,
$s(272) \le 16.965501175831$, $s(292) \le 17.590016439231$ and
$s(295) \le 17.698115018700$, and six refinements of registered arrangements that lower
the 12-place print (its Part B), $s(147) \le 12.651043553173$,
$s(156) \le 12.977053087495$, $s(180) \le 13.915618502788$,
$s(270) \le 16.928148603340$, $s(299) \le 17.801004434252$ and
$s(307) \le 17.979230960384$.

The 26 files’ digests are in the packet’s README and
`frozen/checker-frozen-digests.txt`; all 26 equal the issue’s list.

**Reviewed at:** `main` at `f9ddfeeef`, the merge of #1004, as this lane found it at
01:32Z on 17 November and as the issue names it, and the pin above.

**Reviewer:** Claude (AI review), at the strongest tier (`tbd-strong-max`) and maximum
reasoning, the stage 4 mathematical review lane `c-review-1009-1117`, separately
prompted. It read the source as data and ran only programs of its own, kept with their
receipts in
[`packing/resources/web/polkovskyi-1009-review-2026-11-17/`](../../../packing/resources/web/polkovskyi-1009-review-2026-11-17/README.md).
Its checker is a clean-room implementation written for this review: it reuses no code
from any earlier review.
It took the review of #1001 by lane L186 as the model for method, controls, freeze
protocol and layout, read its text, its packet’s README and its frozen checker list, and
did not open the programs of that review or of any other.
It is not a human oversight record.

## Summary for the Author

**Verdict on the bounds: accepted at all thirteen counts.** No finding is blocking or
major.

| n | Part | Squares | Pairs, all apart | Touching pairs | Wall contacts | Least pair margin (pair) | Least wall clearance | Claim, the ceiling | Verdict |
| ---: | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| 147 | B | 147 | 10,731 | 0 | 0 | $2.00004 \times 10^{-28}$ (115, 118) | $10^{-28}$ exactly | 12.651043553173 | accept |
| 156 | B | 156 | 12,090 | 0 | 0 | $2.00006 \times 10^{-28}$ (76, 126) | $10^{-28}$ exactly | 12.977053087495 | accept |
| 180 | B | 180 | 16,110 | 0 | 0 | $1.44492 \times 10^{-24}$ (34, 139) | $10^{-28}$ exactly | 13.915618502788 | accept |
| 210 | A | 210 | 21,945 | 0 | 0 | $2.00004 \times 10^{-28}$ (196, 208) | $10^{-28}$ exactly | 14.971214601589 | accept |
| 260 | A | 260 | 33,670 | 0 | 0 | $2.00012 \times 10^{-28}$ (6, 11) | $10^{-28}$ exactly | 16.633520939840 | accept |
| 262 | A | 262 | 34,191 | 0 | 0 | $2.00004 \times 10^{-28}$ (211, 230) | $10^{-28}$ exactly | 16.698115018700 | accept |
| 268 | A | 268 | 35,778 | 0 | 0 | $2.00003 \times 10^{-28}$ (228, 264) | $10^{-28}$ exactly | 16.871868135103 | accept |
| 270 | B | 270 | 36,315 | 0 | 0 | $2.00004 \times 10^{-28}$ (164, 193) | $10^{-28}$ exactly | 16.928148603340 | accept |
| 272 | A | 272 | 36,856 | 0 | 0 | $2.00006 \times 10^{-28}$ (184, 187) | $10^{-28}$ exactly | 16.965501175831 | accept |
| 292 | A | 292 | 42,486 | 0 | 0 | $4.23790 \times 10^{-15}$ (196, 209) | $10^{-28}$ exactly | 17.590016439231 | accept |
| 295 | A | 295 | 43,365 | 0 | 0 | $1.77633 \times 10^{-20}$ (80, 81) | $10^{-28}$ exactly | 17.698115018700 | accept |
| 299 | B | 299 | 44,551 | 0 | 0 | $2.00004 \times 10^{-28}$ (50, 53) | $10^{-28}$ exactly | 17.801004434252 | accept |
| 307 | B | 307 | 46,971 | 0 | 0 | $2.00010 \times 10^{-28}$ (48, 113) | $10^{-28}$ exactly | 17.979230960384 | accept |

- **How the bounds were checked.** A clean-room exact checker, written and frozen for
  this review before your README, your three programs, or this repository’s witness and
  verifier code, were read, decided all 26 files: every square, every wall and every
  pair, with no distance filter and no tolerance, by two methods that share only the
  readers. They are separating axes in Python integers, from the centres and tangents of
  your `.cert` files, and exact convex clipping in GMP rationals, from the corners of
  your Witness/v2 files, which computes the intersection of each pair and of each square
  with the outside of each wall.
  They agree on all 415,059 pairs and all 12,872 square–wall pairs, and each file is
  also decided on its own by both methods.
- **The two forms are one packing.** At every count the Witness/v2 file’s corners are
  exactly the corners of the `.cert` rows, read as a centre and the tangent of half the
  edge angle, counterclockwise, square by square and in the same order: 3,218 squares.
  Read clockwise, the rows are other squares wherever a square is tilted, and they
  overlap (X1).
- **Controls.** All 481 controls stated in advance, 37 at each count, came out as
  stated. They were written as rules over each certificate’s exact facts and hashed
  before any program read a certificate.
  They include a square placed on another, a corner moved by $10^{-40}$, the side
  lowered by $10^{-40}$, by one unit of its own denominator, to exactly the packing’s
  extent and $10^{-40}$ below it, the whole packing contracted to its first contact and
  past it, the tightest pair closed to exact contact and past it, a square at each wall
  pushed to it and past it, every one of the 415,059 pairs closed along its line of
  centres to exact contact and past it, and every square taken to its nearest wall and
  past it.
- **The claims.** Each claimed side is the 12-place ceiling of the file’s exact side,
  between $1.15 \times 10^{-13}$ (307) and $9.08 \times 10^{-13}$ (292) above it.
  The same squares in the box of the claimed side are accepted by both methods (S1e), so
  each certificate proves its claim as printed; in the box one unit of the twelfth place
  smaller they cross the walls (S1f).
- **Nothing touches, as the issue says.** Every square lies strictly inside its box and
  the closed squares are pairwise disjoint.
  The least wall clearance is exactly $10^{-28}$, at the left and bottom walls of every
  file, and the least pair margins are your “Min pair” column to its four figures:
  $2.000 \times 10^{-28}$ at ten counts, $1.445 \times 10^{-24}$ at 180,
  $1.776 \times 10^{-20}$ at 295 and $4.238 \times 10^{-15}$ at 292. Your “Close pairs”
  column is the number of pairs whose centres lie less than $\sqrt 2$ apart, at every
  count.
- **How the files are built.** At ten counts the adjacent upright squares sit at one
  distance, $1 + 2.0000\ldots \times 10^{-28}$ (every such pair at seven counts, all but
  a few at 210 and 272, 80 of 140 at 270), and the other near pairs open by the same
  factor: each file is a contact packing dilated by about $1 + 2 \times 10^{-28}$, set
  $10^{-28}$ from the left and bottom walls, in a box whose side is its extent plus
  $2 \times 10^{-28}$, rounded up to a decimal of at most 30 places.
  At 180 and 295 the dilation is $2.9 \times 10^{-24}$ and $3.6 \times 10^{-20}$; at 292
  the pairs are open unevenly, by $4 \times 10^{-15}$ to $2 \times 10^{-12}$.
- **295 and 262.** The 295 certificate is the 262 arrangement in the upper right of an
  L-shaped border of 33 squares, solved again: its inner squares lie up to 0.08 from the
  262 certificate’s, and its side is $5.9 \times 10^{-19}$ above the 262 side plus 1,
  which the 262 certificate with a border of upright squares gives exactly.
  The two print alike at 12 places.

## Scope

**Read.**

- Issue #1009 through the REST API (fetched at 01:34:03Z, before any program was
  written; no comments, one event, the label `intake` at 01:32:15Z; created at 23:38:22Z
  on 16 November, its `updated_at` the time of the labelling).
- The 26 certificate files at the pin, as data: first their structure with `grep`,
  `awk`, `head` and `od` (line kinds, field counts, scalar forms, tabs and line ends,
  and the head of the two files at 147) to write the readers, and then through the
  frozen programs. The clone’s commit subjects (81 commits), the pin’s file list, and the
  source’s two `SHA256SUMS` files.
- On `main`: `packing/witnesses/witness.schema.yaml`, for form C’s keys and meaning;
  `packing/campaign/result-import.md` (stages 1 and 4, the house rule, the labels),
  `epistemics.md` and `attribution.md`; and, to place this review’s files, the Ruff,
  BasedPyright, Biome and Flowmark exclusions.
  None of it is witness, verifier or promotion code.
- The model: the review of #1001 by lane L186,
  `docs/project/reviews/review-2026-11-16-joegun-1001.md`, with its packet’s README and
  its frozen lists; and the claim section of the review of #996 by lane L180. Not their
  programs, plans or receipts.
- The bead `think-evxy`, the header of its parent epic, and the bead `think-ruu2`, which
  holds the owner’s open question RV-3.

**Run.** Fourteen Python programs and modules of my own, importing nothing from this
repository or the source ([What I Ran](#what-i-ran)). They decide the certificates
twice, run a self-test, run the controls, and describe the files.

**Seen before my findings were written**, disclosed as the runbook asks:

- the lane’s brief, which states the issue, the pin and the thirteen counts in their two
  parts; that earlier reports of the same day claim 292 (Özden’s #1005 and de Winter’s
  #1006) and 262 and 295 (de Winter’s #1007), with their times and pins; and the checks
  to make after the freeze;
- the issue, which states for each count the claimed side, the “standing `main` bound”
  and the gain; at 262, 292 and 295 the margins below #1005, #1006 and #1007, with two
  of those reports’ sides; the files’ digests, “Min wall”, “Min pair”, “Close pairs” and
  pair counts; the four checks the author ran and what the checkers share; that
  feasibility alone is claimed; the lineage (new arrangements at 210, 262, 272, 292 and
  295; improved packings after Evan Daniel at 260 and after Doğa Özden at 268;
  refinements of registered arrangements at the six Part B counts, “subject to `RV-3`”);
  and the AI assistance (Gemini);
- the notes of `think-ruu2`, which give register entries and padding measurements at
  130, 172, 199, 293, 299, 303 and 307 as they stood between 31 October and 9 November.
  Among this review’s counts they say that the house at 307 was then Couzo’s refinement
  of ntumlnoob’s packing (T-256), with a regularizer’s solve $3.752 \times 10^{-12}$
  below it held unregistered, and that at 299 a certificate of Kaelan Yim’s
  $1.18 \times 10^{-12}$ below the house (T-277) was held;
- the source’s commit subjects, which name earlier releases at some of these counts: a
  260 “graft refinement”, a 270 certificate at 16.928162252197, “Category A” records at
  130, 182 and 268 and “Category B micro-refinements” from 105 to 308;
- the model review, which describes T-174, T-186, T-256, T-268 and T-275 at other
  counts;
- a process listing at 03:07Z, after the session’s worker restarted
  ([What I Ran](#what-i-ran)), which showed other lanes’ command lines: the file names
  of #1005 to #1007’s certificates at their pins and the name of an import packet.
  None of their outputs was read;
- between the checker’s freeze and the findings’ freeze, while the controls ran, what
  the lane needed to write the programs it ran afterwards: the front matter of the case
  record at 127 and the head of the house witness there, the help texts of
  `devtools.contraction_margin` and `devtools.measure_identity`, and the names of the
  adapters of `devtools.upper_bound_reports`. `rv1009_padding.py` was tried on the
  houses at 127, 204, 232, 264 and 305, the model review’s counts, where it reproduces
  the contraction margins that review prints.

**Not read before my checker was frozen** (03:33:14Z) **or my findings were frozen**:
the source’s `README.md`, `SUBMISSION_2026_11_16.md`, `ISSUE_*.md`,
`verify_bound_certificate.py`, `verify_area_exact.py`, `verify_algebraic_bounds.py`,
`check_packing.py`, `certified_bounds.json`, `upper_bounds.json`, its licence files and
its figures (all identified only by their names in the tree listing); this repository’s
`sqpack` witness, verifier and promotion code, its devtools that read witnesses, and the
Rust crates; the register entries, case records and house witnesses at the thirteen
counts; issues #1005, #1006 and #1007 and their sources; any import lane’s work and the
other review lane’s; and the model review’s programs.

**Not run here.** Any of the author’s code; and, before the findings were frozen, any of
this repository’s code on a certificate or a house of the thirteen counts.

## The Claims and What They Need

Issue #1009 claims $s(n) \le C_n$ at thirteen counts, each $C_n$ the 12-place print of
the certificate’s side $S_n$, rounded up.
Each certificate proves $s(n) \le S_n$: there are $n$ closed unit squares, rotated
freely, with pairwise disjoint interiors inside the closed square $[0, S_n]^2$. The
claim follows when $C_n \ge S_n$, and directly when the same squares are accepted in
$[0, C_n]^2$. The issue states more than the bound needs, that every square lies in the
open box $(0, S_n)^2$ and that the closed squares are pairwise disjoint; both are
decided here as facts about the margins, and neither is a hypothesis of the bound.

Each count has two files.

- **Form P**, `nN.cert`: a comment line, a header `n S`, and $n$ rows `x y t` of exact
  rationals. A row is read as the unit square with centre $(x, y)$ and an edge at the
  angle $2\arctan t$ counterclockwise from the $x$-axis: with
  $u = \bigl((1 - t^2)/(1 + t^2),\ 2t/(1 + t^2)\bigr)$ and $v$ its quarter turn, the
  square is the set of points $(x, y) + \alpha u + \beta v$ with
  $\lvert\alpha\rvert \le 1/2$ and $\lvert\beta\rvert \le 1/2$. The file states neither
  the reading nor where the box is.
- **Form C**, `n-N.yaml`: a softschema envelope (`contract: packing.squares:Witness/v2`)
  around a Witness/v2 record with `representation: corners`, `scalar.kind: rational`,
  `origin: lower-left` and `axes: x-right-y-up`: four rational corners per square, ids
  `square-1` to `square-n`.

A packing under any reading proves the bound, so form P’s reading is not a matter of
trust: it is the definition of what is decided.
What fixes it as the author’s is form C, which states its origin and axes: the two files
of a count are the same $n$ squares when form P is read as above, and not when its
tangent is read clockwise (X1).

The hypotheses are six:

1. **The reading.** Form P is ASCII with a final newline and no tab, carriage return,
   blank line or stray space; comment lines only before the header; `n` a plain positive
   integer; exactly $n$ rows of three scalars.
   Form C is one YAML document with no anchors, aliases, explicit tags, duplicate keys,
   tabs or carriage returns, holding only strings, plain decimal integers, mappings and
   sequences; the envelope above, the witness keys inside the schema’s list with every
   required key present, `square_size: '1'`; the squares listed with ids in order, each
   with exactly an id and four corners of two scalars.
   Every scalar is a string `p` or `p/q` with no sign but an optional minus, no leading
   zero and $q \ge 1$. Lowest terms are recorded, not required.
2. **The count and the twin.** $n$ squares in each file, the same side, and square $k$
   of form C is the square of row $k$ of form P: its four corners are
   $C \pm u/2 \pm v/2$, listed as a cyclic rotation of them in either sense.
3. **Unit squares.** In form P the direction is $(a, b)/r$ with $a = q^2 - p^2$,
   $b = 2pq$ and $r = q^2 + p^2$ for $t = p/q$, so $a^2 + b^2 = r^2$ identically, and
   the check is made anyway; no row of form P can state a square that is not a unit
   square. In form C the four corners, in the order listed, are a unit square.
4. **Containment.** Each square lies in $[0, S_n]^2$; the origin is the lower-left
   corner.
5. **Disjoint interiors.** No two squares’ interiors meet.
6. **The rotation sense.** $t$ is read counterclockwise, $x$ to the right and $y$ up.
   Control X1 shows that reading it the other way gives other squares wherever a square
   is tilted, and form C decides which reading is the file’s.

`rv1009_check.py` decides the first two through the readers, and the next three twice.

- **Method A** (`rv1009_axes.py`, Python integers) reads poses and never a corner.
  Each centre is written over one denominator $E$, $C = (X, Y)/E$, and each direction as
  the integers $(a, b, r)$ above; the pose is accepted when $E > 0$, $r > 0$ and
  $a^2 + b^2 = r^2$. On a unit normal $w$ of either square of a pair, square $i$
  projects to an interval of half-length $1/2$ on its own normals and
  $(\lvert\cos D\rvert + \lvert\sin D\rvert)/2$ on the other square’s, $D$ the angle
  between them, so the two half-lengths add to the same $H$ on all four normals.
  The separation on $w$ is $\lvert d \cdot w\rvert - H$, $d$ the centre difference, an
  exact distance; all four share the denominator $2 E_i E_j r_i r_j$, so the margin,
  their maximum, is decided on integers and kept as an exact fraction: positive is
  apart, zero is contact with disjoint interiors, negative is overlap.
  Two convex polygons have disjoint interiors exactly when a line parallel to an edge of
  one of them weakly separates them (the origin then lies outside the interior of their
  Minkowski difference, whose edges are parallel to theirs), and they are disjoint
  exactly when one does so strictly, so the three signs are exactly those three classes.
  A wall’s clearance is the signed distance from the square’s extreme corner to it, from
  the half-extent $(\lvert a\rvert + \lvert b\rvert)/(2r)$.
- **Method B** (`rv1009_clip.py`, `gmpy2.mpq`) is handed corners and nothing else.
  Four points are a unit square in cyclic order when all four sides have squared length
  1 and both diagonals squared length 2; the shoelace sum, $\pm 2$, gives the sense, and
  a clockwise listing is reversed before clipping.
  A pair is decided by clipping one square against the four closed half-planes to the
  left of the other’s counterclockwise edges (Sutherland–Hodgman, keeping points on the
  line), which gives the intersection exactly; it is clipped both ways round, and the
  two results must agree in class and area.
  Empty is apart; non-empty with zero area is contact, since the interior of an
  intersection of convex sets is the intersection of their interiors; positive area is
  overlap, by that area.
  Each wall is classed the same way, by clipping the square against the closed
  half-plane outside it, and containment is decided apart: a unit square lies in the box
  exactly when its intersection with the box has area exactly 1.

The two share the readers (`rv1009_reader.py`), which hand them exact rationals, and
nothing else on the form each reads natively: method A the rows of form P, method B the
corners of form C. That pair of decisions involves no conversion, and with the twin
relation it is the independent one.
`rv1009_forms.py` writes each form in the other’s terms, so that every file is also
decided on its own by both methods: `rv1009_files.py` decides each count a second time,
crossed, with method A on the poses taken from the form C corners and method B on the
corners written from the form P rows.
The verdict is `ACCEPT` only when both files are read and are one packing, both
decisions accept every square, wall and pair with equal classes everywhere, and the two
decisions give the same margin at every pair and the same clearance at every wall.
No distance filter and no tolerance is applied anywhere.

## The Certificates Decided

Every one of the thirteen is `ACCEPT`: both files read, one packing in both forms,
accepted by both methods in both decisions.

| n | Side, exactly | Scalars, P and C | Squares | Pairs, all apart by both methods | Least pair margin (pair) | Pairs below $10^{-27}$, $10^{-18}$, $10^{-9}$, $10^{-3}$ | Next margin above $10^{-9}$ | Claim less side |
| ---: | --- | --- | ---: | ---: | --- | --- | --- | --- |
| 147 | 12.651043553172632772258400324749 | 442, 1,177 | 147 | 10,731 | $2.00003974327 \times 10^{-28}$ (115, 118) | 225, 225, 225, 369 | $5.38 \times 10^{-5}$ | $3.672 \times 10^{-13}$ |
| 156 | 12.977053087494616205652876713394 | 469, 1,249 | 156 | 12,090 | $2.00006175926 \times 10^{-28}$ (76, 126) | 396, 396, 396, 400 | $1.29 \times 10^{-4}$ | $3.838 \times 10^{-13}$ |
| 180 | 13.915618502787316117970670866716 | 541, 1,441 | 180 | 16,110 | $1.44492288516 \times 10^{-24}$ (34, 139) | 0, 369, 369, 397 | $1.00 \times 10^{-9}$ | $6.839 \times 10^{-13}$ |
| 210 | 14.971214601588191477949459822729 | 631, 1,681 | 210 | 21,945 | $2.00004138348 \times 10^{-28}$ (196, 208) | 502, 505, 508, 521 | $1.01 \times 10^{-9}$ | $8.085 \times 10^{-13}$ |
| 260 | 16.633520939839760712361517061493 | 781, 2,081 | 260 | 33,670 | $2.00011705178 \times 10^{-28}$ (6, 11) | 527, 530, 530, 585 | $6.30 \times 10^{-9}$ | $2.393 \times 10^{-13}$ |
| 262 | 16.698115018699394428085085691104 | 787, 2,097 | 262 | 34,191 | $2.00003825289 \times 10^{-28}$ (211, 230) | 354, 354, 354, 361 | $9.90 \times 10^{-8}$ | $6.056 \times 10^{-13}$ |
| 268 | 16.871868135102178272291426509416 | 805, 2,145 | 268 | 35,778 | $2.00003288258 \times 10^{-28}$ (228, 264) | 234, 234, 236, 726 | $1.55 \times 10^{-7}$ | $8.217 \times 10^{-13}$ |
| 270 | 16.928148603339607384058475178539 | 811, 2,161 | 270 | 36,315 | $2.00003780539 \times 10^{-28}$ (164, 193) | 226, 282, 444, 786 | $1.00 \times 10^{-9}$ | $3.926 \times 10^{-13}$ |
| 272 | 16.965501175830215055658601627400 | 817, 2,177 | 272 | 36,856 | $2.00005513506 \times 10^{-28}$ (184, 187) | 695, 695, 704, 759 | $1.10 \times 10^{-7}$ | $7.849 \times 10^{-13}$ |
| 292 | 17.590016439230092219882547056721 | 877, 2,337 | 292 | 42,486 | $4.23790083740 \times 10^{-15}$ (196, 209) | 0, 0, 177, 735 | $3.09 \times 10^{-6}$ | $9.078 \times 10^{-13}$ |
| 295 | 17.698115018699394428678305824795 | 886, 2,361 | 295 | 43,365 | $1.77632627883 \times 10^{-20}$ (80, 81) | 0, 169, 169, 617 | $2.55 \times 10^{-5}$ | $6.056 \times 10^{-13}$ |
| 299 | 17.801004434251766824147518370008 | 898, 2,393 | 299 | 44,551 | $2.00004399879 \times 10^{-28}$ (50, 53) | 606, 606, 609, 700 | $5.20 \times 10^{-8}$ | $2.332 \times 10^{-13}$ |
| 307 | 17.979230960383884604355063038740 | 922, 2,457 | 307 | 46,971 | $2.00010117482 \times 10^{-28}$ (48, 113) | 793, 793, 793, 814 | $7.52 \times 10^{-7}$ | $1.154 \times 10^{-13}$ |

| n | Left and bottom: least clearance; squares at it | Right: least clearance; squares | Top: least clearance; squares | The side less the width, and less the height | Clearances below $10^{-27}$, $10^{-9}$ |
| ---: | --- | --- | --- | --- | --- |
| 147 | $10^{-28}$ exactly; 8 and 9 | $1.001577 \times 10^{-28}$; 7 | $1.001577 \times 10^{-28}$; 6 | $2.001577 \times 10^{-28}$ and $2.001577 \times 10^{-28}$ | 31, 31 |
| 156 | $10^{-28}$ exactly; 7 and 4 | $1.009791 \times 10^{-28}$; 12 | $1.009791 \times 10^{-28}$; 12 | $2.009791 \times 10^{-28}$ and $2.009791 \times 10^{-28}$ | 45, 45 |
| 180 | $10^{-28}$ exactly; 8 and 9 | $1.005122 \times 10^{-28}$; 1 | $1.072922 \times 10^{-28}$; 12 | $2.005122 \times 10^{-28}$ and $2.072922 \times 10^{-28}$ | 40, 41 |
| 210 | $10^{-28}$ exactly; 10 and 10 | $1.009438 \times 10^{-28}$; 13 | $1.009438 \times 10^{-28}$; 14 | $2.009438 \times 10^{-28}$ and $2.009438 \times 10^{-28}$ | 51, 52 |
| 260 | $10^{-28}$ exactly; 13 and 12 | $1.008143 \times 10^{-28}$; 8 | $1.008143 \times 10^{-28}$; 15 | $2.008143 \times 10^{-28}$ and $2.008143 \times 10^{-28}$ | 48, 48 |
| 262 | $10^{-28}$ exactly; 11 and 10 | $1.004989 \times 10^{-28}$; 8 | $1.004989 \times 10^{-28}$; 10 | $2.004989 \times 10^{-28}$ and $2.004989 \times 10^{-28}$ | 41, 41 |
| 268 | $10^{-28}$ exactly; 7 and 6 | $1.000055 \times 10^{-28}$; 6 | $1.000055 \times 10^{-28}$; 9 | $2.000055 \times 10^{-28}$ and $2.000055 \times 10^{-28}$ | 28, 28 |
| 270 | $10^{-28}$ exactly; 5 and 1 | $1.005709 \times 10^{-28}$; 1 | $1.005707 \times 10^{-28}$; 1 | $2.005709 \times 10^{-28}$ and $2.005707 \times 10^{-28}$ | 28, 52 |
| 272 | $10^{-28}$ exactly; 9 and 10 | $1.003177 \times 10^{-28}$; 15 | $1.003177 \times 10^{-28}$; 15 | $2.003177 \times 10^{-28}$ and $2.003177 \times 10^{-28}$ | 60, 60 |
| 292 | $10^{-28}$ exactly; 1 and 2 | $1.001727 \times 10^{-28}$; 1 | $5.632455 \times 10^{-16}$; 1 | $2.001727 \times 10^{-28}$ and $5.632455 \times 10^{-16}$ | 4, 20 |
| 295 | $10^{-28}$ exactly; 2 and 8 | $1.004545 \times 10^{-28}$; 7 | $1.004545 \times 10^{-28}$; 2 | $2.004545 \times 10^{-28}$ and $2.004545 \times 10^{-28}$ | 19, 20 |
| 299 | $10^{-28}$ exactly; 14 and 7 | $1.009403 \times 10^{-28}$; 13 | $1.009403 \times 10^{-28}$; 17 | $2.009403 \times 10^{-28}$ and $2.009403 \times 10^{-28}$ | 54, 54 |
| 307 | $10^{-28}$ exactly; 9 and 17 | $1.000641 \times 10^{-28}$; 15 | $1.000641 \times 10^{-28}$; 10 | $2.000641 \times 10^{-28}$ and $2.000641 \times 10^{-28}$ | 64, 64 |

| n | Exactly upright | Turned by less than $10^{-9}$ degrees | $10^{-9}$ degrees to 1° | Beyond 1°; the largest | Distinct tangents | Near pairs: both upright, equal tangents, other | Commonest margin; pairs at it | One less the contact factor over the near pairs: least to greatest |
| ---: | ---: | ---: | ---: | --- | ---: | --- | --- | --- |
| 147 | 90 | 0 | 13 | 44; 27.72° | 23 | 140, 54, 31 | $2.00007110 \times 10^{-28}$; 140 | $2.000036 \times 10^{-28}$ to $2.000107 \times 10^{-28}$ |
| 156 | 95 | 0 | 1 | 60; 32.38° | 19 | 273, 48, 75 | $2.00007016 \times 10^{-28}$; 273 | $2.000036 \times 10^{-28}$ to $2.000130 \times 10^{-28}$ |
| 180 | 129 | 0 | 11 | 40; 44.77° | 50 | 308, 3, 58 | $2.88964577 \times 10^{-24}$; 250 | $1.444923 \times 10^{-24}$ to $3.521099 \times 10^{-24}$ |
| 210 | 135 | 1 | 1 | 73; 33.51° | 28 | 363, 61, 84 | $2.00007618 \times 10^{-28}$; 357 | $2.000041 \times 10^{-28}$ to $1.001001 \times 10^{-13}$ |
| 260 | 133 | 0 | 24 | 103; 27.27° | 31 | 270, 173, 87 | $2.00015966 \times 10^{-28}$; 270 | $2.000080 \times 10^{-28}$ to $2.528763 \times 10^{-20}$ |
| 262 | 152 | 0 | 38 | 72; 29.19° | 62 | 272, 70, 12 | $2.00007651 \times 10^{-28}$; 272 | $2.000038 \times 10^{-28}$ to $2.000102 \times 10^{-28}$ |
| 268 | 148 | 0 | 74 | 46; 44.17° | 108 | 203, 17, 16 | $2.00006577 \times 10^{-28}$; 203 | $2.000033 \times 10^{-28}$ to $1.953764 \times 10^{-13}$ |
| 270 | 70 | 85 | 49 | 66; 43.10° | 122 | 140, 83, 221 | $2.00007561 \times 10^{-28}$; 80 | $2.000038 \times 10^{-28}$ to $9.901951 \times 10^{-10}$ |
| 272 | 175 | 1 | 7 | 89; 33.39° | 31 | 511, 83, 110 | $2.00008626 \times 10^{-28}$; 508 | $2.000044 \times 10^{-28}$ to $7.217610 \times 10^{-11}$ |
| 292 | 14 | 104 | 115 | 59; 43.92° | 195 | 4, 33, 140 | $6.07782695 \times 10^{-15}$; 4 | $4.237901 \times 10^{-15}$ to $2.065869 \times 10^{-12}$ |
| 295 | 95 | 2 | 126 | 72; 29.19° | 199 | 124, 2, 43 | $3.55265254 \times 10^{-20}$; 120 | $1.776326 \times 10^{-20}$ to $3.558428 \times 10^{-20}$ |
| 299 | 181 | 0 | 33 | 85; 30.89° | 54 | 427, 105, 77 | $2.00007999 \times 10^{-28}$; 427 | $2.000044 \times 10^{-28}$ to $6.111671 \times 10^{-10}$ |
| 307 | 193 | 0 | 2 | 112; 32.38° | 27 | 575, 104, 114 | $2.00013191 \times 10^{-28}$; 575 | $2.000066 \times 10^{-28}$ to $2.000202 \times 10^{-28}$ |

- **Reading.** All 26 files read strictly, and every scalar is in lowest terms.
  Form P has one comment line, “Exact rational square-packing certificate (n = N);
  verify with python3 verify_cert.py”, then the header and $n$ rows; no tangent is
  negative. Form C lists ids `square-1` to `square-n` in order and writes every scalar as
  `p/q`; each envelope is `packing.squares:Witness/v2` with `status: enforced`, and each
  `claim` block says `coordinate_provenance: reported` and `method: exact-algebraic`,
  with a `limitations` sentence that states strict containment, disjoint closed squares
  and that no optimality is claimed.
  No file has a `source` or a `certificate` block.
  Those blocks are the author’s words and are data here (F7).
- **The sides.** Each side is written identically in the two forms and is a decimal of
  at most 30 places (its denominator runs from $5 \times 10^{27}$ at 272 to $10^{30}$),
  so the table gives it exactly.
- **The twin.** At every one of the 3,218 squares form C’s four corners are form P’s
  $C - u/2 - v/2$, $C + u/2 - v/2$, $C + u/2 + v/2$ and $C - u/2 + v/2$ in that order:
  the same offset and the same sense everywhere.
  The crossed decision gives the same margin at every pair (one digest over all the
  margins of a count) and the same clearance at every wall.
- **Squares.** Every square is a unit square by both methods, and form C lists every
  square counterclockwise.
- **Walls.** Every square lies in its box by both methods, with area exactly 1 inside,
  and the two methods’ classes agree on all 12,872 square–wall pairs: all clear.
  The left and bottom walls are cleared by exactly $10^{-28}$ in every file, by 1 to 17
  squares; the right and top by $1.0001 \times 10^{-28}$ to $1.01 \times 10^{-28}$,
  except the top at 180 ($1.073 \times 10^{-28}$) and at 292 ($5.6 \times 10^{-16}$:
  that packing is narrower in height than in width).
  The box is therefore larger than the packing’s extent by $2.0001 \times 10^{-28}$ to
  $2.0098 \times 10^{-28}$ (E1c): $10^{-28}$ on each side, and the rounding of the side.
- **Near pairs.** No pair touches.
  Below $10^{-9}$ lie 169 to 793 pairs at each count, and the next pair lies between
  $10^{-9}$ and $1.3 \times 10^{-4}$. At 147, 156, 262 and 307 every near pair lies
  between $2.00003 \times 10^{-28}$ and $2.4 \times 10^{-28}$; at 210, 260, 268, 272 and
  299 all but 2 to 9 lie below $10^{-27}$, the rest reaching at most
  $6.2 \times 10^{-10}$; at 270 only 226 of 444 do, and 218 lie between $10^{-27}$ and
  $10^{-9}$. At 180 the near pairs lie between $1.44 \times 10^{-24}$ and
  $3.7 \times 10^{-24}$, at 295 between $1.78 \times 10^{-20}$ and
  $4.2 \times 10^{-20}$, and at 292 between $4.2 \times 10^{-15}$ and
  $2.1 \times 10^{-12}$ with 173 distinct values among 177.
- **One dilation.** A pair in contact, with its centres moved apart by a factor
  $1 + \varepsilon$, opens to a margin of $\varepsilon H$, $H$ the sum of its two
  half-lengths; its contact factor, the contraction of the centres that closes it again,
  is then $1/(1 + \varepsilon)$ whatever $H$ is.
  At ten counts the near pairs of upright squares share one margin exactly, between
  $2.00007 \times 10^{-28}$ and $2.00016 \times 10^{-28}$: all of them at seven counts
  (140 to 575 pairs), all but 6 and 3 at 210 and 272, and 80 of 140 at 270. At 147, 156,
  262 and 307 every near pair’s contact factor lies within $10^{-4}$ of that distance
  from 1 (the last column), so each of those files is a packing in contact to about
  $10^{-32}$, dilated once by $1 + 2.0000\ldots \times 10^{-28}$; the other six are the
  same but for their looser pairs.
  At 180 the common gap is $2.89 \times 10^{-24}$ and at 295 $3.55 \times 10^{-20}$,
  each with its tightest pair at half of it; 292 shows no single factor.
- **Tilts.** Between 14 (292) and 193 (307) squares are exactly upright.
  The rest are turned by up to 44.77°, each by a rational tangent of at most 33 digits.
  At 270 and 292, 85 and 104 squares are turned by less than $10^{-9}$ degrees without
  being upright, and at 268, 292 and 295, 74, 115 and 126 by between $10^{-9}$ degrees
  and 1°. Nothing in the bound depends on the tilts; they are described in
  `out/describe-nNNN.json`.
- **295 and 262.** `rv1009_lstep.py` (`out/lstep-262-295.json`) pairs each square of the
  262 certificate, moved by $(1, 1)$, with the nearest square of the 295 certificate.
  The pairing is one to one; 240 of the 262 squares lie more than $10^{-3}$ from their
  partner, the farthest by 0.079, and 85 keep their tangent.
  The 33 squares left over run along the left and bottom walls, 10 of them exactly
  upright. The 295 side is the 262 side plus $1 + 5.93 \times 10^{-19}$ (F8).

The margins and clearances are exact fractions in the receipts; the prints here are
shortened.

`rv1009_selftest.py` holds the readers, both methods, the forms and the closed forms to
34,183 checks and passes:

- edge contacts of two parallel squares, upright and turned by the tangents $1/2$, $2/3$
  and $1/4$ (the directions $(3, 4)/5$, $(5, 12)/13$ and $(15, 8)/17$), across each of
  the four edges at an offset of 0 and $\pm 1/3$ along the edge, and corner-to-corner
  contacts along each diagonal, each at a gap $\delta$ of $10^{-40}$, 0, $-10^{-40}$ and
  $\pm 1/7$, with the second square listed from each corner in both senses and the pair
  in both orders; the margin is $\delta$ by method A, by the closed form and by the
  corner projections, and the overlap areas, derived by hand, are
  $\lvert\delta\rvert(1 - \lvert\tau\rvert)$ for an offset $\tau$ and $\delta^2$;
- a 3-4-5 and a 5-12-13 corner on an upright edge under each quarter turn of the plane,
  margin $\delta$, areas $\tfrac{25}{24}\delta^2$ and $\tfrac{169}{120}\delta^2$;
  duplicates (margin $-1$, area 1); an upright square against its concentric turn by
  $(3, 4)/5$ and $(5, 12)/13$, margins $-6/5$ and $-15/13$ and areas $5/6$ and $13/15$;
- each wall at $10^{-40}$ inside, at contact and $10^{-40}$ out, and $1/9$ either way,
  for squares at five tangents under eight listings, with the area outside
  ($\lvert\delta\rvert$ for an upright square, $\delta^2/(2\lvert cs\rvert)$ for a
  tilted one) and method B’s containment;
- the corners of a row, the pose of a tangent and the twin relation against values
  written out by hand; the unit test and listing sense at six tangents, and seven shapes
  both methods must refuse (a corner off by $10^{-40}$, a bowtie listing, a rhombus with
  unit sides, a $1 \times (1 + 10^{-40})$ rectangle, a square of side 2, a point, a
  repeated corner);
- 300 random pairs with tangents of numerator and denominator up to $10^6$, on which
  method A’s margin, both ways round, equals the closed form and the corner projections
  and method B’s class its sign, each then closed along its line of centres to
  $10^{-40}$ short of contact, to it and $10^{-40}$ past it, with margins exactly those;
  100 random turned squares taken to each wall, short of it, at it and past it;
- 25 malformed form P files and 38 malformed form C files the readers must refuse, each
  mutation checked to have applied, valid files read back value for value, a
  non-canonical side read and flagged, and integer ids read; and whole-file decisions: a
  $2 \times 2$ grid (six touching pairs, eight wall contacts), that grid in a box
  $10^{-40}$ too small, a duplicate square, a 3-4-5 square touching all four walls of
  its box, two files that differ in one square, in side and in count, a form C square
  that is not a unit square, an unreadable file, and partial decisions.

Six deliberately broken copies fail it: method A using only the first square’s two
normals (1,485 failures), method A counting a zero margin as apart (91), method B
clipping with open half-planes (1,509), form P read with the other rotation sense
(5,976), method B without its diagonal test (1), and a reader that takes a leading plus
sign (3).

## Controls

`programs/controls-plan.json` states 37 controls for each count, and the outcome of each
as a rule over the certificate’s exact facts (its rows and side, and method A’s margins
and clearances), since those facts were unknown when it was written.
It was hashed with the checker at 03:33:14Z and pushed at 03:34:13Z, before any program
of this lane read a certificate.
`rv1009_controls.py` evaluates each rule exactly and compares it with what both methods
decide on the changed packing; a decision in which the methods disagree fails its
control. Whole-file controls write the changed packing as the bytes of both forms and
read them back through the readers.
“Contact” is a margin or clearance of exactly 0, and “past” is $10^{-40}$ beyond it, a
step below every gap in these files.

A control that moves every square decides every pair again by both methods.
A control that changes one square decides again the $n - 1$ pairs that hold it, and a
control that changes only the side decides no pair again; for every square it does not
change, such a control checks that the row and the corners read back are the original’s.
A pair’s decision is a function of its two squares alone, so each pair not decided again
has the original’s decision.
The receipts print such a decision’s verdict as `PARTIAL` where this review says
accepted.

| Control | Stated | Outcome at the thirteen counts |
| --- | --- | --- |
| C0. Every margin recomputed from the form C corners, by projecting the eight corners on the four edge directions, and every clearance from the form P row in Fractions | equal to method A everywhere | as stated: 0 mismatches over 415,059 pairs and 3,218 squares |
| R1. The last square deleted from the original bytes, the count as stated; each form apart | the changed form’s reader refuses: $n$ stated, $n - 1$ listed | as stated |
| R2. The side written as $2p/2q$ in both forms | read; values equal; accepted; only the side flagged non-canonical | as stated |
| R3. Form C: the ids of squares 1 and 2 exchanged. Form P: rows 1 and 2 exchanged | form C refused, ids out of order; form P read and refused because the twin relation fails at exactly squares 1 and 2 | as stated |
| R4. The side as a 40-place decimal: in form P, in form C quoted, in form C unquoted | the reader refuses each: not a scalar twice, a YAML float once | as stated |
| R5. A leading `+` on square 1’s first coordinate in the original bytes; each form apart | the changed form’s reader refuses, naming the coordinate | as stated |
| G1. Square $n$ given square 1’s row | refused: the margins of the $n - 1$ pairs with square $n$ exactly predicted ($(1, n)$ at $-1$, each $(k, n)$ at the original $(1, k)$), overlapping pairs exactly $[(1, n)]$ with B area 1 | as stated |
| G2. Square 1 translated by $(S, 0)$ | refused: square 1’s clearances exactly $(L + S, B, R - S, T)$; its area inside 0; no pair with it overlaps; other squares unchanged | as stated |
| G3. In form C, square 1’s first corner moved by $10^{-40}$ in $x$ | refused: square 1, and only square 1, not a unit square by B; no pose from its corners; the twin fails at square 1 only | as stated |
| G4. In form C, every square listed in reverse | the original’s verdict with A on the poses taken from the changed corners and B on the corners; margins and clearances identical; senses exchanged | as stated: accepted, all clockwise |
| G5. In form C, every square listed from its second corner | the same, senses unchanged | as stated |
| G6. Every row transposed | margins identical; clearances $(L, B, R, T) \to (B, L, T, R)$ | as stated |
| G7. A quarter turn about the box centre | margins identical; clearances $(L, B, R, T) \to (T, L, B, R)$ | as stated |
| G8. Mirrored, $x \to S - x$, $t \to -t$ | margins identical; clearances $(L, B, R, T) \to (R, B, L, T)$ | as stated |
| S1a. The side lowered by $10^{-40}$ | the side rule: right and top clearances lowered by exactly $\delta$, the left and bottom unchanged, every row and corner the original’s; crossings and contacts exactly those of the new clearances | as stated: accepted at every count |
| S1b. The side lowered by $1/q$, $q$ its denominator | the side rule with $\delta = 1/q$ | as stated: accepted at twelve counts; refused at 272, where $1/q$ exceeds $W$ |
| S1c. The side lowered by $W$, the least right-or-top clearance | the side rule; accepted, contacts exactly at the squares that attain $W$ | as stated: accepted at every count, 1 to 30 squares in contact |
| S1d. The side lowered by $W + 10^{-40}$ | the side rule; refused, those squares crossing | as stated: refused at every count |
| S1e. The side set to the claim | the side rule with $\delta = S - C$ | as stated: accepted at every count |
| S1f. The side set to the claim less $10^{-12}$ | the side rule with $\delta = S - C + 10^{-12}$ | as stated: refused at every count |
| E1c. Every square translated by the least left and bottom clearances and the side set to the extent $X$, the larger of the packing’s width and height | the extent rule: every clearance predicted, margins identical; accepted; left, bottom and the wall of the larger extent touched exactly by the squares that attain the least clearances | as stated: accepted at every count |
| E1p. The same with the side $X - 10^{-40}$ | refused; the squares at the wall of the larger extent cross | as stated |
| K1c. Every centre and the side multiplied by $g^*$, the first contact of a uniform contraction about the origin | accepted; the contacts exactly the pairs and walls whose own factor is $g^*$ | as stated: accepted at every count |
| K1p. The same with $g^*(1 - 10^{-40})$ | refused; overlaps and crossings exactly the pairs and walls whose factor exceeds it | as stated |
| P1c. The tightest eligible pair closed along its line of centres to exact contact | that pair’s margin exactly 0, touching by A and B; the moved square’s other pairs apart; other squares unchanged; accepted | as stated |
| P1p. The same, $10^{-40}$ past | refused: of the moved square’s pairs exactly that pair overlaps, margin exactly $-10^{-40}$ | as stated |
| W1c. At each wall, the eligible square nearest it moved to it | that clearance exactly 0, the opposite one raised by the move, all else unchanged; accepted | as stated at all four walls |
| W1p. The same, $10^{-40}$ further | refused: the only crossing that square at that wall, by exactly $-10^{-40}$ | as stated at all four walls |
| WALL. Every square moved to its nearest wall and past (square-level) | A’s clearance exactly 0 and $-10^{-40}$; B touching and crossing; B’s area inside 1 and below 1 | as stated: 3,218 squares, 6,436 moves |
| PALL. Every pair closed along its line of centres to contact and past (pair-level) | A’s margin exactly 0 and $-10^{-40}$; the corner projections’ exactly 0 at contact; B touching and overlapping, both orders agreeing | as stated: 415,059 pairs, 830,118 closings |
| X1. Form P with every $t$ replaced by $-t$, against the original form C; and the mirrored rows decided | the twin relation fails at exactly the squares whose $t$ is not 0, 1 or $-1$; on the mirrored packing the methods agree everywhere | as stated: the twin fails at the 51 to 278 tilted squares; the mirrored packing is refused at every count |

All 481 came out as stated: `EVERY_CONTROL_AS_STATED` at each count.

How each rule landed at each count:

| n | S1b: $1/q$; verdict | $W$; squares at it | $S - X$; contacts of E1c | K1c: $1 - g^*$; a square in first contact, and its wall | P1: pair, square moved, margin | W1: squares at left, bottom, right, top | X1: tilted squares; mirrored packing |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 147 | $10^{-30}$; accepted | $1.001577 \times 10^{-28}$; 13 | $2.001577 \times 10^{-28}$; 30 | $2.000000 \times 10^{-28}$; square 1, bottom | (115, 118), 118, $2.000 \times 10^{-28}$ | 2, 1, 95, 45 | 57; refused, 56 pairs overlap |
| 156 | $2 \times 10^{-30}$; accepted | $1.009791 \times 10^{-28}$; 24 | $2.009791 \times 10^{-28}$; 35 | $2.000000 \times 10^{-28}$; square 1, left | (76, 126), 126, $2.000 \times 10^{-28}$ | 1, 100, 12, 12 | 61; refused, 60 pairs overlap |
| 180 | $4 \times 10^{-30}$; accepted | $1.005122 \times 10^{-28}$; 1 | $2.005122 \times 10^{-28}$; 18 | $2.000000 \times 10^{-28}$; square 35, left | (34, 139), 139, $1.445 \times 10^{-24}$ | 35, 126, 143, 47 | 51; refused, 63 pairs overlap |
| 210 | $10^{-30}$; accepted | $1.009438 \times 10^{-28}$; 27 | $2.009438 \times 10^{-28}$; 47 | $1.999993 \times 10^{-28}$; square 188, bottom | (196, 208), 208, $2.000 \times 10^{-28}$ | 1, 13, 113, 12 | 75; refused, 86 pairs overlap |
| 260 | $10^{-30}$; accepted | $1.008143 \times 10^{-28}$; 23 | $2.008143 \times 10^{-28}$; 48 | $2.000000 \times 10^{-28}$; square 203, bottom | (6, 11), 11, $2.000 \times 10^{-28}$ | 207, 203, 231, 233 | 127; refused, 170 pairs overlap |
| 262 | $3.2 \times 10^{-29}$; accepted | $1.004989 \times 10^{-28}$; 18 | $2.004989 \times 10^{-28}$; 39 | $2.000000 \times 10^{-28}$; square 1, bottom | (211, 230), 230, $2.000 \times 10^{-28}$ | 117, 1, 14, 92 | 110; refused, 90 pairs overlap |
| 268 | $8 \times 10^{-30}$; accepted | $1.000055 \times 10^{-28}$; 15 | $2.000055 \times 10^{-28}$; 28 | $2.000000 \times 10^{-28}$; square 1, left | (228, 264), 264, $2.000 \times 10^{-28}$ | 1, 93, 173, 5 | 120; refused, 75 pairs overlap |
| 270 | $10^{-30}$; accepted | $1.005707 \times 10^{-28}$; 1 | $2.005707 \times 10^{-28}$; 7 | $2.000000 \times 10^{-28}$; square 69, bottom | (164, 193), 193, $2.000 \times 10^{-28}$ | 75, 69, 260, 223 | 200; refused, 149 pairs overlap |
| 272 | $2 \times 10^{-28}$; refused, 30 cross | $1.003177 \times 10^{-28}$; 30 | $2.003177 \times 10^{-28}$; 49 | $1.999985 \times 10^{-28}$; square 184, left | (184, 187), 187, $2.000 \times 10^{-28}$ | 1, 1, 164, 10 | 97; refused, 99 pairs overlap |
| 292 | $10^{-30}$; accepted | $1.001727 \times 10^{-28}$; 1 | $2.001727 \times 10^{-28}$; 4 | $2.000000 \times 10^{-28}$; square 12, left | (196, 209), 209, $4.238 \times 10^{-15}$ | 12, 116, 223, 62 | 278; refused, 105 pairs overlap |
| 295 | $5 \times 10^{-30}$; accepted | $1.004545 \times 10^{-28}$; 9 | $2.004545 \times 10^{-28}$; 19 | $2.000000 \times 10^{-28}$; square 1, bottom | (80, 81), 81, $1.776 \times 10^{-20}$ | 133, 1, 78, 220 | 200; refused, 107 pairs overlap |
| 299 | $8 \times 10^{-30}$; accepted | $1.009403 \times 10^{-28}$; 30 | $2.009403 \times 10^{-28}$; 51 | $2.000000 \times 10^{-28}$; square 1, bottom | (50, 53), 53, $2.000 \times 10^{-28}$ | 104, 1, 86, 107 | 118; refused, 122 pairs overlap |
| 307 | $2 \times 10^{-29}$; accepted | $1.000641 \times 10^{-28}$; 25 | $2.000641 \times 10^{-28}$; 51 | $2.000000 \times 10^{-28}$; square 21, bottom | (48, 113), 113, $2.000 \times 10^{-28}$ | 73, 21, 28, 42 | 114; refused, 112 pairs overlap |

- **S1.** No certificate touches a wall, so $W$ is positive at every count,
  $1.0001 \times 10^{-28}$ to $1.0098 \times 10^{-28}$. The side lowered by $10^{-40}$
  is still accepted everywhere, and by one unit of its own denominator at twelve counts;
  at 272 that unit, $2 \times 10^{-28}$, exceeds $W$, and 30 squares cross, as the rule
  gives. Lowered by exactly $W$ the box touches the packing at 1 to 30 squares and is
  accepted (S1c), and $10^{-40}$ lower those squares cross (S1d). In the box of the
  claim nothing changes class (S1e); in the box one unit of the twelfth place smaller,
  10 to 32 square–wall pairs cross (S1f).
- **E1.** Moved to the corner of a box of its own extent, each packing touches the left
  and bottom walls and the right or the top, at 4 to 51 square–wall pairs in all: both
  the right and the top at ten counts, where the width and the height are equal, the
  right alone at 180 and 292 and the top alone at 270. $10^{-40}$ smaller, the squares
  at those walls cross.
  So each side exceeds its packing’s extent by exactly the $S - X$ of the table.
- **K1.** With the walls held as constraints the first contact is at the left or bottom
  wall at every count, at $1 - g^* = 2 \times 10^{-28}$ to the figures printed
  ($1.999993 \times 10^{-28}$ at 210 and $1.999985 \times 10^{-28}$ at 272, where a
  tilted square binds); no pair touches first.
  $10^{-40}$ further those squares cross and still no pair overlaps.
  This is a control of the checker at a contact it did not choose, not a measure of the
  certificates’ padding, which the review takes up after the freeze.
- **P1.** At every count the tightest pair is eligible at the first try, with its second
  square moved; the fallback the plan states was not used.
- **W1.** At every wall of every count the nearest square is eligible, so the whole
  packing was never translated.
  The squares moved were $10^{-28}$ to $5.6 \times 10^{-16}$ from their walls.
- **PALL and WALL.** All 415,059 pairs, not only the near ones, were closed along their
  lines of centres: with the centre difference scaled by $s$ the margin is
  $s \max_w \lvert d \cdot w\rvert - H$, so
  $s = (m^* + H)/\max_w \lvert d \cdot w\rvert$ makes it exactly $m^*$ ($0$ or
  $-10^{-40}$). Every square was taken to its nearest wall and past it: 6,436 moves.
- **X1.** Read clockwise, form P differs from form C at exactly the tilted squares, 51
  (180) to 278 (292) of them; the mirrored rows, decided as a packing in both forms, are
  refused at every count, with 56 to 170 pairs overlapping and no square outside the
  box, and the two methods agree at every pair of them.
- **The priors.** The plan’s six predictions held: every certificate is accepted in both
  forms with the twin relation at every square, every pair strictly apart and every wall
  strictly clear; each claim is the 12-place ceiling of its side; S1a is accepted
  everywhere and S1b wherever $1/q \le W$; S1e is accepted and S1f refused; K1c’s first
  contact lies within $10^{-26}$ of scale 1; and X1’s mirrored packing is refused at
  every count, each of which has tilted squares.

## What This Review’s Checker Shares

- **With other checkers.** It shares no code with any other checker, and it was written
  and frozen before the author’s programs, or any of this repository’s witness, verifier
  or promotion code, was read.
  It reuses nothing of any earlier review’s programs, none of which it opened.
  Its two methods follow the mathematics the model’s text describes, separating axes in
  integer arithmetic and exact clipping with a sides-and-diagonals unit test, wall
  classes by clipping against each wall’s outer half-plane and containment by area, and
  implement them afresh.
  Unlike the model, method A works from centres and directions and never reads a corner,
  as these certificates’ form P allows, and the corner projections are the third
  formulation, checked against method A on every pair (C0). Its controls follow the
  model’s list, recast for certificates that touch nothing: the box brought to the
  packing’s extent (S1c, S1d, E1), the whole packing contracted to its first contact
  (K1), and the tangent read the other way (X1) are this review’s.
- **With the author’s tools.** The issue says three programs of the author’s checked
  form P, `verify_bound_certificate.py` (Fractions; separating axes, strict),
  `verify_area_exact.py` (Fractions; Sutherland–Hodgman clipping) and
  `verify_algebraic_bounds.py` (the sides against closed forms and other reports), and
  that this repository’s `check_rational_witness_independent.py` accepted form C. The
  author’s two deciders use the same two ideas as this review’s methods; this checker
  shares no code with them or with the repository’s, none of which it has read.
  It shares the files, the definitions (unit square, box, disjoint interiors) and form
  C’s stated meaning.
- **Its trust base.** CPython 3.14.7’s integers and `fractions`, GMP 6.3.0 through
  `gmpy2` 2.3.1, PyYAML 6.0.3 for parsing and composing only, and the facts its
  self-test exercises.
  Its two methods share the readers and, where a file is decided on its own, the
  conversion between the forms, which the twin relation and both methods’ unit tests
  check.
- **Authorship.** The issue says the packings were “discovered by Mykhailo Polkovskyi,
  assisted by Gemini”.
  This review was written by a Claude agent, as was the model review; the independence
  claimed here is of code and of what was read.

## Findings

| Id | Severity | Where | Finding |
| --- | --- | --- | --- |
| F1 | note | the 26 files | each count’s two files are one exact packing at its side by both methods, every square, wall and pair, with no distance filter; every pair strictly apart and every wall strictly clear |
| F2 | note | the controls | all 481 stated controls, 37 at each count, came out as stated |
| F3 | note | the claims | each claim is the 12-place ceiling of its side; the squares are accepted in the box of the claim and cross the walls of the box one unit of the twelfth place smaller |
| F4 | note (records) | the two forms | form C is form P’s corners, square by square in one order; form P states neither its reading nor its box, and form C fixes both; read clockwise, form P is another configuration, which overlaps |
| F5 | note (records) | the margins | no contact anywhere: walls cleared by $10^{-28}$, pairs by $2.0000 \times 10^{-28}$ at ten counts, $1.44 \times 10^{-24}$ at 180, $1.78 \times 10^{-20}$ at 295 and $4.24 \times 10^{-15}$ at 292; each side exceeds its packing’s extent by $2.0001 \times 10^{-28}$ to $2.0098 \times 10^{-28}$; what this slack is against the record’s is measured after the freeze |
| F6 | note (author) | the issue’s certificate table | “Min wall” and “Min pair” are this review’s least clearance and least margin to the figures printed, “All pairs” is $n(n - 1)/2$, and “Close pairs” is the number of pairs with centres less than $\sqrt 2$ apart |
| F7 | note (records) | each form C file, `claim` | the files call their coordinates `reported` and their method `exact-algebraic`, and state strict containment and disjoint closed squares, which hold; they name no source, and the record states its own provenance |
| F8 | note (author, records) | `n295.cert` against `n262.cert` | the 295 certificate is the 262 arrangement in an L border, solved again; its side is $5.93 \times 10^{-19}$ above the 262 side plus 1, which the 262 certificate with a border of 33 upright squares proves; the 12-place prints are equal |
| F9 | note (author) | form P, line 1 | the comment names `verify_cert.py`, a program the issue does not list among its checks |
| F10 | note (records, at adoption) | 270 and 292 | the least regular of the thirteen: at 270, 85 squares turned by less than $10^{-9}$ degrees and 218 near pairs open by $10^{-27}$ to $10^{-9}$; at 292, 14 upright squares, 219 turned by less than 1°, and pair gaps of $4 \times 10^{-15}$ to $2 \times 10^{-12}$ |

**F1. Feasibility.** Each count’s certificate is an exact packing at its side: 415,059
pairs in all, each decided by both methods with equal classes and strictly apart, and
every one of the 3,218 squares a unit square inside its box by both, with area exactly 1
inside. Each file is so decided on its own, form P and form C, and the two are the same
squares. The bounds $s(n) \le S_n$ hold at 147, 156, 180, 210, 260, 262, 268, 270, 272,
292, 295, 299 and 307.

**F2. Controls.** As [Controls](#controls) gives them: 37 of 37 as stated at each count.

**F3. The claims.** Each $C_n$ is the ceiling of $S_n$ at 12 places, above it by
$1.15 \times 10^{-13}$ (307) to $9.08 \times 10^{-13}$ (292). Control S1e decides each
claim directly: in the box of side $C_n$ the squares are accepted by both methods.
Control S1f shows that the print one unit lower would not do: 10 to 32 square–wall pairs
cross it. A record can therefore hold each bound as the 12-place decimal the issue
prints, with the certificate’s own coordinates as its proof.

**F4. One packing, two forms.** The twin relation holds at all 3,218 squares with one
offset and one sense, so form C was written from form P by the formula of
[The Claims and What They Need](#the-claims-and-what-they-need).
Form P alone leaves its reading to its reader: it has no key for the origin, the axes or
the sense of $t$, and its one comment names a program.
A record that retains form P should say how it is read, or retain form C, which says so
itself. Either file alone proves the bound.

**F5. Margins of $10^{-28}$.** Every certificate is strictly inside its box and strictly
separated, as the issue claims and as the bound does not need.
The slack is by construction: $10^{-28}$ at the left and bottom walls, the side rounded
up to at most 30 places above the extent plus $2 \times 10^{-28}$, and the pairs opened
by one dilation of about $2 \times 10^{-28}$ at ten counts.
At 180, 295 and 292 the pairs are opened further, by $2.9 \times 10^{-24}$,
$3.6 \times 10^{-20}$ and $4 \times 10^{-15}$ to $2 \times 10^{-12}$. A dilation by
$\varepsilon$ of squares that span a box of side $S$ costs about $\varepsilon (S - 1)$
in side, so the first ten give away some $3 \times 10^{-27}$, 180 and 295 some
$4 \times 10^{-23}$ and $6 \times 10^{-19}$, and 292 at least $7 \times 10^{-14}$. These
are far below the gains the issue claims, and how they compare with the padding of the
packings the record holds, which is the owner’s open question RV-3, is measured after
the freeze.

**F6. The issue’s table.** The four columns of the issue’s certificate table are
reproduced: the least wall clearance prints as `1.000e-28` at every count, the least
pair margin as the issue’s value, the pair count is $n(n - 1)/2$, and the pairs whose
centres are less than $\sqrt 2$ apart number 323, 346, 404, 483, 635, 627, 597, 613,
622, 683, 714, 737 and 705, the issue’s “Close pairs”.
Two unit squares whose centres are $\sqrt 2$ or more apart cannot overlap, so a checker
may leave those pairs out; this review’s checker decides them all the same.

**F7. The files’ own claims.** Each form C file says `coordinate_provenance: reported`
and `method: exact-algebraic`, and its `limitations` sentence states “strictly inside
[0, S]^2 with pairwise disjoint closed squares”, which this review confirms as a fact of
the margins, independently re-implemented.
The witness ids are `W-nN-polkovskyi-2026-11-16`. The record should state its own
provenance for retained copies, and its own source.

**F8. 295 is 262 in an L border.** An L-shaped border of width 1 about a box of side
between 16 and 17 holds 33 unit squares, so the 262 certificate proves
$s(295) \le S_{262} + 1$ with no further search.
The 295 certificate is that arrangement solved again: its 33 border squares lie along
the left and bottom walls, 23 of them slightly turned, and its 262 inner squares lie up
to 0.079 from the 262 certificate’s. Its side is $S_{262} + 1 + 5.93 \times 10^{-19}$:
the second solve gained nothing on the first, and the pair gaps it leaves
($3.6 \times 10^{-20}$) are wider.
Both sides print as 17.698115018700 at 12 places, so nothing the issue claims changes.
A bound at 295 within $6 \times 10^{-19}$ of the certificate’s is thus a consequence of
the 262 packing, which bears on how the 295 is credited and scored.

**F9. The comment line.** Every form P file’s comment ends “verify with python3
verify_cert.py”. The issue’s checks are `verify_bound_certificate.py`,
`verify_area_exact.py` and `verify_algebraic_bounds.py`. Whether `verify_cert.py` is one
of them under another name is a question for the author.

**F10. 270 and 292.** In the other eleven files nearly every near pair sits at the
dilation’s gap. At 270, 218 of the 444 near pairs are open by more than the dilation, up
to $9.9 \times 10^{-10}$, and 85 squares are turned by angles below $10^{-9}$ degrees;
at 292 only 14 squares are upright, 219 are turned by less than 1°, and the 177 near
pairs have 173 different gaps.
Neither bears on the bounds.
They say that these two packings are not at a clean contact structure, which matters
when a house is regularized and when a later certificate claims a small gain on them.

None changes a verdict; all are notes.

## Verdict

**Accepted as upper bounds at all thirteen counts.** Each certificate proves
$s(n) \le S_n$ at its side exactly, and each of the issue’s thirteen claims is decided
directly by both methods (S1e).

- Every hypothesis holds exactly, for every square, wall and pair, by two methods that
  agree everywhere, in each of the two forms and across them.
- Every control is decided as stated beforehand.
- No defect of the certificates or of their mathematics is open; every finding is a
  note.

Mapped as an adversarial review with verdict `accepted`, it supports `V3` and `C3` at
each of the thirteen counts, provided `rv1009_check.py`’s runs are registered as
exact-algebraic evidence replayed here with full coverage of each certificate.
That reads as confirmed, independently re-implemented, clean room, by a Claude agent.
`V4` and `C4` would need a second accepted adversarial review by a distinct reviewer and
a human oversight record.
What the bounds are worth to the record, count by count, is not decided by this verdict:
the gains, the padding question and the lineage are measured after the freeze.

## What I Ran

All with CPython 3.14.7, the project interpreter, as `python -I -B` under `nice -n 19`,
from this review’s packet, two at a time.
The programs, the frozen files and the receipts are in
[`packing/resources/web/polkovskyi-1009-review-2026-11-17/`](../../../packing/resources/web/polkovskyi-1009-review-2026-11-17/README.md),
whose README gives the commands.

| Program | Receipt | CPU |
| --- | --- | ---: |
| `rv1009_selftest.py` | `out/selftest.json`: `PASSED`, 34,183 checks | 10 s |
| `rv1009_check.py`, thirteen runs | `out/check-nNNN.json`: `ACCEPT` at all thirteen | 4 to 23 s each, 156 s in all |
| `rv1009_controls.py`, thirteen runs | `out/controls-nNNN.json`: 37 of 37 as stated at each | 58 to 282 s each, 2,092 s in all |
| `rv1009_describe.py`, thirteen runs | `out/describe-nNNN.json`: the tilts, near pairs, contact factors and walls; decides nothing | 22 s in all |
| `rv1009_lstep.py` | `out/lstep-262-295.json`: the 295 certificate against the 262; decides nothing | under 1 s |

The run was priced before it started, on a synthetic packing of 106 squares with longer
scalars than the certificates’: at most 8 CPU-minutes for the checks and 2 CPU-hours for
the controls, the largest single run a quarter of an hour.
It took 38 CPU-minutes.

What went wrong along the way, and was redone before the freeze it precedes:

- **The session’s worker restarted** at about 02:00Z, while the lane was trying its
  programs on synthetic packings.
  Nothing had been frozen and no program had read a certificate.
  The lane resumed at 03:06Z from the files on disk, found the 26 pinned files and its
  programs intact, and reran the self-test and the synthetic trials before the freeze.
  No job was cut off.
- A first listing of the source’s tree asked Git for every file’s size, which on a
  blobless clone began to fetch every file; it was stopped, and only the 26 certificate
  files and the two checksum lists were fetched before the findings were frozen.
- The first self-test run found one error in the lane’s own glue (the twin comparison
  was handed fractions where it expected numerator and denominator pairs).
  Later, two expectations the lane had written by hand for the clipping were wrong and
  the code was right: Sutherland–Hodgman lists a vertex that lies on the clipping line
  twice, which changes no area.
  Both were corrected before the freeze.
- The controls program was first run on two synthetic packings in scratch space, of 12
  and 106 squares with the gaps the issue states, and on the smaller under four broken
  copies of the checker, each of which made 9 to 31 of the 37 controls fail.
  Its first price, some 4 CPU-hours at the synthetic scalar lengths, was brought down
  before the freeze: a control that changes one square, or only the side, decides again
  only what it can change and checks that the rest was read back unchanged, as the plan
  states.
- One shell command, a listing of line ends, was refused by the harness’s safety check
  and rewritten; it ran nothing.
- No program of this lane read a certificate before the freeze.
  Before it the files were touched only by `git`, `sha256sum`, `grep`, `awk`, `sed`,
  `head`, `tail`, `wc`, `od`, `file` and the like.
- `rv1009_describe.py` and `rv1009_lstep.py` were written after the freeze and before
  the findings were frozen; they decide nothing and are not in the checker’s digest
  list. `rv1009_custody.py`, `rv1009_padding.py` and `rv1009_sides.py` were written in
  the same interval, while the controls ran, and were not run on anything of the
  thirteen counts until the findings were frozen.

## Note on This Copy

This copy differs from the frozen text
(`frozen/review-2026-11-17-polkovskyi-1009.frozen.md`, bound by
`frozen/findings-frozen-digest.txt`) in one place, changed on 17 November 2026 after the
freeze by lane w3-pass-1117r: the reviewer line, which named a model identifier.
The runbook’s stage 4 says the reviewer line names the system family, tier and reasoning
setting, not a model identifier; the frozen copy is left as it was frozen.
No finding, verdict or number changes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
