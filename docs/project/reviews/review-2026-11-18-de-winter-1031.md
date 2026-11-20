# De Winter’s Packing for $s(299) \le 17.793636991744$ (#1031): Stage 4 Mathematical Review

**Date:** 2026-11-18 UTC. **Subject:** Joost de Winter’s exact rational certificate of a
packing of 299 unit squares, published in two forms, `n299/n299_exact.json` (a centre
and a unit edge direction per square) and `n299/n299_witness.yaml` (a Witness/v2 file of
rational corners), in
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/497eb478b790175ea8690671b66785b70c97f9f2/n299)
at the commit the issue pins, issue
[#1031](https://github.com/jlevy/squares/issues/1031). The issue claims
$s(299) \le 17.793636991744$, the file’s exact side rounded up at 12 places, 0.0074
below the case page’s value when it was written.

**Reviewed at:** `main` at `86284ec20`, the merge of #1023 (the import of #1009, which
made T-325 the house at 299), as this lane found it at 07:34Z on 18 November, and the
pin above.

**Reviewer:** Claude (AI review), at the strongest tier (`tbd-strong-max`) and maximum
reasoning, the blind stage 4 mathematical review lane `r1031-1118`, separately prompted.
It read the source as data and ran only programs of its own, kept with their receipts in
[`packing/resources/web/de-winter-1031-review-2026-11-18/`](../../../packing/resources/web/de-winter-1031-review-2026-11-18/README.md).
Its checker is a clean-room implementation written for this review: it reuses no code
from any earlier review, the author’s or this repository’s. It took the review of #1009
(lane `c-review-1009-1117`) as the model for method, controls and layout, and the blind
review of #1018 for the packet’s layout, read their text and READMEs, and did not open
their programs. It is not a human oversight record.

## Summary for the Author

**Verdict on the bound: accepted.** The certificate proves
$s(299) \le 17.793636991743040580325825384225613703947282755372586749208848013397$, and
the claim $17.793636991744$ is that side’s 12-place ceiling.
No finding is blocking or major.

| Squares | Pairs, all apart | Touching pairs | Wall contacts | Least pair margin (pair) | Least right-or-top clearance | Claim less side | Gain below T-325 | Verdict |
| ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| 299 | 44,551 | 0 | 28 (left 12, bottom 16) | $1.0475 \times 10^{-74}$ (137, 175) | $6.4244 \times 10^{-67}$ | $9.594 \times 10^{-13}$ | $7.367442508726 \times 10^{-3}$ | accept |

- **How the bound was checked.** A clean-room exact checker, written and frozen for this
  review before your README, your two programs, or this repository’s witness and
  verifier code were read, decided both files: every square, every wall and every one of
  the 44,551 pairs, with no distance filter and no tolerance, by two methods that share
  only the readers. They are separating axes in exact rationals, from the centres and
  edge directions of `n299_exact.json`, and exact convex clipping in GMP rationals, from
  the corners of `n299_witness.yaml`. They agree at every pair and every wall, and each
  file is also decided on its own by both methods, with identical margins.
- **The two files are one packing.** At all 299 squares the witness’s four corners are
  exactly $c + u/2 + v/2$, $c - u/2 + v/2$, $c - u/2 - v/2$ and $c + u/2 - v/2$ for the
  JSON row’s centre $c$ and direction $u$, $v$ its quarter turn: one offset and one
  sense everywhere. Both state the same side, written identically.
- **The claim.** The claim is the 12-place ceiling of the file’s side and lies
  $9.59 \times 10^{-13}$ above it; the squares are accepted in the box of the claim by
  both methods, and the box one unit of the twelfth place smaller is crossed at the
  right and top walls by 26 square–wall pairs.
- **Nothing touches but the walls.** No pair of squares is in contact: the 734 nearest
  pairs are open by $1.05 \times 10^{-74}$ to $4.0 \times 10^{-70}$, and 479 of them
  close at one contraction of their centres, $1 - 3.02309 \times 10^{-70}$. Twelve
  squares touch the left wall and sixteen the bottom wall exactly; the right and top
  walls are cleared by $6.4244 \times 10^{-67}$, so the box exceeds the packing’s extent
  by that much, and the certificate’s own contraction margin is
  $6.42436 \times 10^{-67}$.
- **Your structural statements are reproduced exactly:** 714 pairs with centres closer
  than $\sqrt 2$ (the “close pairs” your checkers test; a pair farther apart cannot
  overlap), 184 upright squares, 55 turned by at least 15° one way and 54 the other.
- **Against the record.** The house on `main` is T-325 (Polkovskyi, #1009), not T-277 as
  the case page said when you wrote; it is $3.5 \times 10^{-12}$ below T-277, and your
  gain is $7.367442508726 \times 10^{-3}$ below it.
  T-325’s own certificate shrinks by only $3.561 \times 10^{-27}$ before its squares
  first touch, so the gain is $2.07 \times 10^{24}$ times that margin.
- **A new arrangement.** No symmetry of the box pairs your squares one to one with those
  of T-325 or of any packing the record holds at 299, back to the catalogue packing; the
  closest assignment moves 121 to 131 squares by more than a tenth.
  Each of your two tilted groups does coincide, for 50 to 53 of its squares, with the
  tilted band those houses have carried since T-248, under a rigid motion of its own
  (Q2).

## Scope

**Read.**

- Issue #1031 through the REST API, the body only (fetched at 07:36:09Z, before any
  program was written; no comments then, the label `intake`; created at 06:44:45Z on 18
  November). It is kept as `programs/issue-1031.json`.
- The two certificate files at the pin, as data: first their structure with `grep`,
  `awk`, `head`, `tail`, `od` and `file` (key lines, scalar forms, line counts, tabs,
  line ends and the final byte) to write the readers, and then through the frozen
  programs. The pin’s tree listing of `n299/`, its commit metadata, the source head’s
  listing, the comparison of the pin with the head, and the source’s `SHA256SUMS`, added
  in the pin’s child commit.
- On `main`, before the checker’s freeze: `packing/witnesses/witness.schema.yaml`, for
  form C’s keys and meaning; `packing/campaign/result-import.md` (stage 4, the labels);
  `epistemics.md` (significance and novelty); the Ruff, BasedPyright and Flowmark
  exclusions, to place this review’s files; and, to locate T-325’s certificate, the file
  names of the import packet of #1009 and the heads of its two 299 files and of
  `packing/witnesses/known-best/n-299.yaml`. None of it is witness, verifier or
  promotion code.
