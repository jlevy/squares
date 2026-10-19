# Review: Evan Daniel’s Upper-Bound Imports of 16 to 18 October (#659, #664, #669, #674)

**Date:** 19 October 2026. **Verdict: accepted, for finite feasibility only.** The five
rational certificates that five register entries cite prove the upper bounds those
entries state: #669’s s(155) (T-197), #674’s opening and updated s(229) (T-198 and
T-199), and #659’s s(236) and #664’s s(271), which the records lane has registered on
its branch as T-218 and T-219. Those two numbers are assigned in merge order and may
change, so this review names those entries by issue and count as well.
Every retained receipt job reproduces here job for job on both maintained routes; a
third exact route written for this review and the repository’s clipping-area route each
decide all five certificates again, with six controls each at their required outcome;
and every file of every pinned scope was fetched again at its pin and found at the
digest its packet records.
The two dilation certificates at 229 are exactly what their headers state, and each
least margin splits exactly into the binary64 input’s own clearance, the dilation’s
share and the rounding’s. The credit each entry states was measured pose by pose: the
155 and the 236 are new arrangements, the 271 continues Francisco Couzo’s #561
arrangement with three squares moved beyond a tenth, and the 229 update is a nearby
arrangement of the opening; no entry is a refinement in the record’s sense, and none
lists one.
Ten findings are recorded, none blocking and one major: no test holds the five
packets’ controls (RV-1). Every entry can take `V3`/`C3` with its confirming evidence
entry and this review, in the pull request that closes RV-1. The houses should then move
at four counts: to T-197 at 155, to T-199 at 229, to #659’s entry at 236 and to #664’s
at 271; T-198 stays as history ([Adoption per Count](#adoption-per-count)). None can
take `V4`/`C4` from this review alone.

This is the stage 4 review lane (W2) of the 19 October intake
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)), for
bead `think-s5u5`, written by an AI agent (Claude, strong sub-agent tier, max reasoning)
prompted separately from the import and records lanes, with no shared context beyond
their committed packets, register entries and branch.
Its relation to the results is `project`. It moves no rung, writes no register row and
changes no case record; it says what the records lane should write.

## For the Author

