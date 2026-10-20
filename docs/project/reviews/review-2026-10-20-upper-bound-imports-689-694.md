# Review: Evan Daniel’s Upper-Bound Imports of 19 and 20 October (#689, #694)

**Date:** 20 October 2026. **Verdict: accepted, for finite feasibility only.** The two
rational certificates that two register entries cite prove the upper bounds those
entries state: #689’s s(308) ≤ 17.997149121270908735153160752315 and #694’s s(154) ≤
12.921100940761680549856582087576, which the records lane has registered on its branch
(PR #699) as T-221 and T-222. Those numbers are assigned in merge order and may change,
so this review names the entries by issue and count as well.
Each retained receipt reproduces here job for job on both maintained routes; a third
exact route written for this review and the repository’s clipping-area route each decide
both certificates again, with six controls each at their required outcome; and every
file of both pinned scopes was fetched again at its pin and found at the digest its
packet records.
Each certificate is exactly what the source’s construction describes: its
80-digit KKT point scaled by $1 + 10^{-20}$, with every centre and tangent as that
construction makes them, so its least wall clearance is exactly $5 \times 10^{-21}$ and
its least pair gap $10^{-20}$ along a face normal.
The credit each entry states was measured pose by pose: the 308 is another arrangement
of the two-wedge design the case’s house holds, 293 of 308 squares within a tenth of the
house’s packing under a quarter turn and 15 moved beyond it, found, by the source’s
account, from Chaoweeraprasit’s 307; the 154 is Couzo’s #586 arrangement with three
squares moved beyond a tenth, the record’s continuation.
Neither is a refinement in the record’s sense, and neither entry lists one.
Six findings are recorded, none blocking and none major.
Both entries can take `V3`/`C3` with a confirming evidence entry and this review, and
both draft `S3` scores stand.
The houses should then move at both counts: to #689’s entry at 308 and to #694’s at 154
([Adoption per Count](#adoption-per-count)). Neither can take `V4`/`C4` from this review
alone.

This is the stage 4 review lane (W2) of the 20 October intake
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)), for
the import beads `think-h8jm` (#689) and `think-115j` (#694), written by an AI agent
(Claude, strong sub-agent tier, max reasoning) prompted separately from the import and
records lanes, with no shared context beyond their committed packets, register entries
and branch. Its relation to the results is `project`. It moves no rung, writes no
register row and changes no case record; it says what the records lane should write.

## For the Author

Evan Daniel: each of your two certificates (#689’s `s308_d308.cert` and #694’s
`s154_sw.cert`) was decided again here from the bytes this repository keeps.
This repository’s two maintained exact routes decided each again and agreed with the
import lane’s receipts job for job; a third exact route written for this review and the
repository’s clipping-area route each decided both, with controls.
Each file was fetched again at its commit and found unchanged, at the digest your issue
prints. Both are accepted as finite upper bounds at their exact sides.
Nothing here bears on optimality, local minimality or rigidity: your 80-digit KKT,
second-order and MILP statements stay yours, as you present them, including #694’s
inconclusive second-order status.

- **#689, s(308).** Measured square by square, the packing is another arrangement of the
  design #484 and #489 share, as your issue says (“the same family as #484 and #489
  (mirrored)”): under a quarter turn, the best one-to-one assignment against #489’s
  packing moves 15 squares by more than a tenth (at most 0.708, your 0.706) and keeps
  293 within a tenth, with 111 squares turned by more than 0.01°; against #484’s, 12
  squares beyond a tenth and 296 within.
  Your “not a refinement of #489” holds in the record’s sense, which keeps that word for
  a pairing in which no square moves more than a tenth.
  Chaoweeraprasit’s 307 packing, which you name as the ultimate start, lies within a
  tenth of this packing at 263 of its 307 squares under the identity.
  This review recommends recording the packing as your new arrangement of that design,
  found from #481’s 307 as you describe, with the credit you asked for.
- **#694, s(154).** Against #586’s packing (and Polkovskyi’s re-solve of it, the case’s
  house), the nearest-centre pairing is one to one under a quarter turn and moves three
  squares by more than a tenth (at most 0.204), 151 within; 32 squares turn by more than
  0.01°. Your band of ten at 26.5322° sits where #586 has eleven at 26.530°. In the
  record’s terms that is #586’s arrangement continued to a different KKT point, as
  #664’s 271 was recorded; this review recommends recording it so, with the credit you
  asked for. Ostashev’s 156 packing, which you name as the start, lies within a tenth of
  this packing at 94 of its 156 squares, so that credit rests on your account of the
  search, as the record states it.

Three questions:

1. The regularized view’s report says `"by": []` at 308 and `"by": ["Francisco Couzo"]`
   at 154, where the earlier views (155, 236, 271) all said Couzo.
   Is the name at 154 deliberate, crediting #586’s arrangement, and the empty field at
   308 the regularizer’s default now?
2. Each KKT file prints some rows at binary64 precision rather than 70 digits: 7 of 308
   (the five free squares 6, 56, 57, 85, 86 and squares 1 and 65) and 33 of 154 (the
   nine free squares and 24 others), three of each identical to the binary64 input’s
   row. Are the others the squares frozen in exact flat motions?
   Nothing here depends on it: the certificate reads every literal exactly, and the
   geometry is decided exactly whatever precision the solver carried for those squares.
3. At 154 the second-order test finds one negative-curvature direction blocked only to
   first order. Was a descent along it tried at second order, or is the status left open
   on purpose?

