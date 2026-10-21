# Review: Evan Daniel’s Upper-Bound Import at 270 (#703, T-224, PR #708)

**Date:** 21 October 2026. **Verdict: accepted, for finite feasibility only.** The
rational certificate that T-224 cites proves the upper bound its entry states, s(270) ≤
16928162252196750114897964982713/10^30 = 16.928162252196750114897964982713, which PR
#708 (head `0a86f70c3`, merge base `e7de85ff6`) registers at V0/C0. The retained receipt
reproduces here on both maintained routes; a standard-library exact checker written for
this review decides the certificate again (containment of every corner in the closed
box, all 36,315 pairs by separating axes, the 590 pairs within √2 again by exact
clipping area) and agrees with both routes digit for digit on the side, the least wall
clearance, the least pair gap, the closest pair and the pair count.
Four sharp controls at 10^-30 bracket both routes in both directions through the
`evand-cert` adapter, and two format controls behave as documented.
The certificate is exactly the source’s construction: its 80-digit KKT point scaled by 1
\+ 10^-20, every centre and tangent as that construction makes them.
Against every result registered at 270 the certificate is the smallest, below the house
best packing T-174 by 3.4741132266…×10^-5 exactly as the frozen record states.
Measured square by square, the packing is another arrangement of the design the house
best packing holds, found from Chaoweeraprasit’s #500 packing as the source says: under
the identity, one to one, 255 of 270 squares lie within a tenth of T-174’s (which is
#500’s packing to 10^-31) and 15 move beyond it, at most 0.224; it is not a refinement
in the record’s sense.
Five findings, none blocking and none major.
T-224 can take `V3`/`C3` with a confirming evidence entry and this review; the draft
`S3` stands; the house best packing at 270 should move to T-224. Not `V4`/`C4` from this
review alone.

This is the stage 4 review lane of the 21 October intake
([result-import.md](../../../packing/campaign/result-import.md#stage-4-validate)) for
the import bead `think-a9jp`, written by an AI agent (Claude, strong tier, maximum
reasoning) prompted separately from the import and records lanes, with no shared context
beyond the committed packet, register entry and branch.
Its relation to the result is `project`. It is read-only: it moves no rung, writes no
register row and changes no case record; it says what the records lane should write.

## For the Author

Evan Daniel: your `s270_sw.cert` was decided again here from the bytes this repository
keeps, fetched again from `evand/square-packing` at `88385ab` and found at the digest
your issue prints. Both maintained routes decided it and agreed with the import lane’s
receipt job for job; a checker written for this review decided it a third way, with
controls. It is accepted as a finite upper bound at its exact side.
Nothing here bears on optimality, local minimality or rigidity: your KKT, second-order
and MILP statements stay yours, as you present them.

Measured square by square against the register’s packing (T-174, PingYou’s certificate
refinement of your start, #500’s packing, which moves no square by more than 10^-30),
the best one-to-one assignment is the identity symmetry of the box: 255 of 270 squares
within a tenth, 15 beyond it (at most 0.224), 65 beyond 0.01, 56 squares turned by more
than 0.01° (at most 31.6°). Your issue reports 0.391, 17 and 59 on the regularized
views’ load-bearing squares.
In the record’s terms the packing is another arrangement of the design the house best
packing holds, not a refinement of it, found from #500’s packing as you describe, with
the credit you asked for.

Two questions:

1. Your matching reports a largest move of 0.391 with 17 squares beyond 0.1; on the
   certificates under the identity the largest move is 0.224 with 15 beyond 0.1, and no
   other box symmetry pairs the squares one to one.
   Does your 0.391 come from the rattler, or from a matching on a different set of
   squares?
2. The certificate’s square 82, at the origin corner, is tilted 0.2175° and is the one
   square your regularized view turns upright (269 of 270 tangents are identical; the
   view is the certificate under a reflection with that square set to t = 0). Is that
   square the one rattler your report counts?

## Claims Covered

| Entry | Issue and pin in `evand/square-packing` | n | Certificate kept |
| --- | --- | --- | --- |
| T-224 (PR #708) | #703, `88385abc95ab25d520302282d1946cbb07bc9cf3` | 270 | `s270_sw.cert` (SHA-256 `a01114af…`), retained under MIT, with its KKT point, binary64 input, solver report, prior summary, comparison, and the same-side `s270_sw_regularized.cert` (`776433d8…`) |

| n | Exact side | Issue prints | Rounded up at 16 places |
| --- | --- | --- | --- |
| 270 | 16928162252196750114897964982713/10^30 = 16.928162252196750114897964982713 | 16.928162252197 | 16.9281622521967502 |

The claim states its side exactly as the certificate’s header does; the issue’s print is
the side rounded up at twelve places and the packet’s `ceiling` the side rounded up at
sixteen (`review_708_check.py` computes both).
The regularized view states the same packing at the same side for display and is decided
here too; the KKT point and the binary64 input are what the certificate was made from;
the solver, prior and comparison reports are the source’s numerical statements, read as
data.

## Replays Reproduced Here

Run from `packing/` with the project interpreter (Python 3.14.7) in a worktree at
`0a86f70c3`, niced, on a four-core host shared with other lanes.
The retained receipt (`receipts/exact-certification.json.xz`, format
`evand-703-exact-replay-v1`) holds three jobs, each decided by both routes: the positive
passes both (`verification_passed:
true`, 36,315 pairs each); the duplicate-square control is refused by both (`squares 0
and 1 overlap`; `1 overlapping pairs; worst exact gap -1`); the translated-square
control is refused by both (`square 0 violates x<=s`; `container penetration
-3.99…`). The three jobs’ 217,890 pair decisions are 36,315 × 2 routes × 3 jobs, as the
packet counts; 26.65 route CPU seconds summed.

Both routes state the same margins for the positive: least wall clearance
`1/200000000000000000000` = 5×10^-21 exactly, least pair gap
`326977500424421726639659470647872033976162222194784412488318157416719240490668134461/326977500424422112934719589955152273188932133102127238938336418955664500000…`
(84 and 104 digits) = 9.999999999999989×10^-21.

The branch’s tests hold the packet: `test_upper_bound_reports.py` lists it in `EVERY`,
and `test_upper_bound_reports_703.py` holds the issue’s two digests, the side’s
construction from the KKT point at 1 + 10^-20 rounded up at 30 places, the margin below
T-174 bracketed in units of 10^-12, that every report at 270 is above, and the replay’s
clearances. The 69 tests selected by those names pass here, 35.5 s at 02:53:30Z. Hosted
`packing-required`, `pages-required`, `pdf`, `frontend`, `macos-portability` and
`measure-verifier` are all successful on `0a86f70c3`.

## The Review’s Route

`review_708_check.py`, written for this review, uses the standard library only, imports
nothing from this repository, and reads the `evand-cert` text with a reader of its own
that admits only integer and `p/q` literals and refuses a file with other than n rows.
For every square it holds the half-angle map to the unit circle (c² + s² = 1 exactly)
and every corner to the closed box [0, S]², agreeing with the half-extent test.
Every one of the 36,315 pairs is decided by separating axes on the four face normals,
contact allowed; every pair whose centres are within √2 (590) is decided a second way,
the exact area of one closed square clipped by the other’s four closed half-planes,
which must be 0.

| Certificate | Outcome | Wall (square) | Gap (pair) | Pairs (clipped) | CPU |
| --- | --- | --- | --- | --- | --- |
| `s270_sw.cert` | passed, no overlap, no nonzero clipped area | 5×10^-21 exactly (15, at the near wall y = 0) | 9.999999999999989×10^-21 (41, 56), along a face normal of 41, the two squares at one tilt | 36,315 (590) | 4.3 s |
| `s270_sw_regularized.cert` | passed likewise | 5×10^-21 (15) | the same gap at (41, 56) | 36,315 (590) | 4.0 s |

The side, the least wall clearance, the least gap, the closest pair and the pair count
equal both maintained routes’ receipt digit for digit (`out-check.json`,
`agrees_with_receipt: true`). The view has 203 upright squares to the certificate’s 202
and 21 distinct tangents to its 22; against the certificate it is one to one under a
reflection with no square moved beyond 10^-9 (largest 9.4×10^-16, the regularizer’s
re-solve) and one square turned, square 82 (`out-view.json`).

### Sharp controls

`sharp_controls_708.py` makes mutants of the certificate’s bytes at the scale of its
margins and passes each through the `evand-cert` adapter to both maintained routes
(`out-controls-n270.json`), as the 704 review’s controls did:

| Control | Required | `exact_verify` | `independent` | Review checker |
| --- | --- | --- | --- | --- |
| W1: side lowered by exactly the least wall clearance, 5×10^-21 | pass | passed, wall +4.88×10^-31 | passed, the same | — |
| W2: and 10^-30 further | refuse | refused, wall −5.12×10^-31, `square 216 violates x<=s` | refused, `container penetration -3199/6.25·10^33` | — |
| P1: square 56 moved toward 41 along the separating axis by exactly the gap | pass | passed, gap 0 | passed, gap 0 | gap 0, clipped area 0 |
| P2: and 10^-30 further | refuse | refused, gap −10^-30, `squares 41 and 56 overlap` | refused, `worst exact gap -1/10^30` | gap −10^-30, clipped area 8.42×10^-31 |
| F1: a plain decimal literal in a coordinate | — | accepted by the adapter, read as that exact decimal rational |  |  |
| F2: 269 rows for n = 270 | refuse | refused, `269 square rows for n = 270` |  |  |

W1 does not reach contact because the least clearance is square 15’s against the near
wall y = 0, which lowering the side leaves alone; the far wall’s nearest square, 216, is
4.88×10^-31 further off, the side’s rounding above S*(1 + 10^-20), so W1 and W2 bracket
the far wall within 10^-30 in both directions.
P1 and P2 bracket the closest pair at contact exactly.
Both routes are exact at 10^-30 in both directions.

The packet’s own two controls are gross (gap −1; wall about −18); they prove the routes
refuse, not that they refuse at the margin.
The sharp controls above do the latter (finding A2).

## From Certificate to Bound

The argument is the one the
[20 October review](review-2026-10-20-upper-bound-imports-689-694.md#from-certificate-to-bound)
gives and is not repeated in full.
Row k places the closed unit square Q_k = (x_k, y_k) + R_k[−½, ½]² with (c_k, s_k) = ((1
− t_k²)/(1 + t_k²), 2t_k/(1 + t_k²)), on the unit circle identically for rational t. The
box is convex, so containment is containment of the four corners; disjoint interiors are
decided pair by pair by separating axes (both maintained routes, the source’s
`verify_cert.py`, and this review’s route) and again by zero clipped area (this review’s
route, the method of the registered V-check-half-angle-area).
n unit squares with pairwise disjoint interiors in the closed square of side S give s(n)
≤ S. Every route decides in exact rational arithmetic; none rounds, dilates or
tolerates. What every checker assumes: that the literals mean the rationals they write;
that the format means what the source’s `search/exact/README.md` and both checkers say
(centre, lower-left origin, t the tangent of half the rotation); Python’s integers and
`fractions.Fraction`; and the plane-geometry lemma of the pair test.

## How the Certificate Was Made

`construction_708.py` holds the certificate to the construction the source’s
`search/exact/README.md` describes, reading `s270_sw.exact.txt` (`n S*`, then
`x y theta_deg`, 70 digits) with tan at 80 digits (mpmath):

|  | `s270_sw.cert` |
| --- | --- |
| KKT side S* (first 30 digits) | 16.928162252196750114728683360 |
| Side is ⌈S*(1 + 10^-20)·10^30⌉/10^30 | yes, exactly; rounded up by 4.88×10^-31 |
| Side exceeds S* by | 1.69×10^-19 |
| Centres as the scaled KKT centre rounded to 10^-35 | 270 of 270 within 5×10^-36 (largest 4.99×10^-36) |
| Tangents as tan(θ/2) rounded to 10^-35 | 270 of 270 within 10^-35 (largest 4.90×10^-36) |
| Upright squares, t = 0 | 202 |

So the least wall clearance is exactly ε/2 at an upright square whose centre is half a
unit from a wall, as scaling predicts, and the least pair gap is ε times a unit
face-to-face centre distance less the centres’ rounding (1.1×10^-35), which is what all
three routes measure.

## Custody

The pinned commit `88385ab` was read again over the GitHub REST API on 21 October: its
tree is `34fd62e00173b6b9abf84d8368a9edf83e4b6a97` and its committer date
2026-10-20T21:47:03Z, as the packet’s acquisition record states.
The three blobs the claim and its construction rest on (`s270_sw.cert`,
`s270_sw_regularized.cert`, `s270_sw.exact.txt`) were fetched at the pin and are byte
for byte the retained files, at SHA-256 `a01114af…`, `776433d8…` and `0234b886…`; the
first two are the digests the issue prints.
The manifest’s other 17 lines were not fetched again; `acquire_source
--check` holds them to the packet’s record on the branch.

## Trust Boundaries

| Route | Decides | Shares with the others |
| --- | --- | --- |
| `exact_verify` (V-sqpack-verify) | unit shape, corners in the box, every pair by exact separating axes | the `evand-cert` adapter, the parse and half-angle map of `devtools.evand_exact_certificates`; `Fraction`; the separating-axis method |
| `independent` (V-check-rational-witness-independent) | the same on rational corners | the same |
| this review’s route (`review_708_check.py`) | own reader; unit circle; corners in the closed box and half-extent; all pairs by separating axes; near pairs again by exact clipped area | `Fraction` and the format’s meaning; its pair tests are the methods of the source’s first checker and of V-check-half-angle-area, in code of its own |

No source program ran.
The source reports that `verify_cert.py` and `verify_cert2.py` accept the certificate;
both are pinned by digest as copies of the n183 packet’s and were not read for this
review (the 20 October review read them, after writing its route).
The review lane, the import lane, the maintained routes and the source’s assistant are
one AI system family: the packet’s `CREDITS.md` says the source’s work was produced by
Claude (Anthropic) under human direction, and the pinned commit names Claude Opus 5.5 as
co-author with Evan Daniel’s approval.

## Margins at 270

`margins_708.py` rebuilds every registered side at 270 from its own retained packet
through the importer’s house readers (T-056 from Couzo’s decimal print, as the record
reads it), compares each exactly, and rebuilds the frozen `claims.json` differences, all
13 equal (`out-margins.json`).

| Entry | Holder | Side, rounded up at 16 places | Above this certificate by |
| --- | --- | --- | --- |
| **T-224 (#703)** | Daniel | **16.9281622521967502** | — |
| T-174, the house best packing | Chaoweeraprasit, improved by PingYou Ltd (PR #574) | 16.9281969933290166 | 3.474113×10^-5 (exactly the frozen difference, 0.0000347411322664733798710171…) |
| T-151 (#500) | Chaoweeraprasit | 16.9281969933290166 | 3.474113×10^-5 (T-151 is above T-174 by 1.59×10^-31) |
| T-140 (#488) | Couzo | 16.9297753535413596 | 1.613101×10^-3 |
| T-136 (#481) | Chaoweeraprasit | 16.9297801262411717 | 1.617874×10^-3 |
| T-134 (#476) | Couzo | 16.9367200311210158 | 8.557779×10^-3 |
| T-130 (#460) | Couzo | 16.9367230228761835 | 8.560771×10^-3 |
| T-138 (#470) | Polkovskyi | 16.9367231550380000 | 8.560903×10^-3 |
| T-119 (#399) | Daniel | 16.9378072284460292 | 9.644976×10^-3 |
| T-098 (#375) | Daniel, at Couzo’s packing | 16.9378103293409542 | 9.648077×10^-3 |
| T-056 | Couzo | 16.9378103293906290 | 9.648077×10^-3 |

The pending reports the frozen record names (#593 and Mishapolk’s census at T-174’s
side, 3.474×10^-5; #573 at 1.613×10^-3) are above too, as frozen.
No open report through #708 states a bound at 270 (#702, the same commit’s other
certificate, is at 343). **The smallest packing at 270 is T-224’s, and it should be the
house best packing.**

## Credit and Lineage

`lineage_708.py` measures the certificate against T-174 and T-151 through the area
module’s readers: `arrangement_gap` and `unmoved` (nearest-centre pairing under the
eight box symmetries), and an optimal assignment (least total squared displacement,
scipy in binary64). None decides anything.
The record’s sense of a refinement is a one-to-one pairing in which no square moves
beyond a tenth (T-150, T-152).

| Against | Nearest-centre pairing | Best assignment: moved beyond 10^-4 / 10^-3 / 10^-2 / 10^-1; largest | Turned beyond 0.01° |
| --- | --- | --- | --- |
| T-174, the house best packing | one to one under the identity: 255 within a tenth, 15 beyond; largest 0.224 | the identity: 86 / 81 / 65 / 15; 0.224, 255 within a tenth | 56, at most 31.6° |
| T-151, Chaoweeraprasit’s #500, the start the issue names | the same, exactly | the same | 56 |
| T-174 against T-151 | identity: no square beyond 10^-9; largest 2.2×10^-31 | 0 / 0 / 0 / 0; 0 | 0 |

The tilts say the same: the certificate has 68 squares above 10^-6° (67 load-bearing at
the issue’s 19 angles, 14.1474° ×1 to 43.1392° ×2, grouped here exactly as the issue
lists them, and square 82 at 0.2175°); T-174 has 70 (the issue’s 18 angles and one at
1.4185°). No angle is shared; the nearest are 21.2504° against 21.2224°, 21.4047°
against 21.4296°, 29.9925°–29.9951° against 29.9993°, and 30.7849° against 30.7901°.

So the measurement bears out the issue in the record’s terms: a new KKT point of the
design the house best packing holds, with 15 squares moved beyond a tenth under the
identity, as #689’s 308 was (15 beyond a tenth against its house) and more than #664’s
271 (3). T-174 is #500’s packing to 10^-31, so “found from #500’s packing” and “a
different local minimum from T-174’s” are one statement about one packing, and the
credit the entry states, Daniel after Chaoweeraprasit, is what the measurement says as
well as what the source asks.
The source’s matching (0.391, 17, 59) is on the regularized views’ load-bearing squares
and differs from the certificates’ under the identity (0.224, 15, 65); nothing turns on
it (question 1).

## The Issue’s and the Entry’s Assertions, Mapped

| Assertion | Where | Status here |
| --- | --- | --- |
| s(270) ≤ 16928162252196750114897964982713/10^30 | issue; T-224 claim | **computationally verified**: both maintained routes, this review’s route with clipped areas, sharp controls |
| The issue’s print 16.928162252197 is the side rounded up at 12 places | issue; claims.json | computationally verified |
| The two digests the issue prints | issue; packet README | computationally verified, against the retained bytes and the upstream blobs at the pin |
| `verify_cert.py` and `verify_cert2.py` accept it | issue | asserted but unverified (not run here; the methods are reproduced in code of this repository’s and this review’s) |
| The certificate is the KKT point scaled by 1 + 10^-20, centres and tangents rounded at 35 places | source README | computationally verified (construction table) |
| Below T-174 by 3.47×10^-5 and below every report at 270 | issue; T-224 notes; claims.json | computationally verified, exactly, from each packet |
| Best public before it is the register’s (T-174) | issue | best known: no open report through #708 at 270 is smaller; Couzo’s and Mishapolk’s stated sides are T-174’s |
| KKT point, local minimum strict modulo 23 exact flat motions, not isolated, 113 + 1,524 contact equations, 263 corner–corner contacts, no MILP descent, 1 rattler, 67 tilted | issue; T-224 claim | asserted but unverified (the source’s numerical evidence at 80 digits; not replayed) |
| 67 load-bearing tilted squares at the 19 listed angles | issue | computationally verified as the certificate’s tilt groups (68 with the 0.2175° square); “load-bearing” is the source’s |
| A different local minimum from the register’s packing; exact sides differ by 3.47×10^-5; no tilt angle shared | issue; T-224 claim | the side difference and the unshared tilts verified; “different local minimum” is the source’s; by pose, another arrangement with 15 squares beyond a tenth (verified) |
| Contact graphs share 514 pairs with 49 only in each; 0 of 1 rattlers shared | issue; T-224 claim | asserted but unverified (contact graphs not built here) |
| Under its matching the largest move is 0.391, 17 beyond 0.1, 59 beyond 0.01 | issue; T-224 claim | asserted; measured here as 0.224, 15 and 65 on the certificates under the identity (question 1) |
| The regularized view is the same packing at the same side, 21 angle groups from 22 | issue; packet README | computationally verified: same side, passes, 269 of 270 tangents identical, 22 and 21 distinct tangents |
| Found by the basin explorer from #500’s packing: eight generations stored, a near-record sweep over 1,069 stored 270s, 24 starts, four 40-minute runs, five moves | issue; T-224 claim | asserted but unverified (the source’s account of the search; consistent with the pose measurement) |
| Credit: Evan Daniel, with #500’s packing as the ultimate start | issue; T-224 claim; bibliography | the record’s decision; the measurement supports it |
| Claude assisted under Evan Daniel’s direction | CREDITS.md; pinned commit | asserted by the source; recorded |
| Replay: 3 jobs, 217,890 pair decisions, 26.65 route CPU s, walls ≥ 5.00×10^-21, pairs ≥ 9.99×10^-21 | T-224 notes; evidence limitations | computationally verified: the receipt reproduces; the margins are the same to every digit |

## Findings

Graded blocking, major, minor or note, each with the file and line it concerns, on the
branch at `0a86f70c3`. None is blocking and none is major.

**A1, minor: T-224’s `controls` names the general test only.**
`packing/frontier/results.yaml` lines 30553 to 30554, `controls:
[packing/tests/test_upper_bound_reports.py]`. The packet’s particular tests are in
`packing/tests/test_upper_bound_reports_703.py` (the digests, the construction, the
margins and the clearances) and its refused controls in
`receipts/exact-certification.json.xz`; neither is cited, as RW-3 of the 20 October
review found for T-221 and T-222. The entry should cite both, as T-220 does.

**A2, minor: the kernel’s two controls are gross, and the record should say so.**
`packing/devtools/evand_arrangement_reports.py` lines 238 to 243 (a duplicated square,
gap −1; a square moved S + 2 outside) and `packing/frontier/evidence.yaml` line 39166
(`limitations`), which describes them as “passed their required outcomes”.
Every margin of the certificate is 10^-20 or less, so a tolerant checker would pass the
packet as retained. The sharp controls here show both routes exact at 10^-30 in both
directions (wall and pair); `limitations` should say the kernel’s controls are gross and
cite this review’s once retained.
The durable fix, a contact-plus-ε job in `JOBS`, was asked for by the 10 October review
(RD-2), the #678 review (RF-2) and the #704 review (A2).

**A3, minor: the claim and notes carry no pose measurement against the house best
packing.** `packing/frontier/results.yaml` line 30504 (`claim`: “under its matching the
largest square move is 0.391, with 17 squares moving by more than 0.1”) and line 30555
(`notes`), and the packet README lines 122 to 142 (“no identity or lineage is measured
here”). The measurement is now made ([Credit and Lineage](#credit-and-lineage)): under
the identity 255 of 270 squares lie within a tenth of T-174’s packing and 15 move beyond
it, at most 0.224, 56 turned beyond 0.01°, no tilt angle shared; T-174 is #500’s packing
to 10^-31. The notes should state it with this review as `measured_in`, keeping the
source’s 0.391/17/59 in the source’s voice, and the claim should say, in the record’s
voice, that the packing is another arrangement of the design the house best packing
holds, not a refinement, found from #500’s packing as the source describes.

**A4, note: the `evand-cert` adapter accepts a plain decimal literal.**
`packing/devtools/evand_exact_certificates.py` line 158 (`_RATIONAL`, which admits
`-?\d+(?:/[1-9]\d*|\.\d+)?`) and line 198. Control F1 shows a coordinate written as a
decimal is accepted and read as that exact decimal rational, which the docstring
documents and which loses no exactness; the retained certificate holds only integer and
`p/q` literals (this review’s reader, which refuses decimals, read it).
Nothing is wrong; the format’s comment line says rational, and the test module could
hold the retained file to the two literal forms so that a decimal in a later import is
noticed.

**A5, note: this review’s decisions are kept but cited by nothing, and the snapshot is
nearly full.** The checker, the sharp controls, the construction, the margins and the
lineage programs, with their JSON outputs and timings, are in `review708/` beside this
document, 55.7 kB of programs and outputs after the decompressed receipt and the
upstream copies are dropped (27 kB of it the five programs).
PR #708’s body reports 56,830 bytes of headroom under the negative-control snapshot cap.
The records lane should retain them under the packet’s `review/` as the n308 packet
does, compressed with xz where the cap requires, or prune `out-lineage.json` (15 kB) to
its summary; until retained and named in `verifiers.yaml` they decide nothing for the
record (RW-5 of the 20 October review), and the confirming evidence should not list
V-check-half-angle-area.

## Rungs

**`V3`/`C3` for T-224.** Machine-replayed here: the certificate and its two kernel
controls on both maintained routes, with the certificate, replay commands, passing
replays and the retained receipt, the controls held by the branch’s tests; reviewed
adversarially here with a third route and sharp controls.
`C3`’s named control is held by `test_upper_bound_reports.py` (the receipt’s refused
controls) and `test_upper_bound_reports_703.py` (the margins), which A1 asks the entry
to cite. Not `V4`/`C4`: one AI review, no human oversight record.
No lower bound, optimum, local minimum, rigidity, novelty or priority follows.

**Verdict lines for the records lane.** A confirming evidence entry
`E-evand-703-n270-exact-feasibility` modelled on `E-evand-694-n154-exact-feasibility`:
`assurance: verified`, `method: exact-algebraic`, `performed_by: repository`, `origin:
replayed-here`, `relationship_to_generator: independent-implementation`, the packet’s
certificate, the `check --replay` command, `replay_status: passed`, the verifiers
V-sqpack-verify, V-check-rational-witness-independent, V-evand-arrangement-receipts,
V-upper-bound-reports and V-evand-exact-certificates, an `independence` record
(`coverage: full`, one of one; `read: [specification, certificate-format]`;
`clean_room: false`; `shares: []`; `overlaps_producer` of `extent: system-family`,
`separate_prompt: true`, `separate_code: true`, noting `CREDITS.md`, the pinned commit
and that V-evand-exact-certificates’ author read the source’s checkers) and this review
as `independence_record` and `external_review` (`informally-verified`). On T-224: the
evidence, `V3`/`C3`, a `reviews` item (`kind: adversarial`, `reviewer_kind: ai`,
`relation: project`, `verdict: accepted`, `covers: [T-224]`), `controls` naming both
tests and the receipt (A1), and claim, notes and `next_rung` rewritten together (A3).

## Significance

| Entry | Draft | Here | Why |
| --- | --- | --- | --- |
| T-224 | `S3` | `S3` | another arrangement of the design at 270, 3.47×10^-5 below the case and every report there, to a new KKT point with 15 squares moved beyond a tenth, two fewer tilted squares and no tilt angle shared; between #664’s 271 (4.46×10^-5, three squares, `S3`) and #689’s 308 (1.12×10^-3, 15 squares, `S3`), and well above T-188’s 9.29×10^-6 (`S2`) |

`by` should name this review.

## Adoption at 270

T-224’s certificate is the smallest exact certificate at 270, replayed on both
maintained routes and on this review’s with no blocking defect, below the case ceiling
(T-174, 16.9281969933290166) by 3.474113×10^-5. Once T-224 holds `V3`/`C3`, the
confirming evidence and this review with `covers: [T-224]`, `devtools.select_houses`
takes it, and the house best packing at 270 should move from T-174 to T-224, Daniel
after Chaoweeraprasit, with T-174 retained as history and the reported and verified
ceilings moving together.
The pull request that adopts it owes the count both strong generators’ runs under the
house rule; the source’s same-side view (21 angle groups) is a display view at the
house’s side, not a candidate below it.
T-224 lists no `regularizations` item, rightly.

## Proposed Record Changes

For the records lane; this review writes none of them: the confirming evidence and
register fields under [Rungs](#rungs); `controls` naming both tests and the receipt
(A1); `limitations` on the kernel’s controls (A2); the pose measurement in the claim and
notes with this review as `measured_in` (A3); significance as tabled; the house best
packing at 270 with its regularization runs; this review’s programs retained under the
packet’s `review/` within the snapshot cap (A5); and, for the author at stage 7, the two
questions under [For the Author](#for-the-author).

## Programs Run Here

In `review708/`, retained by the records lane in the n270 packet’s
[`review/review-2026-10-21/`](../../../packing/resources/web/evand-n270-sweep-2026-10-20/review/review-2026-10-21/README.md)
(A5), each run niced from the worktree’s `packing/` with its venv, logged with UTC start
and end (`*.time`):

- **`review_708_check.py`** (`python -I`, standard library): the review’s route;
  `out-check.json` (against the receipt) and `out-check-view.json`; 02:48:12Z to
  02:48:20Z.
- **`sharp_controls_708.py`**: the six controls through the adapter and both routes;
  `out-controls-n270.json`; 02:51:31Z to 02:52:09Z. Its first run
  (`controls-first-run.log`) stopped on a formatting error in this review’s own report
  code after the first control had been decided, and was fixed and run again; the
  decisions were the same.
- **`construction_708.py`**: the certificate against its KKT point;
  `out-construction.json`.
- **`margins_708.py`**: every registered side at 270 from its packet;
  `out-margins.json`. Its first run took T-056’s print as a binary64 value where the
  record takes the decimal; the second takes the decimal, and every row is unchanged but
  that one’s equality with the frozen record.
- **`lineage_708.py`**: the pose measurements; `out-lineage.json`; `out-view.json` is
  the view against the certificate by the same functions.
  02:50:42Z to 02:50:52Z.
- `pytest.log`: the 69 selected tests.

## Earlier Reviews That Touch This Result

The branch holds no earlier review, audit or handoff naming #703 or T-224 besides the
packet, the register entry and the rendered views.
This review read the 20 October review of #689 and #694 and the #704 review before
writing, as the precedents whose form and controls it follows, and discloses that;
neither covers this certificate.

## What This Review Does Not Establish

No optimality, lower bound, local minimum, rigidity, novelty or priority; no run or
reading of the source’s checkers, solver, regularizer, explorer or sweep; no decision of
the KKT point, the binary64 input, the contact graphs or the source’s comparison report;
no re-fetch of the manifest’s other 17 files; no evidence entry for the kept decisions
(A5); no house adoption or case-record change.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