- After the checker’s freeze: the front matter of `packing/frontier/n-299.md`; the
  claims, evidence lists and significance rationales of the register entries at 299
  (T-101, T-155, T-248, T-258, T-263, T-277, T-280 and T-325) and of the entries a
  search of `results.yaml` for 299 also returned (T-114, T-181, T-188, T-254, T-278,
  T-283, T-292 to T-295 and T-306); the certificate paths of their evidence entries; the
  heads of those certificates and of the record’s certificates at 335 and 372; and
  `attribution.md` on credit text, lineage and rearrangements.
- The models: the review of #1009,
  `docs/project/reviews/review-2026-11-17-polkovskyi-1009.md`, and its packet’s file
  list; the blind review of #1018, its packet’s README, its findings digest list and the
  difference between its frozen and mapped copies; the lines of the review of #1015,
  #1017 and #1020 by lane r127b that mention the Panoras compilation.
  Not their programs.
- The owner decisions `think-b0w5` (option D) and `think-bx2a` (credit at 262 and 292),
  their descriptions and close reasons; this lane’s bead `think-r3tn`.

**Run.** Fifteen Python programs and modules and one shell script of my own, importing
nothing from this repository or the source ([What I Ran](#what-i-ran)). They decide the
certificate twice, run a self-test and the controls, measure the contraction margins of
the certificate and of T-325, and measure custody, identity, structure, lineage and the
gains.

**Seen before my findings were written**, disclosed as the runbook asks:

- the lane’s brief, which states the issue, the pin and the two files; that T-325
  (Polkovskyi, #1009, merged in #1023) is the house; that option D asks for the gain and
  T-325’s contraction margin computed on its own certificate; the owner’s rule that
  credit follows measured identity; and the lineage the issue states;
- the coordinator’s later instruction to write this lane’s notes only in `think-r3tn`.
  Before it, at about 07:35Z, this lane had run `tbd show think-10mx --json` once, the
  import lane’s bead, and printed only its title, status, labels and parent; the title
  reads “Import #1031: Joost de Winter’s s(299) <= 17.793636991744 (0.0074 below the
  house)”. Nothing was ever written there;
- the issue, which states the claim, the case page’s value (17.801004434255294, T-277),
  the gain, the two files, the author’s two checkers and what they share, the Kaggle
  value of Nick Sarris (17.793636991746555), the lineage (diagonal slices of Asterios
  Panoras’s compilation, version 17, at 372 and 335, then local optimization and a
  reflection across $x + y = S$), the tilt counts and the AI assistance;
- the model review of #1009, which describes T-325’s certificate (its side, its
  $2 \times 10^{-28}$ margins, its least pair (50, 53)) and states that it measured
  neither padding nor identity; the descriptions of `think-b0w5` and `think-bx2a`;
- the names, and only the names, of other lanes’ files in the shared scratch space and
  under `/home/user/wt`, among them a directory `dl-1031`, which this lane did not open.

**Not read before my checker was frozen** (08:02:05Z) **or my findings were frozen**:
the source’s `README.md`, `REGISTRATION.md`, `verify_exact.py`, `check_area.py` and
`n299_record.png`; this repository’s `sqpack` witness, verifier and promotion code, its
devtools and the Rust crates; the import packet of #1009’s `measure/` and `receipts/`
directories; the import lane of #1031 (its branch
`claude/intake-2026-11-18-import-1031`, packets, receipts, ledger and bead notes); the
issue’s comments; and the model reviews’ programs.

**Not run here.** Any of the author’s code, and any of this repository’s.

## The Claim and What It Needs

Issue #1031 claims $s(299) \le C$, $C = 17.793636991744$, the 12-place print of the
certificate’s side $S$ rounded up.
The certificate proves $s(299) \le S$: there are 299 closed unit squares, rotated
freely, with pairwise disjoint interiors inside the closed square $[0, S]^2$. The claim
follows when $C \ge S$, and directly when the same squares are accepted in $[0, C]^2$.

The two files are read as follows.

- **Form J**, `n299_exact.json`: one JSON object with exactly the keys `n`, `side`,
  `square_size`, `format` and `squares`; each square a list of four scalar strings
  $[x, y, \cos, \sin]$, read as the unit square with centre $c = (x, y)$ and edge
  direction $u = (\cos, \sin)$: the set $c + \alpha u + \beta v$ with
  $\lvert\alpha\rvert \le 1/2$ and $\lvert\beta\rvert \le 1/2$, $v$ the quarter turn of
  $u$. The file’s `format` string says so, and nothing else in it states a box; the
  reading is fixed here by the witness.
- **Form C**, `n299_witness.yaml`: a softschema envelope
  (`contract: packing.squares:Witness/v2`) around a Witness/v2 record with
  `representation: corners`, `scalar.kind: rational`, `origin: lower-left` and
  `axes: x-right-y-up`: four rational corners per square, ids `square-1` to
  `square-299`.

The hypotheses are six:

1. **The reading.** Form J is ASCII JSON with no duplicate key, no number with a
   fraction or exponent and no non-finite constant; `n` an integer, `side` and every
   coordinate a scalar string.
   Form C is one YAML document with no anchors, aliases, explicit tags, duplicate keys,
   tabs or carriage returns; the envelope above, the witness keys within the schema’s
   list with every required key present, `square_size: '1'`; the squares listed with ids
   in order, each with exactly an id and four corners of two scalars.
   Every scalar is a string `p` or `p/q` with no sign but an optional minus, no leading
   zero and $q \ge 1$; lowest terms are recorded, not required.
2. **The count and the twin.** 299 squares in each file, the same side, and square $k$
   of form C is square $k$ of form J: its four corners are $c \pm u/2 \pm v/2$, listed
   as a cyclic rotation of them in either sense.
3. **Unit squares.** In form J, $\cos^2 + \sin^2 = 1$ exactly for every row.
   In form C the four corners, in the order listed, are a unit square.
4. **Containment.** Each square lies in $[0, S]^2$, the origin at the lower-left corner.
5. **Disjoint interiors.** No two squares’ interiors meet.
6. **The sense.** $x$ to the right and $y$ up, which form C states; form J’s direction
   and its quarter turn span the same square whichever edge it names.

`rv1031_check.py` decides the first two through the readers and the next three twice.

- **Method A** (`rv1031_axes.py`, `fractions.Fraction`) reads poses and never a corner.
  For a pair with centre difference $d$, the projections on any of the four unit normals
  $u_i, v_i, u_j, v_j$ have half-lengths adding to the same
  $H = 1/2 + (\lvert\cos D\rvert + \lvert\sin D\rvert)/2$, $D$ the angle between the
  squares, so the separation on a normal $w$ is $\lvert d \cdot w\rvert - H$, an exact
  distance, and the margin is the largest of the four.
  Two convex polygons have disjoint interiors exactly when a line parallel to an edge of
  one of them weakly separates them, and are disjoint exactly when one does so strictly,
  so the margin’s sign is the class: positive apart, zero contact, negative overlap.
  A wall’s clearance is the signed distance from the square’s extreme corner, from the
  half-extent $(\lvert\cos\rvert + \lvert\sin\rvert)/2$.
