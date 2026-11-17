# Evan Daniel’s Seven Certificates of #914: Stage 4 Mathematical Review

**Date:** 2026-11-05. **Subjects:** the seven certificates and six regularized views
that
[evand/square-packing@bb4cc78](https://github.com/evand/square-packing/tree/bb4cc78e5b35103c1f177db55e9cf08974e66563/search/packer/candidates)
adds under `search/packer/candidates/`: `s175_1105.cert`, `s204_trig1.cert`,
`s260_ks_1105.cert`, `s268_1105.cert`, `s293_1105.cert`, `s303_1105.cert` and
`s304_1105.cert`, and the views `*_regularized.cert` at every count but 260. They were
reported on issue [#914](https://github.com/jlevy/squares/issues/914) and are retained
as the packets
[evand-issue914-2026-11-05](../../../packing/resources/web/evand-issue914-2026-11-05/README.md)
and
[evand-issue914-views-2026-11-05](../../../packing/resources/web/evand-issue914-views-2026-11-05/README.md).
Draft pull request [#916](https://github.com/jlevy/squares/pull/916) registers them as
the entries for #914, one at each of 175, 204, 260, 268, 293, 303 and 304. Bead
`think-lrj4`.

**Reviewed at:** branch `claude/bold-ritchie-xo28us-l51`, head `f09acabbc`; `main`
`81f06acb3`.

**Reviewer:** Claude (AI review), strong tier (`tbd-strong-max`) at maximum reasoning,
the stage 4 mathematical review lane, separately prompted.
It shared no context with the import lane.
It read the source and the lane’s records as data, and ran only programs of its own.
Those programs and their receipts are kept for the packet’s `review/review-2026-11-05/`.
It is not a human oversight record.

## Summary for the Author

**Verdict: accepted at all seven counts, at 260 with findings.** No finding is blocking
or major.

| n | Certificate | Exact side (header) | Rounded up at 12 | Least wall clearance | Least pair gap | Below the house on `main` | Verdict |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 175 | `s175_1105.cert` | $13764050051543175143919941166751/10^{30}$ | 13.764050051544 | $5 \times 10^{-21}$ exactly | $9.99999999999999 \times 10^{-21}$ | T-186 by $1.24266 \times 10^{-4}$ | accept |
| 204 | `s204_trig1.cert` | $7402180691825929362760144937013/(5 \cdot 10^{29})$ | 14.804361383652 | $5 \times 10^{-21}$ exactly | $9.99999999999999 \times 10^{-21}$ | T-264 by $3.25961 \times 10^{-3}$ | accept |
| 260 | `s260_ks_1105.cert` | $8316760475444266760475435949833/(5 \cdot 10^{29})$ | 16.633520950889 | $4.98999\ldots \times 10^{-13}$ | $9.98999\ldots \times 10^{-13}$ | T-265 by $4.61551 \times 10^{-4}$ | accept with findings |
| 268 | `s268_1105.cert` | $2109062439766878830759866953431/(1.25 \cdot 10^{29})$ | 16.872499518136 | $5 \times 10^{-21}$ exactly | $9.99999999999999 \times 10^{-21}$ | T-242 by $1.86220 \times 10^{-3}$ | accept |
| 293 | `s293_1105.cert` | $17623065212060701770633564247069/10^{30}$ | 17.623065212061 | $5 \times 10^{-21}$ exactly | $9.99999999999999 \times 10^{-21}$ | T-257 by $1.09173 \times 10^{-2}$ | accept |
| 303 | `s303_1105.cert` | $17901832750854048761575294038467/10^{30}$ | 17.901832750855 | $5 \times 10^{-21}$ exactly | $9.99999999999999 \times 10^{-21}$ | T-240 by $5.14548 \times 10^{-3}$ | accept |
| 304 | `s304_1105.cert` | $17920944093340242061198022152503/10^{30}$ | 17.920944093341 | $5 \times 10^{-21}$ exactly | $9.99999999999999 \times 10^{-21}$ | T-242 by $5.95481 \times 10^{-3}$ | accept |

- **How it was checked.** A clean-room exact checker written for this review decided all
  thirteen files, every wall and every pair, with no distance filter, by two methods:
  separating axes in Python fractions, and exact clipped areas in GMP rationals.
  The two methods agree pair by pair.
  Every pair is strictly apart (none touches), and every square lies strictly inside its
  box. The six views decide the same way at their certificates’ sides.
- **Controls.** Fourteen sharp and gross controls per file, 182 in all, come out as
  stated in advance, and reading the rotation the other way makes every file infeasible.
- **Your points.** Each KKT certificate is its 80-digit point dilated by $1 + 10^{-20}$
  about the corner, side rounded up at 30 places; each view is its regularized point
  dilated the same way, and at 303 the view’s box is $1.9066 \times 10^{-32}$ above
  $S^*$, as you say.
- **260.** The certificate dilates `s260_ks_1105.input.txt` by the factor
  $1 + 10^{-12}$, as its first line says (“delta 1e-12”), so its side is
  $1.66 \times 10^{-11}$ above the input’s; the issue’s $8.8 \cdot 10^{-12}$ is its
  excess over the pre-descent input’s side (F3, question 1). The issue’s
  $S' = 16.633520950888535$ is the side’s binary64 value (F4).
- **Against the houses.** No symmetry of the box pairs any of the seven one to one with
  the house’s packing, so all seven are new arrangements, as you say.
  At 260 the tilted island is #845’s, turned through a half turn and raised by one unit,
  in a rebuilt frame: a new arrangement built on that island, not a further arrangement
  of #845’s packing.
- **The gains are real.** Each improvement is at least $6 \times 10^{8}$ times all of
  its house’s slack, measured exactly.
- **Custody.** The thirteen digests you printed are the files’, and the retained files
  are the bytes at `bb4cc78`, fetched here independently.
- **Credit.** As you ask: Evan Daniel, with Chris Deotte credited for the method; the
  register’s 175 packing as the start at 175, and #845’s island from Kirill Tymchishin’s
  Kaggle start at 260.
- **Significance.** S3 at all seven, as drafted.

F3 is a minor finding for you, which the record repeats (question 1); F13 is a minor
finding for this repository’s records; the rest are notes.

## Scope

**Read.**

- `packing/campaign/result-import.md`, stages 3 and 4, and `epistemics.md`: the ladders,
  independence, significance and credit; `attribution.md`.
- Issue #914 through GitHub’s REST API (body last edited 21:18:34Z; no comments).
- Both packets as data: the certificates, views, 80-digit points, inputs, pre-descent
  inputs, run summaries, prior facts, regularized JSON, `LICENSE`, `CREDITS.md` and
  `acquisition/`. After the freeze, also the packet READMEs, `receipts/` and `measure/`.
- On `main`: the house witnesses `n-175.yaml` … `n-304.yaml`, T-257’s `s204_1028.cert`,
  `s260_1028.cert` and `s293_1028.cert`, `upper_bound_houses.ADOPTED`, and the register
  rows named below.
- A blobless fetch of evand/square-packing at `bb4cc78` and its parent, made for this
  review through the session’s git proxy.
- After the freeze: the seven draft entries for #914 on the branch, the report evidence
  `E-evand-914-certificate-report`, the bibliography key, and the lane’s ledger.

**Run.** Thirteen programs, all mine, importing nothing from this repository or the
source ([What I Ran](#what-i-ran)). They decide all thirteen files twice, run the
controls and a self-test, do the side arithmetic, read your points against the
certificates, measure each house’s slack, measure the identity against each house, and
check custody.

**Seen before my findings were written**, disclosed as the runbook asks:

- The brief (`think-lrj4` and its parent).
  It quotes the lane’s results: the route totals, the clearances ($5 \times 10^{-21}$
  and $9.99 \times 10^{-21}$; at 260 $4.98 \times 10^{-13}$ and $9.98 \times 10^{-13}$),
  the identity counts (60, 66, 42 and 33 against T-257, 80, 193, 124, 66) and tilt
  counts, the views’ and inputs’ relations, and the issue’s relationship numbers.
- The draft entry for #914 at 175 on the branch, read after this review’s identity run;
  its notes give the lane’s identity figures at 175 and its sharp-control design.
- Register rows on `main` for T-186, T-188, T-230, T-239, T-240, T-242, T-257, T-263,
  T-264 and T-265, and the significance rationales of T-185, T-189, T-230, T-244, T-257
  and T-265. The last two state the 31 October and 5 November reviews’ significance
  conclusions.
- The 23 October review of T-239 (its identity section and RF-4) and the 16 October
  review’s RT-1, read for the record’s rule on refinements and arrangements.
- Packet A’s `acquisition/sources.json` and the keys of `acquisition/report.json`.

**Not read before my findings were frozen.** The lane’s `receipts/` and `measure/` in
either packet, its ledger, the packet READMEs, the draft entries at 204 to 304, and the
31 October, 4 November and 5 November reviews.
The coordinator named the 4 and 5 November reviews as the structural precedent; their
format was taken after the freeze ([Frozen Findings](#frozen-findings)).

**Not read here.** Evan Daniel’s `verify_cert.py` and `verify_cert2.py` (hashed only),
any other source program, `sqpack`’s witness verifier,
`devtools.check_rational_witness_independent` and `devtools.upper_bound_reports`. None
of the maintained routes, and none of the author’s code, ran here.

**Not reviewed.** The adoption and regularization at each count, which follow on the
same branch; the local-optimality statements, which are the author’s.

## The Claim and What It Needs

Each claim is $s(n) \le S$: $n$ closed unit squares, rotated freely, with pairwise
disjoint interiors inside the closed square $[0, S]^2$, where $S$ is the header side.

**The format.** After comment lines starting with `#`, a header `n S` is followed by $n$
rows `x y t`: a rational centre and the rational $t = \tan(\theta/2)$. Line 1 of the six
KKT certificates and the six views says so: “unit squares, centre (x, y), rotation (c,
s) = ((1-t^2)/(1+t^2), 2t/(1+t^2))”. Line 1 of the 260 certificate names its generator
and input instead (“dilation certificate (dilate_cert.py, delta 1e-12) of …”).

**The squares.** With $c = (1 - t^2)/(1 + t^2)$, $s = 2t/(1 + t^2)$, $u = (c, s)$ and
$u^\perp = (-s, c)$, square $i$ is
$Q_i = \{(x_i, y_i) + \alpha u_i + \beta u_i^\perp : \lvert\alpha\rvert, \lvert\beta\rvert \le 1/2\}$.

The claim needs six hypotheses, each checked separately:

1. **The reading.** Each file is ASCII with LF line ends and a final newline: one
   comment line, the header, and $n$ rows of three rational tokens (integers or `p/q`).
   The reader refuses any other token, line or count.
2. **The side.** The header side is the claim’s fraction.
3. **Unit squares.** $c^2 + s^2 = 1$ for every rational $t$; method B also requires each
   square’s shoelace area to be exactly 1, and it is, for all 3,354 rows.
4. **Containment.** $Q_i \subseteq [0, S]^2$ exactly when every corner lies in it
   (method A), equivalently when $Q_i$ clipped to the box keeps area 1 (method B).
5. **Disjoint interiors.** Two convex polygons have disjoint interiors exactly when,
   along one of the edge normals $\pm u_i, \pm u_i^\perp, \pm u_j, \pm u_j^\perp$, their
   projections overlap in at most a point (method A: the Minkowski difference
   $Q_i - Q_j$ has those normals, and $0$ lies outside its interior exactly then).
   Equivalently, $\operatorname{area}(Q_i \cap Q_j) = 0$, since a convex set has
   positive area exactly when its interior is nonempty (method B).
6. **The rotation sense.** The format fixes the sense only through $(c, s)$. Read the
   other way, with $u = (c, -s)$, every file has overlapping pairs, so the sense
   matters, and the stated one is the one that holds.

Method A is `fractions.Fraction`, with corner projections onto the four axes.
Method B is Sutherland–Hodgman clipping by cross products with the shoelace area, in
`gmpy2.mpq`, building its corners from $t = p/q$ by its own formula.
The two methods share only the reader.
Each also classifies a pair three ways, and the classes must agree: separated (gap
$> 0$; clipped polygon empty), touching (gap $= 0$; non-empty, area 0) and overlapping.

## The Certificates Decided

| File | SHA-256 | Pairs | Least wall clearance (square, line, wall) | Least pair gap (squares, lines) | Reversed sense |
| --- | --- | ---: | --- | --- | --- |
| `s175_1105.cert` | `32749cb2…` | 15,225 | $5 \times 10^{-21}$ (1, line 3, left and bottom) | $9.999999999999992 \times 10^{-21}$ (145, 164; lines 147, 166) | refused: 69 pairs |
| `s175_1105_regularized.cert` | `786519ad…` | 15,225 | $5 \times 10^{-21}$ (1, line 3) | $9.999999999999990 \times 10^{-21}$ (157, 160) | refused: 63 |
| `s204_trig1.cert` | `17ed0e5b…` | 20,706 | $5 \times 10^{-21}$ (1, line 3) | $9.999999999999992 \times 10^{-21}$ (131, 132; lines 133, 134) | refused: 67 |
| `s204_trig1_regularized.cert` | `55007aca…` | 20,706 | $5 \times 10^{-21}$ (87, line 89) | $9.999999999999990 \times 10^{-21}$ (162, 169) | refused: 69 |
| `s260_ks_1105.cert` | `24edcc0b…` | 33,670 | $4.98999999999999991\ldots \times 10^{-13}$ (258, line 260, right) | $9.98999999999999981\ldots \times 10^{-13}$ (98, 244; lines 100, 246) | refused: 173 |
| `s268_1105.cert` | `50f97048…` | 35,778 | $5 \times 10^{-21}$ (11, line 13) | $9.999999999999990 \times 10^{-21}$ (20, 27; lines 22, 29) | refused: 96 |
| `s268_1105_regularized.cert` | `cfb1f7a7…` | 35,778 | $5 \times 10^{-21}$ (6, line 8) | $9.999999999999989 \times 10^{-21}$ (81, 82) | refused: 93 |
| `s293_1105.cert` | `0fc70228…` | 42,778 | $5 \times 10^{-21}$ (1, line 3) | $9.999999999999992 \times 10^{-21}$ (187, 198; lines 189, 200) | refused: 76 |
| `s293_1105_regularized.cert` | `76d57b85…` | 42,778 | $5 \times 10^{-21}$ (127, line 129) | $9.999999999999992 \times 10^{-21}$ (183, 191) | refused: 78 |
| `s303_1105.cert` | `2f53c049…` | 45,753 | $5 \times 10^{-21}$ (236, line 238) | $9.999999999999990 \times 10^{-21}$ (90, 91; lines 92, 93) | refused: 117 |
| `s303_1105_regularized.cert` | `42a8ecd9…` | 45,753 | $5 \times 10^{-21}$ (271, line 273) | $9.999999999999987 \times 10^{-21}$ (6, 203) | refused: 118 |
| `s304_1105.cert` | `44040232…` | 46,056 | $5 \times 10^{-21}$ (239, line 241) | $9.999999999999989 \times 10^{-21}$ (29, 233; lines 31, 235) | refused: 106 |
| `s304_1105_regularized.cert` | `ee95b657…` | 46,056 | $5 \times 10^{-21}$ (239, line 241) | $9.999999999999989 \times 10^{-21}$ (29, 233) | refused: 96 |

All 446,262 pairs and every square’s containment (13,416 wall constraints by method A,
3,354 clipped areas by method B) are decided with equal verdicts, and every file is
**accepted**. The least clearances and gaps are exact fractions in the receipts; the
least wall clearance of the twelve KKT files and views is exactly $1/(2 \cdot 10^{20})$.
The pairs below $10^{-6}$ are mostly the dilated point’s contacts near $10^{-20}$ (210
at 175 to 886 at 293), with a few weakly active pairs between $10^{-16}$ and $10^{-7}$;
the 303 view has 20 pairs between $10^{-19}$ and $10^{-16}$, from its regularized box,
and at 260 the contacts sit near $10^{-12}$.

`self_test.py` holds both methods to 19 known answers: aligned squares edge to edge and
corner to corner, a 3-4-5 square ($t = 1/2$) with a vertex on an edge and on a corner,
in both senses, $10^{-30}$ either side of each, a duplicate, a nested square, and walls
at contact and $10^{-30}$ past.
It decides 3,000 random rational pairs and 6,000 more moved to exact contact along their
separating axis and $10^{-30}$ past it, and both methods agree on every one.
The reader refuses 14 malformed variants (a blank line, CRLF, no final newline, a count
mismatch, four tokens, a decimal, a zero or signed denominator, a plus sign, an
underscore, a double space, a zero count, an exponent, a non-ASCII digit).

## Sharp Controls

`sharp_controls.py` states each control’s expected verdict from its construction before
either method decides it.
“Contact” is a margin of exactly 0, “past” is $10^{-30}$ beyond it.
Every control below was decided by both methods for all thirteen files.

| Control | At contact | Past |
| --- | --- | --- |
| C1: the side set to the largest corner coordinate (every wall decided; pairs unchanged) | accepted | refused at the square that sets it |
| C2: the packing translated so its least corner coordinates are 0 (every wall decided) | accepted | refused, past the left wall and, separately, past the bottom |
| C3: the least-gap pair closed along the axis of its gap | accepted, and the moved square’s other walls and pairs all hold | refused; the moved square then overlaps one or two squares |
| C4: the least-clearance square moved to its wall | accepted | refused |
| C5: a square of the least-gap pair enlarged by the least amount that closes the pair | accepted | refused |
| G1: the last square replaced by a copy of the first | refused |  |
| G2: square 1 centred at $x = -1$ | refused |  |
| G3: every square turned to $t = 0$ in place (no expectation stated) | refused (83 to 200 overlapping pairs, equal by both methods) |  |

The C3 “past” expectation needs every axis of the pair not parallel to the closing axis
to keep a gap below $-2(g + 10^{-30})$. That holds at twelve files.
At 260 the pair (98, 244) has $t = 10^{-15}$ against $t = 0$, two nearly parallel axes
with equal gaps, so the rule states no expectation there; both methods refuse it, and C5
at the same pair, whose expectation is stated, passes.

Two of this review’s own constructions were corrected before the final run, and both
earlier runs are kept: G2 first moved square 1 left by 1, which leaves it inside
wherever it sits more than about 1.71 from the left wall (seven files; both methods
accepted it there, correctly); and C3 first counted a parallel axis as a second axis.

## The Sides and the Prints

`sides_and_kkt.py` does the arithmetic exactly.

- **The claim fractions.** Each header side equals, exactly, the fraction the record
  states for its count.
- **The 12-place prints.** Each side rounds up at 12 places to the issue’s print:
  13.764050051544, 14.804361383652, 16.633520950889, 16.872499518136, 17.623065212061,
  17.901832750855 and 17.920944093341. Each side lies 0.14 to 0.97 of a unit of the 12th
  place below its print, and each gain is over $10^{8}$ such units, so none is a
  sub-print restatement.
- **The issue’s $S'$.** At six counts the issue’s $S'$ is the header side to all 30
  places. At 260 it prints $16.633520950888535$, $1.48 \times 10^{-15}$ above the side
  $16.633520950888533520950871899666$; that is the side’s binary64 value (F4).
- **The coordinates’ extent.** In the twelve KKT files and views the least corner
  coordinate is exactly $5 \times 10^{-21}$, and the side lies $5 \times 10^{-21}$ (plus
  the 30-place round-up, at most $9.2 \times 10^{-31}$) above the largest.
  So the corners span the side less $1.0 \times 10^{-20}$ in each direction: the
  dilation’s padding. At 260 they span it less $1.0002 \times 10^{-12}$ in $x$ and
  $1.0007 \times 10^{-12}$ in $y$ ($5.012 \times 10^{-13}$ at the near walls,
  $4.990 \times 10^{-13}$ and $4.995 \times 10^{-13}$ at the far ones).
  The claims are the header sides; the extents are smaller and change no print.
- **The views.** Each view’s header states its certificate’s side exactly, and each has
  the same $5 \times 10^{-21}$ margins.
- **The houses’ sides.** Each house side on `main`, rounded up at 12 places, is the
  issue’s “best public bound before it”.

## Your Points and Views

Read as data at 120 digits, only as far as they bear on the certificates:

- **The six KKT certificates** are their `.exact.txt` points dilated by $1 + 10^{-20}$
  about the corner. $S' - (1 + 10^{-20}) S^*$ lies between $6.7 \times 10^{-32}$ and
  $9.2 \times 10^{-31}$ (the 30-place round-up of the side); every centre is
  $(1 + 10^{-20})$ times the point’s within $5.0 \times 10^{-36}$, and every angle
  $2 \arctan t$ is the point’s within $5.7 \times 10^{-34}$ degree.
  The issue’s $S^*$ prints are prefixes of the points’ values.
- **The six views** are likewise $(1 + 10^{-20})$ times the regularized points their
  JSON files carry (centres within $5.0 \times 10^{-36}$). Each regularized point’s box
  is $S^*$ within $5 \times 10^{-49}$, except at 303, where it is
  $1.9066 \times 10^{-32}$ above $S^*$, and $(1 + 10^{-20}) S_{\text{reg}} \le S'$ there
  too, as the issue says.
- **The 260 certificate** is `s260_ks_1105.input.txt` dilated by
  $1 + \mathrm{fl}(10^{-12})$: its side is the input’s stated $16.6335209508719$ times
  that factor rounded up at 30 places, exactly, and every centre is the input’s times
  the same factor within $5.0 \times 10^{-31}$ in $x$ and in $y$. Its angles are the
  input’s within $5.7 \times 10^{-14}$ degree modulo 90. Read exactly, the input itself
  overlaps in 19 pairs, by up to $3.9 \times 10^{-16}$, and reaches
  $8.3 \times 10^{-16}$ past its own stated side, which the dilation clears (F3, F4).

The KKT, local-minimum and rattler statements remain the author’s numerical evidence;
nothing here tests them.

## Is the Improvement Real?

Against each house’s precision and slack, all decided exactly:

| n | House on `main` | House side | Gain | House least wall, least pair gap | House side slack |
| ---: | --- | --- | --- | --- | --- |
| 175 | T-186 | 13.76417431748659662929… | $1.24266 \times 10^{-4}$ | $3.6 \times 10^{-78}$, $7.3 \times 10^{-78}$ | $1.0 \times 10^{-76}$ |
| 204 | T-264 | 14.80762099558520801803… | $3.25961 \times 10^{-3}$ | $1.0 \times 10^{-17}$, $1.0 \times 10^{-17}$ | $1.26 \times 10^{-16}$ |
| 260 | T-265 | 16.63398250192261413979… | $4.61551 \times 10^{-4}$ | 0, $1.34 \times 10^{-15}$ | 0 |
| 268 | T-242 | 16.87436171586934582448… | $1.86220 \times 10^{-3}$ | $5 \times 10^{-21}$, $1.0 \times 10^{-20}$ | $1.69 \times 10^{-19}$ |
| 293 | T-257 | 17.63398250212278198250… | $1.09173 \times 10^{-2}$ | $5.0 \times 10^{-13}$, $1.0 \times 10^{-12}$ | $1.76 \times 10^{-11}$ |
| 303 | T-240 | 17.90697823379890015942… | $5.14548 \times 10^{-3}$ | $1.0 \times 10^{-15}$, $2.1 \times 10^{-13}$ | $3.58 \times 10^{-14}$ |
| 304 | T-242 | 17.92689890035674158972… | $5.95481 \times 10^{-3}$ | $5 \times 10^{-21}$, $1.0 \times 10^{-20}$ | $1.79 \times 10^{-19}$ |

- **Precision.** Each gain is at least $1.2 \times 10^{8}$ units of the 12th place and
  at least $7.0 \times 10^{10}$ binary64 steps at its side (both at 175). It is not
  rounding.
- **Slack.** The house side slack is how far the house’s side falls if its centres and
  side are scaled about the corner, orientations kept, until something touches
  (`scale_slack.py`, added after the freeze).
  Every gain exceeds it by at least $6.2 \times 10^{8}$ (at 293); at 260 the house has
  none, since one of its squares touches the right wall.
  The same measure gives each new certificate a slack of $S \times 10^{-20}$ ($1.4$ to
  $1.8 \times 10^{-19}$), its dilation, and the 260 one $1.66 \times 10^{-11}$.
- So no rescaling of any house reaches the new side; squares had to move, and they did
  (below).

## Identity, Lineage and the Houses

`identity.py` measures each certificate pose by pose against the house witness on
`main`, in binary64, under all eight symmetries of the box applied to the house in its
own box. It reports nearest-centre pairing and the assignment minimizing the summed
squared move, by its own Hungarian algorithm, whose optimal cost is checked against
SciPy’s.

| n | House | Best symmetry | Nearest centres one to one | Distinct nearest | Beyond 0.1 | Beyond 0.01 | Largest move | Turned beyond 1° | Tilted beyond 1° (new, house) | Tilts reversed |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| 175 | T-186 | half turn | under none | 172 | 60 | 83 | 0.774 | 38 | 48, 50 | 24 |
| 204 | T-264 | anti-transpose | under none | 202 | 66 | 126 | 1.032 | 51 | 63, 76 | 0 |
| 260 | T-265 | identity | under none | 258 | 42 | 165 | 0.602 | 15 | 103, 105 | 2 |
| 260 | T-257 | identity | under none | 256 | 33 | 160 | 0.633 | 15 | 103, 104 | 2 |
| 268 | T-242 | half turn | under none | 264 | 80 | 139 | 1.072 | 80 | 98, 81 | 29 |
| 293 | T-257 | anti-transpose | under none | 269 | 193 | 249 | 0.995 | 137 | 54, 104 | 15 |
| 303 | T-240 | anti-transpose | under none | 298 | 124 | 144 | 1.104 | 125 | 112, 102 | 42 |
| 304 | T-242 | identity | under none | 302 | 66 | 157 | 0.867 | 76 | 110, 99 | 43 |

Box-centred assignments give the same counts within three.

**Calibration.** The same program finds T-264 one to one with T-257’s 204 under the
identity, 6 squares beyond 0.1 (largest 0.190), and T-265 one to one with T-257’s 260,
26 beyond 0.1 (largest 0.382), both as the register states; and the house witness at 293
has the poses of T-257’s `s293_1028.cert`, in binary64.

**Tilts.** No tilted square of a new packing shares an angle (within 0.01°, up to sign)
with any of its house’s at 175, 293, 303 and 304. At 204 five do, and at 268 fourteen,
single coincidences beside different main groups: 26.37° ×9, 27.00° ×8 against the
house’s 26.64° ×30, 26.43° ×18 at 204; 22.29° ×24, 23.64° ×18 against 24.16° ×74 at 268.
The issue’s “no shared tilt angle”, measured on regularized views, is the author’s.

**Inputs and views.** Each certificate pairs one to one with its binary64 input under
the identity, row for row: largest move $1.41 \times 10^{-4}$ at 175, 303 and 304,
$1.25 \times 10^{-6}$ at 204, $1.64 \times 10^{-7}$ at 293, $1.57 \times 10^{-8}$ at 268
and $2.28 \times 10^{-11}$ at 260. Each view pairs with its certificate by the optimal
assignment, under a half turn at 204, 293 and 303 and the identity elsewhere, with 3 to
8 squares beyond 0.1 (largest 0.332 to 0.623); by nearest centres it is one to one
except at 293 (292 distinct).

**The reading.** The record keeps “refinement” for a packing that pairs one to one with
another and moves no square beyond a tenth, and “further arrangement”, or “another
arrangement of” it, for one that pairs one to one and moves some (T-239 against T-230;
T-264 and T-265 against T-257). A packing that no symmetry pairs one to one is another
arrangement than the house’s (T-230 against T-186; T-257 against T-225). By that rule
all seven are **new arrangements**, as the drafts and the issue say.

**260 and #845’s island.** The question for 260 is whether it is a further arrangement
of T-257’s packing, as T-265 is.
It is not.

- No symmetry pairs it one to one with T-257’s 260: 256 distinct nearest centres for 260
  squares. Against T-257 it moves 33 squares beyond 0.1 and 160 beyond 0.01, where T-265
  moves 26 and 64 and pairs one to one.
- `island_260.py` takes each packing’s 97 squares tilted beyond 10° (63 of them at 24.5°
  in both, as the issue says).
  Matched under each symmetry with the best translation, the new island is T-257’s
  within 0.042 (RMS 0.012, none beyond 0.1, 7 turned beyond 0.5°) only after a **half
  turn about the box centre and a shift of 1.0011 upward**. In place, with its best
  translation, 26 island squares sit beyond 0.1.
- So the island was turned and moved as a block, and the 163-square frame rebuilt around
  it: “recomposed in a 260 frame”, as the issue says, not a deformation of T-257’s
  packing. The same match finds T-265’s island T-257’s in place (identity, one beyond
  0.1), as a further arrangement’s should be.

The record’s reading is a new arrangement whose island is T-257’s, credited after
T-257’s lineage as the issue asks, and scored as a new arrangement (F8, F12).

**Lineage measured.** At 175 the issue names the register’s packing as the start,
through gadgets; the measurement shows a different arrangement (24 tilts reversed, no
shared tilt angle), consistent with a build from cropped gadgets rather than a
deformation of that packing.
At 204 the donors (Daniel’s own $s(233)$ and $s(370)$) are not public, and at 268, 293,
303 and 304 they were not recorded; nothing here can test those statements.

## What the Checkers Share

- **This review’s checker** shares no code with any other checker.
  It shares the mathematics above and the format’s meaning: $t = \tan(\theta/2)$, the
  counterclockwise sense, and the box $[0, S]^2$, taken from the certificates’ first
  line and the issue, with the sense fixed by the reversed-sense control.
  Its two methods share only the reader.
  It trusts CPython’s integers and `fractions`, GMP through `gmpy2` 2.3.1, and the
  clipping and shoelace identities its self-test exercises.
- **The source’s checkers**, by the issue’s description, use separating axes and polygon
  intersection: the same mathematics as methods A and B, which this review read only as
  that one-line description.
- **The maintained routes.** By the record’s own statements on `main` (T-248’s and
  T-257’s entries), both read Daniel’s format through the `evand-cert` reader, whose
  line filter and corner construction are transcribed from his checkers, so the lane’s
  replay shares those components with the producer (F15). Their least gaps and
  clearances equal this review’s as exact fractions (after the freeze).
- **Authorship.** The issue says the composer, the search, the checks and the request
  were done with Claude, the commit carries a Co-Authored-By trailer naming Claude, and
  `CREDITS.md` says the work was produced by Claude under human direction.
  This review was also written by a Claude agent, so the producer and the reviewer share
  a system family.
- **What is common to all.** An error in the format’s meaning or in the definition of a
  packing would be common to every checker; an error in one implementation would not.

## Custody and Licence

`custody.py` compares the packet with the issue and with this review’s own fetch.

- **The commit.** `bb4cc78e5b35103c1f177db55e9cf08974e66563`, authored and committed by
  Evan Daniel at 2026-11-05T18:29:13Z, tree `341f5ffb`, parent `39fb4f02` (the
  regularizer fix the issue names).
  It adds exactly 56 files, all under `search/packer/candidates/`.
- **The bytes.** The packet’s 53 plain copies equal upstream, and its three
  `*_vs_prior.json.gz` decompress to the upstream bytes.
  `LICENSE` and `CREDITS.md` equal upstream.
  The two checkers at the pin equal the n183 packet’s copies.
- **The digests.** The thirteen SHA-256 digests the issue prints equal the packet’s
  files and upstream’s.
- **The licence.** MIT, “Copyright (c) 2026 Evan Daniel”.
  The README at the pin scopes the MIT licence to the code and carves out only
  `site/www/data/`; the certificates are not in the carve-out.
- **The issue.** Opened at 2026-11-05T19:07:50Z, 38 min 37 s after the commit, and last
  edited at 21:18:34Z. This review read the edited body (SHA-256 `d3d3b498…`); the edit
  history is not readable from this session (question 5).

Custody holds.

## Credit

- **As asked.** Evan Daniel, with Chris Deotte credited for the method (Daniel’s
  fault-line composer is his implementation of Deotte’s multi-gadget fault DP). At 175
  the register’s packing as the start (Daniil Ostashev’s, as PingYou Ltd and Mykhailo
  Polkovskyi refined it).
  At 260, #845’s island, from Kirill Tymchishin’s Kaggle $s(260)$. At 204, his own
  $s(233)$ and $s(370)$; at 268, 293, 303 and 304, donors not recorded.
- **Where it is written.** The credit is the issue’s; `CREDITS.md` and `README.md` at
  the pin do not name Deotte or the composer (question 4). The record’s precedent for
  Daniel’s composer packings is “Daniel after Deotte” (T-248, T-258).
- **175 needs no other credit.** The packing is not one to one with T-186’s under any
  symmetry (60 squares beyond a tenth, 24 tilts reversed), so it is no regularization or
  refinement of T-186’s: no `regularizations` item and no “improved by” credit, only the
  “after” credit for the start the issue asks for, as T-230’s “after Ostashev” did for a
  new arrangement found from Ostashev’s packing.
  The draft does exactly that.
- **One key for seven entries.** The draft gives all seven entries one bibliography key
  whose credit is the union of their lineages (F13), and names Polkovskyi by his handle
  (F14).

## Significance

**S3 at all seven, confirmed.** Each claim, if correct, is the smallest side on record
at its count, by a new arrangement that no symmetry pairs one to one with the house’s
packing, $1.24 \times 10^{-4}$ to $1.09 \times 10^{-2}$ below it.

- That is the record’s S3 family: T-230 at 303 ($1.86 \times 10^{-4}$, new arrangement,
  S3), T-257 at 172 to 293 ($1.64 \times 10^{-4}$ to $1.18 \times 10^{-2}$, new, S3),
  T-248 and T-258 at 299 (Daniel after Deotte, S3).
- The least, 175’s $1.24 \times 10^{-4}$, is above T-189’s $1.01 \times 10^{-4}$ (S3, a
  refinement) and of T-230’s scale.
- It is not S2: those are further arrangements and refinements, T-188
  ($9.29 \times 10^{-6}$), T-239 ($9.89 \times 10^{-6}$), T-264 ($6.48 \times 10^{-6}$)
  and T-265 ($1.99 \times 10^{-10}$). 260 is S3 by F8, not S2 as T-265 was.
- It is not S4: no new technique is claimed for the record; the composer is the author’s
  implementation of Deotte’s published method.

## Findings

| Id | Severity | Where | Finding |
| --- | --- | --- | --- |
| F1 | note | all thirteen files | each is an exact packing at its header side, by both methods, every wall and pair |
| F2 | note | this review’s controls | 182 controls and the reversed sense as stated; two of this review’s own constructions corrected |
| F3 | minor (author; the record repeats it) | issue #914, “Local optimality”, 260; `results.yaml:39213`–39214, the 260 entry’s claim; packet `acquisition/sources.json:106`, `declaration.json:14`, `report.json:178` and `README.md:23` | the certificate dilates its binary64 input by $1 + 10^{-12}$ (side $+1.66 \times 10^{-11}$), not by $8.8 \times 10^{-12}$ |
| F4 | note (author) | issue #914, the certificates table, 260 row | the $S'$ print is the side’s binary64 value; the input itself overlaps by up to $3.9 \times 10^{-16}$ |
| F5 | note | all seven | sides, prints and extents as stated |
| F6 | note | the six KKT points and views | each certificate and view is its point dilated by $1 + 10^{-20}$ |
| F7 | note (records) | the entries’ notes | identity: all seven new arrangements; the measured account for the notes |
| F8 | note (records) | the 260 entry | a new arrangement on #845’s island, half-turned and raised one unit; not a further arrangement |
| F9 | note | all seven | the gains exceed every house’s slack by at least $6.2 \times 10^{8}$ |
| F10 | note (author) | issue #914 | custody holds; the issue was edited after it was opened |
| F11 | note (records) | the 175 entry | the start credit needs no regularization or improvement credit |
| F12 | note (records) | `significance` of all seven | S3 confirmed |
| F13 | minor (records; added after the freeze) | `bibliography.yaml:4661`; `RESULTS.md:269`–275, the seven credit cells | one key’s union credit names, at five counts, antecedents the source does not give for them |
| F14 | note (records; added after the freeze) | `bibliography.yaml:4661`; the 175 entry’s claim; `n-175.md:29` on `main` | “Mishapolk” is a handle; the record’s credit name is Polkovskyi |
| F15 | note (records; added after the freeze) | the replay and review evidence still to be registered; `evidence.yaml:56623` limitations | which confirmation each run is |

**F1. Feasibility.** All thirteen files are exact packings at their header sides:
239,966 pairs over the certificates and 206,296 over the views, every one decided by
both methods with equal three-way classes, every pair strictly apart and every square
strictly inside. The bounds hold.

**F2. Controls.** As [Sharp Controls](#sharp-controls) gives them.
The reversed sense makes every file infeasible (69, 67, 173, 96, 76, 117 and 106
overlapping pairs in the certificates, the deepest about 0.29). The two corrected
constructions are this review’s, not the certificates’.

**F3. The 260 dilation.** The issue says “the certificate dilates the f64 packing (by
$8.8 \cdot 10^{-12}$)”.

- Measured, the certificate is `s260_ks_1105.input.txt` times
  $1 + \mathrm{fl}(10^{-12})$: the side exactly (rounded up at 30 places) and every
  centre within $5.0 \times 10^{-31}$. Its line 1 says “dilation certificate
  (dilate_cert.py, delta 1e-12)”, and its side is $1.663 \times 10^{-11}$ above the
  input’s ($16.6335209508719$).
- $8.83 \times 10^{-12}$ is the side’s excess over the pre-descent input’s stated side,
  $16.633520950879706$.
- The issue’s table names the input, and its “Local optimality” section gives the
  $8.8 \cdot 10^{-12}$. The draft claim at 260 and the acquisition records join the two
  as the issue’s statement, correctly attributed, but add no measurement beside it, and
  the brief repeats it.
- Proposed: “the certificate dilates its binary64 input, `s260_ks_1105.input.txt`, by
  the factor $1 + 10^{-12}$ (its side $1.66 \times 10^{-11}$ above the input’s, measured
  here); the issue gives $8.8 \times 10^{-12}$”, as T-257’s entry gives its dilations in
  side units. Question 1 asks which the issue meant.

**F4. The 260 prints and input.** The $S'$ print $16.633520950888535$ is the side’s
binary64 value, $1.48 \times 10^{-15}$ above it; its 15-place rounding would end `…534`.
The exact side is the header’s, whose 12-place round-up is the issue’s claim, so nothing
changes. The input read exactly overlaps in 19 pairs by up to $3.9 \times 10^{-16}$ and
reaches $8.3 \times 10^{-16}$ past its own side: it is not itself a packing, and the
dilation is what makes the certificate one.

**F5. Sides, prints and extents.** As
[The Sides and the Prints](#the-sides-and-the-prints) gives them.

**F6. Points and views.** As [Your Points and Views](#your-points-and-views) gives them.
Those are the author’s points read as data; they confirm how each certificate was made,
and test no optimality.

**F7. Identity.** As the table above gives it.
For the notes, the measured account adds: the best symmetry and the counts (already
there), the tilt groups, and that each view pairs with its certificate under a half turn
at 204, 293 and 303.

**F8. 260.** As [260 and #845’s island](#identity-lineage-and-the-houses) gives it.
Proposed for the notes: “its 97 squares tilted beyond 10° are T-257’s island within
0.042 after a half turn about the box centre and a shift of one unit upward; the frame
around it is rebuilt”.

**F9. The gains.** As [Is the Improvement Real?](#is-the-improvement-real) gives them.
The frozen finding compared each gain with its house’s least clearances (a factor of at
least $10^{10}$); the side-slack measure, added after the freeze, gives at least
$6.2 \times 10^{8}$.

**F10. Custody.** As [Custody and Licence](#custody-and-licence) gives it.

**F11. 175’s credit.** As [Credit](#credit) gives it.

**F12. Significance.** As [Significance](#significance) gives it.

**F13. One key, seven entries.** The seven entries share the key
`[Daniel issue 914 2026-11-05]`, whose credit is “Daniel after Deotte, Ostashev, PingYou
Ltd, Mishapolk, Tymchishin”, and the register prints that credit on each entry.

- So the entries at 204, 268, 293, 303 and 304 credit Ostashev, PingYou Ltd, Polkovskyi
  and Tymchishin, whom the source names at none of those counts; the 175 entry credits
  Tymchishin and the 260 entry Ostashev, PingYou Ltd and Polkovskyi.
- `attribution.md` asks a source’s credit to name the antecedents the source names, and
  the key does that for the issue as a whole.
  Printed on each entry, though, it reads as each packing’s lineage, which the source
  gives at none of those five counts.
  A single entry over several counts takes the union naturally (T-257, T-240); seven
  entries need not.
- Proposed: one key per lineage, “Daniel after Deotte, Ostashev, PingYou Ltd,
  Polkovskyi” at 175, “Daniel after Deotte, Tymchishin” at 260 and “Daniel after Deotte”
  at the other five (as T-248 and T-258 are credited), or whatever per-entry credit the
  register supports. The owner may prefer the union; the record should then say why.

**F14. The handle.** The key and the 175 claim name “Mishapolk”, the handle, where the
record’s credit name for Mykhailo Polkovskyi is “Polkovskyi” (`bibliography.yaml`
`credited_names`; T-186’s own key credits “Polkovskyi after Ostashev, Couzo, PingYou
Ltd, Levy”), and `attribution.md` lines 14–17 ask for the surname in a credit line.
The draft follows `n-175.md`, whose `improved_by` on `main` lists “Mishapolk”, so the
case record would need the same change.
The issue’s own “Mishapolk’s” may stay as its words.

**F15. Which confirmation.** When the replay and this review are registered:

- the lane’s replay of both packets is re-implemented, sharing named components with the
  producer (`shared-components`: the `evand-cert` reader’s line filter and corner
  construction), as T-248’s and T-257’s replays are recorded;
- this review’s run is independently re-implemented, clean room, full coverage of the
  thirteen files, by a Claude agent, a system family the producer also used.

The draft entries’ notes and the report evidence’s limitations (`evidence.yaml:56623`
and following) say what the two routes share with each other, but not what they share
with the producer; T-248’s entry says both.
The result’s level is then independently re-implemented.

## Questions for the Author

1. At 260 the issue says the certificate dilates the f64 packing by
   $8.8 \cdot 10^{-12}$. Measured, it dilates `s260_ks_1105.input.txt` by the factor
   $1 + 10^{-12}$ (its side $1.66 \times 10^{-11}$ above the input’s), and
   $8.8 \times 10^{-12}$ is its side’s excess over the pre-descent input’s. Which did
   you mean?
2. At 260 is the exact side the header’s
   $8316760475444266760475435949833/(5 \cdot 10^{29})$, with $16.633520950888535$ its
   binary64 print?
3. At 260 your island matches #845’s after a half turn about the box centre and a shift
   of one unit upward. Is that how the composer placed it?
4. Would you name the composer and Chris Deotte’s method in `CREDITS.md` or a README, so
   the credit is in your repository’s own attribution files as well as in the issue?
5. The issue was edited at 21:18:34Z after it was opened.
   Did the edit change a claim, a digest or a credit?

## What I Ran

All runs used CPython 3.14.7 (`packing/.venv/bin/python3 -I`) under `nice -n 19`, at
most two processes, on a shared four-core host.
The receipts are in `out/`; `out/program-digests.txt` records the SHA-256 of every
program as the final run read it, and `programs/run_all.sh` reruns everything.

| Program | Receipt | CPU |
| --- | --- | ---: |
| `self_test.py` | `self-test.json`: passed | 10.4 s |
| `decide_feasibility.py`, both senses | `feasibility/*.json`: 13 accepted; `reversed-sense/*.json`: 13 refused | 107.9 s, 106.8 s |
| `sharp_controls.py` | `controls/*.json`: 182 as stated | 142.5 s |
| `sides_and_kkt.py` | `sides-and-kkt.json` | 0.6 s |
| `house_slack.py` | `slack-and-contacts.json` | 3.6 s |
| `scale_slack.py` (after the freeze) | `scale-slack.json` | 3.8 s |
| `identity.py` | `identity.json` | 5.8 s |
| `island_260.py` | `island-260.json` | 3.0 s |
| `tilts.py` | `tilts.json` | 1.2 s |
| `input_260.py` | `input-260.json` | 0.2 s |
| `custody.py` | `custody.json`: custody holds | 0.04 s |

The final run took 388.6 CPU-seconds.
With the development runs, among them two kept control runs, the review used about 0.30
CPU-hours, within the brief’s 0.1 to 0.3; the upstream fetch used the network, not the
CPU.

What went wrong along the way, and was redone:

- G2, the outside control, first moved square 1 left by 1 and was redefined (see
  [Sharp Controls](#sharp-controls)). That run is kept.
- C3’s “past” expectation first counted a parallel axis as a second axis.
  That run is kept.
- One measurement, the 260 input’s overlaps against its pre-descent side, first ran as
  an inline script; it is now `input_260.py`, and its receipt is that program’s.

## Verdict

**Accepted at all seven counts, at 260 with findings.** Each certificate proves
$s(n) \le S$ at its header side exactly.

- Every hypothesis holds exactly, for the certificates and for the views at their
  certificates’ sides.
- Every wall and every pair is decided by two methods that agree everywhere.
- Every control is decided as stated beforehand.

No defect of a certificate or its mathematics is open.
F3 is for the author, and the record repeats it; F13 is a correction for this
repository’s records; the rest are notes.

Mapped as an adversarial review with verdict `accepted` on each of the seven entries, it
supports V3 and C3 at each, provided this review’s run is registered as exact-algebraic
evidence replayed here with full coverage of the thirteen files.
That reads as confirmed, independently re-implemented, clean room, by a Claude agent, a
system family the producer also used.
V4 and C4 would need a second accepted adversarial review by a distinct reviewer and a
human oversight record.
The significance S3 is confirmed at all seven.

## Comparison With the Lane’s Receipts and the Earlier Reviews

Everything above, except what is marked as added after the freeze, follows findings that
were frozen before I opened the lane’s receipts, its measurements, its ledger, the
packet READMEs or any of the three earlier reviews.
Its findings F1 to F12 are this document’s F1 to F12, the wording tightened; F9’s
side-slack figure and F13 to F15 were added after the freeze.

**The lane’s receipts.**

- `receipts/exact-certification.json.xz` in both packets gives each route’s least pair
  gap and least containment clearance for every positive.
  All 26 pairs of values equal this review’s as exact fractions.
- `receipts/sharp-controls-nNNN.json` chooses the same pairs and squares where both
  look: at 260 it closes pair 244 against 98 and lowers the side by the clearance of
  square 258, the same exact fractions as here.
  It moves every square to the near wall where this review translates the packing, and
  its enlargements are against the pair and the wall; this review adds the reversed
  sense and the all-upright control.
- `measure/identity-nNNN.json` gives the same counts in every row of the identity table:
  60, 66, 42, 80, 193, 124 and 66 beyond 0.1, 33 against T-257 at 260, the same largest
  moves and tilt counts, the inputs’ largest moves ($2.28 \times 10^{-11}$ at 260, at
  most $1.42 \times 10^{-4}$ elsewhere) and the views’ 3 to 8. Nothing differs.
- The ledger records all seven as new packings, three of them continuing an earlier
  arrangement (175, 204, 260), which F8 and F11 measure.

**The 31 October review of T-257.**

- Its least clearances for T-257’s 260, $6.010 \times 10^{-13}$ and
  $1.2016 \times 10^{-12}$, equal this review’s measurement of the same file.
- It found T-257’s 293 to be its 260 plus one L-shaped strip, which the draft’s “his 260
  with one L-shaped strip” repeats; here T-257’s 293 is the house at 293, and the new
  293 pairs with it under no symmetry.
- Its N-8 (the rotation sense is fixed only through $(c, s)$) is hypothesis 6 here, and
  its reversed-sense control is this review’s.
- Its M-1, one name for the 260 start’s finder, is honoured in the new key
  (“Tymchishin”).
- Its reading of T-257’s 260 certificate as a $1 + 10^{-12}$ dilation of a binary64
  packing is the reading F3 asks the record to give this 260 as well.

**The 4 November review of #893 and #894.** Its F6 (which confirmation each route is) is
the shape of F15 here, with the producer relation through the `evand-cert` reader
instead of `packing-witness verify`. Its reading of T-264 as a further arrangement of
T-257’s packing is this review’s calibration.

**The 5 November review of #895.** This document takes its format.

- Its slack measure (T-257’s 260 at $1.9988 \times 10^{-11}$ of side; #895’s at 0, row
  253 at the right wall) is reproduced exactly by `scale_slack.py`, which was written
  after the freeze from its description and gives F9 its side-slack figures.
- Its rule that “refinement” means no square beyond a tenth, and its reading of T-265 as
  a further arrangement, S2, against the S3 of new arrangements “that no symmetry pairs
  one to one with the house’s packing”, are the rule F7, F8 and F12 apply.
- Its F10 asked for one name for the 260 start’s finder; the new key writes Tymchishin.

Nothing in the lane’s receipts or the earlier reviews changes a verdict or the
significance.

## Frozen Findings

The findings were frozen at 22:48:14Z on 5 November 2026, before the lane’s receipts,
measurements and ledger, the packet READMEs or any of the three earlier reviews were
opened.
The frozen text, `frozen-findings.md`, is 222 lines and 15,512 bytes with a final
newline. It lists the per-count verdicts, F1 to F12, five questions, the cost and what
was seen first. Its SHA-256 is
`b699af79aaf21ead643f17187e8c4a7673a3594001e0ffdc012221a39f169f32`, and it is kept
beside the programs.
It names the entries by their draft ids, which this document does not use.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