## Claims Covered

| Entry | Issue and pin in `evand/square-packing` | n | Certificate kept |
| --- | --- | --- | --- |
| T-221 on the records branch (#689) | #689, `bc0708f` | 308 | `s308_d308.cert`, retained under MIT, with its KKT point, binary64 input and same-side `s308_d308_regularized.cert` |
| T-222 on the records branch (#694) | #694, `1d2bb82` | 154 | `s154_sw.cert`, retained, likewise, with `s154_sw_regularized.cert` |

Each entry’s claim states its side exactly, as its certificate’s header does:

| Entry | n | Exact side | Issue prints | Rounded up at 16 places |
| --- | --- | --- | --- | --- |
| #689 | 308 | 3599429824254181747030632150463/200000000000000000000000000000 = 17.997149121270908735153160752315 | 17.997149121271 | 17.9971491212709088 |
| #694 | 154 | 1615137617595210068732072760947/125000000000000000000000000000 = 12.921100940761680549856582087576 | 12.921100940762 | 12.9211009407616806 |

`adoption_1020.py` held each claim to its certificate’s header exactly, each issue’s
print to the side rounded up at twelve places, and each packet’s `ceiling` to the side
rounded up at sixteen.
The packets’ other files are not claims.
The two regularized views state the same packings at the same sides for display, and are
decided here too ([The Regularized Views](#the-regularized-views)); the KKT points and
binary64 inputs are what the certificates were made from; the solver, prior-record and
comparison reports are the source’s numerical statements, read here as data.

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) in a worktree at
`34d72a95a`, the head of `claude/intake-2026-10-20-evand-308-154`, niced, one process of
this review at a time, on a four-core host that other lanes shared at a load average of
about 3. At `34d72a95a` the code differs from `main` (`d588ad987`) only by the two
`HOUSES` readers the lane added to `devtools/upper_bound_reports.py` and a release
module change; the replay path, the kernel of `devtools.evand_arrangement_reports` and
both routes are `main`’s.

From 18:51:53Z to 18:52:54Z on 20 October, for each packet:
`acquire_source PACKET --check` reported `PACKET_MATCHES_ITS_CONTRACT`;
`upper_bound_reports PACKET check-claims` rebuilt the frozen claim record equal; and
`check` admitted the receipt, one certificate and three jobs each.
Then each command `python -m devtools.upper_bound_reports PACKET check --replay` decided
every retained job again through both routes, in process, and compared every field with
its retained row except the two times; an unequal row stops the run.

| Packet | Entry | Receipt: jobs, pair decisions, route CPU s, job wall s, longest job s | Replay here | Wall here |
| --- | --- | --- | --- | --- |
| `evand-n308-2026-10-19` | #689 | 3, 283,668, 35.66, 36.22, 12.41 | every job equal, exit 0 | 45 s, 18:51:57Z to 18:52:42Z |
| `evand-n154-sweep-2026-10-20` | #694 | 3, 70,686, 8.90, 9.03, 3.14 | every job equal, exit 0 | 11 s, 18:52:43Z to 18:52:54Z |

The 6 jobs, 354,354 pair decisions and 44.56 route CPU seconds of the two receipts were
all decided again, 56 seconds of wall in all, and every row is equal to its retained row
(`receipt_totals_1020.py` sums them; a pair decision counts each pair once per route per
job, $2\binom{n}{2}$ a job, as the packets count).
Each positive passes both routes, and both routes refuse each duplicate-square control
(`exact_verify`: “squares 0 and 1 overlap”; `independent`: “1 overlapping pairs; worst
exact gap −1”) and each outside-container control (“square 0 violates x<=s”; “container
penetration”), with the failures the receipts record.
Both routes state the same margins for each positive, the least wall clearance and the
least separating-axis gap over pairs: $1/(2 \cdot 10^{20})$ exactly and
$1.0000 \times 10^{-20}$ at both counts.

The tests the branch adds hold the packets: `test_upper_bound_reports.py` lists both in
`EVERY`, so `test_the_receipt_admits_every_job_on_both_routes` admits each receipt with
its two refused controls, and `test_upper_bound_reports_689_694.py` holds each side to
its KKT point at $1 + 10^{-20}$, each certificate below its house and every report at
its count by the bracketed margin, and the replay’s margins.
The twelve tests selected by those names pass here, 3.5 seconds at 19:10:06Z.

## The Third Route

### This review’s route

`third_route_1020.py`, written for this review and kept in the n308 packet’s
[`review/review-2026-10-20/`](../../../packing/resources/web/evand-n308-2026-10-19/review/review-2026-10-20/README.md),
decides each certificate from its retained bytes.
It uses the standard library only, imports nothing from this repository, and reads the
literals with a reader of its own, refusing a file with other than n rows.
For every square it holds the half-angle map to the unit circle and the placed square to
four edges of squared length 1 at right angles, turning counter-clockwise, with area 1;
every corner must lie in the closed box.
Pairs whose centres are more than 2 apart are decided by their circumscribed discs.
Every closer pair is decided on the closed squares by exact orientation tests: a corner
of one in the other, or an edge of one meeting an edge of the other.
Where the closed squares are disjoint, the route records their exact squared Euclidean
distance, the least corner-to-edge one, a rational; where they meet, the route decides
the interiors by the Minkowski difference, the exact convex hull of the sixteen corner
differences, whose interior holds the origin exactly when the interiors meet.

| Command | Outcome | Wall |
| --- | --- | --- |
| `python -I third_route_1020.py --json OUT CERT CERT` | 2 certificates passed, 59,059 pairs (1,741 decided and measured exactly), 12 of 12 controls at their required outcome, no disagreement, exit 0 | 11 s, 19:02:57Z to 19:03:08Z |

Per certificate: least wall clearance and the square at it; least Euclidean distance
between squares and the pair; pairs decided (measured exactly); seconds for the positive
and its six controls.

| Entry | n: wall (square); distance (pair); pairs (measured); time |
| --- | --- |
| #689 | 308: $1/(2 \cdot 10^{20})$ exactly (square 0); $1.0000 \times 10^{-20}$ (23, 24); 47,278 (1,189); 7.3 s |
| #694 | 154: $1/(2 \cdot 10^{20})$ exactly (square 39); $1.0000 \times 10^{-20}$ (11, 12); 11,781 (552); 3.0 s |

Both positives pass, all 12 controls reach their required outcome, and the route
disagrees with nothing.
Every least wall clearance equals both maintained routes’ exactly; each least squared
distance equals the square of their separating-axis gap exactly, so each closest pair is
separated along a face normal of one of its squares, and the gap both maintained routes
state is the Euclidean distance.
Every side is the side its entry’s claim states, exactly, and rounds up at twelve places
to its issue’s print.
Each retained certificate is byte for byte the file `custody_1020.py` fetched at its
pin.

The six controls are the precedent’s
([19 October review](review-2026-10-19-upper-bound-imports-659-664-669-674.md#the-third-route)):
square 1 replaced by square 0 (refused, “squares 0 and 1 overlap”) and square 0 moved by
S + 2 (refused, “square 0 leaves the closed box”); the side lowered to the largest
corner coordinate, a far-wall contact (accepted, the box being closed, wall clearance 0)
and $10^{-40}$ below it (refused: square 74 leaves at 308, square 39 at 154); and the
closest pair, its second square translated by the exact difference of the closest points
into contact (that pair, decided alone, one contact by the Minkowski difference,
accepted) and then $10^{-30}$ of the centre difference further (the certificate refused,
that pair overlapping).
Neither certificate touches a wall or has two squares in contact, so every contact
control starts from a positive clearance.

### The registered clipping-area route

`area_route_1020.py` runs `devtools.check_half_angle_area` (`V-check-half-angle-area`)
on the two certificates: its own reader, half-extent containment, the disc rule at
centre distance $\sqrt 2$, and for every closer pair the exact area of one square
clipped by the other’s closed half-planes, with its least distance and its six controls
(`verdict`). Its tables name neither packet; the driver adds nothing to them and changes
no decision. Both passed, 716 and 358 pairs clipped, all 12 controls at their required
outcome, with the same least wall clearances, least distances and closest pairs as the
third route; 7 s, 19:09:42Z to 19:09:49Z.

### The regularized views

`construction_1020.py` decides the source’s two same-side views
(`s308_d308_regularized.cert` and `s154_sw_regularized.cert`) on the third route,
without controls.
Both pass at their certificates’ exact sides, with least wall clearance
$5 \times 10^{-21}$ and least distance $10^{-20}$ (closest pairs 114 and 115, and 11 and
12), with 29 and 10 distinct tangents, the angle groups the packets count; 3.0 s and 1.1
s. No maintained route has replayed either, and the bound needs neither.

## From Certificate to Bound

The argument is the one the
[19 October review](review-2026-10-19-upper-bound-imports-659-664-669-674.md#from-certificate-to-bound)
gives, after the #528/#529 and 16 October reviews, and is not repeated in full.
Each certificate is a text file: comment lines beginning with `#`, a header `n S`, and
then exactly n rows `x y t` of rational literals.
Row k places the closed unit square $Q_k = (x_k, y_k) + R_k[-\tfrac12, \tfrac12]^2$ with
$(c_k, s_k) = ((1 - t_k^2)/(1 + t_k^2),\ 2t_k/(1 + t_k^2))$, which lies on the unit
circle identically for rational $t$, so $Q_k$ is exactly unit whatever angle the
producer meant. The box $[0, S]^2$ is convex, so containment is containment of the four
corners. Disjoint interiors are decided pair by pair by a theorem about two convex
polygons: separating axes (both maintained routes and the source’s `verify_cert.py`);
closed polygons meet iff a corner of one lies in the other or two edges meet, and
interiors meet iff the origin is interior to $Q_j - Q_k$ (this review’s route; the
closed test is the method of the source’s `verify_cert2.py`); zero clipped area (the
area route).
n unit squares with pairwise disjoint interiors in the closed square of side
S give $s(n) \le S$ by the definition of $s(n)$.

Every route decides in exact rational arithmetic and none rounds, dilates or tolerates.
How a certificate was made enters no decision.
The source’s own checkers test the open box with strict inequalities; the closed box is
what the bound needs, and a certificate the open test accepts the closed one accepts.

**What every checker assumes.** That the file’s literals mean the rationals they write,
read without floating point; that the format means what its comment line, the source’s
`search/exact/README.md` and both of its checkers say: a centre (not a corner), the
lower-left origin, and $t$ the tangent of half the rotation; that Python’s integers and
`fractions.Fraction` compute exactly; and the plane-geometry lemma its pair test rests
on, with the disc rule.
Nothing else is assumed: no tolerance, no rounding of a decision, and no fact about the
producer’s search or solver.

## How Each Certificate Was Made

`construction_1020.py` holds each certificate to the construction the source’s
`search/exact/README.md` describes (read as data): the exact KKT configuration scaled
about the origin corner by $1 + \varepsilon$, $\varepsilon = 10^{-20}$, centres rounded
to $10^{-35}$, rotations as rational $t = \tan(\theta/2)$, and $S' = S^*(1 +
\varepsilon)$ rounded up.
It reads the retained `NAME.exact.txt` (`n S*`, then `x y theta_deg` per square, 70
digits).

|  | #689, `s308_d308.cert` | #694, `s154_sw.cert` |
| --- | --- | --- |
| KKT side $S^*$ (70 digits, first 30) | 17.997149121270908734973189261102 | 12.921100940761680549727371078168 |
| Side is $\lceil S^*(1 + 10^{-20}) \cdot 10^{30} \rceil / 10^{30}$ | yes, exactly; rounded up by $2.2 \times 10^{-32}$ | yes, exactly; rounded up by $2.0 \times 10^{-32}$ |
| Centres as the construction makes them | 308 of 308 within $5.0 \times 10^{-36}$ of the scaled KKT centre (the nearest $10^{-35}$) | 154 of 154, likewise |
| Tangents as $\tan(\theta/2)$ of the KKT angle, at 60 digits | 308 of 308 within $10^{-35}$ (largest difference $4.8 \times 10^{-36}$) | 154 of 154 (largest $4.2 \times 10^{-36}$) |
| Upright squares, $t = 0$ | 206 | 112 |
| KKT rows printed at binary64 precision | 7 (the 5 free squares and squares 1 and 65); 3 equal the input’s row | 33 (the 9 free squares and 24 others); 3 equal the input’s row |

So each side exceeds its KKT side by $S^* \cdot 10^{-20}$ plus the rounding, about
$1.8 \times 10^{-19}$ and $1.3 \times 10^{-19}$; the least wall clearance is exactly
$\varepsilon/2$ at an upright square against a wall, as scaling a square with its centre
half a unit from the wall predicts; and the least pair gap is $\varepsilon$ times the
centre distance along a face normal, one unit for a face-to-face pair, which is what
both certificates measure.
The 308’s KKT file prints the upright square 0’s angle as $-3.0 \times 10^{-80}$
degrees, which rounds to $t = 0$. The tangents are rounded at 35 places, which the
README does not say and which the measurement shows.
The binary64 rows (question 2) change nothing about the bound: every literal is read
exactly and every decision is exact.

## Custody

Both pinned scopes were fetched over HTTPS on 20 October at 18:51:59Z, as one blobless
Git clone of `evand/square-packing` whose head was `1d2bb82`, read at each pin into
scratch space outside the repository, as data, and checked from 19:03:08Z to 19:03:23Z.
Each pin is an ancestor of the default branch’s head, and the 154 pin is that head; each
pinned commit’s tree is the `git_tree` its packet’s acquisition record states
(`e5c826d…`, `0eeb614…`), and its committer date is the record’s `committed_utc`
(2026-10-19T22:41:02Z, 2026-10-20T03:54:48Z). All 41 manifest lines (906,877 and 766,052
bytes) have their pinned SHA-256. All 15 `pinned_only` entries have their digest and
byte count, and the eight that name an identical copy in the n183 packet (the two
checkers, the solver and the explorer, twice) equal it byte for byte.
The 26 retained files (309,168 and 164,990 bytes) are byte for byte their upstream
blobs, `s308_d308_vs_prior.json.gz` after decompression.
Each certificate the claims rest on, and each view beside it, has the digest its issue
prints.
On the default branch each of those four paths is touched by one commit, its pin,
and the head still holds the pinned blob, so no later commit changes a certificate.
The 308 packet’s README is right that the two commits after its pin leave its files
unchanged.

## Trust Boundaries

| Route | Decides | Shares with the others |
| --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, every pair by exact separating axes | the importer’s `evand-cert` adapter, the parse and half-angle map of `devtools.evand_exact_certificates`; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same on rational corners | the same adapter, parse and map; `Fraction`; the separating-axis method |
| this review’s route (`third_route_1020.py`, kept, cited by nothing) | unit circle and unit square; corners in the closed box; far pairs by discs; near pairs on the closed squares with exact distance, meeting pairs by the Minkowski difference | `Fraction` and the format’s meaning; its near-pair test is the method of the source’s `verify_cert2.py` |
| the area route (V-check-half-angle-area, driven here) | unit circle, half-extent containment, discs, exact clipped area | `Fraction` and the format’s meaning |

No source program ran.
The source reports that its two standard-library checkers accept each certificate and
its view: `verify_cert.py` (separating axes over the four face normals, strict
inequalities, a disc shortcut at $|\Delta c|^2 > 2$) and `verify_cert2.py` (every corner
strictly inside the box; no corner of one square in the other and no meeting edges, over
closed squares, with the same shortcut).
Both read the first n rows and ignore any others.
Both packets pin them by digest as byte-identical copies of the n183 packet’s, which
this review read as data after its route was written and run; before writing it, its
author had read the 19 October review’s one-paragraph description of that review’s route
and the source README’s one-line description of each checker.
So this review’s near-pair test coincides with the method of the source’s second
checker, in code of its own, and adds what that checker lacks: an exact distance for
every near pair, a decision for squares that touch (`verify_cert2.py` refuses contact,
which the closed problem allows), the closed box, a refusal of a file with other than n
rows, and controls. It is an independent implementation of the producer’s second method,
not a method beside it.
The maintained routes repeat the method of the source’s first checker, in code of their
own. The area route is the one decision here whose pair test neither the source nor the
maintained routes use.

What every route shares: Python’s integer arithmetic and `fractions.Fraction`, the
CPython 3.14.7 build that ran them, and the format’s reading.
An error common to the format’s meaning would pass all of them; the format is stated
three times in the source and every route reads it the same way.
The review lane, the import lane, the maintained routes, the area route and the source’s
assistant are one AI system family.
Each packet’s `CREDITS.md` says the source’s work was produced by Claude (Anthropic)
under human direction, and each pinned commit names Claude as co-author and says Evan
Daniel approved the commit and its post; the issues themselves do not say.

## Credit and Lineage

`lineage_1020.py` measures each certificate against the packings its entry names,
through the readers of `devtools.check_half_angle_area`, after each packet’s custody.
`arrangement_gap` pairs each square with the nearest centre of the other packing under
the box symmetry whose one-to-one matching moves its farthest square least; `unmoved`
finds the symmetry that keeps the most squares in place.
An optimal assignment, the matching of least total squared displacement under each
symmetry (`scipy`, in binary64), is how the source compares.
Each tilt is the square’s angle folded into [0°, 45°], which no symmetry changes.
Against a start at a neighbouring count the measurement is one-sided: each square of the
smaller packing to its nearest centre in the larger.
None of these decides anything.
The record’s sense of a refinement is a one-to-one pairing in which no square moves
beyond a tenth (T-150, T-152).

| Certificate | Against | Nearest-centre pairing | Best assignment: moved beyond $10^{-3}$ / $10^{-2}$ / $10^{-1}$; largest | What it says |
| --- | --- | --- | --- | --- |
| #689 308 | T-174, the house (PingYou’s refinement of #489’s packing) | one to one under a reflection: 301 / 69 / 15; 0.731 | a quarter turn: 300 / 60 / 13; 0.708, 295 within a tenth; 111 turned beyond 0.01°, at most 20.9° | another arrangement of the design, 13 to 15 squares beyond a tenth |
| #689 308 | T-141, Daniel (#489) | one to one under a reflection: 301 / 68 / 16; 0.731 | a quarter turn: 299 / 58 / 15; 0.708, 293 within a tenth; 111 turned | the same; the source’s 0.706 and “295 load-bearing beyond $10^{-4}$” (306 beyond $10^{-4}$ here, all squares counted) |
| #689 308 | T-135, Fang (#484) | one to one under a reflection: 302 / 71 / 16; 0.732 | a quarter turn: 298 / 54 / 12; 0.682, 296 within a tenth; 135 turned | the same design, #484’s packing being a binary64 one with 144 squares within 0.1° of upright |
| #689 308 | T-136 at 307, Chaoweeraprasit (#481), the start the issue names | one-sided, identity: 263 of 307 within a tenth, 11 within $10^{-2}$; largest 0.749 | 307 into 308, identity: 296 / 44 beyond $10^{-2}$ / $10^{-1}$; 0.749 | the same design one square short, as the issue’s history says |
| #694 154 | T-186, the house (Polkovskyi’s re-solve of #586’s packing); T-182, Couzo (#586) | one to one under a quarter turn: 90 / 51 / 3; 0.204 | a quarter turn: 90 / 51 / 3; 0.204, 151 within a tenth; 32 turned beyond 0.01°, at most 38.1° | #586’s arrangement continued, three squares beyond a tenth |
| #694 154 | T-172, Couzo (#583) | one to one under a quarter turn: 135 / 47 / 20; 0.290 | the same: 134 within a tenth | further from #583 than from #586, as the chain #552 → #583 → #586 runs |
| #694 154 | T-160, Daniel (#552) | one to one, identity: 132 / 45 / 20; 0.290 | the same: 134 within a tenth | the same |
| #694 154 | T-149 at 156, Ostashev (#501), the start the issue names | one-sided, identity: 94 of 156 within a tenth, 18 within $10^{-2}$; largest 0.835 | 154 into 156, identity: 136 / 60 beyond $10^{-2}$ / $10^{-1}$; 0.864 | a different design by pose; the start is the source’s account of the search |

T-186 at 154 is Polkovskyi’s certificate refinement of T-182’s packing, which moves no
square beyond $10^{-3}$, and T-174 at 308 refines T-141’s, so each pair of rows agrees.

The tilts say the same as the poses:

| n | This certificate’s tilted squares, folded | The packing it is measured against |
| --- | --- | --- |
| 308 | 102 squares: 17.21° ×2, 17.98° to 18.69° ×58 in six groups, 18.83° ×5, 19.05° to 19.22° ×18, 19.67° ×5, 20.18° ×5, 21.30° to 21.75° ×3, and singles at 3.38°, 4.07°, 15.77°, 23.40°, 27.73°, 28.24° | T-141: 112 squares, 16.65° to 18.70° ×83 in nine groups, 20.16° to 20.26° ×18, 20.93° ×2, 21.67° ×2, 25.32°, 28.11° ×2, and four below 3.6°; T-136 at 307: 103 squares, 17.82° to 20.94° ×92, 22.21° to 28.72° ×8, and three below 6° |
| 154 | 38 squares above 1°: 26.5322° ×10, 26.66° to 26.84° ×3, 28.70°, 37.51° ×2, 37.94° ×4, 38.08° to 38.13° ×3, 39.41° ×2, 40.07° ×6, 40.18°, 42.67° ×2, 44.23° ×4; four within 0.86° of upright | T-182: 40 squares above 1°: 26.530° ×11, 24.36°, 24.58°, 28.85° ×3, 37.96° ×5, 38.08° ×2, 38.52°, 40.65° ×5, 42.93° ×9, 44.43°, 3.47°; three near upright |

So the measurements bear out each issue’s description, in the record’s terms.
#689’s 308 is not a refinement of #489’s packing, as the issue says, and is another
arrangement of the design that #484, #489 and #481’s 307 share: by pose it is nearer to
the case’s house than #659’s 236 was to its (10 squares beyond a tenth), and further
than #664’s 271 (3). Its lineage, from #481’s 307 by one insertion and the explorer, is
the source’s account, which the measurement does not contradict: that 307 packing lies
within a tenth of it at 263 squares.
#694’s 154 is Couzo’s #586 arrangement with three squares moved beyond a tenth, as
#664’s 271 was Couzo’s #561 arrangement with three; the issue calls it a different KKT
point in #586’s family and credits #586’s arrangement, which is right, and T-222 lists
no `regularizations`, rightly.
Ostashev’s 156 packing is not near it by pose; the issue credits it as the chained
explorer’s start, which the record should keep in the source’s voice (RW-2). The
source’s own matching at 308 prints 0.706 where the certificates measure 0.708 here, the
views and the matching differing a little, and nothing turns on it.

## Findings

Graded blocking, major, minor or note, each with the file and line it concerns.
None is blocking and none is major.

**RW-1, minor: T-221’s claim and notes carry no pose measurement against the house.**
`packing/frontier/results.yaml`, T-221’s `claim` (line 30165: “says it is not a
refinement of #489: 295 load-bearing squares move by more than 1e-4 under its matching
and no tilt angle is shared”) and `notes` (line 30214) state the source’s comparison
only, and the case record’s pending paragraph (`packing/frontier/n-308.md` lines 179 to
192\) says “No measured packing identity or lineage is asserted here.”
The measurement is now made ([Credit and Lineage](#credit-and-lineage)): under a quarter
turn 293 of 308 squares lie within a tenth of the house’s packing and 15 move beyond it,
at most 0.708, with 111 squares turned beyond 0.01° and no tilt group shared exactly.
The notes should state it with this review as `measured_in`, and the headline (“started
from Chaoweeraprasit’s 307 packing”) should keep the start in the source’s voice while
the claim says, in the record’s voice, that the packing is another arrangement of the
two-wedge design the house holds, found from #481’s 307 as the source describes.
The credit is as the entry states it, Daniel after Chaoweeraprasit; whether Kevin Fang’s
#484 construction, which the issue names as the design’s family and which the owner’s
bead `think-a95t` considers for the old house, belongs in the new house’s credit
sentence is the owner’s decision under that bead, which the adoption should put to it
rather than decide.

**RW-2, minor: T-222’s credit to Ostashev should say what it rests on.**
`packing/frontier/results.yaml`, T-222’s `claim` (line 30237: “whose chained explorer
removed two squares from the register’s s(156) packing (Daniil Ostashev’s) … the issue
asks that #586’s arrangement … and Ostashev’s s(156) packing be credited as its
starts”), its `notes` (line 30287) and `packing/resources/bibliography.yaml` line 2992,
`credit: Daniel after Couzo, Ostashev, Levy`. By pose the packing is #586’s arrangement
with three squares moved beyond a tenth, and Ostashev’s 156 packing lies within a tenth
of it at 94 of 156 squares.
The claim is honest as written, since it reports what the issue asks; the notes should
add the measurement, citing this review, and say that Ostashev’s credit rests on the
source’s account of the search while Couzo’s rests on the measured arrangement.
The register’s “Levy” in the bibliography string is the project-lineage convention the
19 October review discussed (RV-3) and the claim sentences, rightly, do not repeat it.

**RW-3, minor: both entries’ `controls` name the general test only.**
`packing/frontier/results.yaml` lines 30212 to 30213 (T-221) and 30285 to 30286 (T-222),
`controls: [packing/tests/test_upper_bound_reports.py]`. T-220’s entry, registered the
day before, names the general test and its packet’s receipt; the 19 October review
(RV-1) asked that each import’s particular tests be in a file of their own and cited.
That file exists here, `packing/tests/test_upper_bound_reports_689_694.py` (its
docstring cites RV-1), and holds the construction, the margins and the house readers;
neither entry cites it, and neither cites its receipt.
Both should, as T-220 does.

**RW-4, note: the two views’ `by` fields differ.**
`packing/resources/web/evand-n308-2026-10-19/README.md` lines 57 to 58 (`"by": []`) and
`packing/resources/web/evand-n154-sweep-2026-10-20/README.md` lines 61 to 65
(`"by": ["Francisco Couzo"]`, “retained as the source wrote it”). The 19 October review
asked the author whether the field was the regularizer’s default (RV-7); an empty field
at 308 says it is not simply a default, and the name at 154 may be deliberate, since the
issue credits #586’s arrangement.
Question 1 under [For the Author](#for-the-author) asks; the record should read the
field neither way until answered.

**RW-5, note: this review’s decisions are kept but cited by nothing.** As RV-6 of the 19
October review found for its own, the third route, the area route and the view decisions
are kept in the n308 packet’s
[`review/review-2026-10-20/`](../../../packing/resources/web/evand-n308-2026-10-19/review/review-2026-10-20/README.md),
with every log and report they wrote, but no evidence entry cites them, and
`third_route_1020.py` is in no `verifiers.yaml` entry.
The confirming evidence rests on the maintained replay, which needs nothing more.
The records lane can make the area route’s decision citable by adding the two packets’
keys and rosters to `devtools.check_half_angle_area` with tests and running it with
`--receipts`; until then the confirming evidence should not list
V-check-half-angle-area.

**RW-6, note: a re-housed count owes its regularization runs, and the case records
differ in what they say meanwhile.**
[The House Rule](../../../packing/campaign/result-import.md#the-house-rule) makes the
pull request that adopts a house run both strong generators on each count it re-houses,
here 154 and 308. The source’s same-side views (29 and 10 angle groups), valid here, are
display views at the house’s side, not candidates below it.
The branch gives `packing/frontier/n-308.md` a pending-adoption paragraph (lines 179 to
192\) and `packing/frontier/n-154.md` none, by the 154 packet’s choice (“the case record
at 154 is the adoption writer’s”); the adoption rewrites both, and the 19 October
adoption marked such paragraphs as history afterwards (#692, A1), so nothing is wrong,
but the two cases should read alike when the adoption lands.

## Rungs

**`V3`/`C3` for both entries.** Machine-replayed here: each certificate the entries cite
and its two kernel controls on both maintained routes, with certificates, replay
commands, passing replays and the retained receipts, the controls held by the tests the
branch adds; reviewed adversarially here.
Beside the rung, by the kept programs that no evidence entry cites (RW-5): each
certificate with six controls on this review’s route and on the area route, the views on
this review’s route, each certificate held to its KKT point, and each retained file held
to its upstream bytes.
`V` is the strongest verification anywhere, the record’s replay being `V3`’s predicate
for exact-algebraic evidence of any origin.
`C3`’s named control is held by `test_upper_bound_reports.py` (the receipt’s refused
controls) and `test_upper_bound_reports_689_694.py` (the margins), which RW-3 asks the
entries to cite. Not `V4`/`C4`: one AI review, no human oversight record.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

| Entry | Verdict | Blocking findings | Confirming evidence entry to write | Adoption |
| --- | --- | --- | --- | --- |
| #689 (T-221 on the records branch) | accepted; `V3`/`C3` supported | no | `E-evand-689-n308-exact-feasibility` | the house at 308 |
| #694 (T-222 on the records branch) | accepted; `V3`/`C3` supported | no | `E-evand-694-n154-exact-feasibility` | the house at 154 |

**Verdict lines for the records lane.** For each entry, a confirming evidence entry as
tabled, modelled on `E-evand-664-n271-exact-feasibility`: `assurance: verified`,
`method: exact-algebraic`, `performed_by: repository`, `origin: replayed-here`,
`relationship_to_generator: independent-implementation`, the packet’s certificate, the
`check --replay` command, `replay_status: passed`, the verifiers V-sqpack-verify,
V-check-rational-witness-independent, V-evand-arrangement-receipts,
V-upper-bound-reports and V-evand-exact-certificates (and V-check-half-angle-area only
once RW-5’s roster lands), an `independence` record and this review as
`independence_record` and `external_review` (`informally-verified`). Each `independence`
record has `coverage: full`, one certificate of one;
`read: [specification, certificate-format]`; `clean_room: false`; `shares: []`; and an
`overlaps_producer` of `extent: system-family`, `separate_prompt: true` and
`separate_code: true`, whose note names what each packet’s `CREDITS.md` and pinned
commit state and that V-evand-exact-certificates’ author read the source’s checkers.
On each reported entry, `external_review` naming this review; on each register entry,
the evidence, the rungs, a `reviews` item (`kind: adversarial`, `reviewer_kind: ai`,
`relation: project`, `verdict: accepted`), `controls` naming both tests and the receipt
(RW-3), and claim, notes and `next_rung` rewritten together.

## Significance

| Entry | Draft | Here | Why |
| --- | --- | --- | --- |
| #689 (T-221) | `S3` | `S3` | another arrangement of the two-wedge design at 308, $1.12 \times 10^{-3}$ below the case and every report there, to a new KKT point with 15 squares moved beyond a tenth and eight fewer tilted squares; as #659’s 236 ($2.02 \times 10^{-3}$, 10 squares) is; well above T-188’s $9.29 \times 10^{-6}$ (`S2`) |
| #694 (T-222) | `S3` | `S3` | #586’s arrangement continued to a new KKT point $1.06 \times 10^{-4}$ below the case, three squares beyond a tenth; as #664’s 271 ($4.46 \times 10^{-5}$, three squares, `S3`) and T-172’s $6.66 \times 10^{-5}$ at this count are; the nearer call of the two, and the source’s inconclusive second-order status bears on the minimum, not on the bound |

`by` should name this review.

## Adoption per Count

Each comparison exact, sides rounded up at sixteen places, every side re-read from
retained bytes by `adoption_1020.py`: the case ceiling from each case record’s front
matter and from the house witness, which agree; T-141, T-135, T-182, T-172 and T-160
from their certificates’ headers; #593 from Mishapolk’s facts at 154 and 308. Each
packet’s frozen claim record, which `check-claims` rebuilt equal here, states these
sides and differences exactly.
Each recommended house is the smallest exact certificate at its count, replayed on both
maintained routes and on two more here with no blocking defect, and below the case.
No other report at these counts is smaller: Mykhailo Polkovskyi’s #593 states
certificates at 154 and 308 equal to T-172’s and T-141’s sides, and no open report
through #698 states a bound at either count.

| n | Case ceiling, house | Reviewed and pending certificates, smallest first | House |
| --- | --- | --- | --- |
| 154 | 12.9212065771326311, T-186 | #694 12.9211009407616806, below the case by $1.0564 \times 10^{-4}$; T-186 and T-182 equal at 16 places; T-172 and #593 12.9224998146423975; T-160 12.9225664019340596 | #694’s entry, Daniel after Couzo (#586’s arrangement continued), after Ostashev by the source’s account |
| 308 | 17.9982698795262559, T-174 | #689 17.9971491212709088, below the case by $1.1208 \times 10^{-3}$; T-174, T-141 and #593 equal at 16 places; T-135 17.9993098551627480 | #689’s entry, Daniel after Chaoweeraprasit (RW-1 on the design’s credit) |

The earlier houses stay retained as history, and the reported and verified ceilings move
together. `devtools.select_houses` takes each house once its entry is a candidate:
`V3`/`C3` with an accepted review covering it and a confirming evidence entry whose
scope reaches the count.
Neither entry lists a `regularizations` item, so each house credits its entry, as the
House column does.
The witnesses these houses replace are 926 KB (308) and 64 KB (154) on
the branch; the new certificates are 47 KB and 24 KB as text; the records lane measures
it with `python -m devtools.upper_bound_houses sizes`.

## Proposed Record Changes

For the records lane; this review writes none of them.

- The confirming evidence and register fields under [Rungs](#rungs), for both entries,
  with `controls` naming both tests and each receipt (RW-3).
- Claims, notes and `next_rung`: the measurements of
  [Credit and Lineage](#credit-and-lineage) on both entries, with this review as
  `measured_in` (RW-1, RW-2); the reading of the views’ `by` fields left open (RW-4).
- Significance as tabled, `by` naming this review.
- Houses at both counts of [Adoption per Count](#adoption-per-count), with the
  regularization runs each re-housed count owes and the two case records brought to read
  alike (RW-6), and the question of the design’s credit at 308 put to the owner under
  `think-a95t` (RW-1).
- The area route’s roster and receipts, if the record is to cite it (RW-5).
- For the author, in the replies drafted at stage 7: the questions under
  [For the Author](#for-the-author).

## Programs Run Here

The programs this review wrote are kept, with their logs and reports, in the n308
packet’s
[`review/review-2026-10-20/`](../../../packing/resources/web/evand-n308-2026-10-19/review/review-2026-10-20/README.md),
whose README says how to run each one, what it read and what it printed.
They run only this repository’s maintained tools and code written for this review, read
the sources as data, and write nothing in the repository outside that directory.

- **`custody_1020.py`** made one blobless clone of the source over HTTPS and held the
  trees, the manifests, the `pinned_only` entries, the retained files, the issue-printed
  digests and the default branch’s history of each certificate path to the packets’
  acquisition records.
- **`third_route_1020.py`** is this review’s exact route; **`area_route_1020.py`** runs
  `devtools.check_half_angle_area`’s `verdict` on the two certificates.
- **`construction_1020.py`** holds each certificate to its KKT point at $1 + 10^{-20}$
  and decides the two views on the third route.
- **`lineage_1020.py`** makes the measurements of
  [Credit and Lineage](#credit-and-lineage); **`adoption_1020.py`** the comparisons of
  [Adoption per Count](#adoption-per-count); **`receipt_totals_1020.py`** sums the
  receipts.
- **`chain_review.sh`**, **`chain_review2.sh`** and **`chain_review3.sh`** ran each
  program niced and logged its UTC start, end, wall and exit status; the maintained
  replays’ log is `outputs/chain_replay.log`.

Three runs stopped on errors in this review’s own report code before writing anything,
and were fixed and run again: `adoption_1020.py` on the case record’s front-matter
indentation, `lineage_1020.py` twice on entries the area module’s reader table does not
name (T-135, T-182), and `area_route_1020.py` on the name of the verdict’s success
field, whose decision was the same both times.
Every first log is kept.

## Earlier Reviews That Touch These Results

Before its findings were written, this review searched the branch for documents naming
#689, #694, T-221 or T-222 and found, besides the packets, the register entries and the
rendered register, none: no earlier review, audit or handoff on the branch touches these
results. It read the 19 October review of #659 to #674 before writing, as the precedent
whose form and controls it follows, and discloses that; that review covers none of these
certificates. The bead `think-a95t` (the owner’s pending decision on Kevin Fang’s
structured credit at 308 after #673) was read as data for RW-1; it concerns the old
house, and its outcome bears on the new house’s credit sentence only as RW-1 says.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty or priority; no run of any
source’s checker, solver, regularizer, explorer or morph walk; no decision of the KKT
points, the binary64 inputs or the source’s numerical and contact-graph reports; no
measurement of the source’s search history; no evidence entry for the kept third-route,
area-route and view decisions (RW-5); no house adoption or case-record change.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