- **Method B** (`rv1031_clip.py`, `gmpy2.mpq`) is handed corners and nothing else.
  Four points are a unit square in cyclic order when all four sides have squared length
  1 and both diagonals squared length 2; the shoelace sum, $\pm 2$, gives the sense, and
  a clockwise listing is reversed.
  A pair is decided by clipping one square against the four closed half-planes to the
  left of the other’s edges (Sutherland–Hodgman, keeping points on the line), both ways
  round: empty is apart, non-empty with zero area contact, positive area overlap.
  Each wall is classed by the corners’ signed distances, and containment is decided
  apart: a unit square lies in the box exactly when its intersection with the box, by
  clipping, has area exactly 1.

The two share the readers (`rv1031_reader.py`) and nothing else on the form each reads
natively. `rv1031_check.py` also decides the files crossed: method A on the poses taken
from the witness’s corners and method B on the corners written from the JSON’s poses.
The verdict is `ACCEPT` only when both files are read and are one packing, both
decisions accept every square, wall and pair with equal classes everywhere and equal
clearances, the crossed decision gives the same margin at every pair, and the claim is
proved in its box. No distance filter and no tolerance is applied anywhere.

## The Certificate Decided

`out/check.json`: **`ACCEPT`**, with no problem listed.

| Fact | Value |
| --- | --- |
| Side, exactly | $17793636991743040580325825384225613703947282755372586749208848013397 / 10^{66}$, the same text in both forms |
| Squares, twin relation | 299; the witness lists every square from $c + u/2 + v/2$ counterclockwise (offset 0, all 299) |
| Pairs | 44,551, apart by both methods, directly and crossed; one margin digest `6d20ef8e…` for both |
| Least pair margin | $1.04753468319 \times 10^{-74}$, pair (137, 175) |
| Positive margins below $10^{-30}$, $10^{-12}$, $10^{-9}$, $10^{-6}$, $10^{-3}$, $10^{-2}$, $10^{-1}$ | 734, 737, 737, 745, 769, 848, 941 |
| Wall contacts (clearance exactly 0) | left 12, bottom 16, right 0, top 0 |
| Least positive clearance | $4.85 \times 10^{-71}$, square 270 at the left wall |
| Side less the width, less the height | $6.4243940592874342 \times 10^{-67}$ and $6.4243630592874417 \times 10^{-67}$ |
| Claim less side | $9.59419674175 \times 10^{-13}$; the claim is the side’s 12-place ceiling |
| In the box of the claim | accepted by both methods |
| Method B | every square counterclockwise in the witness, a unit square, area exactly 1 inside the box |
| CPU | 25 s |

`out/describe-1031.json` describes the file (it decides nothing):

- **Reading.** Both files read strictly with no scalar out of lowest terms.
  Form J has no final newline (N1). Form C’s envelope is `status: enforced`; its `claim`
  says `coordinate_provenance: reported`, `method: exact-algebraic`, and names
  `verify_exact.py` in its limitations; it has no `source` or `certificate` block.
- **Tilts.** 184 squares are exactly upright and 115 turned, by 0.0065° to 27.89°, at 32
  distinct directions: 55 by $+24.97°$ to $+27.87°$, along the top of the box ($y$ from
  11.3 to 17.1), and 60 by $-27.89°$ to $-0.0065°$, 54 of them by at least 15°, along
  the left side ($x$ from 0.66 to 6.1). Scalars have up to 167 digits.
- **Near pairs.** The 734 pairs below $10^{-30}$ are open by $1.05 \times 10^{-74}$ to
  $4.00 \times 10^{-70}$; the contraction of the centres that would close each lies
  $1.0 \times 10^{-74}$ to $3.6 \times 10^{-70}$ below 1, at 230 distinct values to 12
  figures, 479 of them at $1 - 3.02309 \times 10^{-70}$. 556 of the 734 have centres
  closer than $\sqrt 2$; the other 178 have centres at least $\sqrt 2$ apart, which two
  nearly touching unit squares reach only corner to corner.
- **Close pairs.** 714 pairs have centres closer than $\sqrt 2$: the issue’s figure.
  Two unit squares whose centres are $\sqrt 2$ or more apart lie in disjoint open discs
  of radius $\sqrt 2/2$, so a checker may leave those pairs out; this one decides them
  all.
- **Walls.** Besides the 28 exact contacts, 4 left-or-bottom clearances lie between 0
  and $10^{-60}$, and 26 right-or-top clearances lie between $6.42436 \times 10^{-67}$
  (square 95, top) and $6.42500 \times 10^{-67}$, a spread of $6.34 \times 10^{-71}$;
  the width is $3.1 \times 10^{-72}$ below the height.

## Controls

`programs/controls-plan.json` states 36 controls and the outcome of each as a rule over
the certificate’s exact facts, since those facts were unknown when it was written.
It was frozen with the checker at 08:02:05Z, before any program of this lane read a
certificate. `rv1031_controls.py` evaluates each rule exactly and compares it with what
both methods decide on the changed packing; a decision in which the methods disagree
fails its control. Reader controls change the original bytes.
A control that changes one square decides again the 298 pairs that hold it and checks
that every other square reads back as the original’s; one that changes only the side
decides no pair again.

**34 of the 36 came out as stated; S1d and E1p did not**, and the reason is the plan’s
(F3).