Evan Daniel: each of your five certificates (#669’s `s155_ex2.cert`, #674’s `s229.cert`
and `s229_v2.cert`, #659’s `s236_bm3c.cert` and #664’s `s271_ex1.cert`) was decided
again here from the bytes this repository keeps.
This repository’s two maintained exact routes decided each again and agreed with the
import lane’s receipts job for job; a third exact route written for this review and the
repository’s clipping-area route each decided all five, with controls.
Each file was fetched again at its commit and found unchanged, at the digest your issue
prints. Every one is accepted as a finite upper bound at its exact side.
Nothing here bears on optimality, local minimality or rigidity: your 80-digit KKT,
second-order and MILP checks stay yours, as you present them.

- **#669, s(155).** Measured square by square, the packing is not Daniil Ostashev’s #501
  packing refined: no symmetry of the box pairs the two one to one by nearest centres,
  and the best one-to-one assignment moves 29 squares by more than a tenth, at most
  0.737, your figure. Its tilts, 22.3° to 25.0° with one at 7.8° and four at 33.6° to
  34.8°, share none of #501’s, 25.0° to 32.7°. This review recommends recording it as
  your new arrangement, found from Ostashev’s packing, with the credit you asked for.
- **#674, s(229).** Both certificates are exactly what their first lines say.
  Each side is the binary64 input’s side times 1 + δ, rounded up at 30 places, where δ
  is the double nearest $10^{-12}$, $2.0 \times 10^{-29}$ below it; every centre and
  every tangent is as `dilate_cert.py` makes it.
  The margins split exactly.
  The opening’s input clears its walls by $1.0 \times 10^{-15}$ and overlaps one pair by
  $3.4 \times 10^{-16}$, which the dilation’s $5 \times 10^{-13}$ and $10^{-12}$ absorb.
  The update’s input already clears every wall by $1.005 \times 10^{-13}$ and every pair
  by $2.02 \times 10^{-13}$, which is why its margins are $6.0 \times 10^{-13}$ and
  $1.2 \times 10^{-12}$ and not the dilation’s alone.
  The update pairs with the opening square for square, eight squares moving more than a
  tenth (at most 0.54), with the same four tilt bands.
  Neither pairs one to one with Joost de Winter’s #668 packing, though both carry its
  bands to within 0.03°. Francisco Couzo’s #672, which you name as the start, is not yet
  retained here, so the step from it is not measured.
- **#659, s(236).** Another arrangement of itsnaka’s #481 design.
  Against the regularized view of #481’s packing that the case now holds, the best
  one-to-one assignment moves 10 squares by more than a tenth (at most 0.747, your
  figure) and keeps 226 within a tenth; the main tilt band moves from 38.09° to
  37.69°–37.79°. This review recommends recording it as your packing, with itsnaka’s
  composition credited for the construction, as you asked.
- **#664, s(271).** Couzo’s #561 arrangement with three squares moved by more than a
  tenth (at most 0.197) and one tilt group a square short: 268 of 271 squares lie within
  a tenth of #561’s under the identity, and every tilt group matches within 0.12°, as
  you say. This record keeps the word refinement for a pairing in which no square moves
  more than a tenth, so this review recommends recording the packing as your
  continuation of Couzo’s arrangement, which refines SQUISH’s #500, with the credit you
  asked for.

Three questions:

1. The three regularized-view reports (`s155_ex2_regularized.json`,
   `s236_bm3c_regularized.json` and `s271_ex1_regularized.json`) each say
   `"by": ["Francisco Couzo"]`. Is that a default of the regularizer, or does it credit
   Couzo with something in those views?
2. The update’s binary64 input, `s229_v2.input.txt`, already clears its walls by about
   $1.0 \times 10^{-13}$ and its pairs by about $2.0 \times 10^{-13}$, while the
   opening’s touches to within $10^{-15}$. Was it solved at a slightly larger side, or
   loosened on purpose?
   A tight input would have given a side about $3 \times 10^{-12}$ smaller; nothing here
   depends on it.
3. Is the 229 packing a point `exactsolve.py` can certify at $1 + 10^{-20}$, as for the
   other three? That would lower the 229 bound by about $1.6 \times 10^{-11}$.

## Claims Covered

| Entry | Issue and pin in `evand/square-packing` | n | Certificate kept |
| --- | --- | --- | --- |
| T-197 | #669, `59326b8` | 155 | `s155_ex2.cert`, retained under MIT, with the same-side `s155_ex2_regularized.cert` |
| T-198 | #674, opening post, `e0338c7` | 229 | `s229.cert`, retained, with its binary64 input `s229.input.txt` |
| T-199 | #674, comment of 18 October, `00e68df` | 229 | `s229_v2.cert`, retained, with `s229_v2.input.txt` |
| T-218 on the records branch (#659) | #659, `5ad0069` | 236 | `s236_bm3c.cert`, retained, with its KKT point and same-side regularized view |
| T-219 on the records branch (#664) | #664, `757b40b` | 271 | `s271_ex1.cert`, retained, likewise |

Each entry’s claim states its side exactly, as its certificate’s header does:

| Entry | n | Exact side | Issue prints | Rounded up at 16 places |
| --- | --- | --- | --- | --- |
| T-197 | 155 | 2590452188930112807053435932173/200000000000000000000000000000 = 12.952260944650564035267179660865 | 12.952260944651 | 12.9522609446505641 |
| T-198 | 229 | 7825081627429265081627421439843/500000000000000000000000000000 = 15.650163254858530163254842879686 | 15.650163254859 | 15.6501632548585302 |
| T-199 | 229 | 7825080756947776580756939951343/500000000000000000000000000000 = 15.650161513895553161513879902686 | 15.650161513896 | 15.6501615138955532 |
| #659 | 236 | 15.861934390607358617243798571394 | 15.861934390608 | 15.8619343906073587 |
| #664 | 271 | 16.948947733713657510723401112423 | 16.948947733714 | 16.9489477337136576 |

The third route held each claim to its certificate, exactly, and each issue’s print to
the side rounded up at twelve places, which is what each issue says it prints.
The packets’ other files are not claims.
The three regularized views state the same packings at the same sides for display, and
are decided here too ([The Third Route](#the-third-route)); the KKT points and binary64
inputs are what the certificates were made from; the solver, prior-record and comparison
reports are the source’s numerical statements, read here as data.

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) in a worktree at
`d7413ccdb`, the head of `claude/intake-2026-10-19-evand-singles`, niced, one process of
this review at a time under a lock file, on a four-core host that other lanes shared at
a load average of 15 to 30. At `d7413ccdb` the code differs from `main` (`14fd9e27f`)
only by the five `HOUSES` readers the lane added to `devtools/upper_bound_reports.py`;
the replay path, the kernel of `devtools.evand_arrangement_reports` and both routes are
`main`’s.

From 21:16:12Z to 21:17:43Z on 19 October, for each packet:
`acquire_source PACKET --check` reported `PACKET_MATCHES_ITS_CONTRACT`;
`upper_bound_reports PACKET check-claims` rebuilt the frozen claim record equal, 5.3 to
26.5 seconds each; and `check` admitted the receipt, one certificate and three jobs
each. Then each command `python -m devtools.upper_bound_reports PACKET check --replay`
decided every retained job again through both routes, in process, and compared every
field with its retained row except the two times (`stable_row`); an unequal row stops
the run.

| Packet | Entry | Receipt: jobs, pair decisions, route CPU s, job wall s | Replay here | Wall here |
| --- | --- | --- | --- | --- |
| `evand-n155-explorer-2026-10-17` | T-197 | 3, 71,610, 43.29, 86.75 | every job equal, exit 0 | 193 s, 21:17:43Z to 21:20:56Z |
| `evand-n229-dilation-2026-10-17` | T-198 | 3, 156,636, 92.75, 140.22 | every job equal, exit 0 | 425 s, 21:20:56Z to 21:28:01Z |
| `evand-n229-dilation-update-2026-10-18` | T-199 | 3, 156,636, 88.93, 157.25 | every job equal, exit 0 | 228 s, 21:28:02Z to 21:31:50Z |
| `evand-n236-2026-10-16` | #659 | 3, 166,380, 70.45, 104.20 | every job equal, exit 0 | 249 s, 21:31:50Z to 21:35:59Z |
| `evand-n271-2026-10-17` | #664 | 3, 219,510, 103.33, 119.55 | every job equal, exit 0 | 375 s, 21:41:38Z to 21:47:53Z |

The 15 jobs, 770,772 pair decisions and 398.75 route CPU seconds of the five receipts
were all decided again, 1,470 seconds of wall in all, and every row is equal to its
retained row. Each positive passes both routes, and both routes refuse each
duplicate-square control (squares 0 and 1 overlap) and each outside-container control
(square 0 moved by S + 2), with the failures the receipts record.
Both routes state the same margins for each positive, the least wall clearance and the
least separating-axis gap over pairs: $1/(2 \cdot 10^{20})$ exactly and
$1.0000 \times 10^{-20}$ at 155, 236 and 271; $5.0100 \times 10^{-13}$ and
$9.9966 \times 10^{-13}$ for the opening 229; $6.0050 \times 10^{-13}$ and
$1.2021 \times 10^{-12}$ for the update.

## The Third Route

### This review’s route

`third_route_1019.py`, written for this review and kept in the n155 packet’s
[`review/review-2026-10-19/`](../../../packing/resources/web/evand-n155-explorer-2026-10-17/review/review-2026-10-19/README.md),
decides each certificate from its retained bytes.
It uses the standard library only, imports nothing from this repository, and reads the
literals with a reader of its own.
For every square it holds the half-angle map to the unit circle and the placed square to
four edges of squared length 1 at right angles, turning counter-clockwise, with area 1;
every corner must lie in the closed box.
Pairs whose centres are 2 or more apart are decided by their circumscribed discs.
Every closer pair is decided on the closed squares by exact orientation tests: an edge
of one meeting an edge of the other, or a corner of one in the other.
Where the closed squares are disjoint, the route records their exact squared Euclidean
distance, the least corner-to-edge one, a rational since every edge has length 1; where
they meet, the route decides the interiors by the Minkowski difference, the exact convex
hull of the sixteen corner differences, whose interior holds the origin exactly when the
interiors meet.

| Command | Outcome | Wall |
| --- | --- | --- |
| `python -I third_route_1019.py --json OUT --upstream SCRATCH` | 5 certificates passed, 128,462 pairs (4,145 decided and measured exactly), 30 of 30 controls at their required outcome, no disagreement, exit 0 | 339 s, 21:35:59Z to 21:41:38Z |

Per certificate: least wall clearance; least Euclidean distance between squares; pairs
decided (measured exactly); seconds for the positive and its six controls.

| Entry | n: wall; distance; pairs (measured); time |
| --- | --- |
| T-197 | 155: $1/(2 \cdot 10^{20})$ exactly; $1.0000 \times 10^{-20}$; 11,935 (575); 59 s |
| T-198 | 229: $5.0100 \times 10^{-13}$; $9.9966 \times 10^{-13}$; 26,106 (851); 88 s |
| T-199 | 229: $6.0050 \times 10^{-13}$; $1.2021 \times 10^{-12}$; 26,106 (850); 66 s |
| #659 | 236: $1/(2 \cdot 10^{20})$ exactly; $1.0000 \times 10^{-20}$; 27,730 (851); 48 s |
| #664 | 271: $1/(2 \cdot 10^{20})$ exactly; $1.0000 \times 10^{-20}$; 36,585 (1,018); 77 s |

Every positive passes, all 30 controls reach their required outcome, and the route
disagrees with nothing.
Every side, centre and tangent equals the positive job’s input in the packet’s receipt;
every least wall clearance equals both maintained routes’ exactly; every least distance
is at least their separating-axis gap, and equal to it at ten digits, each closest pair
being separated along a face normal of one of its squares.
Every side is the side its entry’s claim states, exactly, and rounds up at twelve places
to its issue’s print.
Each retained certificate is byte for byte the file `custody.py` fetched at its pin.

The six controls are the precedent’s
([16 October review](review-2026-10-16-upper-bound-imports-506-607.md#the-third-route)):
square 1 replaced by square 0 and square 0 moved by S + 2 (refused); the side at
far-wall contact (accepted, the box being closed) and $10^{-40}$ past it (refused); and
the closest pair, its second square translated by the exact difference of the closest
points into contact (that pair, decided alone, a contact by the Minkowski difference)
and then $10^{-30}$ of the centre difference further (the certificate refused, that pair
overlapping). No certificate here touches a wall or has two squares in contact, so every
contact control starts from a positive clearance.

### The registered clipping-area route

`area_route_1019.py` runs `devtools.check_half_angle_area` (`V-check-half-angle-area`),
unchanged since `e1fc548d9`, on the five certificates: its own reader, half-extent
containment, the disc rule at centre distance $\sqrt 2$, and for every closer pair the
exact area of one square clipped by the other’s closed half-planes, with its least
distance and its six controls (`verdict`). Its tables name none of these packets; the
driver adds nothing to them and changes no decision.
All five passed, 2,552 pairs clipped, all 30 controls at their required outcome, with
the same least wall clearances, least distances and closest pairs as the third route; 93
s, 21:47:58Z to 21:49:31Z.

### The regularized views

`views_1019.py` decides the source’s three same-side views (`s155_ex2_regularized.cert`,
`s236_bm3c_regularized.cert` and `s271_ex1_regularized.cert`) on the third route,
without controls. All three pass at their certificates’ exact sides, with least wall
clearance $5 \times 10^{-21}$ and least distance $10^{-20}$; 41 s, 21:51:00Z to
21:51:41Z. T-197 lists its view among its artifacts.
No maintained route has replayed any of the three, and the bound needs none of them.

## From Certificate to Bound

The argument is the one the
[#528/#529 review](review-2026-10-12-upper-bound-imports-528-529.md#from-certificate-to-bound)
and the 16 October review give.
Each certificate is a text file: comment lines beginning with `#`, a header `n S`, and
then exactly n rows `x y t` of rational literals.
Row k places the closed unit square

$$
Q_k = (x_k, y_k) + R_k\,[-\tfrac12, \tfrac12]^2,\qquad
R_k = \begin{pmatrix} c_k & -s_k \\ s_k & c_k \end{pmatrix},\qquad
(c_k, s_k) = \Bigl(\frac{1 - t_k^2}{1 + t_k^2}, \frac{2t_k}{1 + t_k^2}\Bigr).
$$

1. **Unit size.** For rational $t$, $c$ and $s$ are rational and
   $c^2 + s^2 = (1 + t^2)^2/(1 + t^2)^2 = 1$ identically, so $R_k$ is the rotation by
   $2 \arctan t_k$ and $Q_k$ is a unit square with rational corners.
   Nothing is approximated: the tangent is the certificate’s, and the square it gives is
   exactly unit, whatever angle the producer meant.
2. **Containment.** The box $[0, S]^2$ is convex, so $Q_k$ lies in it iff its four
   corners do, equivalently iff $h_k \le x_k \le S - h_k$ and $h_k \le y_k \le S - h_k$
   with $h_k = (|c_k| + |s_k|)/2$.
3. **Disjoint interiors.** For $j \ne k$, the interiors of $Q_j$ and $Q_k$ are disjoint,
   decided pair by pair by a theorem about two convex polygons: the separating-axis
   theorem (both maintained routes and the source’s `verify_cert.py`); closed polygons
   are disjoint iff no corner of one lies in the other and no edges meet (this review’s
   route and the source’s `verify_cert2.py`), and interiors are disjoint iff the origin
   is not interior to $Q_j - Q_k$ (this review’s route, for meeting pairs); interiors
   are disjoint iff the intersection has zero area (the area route).
   Pairs far apart are decided by circumscribed discs, or, on the maintained routes, by
   the same test as every other pair.
4. **The bound.** n unit squares with pairwise disjoint interiors in the closed square
   of side S give $s(n) \le S$, by the definition of $s(n)$ as the least side of a
   square holding n non-overlapping unit squares, rotations allowed.

Every route decides in exact rational arithmetic and none rounds, dilates or tolerates.
How a certificate was made enters no decision.
The 155, 236 and 271 certificates are the source’s 80-digit KKT points scaled by
$1 + 10^{-20}$ about the origin corner, as `search/exact/README.md` describes.
Each side is $\lceil S^* (1 + 10^{-20}) \cdot 10^{30} \rceil / 10^{30}$ for the retained
70-digit KKT side $S^*$, and every centre but one of the 236’s is the KKT centre scaled
and rounded at 35 places; the one differs by $10^{-35}$, plausibly because the point is
printed at 70 digits and the certificate was made from the solver’s 80. So the least
wall clearance is exactly $5 \times 10^{-21}$, at a square upright against a wall, and
the least pair gap about $10^{-20}$. The 229 certificates are dilations of binary64
packings ([The Dilation Certificates at 229](#the-dilation-certificates-at-229)). No
certificate touches a wall or has two squares in contact; the bound needs only the
closed box.

**The exact side and its prints.** S is the header’s fraction.
Each claim states it exactly: T-197, T-198 and T-199 as the fraction, #659’s and #664’s
entries as the terminating decimal it equals.
Each issue prints $\lceil S \cdot 10^{12} \rceil/10^{12}$, the register’s tables print
$\lceil S \cdot 10^{16} \rceil/10^{16}$, and the third route checked both exactly.
No print is a bound the certificate does not prove.

**What every checker assumes.** That the file’s literals mean the rationals they write,
read without floating point; that the format means what its comment line, the source’s
`search/exact/README.md` and both of its checkers say: a centre (not a corner), the
lower-left origin, and $t$ the tangent of half the rotation; that Python’s integers and
`fractions.Fraction` compute exactly; and the plane-geometry lemma its pair test rests
on, with the disc rule.
Each lemma above is standard and each route applies it to closed convex quadrilaterals
given exactly. Nothing else is assumed: no tolerance, no rounding of a decision, and no
fact about the producer’s search or solver.

## The Dilation Certificates at 229

`dilation_1019.py` re-derives each 229 certificate from its retained binary64 input by
the construction the retained `search/packer/dilate_cert.py` documents, written again
from that description; the source program did not run.
Read as data, `dilate_cert.py` line 23 sets the factor `f = 1 + Fr(a.delta)` from the
float `1e-12`, so the factor is $1 + \delta$ with $\delta = 4951760157141521/2^{92}$,
the double nearest $10^{-12}$ and $2.01 \times 10^{-29}$ below it; line 36 rounds the
side up at 30 places, line 35 rounds each centre to the nearest $10^{-30}$, and line 34
takes each tangent as the best rational with denominator at most $10^{15}$ to the double
$\tan(\theta/2)$.

|  | Opening, `s229.cert` | Update, `s229_v2.cert` |
| --- | --- | --- |
| Input side S | 15.65016325484288 | 15.650161513879903 |
| Side is $\lceil S(1 + \delta) \cdot 10^{30}\rceil/10^{30}$ | yes, exactly; rounded up by $7.8 \times 10^{-31}$ | yes, exactly; rounded up by $7.8 \times 10^{-31}$ |
| With $\delta = 10^{-12}$ exactly instead | $3.14 \times 10^{-28}$ larger | $3.14 \times 10^{-28}$ larger |
| Centres as the construction makes them | 229 of 229, each rounded by at most $5.0 \times 10^{-31}$ | 229 of 229, at most $5.0 \times 10^{-31}$ |
| Tangents as the construction makes them, recomputed on this host | 229 of 229 | 229 of 229 |
| Least wall clearance (squares counted from 0) | $5.0100 \times 10^{-13}$, square 8 at x = 0 | $6.0050 \times 10^{-13}$, square 64 at x = S |
| = input’s own + dilation’s + rounding’s | $1.000 \times 10^{-15} + 5.000 \times 10^{-13} + 5.7 \times 10^{-32}$ | $1.005 \times 10^{-13} + 5.000 \times 10^{-13} + 1.1 \times 10^{-30}$ |
| Least separating-axis gap | $9.9966 \times 10^{-13}$, squares 193 and 199 | $1.2021 \times 10^{-12}$, squares 13 and 86 |
| = input’s own + dilation’s + rounding’s | $-3.38 \times 10^{-16} + 1.000 \times 10^{-12} + 1.1 \times 10^{-31}$ | $2.021 \times 10^{-13} + 1.000 \times 10^{-12} + 1.1 \times 10^{-31}$ |
| Least input clearance, wall; pair | $1.0 \times 10^{-15}$; $-3.38 \times 10^{-16}$ | $1.005 \times 10^{-13}$; $2.021 \times 10^{-13}$ |

Both sides are exactly what the header’s `delta 1e-12` gives, and the margins are what a
dilation predicts. Scaling the centres and the box by $f$ about the origin adds $\delta$
times the centre’s distance from a wall to that wall’s clearance, and $\delta$ times the
centre distance along a separating axis to a pair’s gap there.
A square on a wall has its centre at least $\tfrac12$ from it, and two squares in
contact along a face normal have centres at least 1 apart along it, so a tight input
gives margins of about $\delta/2$ and $\delta$. Each identity in the table holds
exactly, measured with the certificate’s rotations at the input’s centres and side, so
that only the scaling and the rounding of centres and side differ between the two.
The least margins sit at an upright square half a unit from its wall and a face-to-face
pair one unit apart, with levers 1/2 and 1. The opening’s input clears its walls by
$10^{-15}$ and overlaps one pair by $3.4 \times 10^{-16}$, which the dilation absorbs,
as `dilate_cert.py`’s docstring says it absorbs binary64 overlaps up to about
$\delta/4$. The update’s input overlaps nothing and already clears every wall by
$1.005 \times 10^{-13}$ and every pair by $2.02 \times 10^{-13}$, so a sixth of the
update’s reported margins ($6.0 \times 10^{-13}$ and $1.2 \times 10^{-12}$ in #674’s
comment) is the input’s own slack (RV-5). Both receipts’ margins are these exactly, on
both routes.

## Custody

All five pinned scopes were fetched over HTTPS on 19 October between 21:20:28Z and
21:20:38Z, as one blobless Git clone of `evand/square-packing` read at each pin, into
scratch space outside the repository, and read as data.
Each pin is an ancestor of the source’s default branch, whose head was `3a9948c`; each
pinned commit’s tree is the `git_tree` its packet’s acquisition record states, and its
committer date is the record’s `committed_utc`. All 74 manifest lines (2,382,324 bytes)
have their pinned SHA-256. All 15 `pinned_only` entries have their digest and byte
count, and the six that name an identical copy in another packet (the update’s two
opening files, and the 236 and 271 packets’ four copies of the checkers) equal it byte
for byte. The 59 retained files (842,821 bytes) are byte for byte their upstream blobs,
`s236_bm3c_vs_prior.json.gz` after decompression.
Each certificate the claims rest on, and each file beside it whose digest its issue
prints (the three views and the two 229 inputs), has that digest.
On the default branch each of those ten paths is touched by one commit, its pin, and the
head still holds the pinned blob, so no later commit changes a certificate.

## Trust Boundaries

| Route | Decides | Shares with the others |
| --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, every pair by exact separating axes | the importer’s `evand-cert` adapter, the parse and half-angle map of `devtools.evand_exact_certificates`; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same on rational corners | the same adapter, parse and map; `Fraction`; the separating-axis method |
| this review’s route (`third_route_1019.py`, kept, cited by nothing) | unit circle and unit square; corners in the closed box; far pairs by discs; near pairs on the closed squares with exact distance, meeting pairs by the Minkowski difference | `Fraction` and the format’s meaning; its near-pair test is the method of the source’s `verify_cert2.py` |
| the area route (V-check-half-angle-area, driven here) | unit circle, half-extent containment, discs, exact clipped area | `Fraction` and the format’s meaning |

No source program ran.
The source reports that its two standard-library checkers accept each certificate:
`verify_cert.py` (separating axes over the four face normals, strict inequalities, a
disc shortcut at $|\Delta c|^2 > 2$) and `verify_cert2.py` (every corner strictly inside
the box; no corner of one square in the other and no meeting edges, over closed squares,
with the same shortcut).
Both read the first n rows and ignore any others.
This review read them as data, after its route was written and run.
The n155 packet and both 229 packets retain them; the 236 and 271 packets pin them by
digest as byte-identical copies.

Three methods decide here.
The maintained routes repeat the method of the source’s first checker, in code of their
own.
This review’s route decides near pairs by the method of the source’s second checker;
its author had read the n155 packet README’s one-sentence description of that method,
and the docstring of `devtools.check_half_angle_area`, before writing it.
It imports nothing from either and adds what `verify_cert2.py` lacks: an exact distance
for every near pair, a decision for squares that touch (`verify_cert2.py` refuses
contact, which the closed problem allows), and controls.
So it is an independent implementation of the producer’s second method, not a method
beside it.
The area route is the one decision here whose pair test neither the source nor
the maintained routes use.
`devtools.evand_exact_certificates`, whose parse and half-angle map both maintained
routes take, was written after its author read `verify_cert.py` and `verify_cert2.py`
(its `verifiers.yaml` note), as the 16 October review recorded.

What every route shares: Python’s integer arithmetic and `fractions.Fraction`, the
CPython 3.14.7 build that ran them, and the format’s reading.
An error common to the format’s meaning would pass all of them; the format is stated
three times in the source and every route reads it the same way.
The review lane, the import lane, the maintained routes, the area route and the source’s
assistant are one AI system family.
Each packet’s `CREDITS.md` says the source’s work was produced by Claude (Anthropic)
under human direction, and each pinned commit names Claude as co-author (two with a
Claude Code session link) and says Evan Daniel approved the commit and its post or
comment; the issues themselves do not say.

## Credit and Lineage

`lineage_1019.py` measures each certificate against the packings its entry names,
through the readers of `devtools.check_half_angle_area`, after each packet’s custody.
`arrangement_gap` pairs each square with the nearest centre of the other packing under
the box symmetry whose one-to-one matching moves its farthest square least; `unmoved`
finds the symmetry that keeps the most squares in place.
An optimal assignment, the matching of least total squared displacement under each
symmetry (`scipy`, in binary64), is how the source compares.
Each tilt is the square’s angle folded into [0°, 45°], which no symmetry changes.
None of these decides anything.
The record’s sense of a refinement is a one-to-one pairing in which no square moves
beyond a tenth (T-150, T-152).

| Certificate | Against | Nearest-centre pairing | Best assignment: moved beyond $10^{-3}$ / $10^{-2}$ / $10^{-1}$; largest | What it says |
| --- | --- | --- | --- | --- |
| #669 155 | T-149, Ostashev (#501) | none one to one; at most 125 within 0.1 | identity: 73 / 61 / 29; 0.737, a turn of 41.7° | a new arrangement, not #501’s refined |
| #669 155 | T-174, the house (#501’s packing as PingYou refined it) | none; at most 125 within 0.1 | identity: 71 / 61 / 29; 0.737 | the same |
| #674 update 229 | #674 opening (T-198) | one to one, identity: 94 / 23 / 8; 0.538 | identity: 94 / 23 / 8; 0.538, a turn of 26.1° | a nearby arrangement, the same four tilt bands |
| #674 opening 229 | T-196, de Winter (#668) | none; at most 24 within 0.1 | a reflection: 154 / 83 / 77; 0.807 | de Winter’s tilt bands within 0.03°, placed otherwise |
| #674 update 229 | T-196, de Winter (#668) | none; at most 27 within 0.1 | a reflection: 170 / 88 / 79; 0.873 | the same |
| #659 236 | T-136, SQUISH (#481) | none; at most 179 within 0.1 | a reflection: 236 / 57 / 10; 0.745 | another arrangement of #481’s design |
| #659 236 | T-146, the house (Daniel’s regularized view of #481’s packing); T-174 | none; at most 226 within 0.1 | a reflection: 235 / 51 / 10; 0.747 | the same; 226 squares within a tenth |
| #664 271 | T-186, the house; T-161, Couzo (#561); T-174 | one to one, identity: 34 / 4 / 3; 0.197 | identity: 34 / 4 / 3; 0.197, a turn of 31.7° | #561’s arrangement continued, three squares beyond a tenth |
| #664 271 | T-151, SQUISH (#500) | one to one, a quarter turn: 75 / 35 / 3; 0.197 | the same | the same, through #561 |

At 236 every square moves more than $10^{-3}$ under the best assignment because the two
boxes differ by $2.02 \times 10^{-3}$ and the reflection maps one corner to another; the
counts at a tenth are the ones that bear on credit.
T-186 and T-174 at 271 are certificate refinements of T-161’s packing that move no
square beyond $10^{-3}$, and T-174 at 155 and 236 refines T-149’s and T-146’s packings
(`regularizations` of T-174 and T-186), so the rows against them agree, but for the few
squares T-174’s refinement moved at 155.

The tilts say the same as the poses:

| n | This certificate’s tilted squares, folded | The packing it is measured against |
| --- | --- | --- |
| 155 | 22.30° ×10, 23.04° to 23.43° ×35, 23.66°, 24.86° ×2, 24.97° ×3, 33.64° ×2, 34.77° ×2, 7.78°, and three within 0.7° of upright | T-149: 25.01° to 32.73°, 45 squares, and one at 0.33° |
| 229 | update: 25.87° to 25.97° ×24, 26.05° ×18, 26.16° ×3, 27.42° to 27.46° ×15, and 35 within 0.06° of upright; opening: the same bands (24, 19, 3, 15), single squares at 25.71°, 15.07° and 0.53°, and 37 within 0.16° of upright | T-196: 25.87° to 25.99° ×25, 26.05° ×19, 26.16° ×3, 27.42° to 27.44° ×17, 24.19° |
| 236 | 37.69° to 37.79° ×32, 35.55° to 35.61° ×4, 43.87° ×2, 44.03°, 44.25°, and seven near upright | T-136: 38.09° ×19, 37.41° to 37.42° ×4, 37.84° ×3, 44.68° ×8, 43.39° to 43.43° ×3, and singles; T-146: 38.09° ×28, 43.39° to 43.43° ×4, 44.68° ×8 |
| 271 | above 1°, 69 squares in 19 groups, each within 0.12° of one of T-161’s (at most 0.112°), with 31.71°, 31.90° and 31.98° where T-161 has 31.65° to 31.69° ×3 and 31.97°; two near upright | T-161: above 1°, 70 squares in the same groups; two near upright |

So the measurements bear out each issue’s description, in the record’s terms.
#669’s 155 is a new arrangement found from Ostashev’s packing, as the issue says (“Not a
refinement of the T-149 packing: no load-bearing tilt angle is shared”). #659’s 236 is
another arrangement of #481’s composition, which the issue asks to credit for the
construction; ten squares move beyond a tenth and the main band turns by 0.35°. #664’s
271 is Couzo’s #561 arrangement with three squares moved beyond a tenth, which the issue
calls a refinement of #561’s packing and a different local minimum; in the record’s
sense it is a continuation, as T-188’s 211 was (RT-1 of the 16 October review), and
T-219 lists no `regularizations`, rightly (RV-2). #674’s update is the opening’s
arrangement with eight squares moved beyond a tenth, and neither entry lists a
regularization, rightly.
Both carry de Winter’s four tilt bands, but neither pairs with his #668 packing; Couzo’s
#672, which the issue names as the start and says refines #668, is in no packet yet
(think-2vjc), so the step from it is not measured (RV-9). The source’s own matchings,
over its regularized views, print the same largest moves at 155 and 236 (0.737 and
0.747). At 271 the source prints 0.391 where the certificates measure 0.197 here; the
views and the matching differ, and nothing here turns on it.

## Findings

Graded blocking, major, minor or note, each with the file and line it concerns.
None is blocking; one is major.

**RV-1, major: no test holds the five packets’ controls.**
`packing/tests/test_upper_bound_reports.py` lines 100 to 127 list in `EVERY` each packet
whose receipt `test_the_receipt_admits_every_job_on_both_routes` admits, and whose
register plan the plan test reads; none of the five packets is there, and no per-import
test file names them (`git grep` over `packing/tests`, `packing/devtools` and
`packing/src` finds them only in `devtools/upper_bound_reports.py`). Yet
`packing/frontier/results.yaml` lines 29406 and 29473 cite that file as the `controls`
of #659’s and #664’s entries.
Stage 4 asks that “two mutated certificates are refused by every checker that accepted
the original, and a test holds them”
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)). The
controls ran and were refused, in the receipts and again here, but no test keeps them
refused. The records lane should add the five packets to `EVERY`, with their
`attribution.published` dates in the plan test’s table, and should write a test file for
what is particular to them, as `test_upper_bound_reports_606_70a033f.py` does for #606:
the 229 sides as the dilations of their inputs, the 155, 236 and 271 sides as their KKT
points at $1 + 10^{-20}$, each certificate below every report at its count, and the
`HOUSES` readers rebuilding the sides.
T-197, T-198 and T-199 then cite the same file as `controls`.

**RV-2, minor: T-219’s headline calls the 271 a refinement of Couzo’s packing.**
`packing/frontier/results.yaml` line 29428 (“Daniel’s smaller n271 packing, refining
Couzo’s packing”) and the credit sentence at lines 29444 to 29447 (“Francisco Couzo’s
#561 packing and Nate Chaoweeraprasit’s SQUISH packing (#500) it refines”) use the word
in the record’s voice.
By pose three squares move beyond a tenth, at most 0.197, against T-161, T-186 and T-174
and, under a quarter turn, against T-151 ([Credit and Lineage](#credit-and-lineage)). As
RT-1 of the 16 October review did for T-188, the headline should say “continuing Couzo’s
arrangement”, the claim should keep “the source calls it a refinement of #561’s packing”
in the source’s voice, as line 29437 already does, and the notes should state the
measurement, citing this review; the credit is the same either way, Daniel after Couzo
after Chaoweeraprasit.

**RV-3, minor: T-199’s claim credits “Daniel after Couzo, de Winter and Levy”.**
`packing/frontier/results.yaml` line 27402 (claim) and line 27435 (notes), and
`packing/frontier/evidence.yaml` line 37948, copy the bibliography’s `credit` string,
where “Levy” stands for this project’s lineage (`builds-on-project`, the convention at
the head of `packing/resources/bibliography.yaml`). In a claim’s credit sentence it
reads as a person in the packing’s lineage; T-198’s claim, of the same packing family,
does not say it, and #674 asks for credit to Couzo’s #672 packing, which refines de
Winter’s #668. The sentence should read “Credit Evan Daniel after Francisco Couzo’s #672
packing, which refines Joost de Winter’s #668, as the issue asks”, leaving the project’s
lineage to the bibliography.

**RV-4, note: the dilation’s δ is the double nearest $10^{-12}$, not $10^{-12}$.**
`search/packer/dilate_cert.py` line 23 (`f = 1 + Fr(a.delta)`, `a.delta` a float) and
#674 (“scaled by $1 + 10^{-12}$”). The factor is $1 + 4951760157141521/2^{92}$,
$2.01 \times 10^{-29}$ below $1 + 10^{-12}$; each side is the ceiling of the input’s
side times it at 30 places, and with the exact power it would be $3.14 \times 10^{-28}$
larger. The bound is the certificate’s side whatever made it, so nothing changes; the
packets already say “approximately”, and the record should keep saying so.

**RV-5, note: the update packet attributes its clearances to the dilation alone.**
`packing/resources/web/evand-n229-dilation-update-2026-10-18/README.md` line 131: “The
clearances are the dilation’s $10^{-12}$ margin, as the source describes it.”
For the update, $6.005 \times 10^{-13}$ is the input’s $1.005 \times 10^{-13}$ plus the
dilation’s $5 \times 10^{-13}$, and $1.2021 \times 10^{-12}$ is the input’s
$2.021 \times 10^{-13}$ plus $10^{-12}$
([The Dilation Certificates at 229](#the-dilation-certificates-at-229)). The opening
packet’s same sentence, line 128, is right.
The line could say so, citing this review.

**RV-6, minor: this review’s decisions are kept but cited by nothing.** As RT-8 of the
16 October review found for its own, the third route, the area route and the view
decisions are kept in the n155 packet’s
[`review/review-2026-10-19/`](../../../packing/resources/web/evand-n155-explorer-2026-10-17/review/review-2026-10-19/README.md),
with every log and report they wrote, but no evidence entry cites them, and
`third_route_1019.py` is in no `verifiers.yaml` entry.
The confirming evidence rests on the maintained replay, which needs nothing more.
The records lane can make the area route’s decision citable by adding the five packets’
keys and rosters to `devtools.check_half_angle_area` with tests, as the 14 October
roster was, and running it with `--receipts`; until then the confirming evidence should
not list V-check-half-angle-area.

**RV-7, note: T-197 reads the view’s `by` field as a conflict.**
`packing/frontier/results.yaml` lines 27273 to 27275 and its notes: the regularized JSON
“instead says by Francisco Couzo”.
The 236 and 271 views’ reports say the same, and their packets read the field as the
regularizer’s default (n236 README line 54, n271 README line 54). The three should read
alike; question 1 under [For the Author](#for-the-author) asks the source.

**RV-8, note: the 229 dilation certificates carry about $1.6 \times 10^{-11}$ of
guard.** Each 229 side exceeds its input’s by $S\delta = 1.565 \times 10^{-11}$, and the
update’s input carries another $2 \times 10^{-13}$ of slack between squares, about
$3 \times 10^{-12}$ of side.
Neither is a defect, since a dilation certificate is valid at any factor above 1, but a
certificate of the same packing at $1 + 10^{-20}$, as the other three are made, would
state a smaller bound; question 3 asks it.

**RV-9, note: neither 229 is de Winter’s packing by pose.** Against de Winter’s #668
(T-196), the only antecedent the record retains, no symmetry pairs either 229 one to one
by nearest centres, and the best assignment moves 77 and 79 squares beyond a tenth,
while the four tilt bands agree within 0.03°. That bears out #674’s “the tilted
structure is the same … the upright part is rearranged” as to angles, and says the
placement moved too.
The credit chain the entries preserve (de Winter, then Couzo’s #672, then Daniel) stays
the sources’; the record cannot measure the step from #672 until its intake retains it
(think-2vjc).

**RV-10, note: a re-housed count owes its regularization runs.**
[The House Rule](../../../packing/campaign/result-import.md#the-house-rule) makes the
pull request that adopts a house run both strong generators on each count it re-houses,
here 155, 229, 236 and 271. The source’s own same-side views (17, 6 and 21 angle groups
at 155, 236 and 271), valid here, are display views at the house’s side, not candidates
below it; whether one is admitted as a drawing is the regularization policy’s question.

## Rungs

**`V3`/`C3` for all five entries.** Machine-replayed here: every certificate the entries
cite and its two kernel controls on both maintained routes, with certificates, replay
commands, passing replays and the retained receipts; reviewed adversarially here.
Beside the rung, by the kept programs that no evidence entry cites (RV-6): every
certificate with six controls on this review’s route and on the area route, the views on
this review’s route, and each retained file held to its upstream bytes.
`V` is the strongest verification anywhere, the record’s replay being `V3`’s predicate
for exact-algebraic evidence of any origin.
`C3` needs the named control that a test holds (RV-1): the rungs move in the pull
request that closes it.
Not `V4`/`C4`: one AI review, no human oversight record.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

| Entry | Verdict | Blocking findings | Confirming evidence entry to write | Adoption |
| --- | --- | --- | --- | --- |
| T-197 (#669) | accepted; `V3`/`C3` supported | no | `E-evand-669-n155-exact-feasibility` | the house at 155 |
| T-198 (#674 opening) | accepted; `V3`/`C3` supported | no | `E-evand-674-n229-opening-exact-feasibility` | none: T-199 is smaller; kept as history |
| T-199 (#674 update) | accepted; `V3`/`C3` supported | no | `E-evand-674-n229-update-exact-feasibility` | the house at 229 |
| #659 (T-218 on the records branch) | accepted; `V3`/`C3` supported | no | `E-evand-659-n236-exact-feasibility` | the house at 236 |
| #664 (T-219 on the records branch) | accepted; `V3`/`C3` supported | no | `E-evand-664-n271-exact-feasibility` | the house at 271 |

**Verdict lines for the records lane.** For each entry, a confirming evidence entry as
tabled, modelled on `E-evand-606-n146-exact-feasibility`: `assurance: verified`,
`method: exact-algebraic`, `performed_by: repository`, `origin: replayed-here`,
`relationship_to_generator: independent-implementation`, the packet’s certificate, the
`check --replay` command, `replay_status: passed`, the verifiers V-sqpack-verify,
V-check-rational-witness-independent, V-evand-arrangement-receipts,
V-upper-bound-reports and V-evand-exact-certificates (and V-check-half-angle-area only
once RV-6’s roster lands), an `independence` record and this review as
`independence_record` and `external_review` (`informally-verified`). Each `independence`
record has `coverage: full`, one certificate of one;
`read: [specification, certificate-format]`; `clean_room: false`; `shares: []`; and an
`overlaps_producer` of `extent: system-family`, `separate_prompt: true` and
`separate_code: true`, whose note names what each packet’s `CREDITS.md` and pinned
commit state (the work produced by Claude under Evan Daniel’s direction, each commit
co-authored by Claude and approved by him) and that V-evand-exact-certificates’ author
read the source’s checkers.
On each reported entry, `external_review` naming this review; on each register entry,
the evidence, the rungs, a `reviews` item (`kind: adversarial`, `reviewer_kind: ai`,
`relation: project`, `verdict: accepted`), `controls` naming the test RV-1 adds to, and
claim, notes and `next_rung` rewritten together, the `unfinished_confirmations` that
`think-s5u5`, `think-8kx2` and `think-0lu6` name removed.

## Significance

| Entry | Draft | Here | Why |
| --- | --- | --- | --- |
| T-197 (#669) | `S2` | `S3` | a new arrangement at 155, $1.64 \times 10^{-4}$ below the case and every report, found from Ostashev’s packing, as T-149 ($7.35 \times 10^{-5}$ below the pending T-128), T-160 and T-183 are |
| T-198 (#674 opening) | `S2` | `S2` | an arrangement of de Winter’s tilted design $1.15 \times 10^{-5}$ below the smallest earlier report, de Winter’s T-196, superseded the next day, as T-188 ($9.29 \times 10^{-6}$) is; the $6.69 \times 10^{-3}$ drop below the case is de Winter’s |
| T-199 (#674 update) | `S2` | `S2` | the same, $1.32 \times 10^{-5}$ below T-196 and $1.74 \times 10^{-6}$ below T-198 |
| #659 (T-218) | `S2` | `S3` | another arrangement of #481’s design $2.02 \times 10^{-3}$ below the case, as T-160’s $5.04 \times 10^{-4}$ at 154 and T-183’s $2.45 \times 10^{-4}$ at 237 are |
| #664 (T-219) | `S2` | `S3` | a continuation of #561’s arrangement to a new local minimum $4.46 \times 10^{-5}$ below the case, as T-119’s $3.3 \times 10^{-5}$ new arrangements and T-130’s refinements from $3.03 \times 10^{-5}$ are, and T-172’s $6.66 \times 10^{-5}$; above T-188’s $9.29 \times 10^{-6}$ (`S2`). The nearest call of the five |

`by` should name this review.

## Adoption per Count

Each comparison exact, sides rounded up at sixteen places, from each packet’s frozen
claim record, which `check-claims` rebuilt equal here, with each case’s ceiling read
from its case record on the branch at `d7413ccdb` (`adoption_1019.py`). Each recommended
house is the smallest exact certificate at its count among the reviewed entries,
replayed on both maintained routes and on two more here with no blocking defect, and
below the case. No other report at these counts is smaller.
Mykhailo Polkovskyi’s #593 states certificates at 155, 236 and 271 equal to the cases’
sides at sixteen places, and the open issues through #686 add only de Winter’s #668
(T-196) and Couzo’s #672 at 229, both above T-199. The intake audit of 18 October notes
that Couzo’s #675 index includes Daniel’s 229 itself, not a smaller side.

| n | Case ceiling, house | Reviewed and pending certificates, smallest first | House |
| --- | --- | --- | --- |
| 155 | 12.9524254069584562, T-174 | T-197 12.9522609446505641, below the case by $1.645 \times 10^{-4}$; T-149 equal to the case at 16 places | T-197, Daniel (a new arrangement found from Ostashev’s packing) |
| 229 | 15.6568542494923802, T-155 (the catalogue’s $10 + 4\sqrt2$) | T-199 15.6501615138955532, below the case by $6.693 \times 10^{-3}$; T-198 15.6501632548585302, $1.741 \times 10^{-6}$ above T-199; Couzo’s #672, print 15.650174740273; T-196, de Winter, 15.6501747569482132, $1.324 \times 10^{-5}$ above T-199 | T-199, Daniel after Couzo after de Winter (the sources’ chain, RV-9) |
| 236 | 15.8639557471592675, T-146 | #659 15.8619343906073587, below the case by $2.021 \times 10^{-3}$; T-174 equal to the case at 16 places; T-136 15.8639557471592678 | #659’s entry, Daniel after Chaoweeraprasit (itsnaka)’s #481 composition |
| 271 | 16.9489923564512057, T-186 | #664 16.9489477337136576, below the case by $4.462 \times 10^{-5}$; T-161 and T-174 equal to the case at 16 places; T-151 16.9491166878150100 | #664’s entry, Daniel after Couzo after Chaoweeraprasit (RV-2) |

T-198 is recorded and superseded, kept as history.
The earlier houses stay retained as history, and the reported and verified ceilings move
together. `devtools.select_houses` takes each house once its entry is a candidate:
`V3`/`C3` with an accepted review covering it and a confirming evidence entry whose
scope reaches the count.
No entry here lists a `regularizations` item, so each house credits its entry, as the
House column does. The witnesses these houses replace are 306 KB (155), 33 KB (229), 58
KB (236) and 211 KB (271) on the branch; the new certificates are 26 KB to 43 KB as
text, so the houses change little in size; the records lane measures it with
`python -m devtools.upper_bound_houses sizes`.

## Proposed Record Changes

For the records lane; this review writes none of them.

- The confirming evidence and register fields under [Rungs](#rungs), for all five, in
  the pull request that adds the five packets to the tests (RV-1).
- Claims, notes and `next_rung`: RV-2’s headline and measurement on #664’s entry; RV-3’s
  credit sentence on T-199; RV-7’s reading of the views’ `by` field on T-197; the credit
  measurements of [Credit and Lineage](#credit-and-lineage) on all five, with this
  review as `measured_in`; RV-5’s sentence in the update packet’s README.
- Significance as tabled, `by` naming this review.
- Houses at the four counts of [Adoption per Count](#adoption-per-count), with the
  regularization runs each re-housed count owes (RV-10).
- The area route’s roster and receipts, if the record is to cite it (RV-6).
- For the author, in the replies drafted at stage 7: the questions under
  [For the Author](#for-the-author).

## Programs Run Here

The programs this review wrote are kept, with their logs and reports, in the n155
packet’s
[`review/review-2026-10-19/`](../../../packing/resources/web/evand-n155-explorer-2026-10-17/review/review-2026-10-19/README.md),
whose README says how to run each one, what it read and what it printed.
They run only this repository’s maintained tools and code written for this review, read
the sources as data, and write nothing in the repository outside that directory.

- **`custody.py`** made one blobless clone of the source over HTTPS and held the trees,
  the manifests, the `pinned_only` entries, the retained files and the issue-printed
  digests to the packets’ acquisition records.
- **`third_route_1019.py`** is this review’s exact route, and **`views_1019.py`** runs
  it on the three views.
- **`area_route_1019.py`** runs `devtools.check_half_angle_area`’s `verdict` on the five
  certificates.
- **`dilation_1019.py`** re-derives the 229 certificates from their inputs and splits
  their margins, and holds the other three to their KKT points.
- **`lineage_1019.py`** makes the measurements of
  [Credit and Lineage](#credit-and-lineage); **`adoption_1019.py`** the comparisons of
  [Adoption per Count](#adoption-per-count); **`receipt_totals_1019.py`** sums the
  receipts.
- **`run_serial.sh`**, **`chain_replay.sh`**, **`chain_review.sh`** and
  **`chain_review2.sh`** ran each heavy command niced under one lock file and logged its
  UTC start, end, wall and exit status.

Two runs stopped on errors in this review’s own report code before writing anything, and
were fixed and run again: `dilation_1019.py` on an empty minimum, and `lineage_1019.py`
on a reader that named T-186 by an entry its module does not map.
Both first logs are kept.

## Earlier Reviews That Touch These Results

Before its findings were written, this review had seen, of the earlier documents that
touch these results, only the names of `review-2026-10-18-intake-audit.md` and
`review-2026-10-18-open-work.md` and a count of the lines in each that name these issues
or entries; it read them afterwards.
Both are coordination audits of the 18 October intake, not mathematical reviews.
They report two stage 4 results that no document on this branch holds:

- “Astra’s independent #669/#674 mathematics review”, which “accepted four certificates
  and all 76,082 pairs”, with 40 control outcomes agreeing in ordinary and optimized
  Python, found no blocking defect, and recorded a Low limitation of the source’s
  checkers: “completeness guards based on `assert` disappear under optimized Python”.
  Its four certificates are #669’s two and #674’s two (2 × 11,935 + 2 × 26,106 pairs is
  76,082). This review agrees on every certificate both decided: #669’s certificate and
  view and #674’s two certificates pass here too.
  It did not record the limitation.
  The guards are asserts, as that review says: `verify_cert.py` lines 31 and 37 and
  `verify_cert2.py` line 49 hold the row count and the unit circle by `assert`, which
  `python -O` removes.
  By this review’s reading, a file with fewer than n rows would then fail on an index
  error in each checker’s pair loop, at `verify_cert.py` line 49 and `verify_cert2.py`
  line 57, and still exit non-zero, except that `verify_cert2.py` would accept a header
  `1 S` with no row at all, its pair loop being empty; and the unit circle holds for
  every rational t. So the limitation is real at that one degenerate input and changes
  elsewhere only how a short file is refused.
  It touches no certificate here, each of which has exactly n rows, as every route here
  enforces. The review’s document is not on this branch and was not read.
- “A separate normal source-checker replay of those four certificates”, the source’s own
  two checkers run on them, “eight accepted decisions and 16 geometric mutant refusals
  in 41.386 seconds”, whose sealed receipt (SHA-256 `cab73c96…`) belongs to `think-8kx2`
  and `think-0lu6`, the beads the entries’ notes name as awaiting integration.
  Run as the source published them, that replay is reproduced with the producer’s code
  (`same-implementation`); the rungs here rest on the maintained routes’ replay,
  independently re-implemented after their authors read the producer’s checkers, and the
  records lane may record the source replay beside them when its receipt lands.
  This review neither read nor used it.

Both audits also record, from the other side, two things measured here: at 155, that the
issue and `s155_ex2_prior.json` credit Ostashev while the view’s report says
`by: ["Francisco Couzo"]` (RV-7); and at 229, that no `regularizations.of` is assigned
“because Couzo’s antecedent is not registered”.
The measurement here gives a second reason: neither 229 is a refinement of de Winter’s
registered packing by pose (RV-9).

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty or priority; no run of any
source’s checker, solver, regularizer or search; no decision of the KKT points, the
binary64 inputs or the source’s numerical reports; no measurement against Couzo’s #672;
no evidence entry for the kept third-route, area-route and view decisions (RV-6); no
house adoption or case-record change.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