| Control | Stated | Outcome |
| --- | --- | --- |
| C0. Margins from the witness’s corners by corner projections; clearances from the corners | equal to method A everywhere | as stated: 0 mismatches over 44,551 pairs and 299 squares |
| R1. The last square deleted, the count as stated; each form | refused: 299 stated, 298 listed | as stated |
| R2. The side as $2p/2q$ in both forms | read, values equal, flagged not in lowest terms | as stated |
| R3. Form J: squares 1 and 2 exchanged; form C: their ids exchanged | form J read, the twin failing at exactly 1 and 2; form C refused, ids out of order | as stated |
| R4. The side as a 40-place decimal: form J, form C quoted, form C unquoted | refused: not a scalar twice, a YAML float once | as stated |
| R5. A leading `+` on square 1’s first coordinate; each form | refused | as stated |
| R6. `n` repeated; each form | refused: duplicate key | as stated |
| R7. Form J: $10^{-40}$ added to the first turned square’s cos (square 4) | refused: not a unit vector | as stated |
| G1. Square 299 given square 1’s pose and corners | refused; (1, 299) at $-1$ and each $(k, 299)$ at the original $(1, k)$; only (1, 299) overlaps, B area 1 | as stated |
| G2. Square 1 moved by $(S, 0)$ | refused; its clearances exactly $(L + S, B, R - S, T)$, area inside 0, no pair overlapping | as stated |
| G3. Form C: square 1’s first corner moved by $10^{-40}$ | refused: square 1 alone not a unit square, no pose, the twin failing there only | as stated |
| G4, G5. Form C listed in reverse; from the second corner | accepted; margins, clearances, B’s classes and areas identical; senses all clockwise, then unchanged with every offset moved by one | as stated |
| G6, G7, G8. Transposed; a quarter turn; mirrored | accepted; margins identical, clearances permuted as stated | as stated |
| S1a, S1b. The side lowered by $10^{-40}$, by $1/q = 10^{-66}$ | the side rule: right and top lowered by exactly that, crossings exactly where a clearance is smaller | as stated: refused, 26 crossings each |
| S1c. The side lowered by $W = 6.4243630592874417 \times 10^{-67}$ | accepted, contacts exactly where $W$ is attained | as stated: accepted, square 95 touching the top |
| S1d. The side lowered by $W + 10^{-40}$ | refused, exactly the squares that attain $W$ crossing | **not as stated**: refused, 26 crossings, as the side rule gives |
| S1e. The side set to the claim | accepted | as stated |
| S1f. The side set to the claim less $10^{-12}$ | the side rule | as stated: refused, 26 crossings |
| E1c. Moved by the least left and bottom clearances (both 0), the side set to the extent $X$, the height | accepted; contacts at left, bottom and top exactly as predicted | as stated: 29 contacts |
| E1p. The same with $X - 10^{-40}$ | refused, exactly the squares at the top crossing | **not as stated**: refused, 26 crossings at the right and top |
| K1c. Centres and side times $1 + 10^{-40}$ | accepted, margins exactly $(1 + \varepsilon)M - H$, no contact anywhere | as stated |
| K1p. Centres contracted towards the box centre by $1 - 10^{-40}$ | overlaps exactly where $(1 - \varepsilon)M < H$ | as stated: 734 overlaps |
| P1c, P1p. The tightest pair (137, 175) closed along its line of centres, square 175 moved | contact, accepted; then $10^{-40}$ past, only that pair overlapping at exactly $-10^{-40}$ | as stated |
| P0p. The first pair in contact pushed past | (no pair is in contact) | not applicable |
| W1c, W1p. At each wall the nearest eligible square moved to it, and past | contact, accepted; then refused, only that crossing at exactly $-10^{-40}$ | as stated at all four walls (squares 290, 297, 25, 95) |
| W0p. At each wall the first square in contact pushed $10^{-40}$ past | refused, only that crossing | as stated at the left (129) and bottom (138); not applicable at the right and top |
| WALL. Every square to its nearest wall and past | clearances exactly 0 and $-10^{-40}$ by A and B; area inside 1, then below 1 | as stated: 598 moves |
| PALL. Every pair closed along its line of centres to contact and past | margins exactly 0 and $-10^{-40}$ by A and the corner projections; B touching, then overlapping | as stated: 89,102 closings |
| X1. Form J with every sin negated, against form C; that packing decided | the twin failing at exactly the turned squares not at 45°; the methods agreeing everywhere | as stated: 115 squares; the changed packing refused with 132 overlapping pairs |
| T1. The contraction program on the original and on K1c’s dilation | $g^* = 1$ exactly when a pair touches; its own verification passing | as stated: no pair touches, $1 - g^* = 1.0007 \times 10^{-74}$ |

**What S1d and E1p show.** Both rules assumed that the least right-or-top clearance lies
more than $10^{-40}$ below the next, as it does in the certificates of #1009 on which
the plan was modelled.
Here the 26 right-or-top clearances all lie within $6.34 \times 10^{-71}$ of $W$, and
the width is only $3.1 \times 10^{-72}$ below the height, so lowering the side by
$W + 10^{-40}$, or the extent by $10^{-40}$, crosses all 26 at the right and the top.
That is exactly what the side rule of S1a predicts, both methods agree at every wall,
and nothing else changed; the two rules, not the checker or the certificate, were wrong.

**Broken copies.** The self-test fails under all seven of its broken copies
(`out/selftest.json`). Run on this certificate with an always-accepting verdict, the
controls fail G1, G2, P1p, W1p and W0p besides S1d and E1p; with an always-refusing
verdict they fail E1c, K1c, P1c and W1c besides those two (`out/broken-copies/`). On the
synthetic packing of `rv1031_synth.py`, where all 36 come out as stated, each of the
nine broken copies fails 1 to 18 controls but one, form P read clockwise, which no
control reads and the self-test catches (`out/synthetic/`).

## Against the House: Gain and Contraction Margin

The house at 299 on `main` is T-325, Mykhailo Polkovskyi’s re-solve of T-277 (#1009,
merged in #1023). Its own certificate is the import packet’s form C file,
`packing/resources/web/mishapolk-issue1009-2026-11-16/source/witnesses/2026-11-16/n-299.yaml`,
read with its form P twin `…/certificates/0000-0999/n299.cert`: the two are one packing
at all 299 squares (`out/contraction-t325.json`).

`rv1031_contract.py` shrinks a packing until its squares first touch: every centre is
multiplied by one factor $g$, the squares keeping their size and directions, and the box
is taken as small as the moved squares allow.
A pair first touches at $g_{ij} = H/M$, $M$ the largest $\lvert d \cdot w\rvert$ over
its four normals, so the packing first touches at $g^* = \max g_{ij}$; the contraction
margin is the side less the larger of the width and height at $g^*$. All of it is exact,
and the program then decides the contracted packing (accepted, with contacts exactly at
the pairs whose own factor is $g^*$) and the packing contracted $10^{-40}$ further
(those pairs, and only those, overlap).

|  | T-325 | #1031 |
| --- | --- | --- |
| Side | $17.801004434251766824147518370008$ | $17.79363699174304058032582538422561\ldots$ |
| $1 - g^*$; first pair | $2.00004386193 \times 10^{-28}$; (71, 140) | $1.00072861528 \times 10^{-74}$; (137, 175) |
| Wall slack (side less extent) | $2.00940328282 \times 10^{-28}$ | $6.42436305929 \times 10^{-67}$ |
| Contraction part | $3.36027457930 \times 10^{-27}$ | $1.68 \times 10^{-73}$ |
| Contraction margin | $3.56121490758 \times 10^{-27}$ | $6.42436473987 \times 10^{-67}$ |
| Shrunk side | $17.80100443425176682414751836644678509\ldots$ | — |
| Verification | contracted packing accepted with only (71, 140) in contact and 51 wall contacts; past it, only (71, 140) overlaps | the same with (137, 175); past it, the 734 near pairs overlap |

`out/measures.json` gives the gains exactly:

- **Below T-325:**
  $7367442508726243821692985782386296052717244627413250791151986603 / 10^{66}$, that is
  $7.36744250872624 \times 10^{-3}$.
- **Below T-325 shrunk to first contact:** $7.36744250872624 \times 10^{-3}$ to 15
  figures, the gain less $3.56 \times 10^{-27}$; the gain is $2.06880 \times 10^{24}$
  times T-325’s contraction margin.
- **Below the earlier houses:** T-280 $7.36744251107 \times 10^{-3}$, T-277
  $7.36744251225 \times 10^{-3}$ (the house the issue cites), T-263
  $7.60154223602 \times 10^{-3}$, T-258 $7.60155764554 \times 10^{-3}$, T-248
  $1.00584435893 \times 10^{-2}$, T-101 $2.92386637893 \times 10^{-2}$.

Under option D (`think-b0w5`), a re-certification of a standing packing is a new result
only if its side is below the predecessor shrunk until its squares first touch.
#1031 is not a re-certification ([Identity and Lineage](#identity-and-lineage)), and it
would pass that test by a factor of $2 \times 10^{24}$ if it were.

## Identity and Lineage

**Identity against every house at 299** (`rv1031_identity.py`, `out/identity.json`).
Each packing the record holds at 299 was read from its retained certificate, and for
each of the box’s eight symmetries, in the lower-left frame and the box-centred frame,
the nearest-centre map and the optimal assignment were measured; the table gives the
lower-left frame, and the box-centred frame agrees on every one-to-one question.
T-280’s `.cert` has a UTF-8 comment line, which the frozen reader refuses; it was read
from a copy with the comment line removed.

| House | Tilted squares | One to one under some symmetry | Best symmetry | Moved beyond $10^{-2}$, $10^{-1}$ | Largest move | Turned beyond 1° |
| --- | ---: | --- | --- | --- | ---: | ---: |
| T-325 (and the house witness drawn from it) | 118 | no, in either frame | quarter turn (rot270) | 182, 127 | 1.074 | 85 |
| T-280 | 125 | no | rot270 | 182, 127 | 1.074 | 85 |
| T-277 | 118 | no | rot270 | 183, 127 | 1.074 | 85 |
| T-263 | 117 | no | rot270 | 163, 122 | 1.074 | 84 |
| T-258 | 111 | no | rot270 | 186, 123 | 1.074 | 85 |
| T-248 | 112 | no | rot270 | 297, 121 | 1.069 | 125 |
| T-101, T-155 | 42, 38 | no | identity | 297, 129 and 131 | 1.143 | 127 |

At best, 291 of the 299 squares have distinct nearest partners in T-325, and the
assignment moves 127 squares by more than a tenth.
By the record’s measure, #1031 is a new arrangement relative to every packing it holds
at 299.

**The band the houses share** (`rv1031_lineage.py`, `out/lineage-houses.json`). Every
house from T-248 on has 111 to 125 tilted squares in a band.
Each of #1031’s two tilted groups coincides with part of that band under a rigid motion
of its own: under T-325 turned a quarter turn (rot270) and moved by $(-0.996, 0.019)$,
53 of the 60 negatively turned squares lie within 0.1 of a T-325 square whose tilt
agrees within 2°; under T-325 mirrored ($x \to S - x$) and moved by $(4.978, 9.993)$, 50
of the 55 positively turned squares do; together 103 of the 115 turned squares, the two
sets disjoint. T-258, T-263, T-277 and T-280 give 52 or 53 under the first motion, and
T-248 gives 52 and 51 under the identity and a transposition; T-101, the catalogue
construction, gives 1. These are partial coincidences: the first motion also lines up
157 upright squares, which a lattice of upright squares does under many shifts, and no
motion pairs the packings as a whole.

**The reflection across $x + y = S$** (`out/lineage.json`). Under
$(x, y, \theta) \to (S - y, S - x, -\theta)$, 258 of the 299 squares land within 0.01 of
a square of the same tilt (within 1°), 281 within 0.05 and 283 within 0.1; 50 of each
tilted group land within 0.05 on a square of the other, with median distances of
$8.7 \times 10^{-4}$ and $4.6 \times 10^{-4}$. The packing is the mirror image of itself
across that diagonal but for about 16 squares, as the issue’s last step, a reflection of
part of a tilted group across $x + y = S$, leads one to expect.

**The donors** (`out/lineage.json`). The issue names packings of 372 and 335 squares in
Asterios Panoras’s Kaggle compilation, version 17. The record holds no copy of that
compilation, and none was fetched (a Kaggle download needs an account).
Against the eight packings the record does hold at 335 and 372 (Couzo’s of 9, 15, 23 and
24 October and Polkovskyi’s of 22 and 23 October), the scan’s best motions match at most
3 turned squares: none of them supplies a slice of #1031. The issue’s lineage can
therefore be neither confirmed nor refuted here (Q1).

**Credit.** By the owner’s rule (`think-bx2a`) credit follows measured identity.
The measurement makes #1031 a new arrangement relative to every packing the record holds
at 299, so it does not take the credit of any of them, and its finder is Joost de
Winter. The antecedents the record can state are the source’s own: the 335- and
372-square packings of Panoras’s compilation (prvsiyan, areebbb, jazivxt, alexchilton).
`attribution.md` does not infer lineage from resemblance, so the band coincidence is a
measurement for the record and a question for the author (Q2), not a credit.

## Significance

**S3, as this review scores it.** The import lane’s draft score was not read, since this
lane is blind to that lane’s work; this score is for the coordinator to compare with it.

A new arrangement at 299 relative to every packing the record holds there, $7.37 \times
10^{-3}$ below the house (T-325): the second-largest step the record holds at this
count, after T-248’s $1.92 \times 10^{-2}$ below the catalogue construction (S3), and
larger than T-258’s $2.46 \times 10^{-3}$ (S3) and T-277’s $2.34 \times 10^{-4}$ (S3).
It is 392 times the top of the band where T-239’s rationale draws the S2/S3 line,
between T-198’s $1.15 \times 10^{-5}$ (S2) and T-226’s $1.88 \times 10^{-5}$ (S3), above
which new and continued arrangements are S3. The method, slices of public Kaggle
packings followed by local optimization and a reflection, is no new technique, as
T-306’s fault-line DP and quench on a public Kaggle packing is not, so not S4. No lower
bound or optimum.

Novelty is `apparently-novel` with one stated gap: the issue reports a Kaggle
leaderboard side for 299 by Nick Sarris, 17.793636991746555, $3.51 \times 10^{-12}$
above this certificate’s side, which the author takes to be the same local optimum; it
states no packing, so the record can measure nothing of it (N5).

## Custody

`rv1031_custody.py` (`out/custody.json`): **`CUSTODY_HOLDS`.**

- Both files were fetched at 07:37:14Z by two routes, raw.githubusercontent.com at the
  pin and the git-blob API by the blob ids of the pin’s tree; the bytes are identical,
  `n299_exact.json` 182,141 bytes with SHA-256 `199e6132…5ed4a9c` (blob `0a8e8120`) and
  `n299_witness.yaml` 712,311 bytes with SHA-256 `bb52b883…ddea95a6` (blob `7b6331f2`).
- The blob ids are those the pin lists and those the source’s head (`72323289`, 07:31Z)
  lists; the pin’s child `3293038d` adds `n299/SHA256SUMS`, whose two lines give these
  digests, and `n299/REGISTRATION.md`. No later commit changes the two files, as the
  issue says.
- The pin `497eb478`, “Add the packing for n = 299”, was committed at 06:34:51Z, ten
  minutes before the issue was opened.

## What This Review’s Checker Shares

- **With other checkers.** It shares no code with any other checker, and it was written
  and frozen before the author’s programs, or any of this repository’s witness, verifier
  or promotion code, was read.
  It reuses nothing of the model reviews’ programs, none of which it opened.
  Its two methods follow the mathematics the model’s text describes and implement it
  afresh; unlike the model, method A reads a centre and a direction where the model read
  a half-angle tangent.
  The controls follow the model’s list and add cases for exact contact at a pair and at
  a wall (P0p, W0p), the direction read the other way (X1) and the contraction program
  (T1).
- **With the author’s tools.** The issue says `verify_exact.py` (Fractions; separating
  axes over the pairs with centres closer than $\sqrt 2$) and `check_area.py`
  (Fractions; clipping, area exactly 0 over the same pairs) checked form J. They use the
  same two ideas as this review’s methods; this checker shares no code with them, which
  it has not read, and decides every pair, not only the close ones.
  It shares the files, the definitions (unit square, box, disjoint interiors) and form
  C’s stated meaning.
- **Its trust base.** CPython 3.14.7’s integers and `fractions`, GMP through `gmpy2`
  2.3.1, PyYAML 6.0.3 for parsing only, numpy 2.5.2 and scipy 1.17.1 for the identity
  and lineage measures (which decide nothing), and the facts its self-test exercises.
- **Authorship.** The issue says the search, the optimization and the rational
  certificate were produced with an OpenAI model and the repository files, checks and
  figure with Claude, under the author’s direction.
  This review was written by a Claude agent; the independence claimed here is of code
  and of what was read.

## Findings

| Id | Severity | Where | Finding |
| --- | --- | --- | --- |
| F1 | note | both files | one exact packing at its side by both methods, every square, wall and pair, with no distance filter; every pair strictly apart; 28 exact wall contacts at the left and bottom |
| F2 | note | the claim | the claim is the 12-place ceiling of the file’s side, the side the two files state; the squares are accepted in the box of the claim |
| F3 | note (this review) | `programs/controls-plan.json`, S1d and E1p | 34 of 36 controls as stated; the rules of S1d and E1p assumed a gap above $10^{-40}$ between the least right-or-top clearance and the next, which this certificate does not have |
| F4 | note (records) | the margins | no pair touches: 734 pairs open by $1.05 \times 10^{-74}$ to $4.0 \times 10^{-70}$; the box exceeds the extent by $6.4244 \times 10^{-67}$; the certificate’s own contraction margin is $6.42436 \times 10^{-67}$ |
| F5 | note (records) | the gain | $7.367442508726 \times 10^{-3}$ below T-325, $2.07 \times 10^{24}$ times T-325’s contraction margin of $3.561 \times 10^{-27}$; below T-325 shrunk to first contact by the same to 15 figures |
| F6 | note (records) | identity | one to one with no packing the record holds at 299 under any symmetry; the best assignment moves 121 to 131 squares beyond a tenth: a new arrangement, credited to its finder |
| F7 | note (records, author) | the two tilted groups | each coincides, for 50 to 53 of its squares within 0.1, with the tilted band the houses have carried since T-248, under a rigid motion of its own; the record’s packings at 335 and 372 show no such match |
| F8 | note (author) | the issue’s lineage | the donors are not retained here, so the slices cannot be measured; the packing is its own mirror image across $x + y = S$ for 283 of 299 squares within 0.1 |
| F9 | note (author) | the issue’s house | the issue cites T-277 (17.801004434255294); the house on `main` is now T-325, $3.5 \times 10^{-12}$ lower; the printed gain, 0.0074, is unchanged |
| N1 | note (author) | `n299_exact.json` | no final newline; harmless |
| N2 | note (author) | the issue’s structural figures | reproduced exactly: 714 close pairs, 184 upright, 55 and 54 turned by at least 15° |
| N3 | note (records) | custody | identical by two routes, as listed at the pin and the head and in the source’s `SHA256SUMS` |
| N4 | note (records) | form C, `claim` | `coordinate_provenance: reported`, `method: exact-algebraic`, no `source` block; the record states its own provenance |
| N5 | note (records) | novelty | `apparently-novel`, with the gap of a Kaggle side-only value $3.51 \times 10^{-12}$ above this side |

**F1. Feasibility.** The certificate is an exact packing at its side: 44,551 pairs, each
decided by both methods with equal classes and strictly apart, and every one of the 299
squares a unit square inside its box by both, with area exactly 1 inside.
Each file is so decided on its own, and the two are the same squares.
The bound $s(299) \le S$ holds.

**F2. The claim.** $C = 17.793636991744$ is the ceiling of $S$ at 12 places, above it by
$9.594 \times 10^{-13}$, and the squares are accepted in $[0, C]^2$ by both methods
(S1e). In the box $10^{-12}$ smaller they cross at 26 square–wall pairs (S1f). The side
the issue states is the side the files state, which is not the packing’s extent: the box
is larger by $6.42 \times 10^{-67}$.

**F3. The controls.** As [Controls](#controls) gives them, S1d and E1p came out other
than the plan stated, by the plan’s mistake; their outcomes are the side rule’s,
exactly, with both methods agreeing.
P0p is not applicable, since no pair touches, and W0p is not applicable at the right and
top walls, which no square touches.

**F4. Margins.** Nothing touches but the left and bottom walls.
The near pairs are open by $10^{-74}$ to $4 \times 10^{-70}$, most at one contraction
factor $1 - 3.02309 \times 10^{-70}$, which says the file is a contact packing opened
slightly and rounded to rationals of up to 167 digits.
The padding is $6.42 \times 10^{-67}$ in side, about $5.5 \times 10^{39}$ times below
T-325’s.

**F5 and F6. The house, and the arrangement.** See
[Against the House](#against-the-house-gain-and-contraction-margin) and
[Identity and Lineage](#identity-and-lineage).
The gain needs no padding argument: it is $10^{24}$ times T-325’s contraction margin,
and the packing is not T-325’s.

**F7. The band.** The two tilted groups of #1031, one along the left side turned
negatively and one along the top turned positively, are each a near copy of a band of
the record’s 299 houses since T-248, placed by a quarter turn and a mirror of T-325
respectively. This does not make #1031 a rearrangement of a house (no motion pairs the
packings as a whole), and the record does not infer lineage from resemblance.
It is worth knowing where the band came from: the donors at 335 and 372 may carry it
too.

**F8. The lineage.** What can be checked of the issue’s account holds: the packing is
nearly symmetric across $x + y = S$, and the tilt counts are as stated.
The slices themselves cannot be checked without the donors.

**F9. The house the issue cites.** T-325 became the house when #1023 merged, after the
issue was drafted against the case page; the gain below it is $3.5 \times 10^{-12}$
smaller than below T-277, which changes nothing printed.

None changes the verdict; all are notes.

## Questions for the Author

1. Which files of Panoras’s compilation, version 17, did the slices come from (a link, a
   commit, or the two packings themselves)?
   The record could then measure each slice against its donor, as it measures identity
   against its own houses.
2. Each of your two tilted groups coincides, for about 50 squares, with the tilted band
   of the record’s 299 packings since Evan Daniel’s T-248 (#824), under a quarter turn
   or a mirror. Did the donors at 335 and 372 already carry that band, or did the search
   use any of the record’s 299 packings?
3. Is any record of Nick Sarris’s 17.793636991746555 at 299 public beyond the
   leaderboard value, such as a notebook or coordinates?

## Verdict

**Accepted as an upper bound:** $s(299) \le S$ at the file’s side exactly, and the
issue’s claim $s(299) \le 17.793636991744$ decided directly by both methods (S1e).

- Every hypothesis holds exactly, for every square, wall and pair, by two methods that
  agree everywhere, in each of the two forms and across them.
- 34 of the 36 controls stated beforehand came out as stated; the other two came out as
  the side rule gives, against a rule of the plan that was wrong for this certificate.
- No defect of the certificate or of its mathematics is open; every finding is a note.

Mapped as an adversarial review with verdict `accepted`, it supports `V3` and `C3` at
299 provided `rv1031_check.py`’s run is registered as exact-algebraic evidence replayed
here with full coverage of the certificate.
That reads as confirmed, independently re-implemented, clean room, by a Claude agent.
`V4` and `C4` would need a second accepted adversarial review by a distinct reviewer and
a human oversight record.
What the bound is worth to the record is measured above: a new arrangement,
$7.37 \times 10^{-3}$ below T-325, S3.

## What I Ran

All with CPython 3.14.7, the project interpreter, as `python -I -B` under `nice -n 19`,
from this review’s packet, at most two at a time.
The programs, the frozen files and the receipts are in
[`packing/resources/web/de-winter-1031-review-2026-11-18/`](../../../packing/resources/web/de-winter-1031-review-2026-11-18/README.md),
whose README gives the commands.

| Program | Receipt | CPU |
| --- | --- | ---: |
| `rv1031_selftest.py` | `out/selftest.json`: `PASSED`, 14,785 checks; seven broken copies fail 1 to 1,084 checks each | 13 s |
| `rv1031_check.py` | `out/check.json`: `ACCEPT` | 25 s |
| `rv1031_controls.py` | `out/controls.json`: 34 of 36 as stated | 396 s |
| `rv1031_controls.py --mutant …`, two runs | `out/broken-copies/`: the always-accepting copy fails 7 controls, the always-refusing 6 | 790 s |
| `rv1031_contract.py`, two runs | `out/contraction-1031.json`, `out/contraction-t325.json`: `MEASURED`, verified | 25 s |
| `rv1031_custody.py` | `out/custody.json`: `CUSTODY_HOLDS`; decides nothing | under 1 s |
| `rv1031_identity.py` | `out/identity.json`; decides nothing | 3 s |
| `rv1031_describe.py` | `out/describe-1031.json`; decides nothing | 5 s |
| `rv1031_lineage.py`, two runs | `out/lineage.json`, `out/lineage-houses.json`; decide nothing | 8 s |
| `rv1031_measures.py` | `out/measures.json`; decides nothing | under 1 s |
| `rv1031_synthetic.sh` (`rv1031_synth.py` and the trials) | `out/synthetic/`; decide nothing | 5 s |
| `rv1031_price.py`, in scratch before the freeze | printed only; decides nothing | 7 s |

The run was priced before it started, on a synthetic packing of 299 squares with
84-digit centre denominators: a full decision by both methods in under 4 CPU-seconds,
the controls under an hour.
It took about 22 CPU-minutes in all, 0.37 CPU-hours, including the synthetic trials
before the freeze.

What went wrong along the way:

- **Before the freeze, on synthetic data only.** Under `python -I` the programs could
  not import one another until each added its own directory to `sys.path`. The self-test
  first expected an unquoted integer corner to be read, and the reader rightly refused
  it as the schema requires a string; the synthetic writer was corrected to quote
  integers, as the source does.
  A synthetic side `8` written unquoted was refused for the same reason.
  The self-test was then made to count a crashing broken copy check by check, and the
  symmetry controls were made to hold method B’s classes to the original’s directly;
  both before the freeze.
- **After the freeze.** `/usr/bin/time` is not installed, so the first launch of the
  self-test and the check ran nothing; they were relaunched without it.
  The frozen form P reader refuses T-280’s certificate, whose comment line is UTF-8; the
  identity and lineage measures read a copy without that line.
  The API’s commit record of the pin carries the files’ patches, the author’s programs
  among them; the copy kept in `out/custody-inputs/` keeps only its metadata and file
  list, and the patches were not read.
- **The controls plan.** Two of its rules were wrong for this certificate (F3).

## After the Freeze

Written after the findings were frozen at 08:27:44Z; it changes no finding.
Its files are in the packet’s
[`after-freeze/`](../../../packing/resources/web/de-winter-1031-review-2026-11-18/after-freeze/README.md),
outside both frozen digest lists.

- **The record’s own measure of T-325.** The import of #1009 measured T-325’s
  contraction margin with `devtools.contraction_margin`
  (`packing/resources/web/mishapolk-issue1009-2026-11-16/measure/contraction-n299-own.json`).
  That receipt, read here and its tool not run, agrees exactly with this review’s: the
  same side, the same factor ($1 - \lambda^* = 2.000044 \times 10^{-28}$), the same
  contracted side, the same margin ($3.561215 \times 10^{-27}$) and the same binding
  pair (71, 140) (`after-freeze/compare-t325-contraction.json`, from
  `rv1031_compare.py`). Two implementations that share no code give the figure option D
  needs.
- **The author’s files, read as data at 08:28:50Z** (`verify_exact.py`, `check_area.py`
  and `README.md` at the pin, `REGISTRATION.md` at `3293038d`; their digests are the
  source’s `SHA256SUMS` lines).
  Neither checker was run.
  Both do what the issue says.
  `verify_exact.py` tests each pair whose centres are closer than $\sqrt 2$ on the four
  edge directions of the two squares, with weak inequalities, so that contact passes;
  `check_area.py` clips one square of each such pair against the other with closed
  half-planes (Sutherland–Hodgman, points on a line kept) and requires an intersection
  of fewer than three vertices or of area exactly 0, and checks each square’s shoelace
  area is 1. Both build the corners in the witness’s order and both skip the pairs
  farther apart, which cannot overlap.
  Both read scalars with `Fraction(v)`, which accepts forms this review’s readers refuse
  (decimals, spaces, a leading `+`); nothing in these files uses them.
  One note for the author: `verify_exact.py`’s docstring says it runs the
  separating-axis test “on all pairs”, while it tests the 714 close pairs, as its output
  line says. `README.md` and `REGISTRATION.md` restate the issue’s text.

### Review A of #1036

Review A of the pull request that carried this review (round 1, at `573b8c3df`) approved
it and asked for the following, which this section answers.
None of it changes the verdict, a bound or a rung; the frozen text above is left as it
was frozen.

- **N5’s label (A1).** The novelty label for #1031 is `previously-published`, as for
  every result by others: the packing is published in the author’s repository at
  `497eb478` and in the issue (Custody).
  N5 should read so. The Kaggle side-only value of Nick Sarris stays a note, a priority
  note for the owner, and changes no label.

- **Whether the coincidence with T-325 is generic (A2).** F7 counted only the turned
  squares, while T-325’s best motion lines up 210 of the 299 squares.
  Written after the findings’ freeze and run at 08:55Z, `after-freeze/rv1031_generic.py`
  (`after-freeze/generic.json`) scores, for each reference and each of the eight
  symmetries of its box, the strongest translations that carry a turned square onto a
  turned square of the same tilt or an upright square onto an upright one, and the unit
  shifts of the best turned motion: 780 to 832 motions a reference.

| Reference | Best motion | Squares within 0.1, turned and upright | Motions lining up 150 or more |
| --- | --- | --- | ---: |
| T-325 | rot270, moved by $(-0.996, 0.019)$ | 210: 53 and 157 | 6 |
| T-325, its best for upright squares | rot270, moved by $(-0.006, -0.003)$ | 164: 2 and 162 | — |
| T-248 | rot270, moved by $(-0.008, -0.002)$ | 160: 0 and 160 | 4 |
| T-101, the catalogue construction, unrelated | anti-transpose, moved by $(-0.023, -0.007)$ | 162: 1 and 161 | 8 |
| #1031 itself, the identity left out | the reflection across $x + y = S$ | 283: 103 and 180 | 9 |
| #1031 itself, a unit shift | identity, moved by $(-1.000, 0.000)$ | 155: 3 and 152 | — |

The upright part of the coincidence is generic: an unrelated house lines up 161 of the
packing’s upright squares, T-325 lines up 162 under another motion, and a shift of one
unit lines up 152 of the packing’s own.
What is specific is the turned band: under T-325’s best motion, 53 of the 60 negatively
turned squares.
The motion leaves 89 squares, 30% of the packing, with no partner: all 55
positively turned squares, 7 negatively turned ones and 27 upright ones.
The positively turned group matches the same band of T-325 under a second motion
(mirror-y, moved by $(-0.024, 0.991)$, 51 turned squares), and the two groups are each
other’s mirror image across $x + y = S$.

**#1031 is not a measured continuation of T-325.** By the record’s measure it is one to
one with no house at 299. Under the best rigid motion with a free translation, 30% of
its squares, a whole turned group among them, have no partner, and what that motion
lines up beyond a generic lattice is the turned band that every house since T-248 (Evan
Daniel’s #824) carries, which #1031 holds twice.
It is a new arrangement, credited to Joost de Winter after the antecedents the source
names, and not “improved from Polkovskyi’s T-325”; were the band itself to be credited,
its first holder in the record is T-248, not T-325. The reply to Q2 and the import’s
credit note should state these counts.

- **The freeze times (A3).** GitHub’s activity record for the branch gives the evidence:
  the branch was created at `212876836f` at 08:02:06Z (committed at 08:01:53Z), and
  `c8e59efe1e` was pushed at 08:27:59Z (committed at 08:27:52Z; the digest list was
  written at 08:27:44Z). The first program run on a certificate began at 08:02:41Z, and
  the first reads after the freeze at 08:28:12Z and 08:28:50Z. The times in the frozen
  text and the frozen README (08:02:05Z and 08:27:44Z) are the lane’s own clock.

- **The house the issue cites (A5).** #1023 merged at 05:46:46Z, 48 minutes before the
  pin was committed and 58 before the issue was opened.
  The issue quotes the case page as the author read it; whether it was drafted before
  the merge, or the page had not yet been regenerated, is not known here.
  F9’s “after the issue was drafted” should read so.

- **The read of `think-10mx` (A6).** The JSON that `tbd show think-10mx --json` returned
  at 07:35:53Z held the import lane’s triage note, synced at 07:33:51Z. The filter
  printed only the title, status, labels and parent, and the note was neither printed
  nor read. Review A reports that it held the exact side, T-325’s side, the gain, the
  lineage and the Kaggle value, and no identity, margin or significance.

- **Source lines (A7).** N1 is the last byte of `n299_exact.json`, byte 182,141, a `}`
  with no newline after it.
  N4 is `n299_witness.yaml` lines 18 to 21, the `claim` block.

## Note on This Copy

This copy differs from the frozen text
(`frozen/review-2026-11-18-de-winter-1031.frozen.md`, bound by
`frozen/findings-frozen-digests.txt`) in three places, added after the findings’ freeze:
the section After the Freeze (with its answers to review A of #1036), this note and the
footer below. No finding, verdict or number changes; where review A corrects a line of
the frozen text (N5, F9), After the Freeze says so and the frozen line stays.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
